# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
Other wavelet related functions.
"""

__all__ = ["intwave", "centfrq", "scal2frq", "qmf", "orthfilt"]

from math import sqrt

from _pywt import Wavelet

from numerix import asarray, array, float64
from numerix import integrate
from numerix import argmax
from numerix import fft

WAVELET_CLASSES = (Wavelet)


def wavelet_for_name(name):
    if not isinstance(name, basestring):
        raise TypeError(
            "Wavelet name must be of string type, not %s" % type(name))
    try:
        wavelet = Wavelet(name)
    except ValueError:
        raise
        #raise ValueError("Invalid wavelet name - %s." % name)
    return wavelet


def intwave(wavelet, precision=8):
    """
    intwave(wavelet, precision=8) -> [int_psi, x]
        - for orthogonal wavelets

    intwave(wavelet, precision=8) -> [int_psi_d, int_psi_r, x]
        - for other wavelets

    intwave((function_approx, x), precision=8) -> [int_function, x]
        - for (function approx., x grid) pair

    Integrate *psi* wavelet function from -Inf to x using the rectangle
    integration method.

    wavelet         - Wavelet to integrate (Wavelet object, wavelet name string
                      or (wavelet function approx., x grid) pair)

    precision = 8   - Precision that will be used for wavelet function
                      approximation computed with the wavefun(level=precision)
                      Wavelet's method.

    (function_approx, x) - Function to integrate on the x grid. Used instead
                           of Wavelet object to allow custom wavelet functions.
    """

    if isinstance(wavelet, tuple):
        psi, x = asarray(wavelet[0]), asarray(wavelet[1])
        step = x[1] - x[0]
        return integrate(psi, step), x

    else:
        if not isinstance(wavelet, WAVELET_CLASSES):
            wavelet = wavelet_for_name(wavelet)

        functions_approximations = wavelet.wavefun(precision)
        if len(functions_approximations) == 2:      # continuous wavelet
            psi, x = functions_approximations
            step = x[1] - x[0]
            return integrate(psi, step), x
        elif len(functions_approximations) == 3:    # orthogonal wavelet
            phi, psi, x = functions_approximations
            step = x[1] - x[0]
            return integrate(psi, step), x
        else:                                       # biorthogonal wavelet
            phi_d, psi_d, phi_r, psi_r, x = functions_approximations
            step = x[1] - x[0]
            return integrate(psi_d, step), integrate(psi_r, step), x


def centfrq(wavelet, precision=8):
    """
    centfrq(wavelet, precision=8) -> float
        - for orthogonal wavelets

    centfrq((function_approx, x), precision=8) -> float
        - for (function approx., x grid) pair

    Computes the central frequency of the *psi* wavelet function.

    wavelet         - Wavelet (Wavelet object, wavelet name string
                      or (wavelet function approx., x grid) pair)
    precision = 8   - Precision that will be used for wavelet function
                      approximation computed with the wavefun(level=precision)
                      Wavelet's method.

    (function_approx, xgrid) - Function defined on xgrid. Used instead
                      of Wavelet object to allow custom wavelet functions.
    """

    if isinstance(wavelet, tuple):
        psi, x = asarray(wavelet[0]), asarray(wavelet[1])
    else:
        if not isinstance(wavelet, WAVELET_CLASSES):
            wavelet = wavelet_for_name(wavelet)
        functions_approximations = wavelet.wavefun(precision)

        if len(functions_approximations) == 2:
            psi, x = functions_approximations
        else:
            # (psi, x)   for (phi, psi, x)
            # (psi_d, x) for (phi_d, psi_d, phi_r, psi_r, x)
            psi, x = functions_approximations[1], functions_approximations[-1]

    domain = float(x[-1] - x[0])
    assert domain > 0

    index = argmax(abs(fft(psi)[1:])) + 2
    if index > len(psi) / 2:
        index = len(psi) - index + 2

    return 1.0 / (domain / (index - 1))


def scal2frq(wavelet, scale, delta, precision=8):
    """
    scal2frq(wavelet, scale, delta, precision=8) -> float
        - for orthogonal wavelets

    scal2frq(wavelet, scale, delta, precision=8) -> float
        - for (function approx., x grid) pair

    wavelet
    scale
    delta   - sampling
    """
    return centfrq(wavelet, precision=precision) / (scale * delta)


def qmf(filter):
    filter = array(filter)[::-1]
    filter[1::2] = -filter[1::2]
    return filter


def orthfilt(scaling_filter):
    assert len(scaling_filter) % 2 == 0

    scaling_filter = asarray(scaling_filter, dtype=float64)

    rec_lo = sqrt(2) * scaling_filter / sum(scaling_filter)
    dec_lo = rec_lo[::-1]

    rec_hi = qmf(rec_lo)
    dec_hi = rec_hi[::-1]

    return (dec_lo, dec_hi, rec_lo, rec_hi)
