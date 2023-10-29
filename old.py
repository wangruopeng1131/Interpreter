import logging
import numba

code = {
    '#{': 'VARIABLE',
    '<-': 'ASSIGNMENT',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIVISION',
    '//': 'DIVISION',
    '%': 'MOD',
    '^': 'POWER',
    'sqrt': 'ROOT',
    'log': 'LOG',
    'sin': 'SIN',
    'cos': 'COS',
    'tan': 'TAN',
    'asin': 'ASIN',
    'acos': 'ACOS',
    'atan': 'ATAN',
    'sinh': 'SINH',
    'cosh': 'COSH',
    'tanh': 'TANH',
    'asinh': 'ASINH',
    'acosh': 'ACOSH',
    'atanh': 'ATANH',
    'degree': 'DEGREE',
    'radian': 'RADIAN',
    'to_degree': 'TODEGREE',
    'to_radian': 'TORADIAN',
    'to_numeric': 'TONUMERIC',
    'len': 'LEN',
    'abs': 'ABS',
    'round': 'ROUND',
    'ceil': 'CEIL',
    'floor': 'FLOOR',
    'trunc': 'TRUNC',
    'intersection': 'INTERSECTION',
    'union': 'UNION',
    'difference': 'DIFFERENCE',
    'product': 'PRODUCT',
    'join': 'JOIN',
    'in': 'IN',
    ':': 'SPLICE',
    ',': 'CONNECT',
    ')': 'RPAREN',
    '(': 'LPAREN',
    ']': 'RBRACK',
    '[': 'LBRACK',
    '}': 'RBRACE',
    '{': 'LBRACE',
    r'\left': 'IGNORE',
    r'\right': 'IGNORE',
    '=': 'RELATIONS',
    '<': 'RELATIONS',
    '>': 'RELATIONS',
    '!=': 'RELATIONS',
    '<=': 'RELATIONS',
    '>=': 'RELATIONS',
    'not': 'RELATIONS',
    'and': 'RELATIONS',
    'or': 'RELATIONS',
    'string': 'string',
    'contain': 'CONTAIN',
    'isinf': 'INF',
    'isnan': 'NAN',
    'subseteq': 'SUBSETQE',
    'subset': 'SUBSET',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'Sampling': 'SAMPLING'
}

class Interpreter(object):
    def __init__(self):
        '''
        解释器
        '''
        self.ASTree = {}
        self.scanner = Scanner()
        self.set = {}
        self.token_pointer = 0

    def get_next_token(self):
        return self.scanner[self.token_pointer]

    def expression(self, expression):
        length = len(expression)
        if length == 0:
            # 空表达式不分析
            return

    def create_set(self):
        '''创建基本集合对象，集合对象内应该包括元素，运算，抽样三种属性'''
        pass


    def create_astree(self):
        '''创建语法树，用字典存储每一个nodes及edges'''
        pass


class Token(object):
    def __init__(self, type, value):

        self.type = type
        self.value = value

    def __str__(self):
        """string representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        if key == 'type':
            return self.type
        else:
            return self.value

    def __eq__(self, other):
        if self.type == other:
            return True
        else:
            return False


class Scanner:
    def __init__(self):
        self.tokenlist = []


    @numba.jit(nopython=True,parallel=True)
    def split(self, expression):
        '''拆分语句为一串词'''
        stack = []
        pair_stack = []
        word = []
        wordDict = list(code.keys())
        pair_check = {')': '(', ']': '[', '}': '{', '#': '#'}
        pair_list = ['{', '}', '[', ']', '(', ')', '#']
        def pop_stack(times):
            s = ''
            for _ in range(times):
                s += stack.pop(0)
            return s

        pointer = 0  # 字符识别指针，用来标记不在字典内的字符长度
        temp = ''  # 用来记录多目字符
        for i, w in enumerate(expression):
            if w == ' ':
                continue
            stack.append(w)
            temp += w
            # print('stack:{}'.format(stack))
            # 分离字符靠三个条件
            if w in wordDict or w == '\\':  # 单目字符查字典
                if pointer == 0:  # 首位是字典内单目符号
                    if w != '\\':
                        word.append(pop_stack(1))
                        temp = ''
                    else:
                        pointer += 1
                else:  # 首位不是字典内单目符号
                    word.append(pop_stack(pointer))
                    temp = ''
                    if stack[0] != '\\':  # 首位不是'\'才可出栈
                        word.append(pop_stack(1))
                        temp = ''
                    # print('word:{}'.format(word))
                    pointer = 0
            elif temp in wordDict:  # 多目字符查字典
                word.append(pop_stack(pointer + 1))  # 出栈，+1是因为新入栈的字符也要出栈
                pointer = 0
                temp = ''
            else:  # 不在字典内
                pointer += 1
            # 括号配对检查
            if w in pair_list:
                if pair_stack and w in pair_check:
                    if pair_stack[-1] == pair_check[w]:
                        pair_stack.pop()
                    else:
                        pair_stack.append(w)
                else:
                    pair_stack.append(w)
                #print('pair_stack:{}'.format(pair_stack))

        if len(stack):  # 栈内不为空则不是字典内符号，需全部出栈
            word.append(pop_stack(len(stack)))
        #print('word:{}'.format(word))
        if len(pair_stack):
            return '括号不配对'
        self._word = word


    @numba.jit(nopython=True, parallel=True)
    def get_token(self, expression):
        '''标记每一个词的类别'''
        word = self._word
        wordDict = list(code.keys())
        # 如果字符串在code表内则创建token
        i = 0
        while i < len(word) - 1:
                if word[i] == '#' and word[i + 1] == '{':
                    self.tokenlist.append(Token(word[i + 2]), 'VARIABLE')
                    i += 5 # 跳过以下 # { 变量 } #
                elif (word[i] == '+' and word[i + 1] == '-') or (word[i] == '-' and word[i + 1] == '+'):
                    return '加减法语法错误,请在中间添加括号'
                else:
                    if word[i] in wordDict: # 查表看符号类别
                        self.tokenlist.append(Token(word[i], code[word[i]]))
                    elif self.isnumeric(word[i]): # 判断是不是数字
                        self.tokenlist.append(Token(word[i], 'NUM'))
                    else:
                        self.tokenlist.append(Token(word[i], 'STR'))
                    i += 1
        else:
            if word[i] in wordDict: # 查表看符号类别
                self.tokenlist.append(Token(word[i], code[word[i]]))
            elif self.isnumeric(word[i]): # 判断是不是数字
                self.tokenlist.append(Token(word[i], 'NUM'))
            else:
                self.tokenlist.append(Token(word[i], 'STR'))


    def isnumeric(self, number):
        '''
        判断是否是数字类型
        '''
        number = number.split('.')
        if len(number) == 1:
            return number[0].isnumeric()
        else:
            if len(number) == 2:
                if number[0].isnumeric() and number[1].isnumeric():
                    return True
                else:
                    return False
            else:
                return False


    def __getitem__(self, item):
        return self.tokenlist[item]