# -*- coding: utf-8 -*-
import re
from typing import List

from Symbols import *
from utils import Token


class Scanner:
    wordDict = list(Reserved.keys()) + list(Assign.keys()) + list(BinaryOp.keys()) + list(UnaryOp.keys()) + \
               seperator

    def __init__(self):
        self.tokenlist = None

    def __call__(self, expression):
        return self.split(expression)

    def split(self, expression: str) -> List[Token]:
        """拆分语句为一串词"""
        stack = []
        pair_stack = []
        pair_check = {')': '(', ']': '[', '}': '{'}
        pair_list = ['{', '}', '[', ']', '(', ')']
        self.tokenlist = []

        def pop_stack(times):
            s = ''
            for _ in range(times):
                s += stack.pop(0)
            return s

        variable, temp = '', ''  # 用来记录多目字符
        count = 0
        signal = False
        for i, w in enumerate(expression):
            if w == ' ':
                continue
            stack.append(w)

            # 括号配对检查
            if w in pair_list:
                if pair_stack and w in pair_check:
                    if pair_stack[-1] == pair_check[w]:
                        pair_stack.pop()
                    else:
                        pair_stack.append(w)
                else:
                    pair_stack.append(w)

            # 专门识别//等类似符号
            if i < len(expression) - 1:
                if w + expression[i + 1] in ['//', '==']:
                    if stack:
                        t = pop_stack(len(temp))
                        self._to_token(count, t)
                        temp = ''
                    signal = True
                    continue
                if signal:
                    self._to_token(count, expression[i - 1] + w)
                    pop_stack(2)
                    count += 1
                    signal = False
                    continue

            # 分离字符靠三个条件
            if w in self.wordDict:  # 单目字符查字典
                if temp:
                    self._to_token(count, temp)
                    pop_stack(len(temp))  # 出栈，+1是因为新入栈的字符也要出栈
                    variable, temp = '', ''
                    count += 1
                self._to_token(count, w)
                stack.pop()
                count += 1
                continue
            elif temp in self.wordDict:  # 多目字符查字典
                t = pop_stack(len(temp))  # 出栈，+1是因为新入栈的字符也要出栈
                self._to_token(count, t)
                variable, temp = '', ''
                count += 1
                continue
            else:
                temp += w

            # 检查变量
            if i < len(expression) - 1:
                if w.isalpha() or (variable and w.isdigit()):  # 第一个字符是字母或者变量有数值且当且是数字
                    variable += w
                    if expression[i + 1].isalpha() or expression[i + 1].isdigit():
                        continue
                if variable:
                    self._to_token(count, variable)
                    pop_stack(len(variable))
                    variable, temp = '', ''
                    count += 1
            elif i == len(expression) - 1:  # 检查最后一位是否是变量
                if variable:
                    if w.isalpha() or w.isdigit():
                        variable += w
                        self._to_token(count, variable)
                        pop_stack(len(variable))

        if len(stack):  # 栈内不为空则不是字典内符号，需全部出栈
            self._to_token(count, temp)

        if len(pair_stack):
            raise ValueError('括号不配对')

        return self.tokenlist

    def isnumeric(self, number):
        """
        判断是否是数字类型，弃用
        """
        if number.isdigit():
            return True
        if '.' in number:
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
        else:
            return False

    def _to_token(self, i: int, word: str, j: int = 0):
        """
        token化
        参数：
            i:行
            j:列
            word: 可识别的字符
        """
        # TODO：需要检查变量是否在变量管理器内
        # TODO: 需要确定布尔、集合、RGB等识别符
        if word in Reserved.keys():  # 保留字
            token = Token('T', Reserved[word], Reserved[word], word, j, i)
        # 数字
        elif self.isnumeric(word):  # 判断是不是数字
            token = Token('T', 'number', 'number', float(word), j, i)
        elif word in seperator:  # 分隔符
            token = Token('T', 'seperator', word, word, j, i)
        elif word in Assign.keys():  # 赋值
            token = Token('T', 'assignment', word, word, j, i)
        elif word in BinaryOp.keys() or word in UnaryOp.keys():  # 运算符
            token = Token('T', 'operator', word, word, j, i)
        elif re.findall('\".+?\"', word, flags=re.DOTALL):  # 字符串，注意：字符使用单引号
            token = Token('T', 'string', word, word, j, i)
        elif re.findall('[a-zA-Z_][a-zA-Z_0-9]*', word, flags=re.DOTALL):  # 变量
            token = Token('T', 'ID', 'id', word, j, i)
        else:
            print('无法识别字符{}'.format(word))
            return
        self.tokenlist.append(token)


if __name__ == "__main__":
    expressions = ['a1 = ((534-23)//2.1+423)*23.1+1.1',
                   'a = ((534-23)//2.1+423)*23.1+1.1',
                   'a1.1 = ((534-23)//2.1+423)*23.1+1.1',
                   'if () {} elif () {} else {}',
                   'a1a = (log((1+2)*2.5) + 1) * 1 + a1a',
                   'aa = (log((1+2)*2.5) + 1) * 1 + aa',
                   'aa = (log((1+2)*2.5) + 1) * 1 + a1.1',
                   'aa = (log((1+2)*2.5) + 1) * 1 + a1.1',
                   'aa = (log((1+2)*2.5) + 1)) * 1 + aa']
    scanner = Scanner()
    for expression in expressions:
        tokens = scanner(expression)
        print(tokens)
