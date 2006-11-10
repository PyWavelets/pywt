# -*- coding: utf-8 -*-

# Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
# See COPYING for license details.

# $Id$

"""
Multilevel DWT and IDWT transforms.
"""

from _pywt import Wavelet, MODES, dwt, idwt, dwt_max_level

def wavedec(data, wavelet, level=None, mode='sym'):
    """
    Multilevel one-dimensional Discrete Wavelet Transform of data.
    Returns coefficient list - [cAn cDn cDn-1 ... cD2 cD1]

    data    - input data
    wavelet - wavelet to use (Wavelet object or name string)
    level   - decomposition level. If level is None then it will be
              calculated using `dwt_max_level` function.
    mode    - signal extension mode, see MODES
    """
    
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    
    if level is None:
        level = dwt_max_level(len(data), wavelet.dec_len)
    elif level < 0:
        raise ValueError, "Level value of %d is too low . Minimum '1' required." % level

    coeffs_list = []

    a = data
    for i in xrange(level):
        a, d = dwt(a, wavelet, mode)
        coeffs_list.append(d)
    
    coeffs_list.append(a)
    coeffs_list.reverse()
    
    return coeffs_list
    

def waverec(coeffs_list, wavelet, mode='sym'):
    """
    Multilevel one-dimensional IDWT of data from coefficients list.

    coeffs_list - coefficients list [cAn aDn cDn-1 ... cD2 cD1]
    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES
    """
    
    if not isinstance(coeffs_list, (list, tuple)):
        raise ValueError, "Expected sequence of coefficient arrays"
        
    if len(coeffs_list) < 2:
        raise ValueError, "Coefficient list too short (minimum 2 arrays required)"

    a, ds = coeffs_list[0], coeffs_list[1:]
    
    for d in ds:
        a = idwt(a, d, wavelet, mode, 1)
        
    return a

__all__ = ['wavedec', 'waverec']
