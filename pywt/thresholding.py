# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
The thresholding helper module implements the most popular signal thresholding
functions.
"""

from __future__ import division, print_function, absolute_import

__all__ = ['soft', 'hard', 'greater', 'less']

import numpy as np


def soft(data, value, substitute=0):
    """
    Soft thresholding.

    Parameters
    ----------
    data : array_like
        Numeric data.
    value : scalar
        Thresholding value.
    substitute : double, optional
        Substitute value (default: 0).

    Returns
    -------
    soft : array
        Result.

    Examples
    --------
    >>> from pywt import thresholding
    >>> data = np.linspace(1, 4, 7)
    >>> data
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> thresholding.soft(data, 2)
    array([ 0. ,  0. ,  0. ,  0.5,  1. ,  1.5,  2. ])
    """
    mvalue = -value

    cond_less = np.less(data, value)
    cond_greater = np.greater(data, mvalue)

    data = np.where(cond_less & cond_greater, substitute, data)
    data = np.where(cond_less, data + value, data)
    data = np.where(cond_greater, data - value, data)

    return data


def hard(data, value, substitute=0):
    """
    Hard thresholding.

    Replace all data values with substitute where their
    absolute value is less than the value param.
    Data values with absolute value greater or equal to the thresholding value
    stay untouched.

    Parameters
    ----------
    data : array_like
        Numeric data.
    value : scalar
        Thresholding value.
    substitute : double, optional
        Substitute value (default: 0).

    Returns
    -------
    hard : array
        Result.

    Examples
    --------
    >>> from pywt import thresholding
    >>> data = np.linspace(1, 4, 7)
    >>> data
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> thresholding.hard(data, 2)
    array([ 0. ,  0. ,  2. ,  2.5,  3. ,  3.5,  4. ])
    """
    mvalue = -value

    cond = np.less(data, value)
    cond &= np.greater(data, mvalue)

    return np.where(cond, substitute, data)


def greater(data, value, substitute=0):
    """
    Replace data with substitute where data is below the thresholding value.
    Greater data values pass untouched.

    Parameters
    ----------
    data : array_like
        Numeric data.
    value : scalar
        Thresholding value.
    substitute : double, optional
        Substitute value (default: 0).

    Returns
    -------
    greater : array
        Result.

    Examples
    --------
    >>> from pywt import thresholding
    >>> data = np.linspace(1, 4, 7)
    >>> data
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> thresholding.greater(data, 2)
    array([ 0. ,  0. ,  2. ,  2.5,  3. ,  3.5,  4. ])
    """
    return np.where(np.less(data, value), substitute, data)


def less(data, value, substitute=0):
    """
    Replace data with substitute where data is above the thresholding value.
    Less data values pass untouched.

    Parameters
    ----------
    data : array_like
        Numeric data.
    value : scalar
        Thresholding value.
    substitute : double, optional
        Substitute value (default: 0).

    Returns
    -------
    less : array
        Result.

    Examples
    --------
    >>> from pywt import thresholding
    >>> data = np.linspace(1, 4, 7)
    >>> data
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> thresholding.less(data, 2)
    array([ 1. ,  1.5,  2. ,  0. ,  0. ,  0. ,  0. ])
    """
    return np.where(np.greater(data, value), substitute, data)
