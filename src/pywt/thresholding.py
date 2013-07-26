# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
The thresholding helper module implements the most popular signal thresholding
functions.
"""

__all__ = ['soft', 'hard', 'greater', 'less', 'zero', 'copy']

import numerix


def soft(data, value, substitute=0):
    """
    Soft thresholding.

    Parameters
    ----------
    data : array
        Numeric data.
    value : double
        Thresholding value.
    substitute : double, optional (default: 0)
        Substitute value.

    Returns
    -------
    soft : array
        Result.

    Examples
    --------
    >>> import numpy as np
    >>> data = np.linspace(1, 4, 7)
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> soft(data, 2)
    array([ 0. ,  0. ,  0. ,  0.5,  1. ,  1.5,  2. ])
    """
    mvalue = -value

    cond_less = numerix.less(data, value)
    cond_greater = numerix.greater(data, mvalue)

    data = numerix.where(cond_less & cond_greater, substitute, data)
    data = numerix.where(cond_less, data + value, data)
    data = numerix.where(cond_greater, data - value, data)

    return data


def hard(data, value, substitute=0):
    """
    Hard thresholding. Replace all data values with substitute where their
    absolute value is less than the value param

    Data values with absolute value greater or equal to the thresholding value
    stay untouched.

    Parameters
    ----------
    data : array
        Numeric data.
    value : double
        Thresholding value.
    substitute : double, optional (default: 0)
        Substitute value.

    Returns
    -------
    hard : array
        Result.

    Examples
    --------
    >>> import numpy as np
    >>> data = np.linspace(1, 4, 7)
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> hard(data, 2)
    array([ 0. ,  0. ,  2. ,  2.5,  3. ,  3.5,  4. ])
    """
    mvalue = -value

    cond_less = numerix.less(data, value)
    cond_greater = numerix.greater(data, mvalue)

    data = numerix.where(cond_less & cond_greater, substitute, data)
    data = numerix.where(cond_less, data + value, data)
    data = numerix.where(cond_greater, data - value, data)
    mvalue = -value

    cond = numerix.less(data, value)
    cond &= numerix.greater(data, mvalue)

    return numerix.where(cond, substitute, data)


def greater(data, value, substitute=0):
    """
    Replace data with substitute where data is below the thresholding value.
    Greater data values pass untouched.

    Parameters
    ----------
    data : array
        Numeric data.
    value : double
        Thresholding value.
    substitute : double, optional (default: 0)
        Substitute value.

    Returns
    -------
    greater : array
        Result.

    Examples
    --------
    >>> import numpy as np
    >>> data = np.linspace(1, 4, 7)
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> greater(data, 2)
    array([ 0. ,  0. ,  2. ,  2.5,  3. ,  3.5,  4. ])
    """
    return numerix.where(numerix.less(data, value), substitute, data)


def less(data, value, substitute=0):
    """
    Replace data with substitute where data is above the thresholding value.
    Less data values pass untouched.

    Parameters
    ----------
    data : array
        Numeric data.
    value : double
        Thresholding value.
    substitute : double, optional (default: 0)
        Substitute value.

    Returns
    -------
    less : array
        Result.

    Examples
    --------
    >>> import numpy as np
    >>> data = np.linspace(1, 4, 7)
    array([ 1. ,  1.5,  2. ,  2.5,  3. ,  3.5,  4. ])
    >>> less(data, 2)
    array([ 1. ,  1.5,  2. ,  0. ,  0. ,  0. ,  0. ])
    """
    return numerix.where(numerix.greater(data, value), substitute, data)


def zero(data, *args):
    if isinstance(data, numerix.ndarray):
        return numerix.zeros(data.shape, data.dtype)
    return numerix.zeros(len(data))


def copy(data, *args):
    return numerix.array(data)
