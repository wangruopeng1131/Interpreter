# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 14:36:59 2021

@author: 赵匡是
"""
from .base import BaseVariable, Enumerable


class ConstantVariable(BaseVariable, Enumerable):
    def __init__(self, value: object, mode: str = 'none', weight : list = None,
                 refresh_moment : str = 'other', random_seed: int = None, name: str = None,
                 *args, **kwargs):
        value = [value]
        BaseVariable.__init__(self, name=name)
        Enumerable.__init__(self, value, 'none')
        self._current_seq = None
        self.set_moment('other')

    def refresh(self, seq: int = None):
        pass  # 不做刷新

    def preload(self, total_times: int = None):
        super(ConstantVariable, self).preload(total_times)
        # 不做预加载

    def __call__(self):
        return (self._population[0]() if callable(self._population[0])
                else self._population[0])

    def _create_sequence(self):
        pass