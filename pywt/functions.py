# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
Other wavelet related functions.
"""

from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.fft import fft

from ._pywt import Wavelet


__all__ = ["intwave", "centfrq", "scal2frq", "qmf", "orthfilt"]


WAVELET_CLASSES = (Wavelet)


def wavelet_for_name(name):
    if not isinstance(name, str):
        raise TypeError(
            "Wavelet name must be of string type, not %s" % type(name))
    try:
        wavelet = Wavelet(name)
    except ValueError:
        raise ValueError("Invalid wavelet name - %s." % name)

    return wavelet


def _integrate(arr, step):
    integral = np.cumsum(arr)
    integral *= step
    return integral


def intwave(wavelet, precision=8):
    """
    Integrate `psi` wavelet function from -Inf to x using the rectangle
    integration method.

    Parameters
    ----------
    wavelet : Wavelet instance, str or tuple
        Wavelet to integrate.  If a string, should be the name of a wavelet.
        If a tuple, should contain ``(wavelet function approx., x grid)``.
    precision : int, optional
        Precision that will be used for wavelet function
        approximation computed with the wavefun(level=precision)
        Wavelet's method (default: 8).

    Returns
    -------
    [int_psi, x] :
        for orthogonal wavelets
    [int_psi_d, int_psi_r, x] :
        for other wavelets
    [int_function, x] :
        for (function approx., x grid) pair

    Notes
    -----
    (function_approx, x) :
        Function to integrate on the x grid. Used instead
        of Wavelet object to allow custom wavelet functions.

    Examples
    --------
    >>> import pywt
    >>> wavelet1 = pywt.Wavelet('db2')
    >>> [int_psi, x] = pywt.intwave(wavelet1, precision=5)
    >>> wavelet2 = pywt.Wavelet('bior1.3')
    >>> [int_psi_d, int_psi_r, x] = pywt.intwave(wavelet2, precision=5)

    """
    # FIXME: this function should really use scipy.integrate.quad

    if isinstance(wavelet, tuple):
        psi, x = np.asarray(wavelet[0]), np.asarray(wavelet[1])
        step = x[1] - x[0]
        return _integrate(psi, step), x

    else:
        if not isinstance(wavelet, WAVELET_CLASSES):
            wavelet = wavelet_for_name(wavelet)

        functions_approximations = wavelet.wavefun(precision)
        if len(functions_approximations) == 2:      # continuous wavelet
            psi, x = functions_approximations
            step = x[1] - x[0]
            return _integrate(psi, step), x
        elif len(functions_approximations) == 3:    # orthogonal wavelet
            phi, psi, x = functions_approximations
            step = x[1] - x[0]
            return _integrate(psi, step), x
        else:                                       # biorthogonal wavelet
            phi_d, psi_d, phi_r, psi_r, x = functions_approximations
            step = x[1] - x[0]
            return _integrate(psi_d, step), _integrate(psi_r, step), x


def centfrq(wavelet, precision=8):
    """
    Computes the central frequency of the `psi` wavelet function.

    Parameters
    ----------
    wavelet : Wavelet instance, str or tuple
        Wavelet to integrate.  If a string, should be the name of a wavelet.
        If a tuple, should contain ``(wavelet function approx., x grid)``.
    precision : int, optional
        Precision that will be used for wavelet function
        approximation computed with the wavefun(level=precision)
        Wavelet's method (default: 8).

    Returns
    -------
    scalar

    Notes
    -----
    (function_approx, xgrid) :
        Function defined on xgrid. Used instead
        of Wavelet object to allow custom wavelet functions.
    """

    # FIXME: `wavelet` handling should be identical to intwave, factor out
    if isinstance(wavelet, tuple):
        psi, x = np.asarray(wavelet[0]), np.asarray(wavelet[1])
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

    index = np.argmax(abs(fft(psi)[1:])) + 2
    if index > len(psi) / 2:
        index = len(psi) - index + 2

    return 1.0 / (domain / (index - 1))


def scal2frq(wavelet, scale, delta, precision=8):
    """

    Parameters
    ----------
    wavelet : Wavelet instance, str or tuple
        Wavelet to integrate.  If a string, should be the name of a wavelet.
        If a tuple, should contain ``(wavelet function approx., x grid)``.
    scale : scalar
    delta : scalar
        sampling
    precision : int, optional
        Precision that will be used for wavelet function approximation computed
        with ``wavelet.wavefun(level=precision)``.  Default is 8.

    Returns
    -------
    freq : scalar

    Notes
    -----
    (function_approx, xgrid) :
        Function defined on xgrid. Used instead
        of Wavelet object to allow custom wavelet functions.

    """
    return centfrq(wavelet, precision=precision) / (scale * delta)


def qmf(filter):
    """
    Returns the Quadrature Mirror Filter(QMF).

    The magnitude response of QMF is mirror image about `pi/2` of that of the
    input filter.

    Parameters
    ----------
    filter : array_like
        Input filter for which QMF needs to be computed.

    Returns
    -------
    qm_filter : ndarray
        Quadrature mirror of the input filter.

    """
    qm_filter = np.array(filter)[::-1]
    qm_filter[1::2] = -qm_filter[1::2]
    return qm_filter


def orthfilt(scaling_filter):
    """
    Returns the orthogonal filter bank.

    The orthogonal filter bank consists of the HPFs and LPFs at
    decomposition and reconstruction stage for the input scaling filter.

    Parameters
    ----------
    scaling_filter : array_like
        Input scaling filter (father wavelet).

    Returns
    -------
    orth_filt_bank : tuple of 4 ndarrays
        The orthogonal filter bank of the input scaling filter in the order :
        1] Decomposition LPF
        2] Decomposition HPF
        3] Reconstruction LPF
        4] Reconstruction HPF

    """
    if not (len(scaling_filter) % 2 == 0):
        raise ValueError("`scaling_filter` length has to be even.")

    scaling_filter = np.asarray(scaling_filter, dtype=np.float64)

    rec_lo = np.sqrt(2) * scaling_filter / np.sum(scaling_filter)
    dec_lo = rec_lo[::-1]

    rec_hi = qmf(rec_lo)
    dec_hi = rec_hi[::-1]

    orth_filt_bank = (dec_lo, dec_hi, rec_lo, rec_hi)
    return orth_filt_bank
