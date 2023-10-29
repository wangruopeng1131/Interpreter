import os


terminal = ['+', '-', '*', '/', '//', '%', '=', '!=', '<', '>', '<=', '>=',
            'sqrt', 'pow', 'log', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh',
            'tanh', 'asinh', 'acosh', 'atanh', 'degree', 'radian', 'to_degree',
            'to_radian', 'to_numeric', 'len', 'abs', 'round', 'ceil', 'floor', 'trunc',
            'intersection', 'union', 'difference', 'product', 'join', 'contain', 'not',
            'or', 'and', 'isinf', 'isnan', 'subseteq', 'subset', 'in', '{', '}', '(',
            ')', '[', ']', '$', '<-', 'if', 'elif', 'else', 't', 'n', 'm', 's', 'i',
            'r', 'Sampling', 'Bool', 'Numeric', 'string', 'Position', 'Displacement',
            'Color', 'Shape', 'Size', 'Set', 'd', 'x', 'y', 'z', 'a', 'b', 'c', 'g', 'f']


name_list = ['F', 'H', 'J', 'V', 'P']


# 产生式树
class TreeNode:
    '''产生式树，用来提取左公因子'''
    def __init__(self, name: str, is_leaf: bool = False, is_root: bool = False, is_have_father: bool = True):
        self.name = name
        self.edges = {}
        self._is_leaf = is_leaf
        self._is_root = is_root
        self._counter = 0
        self._is_have_father = is_have_father

    def __repr__(self):
        s = ''
        if not self.edges:
            return self.name
        else:
            for edge in self.edges.keys():
                s += '{}->{}'.format(self.name, edge)
                s += '\n'
            return s

    def add_edge(self, child):
        self.edges[child.name] = child
        self._counter += 1

    @property
    def children_counter(self):
        return self._counter

    @property
    def is_leaf(self) -> bool:
        return self._is_leaf

    @property
    def is_root(self) -> bool:
        return self._is_root

    @property
    def is_have_father(self) -> bool:
        return self._is_have_father
# 全局变量


def _isterminal(name: str) -> bool:
    if name in terminal:
        return True
    return False


def _create_tree(left: str, rights: list) -> TreeNode:
    '''
    输入：root：语法单元 -> 语法单元 | 语法单元 |  ...
         left：产生式左边
         right：产生式右边
    例如：S -> d | aaB | aaaC | aaaDd | f，空格不会造成影响
    输出：单个语法字符串树
    '''

    if isinstance(left, str) and isinstance(rights, list):
        # 生成树
        if left == 'ε':
            raise ValueError('产生式左边必须是非终结符!')

        root = TreeNode(left, is_root=True)
        for g in rights:
            father = root  # father作为一个指针
            if len(g) == 1:  # 判断语法单元长度是否为1，若为1就是叶子节点
                child = TreeNode(g[0], is_leaf=True)
                father.add_edge(child)
            else:  # 若不为1，就将语法单元拆成树的形式
                for i, s in enumerate(g):
                    if s not in father.edges.keys():  # 判断此语法单元的元素是否在父节点的边当中，若不在就添加边
                        if i == len(g) - 1:
                            child = TreeNode(s, is_leaf=True)
                        else:
                            child = TreeNode(s)
                        father.add_edge(child)
                        father = child
                    else:
                        father = father.edges[s]  # 若在就将指针向下移动
        return root
    else:
        raise ValueError('左侧输入必须是字符串，右侧必须是列表！')


