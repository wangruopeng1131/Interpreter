# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 09:05:20 2021

@author: 赵匡是
"""
from .type import (Numeric, string, Logic, Size, Position, Color)
from .operator import (Operator, Compare, Equal, Unequal, Less, Greater,
                       LessEqual, GreaterEqual, And, Or, Not,
                       Positive, Negative, Absolute, Round, Floor, Ceil, Trunc,
                       Sum, Difference, Product, Quotient, FloorQuotient,
                       Remainder, Power, Logarithmic,
                       Sine, Cosine, Tangent, Arcsine, Arccosine, Arctangent)

class NumCompare(Compare, Logic):
    def __init__(self, a, b):
        super(NumCompare, self).__init__(a, b)


class NumEqual(Equal, Logic):
    def __init__(self, a, b):
        super(NumEqual, self).__init__(a, b)


class NumUnequal(Unequal, Logic):
    def __init__(self, a, b):
        super(NumUnequal, self).__init__(a, b)


class NumLess(Less, Logic):
    def __init__(self, a, b):
        super(NumLess, self).__init__(a, b)


class NumGreater(Greater, Logic):
    def __init__(self, a, b):
        super(NumGreater, self).__init__(a, b)


class NumLessEqual(LessEqual, Logic):
    def __init__(self, a, b):
        super(NumLessEqual, self).__init__(a, b)


class NumGreaterEqual(GreaterEqual, Logic):
    def __init__(self, a, b):
        super(NumGreaterEqual, self).__init__(a, b)


class StrCompare(Compare, Logic):
    def __init__(self, a, b):
        super(StrCompare, self).__init__(a, b)


class StrEqual(Equal, Logic):
    def __init__(self, a, b):
        super(StrEqual, self).__init__(a, b)


class StrUnequal(Unequal, Logic):
    def __init__(self, a, b):
        super(StrUnequal, self).__init__(a, b)


class StrLess(Less, Logic):
    def __init__(self, a, b):
        super(StrLess, self).__init__(a, b)


class StrGreater(Greater, Logic):
    def __init__(self, a, b):
        super(StrGreater, self).__init__(a, b)


class StrLessEqual(LessEqual, Logic):
    def __init__(self, a, b):
        super(StrLessEqual, self).__init__(a, b)


class StrGreaterEqual(GreaterEqual, Logic):
    def __init__(self, a, b):
        super(StrGreaterEqual, self).__init__(a, b)


class NumPositive(Positive, Numeric):
    def __init__(self, var):
        super(NumPositive, self).__init__(var)


class NumNegative(Negative, Numeric):
    def __init__(self, var):
        super(NumNegative, self).__init__(var)


class NumAbsolute(Absolute, Numeric):
    def __init__(self, var):
        super(NumAbsolute, self).__init__(var)


class NumRound(Round, Numeric):
    def __init__(self, var, n: int = 0):
        super(NumRound, self).__init__(var, n)


class NumFloor(Floor, Numeric):
    def __init__(self, var):
        super(NumFloor, self).__init__(var)


class NumCeil(Ceil, Numeric):
    def __init__(self, var):
        super(NumCeil, self).__init__(var)


class NumTrunc(Trunc, Numeric):
    def __init__(self, var):
        super(NumTrunc, self).__init__(var)


class NumSum(Sum, Numeric):
    def __init__(self, addend_a, addend_b):
        super(NumSum, self).__init__(addend_a, addend_b)


class NumDifference(Difference, Numeric):
    def __init__(self, minuend, subtrahend):
        super(NumDifference, self).__init__(minuend, subtrahend)


class NumProduct(Product, Numeric):
    def __init__(self, factor_a, factor_b):
        super(NumProduct, self).__init__(factor_a, factor_b)


class NumQuotient(Quotient, Numeric):
    def __init__(self, numerator, denominator):
        super(NumQuotient, self).__init__(numerator, denominator)


class NumFloorQuotient(FloorQuotient, Numeric):
    def __init__(self, numerator, denominator):
        super(NumFloorQuotient, self).__init__(numerator, denominator)


class NumRemainder(Remainder, Numeric):
    def __init__(self, numerator, denominator):
        super(NumRemainder, self).__init__(numerator, denominator)


class NumPower(Power, Numeric):
    def __init__(self, base, exponent):
        super(NumPower, self).__init__(base, exponent)


class NumLogarithmic(Logarithmic, Numeric):
    def __init__(self, base, antilogarithm):
        super(NumLogarithmic, self).__init__(base, antilogarithm)


class NumSine(Sine, Numeric):
    def __init__(self, var, unit: str = 'rad'):
        super(NumSine, self).__init__(var, unit)


class NumCosine(Cosine, Numeric):
    def __init__(self, var, unit: str = 'rad'):
        super(NumCosine, self).__init__(var, unit)


class NumTangent(Tangent, Numeric):
    def __init__(self, var, unit: str = 'rad'):
        super(NumTangent, self).__init__(var, unit)


class NumArcsine(Arcsine, Numeric):
    def __init__(self, var, unit: str = 'rad'):
        super(NumArcsine, self).__init__(var, unit)


class NumArccosine(Arccosine, Numeric):
    def __init__(self, var, unit: str = 'rad'):
        super(NumArccosine, self).__init__(var, unit)


class NumArctangent(Arctangent, Numeric):
    def __init__(self, var, unit: str = 'rad'):
        super(NumArctangent, self).__init__(var, unit)


class StrSum(Sum, string):
    def __init__(self, addend_a, addend_b):
        super(StrSum, self).__init__(addend_a, addend_b)

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        a = str(a)
        b = str(b)
        return a + b


class StrProduct(Product, string):
    def __init__(self, factor_a, factor_b):
        super(StrProduct, self).__init__(factor_a, factor_b)

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        if ((isinstance(a, int) and isinstance(b, str))
            or (isinstance(a, str) and isinstance(b, int))):
            return a * b
        elif (isinstance(a, float) and isinstance(b, str)
              and abs(a - int(a)) <= 1e-3):
            a = int(a)
            return a * b
        elif (isinstance(b, float) and isinstance(a, str)
              and abs(b - int(b)) <= 1e-3):
            # 近似于整数的float型
            b = int(b)
            return a * b
        else:
            raise TypeError(f'无法理解的运算。收到了{type(a)}和{type(b)}的'
                            '两个变量')


class LogAnd(And, Logic):
    def __init__(self, a, b):
        super(LogAnd, self).__init__(a, b)


class LogOr(Or, Logic):
    def __init__(self, a, b):
        super(LogOr, self).__init__(a, b)


class LogNot(Not, Logic):
    def __init__(self, a):
        super(LogNot, self).__init__(a)

