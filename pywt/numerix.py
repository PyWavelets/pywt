# -*- coding: utf-8 -*-

# Copyright (c) 2006-2007 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

# $Id$

"""A thin wrapper for numeric libraries. Modify this to use wavelets with
libraries other than NumPy."""

from numpy import ndarray
from numpy import float64
from numpy import array as _array
from numpy import asarray, empty, zeros
from numpy import transpose

def contiguous_array_from_any(source):
    return _array(source, float64, ndmin=1) # ensure contiguous

def astype(source, dtype):
    return asarray(source, dtype)

def memory_buffer_object(size):
    return zeros((size,), float64)

def array(*args, **kwds):
    return _array(*args, **kwds)

def is_array_type(ar, typ):
    return isinstance(ar, ndarray) and ar.dtype == typ
    