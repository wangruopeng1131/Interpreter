# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 17:03:59 2021

@author: 赵匡是
"""

import logging
from typing import Union
from math import (log, radians, degrees, sin, cos, tan, asin, acos, atan,
                  floor, ceil, trunc)

from .base import BaseVariable
from .referential import ReferentialVariable

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # TODO: 后期替换


class Operator(BaseVariable):
    def __init__(self):
        super(Operator, self).__init__(refresh_moment = 'other')


class Compare(Operator):
    def __init__(self, a, b):
        super(Compare, self).__init__()
        self.a = a
        self.b = b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        if a > b:
            return 1
        if a == b:
            return 0
        if a < b:
            return -1


class Equal(Compare):
    def __call__(self):
        r = super(Equal, self).__call__()
        if r == 0:
            return True
        else:
            return False


class Unequal(Compare):
    def __call__(self):
        r = super(Unequal, self).__call__()
        if r != 0:
            return True
        else:
            return False


class Less(Compare):
    def __call__(self):
        r = super(Less, self).__call__()
        if r < 0:
            return True
        else:
            return False


class Greater(Compare):
    def __call__(self):
        r = super(Greater, self).__call__()
        if r > 0:
            return True
        else:
            return False


class LessEqual(Compare):
    def __call__(self):
        r = super(LessEqual, self).__call__()
        if r <= 0:
            return True
        else:
            return False


class GreaterEqual(Compare):
    def __call__(self):
        r = super(GreaterEqual, self).__call__()
        if r >= 0:
            return True
        else:
            return False


class And(Operator):
    def __init__(self, a, b):
        super(And, self).__init__()
        self.a = a
        self.b = b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        return (a and b)


class Or(Operator):
    def __init__(self, a, b):
        super(Or, self).__init__()
        self.a = a
        self.b = b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        return (a or b)


class Not(Operator):
    def __init__(self, a):
        super(Not, self).__init__()
        self.a = a

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        return (not a)


class Positive(Operator):
    def __init__(self, var):
        # 实现取正操作
        super(Positive, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return var


class Negative(Operator):
    def __init__(self, var):
        # 实现取负操作
        super(Negative, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return -1 * var


class Absolute(Operator):
    def __init__(self, var):
        super(Absolute, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return abs(var)


class Round(Operator):
    def __init__(self, var, n: int = 0):
        # 实现内建函数 round() ，n 是近似小数点的位数
        super(Round, self).__init__()
        self.var = var
        self.n = n

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return round(var, self.n)


class Floor(Operator):
    def __init__(self, var):
        # 实现 math.floor() 函数，即向下取整
        super(Floor, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return floor(var)


class Ceil(Operator):
    def __init__(self, var):
        # 实现 math.ceil() 函数，即向上取整
        super(Ceil, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return ceil(var)


class Trunc(Operator):
    def __init__(self, var):
        # 实现 math.trunc() 函数，即距离零最近的整数
        super(Trunc, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return trunc(var)


class Sum(Operator):
    def __init__(self, addend_a, addend_b):
        super(Sum, self).__init__()
        self.a = addend_a
        self.b = addend_b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        return a + b


class Difference(Operator):
    def __init__(self, minuend, subtrahend):
        super(Difference, self).__init__()
        self.minuend = minuend
        self.subtrahend = subtrahend

    def __call__(self):
        minuend = self.minuend() if callable(self.minuend) else self.minuend
        subtrahend = (self.subtrahend() if callable(self.subtrahend)
                      else self.subtrahend)
        return minuend - subtrahend


class Product(Operator):
    def __init__(self, factor_a, factor_b):
        super(Product, self).__init__()
        self.a = factor_a
        self.b = factor_b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        return a * b


class Quotient(Operator):
    def __init__(self, numerator, denominator):
        super(Quotient, self).__init__()
        self.numerator = numerator
        self.denominator = denominator

    def __call__(self):
        numerator = (self.numerator() if callable(self.numerator)
                     else self.numerator)
        denominator = (self.denominator() if callable(self.denominator)
                       else self.denominator)
        return numerator / denominator


class FloorQuotient(Operator):
    def __init__(self, numerator, denominator):
        super(FloorQuotient, self).__init__()
        self.numerator = numerator
        self.denominator = denominator

    def __call__(self):
        numerator = (self.numerator() if callable(self.numerator)
                     else self.numerator)
        denominator = (self.denominator() if callable(self.denominator)
                       else self.denominator)
        return numerator // denominator


class Remainder(Operator):
    def __init__(self, numerator, denominator):
        super(Remainder, self).__init__()
        self.numerator = numerator
        self.denominator = denominator

    def __call__(self):
        numerator = (self.numerator() if callable(self.numerator)
                     else self.numerator)
        denominator = (self.denominator() if callable(self.denominator)
                       else self.denominator)
        return numerator % denominator


class Power(Operator):
    def __init__(self, base, exponent):
        super(Power, self).__init__()
        self.base = base
        self.exponent = exponent

    def __call__(self):
        base = self.base() if callable(self.base) else self.base
        exponent = (self.exponent() if callable(self.exponent)
                       else self.exponent)
        return base ** exponent


class Logarithmic(Operator):
    def __init__(self, base, antilogarithm):
        super(Logarithmic, self).__init__()
        self.base = base
        self.antilogarithm = antilogarithm

    def __call__(self):
        base = self.base() if callable(self.base) else self.base
        antilogarithm = (self.antilogarithm() if callable(self.antilogarithm)
                       else self.antilogarithm)
        return log(antilogarithm, base)


class Sine(Operator):
    def __init__(self, var, unit: str = 'rad'):
        super(Sine, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'deg' or self.unit.lower() == 'degree':
            var = radians(var)
        return sin(var)


class Cosine(Operator):
    def __init__(self, var, unit: str = 'rad'):
        super(Cosine, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'deg' or self.unit.lower() == 'degree':
            var = radians(var)
        return cos(var)


class Tangent(Operator):
    def __init__(self, var, unit: str = 'rad'):
        super(Tangent, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'deg' or self.unit.lower() == 'degree':
            var = radians(var)
        return tan(var)


class Arcsine(Operator):
    def __init__(self, var, unit: str = 'rad'):
        super(Arcsine, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'rad' or self.unit.lower() == 'radian':
            return asin(var)
        else:
            return degrees(asin(var))


class Arccosine(Operator):
    def __init__(self, var, unit: str = 'rad'):
        super(Arccosine, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'rad' or self.unit.lower() == 'radian':
            return acos(var)
        else:
            return degrees(acos(var))


class Arctangent(Operator):
    def __init__(self, var, unit: str = 'rad'):
        super(Arctangent, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'rad' or self.unit.lower() == 'radian':
            return atan(var)
        else:
            return degrees(atan(var))