# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""Thresholding routines"""

from __future__ import division, print_function, absolute_import

__all__ = ['soft', 'hard', 'greater', 'less', 'zero', 'copy']

import numpy as np


def soft(data, value, substitute=0):
    mvalue = -value

    cond_less = np.less(data, value)
    cond_greater = np.greater(data, mvalue)

    data = np.where(cond_less & cond_greater, substitute, data)
    data = np.where(cond_less, data + value, data)
    data = np.where(cond_greater, data - value, data)

    return data


def hard(data, value, substitute=0):
    mvalue = -value

    cond = np.less(data, value)
    cond &= np.greater(data, mvalue)

    return np.where(cond, substitute, data)


def greater(data, value, substitute=0):
    return np.where(np.less(data, value), substitute, data)


def less(data, value, substitute=0):
    return np.where(np.greater(data, value), substitute, data)


def zero(data, *args):
    if isinstance(data, np.ndarray):
        return np.zeros(data.shape, data.dtype)
    return np.zeros(len(data))


def copy(data, *args):
    return np.array(data)
