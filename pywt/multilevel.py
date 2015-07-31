# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
Multilevel 1D and 2D Discrete Wavelet Transform
and Inverse Discrete Wavelet Transform.
"""

from __future__ import division, print_function, absolute_import

__all__ = ['wavedec', 'waverec', 'wavedec2', 'waverec2', 'iswt']

import numpy as np

from ._pywt import Wavelet
from ._pywt import dwt, idwt, dwt_max_level
from .multidim import dwt2, idwt2


def wavedec(data, wavelet, mode='sym', level=None):
    """
    Multilevel 1D Discrete Wavelet Transform of data.

    Parameters
    ----------
    data: array_like
        Input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see MODES (default: 'sym')
    level : int, optional
        Decomposition level. If level is None (default) then it will be
        calculated using `dwt_max_level` function.

    Returns
    -------
    [cA_n, cD_n, cD_n-1, ..., cD2, cD1] : list
        Ordered list of coefficients arrays
        where `n` denotes the level of decomposition. The first element
        (`cA_n`) of the result is approximation coefficients array and the
        following elements (`cD_n` - `cD_1`) are details coefficients arrays.

    Examples
    --------
    >>> from pywt import multilevel
    >>> coeffs = multilevel.wavedec([1,2,3,4,5,6,7,8], 'db1', level=2)
    >>> cA2, cD2, cD1 = coeffs
    >>> cD1
    array([-0.70710678, -0.70710678, -0.70710678, -0.70710678])
    >>> cD2
    array([-2., -2.])
    >>> cA2
    array([  5.,  13.])

    """

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    if level is None:
        level = dwt_max_level(len(data), wavelet.dec_len)
    elif level < 0:
        raise ValueError(
            "Level value of %d is too low . Minimum level is 0." % level)

    coeffs_list = []

    a = data
    for i in range(level):
        a, d = dwt(a, wavelet, mode)
        coeffs_list.append(d)

    coeffs_list.append(a)
    coeffs_list.reverse()

    return coeffs_list


def waverec(coeffs, wavelet, mode='sym'):
    """
    Multilevel 1D Inverse Discrete Wavelet Transform.

    Parameters
    ----------
    coeffs : array_like
        Coefficients list [cAn, cDn, cDn-1, ..., cD2, cD1]
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see MODES (default: 'sym')

    Examples
    --------
    >>> from pywt import multilevel
    >>> coeffs = multilevel.wavedec([1,2,3,4,5,6,7,8], 'db2', level=2)
    >>> multilevel.waverec(coeffs, 'db2')
    array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.])
    """

    if not isinstance(coeffs, (list, tuple)):
        raise ValueError("Expected sequence of coefficient arrays.")

    if len(coeffs) < 2:
        raise ValueError(
            "Coefficient list too short (minimum 2 arrays required).")

    a, ds = coeffs[0], coeffs[1:]

    for d in ds:
        a = idwt(a, d, wavelet, mode, 1)

    return a


def wavedec2(data, wavelet, mode='sym', level=None):
    """
    Multilevel 2D Discrete Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        2D input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see MODES (default: 'sym')
    level : int, optional
        Decomposition level. If level is None (default) then it will be
        calculated using `dwt_max_level` function.

    Returns
    -------
    [cAn, (cHn, cVn, cDn), ... (cH1, cV1, cD1)] : list
        Coefficients list

    Examples
    --------
    >>> from pywt import multilevel
    >>> coeffs = multilevel.wavedec2(np.ones((4,4)), 'db1')
    >>> # Levels:
    >>> len(coeffs)-1
    2
    >>> multilevel.waverec2(coeffs, 'db1')
    array([[ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.]])
    """

    data = np.asarray(data)

    if data.ndim != 2:
        raise ValueError("Expected 2D input data.")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    if level is None:
        size = min(data.shape)
        level = dwt_max_level(size, wavelet.dec_len)
    elif level < 0:
        raise ValueError(
            "Level value of %d is too low . Minimum level is 0." % level)

    coeffs_list = []

    a = data
    for i in range(level):
        a, ds = dwt2(a, wavelet, mode)
        coeffs_list.append(ds)

    coeffs_list.append(a)
    coeffs_list.reverse()

    return coeffs_list


def waverec2(coeffs, wavelet, mode='sym'):
    """
    Multilevel 2D Inverse Discrete Wavelet Transform.

    coeffs : array_like
        Coefficients list [cAn, (cHn, cVn, cDn), ... (cH1, cV1, cD1)]
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see MODES (default: 'sym')

    Returns
    -------
    2D array of reconstructed data.

    Examples
    --------
    >>> from pywt import multilevel
    >>> coeffs = multilevel.wavedec2(np.ones((4,4)), 'db1')
    >>> # Levels:
    >>> len(coeffs)-1
    2
    >>> multilevel.waverec2(coeffs, 'db1')
    array([[ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.]])
    """

    if not isinstance(coeffs, (list, tuple)):
        raise ValueError("Expected sequence of coefficient arrays.")

    if len(coeffs) < 2:
        raise ValueError(
            "Coefficient list too short (minimum 2 arrays required).")

    a, ds = coeffs[0], coeffs[1:]

    for d in ds:
        a = idwt2((a, d), wavelet, mode)

    return a

def iswt(coefficients, wavelet):
   """
     Input parameters:

       coefficients
         approx and detail coefficients, arranged in level value
         exactly as output from swt:
         e.g. [(cA1, cD1), (cA2, cD2), ..., (cAn, cDn)]

       wavelet
         Either the name of a wavelet or a Wavelet object

   """
   output = coefficients[0][0].copy() # Avoid modification of input data

   #num_levels, equivalent to the decomposition level, n
   num_levels = len(coefficients)
   for j in range(num_levels,0,-1):
       step_size = int(pow(2, j-1))
       last_index = step_size
       _, cD = coefficients[num_levels - j]
       for first in range(last_index): # 0 to last_index - 1

           # Getting the indices that we will transform
           indices = np.arange(first, len(cD), step_size)

           # select the even indices
           even_indices = indices[0::2]
           # select the odd indices
           odd_indices = indices[1::2]

           # perform the inverse dwt on the selected indices,
           # making sure to use periodic boundary conditions
           x1 = idwt(output[even_indices], cD[even_indices], wavelet, 'per')
           x2 = idwt(output[odd_indices], cD[odd_indices], wavelet, 'per')

           # perform a circular shift right
           x2 = np.roll(x2, 1)

           # average and insert into the correct indices
           output[indices] = (x1 + x2)/2.

   return output