def _extract_left_common_factor(root: TreeNode) -> dict:
    '''
    提取公因子，使用树的后序遍历(递归)自底向上提取公因子
    输入：语法单元树，TreeNode
    输出：提取左公因子后的结果， 左侧str, 右侧list
    '''

    lcf = {}  # 初始化左公因子列表
    if isinstance(root, TreeNode):

        # 树的后序遍历
        def _post_order(root):
            stack = []  # 用栈存储多层左归因结果
            for _, child in root.edges.items():
                if root.is_root and child.is_leaf:  # 这是第一层递归，添加只有一层的左归因结果
                    stack.append([child.name])
                elif root.children_counter == 1 and child.is_leaf:  # 本节点不是根节点，只有一个叶节点
                    return [root.name, child.name]
                elif not root.is_root and child.is_leaf:  # 本节点不是根节点，但一个子节点是叶节点
                    stack.append([child.name])
                else:
                    name = _post_order(child)  # 多层左归因
                    stack.append(name)  # 向栈内添加多层左归因结果

            if not root.is_root and root.children_counter == 1:
                return [root.name] + name

            # 判断是否生成新的节点
            if not root.is_root:  # 需要生成新的名字。非第一层递归，添加本层左归因结果
                if len(stack) > 1:
                    if not _isterminal(root.name):
                        lcf[root.name + "'"] = stack
                        return [root.name, root.name + "'"]
                    else:
                        new = name_list.pop(0)
                        lcf[new] = [[root.name] + i for i in stack]
                        return [new]
                elif len(stack) == 1 and root.is_have_father:  # 此节点只有一个叶节点，直接将名字拼接即可
                    return [root.name] + stack
            else:  # 这是第一层递归，添加多层的左归因结果
                lcf[root.name] = stack

        _post_order(root)  # 开始递归
        return lcf
    else:
        raise ValueError('输入必须是TreeNode!')


def _left_eliminate(lcf: list) -> list:
    '''
    消除语法中的左递归情况。左递归分为两种情况，直接和间接。间接左递归较易处理，直接带入即可。
    而直接情况需要生成新的产生式才能避免。
    输入：提取公因子后的语法，lcf
    输出：消除左递归后的语法，lcf
    ----------------------------------
    例子：
    原始产生式：
                S->Aa|b|ε
                A->Ac|Sd
    消除间接左递归后的产生式：
                S->Aa|b|ε
                A->Ac|Aad|bd|d
    消除直接左递归后的产生式：
                S->Aa|b|ε
                A->bdA'|dA'
                A'->cA'|adA'|ε
    '''

    le = _direct_eliminate(lcf)  # 先消除直接左递归

    le = _indirect_eliminate(le)  # 再消除间接左递归

    le = _direct_eliminate(le)  # 最后再消除直接左递归

    return le


def _direct_eliminate(le: dict) -> dict:
    '''消除直接左递归'''
    new_le = {}
    for left, rights in le.items():
        product_1, product_2 = [], []
        if _is_have_left_recursion(left, rights):  # 满足直接递归条件， 例如，S -> Sa
            new_left = left + "'"
            while new_left in le.keys():
                new_left += "'"

            for right in rights:
                if left == right[0]:  # A -> Aα1 变成 A' ->  α1A' | ε 的结构
                    right.pop(0)
                    right.append(new_left)
                    product_1.append(right)
                else:   # A -> β1 变成 A -> β1A' 的结构
                    right.append(new_left)
                    product_2.append(right)
            product_1.append(['ε'])
            if product_2:
                new_le[left] = product_2
            new_le[new_left] = product_1
        else:
            new_le[left] = rights
    return new_le


def _indirect_eliminate(le: dict) -> dict:
    '''间接消除左递归'''

    circle = _find_circle(le)  # 寻找多层递归序列

    for cir in circle:
        for i in range(len(cir)-2, -1, -1):
            left, rights = cir[i], le[cir[i]]

            left_x, rights_x = cir[i-1], le[cir[i-1]]

            # rights插入rights_x中
            new = []
            for a in rights:
                for b in rights_x:
                    if b[0] != 'ε' and a[0] != 'ε':
                        if left_x == b[0]:
                            new.append(a + b[1:])
                        else:
                            new.append(a + b)
            if ['ε'] in rights_x:
                new.append(['ε'])
            le[left_x] = new
    return le


def _is_have_left_recursion(left: str, rights: list) -> bool:
    '''判断是否存在左递归'''
    for right in rights:
        if left == right[0]:
            return True
    return False


