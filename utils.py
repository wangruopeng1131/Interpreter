from typing import List, Set, Optional, Tuple


class Token(object):
    """
    用来存储字符的信息
    参数：
        class_type: 是否为终结符
        name: 识别的类别
        type: 字符本体
        data: 主要用来存储常数，其他情况下和type一致
        row: 行
        colum: 列
    """
    def __init__(self, class_type: str, name: str, type: str, data: float,
                 row: Optional[int] = None, colum: Optional[int] = None):
        self.class_type = class_type
        self.name = name
        self.type = type
        self.data = data
        self.row = row
        self.colum = colum

    def __str__(self):
        return '{class_type} | ({name}, {type}, {data})'.format(
            class_type=self.class_type,
            name=self.name,
            type=self.type,
            data=self.data
        )

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        return self.__dict__[key]

    def __eq__(self, other):
        pass

    @property
    def position(self) -> Tuple:
        return self.row, self.colum

    @position.setter
    def position(self, value: Tuple):
        self.row, self.colum = value


class Production(object):
    """
    将产生式转化为LR(1)项目，并存储抽象语法树建树规则
    参数：
        left: 产生式左部
        right: 产生式右部
        rules: 抽象语法树建树规则
        position: LR(1)项目当前关注字符
        terminals： LR(1)项目的展望符
    """
    def __init__(self, left, right, rules, position=0, terminals=None):
        self.left = left
        self.right = right
        self.rules = rules
        self.position = position
        self.terminals = terminals

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = self.item()
        result += ',['
        if self.terminals:
            if len(self.terminals) > 0:
                for item in sorted(self.terminals):
                    result += '\''+item+'\''+','
                result = result[:-1]
        result += ']'
        return result

    def __eq__(self, other):
        if other.item() == self.item():
            return True
        return False

    def __add__(self, other):
        """相同产生式合并，只合并展望符"""
        self.terminals += [i for i in other.terminals if i not in self.terminals]
        return self

    def __contains__(self, item):
        """判断两个产生式之间是否是属于关系"""
        for t in item.terminals:
            if t not in self.terminals:
                return False
        return True

    def __len__(self):
        return len(self.right)

    def next(self):
        return Production(self.left,
                          self.right,
                          self.rules,
                          self.position + 1,
                          self.terminals)

    def item(self):
        """不包括展望符的产生式"""
        result = self.left + '->'
        position = 1
        for data in self.right:
            if position == self.position:
                result += '@'
            result += data['type']+' '
            position += 1
        if position == self.position:
            result += '@'
        return result


class State(object):
    def __init__(self, name=None):
        self.name = name
        self.productions = []
        self.string = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        for production in self.productions:
            if str(production) not in self.string:
                self.string.append(str(production))
        return "\n".join(sorted(self.string))

    def __eq__(self, other):
        if str(other) == self.__str__():
            return True
        return False

    def items(self):
        p = []
        for production in self.productions:
            p.append('->'.join([production.left, '|'.join([i['type'] for i in production.right])]))
        return p

    def get_item(self):
        result = []
        for production in self.productions:
            expression = production.right
            position = production.position
            if position < len(expression) + 1:
                node = expression[position - 1]
                if node not in result:
                    result.append(node)
        return result


class DeterministicFiniteAutomata(object):
    def __init__(self):
        self.state = []
        self.edge = []

    def add_state(self, ix: Production):
        self.state.append(ix)

    def add_edge(self, ia: Production, t: str, ib: Production):
        self.edge.append((ia, t, ib))

# def print_table():
#     title = [""]
#     for i in range(len(terminal_symbol_group)):
#         title.append(terminal_symbol_group[i]['type'])
#     for i in range(len(left_group)):
#         title.append(left_group[i])
#     title.sort()
#     x = PrettyTable(title)
#     for i in range(len(dfa.state)):
#         row = [dfa.state[i].name]
#         for j in range(len(terminal_symbol_group)):
#             row.append(ACTION[i][j])
#         for j in range(len(left_group)):
#             row.append(GOTO[i][j])
#         x.add_row(row)
#     print(x)
#     return
