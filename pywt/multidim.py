# -*- coding: utf-8 -*-

# Copyright (c) 2006-2008 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

# $Id$

"""
2D Discrete Wavelet Transform and Inverse Discrete Wavelet Transform.
"""

__all__ = ['dwt2', 'idwt2', 'swt2']

from itertools import izip

from _pywt import Wavelet, MODES
from _pywt import dwt, idwt, swt
from numerix import transpose, array, as_float_array, default_dtype


def dwt2(data, wavelet, mode='sym'):
    """
    2D Discrete Wavelet Transform.
    
    data    - 2D array with input data 
    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES
        
    Returns approximaion and three details 2D coefficients arrays.

    The result form four 2D coefficients arrays organized in tuples:
    
        (approximation,
                (horizontal details,
                vertical details,
                diagonal details)
        )
    
    which sometimes is also interpreted as layed out in one 2D array
    of coefficients, where:

                                -----------------
                                |       |       |
                                | A(LL) | H(LH) |
                                |       |       |
        (A, (H, V, D))  <--->   -----------------
                                |       |       |
                                | V(HL) | D(HH) |
                                |       |       |
                                -----------------
    """
    
    data = as_float_array(data)
    if len(data.shape) != 2:
        raise ValueError("Expected 2D data array")
    
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    mode = MODES.from_object(mode)
    
    # filter rows
    H, L = [], []
    append_L = L.append; append_H = H.append
    for row in data:
        cA, cD = dwt(row, wavelet, mode)
        append_L(cA)
        append_H(cD)
    del data
    
    # filter columns
    H = transpose(H)
    L = transpose(L)
 
    LL, LH = [], []
    append_LL = LL.append; append_LH = LH.append
    for row in L:
        cA, cD = dwt(array(row, default_dtype), wavelet, mode)
        append_LL(cA)
        append_LH(cD)
    del L
    
    HL, HH = [], []
    append_HL = HL.append; append_HH = HH.append
    for row in H:
        cA, cD = dwt(array(row, default_dtype), wavelet, mode)
        append_HL(cA)
        append_HH(cD)
    del H
    
    # build result structure
    #     (approx.,        (horizontal,    vertical,       diagonal))
    ret = (transpose(LL), (transpose(LH), transpose(HL), transpose(HH)))  
        
    return ret

def idwt2(coeffs, wavelet, mode='sym'):
    """
    2D Inverse Discrete Wavelet Transform. Reconstruct data from coefficients
    arrays.
    
    coeffs  - four 2D coefficients arrays arranged as follows:
    
        (approximation,
                (horizontal details,
                vertical details,
                diagonal details)
        )

    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES
    """
    
    if len(coeffs) != 2 or len(coeffs[1]) != 3:
        raise ValueError("Invalid coeffs param")
    
    # L -low-pass data, H - high-pass data
    LL, (LH, HL, HH) = coeffs

    (LL, LH, HL, HH) = (transpose(LL), transpose(LH), transpose(HL), transpose(HH))
    for arr in (LL, LH, HL, HH):
        if len(arr.shape) != 2:
            raise TypeError("All input coefficients arrays must be 2D")
    del arr
    
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    mode = MODES.from_object(mode)
    
    # idwt columns
    L = []
    append_L = L.append
    for rowL, rowH in izip(LL, LH):
        append_L(idwt(rowL, rowH, wavelet, mode, 1))
    del LL, LH

    H = []
    append_H = H.append
    for rowL, rowH in izip(HL, HH):
        append_H(idwt(rowL, rowH, wavelet, mode, 1))
    del HL, HH

    L = transpose(L)
    H = transpose(H)

    # idwt rows
    data = []
    append_data = data.append
    for rowL, rowH in izip(L, H):
        append_data(idwt(rowL, rowH, wavelet, mode, 1))

    return array(data, default_dtype)


def swt2(data, wavelet, level, start_level=0):
    """
    2D Stationary Wavelet Transform.
    
    data    - 2D array with input data 
    wavelet - wavelet to use (Wavelet object or name string)
    level   - how many decomposition steps to perform
    start_level - the level at which the decomposition will start
    
    Returns list of approximation and details coefficients:
    
        [
            (cA_n,
                (cH_n, cV_n, cD_n)
            ),
            (cA_n+1,
                (cH_n+1, cV_n+1, cD_n+1)
            ),
            ...,
            (cA_n+level,
                (cH_n+level, cV_n+level, cD_n+level)
            )
        ]

    where cA is approximation, cH is horizontal details, cV is
    vertical details, cD is diagonal details and n is start_level.
    """
    
    data = as_float_array(data)
    if len(data.shape) != 2:
        raise ValueError("Expected 2D data array")
    
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    ret = []
    for i in range(start_level, start_level+level):
        # filter rows
        H, L = [], []
        append_L = L.append; append_H = H.append
        for row in data:
            cA, cD = swt(row, wavelet, level=1, start_level=i)[0]
            append_L(cA)
            append_H(cD)
        del data
    
        # filter columns
        H = transpose(H)
        L = transpose(L)
 
        LL, LH = [], []
        append_LL = LL.append; append_LH = LH.append
        for row in L:
            cA, cD = swt(array(row, default_dtype), wavelet, level=1, start_level=i)[0]
            append_LL(cA)
            append_LH(cD)
        del L
    
        HL, HH = [], []
        append_HL = HL.append; append_HH = HH.append
        for row in H:
            cA, cD = swt(array(row, default_dtype), wavelet, level=1, start_level=i)[0]
            append_HL(cA)
            append_HH(cD)
        del H
    
        # build result structure
        #     (approx.,        (horizontal,    vertical,       diagonal))
        approx = transpose(LL)
        ret.append((approx, (transpose(LH), transpose(HL), transpose(HH))))
        
        data = approx # for next iteration
        
    return ret

