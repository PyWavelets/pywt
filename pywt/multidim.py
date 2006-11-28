# -*- coding: utf-8 -*-

# Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
# See COPYING for license details.

# $Id$

"""
2D Discrete Wavelet Transform and Inverse Discrete Wavelet Transform.
"""

__all__ = ['dwt2', 'idwt2']

from itertools import izip

from pywt import Wavelet, dwt, idwt, MODES
from numerix import transpose, array, asarray, float64


def dwt2(data, wavelet, mode='sym'):
    """
    2D Discrete Wavelet Transform.
    
    data    - 2D array with input data 
    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES
        
    Returns approximaion and three details 2D coefficients arrays.
    The result has the following form:
    
        (approximation, (horizontal det., vertical det., diagonal det.))
    """
    
    data = asarray(data, dtype=float64)
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
        cA, cD = dwt(array(row), wavelet, mode)
        append_LL(cA)
        append_LH(cD)
    del L
    
    HL, HH = [], []
    append_HL = HL.append; append_HH = HH.append
    for row in H:
        cA, cD = dwt(array(row), wavelet, mode)
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
    
    coeffs  - 2D coefficients arrays arranged in tuples:
    
        (approximation, (horizontal det., vertical det., diagonal det.))

    wavelet - wavelet to use (Wavelet object or name string)
    mode    - signal extension mode, see MODES
    """
    
    if len(coeffs) != 2 or len(coeffs[1]) != 3:
        raise ValueError("Invalid coeffs param")
    
    
    # L -low-pass data, H - high-pass data
    LL, (LH, HL, HH) = coeffs

    (LL, LH, HL, HH) = (transpose(LL), transpose(LH), transpose(HL), transpose(HH))
    for _ in (LL, LH, HL, HH):
        if len(_.shape) != 2:
            raise TypeError("All input coefficients arrays must be 2D")
    del _
    
    
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

    return array(data, float64)


