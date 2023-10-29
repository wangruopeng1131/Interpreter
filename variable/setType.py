#!/usr/bin/python3
# coding:utf8
"""
@Create date: 2021/12/7
@Author: 胡宏达
"""
from collections import Iterable
from .element import Numeric, string, Color


class BaseSet(object):
    def __init__(self):
        super(BaseSet, self).__init__()


class DiscreteSet(BaseSet):
    def __init__(self, a):
        super(DiscreteSet, self).__init__()
        self.a = a

    def __iter__(self):
        return self

    def __getitem__(self, index):
        return self.a[index]


class NumericDiscreteSet(DiscreteSet, Numeric):
    def __init__(self, items=()):
        super(NumericDiscreteSet, self).__init__(items)
        if not isinstance(items, Iterable) or isinstance(items, str):
            raise ValueError("接收到一个不可迭代的对象：{}".format(items))
        for item in items:
            if not isinstance(item, (int, float, Numeric)):
                raise TypeError("可迭代对象数据类型不一致,希望元素类型为float、int、Numeric")
        self.type = Numeric
        self._items = set(items)

    def __getitem__(self, index):
        return list(self._items)[index]

    def add(self, other):
        if not isinstance(other, (int, float, Numeric)):
            return NotImplemented
        self._items.add(other)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __and__(self, other):
        # 交集
        if isinstance(other, NumericDiscreteSet):
            other = other._items
        elif isinstance(other, set):
            other = other
        else:
            return NotImplemented
        return self._items & other

    def __sub__(self, other):
        # 差集，self为被减数
        if isinstance(other, NumericDiscreteSet):
            other = other._items
        elif isinstance(other, (list, set)):
            other = set(other)
        else:
            return NotImplemented
        return self._items - other

    def __rsub__(self, other):
        # 差集，self为减数
        if isinstance(other, NumericDiscreteSet):
            other = other._items
        elif isinstance(other, (list, set)):
            other = set(other)
        else:
            return NotImplemented
        return other - self._items

    def __or__(self, other):
        # 并集
        if isinstance(other, NumericDiscreteSet):
            other = other._items
        elif isinstance(other, (list, set)):
            other = set(other)
        else:
            return NotImplemented
        return self._items | other


class stringDiscreteSet(DiscreteSet, string):
    def __init__(self, items):
        super(stringDiscreteSet, self).__init__(items)
        if not isinstance(items, Iterable) or isinstance(items, str):
            raise ValueError("接收到一个不可迭代的对象：{}".format(items))
        for item in items:
            if not isinstance(item, (str, string)):
                raise TypeError("可迭代对象数据类型不一致,希望元素类型为str、string")
        self.type = string
        self._items = set(items)

    def add(self, other):
        if not isinstance(other, (str, string)):
            return NotImplemented
        self._items.add(other)

    def __getitem__(self, index):
        return list(self._items)[index]

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)


class ComplexDiscreteSet(DiscreteSet):
    def __init__(self, items):
        super(ComplexDiscreteSet, self).__init__(items)


class ContinueSet(BaseSet):
    def __init__(self, start=float("-inf"), end=float("inf"), left_close=False, right_close=False):
        super(ContinueSet, self).__init__()
        if not isinstance(start, (Numeric, string, str, int, float)):
            raise TypeError("传入数据的类型错误，希望是Numeric或string")
        self.min = start
        self.max = end
        self.l_c = left_close
        self.r_c = right_close

    def __str__(self):
        left = "(" if self.l_c else "["
        start = "-∞" if self.min == float("-inf") else self.min
        if start == "-∞":
            left = "("
            self.min = float("-inf")
        end = "+∞" if self.max == float("inf") else self.max
        right = ")" if self.r_c else "]"
        if end == "+∞":
            right = ")"
            self.max = float("inf")
        return "{}{},{}{}".format(left, start, end, right)

    def __repr__(self):
        left = "(" if self.l_c else "["
        start = "-∞" if self.min == float("-inf") else self.min
        if start == "-∞":
            left = "("
            self.min = float("-inf")
        end = "+∞" if self.max == float("inf") else self.max
        right = ")" if self.r_c else "]"
        if end == "+∞":
            right = ")"
            self.max = float("inf")
        return "{}{},{}{}".format(left, start, end, right)

    def __contains__(self, item):
        if self.l_c:
            if self.r_c:
                if self.min < item < self.max:
                    return True
                else:
                    return False
            else:
                if self.min < item <= self.max:
                    return True
                else:
                    return False
        else:
            if self.r_c:
                if self.min <= item < self.max:
                    return True
                else:
                    return False
            else:
                if self.min <= item <= self.max:
                    return True
                else:
                    return False

    def __getitem__(self, key):
        raise ValueError("无法迭代一个连续集合")
