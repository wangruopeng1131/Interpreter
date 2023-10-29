# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:09:46 2021

@author: 赵匡是
"""

import logging
import traceback
import numpy as np
from math import ceil
from typing import Union
from random import uniform, gauss, vonmisesvariate

from .base import BaseVariable, Enumerable
from .manager import VariableManager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # TODO: 后期替换


class DiscreteVariable(BaseVariable, Enumerable):
    '''离散型的变量，一般会从自身内部进行抽取'''
    def __init__(self, population: list, mode = 'full random',
                 weight : list = None, refresh_moment : str = 'per inner loop',
                 random_seed: int = None, repeat_interval: int = 0,
                 least_succession: int = 1, most_succession : int = 100,
                 name: str = None, *args, **kwargs):
        BaseVariable.__init__(self, refresh_moment, random_seed, name=name)
        Enumerable.__init__(self, population, mode)
        self._current_seq = None
        self._previous_seq = None
        self._current = None
        for p in population:
            if isinstance(p, BaseVariable):
                self._variables.combine(p)
        self._seqs = self._get_seqs()  # 行数序号列表
        self._bind_table = False
        self._process_weight(weight)
        assert (least_succession is None) or (least_succession >= 1), ('无法理'
            '解小于1次的最小出现次数')
        assert ((least_succession is None) or (most_succession is None) or 
                least_succession <= most_succession), ('最小连续出现次数不得大于'
               f'最大连续出现次数，此处设定最小出现{least_succession}次，最大出现'
               f'{most_succession}次')
        self._least_succession = least_succession
        self._most_succession = most_succession

    def _get_seqs(self):
        return list(range(len(self._population)))

    def get(self, idx):
        return self._population[idx]

    def bind_table(self, mode : str = 'normal'):
        if mode == 'normal':
            self._bind_table = True
            self.set_moment('other')
        # FIXME: [start]为了兼容临时的列轮转逻辑的垃圾代码
        elif mode == 'column rotation':
            self._bind_table = True
            self.seqs = []
            self.set_moment('per call')  # 每一列都设为per call
        # FIXME: [end]为了兼容临时的列轮转逻辑的垃圾代码

    def refresh(self, seq: int = None):
        if seq is None:
            if len(self.seqs) == 0 and self._mode in ['random', 'sequential',
                                                      'full random']:
                logger.debug('当前离散变量{}重新抽样'.format(seq))
                self._create_sequence()
            elif len(self.seqs) == 0:
                return
            seq = self.seqs.pop(0)
            logger.debug('当前离散变量{}选取第{}行'.format(self.name, seq))
            #while self._current_seq is not None and seq == self._current_seq:
            #    self.seqs.append(seq)
            #    seq = self.seqs.pop(0)
            self._current_seq = seq
            self._current = self._population[seq]
        else:
            if seq >= 0 and seq < len(self._population):
                logger.debug('当前离散变量{}选取第{}行'.format(self.name, seq))
                self._current = self._population[seq]
            elif self._bind_table:
                return None
            else:
                logger.error('传入的序号{}超出了变量{}的取值范围。'.format(
                    self.name, seq))
                raise ValueError('传入的序号超出了变量的取值范围。')

    def preload(self, total_times: int = None):
        super(DiscreteVariable, self).preload(total_times)
        self._total_times = total_times
        # 检查条件
        if self._mode == 'full random' and self._total_times is None:
            logger.warning('无法确定具体的循环次数，所以采样模式将从'
                           '\'full random\'转为\'random\'。')
            self._mode = 'random'
        for i in self._variables:
            if callable(i):
                i.preload(total_times)
        if ((self._least_succession is not None) and (self._least_succession > 1) and
            (min(self._weight) < self._least_succession)):
            from .utils import lcm
            target = lcm(min(self._weight), self._least_succession)
            mult = target // min(self._weight)
            self._weight = [mult * w for w in self._weight]
        self._create_sequence()

    def __call__(self):
        if self._current is None and self._refresh_moment == 'per call':
            self.refresh()
        cur = self._current() if callable(self._current) else self._current
        logger.info('变量 {} 取值 {}'.format(self.name, cur))
        if self._refresh_moment == 'per call':
            self.refresh()
        return cur

    def _create_sequence(self):
        if self._mode == 'sequential':
            if len([i for i in self._weight if i > 0]) > 0:  # 如果权重不统一
                logger.warning('当前模式为顺序读取，不支持权重操作，已经忽略权重')
            self.seqs = self._seqs.copy()
        elif self._mode in ['random', 'full random']:
            meet_condition = False
            trial_count = 0
            while not meet_condition:
                trial_count += 1
                if trial_count > 100:
                    raise StopIteration(self.name + ' 尝试了100次仍无法找到符合要求的序列')
                if self._mode == 'random':
                    tem_seqs = self._rng.permutation(self._unit).tolist()
                elif self._mode == 'full random':
                    tem_seqs = np.repeat(self._unit,
                                ceil(self._total_times / self._unit_capacity))
                    tem_seqs = self._rng.permutation(tem_seqs).tolist()
                if self._previous_seq is not None:
                    test_seq = self._previous_seq + tem_seqs
                else:
                    test_seq = tem_seqs
                meet_condition = self._check_succession(test_seq)
            self.seqs = tem_seqs
            if self._most_succession is not None:
                self._previous_seq = tem_seqs[-1 * self._most_succession:]
            else:
                self._previous_seq = None
        else:
            self.seqs = []
        logger.debug(f'变量 {self.name} 随机后的顺序为：{self.seqs}')

    def _check_succession(self, sequence):
        last = None
        succession = 0
        for idx, seq in enumerate(sequence):
            if last is None:
                last = seq
                succession += 1
                continue
            if last == seq:
                succession += 1
                # 检查至多出现n次
                if (self._most_succession is not None and
                    succession > self._most_succession):
                    if self._weight[seq] < 0.5 * self._unit_capacity:
                        # 不检查出现多于0.5的元素
                        return False
            else:
                # 检查至少出现n次
                if (self._least_succession is not None and
                    succession < self._least_succession):
                    return False
                succession = 1
            last = seq
        return True

    def _process_weight(self, weight):
        if weight is None:  # 如果没有权重，说明是等权重的
            self._weight = [1] * len(self._seqs)
        else:
            weight = [int(i) for i in weight]
            if len(weight) != len(self._seqs):
                raise ValueError('传入的权重序列和离散变量的总体长度不等。传入的权重'
                                 f'序列为{self._weight}，而可选范围只有'
                                 f'{len(self._seqs)}个。')
            elif len([int(i) for i in weight if i <= 0]) > 0:
                # 检查所有的权重应当大于等于0
                raise ValueError('权重序列中不允许出现0，或小于0的数。')
            else:
                from .utils import integral_weight
                # 把所有的权重变为整数
                self._weight = integral_weight(weight)
        logger.info('变量 {} 的权重为 {}'.format(self.name, self._weight))
        unit = []
        self._unit_capacity = sum(self._weight)
        for weight, seq in zip(self._weight, self._seqs):
            unit.extend([seq] * weight)
        self._unit = unit

    def process_weight(self, weight):
        self._process_weight(weight)
        self._create_sequence()


class TableVariable(DiscreteVariable):
    # 表格变量一定是离散的（因为表格的坐标是离散的）
    # 表格变量的每一列都应当是离散的，而且它的列数应当相等
    def __init__(self, population: list, mode = 'random', weight : list = None,
                 refresh_moment: str = 'per inner loop',
                 random_seed: int = None, repeat_interval: int = 0,
                 least_succession: int = 1,
                 most_succession : int = 100, name: str = None,
                 *args, **kwargs):
        nrow = 0
        for col in population:
            assert isinstance(col, DiscreteVariable), ('传入列表变量的变量必须均'
                '为离散型的变量')
            nrow = max([nrow, len(col.population)])
            # FIXME: [start]为了兼容临时的列轮转逻辑的垃圾代码
            if refresh_moment == 'column rotation':
                col.bind_table('column rotation')
            else:
                col.bind_table()
            # FIXME: [end]为了兼容临时的列轮转逻辑的垃圾代码
        self._nrow = nrow
        self._seqs = self._get_seqs()
        super(TableVariable, self).__init__(population, mode, weight,
                                            refresh_moment,
                                            random_seed, name=name)
    def _get_seqs(self):
        return list(range(self._nrow))

    @property
    def population(self):
        return [i.population for i in self._population]

    def get(self, idx_row, idx_col):
        '''
        取二维表格中的单元格。

        参数
        ----
        idx_row : int
            行序号。以0开始。
        idx_col : int
            列序号。以0开始。

        返回
        ----
        单元格的内容，可能是一个任意类型的固定值，也可能是一个变量类型的引用值。

        '''
        return self._population[idx_col].population[idx_row]

    def refresh(self, seq: int = None):
        # FIXME: [start]为了兼容临时的列轮转逻辑的垃圾代码
        if self.refresh_moment == 'column rotation':
            self._create_sequence()
            for col in self._population:
                col.refresh()
            return
        # FIXME: [end]为了兼容临时的列轮转逻辑的垃圾代码
        if seq is None:
            if len(self.seqs) == 0 and self._mode in ['random', 'sequential',
                                                      'full random']:
                self._create_sequence()
            elif len(self.seqs) == 0:
                return
            seq = self.seqs.pop(0)
            '''
            while self._current_seq is not None and seq == self._current_seq:
                self.seqs.append(seq)
                seq = self.seqs.pop(0)
            '''
            self._current_seq = seq
            for col in self._population:
                col.refresh(seq)
            # self._current = self._population[seq]
        else:
            if seq >= 0 and seq < len(self._population):
                logger.debug('当前表格选取第{}行'.format(seq))
                for col in self._population:
                    col.refresh(seq)
            else:
                raise ValueError('传入的序号{}超出了变量的取值范围'.format(seq))

    def __call__(self):
        cur = [col() for col in self._population]
        if self._refresh_moment == 'per call':
            self.refresh()
        return cur

    def bind_table(self):
        raise AttributeError('表格无法再被绑定到表格中，请尝试绑定表格中的一列，'
                             '或者扩增本表格。')

    # FIXME: [start]为了兼容临时的列轮转逻辑的垃圾代码
    def _create_sequence(self) -> np.array:
        try:
            super()._create_sequence()
            if self.refresh_moment == 'column rotation':
                for col in self._population:
                    col.seqs = self.seqs.copy()
                    logger.info(f'变量 {col.name} 的随机顺序变为 {col.seqs}')
        except:
            tb = traceback.format_exc()
            logger.error('当前变量：{}'.format(self.name))
            logger.error(tb)
    # FIXME: [end]为了兼容临时的列轮转逻辑的垃圾代码
