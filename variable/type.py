# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 16:25:45 2021

@author: 赵匡是
"""
from math import floor, ceil, trunc

class BaseType(object):
    pass


class Numeric(BaseType):
    def __cmp__(self, other):
        # 在 self < other 时返回一个负整数
        # 在 self == other 时返回0
        # 在 self > other 时返回正整数
        if ((not isinstance(other, Numeric))
            or (not isinstance(other, (int, float)))):
            raise TypeError('数值类型的变量无法与其它类型的变量进行比较，但此处您'
                            f'希望比较一个数值变量和一个{type(other)}')
        from .cross import NumCompare
        return NumCompare(self, other)

    def __eq__(self, other):
        if ((not isinstance(other, Numeric))
            or (not isinstance(other, (int, float)))):
            raise TypeError('数值类型的变量无法与其它类型的变量进行比较，但此处您'
                            f'希望比较一个数值变量和一个{type(other)}')
        from .cross import NumEqual
        return NumEqual(self, other)

    def __ne__(self, other):
        if ((not isinstance(other, Numeric))
            or (not isinstance(other, (int, float)))):
            raise TypeError('数值类型的变量无法与其它类型的变量进行比较，但此处您'
                            f'希望比较一个数值变量和一个{type(other)}')
        from .cross import NumUnequal
        return NumUnequal(self, other)

    def __lt__(self, other):
        if ((not isinstance(other, Numeric))
            or (not isinstance(other, (int, float)))):
            raise TypeError('数值类型的变量无法与其它类型的变量进行比较，但此处您'
                            f'希望比较一个数值变量和一个{type(other)}')
        from .cross import NumLess
        return NumLess(self, other)

    def __gt__(self, other):
        if ((not isinstance(other, Numeric))
            or (not isinstance(other, (int, float)))):
            raise TypeError('数值类型的变量无法与其它类型的变量进行比较，但此处您'
                            f'希望比较一个数值变量和一个{type(other)}')
        from .cross import NumGreater
        return NumGreater(self, other)

    def __le__(self, other):
        if ((not isinstance(other, Numeric))
            or (not isinstance(other, (int, float)))):
            raise TypeError('数值类型的变量无法与其它类型的变量进行比较，但此处您'
                            f'希望比较一个数值变量和一个{type(other)}')
        from .cross import NumLessEqual
        return NumLessEqual(self, other)

    def __ge__(self, other):
        if ((not isinstance(other, Numeric))
            or (not isinstance(other, (int, float)))):
            raise TypeError('数值类型的变量无法与其它类型的变量进行比较，但此处您'
                            f'希望比较一个数值变量和一个{type(other)}')
        from .cross import NumGreaterEqual
        return NumGreaterEqual(self, other)

    def __pos__(self):
        # 实现取正操作
        from .cross import NumPositive
        return NumPositive(self)

    def __neg__(self):
        # 实现取负操作
        from .cross import NumNegative
        return NumNegative(self)

    def __abs__(self):
        # 实现内建绝对值函数 abs() 操作
        from .cross import NumAbsolute
        return NumAbsolute(self)

    def __round__(self, n: int = 0):
        # 实现内建函数 round() ，n 是近似小数点的位数
        from .cross import NumRound
        return NumRound(self, n)

    def __floor__(self):
        # 实现 math.floor() 函数，即向下取整
        from .cross import NumFloor
        return NumFloor(self)

    def __ceil__(self):
        # 实现 math.ceil() 函数，即向上取整
        from .cross import NumCeil
        return NumCeil(self)
        
    def __trunc__(self):
        # 实现 math.trunc() 函数，即距离零最近的整数
        from .cross import NumTrunc
        return NumTrunc(self)

    def __add__(self, other):
        # 实现加法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumSum
            return NumSum(self, other)
        elif isinstance(other, string) or isinstance(other, str):
            from .cross import StrSum
            return StrSum(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相加，但此处您'
                            f'希望将一个数值变量和一个{type(other)}相加')

    def __sub__(self, other):
        # 实现减法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumDifference
            return NumDifference(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相减，但此处您'
                            f'希望将一个数值变量和一个{type(other)}相减')

    def __mul__(self, other):
        # 实现乘法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumProduct
            return NumProduct(self, other)
        elif isinstance(other, string) or isinstance(other, str):
            from .cross import StrProduct
            return StrProduct(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相乘，但此处您'
                            f'希望将一个数值变量和一个{type(other)}相乘')

    def __floordiv__(self, other):
        # 实现使用 // 操作符的整数除法
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumFloorQuotient
            return NumFloorQuotient(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相除，但此处您'
                            f'希望将一个数值变量和一个{type(other)}相除')

    def __div__(self, other):
        # 实现使用 / 操作符的除法。
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumQuotient
            return NumQuotient(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相除，但此处您'
                            f'希望将一个数值变量和一个{type(other)}相除')

    def __mod__(self, other):
        # 实现 % 取余操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumRemainder
            return NumRemainder(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量取余，但此处您'
                            f'希望将一个数值变量和一个{type(other)}取余')

    def __pow__(self, other):
        # 实现 ** 操作符
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumPower
            return NumPower(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量乘方，但此处您'
                            f'希望将一个数值变量和一个{type(other)}乘方')

    def __radd__(self, other):
        # 实现反射加法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumSum
            return NumSum(self, other)
        elif isinstance(other, string) or isinstance(other, str):
            from .cross import StrSum
            return StrSum(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相加，但此处您'
                            f'希望将一个{type(other)}和一个数值变量相加')
    
    def __rsub__(self, other):
        # 实现反射减法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumDifference
            return NumDifference(other, self)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相减，但此处您'
                            f'希望将一个{type(other)}和一个数值变量相减')
    
    def __rmul__(self, other):
        # 实现反射乘法操作
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumProduct
            return NumProduct(self, other)
        elif isinstance(other, string) or isinstance(other, str):
            from .cross import StrProduct
            return StrProduct(self, other)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相乘，但此处您'
                            f'希望将一个{type(other)}和一个数值变量相乘')

    def __rfloordiv__(self, other):
        # 实现使用 // 操作符的整数反射除法
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumFloorQuotient
            return NumFloorQuotient(other, self)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相乘，但此处您'
                            f'希望将一个{type(other)}和一个数值变量相除')
    
    def __rdiv__(self, other):
        # 实现使用 / 操作符的反射除法
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumQuotient
            return NumQuotient(other, self)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相乘，但此处您'
                            f'希望将一个{type(other)}和一个数值变量相除')

    def __rmod__(self, other):
        # 实现 % 反射取余操作符
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumRemainder
            return NumRemainder(other, self)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量相乘，但此处您'
                            f'希望将一个{type(other)}和一个数值变量相除')

    def __rpow__(self, other):
        # 实现 ** 反射操作符
        if isinstance(other, Numeric) or isinstance(other, (int, float)):
            from .cross import NumPower
            return NumPower(other, self)
        else:
            raise TypeError('数值类型的变量无法与其它类型的变量乘方，但此处您'
                            f'希望将一个{type(other)}和一个数值变量乘方')


class string(BaseType):
    def __cmp__(self, other):
        # 在 self < other 时返回一个负整数
        # 在 self == other 时返回0
        # 在 self > other 时返回正整数
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            raise TypeError('字符串类型的变量无法与其它类型的变量进行比较，但此处'
                            f'您希望比较一个字符串变量和一个{type(other)}')
        from .cross import StrCompare
        return StrCompare(self, other)

    def __eq__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            raise TypeError('字符串类型的变量无法与其它类型的变量进行比较，但此处'
                            f'您希望比较一个字符串变量和一个{type(other)}')
        from .cross import StrEqual
        return StrEqual(self, other)

    def __ne__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            raise TypeError('字符串类型的变量无法与其它类型的变量进行比较，但此处'
                            f'您希望比较一个字符串变量和一个{type(other)}')
        from .cross import StrUnequal
        return StrUnequal(self, other)

    def __lt__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            raise TypeError('字符串类型的变量无法与其它类型的变量进行比较，但此处'
                            f'您希望比较一个字符串变量和一个{type(other)}')
        from .cross import NumLess
        return NumLess(self, other)

    def __gt__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            raise TypeError('字符串类型的变量无法与其它类型的变量进行比较，但此处'
                            f'您希望比较一个字符串变量和一个{type(other)}')
        from .cross import StrGreater
        return StrGreater(self, other)

    def __le__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            raise TypeError('字符串类型的变量无法与其它类型的变量进行比较，但此处'
                            f'您希望比较一个字符串变量和一个{type(other)}')
        from .cross import StrLessEqual
        return StrLessEqual(self, other)

    def __ge__(self, other):
        if (not isinstance(other, string)) or (not isinstance(other, str)):
            raise TypeError('字符串类型的变量无法与其它类型的变量进行比较，但此处'
                            f'您希望比较一个字符串变量和一个{type(other)}')
        from .cross import StrGreaterEqual
        return StrGreaterEqual(self, other)

    def __add__(self, other):
        # 实现加法操作
        if (isinstance(other, (Numeric, string))
            or isinstance(other, (int, float, str))):
            from .cross import StrSum
            return StrSum(self, other)
        else:
            raise TypeError('字符串类型的变量无法与其它类型的变量相加，但此处您'
                            f'希望将一个字符串变量和一个{type(other)}相加')

    def __mul__(self, other):
        # 实现乘法操作
        if (isinstance(other, (Numeric, string))
            or isinstance(other, (int, float, str))):
            from .cross import StrProduct
            return StrProduct(self, other)
        else:
            raise TypeError('字符串类型的变量无法与其它类型的变量相乘，但此处您'
                            f'希望将一个字符串变量和一个{type(other)}相乘')

    def __radd__(self, other):
        # 实现反射加法操作
        if (isinstance(other, (Numeric, string))
            or isinstance(other, (int, float, str))):
            from .cross import StrSum
            return StrSum(self, other)
        else:
            raise TypeError('字符串类型的变量无法与其它类型的变量相加，但此处您'
                            f'希望将一个{type(other)}和一个字符串变量相加')
    
    def __rmul__(self, other):
        # 实现反射乘法操作
        if (isinstance(other, (Numeric, string))
            or isinstance(other, (int, float, str))):
            from .cross import StrProduct
            return StrProduct(self, other)
        else:
            raise TypeError('字符串类型的变量无法与其它类型的变量相乘，但此处您'
                            f'希望将一个{type(other)}和一个字符串变量相乘')


class Position(BaseType):
    pass

class Color(BaseType):
    pass

class Size(BaseType):
    pass

class Logic(BaseType):
    pass