def _find_circle(le: dict) -> list:
    '''寻找间接左递归环'''
    import copy
    def circle(a, b):
        for c in b:
            if c[0] in le.keys():
                if c[0] not in s:  # 若当前遍历产生式的第一个元素不在list环内，则加入
                    s.append(c[0])
                    circle(c[0], le[c[0]])  # 下一层递归
                    s.pop()  # 递归出来扔掉当前层加入的产生式的第一个元素
                else:
                    where = s.index(c[0])
                    copy_s = copy.deepcopy(s)
                    for _ in range(where):  # 丢掉环起始点之前的元素
                        copy_s.pop(0)
                    x, y = key_list.index(copy_s[0]), key_list.index(copy_s[1])
                    if copy_s not in cir and x < y:  # 消除相同环，同时满足从上到下的序
                        cir.append(copy_s)
                    return

    cir = []
    key_list = list(le.keys())
    for a, b in le.items():
        s = [a]  # 用一个list存储环
        circle(a, b)  # 递归寻找环

    circle = []
    for i in range(len(cir)):
        for j in range(i + 1, len(cir)):
            a, b = set(cir[i]), set(cir[j])
            if a.issubset(b) and cir[i] not in circle:
                circle.append(cir[j])

    return circle


def _get_first(grammar: dict) -> dict:
    '''
    获取first集，满足四个条件：
    1. 如果X是终结符，则first(X) = { X }。
    2. 如果X是非终结符，且有产生式形如X → a…，则first( X ) = { a }。
    3.  如果X是非终结符，且有产生式形如X → ABCdEF…（A、B、C均属于非终结符且包含 ε，d为终结符），
    需要把first( A )、first( B )、first( C )、first( d )加入到 first( X ) 中。
    4. 如果X经过一步或多步推导出空字符ε，将ε加入first( X )。
    输入:
        grammar:提取公因子和消除左递归后的语法
    输出:
        语法的fisrt集
    '''

    from copy import deepcopy
    def _find_first(right: list) -> list:
        if right[0] == 'ε':  # 是第一层同时只有一个终结符ε那么直接返回即可
            return ['ε']
        else:
            f = []
            count = 0  # 为了检测是否满足条件4
            for r in right:   # ['S', "S'"]
                if r in terminal:  # 例如：*A中*是终结符,这个文法符号串就此终结
                    return f + [r]
                if r in first.keys():  # 如果first集中存在目标产生式的first集就可直接添加
                    # ε不在非终结符中
                    if 'ε' not in first[r]:
                        return f + first[r]
                elif r in grammar.keys():  # first集中没有当前r的first集创造一个
                    l = []
                    for new_rights in grammar[r]:
                        tmp = _find_first(new_rights)
                        if tmp[0] not in l and tmp not in l:
                            l += tmp
                    first[r] = l
                    # ε不在非终结符中
                    if 'ε' not in l:
                        return f + l
                else:
                    raise ValueError('检测语法或者终结符是否存在错误！')

                # ε在非终结符中
                tmp = deepcopy(first[r])
                tmp.remove('ε')
                f += tmp
                count += 1

            if count != len(right):  # 满足条件3
                return f
            else:   # 满足条件4
                return f + ['ε']

    first = {}
    for left, rights in grammar.items():
        if left not in first.keys():
            f = []
            for right in rights:  # [['S', "S'"], ['ε']]
                tmp = _find_first(right)
                if tmp[0] not in f and tmp not in f:
                    f += tmp
            first[left] = f

    for key in first.keys():
        first[key] = set(first[key])

    return first


def _find_target_follow(left: str, grammar: dict) -> tuple:
    follow = []
    for x, y in grammar.items():
        for r in y:
            if left in r and left != x:
                if (x, y) not in follow:
                    follow.append((x, y))
    return follow


def _get_select(first: dict, follow: dict, grammar: dict) -> dict:
    select = {}
    for left, rights in grammar.items():
        for right in rights:
            f = set()
            for i, r in enumerate(right):
                if r == 'ε':
                    break
                elif r in terminal:
                    f |= {r}
                    break
                elif 'ε' in first[r]:
                    f |= first[r] - {'ε'}
                else:
                    f |= first[r]
                    break

            if 'ε' in right:
                select[left + '->' + ''.join(right)] = follow[left] | f
            else:
                select[left + '->' + ''.join(right)] = f

    return select


