# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 15:50:29 2021

@author: 赵匡是
"""
import logging
import traceback
import numpy as np
from math import ceil

from .manager import VariableManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # TODO: 后期替换

class BaseVariable(object):
    def __init__(self, refresh_moment : str = 'per inner loop',
                 random_seed: int = None, name: str = None):
        #super(BaseVariable, self).__init__()
        self.name = name
        self._variables = VariableManager()
        # === REFRESH MOMENT ===
        self.set_moment(refresh_moment)
        # === RANDOM SEED ===
        self._rng = np.random.default_rng(seed=random_seed)
        self._preloaded = False

    @property
    def refresh_moment(self):
        return self._refresh_moment

    @property
    def variables(self):
        return self._variables

    def set_moment(self, moment: str):
        assert moment in ['per inner loop', 'per outer loop', 'per call',
                          'column rotation', 'other']
        self._refresh_moment = moment
        logger.info('{} 的刷新时机为{}'.format(self.name, self._refresh_moment))

    def refresh(self, *args, **kwargs):
        pass

    def preload(self, total_times: int = None):
        if self._preloaded:
            return
        else:
            self._preloaded = True

    def __call__(self):
        pass


class Enumerable(object):
    def __init__(self, population: list, mode = 'full random'):
        self._population = population
        # super(Enumerable, self).__init__()
        assert mode in ['random', 'sequential', 'full random', 'staircase',
                        'interleaved staircase', 'none']
        self._mode = mode

    def __contains__(self, value):
        return value in self._population

    def __gt__(self, other):  # 大于
        if not callable(other):
            return min(self._population) > other
        elif isinstance(other, Enumerable):
            return min(self._population) > max(other.population)

    def __ge__(self, other):  # 大于等于
        if not callable(other):
            return min(self._population) >= other
        elif isinstance(other, Enumerable):
            return min(self._population) >= max(other.population)

    def __lt__(self, other):  # 小于：<
        if not callable(other):
            return max(self._population) < other
        elif isinstance(other, Enumerable):
            return max(self._population) < min(other.population)

    def __le__(self, other):  # 小于等于：<= 
        if not callable(other):
            return max(self._population) <= other
        elif isinstance(other, Enumerable):
            return max(self._population) <= min(other.population)

    def __len__(self):
        return len(self._population)

    def __eq__(self, other):  # 等于
        if type(self) != type(other):
            return False
        return self._population == other.population

    def __ne__(self, other):  # 不等于
        if type(self) != type(other):
            return True
        return self._population != other.population

    @property
    def population(self):
        rst = []
        for i in self._population:
            if not callable(i):
                rst.append(i)
            elif isinstance(i, Enumerable):
                rst.append(i.population)
        return rst

# 按照数据类型的Mixin，用来区分可加性可减性