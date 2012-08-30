# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
Multilevel 1D and 2D Discrete Wavelet Transform
and Inverse Discrete Wavelet Transform.
"""

__all__ = ['wavedec', 'waverec', 'wavedec2', 'waverec2']

from _pywt import Wavelet
from _pywt import dwt, idwt, dwt_max_level
from multidim import dwt2, idwt2
from numerix import as_float_array


def wavedec(data, wavelet, mode='sym', level=None):
    """
    Multilevel 1D Discrete Wavelet Transform of data.
    Returns coefficients list - [cAn, cDn, cDn-1, ..., cD2, cD1]

    data    - input data
    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES
    level   - decomposition level. If level is None then it will be
              calculated using `dwt_max_level` function.
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
    for i in xrange(level):
        a, d = dwt(a, wavelet, mode)
        coeffs_list.append(d)

    coeffs_list.append(a)
    coeffs_list.reverse()

    return coeffs_list


def waverec(coeffs, wavelet, mode='sym'):
    """
    Multilevel 1D Inverse Discrete Wavelet Transform.

    coeffs  - coefficients list [cAn, cDn, cDn-1, ..., cD2, cD1]
    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES
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

    data    - 2D input data
    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES
    level   - decomposition level. If level is None then it will be
              calculated using `dwt_max_level` function .

    Returns coefficients list - [cAn, (cHn, cVn, cDn), ... (cH1, cV1, cD1)]
    """

    data = as_float_array(data)

    if len(data.shape) != 2:
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
    for i in xrange(level):
        a, ds = dwt2(a, wavelet, mode)
        coeffs_list.append(ds)

    coeffs_list.append(a)
    coeffs_list.reverse()

    return coeffs_list


def waverec2(coeffs, wavelet, mode='sym'):
    """
    Multilevel 2D Inverse Discrete Wavelet Transform.

    coeffs  - coefficients list [cAn, (cHn, cVn, cDn), ... (cH1, cV1, cD1)]
    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES

    Returns 2D array of reconstructed data.
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
