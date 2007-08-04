# -*- coding: utf-8 -*-

# Copyright (c) 2006-2007 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

# $Id$

"""
Thin wrapper for numeric modules. Modify this to use wavelets with libraries other than NumPy.

Provides efficient mathematical functions and array datatypes.
"""

from numpy import ndarray, array, asarray
from numpy import empty, zeros, linspace, arange
from numpy import intp, float64
from numpy import transpose, concatenate
from numpy import cumsum, cos, diff, exp, sinc
from numpy import argmax, mean
from numpy import convolve
from numpy import where, less, greater

def contiguous_array_from_any(source):
    return array(source, float64, ndmin=1) # ensure contiguous

def astype(source, dtype):
    return asarray(source, dtype)

def memory_buffer_object(size):
    return zeros((size,), float64)

def is_array_type(arr, typ):
    return isinstance(arr, ndarray) and arr.dtype == typ

def keep(arr, keep_length):
    length = len(arr)
    if keep_length < length:
        left_bound = (length - keep_length) / 2
        return arr[left_bound:left_bound+keep_length]
    return arr
