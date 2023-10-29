# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 16:52:40 2021

@author: 赵匡是
"""

class NotLoadedError(Exception):
    '''
    当一个需要预加载后才能调用的参数或方法在编译前就被调用时，抛出本错误。
    '''
    pass

class LoopError(Exception):
    '''
    当流程中的循环体无法配对时，抛出本错误。
    '''
    pass

class AlreadyLoadedError(Exception):
    '''
    当一个对象已经被预加载过，尝试再次预加载它时会抛出本错误。
    '''
    pass

class RoutineLogicError(Exception):
    '''
    当一个环节的内部结构存在逻辑错误时会抛出本错误。
    '''
    pass

class ConditionConflictError(Exception):
    '''
    当一个分段变量的多个条件会同时为真时会抛出本错误。
    '''
    pass

class ConditionInapplicableError(Exception):
    '''
    当一个分段变量的多个条件全为假时会抛出本错误。
    '''
    pass