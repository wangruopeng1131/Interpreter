from variable.cross import (NumSum, NumDifference, NumProduct, NumQuotient, NumFloorQuotient,
                           NumRemainder, NumPower, NumEqual, NumUnequal, NumGreater, NumLess, NumLessEqual,
                           NumGreaterEqual, LogAnd, LogOr, LogNot, NumPositive, NumNegative, NumAbsolute,
                           NumRound, NumFloor, NumCeil, NumTrunc, NumLogarithmic, NumSine, NumCosine, NumTangent,
                           NumArcsine, NumArccosine, NumArctangent, StrSum, StrProduct, StrGreaterEqual,
                           StrLessEqual, StrLess, StrGreater, StrUnequal, StrEqual
                            )

from variable.assignment import Assignment
from variable.operatorElement import (SumNumericRGB)
from variable.discrete import DiscreteVariable
from variable.continuous import UniformDistVariable, GaussDistVariable, VonMisesDistVariable

Reserved = {
    'if': 'if',
    'elif': 'elif',
    'else': 'else',
    'while': 'while',
    'break': 'break',
    'continue': 'continue',
    'for': 'for',
    'number': 'number',
    'set': 'set',
    'string': 'string',
    'id': 'id',
    'True': 'True',
    'False': 'False',
}

Assign = {
    '=': {'=': Assignment},
    '+=': None,
    '-=': None,
    '*=': None,
    '/=': None,
    '//=': None,
    '%=': None
}

# 双目运算符
BinaryOp = {
    '+': {'number': NumSum, 'string': StrSum, 'RGB': SumNumericRGB},
    '-': {'number': NumDifference, 'set': None},
    '*': {'number': NumProduct, 'string': StrProduct},
    '/': {'number': NumQuotient},
    '//': {'number': NumFloorQuotient},
    '%': {'number': NumRemainder},
    '^': {'number': NumPower},
    '==': {'number': NumEqual, 'string': StrEqual},
    '≠': {'number': NumUnequal, 'string': StrUnequal},
    '>': {'number': NumGreater, 'string': StrGreater},
    '<': {'number': NumLess, 'string': StrLess},
    '≤': {'number': NumLessEqual, 'string': StrLessEqual},
    '≥': {'number': NumGreaterEqual, 'string': StrGreaterEqual},
    'or': {'True': LogOr, 'False': LogOr},
    'and': {'True': LogAnd, 'False': LogAnd},
    'log': {'number': NumLogarithmic},
    '×': {'set': None},
    '|': {'set': None},
    '&': {'set': None}
}

# 单目运算符
UnaryOp = {
    'not': {'True': LogNot, 'False': LogNot},
    'pos': {'number': NumPositive},
    'neg': {'number': NumNegative},
    'abs': {'number': NumAbsolute},
    'round': {'number': NumRound},
    'floor': {'number': NumFloor},
    'ceil': {'number': NumCeil},
    'trunc': {'number': NumTrunc},
    'sin': {'number': NumSine},
    'cos': {'number': NumCosine},
    'tan': {'number': NumTangent},
    'arcsin': {'number': NumArcsine},
    'arccos': {'number': NumArccosine},
    'arctan': {'number': NumArctangent},
    'discrete': {'set': DiscreteVariable},
    'uniform': {'set': UniformDistVariable},
    'gauss': {'set': GaussDistVariable},
    'vonmises': {'set': VonMisesDistVariable}
}

# 界符
seperator = ['{', '}', '[', ']', '(', ')', ';', '?', ':', ',']