def _get_follow(start: str, first: set, grammar: dict) -> set:
        '''
        获取follow集，满足follow集的条件有两个
        1. 如果存在一个产生式S->αXβ，那么将集合first(β)中除ε外的所有元素加入到FOLLOW(X)当中
        2. 如果存在一个产生式 S->αX , 或者S->αXβ且first(β)中包含ε , 那么将集合FOLLOW(S)中的所有元素加入到集合FOLLOW(X)中
        输入:
            first: first集
            grammar: 提取公因子和消除左递归后的语法
        输出:
            语法的follow集
        '''

        from copy import deepcopy
        follow = {}

        def _find_follow(target: str, left: str, rights: list):
            for right in rights:
                if target in right:
                    for i, r in enumerate(right):
                        if i == len(right) - 1 and r in terminal:  # S->αXβ情况, β最后一个字符是终结符
                            follow[target] |= {r}
                        elif i == len(right) - 1 and i == right.index(target):  # S->αX情况
                            follow[target] |= {left}
                        elif i > right.index(target):  # 若是非终结符则按规则寻找follow
                            if r in terminal:  # β中第一个字符是终结符
                                follow[target] |= {r}
                                break
                            # r是非终结符
                            else:
                                if r == ',':
                                    continue
                                elif 'ε' not in first[r]:   # ε不在r的first集中，那么将集合first(β)中除ε外的所有元素加入到FOLLOW(X)当中
                                    follow[target] |= first[r]
                                else:  # ε在r的first集中，那么将集合FOLLOW(S)中的所有元素加入到集合FOLLOW(X)中
                                    # 剔除r中的ε加入r的follow集中
                                    tmp = deepcopy(first[r])
                                    follow[target] |= tmp - {'ε'}
                                    if i == len(right) - 1:
                                        follow[target] |= {left}

        for left, rights in grammar.items():
            if start == left:
                follow[left] = {'#'}
            else:
                follow[left] = set()


        for left, rights in grammar.items():
            f = _find_target_follow(left, grammar)
            for new_left, new_rights in f:
                _find_follow(left, new_left, new_rights)

        for key in follow.keys():
            f = follow[key]
            for k in follow.keys():
                if k in f:
                    f.remove(k)
                    f |= follow[k]

        return follow


def isLL1(select: dict) -> bool:
    for l1, r1 in select.items():
        x = l1.split('->')[0]
        for l2, r2 in select.items():
            y = l2.split('->')[0]
            if l1 != l2 and x == y and len(r1 & r2) != 0:
                return False
    return True


class GrammarProduct(object):
    def __init__(self, path):
        self.path = path
        grammar = []
        with open(path, "r") as f:
            for line in f.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                grammar.append(line)
        self.grammar = grammar

    def create_tree(self):
        grammar = self.grammar
        if len(grammar) == 1:
            grammar = _create_tree(grammar[0])
        else:
            grammar = _create_tree(grammar)

        return grammar

    def extract_lcf(self):
        root = self.create_tree()
        lcf = _extract_left_common_factor(root)
        return lcf

    def save(self, lcf):
        root, file = os.path.split(self.path)
        file = 'new_' + file
        save_path = os.path.join(root, file)

        with open(save_path, "w") as f:
            for l in lcf:
                f.write(l)
        print('保存完成！文件路径为{}'.format(save_path))


