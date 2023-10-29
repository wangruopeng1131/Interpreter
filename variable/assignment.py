# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 17:05:41 2021

@author: 赵匡是
"""
import logging
import traceback as tb
#from typing import Union

from .base import BaseVariable

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # TODO: 后期替换

class Assignment(BaseVariable):
    def __init__(self, expression, default = 0, name: str = None):
        super(Assignment, self).__init__('other', name = name)
        self._expression = expression
        self.value = default

    def __call__(self):
        return self.value

    def assign(self, *args, **kwargs):
        self.value = self._expression()
        logger.info(f'变量 {self.name} 被赋值为 {self.value}')