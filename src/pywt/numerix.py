# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
Thin wrapper for NumPy module. Modify this to use wavelets with libraries
other than NumPy.

Provides efficient numeric functions and array datatypes.
"""

from __future__ import division, print_function, absolute_import


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


def astype(source, dtype):
    return asarray(source, dtype)


def float64_memory_buffer_object(size):
    return zeros((size,), float64)


def float32_memory_buffer_object(size):
    return zeros((size,), float32)


def is_array_type(arr, typ):
    return isinstance(arr, ndarray) and arr.dtype == typ


def integrate(arr, step):
    integral = cumsum(arr)
    integral *= step
    return integral