if __name__ == '__main__':
    grammar = {
        "S'": [['S', "S'"], ['ε']],
        "S": [['i', '<-', 'E'], ['i', '<-', 'Sampling', '(', 's', 'O', ')'],
              ['s', '<-', 'F'], ['if', '(', 'B', ')', '{', 'S', '}',
               'elif', '(', 'B', ')', '{', 'S', '}', 'else', '{', 'S', '}']],
        "E": [['N'], ['T'], ['R'], ['B']],
        "N": [['M'], ['+', 'M'], ['-', 'M'], ['N', '+', 'M'], ['N', '-', 'M']],
        "M": [['m'], ['L', '*', 'A'], ['L', '/', 'A'], ['L', '//', 'A'], ['L', '%', 'A']],
        "L": [['sqrt', '(', 'A', ')'], ['pow', '(', 'N', ',', 'N', ')'], ['log', '(', 'n', 'A', ')'], ['sin', '(', 'A', ')'],
              ['cos', '(', 'A', ')'], ['tan', '(', 'r', ')'], ['asin', '(', 'A', ')'], ['acos', '(', 'A', ')'],
              ['atan', '(', 'A', ')'], ['sinh', '(', 'A', ')'], ['cosh', '(', 'A', ')'], ['tanh', '(', 'A', ')'],
              ['asinh', '(', 'n', ')'], ['acosh', '(', 'A', ')'], ['atanh', '(', 'A', ')'], ['degree', '(', 'A', ')'],
              ['radian', '(', 'A', ')'], ['to_degree', '(', 'A', ')'], ['to_radian', '(', 'A', ')'],
              ['to_numeric', '(', 'A', ')'], ['len', '(', 'K', ')'], ['abs', '(', 'A', ')'], ['round', '(', 'A', 'n', ')'],
              ['ceil', '( ', 'A', 'n', ')'], ['floor', '(', 'A', 'n', ')'], ['trunc', '(', 'A', 'n', ')']],
        "K": [['U'], ['C']],
        "A": [['i'], ['n'], ['r'], ['(', 'N', ')']],
        "T": [['U'], ['intersection', '(', 'U', 'U', ')'], ['union', '(', 'U', 'U', ')'],
              ['difference', '(', 'U', 'U', ')'], ['product', '(', 'U', 'U', ')'], ['join', '(', 'U', 'U', ')']],
        "U": [['s'], ['{', 'n', '}'], ['(', 'T', ')']],
        "R": [['t', '[', 'I', ']'], ['D', '+', 'R'], ['D', '+', 'N'], ['N', '+', 'D']],
        "I": [['t'], ['n'], ['n', ':', 'n']],
        "D": [['C'], ['t', '*', 'n'], ['n', '*', 't']],
        "C": [['t'], ['$'], ['(', 'R', ')']],
        "B": [['X'], ['Y'], ['i', 'contain', 'T'], ['not', 'B'], ['B', 'and', 'B'], ['B', 'or', 'B']],
        "X": [['E', 'Q', 'E'], ['isinf', '(', 'N', ')'], ['isnan', '(', 'N', ')'], ['R', 'in', 'E'], ['E', '=', 'E'], ['E', '!=', 'E']],
        "Y": [['T', 'Z', 'T']],
        "Z": [['='], ['!='], ['subseteq'], ['subset']],
        "Q": [['='], ['>'], ['<'], ['<='], ['>=']],
        "O": [['Bool'], ['Numeric'], ['string'], ['Position'], ['Displacement'], ['Color'],['Shape'], ['Size'], ['Set']]
              }
    # grammar = {'E': [['E', '+', 'T'], ['T']],
    #            'T': [['T', '*', 'F'], ['F']],
    #            'F': [['(', 'E', ')'], ['d']]}

    # grammar = {
    #     'E': [['T', 'A']],
    #     'A': [['+', 'T', 'A'], ['-', 'T', 'A'], ['ε']],
    #     'T': [['F', 'B']],
    #     'B': [['*', 'F', 'B'], ['/', 'F', 'B'], ['ε']],
    #     'F': [['(', 'E', ')'], ['D']],
    #     'D': [['x'], ['y'], ['z']]
    # }
    # grammar = {
    #     'E': [['E', '+', 'T'], ['E', '-', 'T'], ['T']],
    #     'T': [['T', '*', 'F'], ['T', '/', 'F'], ['F']],
    #     'F': [['(', 'E', ')'], ['D']],
    #     'D': [['x'], ['y'], ['z']]
    # }

    # grammar = {
    #     'A': [['B', 'C', 'c'], ['g', 'D', 'B']],
    #     'B': [['b', 'C', 'D', 'E'], ['ε']],
    #     'C': [['D', 'a', 'B'], ['c', 'a']],
    #     'D': [['d', 'D'], ['ε']],
    #     'E': [['g', 'A', 'f'], ['c']]
    # }

    # lcf = {}
    # for left, rights in grammar.items():
    #     # 建立产生式树
    #     root = _create_tree(left, rights)
    #     # 消除提取公因子
    #     lcf.update(_extract_left_common_factor(root))
    #
    # 消除左递归
    new_grammar = _left_eliminate(grammar)

    # 获取first集
    first = _get_first(new_grammar)


    # 获取follow集
    follow = _get_follow("S'", first, new_grammar)

    # # 获取Select集
    select = _get_select(first, follow, grammar)
    #
    # # 判断是否为LL(1)语法
    # isLL1(select)