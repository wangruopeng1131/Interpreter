#!/usr/bin/python3
# coding:utf8
"""
@Create date: 2021/12/7
@Author: 胡宏达
"""
import math
from math import (log, radians, degrees, sin, cos, tan, asin, acos, atan,
                  floor, ceil, trunc)


class BaseOperator(object):
    def __init__(self):
        super(BaseOperator, self).__init__()


class CartX(BaseOperator):
    def __init__(self, position):
        super(CartX, self).__init__()
        self.position = position
        if not getattr(position, 'dim'):
            raise TypeError("未知数据类型，希望传入一个位置类型的对象")
        if self.position.dim < 2:
            raise ValueError("传入坐标位置参数小于2")

    def __call__(self):
        x = self.position[0]() if callable(self.position[0]) else self.position[0]
        return x


class CartY(BaseOperator):
    def __init__(self, position):
        super(CartY, self).__init__()
        self.position = position
        if self.position.dim < 2:
            raise ValueError("传入坐标位置参数小于2")

    def __call__(self):
        y = self.position[1]() if callable(self.position[1]) else self.position[1]
        return y


class CartZ(BaseOperator):
    def __init__(self, position):
        super(CartZ, self).__init__()
        self.position = position
        if self.position.dim < 3:
            raise ValueError("传入坐标位置参数小于3")

    def __call__(self):
        z = self.position[2]() if callable(self.position[2]) else self.position[2]
        return z


class PolarRho(BaseOperator):
    def __init__(self, position):
        super(PolarRho, self).__init__()
        self.position = position
        if self.position.dim < 2:
            raise ValueError("传入坐标位置参数小于2")

    def __call__(self):
        x = self.position[0]() if callable(self.position[0]) else self.position[0]
        return x


class PolarPhi(BaseOperator):
    def __init__(self, position):
        super(PolarPhi, self).__init__()
        self.position = position
        if self.position.dim < 3:
            raise ValueError("传入坐标位置参数小于3")

    def __call__(self):
        phi = self.position[1]() if callable(self.position[1]) else self.position[1]
        return phi


class PolarTheta(BaseOperator):
    def __init__(self, position):
        super(PolarTheta, self).__init__()
        self.position = position
        if self.position.dim < 2:
            raise ValueError("传入坐标位置参数少于2")
        self.i = 1
        if self.position.dim == 3:
            self.i = 2

    def __call__(self):
        theta = self.position[self.i]() if callable(self.position[self.i]) else self.position[self.i]
        return theta


class SumNumericRGB(BaseOperator):
    def __init__(self, color_a, color_b):
        super(SumNumericRGB, self).__init__()
        self.color_a = color_a
        self.color_b = color_b

    def __call__(self):
        from .element import Numeric
        if isinstance(self.color_a, Numeric) and isinstance(self.color_b, Numeric):
            self.color_a = self.color_a() if callable(self.color_a) else self.color_a
            self.color_b = self.color_b() if callable(self.color_b) else self.color_b
            a_r, a_g, a_b = self.color_a
            b_r, b_g, b_b = self.color_b
            r = (a_r + b_r) / 2
            g = (a_g + b_g) / 2
            b = (a_b + b_b) / 2
            return r, g, b
        else:
            return NotImplemented


class SumstringRGB(BaseOperator):
    def __init__(self, color_a, color_b):
        super(SumstringRGB, self).__init__()
        self.color_a = color_a
        self.color_b = color_b

    def __call__(self):
        from .element import string
        if isinstance(self.color_a, string) and isinstance(self.color_b, string):
            self.color_a = self.color_a() if callable(self.color_a) else self.color_a
            self.color_b = self.color_b() if callable(self.color_b) else self.color_b
            if self.color_a.startswith("#"):
                color_a = self.color_a[1:].zfill(6)
                a_r = int(color_a[0:2], 16)
                a_g = int(color_a[2:4], 16)
                a_b = int(color_a[4:6], 16)
                color_b = self.color_b[1:].zfill(6)
                b_r = int(color_b[0:2], 16)
                b_g = int(color_b[2:4], 16)
                b_b = int(color_b[4:6], 16)
            else:
                color_a = self.color_a.zfill(6)
                a_r = int(color_a[0:2], 16)
                a_g = int(color_a[2:4], 16)
                a_b = int(color_a[4:6], 16)
                color_b = self.color_b.zfill(6)
                b_r = int(color_b[0:2], 16)
                b_g = int(color_b[2:4], 16)
                b_b = int(color_b[4:6], 16)
            r = (a_r + b_r) / 2
            g = (a_g + b_g) / 2
            b = (a_b + b_b) / 2
            return r, g, b
        else:
            raise ValueError("数据格式不合法")


