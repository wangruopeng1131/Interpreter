# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 10:16:29 2021

@author: 赵匡是
"""
import numpy as np


def integral_weight(weight: list, max_trial: int = 100,
                    approximate: bool = True):
    '''
    用倍数缩放来对权重序列进行化整。

    参数
    ----
    weight : list
        传入的权重序列，列表的元素可以为整数或是小数。
    max_trial : int, optional
        最大的尝试次数。默认是100，代表尝试100次。
    approximate: bool, optional
        是否进行近似估计，如果为True的话，则可以对原权重序列进行一定程度的近似来快速
        求得化整结果，化整结果未必是完全等比变化的；如果为False的话，则必须精确地等
        比缩放原序列，但是在一些比较复杂的权重序列中，可能会使化整结果特别大。默认为
        True。

    抛出
    ----
    StopIteration
        在设定的最大尝试次数内没有得到权重的最优解会抛出本异常。可能输入的权重的倍数
        关系是一个无理数，可以尝试将approximate参数设为True来取得近似的结果，或者将
        max_trial的数值改大。

    返回
    -------
    list
        化整后的权重序列。

    '''
    if approximate:
        threshold = 1e-2
    else:
        threshold = 1e-12
    weight = [i / min(weight) for i in weight]
    for f in range(1, max_trial):
        candidate = [i * f for i in weight]
        ctn = False
        for i in candidate:
            if abs(round(i) - i) >= threshold:  # 说明不是整数
                ctn = True
                break
        if ctn:
            continue
        else:
            return [round(i) for i in candidate]
    raise StopIteration('在有限次的尝试中，未能找到你输入的权重的最优解')


def normal_weight(weight: list):
    s = sum(weight)
    return [i / s for i in weight]

def lcm(a: int, b: int) ->int:
    '''
    计算两个整数的最小公倍数

    参数
    ----
    a : int
        整数a
    b : int
        整数b

    返回
    ----
    rst : int
        整数a和b的最小公倍数

    '''
    from math import gcd
    d = gcd(a, b)
    while d != 1:
        a //= d
        d = gcd(a,b)
    rst = (a * b)
    return rst