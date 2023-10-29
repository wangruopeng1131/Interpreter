#!/usr/bin/python3
# coding:utf8
"""
@Create date: 2021/12/8
@Author: 胡宏达
"""
from .baseElement import BaseElement
from .operatorElement import CartX, CartY, CartZ, PolarPhi, PolarRho, PolarTheta


class Numeric(BaseElement):
    def __cmp__(self, other):
        # 在 self < other 时返回一个负整数
        # 在 self == other 时返回0
        # 在 self > other 时返回正整数
        if ((not isinstance(other, Numeric))
                or (not isinstance(other, (int, float)))):
            return NotImplemented
        from .operatorElement import Compare
        return Compare(self, other)

    def __eq__(self, other):
        if ((not isinstance(other, Numeric))
                or (not isinstance(other, (int, float)))):
            return NotImplemented
        from .operatorElement import Equal
        return Equal(self, other)

    def __ne__(self, other):
        if ((not isinstance(other, Numeric))
                or (not isinstance(other, (int, float)))):
            return NotImplemented
        from .operatorElement import Unequal
        return Unequal(self, other)

    def __lt__(self, other):
        if ((not isinstance(other, Numeric))
                or (not isinstance(other, (int, float)))):
            return NotImplemented
        from .operatorElement import Less
        return Less(self, other)

    def __gt__(self, other):
        if ((not isinstance(other, Numeric))
                or (not isinstance(other, (int, float)))):
            return NotImplemented
        from .operatorElement import Greater
        return Greater(self, other)

    def __le__(self, other):
        if ((not isinstance(other, Numeric))
                or (not isinstance(other, (int, float)))):
            return NotImplemented
        from .operatorElement import LessEqual
        return LessEqual(self, other)

    def __ge__(self, other):
        if ((not isinstance(other, Numeric))
                or (not isinstance(other, (int, float)))):
            return NotImplemented
        from .operatorElement import GreaterEqual
        return GreaterEqual(self, other)

    def __pos__(self):
        # 实现取正操作
        from .operatorElement import Positive
        return Positive(self)

    def __neg__(self):
        # 实现取负操作
        from .operatorElement import Negative
        return Negative(self)

    def __abs__(self):
        # 实现内建绝对值函数 abs() 操作
        from .operatorElement import Absolute
        return Absolute(self)

    def __round__(self, n: int = 0):
        # 实现内建函数 round() ，n 是近似小数点的位数
        from .operatorElement import Round
        return Round(self, n)

    def __floor__(self):
        # 实现 math.floor() 函数，即向下取整
        from .operatorElement import Floor
        return Floor(self)

    def __ceil__(self):
        # 实现 math.ceil() 函数，即向上取整
        from .operatorElement import Ceil
        return Ceil(self)

    def __trunc__(self):
        # 实现 math.trunc() 函数，即距离零最近的整数
        from .operatorElement import Trunc
        return Trunc(self)

    def __add__(self, other):
        # 实现加法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Sum
            return Sum(self, other)
        elif isinstance(other, string) or isinstance(other, str):
            from .operatorElement import Sum
            return Sum(self, other)
        else:
            return NotImplemented

    def __sub__(self, other):
        # 实现减法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Difference
            return Difference(self, other)
        else:
            return NotImplemented

    def __mul__(self, other):
        # 实现乘法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Product
            return Product(self, other)
        elif isinstance(other, string) or isinstance(other, str):
            from .operatorElement import Product
            return Product(self, other)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        # 实现使用 // 操作符的整数除法
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import FloorQuotient
            return FloorQuotient(self, other)
        else:
            return NotImplemented

    def __truediv__(self, other):
        # 实现使用 / 操作符的除法。
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Quotient
            return Quotient(self, other)
        else:
            return NotImplemented

    def __mod__(self, other):
        # 实现 % 取余操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Remainder
            return Remainder(self, other)
        else:
            return NotImplemented

    def __pow__(self, other):
        # 实现 ** 操作符
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Power
            return Power(self, other)
        else:
            return NotImplemented

    def __radd__(self, other):
        # 实现反射加法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Sum
            return Sum(self, other)
        elif isinstance(other, string) or isinstance(other, str):
            from .operatorElement import Sum
            return Sum(self, other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        # 实现反射减法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Difference
            return Difference(other, self)
        else:
            return NotImplemented

    def __rmul__(self, other):
        # 实现反射乘法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Product
            return Product(self, other)
        elif isinstance(other, string) or isinstance(other, str):
            from .operatorElement import Product
            return Product(self, other)
        else:
            return NotImplemented

    def __rfloordiv__(self, other):
        # 实现使用 // 操作符的整数反射除法
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import FloorQuotient
            return FloorQuotient(other, self)
        else:
            return NotImplemented

    def __rdiv__(self, other):
        # 实现使用 / 操作符的反射除法
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Quotient
            return Quotient(other, self)
        else:
            return NotImplemented

    def __rmod__(self, other):
        # 实现 % 反射取余操作符
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Remainder
            return Remainder(other, self)
        else:
            return NotImplemented

    def __rpow__(self, other):
        # 实现 ** 反射操作符
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .operatorElement import Power
            return Power(other, self)
        else:
            return NotImplemented


class string(BaseElement):
    def __cmp__(self, other):
        # 在 self < other 时返回一个负整数
        # 在 self == other 时返回0
        # 在 self > other 时返回正整数
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            return NotImplemented
        from .operatorElement import Compare
        return Compare(self, other)

    def __eq__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            return NotImplemented
        from .operatorElement import Equal
        return Equal(self, other)

    def __ne__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            return NotImplemented
        from .operatorElement import Unequal
        return Unequal(self, other)

    def __lt__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            return NotImplemented
        from .operatorElement import Less
        return Less(self, other)

    def __gt__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            return NotImplemented
        from .operatorElement import Greater
        return Greater(self, other)

    def __le__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            return NotImplemented
        from .operatorElement import LessEqual
        return LessEqual(self, other)

    def __ge__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            return NotImplemented
        from .operatorElement import GreaterEqual
        return GreaterEqual(self, other)

    def __add__(self, other):
        # 实现加法操作
        if (isinstance(other, (Numeric, string))
                or isinstance(other, (int, float, str))):
            from .operatorElement import Sum
            return Sum(self, other)
        else:
            return NotImplemented

    def __mul__(self, other):
        # 实现乘法操作
        if (isinstance(other, (Numeric, string))
                or isinstance(other, (int, float, str))):
            from .operatorElement import Product
            return Product(self, other)
        else:
            return NotImplemented

    def __radd__(self, other):
        # 实现反射加法操作
        if (isinstance(other, (Numeric, string))
                or isinstance(other, (int, float, str))):
            from .operatorElement import Sum
            return Sum(self, other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        # 实现反射乘法操作
        if (isinstance(other, (Numeric, string))
                or isinstance(other, (int, float, str))):
            from .operatorElement import Product
            return Product(self, other)
        else:
            return NotImplemented


class ComposedElement(BaseElement):
    pass


class Height(BaseElement):
    def __call__(self):
        pass


class Width(BaseElement):
    def __call__(self):
        pass


class Depth(BaseElement):
    def __call__(self):
        pass


class Size(ComposedElement):
    """
    尺寸
    """
    def __init__(self):
        super(Size, self).__init__()
        self.width = Width()
        self.height = Height()
        self.depth = Depth()
        self.dim = 2

    def set_dim(self, new_dim):
        if not isinstance(new_dim, int):
            raise TypeError("需要传入一个整形数据")
        self.dim = new_dim

    def __len__(self):
        return self.dim

    def __getitem__(self, item):
        if item == 0:
            return self.width
        elif item == 1:
            return self.height
        else:
            raise ValueError("二维数据没有深度信息")


class Position(ComposedElement):
    def __init__(self):
        self.dim = 2
        self.coord = 'cart'
        self.__x = CartX(self)
        self.__y = CartY(self)
        self.__z = CartZ(self)
        self.__rho = PolarRho(self)
        self.__phi = PolarPhi(self)
        self.__theta = PolarTheta(self)

    def __getitem__(self, index):
        if index >= self.dim:
            raise IndexError(f'二维空间的坐标不存在第{index}维。')
        if index < 0:
            raise IndexError('list index out of range')
        if not isinstance(index, (int, slice)):
            return NotImplemented
        if self.coord == 'cart':
            if index == 0:
                return self.x
            if index == 1:
                return self.y
            if index == 2:
                return self.z
        if self.coord == 'polar':
            if index == 0:
                return self.rho
            elif index == 1:
                if self.dim == 3:
                    return self.phi
                elif self.dim == 2:
                    return self.theta
            elif index == 2:
                return self.theta

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        if self.dim < 3:
            raise IndexError('二维空间的坐标不存在z坐标。')
        return self.__z

    @property
    def rho(self):
        return self.__rho

    @property
    def phi(self):
        if self.dim < 3:
            raise IndexError('二维空间的坐标不存在phi坐标。')
        return self.__phi

    @property
    def theta(self):
        return self.__theta

    def __add__(self, other):
        if not isinstance(Position, other):
            return NotImplemented
        if self.dim == 2:
            if self.coord == "cart":
                from .crossElement import CartNumericOffset2D
                return CartNumericOffset2D(self, other)
            elif self.coord == "polar":
                from .crossElement import PolarNumericOffset2D
                return PolarNumericOffset2D(self, other)
        elif self.dim == 3:
            return NotImplemented

    def __radd__(self, other):
        if not isinstance(Position, other):
            return NotImplemented
        if self.dim == 2:
            if self.coord == "cart":
                from .crossElement import CartNumericOffset2D
                return CartNumericOffset2D(self, other)
            elif self.coord == "polar":
                from .crossElement import PolarNumericOffset2D
                return PolarNumericOffset2D(self, other)
        elif self.dim == 3:
            pass


class Color(ComposedElement):
    def __init__(self):
        super(Color, self).__init__()
        self.__RGB = RGBColor(self)
        self.__HSV = HSVColor(self)
        self.space = "RGB"

    def __len__(self):
        if self.space == "RGB" or self.space == "HSV":
            return 3

    def __getitem__(self, item):
        return item


class RGBColor(Color):
    def __init__(self, color):
        super(RGBColor, self).__init__()
        self.color = color

    def __len__(self):
        return len(self.color)

    def __add__(self, other):
        from .operatorElement import SumNumericRGB, SumstringRGB
        if isinstance(other, (Numeric, int, float)):
            return SumNumericRGB(self, other)
        elif isinstance(other, (string, str)):
            return SumstringRGB(self, other)

    def __radd__(self, other):
        from .operatorElement import SumNumericRGB, SumstringRGB
        if isinstance(other, (Numeric, int, float)):
            return SumNumericRGB(self, other)
        elif isinstance(other, (string, str)):
            return SumstringRGB(self, other)


class HSVColor(Color):
    def __init__(self, color):
        super(HSVColor, self).__init__()


class Logic(BaseElement):
    def __init__(self):
        super(Logic, self).__init__()