class SumHSV(BaseOperator):
    def __init__(self, color):
        super(SumHSV, self).__init__()


class Offset(BaseOperator):
    def __init__(self, a, bias):
        super(Offset, self).__init__()
        if a.dim != bias.dim:
            raise ValueError("{}维坐标无法与{}维坐标计算计算".format(a.dim, bias.dim))
        if a.coord != bias.coord:
            raise ValueError("{}坐标无法与{}坐标计算".format(a.coord, bias.coord))
        self.a = a
        self.bias = bias
        self.coord = self.a.coord
        self.dim = self.a.dim

    def __call__(self):
        if self.dim == 2:
            if self.a.coord == 'cart':
                pass
            elif self.a.coord == 'polar':
                pass
        elif self.dim == 3:
            if self.coord == 'cart':
                pass
            elif self.coord == 'polar':
                pass
        return self.a + self.bias


class CartOffset2D(Offset):
    def __init__(self, a, b):
        super(CartOffset2D, self).__init__(a, b)
        self.x1 = a.x
        self.y1 = a.y
        self.x2 = b.x
        self.y2 = b.y

    def __call__(self):
        super(CartOffset2D, self).__call__()
        x1 = self.x1() if callable(self.x1) else self.x1
        y1 = self.y1() if callable(self.y1) else self.y1
        x2 = self.x2() if callable(self.x2) else self.x2
        y2 = self.y2() if callable(self.y2) else self.y2
        return x1 + x2, y1 + y2


class PolarOffset2D(Offset):
    def __init__(self, a, b):
        super(PolarOffset2D, self).__init__(a, b)
        self.rho1 = a.rho
        self.theta1 = a.theta
        self.rho2 = b.rho
        self.theta2 = b.theta

    def __call__(self):
        super(PolarOffset2D, self).__call__()
        rho1 = self.rho1() if callable(self.rho1) else self.rho1
        theta1 = self.theta1() if callable(self.theta1) else self.theta1
        rho2 = self.rho2() if callable(self.rho2) else self.rho2
        theta2 = self.theta2() if callable(self.theta2) else self.theta2
        return


class CartOffset3D(Offset):
    def __call__(self):
        super(CartOffset3D, self).__call__()


class PolarOffset3D(Offset):
    def __call__(self):
        super(PolarOffset3D, self).__call__()


class Compare(BaseOperator):
    def __init__(self, a, b):
        super(Compare, self).__init__()
        self.a = a
        self.b = b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        from .element import ComposedElement, Numeric, string
        if isinstance(a, (string, str)) and isinstance(b, (string, str)):
            if a == b:
                return 0
            else:
                return 1
        elif isinstance(a, ComposedElement) or (isinstance(b, ComposedElement)):
            return -1
        elif not isinstance(a, (Numeric, int, float, bool)) and not \
                isinstance(b, (Numeric, int, float, bool)):
            return NotImplemented
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


class And(BaseOperator):
    def __init__(self, a, b):
        super(And, self).__init__()
        self.a = a
        self.b = b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        return (a and b)


class Or(BaseOperator):
    def __init__(self, a, b):
        super(Or, self).__init__()
        self.a = a
        self.b = b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        return (a or b)


class Not(BaseOperator):
    def __init__(self, a):
        super(Not, self).__init__()
        self.a = a

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        return (not a)


