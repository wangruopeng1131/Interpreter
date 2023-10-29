# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 08:56:50 2021

@author: 赵匡是
"""

import logging
import traceback as tb
#from typing import Union

from .base import BaseVariable
from .exceptions import ConditionConflictError, ConditionInapplicableError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # TODO: 后期替换

class ReferentialVariable(BaseVariable):
    def __init__(self, expression, annotation: str, default = 0,
                 name: str = None):
        super(ReferentialVariable, self).__init__('other', name = name)
        self._expression = expression
        self._annotation = annotation
        self._default = default

    def __call__(self):
        try:
            return self._expression()
        except:
            logger.warning(f'变量 {self.name} 无法取到值，'
                           f'将返回默认值 {self.default}。具体错误信息如下：')
            logger.warning(tb.format_exc())
            return self._default


class PiecewiseVariable(BaseVariable):
    def __init__(self, content: list, annotation: list, name: str = None):
        super(PiecewiseVariable, self).__init__('other', name = name)
        self._conditions = []
        self._values = []
        self._conditions_annotation = []
        self._values_annotation = []
        for cond, value in content:
            self._conditions.append(cond)
            self._values.append(value)
        for cond, value in annotation:
            self._conditions_annotation.append(cond)
            self._values_annotation.append(value)
        # TODO: 检查conditions是否包含全集

    def __call__(self):
        piece = None
        for i, cond in enumerate(self._conditions):
            c = cond()
            if c and piece is None:
                piece = i
            elif c:
                raise ConditionConflictError(f'变量 {self.name} 的条件存在冲突，'
                    f'\'{self._conditions_annotation[piece]}\' 和 '
                    f'\'{self._conditions_annotation[i]}\' 可能同时为真')
        if piece is None:
            raise ConditionInapplicableError(f'变量 {self.name} 的条件无法覆盖'
                                             '全部的已知情况。')