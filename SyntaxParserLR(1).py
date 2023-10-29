# coding:utf-8
import os
import pickle
from typing import List, Set, Optional, Tuple
from copy import deepcopy
from prettytable import *
from Symbols import *
from LexcialAnalyzer import Scanner
from grammar import grammar, tree_rules
from utils import Production, State, DeterministicFiniteAutomata, Token


class Parser(object):
    terminal = list(Reserved.keys()) + list(Assign.keys()) + list(BinaryOp.keys()) + list(UnaryOp.keys()) + seperator

    def __init__(self):
        self.scanner = Scanner()
        self.production_group = []
        self.terminal_symbol_group = []
        self.left_group = None
        self.state_index_table = {}
        self.terminal_index_table = {}
        self.non_terminal_index_table = {}
        self.ACTION = None
        self.GOTO = None
        self.start_production = None
        self.dfa = DeterministicFiniteAutomata()
        self.Reduce = {}
        self.Shift = {}
        self.first = {}

        # 读取语法
        self.read_grammar()
        # 计算first集
        self.get_first()
        # 创建确定有限自动机(DFA)
        self.build_dfa()
        # 生成预测分析表
        self.generate_table()

    def __call__(self, expression: str):
        tokens = self.scanner(expression)
        root = self.analyse(tokens)
        return root

    def read_grammar(self) -> None:
        """
        读取语法创建产生式。
        """
        self.terminal_symbol_group.append({'class': 'T', 'type': '#'})
        self.left_group = list(grammar.keys())
        for i, ((left, rights), rules) in enumerate(zip(grammar.items(), tree_rules.values())):
            if i == 0:  # 为了添加扩展文法的产生式 S->start
                self.start_production = Production(left, [{'class': 'NT', 'type': rights[0][0]}], rules[0], 1, terminals=['#'])
                self.production_group.append(self.start_production)
            for right, rule in zip(rights, rules):
                temp = []
                for r in right:
                    if r == '$':  # 终结符
                        data = {'class': 'T', 'type': '$'}
                    elif r in seperator:  # 界符
                        data = {'class': 'T', 'name': 'seperator', 'type': r}
                    elif r in list(BinaryOp.keys()) + list(UnaryOp.keys()):  # 运算符
                        data = {'class': 'T', 'name': 'operator', 'type': r}
                    elif r in Assign.keys():  # 赋值
                        data = {'class': 'T', 'name': r, 'type': r}
                    elif r in Reserved.keys():  # 保留字
                        data = {'class': 'T', 'name': r, 'type': Reserved[r]}
                    else:  # 非终结符
                        data = {'class': 'NT', 'type': r}
                    if not (data in self.terminal_symbol_group) and data['class'] != 'NT':
                        self.terminal_symbol_group.append(data)
                    temp.append(data)
                self.production_group.append(Production(left, temp, rule, terminals=['#']))

    def get_first(self) -> None:
        """
        获取各产生式的first集。
        """
        for left, rights in grammar.items():
            if left not in self.first.keys():
                f = set()
                for right in rights:  # [['S', "S'"], ['$']]
                    tmp = self._find_first(left, right)
                    f |= tmp
                self.first[left] = f

    def _find_first(self, left: str, right: List[List[str]]) -> Set[str]:
        """
        递归求解first集。满足四个条件：
        1. 如果X是终结符，则first(X) = { X }。
        2. 如果X是非终结符，且有产生式形如X → a…，则first( X ) = { a }。
        3.  如果X是非终结符，且有产生式形如X → ABCdEF…（A、B、C均属于非终结符且包含 &，d为终结符），
        需要把first( A )、first( B )、first( C )、first( d )加入到 first( X ) 中。
        4. 如果X经过一步或多步推导出空字符$，将$加入first( X )。
        参数：
            left: str
            产生式左部。
            right: List
            产生式右部。
        返回： Set
            当前left的first集。
        """
        if right:
            if right[0] == '$':  # 是第一层同时只有一个终结符$那么直接返回即可
                return {'$'}
            else:
                f = set()
                count = 0  # 为了检测是否满足条件4
                for r in right:  # ['S', "S'"]
                    if left == r:
                        continue
                    if r in self.terminal:  # 例如：*A中*是终结符,这个文法符号串就此终结
                        return f | {r}
                    if r in self.first.keys():  # 如果first集中存在目标产生式的first集就可直接添加
                        # $不在非终结符中
                        if '$' not in self.first[r]:
                            return f | self.first[r]
                    elif r in grammar.keys():  # first集中没有当前r的first集创造一个
                        l = set()
                        for new_rights in grammar[r]:
                            tmp = self._find_first(r, new_rights)
                            l |= tmp
                        self.first[r] = l
                        # ε不在非终结符中
                        if '$' not in l:
                            return f | l
                    else:
                        print('无法识别字符{}'.format(r))
                        raise ValueError('检测语法或者终结符是否存在错误！')

                    # ε在非终结符中
                    tmp = deepcopy(self.first[r])
                    f |= tmp
                    count += 1

                if count != len(right):  # 满足条件3
                    return f
                else:  # 满足条件4
                    return f | {'$'}
        return set()

    def _find_production(self, left: str) -> List[Production]:
        """
        搜索项目集中当前产生式的非终结符的产生式。
        参数：
            left: str
                产生式左部。
        返回： List
            产生式左部的扩展产生式。
        """
        result = []
        for production in self.production_group:
            if production.left == left:
                temp = deepcopy(production)
                result.append(temp.next())  # position向后+1
        return result

    def _expand_production(self, production: Production, inherit: bool) -> List[Production]:
        """
        项目集中的产生式扩展，实现第二个规则。
        2. 若项目[A->a.Bβ, a]属于closure(I)，B->γ是一个产生式，则对于first(βa)中的每个终结符b，加入closure(I)中
        参数：
            production: Production
                当前要被扩展的产生式。
            inherit: bool
                判断是否继承当前产生式的展望符。
        返回： List
            扩展后的产生式。
        """
        right = production.right
        position = production.position
        data = []
        #  首先判断position是不是最后一位，若不是position必须为非终结符
        if position < len(right) + 1 and right[position - 1]['class'] == 'NT':

            # 根据当前产生式右边扩展产生式
            productions = self._find_production(right[position - 1]['type'])
            first = list(self._find_first(production.left, [i['type'] for i in right[position:]]))
            if inherit:
                terminal = list(set(first + deepcopy(production.terminals)))  # 继承展望符
            else:
                terminal = first  # 自生展望符
            for item in productions:
                temp = deepcopy(item)
                temp.terminals = terminal
                if not (temp == production and temp.terminals == production.terminals):
                    data.append(temp)
        return data  # 不满足两个条件直接返回为[]

    def closure(self, productions: List[Production]) -> List[Production]:
        """
        求解项目集闭包
        1. I的任何项目都属于closure(I)；
        2. 若项目[A->a.Bβ, a]属于closure(I)，B->γ是一个产生式，则对于first(βa)中的每个终结符b，加入closure(I)中；
        3. 不断重复(2)直到不再扩大。
        参数：
            productions： List
                当前项目集的原始产生式。
        返回： List
            项目集闭包中所有的产生式。
        """
        cache = [p.item() for p in productions]
        result = [p for p in productions]
        procession = [p for p in productions]
        while len(procession) > 0:
            production = procession.pop()
            # 判断是否继承展望符条件
            if production.right[production.position:]:
                left = production.right[production.position : production.position+1][0]['type']
                if left in self.terminal:  # 后面跟终结符
                    inherit = False
                else:  # 后面不跟终结符
                    if '$' in self.first[left]:
                        inherit = True
                    else:
                        inherit = False
            else:
                inherit = True
            data = self._expand_production(production, inherit)  # 根据规则2，求解当前产生式求解扩展产式
            for item in data:
                if item.item() not in cache:
                    result.append(item)
                    cache.append(item.item())
                else:
                    idx = cache.index(item.item())
                    if item not in result[idx]:
                        result[idx] = result[idx] + item
                #  判断是否还有可扩展的产生式
                if len(item) > item.position - 1 and item.right[0]['class'] == 'NT':
                    procession.append(item)

        return result

    def go(self, I: State, item: Production) -> List[Production]:
        """
        确定自动机的state转移
        J的闭包要遍历I中每个形如[A->a.Xβ,a]的项目，将[A->aX.β,a]的项目加入J。
        参数：
            I: State
                当前DFA的项目集。
            item: Production
                下一个转移的产生式。
        返回： List
            下一个状态的项目集闭包。
        """
        params = []
        for production in I.productions:
            expression = production.right
            position = production.position
            if position < len(expression) + 1:
                node = expression[position - 1]
                if node['type'] == '$':
                    continue
                production = production.next()
                if node == item:
                    params.append(production)

        return self.closure(params)

    def build_dfa(self) -> None:
        """
        创建确定自动机，即求解每一个状态的项目集闭包。
        1. 初始化开始符号的项目集闭包；
        2. 遍历开始的项目集闭包的每一个产生式是否满足GO(I,X)不为空且未在下一个项目集当中；
        3. 不断重复2直到项目集闭包不再增加。
        """
        state_table = {}
        current_state = 0
        states = []
        procession = []

        # 初始化扩展文法的项目集闭包
        I = State('I' + str(current_state))
        I.productions = self.closure([self.start_production])

        state_table[I.name] = str(I)
        procession.append(I)
        self.dfa.add_state(I)
        states.append(I)
        current_state += 1
        while len(procession) > 0:
            I = procession.pop(0)
            items = I.get_item()
            for item in items:
                if item['type'] == '$':
                    continue
                # 下一个可转移的产生式
                productions = self.go(I, item)
                temp = State()
                temp.productions = productions
                if temp in states:
                    temp.name = 'I{}'.format(states.index(temp))
                else:
                    temp.name = 'I{}'.format(current_state)
                string = str(temp)
                if string not in state_table.values():
                    states.append(temp)
                    state_table[temp.name] = string
                    self.dfa.add_state(temp)
                    self.dfa.add_edge(I, item, temp)
                    procession.append(temp)
                    current_state += 1
                else:
                    for state in states:
                        if state_table[state.name] == string:
                            self.dfa.add_edge(I, item, state)
                            break
        return

    def _search_goto_state(self, I: State, target: Production) -> Optional[Production]:
        for _from, item, to in self.dfa.edge:
            if (_from, item) == (I, target):
                return to
        return None

    def _show_conflict(self, state, index, x, y):
        if self.ACTION[x][y] != "" and self.ACTION[x][y] != index:
            print("{}包含shift-reduce冲突".format(state.name))
            print(index, end='->')
            print(self.ACTION[x][y])
            print(str(state))
            print('-------------')

    def generate_table(self):
        """
        生成预测分析表，对于当前状态i来说，
        1. 如果产生式满足[A->a.aβ,b]且GOTO(i,a)是下一个状态j，那么执行移入动作，记为ACTION[i,a]=sj；
        2. 如果产生式满足[A->a.Bβ,b]且GOTO(i,B)是下一个状态j，那么转移到下一个状态，记为GOTO[i,B]=j；
        3. 如果产生式满足[A->a.,a]且A不是开始字符，那么执行归约动作，记为ACTION[i,a]=rj；
        4. 如果产生式满足[S'->S.,#]，其中S'是增广开始字符，那么完成分析工作，记为ACTION[i,#]=acc；
        5. 除此以外的情况都是error。
        """
        production_string_group = deepcopy(self.production_group)
        production_string_group[0].position = 0
        production_string_group = [str(p) for p in self.production_group]
        states, edges = self.dfa.state, self.dfa.edge
        self.state_index_table = {states[i].name: i for i in range(len(states))}
        self.terminal_index_table = {self.terminal_symbol_group[i]["type"]: i for i in range(len(self.terminal_symbol_group))}
        self.non_terminal_index_table = {self.left_group[i]: i for i in range(len(self.left_group))}

        # 初始化ACTION和GOTO表
        self.ACTION = [["" for _ in range(len(self.terminal_symbol_group))] for _ in range(len(states))]
        self.GOTO = [["" for _ in range(len(self.left_group))] for _ in range(len(states))]

        end_production = deepcopy(self.start_production)
        end_production.position += 1
        for state in states:
            x = self.state_index_table[state.name]
            for production in state.productions:
                expression = production.right
                position = production.position
                if position < len(expression) + 1:
                    node = expression[position - 1]
                    if node['class'] == 'T':
                        y = self.terminal_index_table[node["type"]]
                        to = self._search_goto_state(state, node)

                        if node['type'] != '$':  # 移入动作，规则1
                            index = 's' + to.name[1:]
                            self._show_conflict(state, index, x, y)
                            self.ACTION[x][y] = index
                            temp = copy.deepcopy(production)
                            temp.position = 0
                            temp.terminals = tuple('#')
                            self.Shift[index] = temp
                        else:  # 规约动作，规则3
                            for i in range(len(production.terminals)):
                                y = self.terminal_index_table[production.terminals[i]]
                                temp = copy.deepcopy(production)
                                temp.position = 0
                                temp.terminals = tuple('#')
                                index = 'r' + str(production_string_group.index(str(temp)))
                                self._show_conflict(state, index, x, y)
                                self.ACTION[x][y] = index
                                self.Reduce[index] = temp

                elif position == len(expression) + 1:
                    for i in range(len(production.terminals)):
                        y = self.terminal_index_table[production.terminals[i]]
                        temp = deepcopy(production)
                        temp.position = 0
                        temp.terminals = tuple('#')
                        self._show_conflict(state, index, x, y)
                        if str(end_production) == str(production):  # 完成分析，规则4
                            self.ACTION[x][y] = 'acc'
                        else:  # 移入动作，规则1
                            index = 'r' + str(production_string_group.index(str(temp)))
                            self.ACTION[x][y] = index
                        self.Reduce[index] = temp

        for _from, item, to in edges:
            if item['class'] == 'NT':  # 状态转移，规则2
                x = self.state_index_table[_from.name]
                y = self.non_terminal_index_table[item['type']]
                if self.GOTO[x][y] != "" and self.GOTO[x][y] != to.name:
                    print(to.name, end='->')
                    print(self.GOTO[x][y])
                    print('-------------')
                self.GOTO[x][y] = to.name

    def analyse(self, tokens: List[Token]):
        """分析tokens"""
        title = ["步骤", "当前栈", "输入串", "动作", "状态栈", "ACTION", "GOTO"]
        step = 0
        table = PrettyTable(title)

        def _find_state_by_name(name):
            for state in self.dfa.state:
                if state.name == name:
                    return state

        def _show_table(step, Operation, action):
            OpStackColumn = " ".join([x['type'] for x in OpStack])
            tokensColumn = " ".join([x['type'] for x in tokens])
            statestackColumn = " ".join([x.name for x in statestack])
            row = [str(step), OpStackColumn, tokensColumn, Operation, statestackColumn, action, ""]
            table.add_row(row)

        end = Token('T', 'end', '#', '#', None, None)
        OpStack = [end]
        statestack = [self.dfa.state[0]]
        while True:
            current_state = statestack[-1]
            if len(tokens) == 0:
                token = end
            else:
                token = tokens[0]
            x = self.state_index_table[current_state.name]
            y = self.terminal_index_table[token['type']]
            action = self.ACTION[x][y]
            if action == '':  # 报错
                print('error', current_state.name, token)
                print(table)
                raise ValueError('语法错误!')
            if action == 'acc':  # 完成分析
                step += 1
                _show_table(step, "accept", action)
                print(table)
                return res

            elif action[0] == 's':  # 移入
                statestack.append(_find_state_by_name('I' + action[1:]))
                temp = tokens.pop(0)
                OpStack.append(temp)
                step += 1
                _show_table(step, "shift", action)

            elif action[0] == 'r':  # 规约
                production = self.Reduce[action]
                cnt = len(production.right)
                if cnt == 1 and production.right[0]['type'] == '$':
                    des = Token('NT', production.left, production.left, '#', None, None)
                    current_state = statestack[-1]
                    statestack.append(self._search_goto_state(current_state, des))
                    OpStack.append(des)
                    continue

                tree = []
                for i in range(cnt):
                    item = production.right[cnt - i - 1]
                    back = OpStack[-1]
                    if item['class'] != back['class_type'] and item['type'] != back['type']:
                        print("error")
                    else:
                        temp = OpStack.pop(-1)
                        tree.append((temp['name'], temp['type'], temp['data']))
                        statestack.pop(-1)

                # 建树
                res, typ = self._build_tree(tree, production.rules)

                # 准备下一个状态
                current_state = statestack[-1]
                left = production.left
                x = self.state_index_table[current_state.name]
                y = self.non_terminal_index_table[left]
                statestack.append(_find_state_by_name(self.GOTO[x][y]))
                OpStack.append(Token('NT', left, typ, deepcopy(res)))
                step += 1
                temp = deepcopy(production)
                temp.position = 0
                _show_table(step, "reduce({})".format(str(temp)), action)

    def _build_tree(self, tree: List[Tuple], rule: List[str]):
        """创建抽象语法树"""
        if rule[0] == 'change':
            return tree[0][-1], tree[0][-2]

        # 去掉分隔符
        stack = []
        for (name, typ, data), right in zip(tree[::-1], rule):
            if right == 'drop':
                continue
            stack.append((name, typ, data, right))

        # 去掉分割符后再判断是否是change-更换名字
        if stack[0][-1] == 'change':
            return stack[0][-2], stack[0][1]

        # 建树
        if stack[1][2] is '=':  # 赋值
            op = stack[1][1]
            typ = stack[1][2]
            op = Assign[op][typ]
            tree = op(stack[-1][2], name=stack[0][2])
        elif len(stack) == 3:  # 双目
            op = stack[1][1]
            typ = stack[0][1]
            if typ in BinaryOp[op].keys():
                op = BinaryOp[op][typ]
            else:
                typ = stack[-1][1]
                op = BinaryOp[op][typ]
            tree = op(stack[0][2], stack[-1][2])
        elif len(stack) == 2:  # 单目
            op = stack[0][1]
            typ = stack[1][1]
            op = UnaryOp[op][typ]
            tree = op(stack[1][2])

        # TODO: if语句的ast

        return tree, typ

    def save_predict(self):
        """保存预测分析表"""
        import pandas as pd
        action = pd.DataFrame(self.ACTION, columns=list(self.terminal_index_table.keys()))
        goto = pd.DataFrame(self.GOTO, columns=self.left_group)
        predict = pd.concat([action, goto], axis=1)
        predict.to_csv('./predict.csv')

def read(path: str) -> Parser:
    """读取Parser"""
    file = open(path, 'rb')
    parser = pickle.load(file)
    file.close()
    return parser


def save(parser: Parser):
    """保存Parser"""
    file = open('./parser.pkl', 'wb')
    pickle.dump(parser, file, 1)
    file.close()


if __name__ == '__main__':
    reset = False
    path = './parser.pkl'
    if os.path.exists(path) and not reset:
        parser = read(path)
        parser.save_predict()
    else:
        parser = Parser()
        save(parser)
    root = parser('a = 1.1 ≥ 1 == 1 ')
    root.assign()