# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 15:31:07 2021

@author: 赵匡是
"""
import logging
from typing import Union

from .base import BaseVariable

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # TODO: 后期替换


class ContinuousVariable(BaseVariable):
    def __init__(self, refresh_moment : str = 'per inner loop', name: str = None):
        '''参考一些统计学分布'''
        super(ContinuousVariable, self).__init__(name=name)
        self.set_moment(refresh_moment)
        self.name = name

    def preload(self, total_times: int = None):
        super(ContinuousVariable, self).preload(total_times)
        self._total_times = total_times
        logger.debug(f'Total times: {self._total_times}')

    def __call__(self):
        cur = self._current
        if self._refresh_moment == 'per call':
            self.refresh()
        return cur


class UniformDistVariable(ContinuousVariable):
    def __init__(self, lower_bound: Union[int, float],
                 upper_bound: Union[int, float], return_int: bool = True,
                 refresh_moment : str = 'per inner loop',
                 random_seed: int = None, name : str = None):
        self._lower = lower_bound
        self._upper = upper_bound
        self._randint = return_int
        super(UniformDistVariable, self).__init__(refresh_moment, name = name)

    def refresh(self):
        self._current = self._rng.uniform(self._lower, self._upper)
        if self._randint:
            self._current = round(self._current)


class GaussDistVariable(ContinuousVariable):
    def __init__(self, mu: Union[int, float],
                 sigma: Union[int, float], return_int: bool = True,
                 refresh_moment : str = 'per inner loop',
                 random_seed: int = None):
        self._mu = mu
        self._sigma = sigma
        self._randint = return_int
        super(GaussDistVariable, self).__init__(refresh_moment)

    def refresh(self):
        self._current = self._rng.normal(self._mu, self._sigma)
        if self._randint:
            self._current = round(self._current)


class VonMisesDistVariable(ContinuousVariable):
    def __init__(self, mu: Union[int, float],
                 kappa: Union[int, float], return_int: bool = True,
                 refresh_moment : str = 'per inner loop',
                 random_seed: int = None, name : str = None):
        self._mu = mu
        self._kappa = kappa
        self._randint = return_int
        super(VonMisesDistVariable, self).__init__(refresh_moment, name=name)

    def refresh(self):
        self._current = self._rng.vonmises(self._mu, self._kappa)
        if self._randint:
            self._current = round(self._current)
