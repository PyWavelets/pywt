# -*- coding: utf-8 -*-

# Copyright (c) 2006-2008 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

# $Id: $

"""
Continuous Wavelet Transform module.
"""

__all__ = ['cwt', 'CWavelet', 'cwavelist']

from math import sqrt, floor

from numerix import asarray, linspace
from numerix import intp
from numerix import concatenate, keep
from numerix import convolve, diff


from continuous_wavelets import cwavelist, function_for_name
from continuous_wavelets import *


class CWavelet(object):
    """

    """
    def __init__(self, name, psi=None, properties={}):
        self.name = name.lower()
        if psi is not None:
            self.psi, self.properties = psi, properties
        else:
            self.psi, self.properties = function_for_name(name)

    def wavefun(self, iter=10, points=None, lower_bound=None, upper_bound=None):
        if points is None:
            assert iter > 0
            points = 2**iter
        assert points > 0

        kwds = {}
        if lower_bound is not None:
            kwds["lower_bound"] = lower_bound
        if upper_bound is not None:
            kwds["upper_bound"] = upper_bound

        return self.psi(points, **kwds)


def cwt(data, wavelet, scales, data_step=1.0, precision=10):
    """
    cwt(data, wavelet, scales, data_step=1, precision=10)

    1D Continuous Wavelet Transform

    data        - 1D input data
    wavelet     - Wavelet name, CWavelet object or Wavelet object.
                  For convenience, a pair of (function_approximation, x_grid)
                  arrays can aslo be passed.
    scales      - List of scales at which the CWT will be computed.
                  Each scale must me in range (0 < scale < len(data)/2).
    data_step   - The distance between two neighbour points on the x-axis.
    precision   - Applicable only when wavelet *name*, *CWavelet* object
                  or *Wavelet* object is passed as the *wavelet* parameter
                  and is used to calculate the wavelet function approximation.
    """
    from functions import intwave

    data = asarray(data)
    if len(data.shape) != 1:
        raise ValueError("Expected 1D array, got %dD." % len(data.shape))
    if isinstance(scales, (int, float)):
        scales = [scales]
    elif not isinstance(scales, (list, tuple)):
        raise ValueError("Scales parameter must be a list or tuple of ints or floats, not %s." % type(scales))
    if not len(scales):
        raise ValueError("Scales parameter must be non-empty list of ints or floats.")
    if not (max(scales) < len(data)/2 and min(scales) > 0):
        raise ValueError("Scales values must be in range (0 < scale < len(data)/2).")

    # integrate wavelet function
    if isinstance(wavelet, tuple):
        psi, psi_x = wavelet
        assert len(psi) == len(psi_x)
        intwavefun, intwavefun_x = intwave((psi, psi_x))
    else:
        _intwavefun = intwave(wavelet, precision)
        intwavefun, intwavefun_x = _intwavefun[0], _intwavefun[-1]
        del _intwavefun

    intwavefun_step = intwavefun_x[1]-intwavefun_x[0]       # xgrid step
    intwavefun_x -= intwavefun_x[0]                         # shift xgrid to start in 0 point
    assert intwavefun_x[-1] > 0

    coeffs = []

    for scale in scales:
        scale = float(scale)
        resampled_intwavefun = resample(intwavefun, intwavefun_x, scale, data_step) # scale integrated wavelet function
        conv = convolve(data, resampled_intwavefun[::-1])   # match data against scaled function
        d = diff(conv)                                      # compute 1st derivative from coefficients
        c = keep(d, len(data))                              # keep only coefficients in range
        c *= -sqrt(scale)                                   # normalize coefficients according to scale
        coeffs.append(c)

    return coeffs


def resample(function, xgrid, scale, data_step):
    """Resample `function` defined on `xgrix` [0, x] using `scale`.
    """
    step = int(floor(scale / data_step * xgrid[-1])) + 1
    resampled = function[linspace(0, (len(xgrid)-1), step).astype(intp)]
    assert len(resampled) > 0
    if len(resampled) == 1:
        resampled = concatenate([resampled, resampled])
    return resampled
