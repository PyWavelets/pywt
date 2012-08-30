# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
Thin wrapper for NumPy module. Modify this to use wavelets with libraries
other than NumPy.

Provides efficient numeric functions and array datatypes.
"""

from numpy import (  # noqa
    ndarray, array, asarray,
    empty, zeros, linspace, arange,
    intp, float64, float32,
    transpose, concatenate,
    cumsum, cos, diff, exp, sinc, argmax, mean,
    convolve,
    where, less, greater,
    apply_along_axis
)
from numpy.fft import fft # noqa

default_dtype = float64


def as_float_array(source):
    if isinstance(source, ndarray) and source.dtype in [float64, float32]:
        return source
    return array(source, default_dtype)


def contiguous_float64_array_from_any(source):
    return array(source, float64)


def contiguous_float32_array_from_any(source):
    return array(source, float32)


def astype(source, dtype):
    return asarray(source, dtype)


def float64_memory_buffer_object(size):
    return zeros((size,), float64)


def float32_memory_buffer_object(size):
    return zeros((size,), float32)


def is_array_type(arr, typ):
    return isinstance(arr, ndarray) and arr.dtype == typ


def keep(arr, keep_length):
    length = len(arr)
    if keep_length < length:
        left_bound = (length - keep_length) / 2
        return arr[left_bound:left_bound + keep_length]
    return arr


def integrate(arr, step):
    integral = cumsum(arr)
    integral *= step
    return integral
