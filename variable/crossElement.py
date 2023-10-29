#!/usr/bin/python3
# coding:utf8
"""
@Create date: 2021/12/8
@Author: 胡宏达
"""
from .element import Logic, Numeric, string
from .operatorElement import CartOffset2D, PolarOffset2D, Equal, Sum


class CartNumericOffset2D(CartOffset2D, Logic):
    def __init__(self, a, b):
        super(CartNumericOffset2D, self).__init__()


class PolarNumericOffset2D(PolarOffset2D, Logic):
    def __init__(self, a, b):
        super(PolarNumericOffset2D, self).__init__()


class NumEqualCross(Equal, Logic):
    def __init__(self, a, b):
        super(NumEqualCross, self).__init__(a, b)


class StrEqualCross(Equal, Logic):
    def __init__(self, a, b):
        super(StrEqualCross, self).__init__(a, b)

