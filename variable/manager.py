# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 13:13:45 2021

@author: 赵匡是
"""
from typing import Optional
from collections.abc import Iterable

# from .base import BaseVariable

class VariableManager(object):
    def __init__(self, variables: Optional[Iterable] = None):
        self._variables = list()
        if variables is not None:
            for v in variables:
                self.append(v)

    def __add__(self, value):
        assert isinstance(value, VariableManager)
        return self.copy().extend(value)

    def __contains__(self, key):
        return key in self._variables

    def __delitem__(self, key: int):
        var, mmt = self.pop(key)
        del var, mmt

    def __eq__(self, value):
        if not isinstance(value, VariableManager):
            return False
        return self._variables == value.variables

    def __getitem__(self, key: int):
        return (self._variables[key], self._variables[key].refresh_moment)

    def __iadd__(self, value):
        assert isinstance(value, VariableManager)
        self.extend(value)
        return self

    def __iter__(self):
        rst = []
        for var in self._variables:
            rst.append((var, var.refresh_moment))
        return iter(rst)

    def __len__(self):
        return len(self._variables)

    def __ne__(self, value):
        if not isinstance(value, VariableManager):
            return True
        return self._variables != value.variables

    def __repr__(self):
        rst = []
        for var in self._variables:
            rst.append((var, var.refresh_moment))
        return str(rst)

    def append(self, variable):
        # assert isinstance(variable, BaseVariable), ('VariableManager类只接受并'
        #                                             '管理变量类型')
        if variable not in self._variables:
            self._variables.append(variable)

    def clear(self):
        self._variables = list()

    def combine(self, variable):
        self.append(variable)
        self.extend(variable.variables)

    def copy(self):
        return VariableManager(self._variables)
            
    def extend(self, iterable):
        assert isinstance(iterable, VariableManager)
        self._variables += iterable.variables

    def insert(self, index: int, variable):
        # assert isinstance(variable, BaseVariable), ('VariableManager类只接受并'
        #                                             '管理变量类型')
        if variable not in self._variables:
            self._variables.insert(index, variable)

    def pop(self, index: int = -1, return_refresh_moment: bool = True):
        var = self._variables.pop(index)
        mmt = var.refresh_moment
        if return_refresh_moment:
            return (var, mmt)
        else:
            return var

    @property
    def refresh_moments(self):
        return [var.refresh_moment for var in self._variables]

    @property
    def variables(self):
        return self._variables