class Positive(BaseOperator):
    def __init__(self, var):
        # 实现取正操作
        super(Positive, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return var


class Negative(BaseOperator):
    def __init__(self, var):
        # 实现取负操作
        super(Negative, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return -1 * var


class Absolute(BaseOperator):
    def __init__(self, var):
        super(Absolute, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return abs(var)


class Round(BaseOperator):
    def __init__(self, var, n: int = 0):
        # 实现内建函数 round() ，n 是近似小数点的位数
        super(Round, self).__init__()
        self.var = var
        self.n = n

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return round(var, self.n)


class Floor(BaseOperator):
    def __init__(self, var):
        # 实现 math.floor() 函数，即向下取整
        super(Floor, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return floor(var)


class Ceil(BaseOperator):
    def __init__(self, var):
        # 实现 math.ceil() 函数，即向上取整
        super(Ceil, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return ceil(var)


class Trunc(BaseOperator):
    def __init__(self, var):
        # 实现 math.trunc() 函数，即距离零最近的整数
        super(Trunc, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return trunc(var)


class Infinity(BaseOperator):
    # 无穷大
    def __init__(self, var):
        super(Infinity, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return True if var == math.inf else False


class Nan(BaseOperator):
    def __init__(self, var):
        super(Nan, self).__init__()
        self.var = var

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        return True if var == math.nan else False


class Sum(BaseOperator):
    def __init__(self, addend_a, addend_b):
        super(Sum, self).__init__()
        self.a = addend_a
        self.b = addend_b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        if isinstance(a, (int, float)):
            if isinstance(b, (int, float)):
                return a + b
            elif isinstance(b, str):
                return str(a) + b
        elif isinstance(a, str):
            if isinstance(b, (int, float)):
                return a + str(b)
            elif isinstance(b, str):
                return a + b
        else:
            return NotImplemented


class Difference(BaseOperator):
    def __init__(self, minuend, subtrahend):
        super(Difference, self).__init__()
        self.minuend = minuend
        self.subtrahend = subtrahend

    def __call__(self):
        minuend = self.minuend() if callable(self.minuend) else self.minuend
        subtrahend = (self.subtrahend() if callable(self.subtrahend)
                      else self.subtrahend)
        return minuend - subtrahend


class Product(BaseOperator):
    def __init__(self, factor_a, factor_b):
        super(Product, self).__init__()
        self.a = factor_a
        self.b = factor_b

    def __call__(self):
        a = self.a() if callable(self.a) else self.a
        b = self.b() if callable(self.b) else self.b
        return a * b


class Quotient(BaseOperator):
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


class FloorQuotient(BaseOperator):
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


class Remainder(BaseOperator):
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


class Power(BaseOperator):
    def __init__(self, base, exponent):
        super(Power, self).__init__()
        self.base = base
        self.exponent = exponent

    def __call__(self):
        base = self.base() if callable(self.base) else self.base
        exponent = (self.exponent() if callable(self.exponent)
                    else self.exponent)
        return base ** exponent


class Logarithmic(BaseOperator):
    def __init__(self, base, antilogarithm):
        super(Logarithmic, self).__init__()
        self.base = base
        self.antilogarithm = antilogarithm

    def __call__(self):
        base = self.base() if callable(self.base) else self.base
        antilogarithm = (self.antilogarithm() if callable(self.antilogarithm)
                         else self.antilogarithm)
        return log(antilogarithm, base)


class SquareRoot(BaseOperator):
    def __init__(self, base):
        super(SquareRoot, self).__init__()
        self.base = base

    def __call__(self):
        base = self.base() if callable(self.base) else self.base
        return math.sqrt(base)


class Sine(BaseOperator):
    def __init__(self, var, unit: str = 'rad'):
        super(Sine, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'deg' or self.unit.lower() == 'degree':
            var = radians(var)
        return sin(var)


class Cosine(BaseOperator):
    def __init__(self, var, unit: str = 'rad'):
        super(Cosine, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'deg' or self.unit.lower() == 'degree':
            var = radians(var)
        return cos(var)


class Tangent(BaseOperator):
    def __init__(self, var, unit: str = 'rad'):
        super(Tangent, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'deg' or self.unit.lower() == 'degree':
            var = radians(var)
        return tan(var)


class ArcSine(BaseOperator):
    def __init__(self, var, unit: str = 'rad'):
        super(ArcSine, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'rad' or self.unit.lower() == 'radian':
            return asin(var)
        else:
            return degrees(asin(var))


class ArcCosine(BaseOperator):
    def __init__(self, var, unit: str = 'rad'):
        super(ArcCosine, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'rad' or self.unit.lower() == 'radian':
            return acos(var)
        else:
            return degrees(acos(var))


class ArcTangent(BaseOperator):
    def __init__(self, var, unit: str = 'rad'):
        super(ArcTangent, self).__init__()
        self.var = var
        self.unit = unit

    def __call__(self):
        var = self.var() if callable(self.var) else self.var
        if self.unit.lower() == 'rad' or self.unit.lower() == 'radian':
            return atan(var)
        else:
            return degrees(atan(var))



