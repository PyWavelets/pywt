# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
2D Discrete Wavelet Transform and Inverse Discrete Wavelet Transform.
"""

from __future__ import division, print_function, absolute_import

__all__ = ['dwt2', 'idwt2', 'swt2', 'dwtn', 'idwtn']

from itertools import cycle, product, repeat, islice

import numpy as np

from ._pywt import Wavelet, MODES
from ._pywt import dwt, idwt, swt, downcoef, upcoef


def dwt2(data, wavelet, mode='sym'):
    """
    2D Discrete Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        2D array with input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see MODES (default: 'sym')

    Returns
    -------
    (cA, (cH, cV, cD)) : tuple
        Approximation, horizontal detail, vertical detail and diagonal
        detail coefficients respectively.

    Examples
    --------
    >>> import pywt
    >>> data = np.ones((4,4), dtype=np.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> cA, (cH, cV, cD) = coeffs
    >>> cA
    array([[ 2.,  2.],
           [ 2.,  2.]])
    >>> cV
    array([[ 0.,  0.],
           [ 0.,  0.]])

    """
    data = np.asarray(data)
    if data.ndim != 2:
        raise ValueError("Expected 2-D data array")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    mode = MODES.from_object(mode)

    # filter rows
    H, L = [], []
    for row in data:
        cA, cD = dwt(row, wavelet, mode)
        L.append(cA)
        H.append(cD)

    # filter columns
    H = np.transpose(H)
    L = np.transpose(L)

    LL, HL = [], []
    for row in L:
        cA, cD = dwt(np.array(row, np.float64), wavelet, mode)
        LL.append(cA)
        HL.append(cD)

    LH, HH = [], []
    for row in H:
        cA, cD = dwt(np.array(row, np.float64), wavelet, mode)
        LH.append(cA)
        HH.append(cD)

    # build result structure: (approx,
    #                          (horizontal, vertical, diagonal))
    ret = (np.transpose(LL),
           (np.transpose(HL), np.transpose(LH), np.transpose(HH)))

    return ret


def idwt2(coeffs, wavelet, mode='sym'):
    """
    2-D Inverse Discrete Wavelet Transform.

    Reconstructs data from coefficient arrays.

    Parameters
    ----------
    coeffs : tuple
        (cA, (cH, cV, cD)) A tuple with approximation coefficients and three
        details coefficients 2D arrays like from `dwt2()`
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see MODES (default: 'sym')

    Examples
    --------
    >>> import pywt
    >>> data = np.array([[1,2], [3,4]], dtype=np.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> pywt.idwt2(coeffs, 'haar')
    array([[ 1.,  2.],
           [ 3.,  4.]])

    """
    if len(coeffs) != 2 or len(coeffs[1]) != 3:
        raise ValueError("Invalid coeffs param")

    # L -low-pass data, H - high-pass data
    LL, (LH, HL, HH) = coeffs

    if LL is not None:
        LL = np.transpose(LL)
    if LH is not None:
        LH = np.transpose(LH)
    if HL is not None:
        HL = np.transpose(HL)
    if HH is not None:
        HH = np.transpose(HH)

    all_none = True
    for arr in (LL, LH, HL, HH):
        if arr is not None:
            all_none = False
            if arr.ndim != 2:
                raise TypeError("All input coefficients arrays must be 2D.")

    if all_none:
        raise ValueError(
            "At least one input coefficients array must not be None.")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    mode = MODES.from_object(mode)

    # idwt columns
    L = []
    if LL is None and LH is None:
        L = None
    else:
        if LL is None:
            # IDWT can handle None input values - equals to zero-array
            LL = cycle([None])
        if LH is None:
            # IDWT can handle None input values - equals to zero-array
            LH = cycle([None])
        for rowL, rowH in zip(LL, LH):
            L.append(idwt(rowL, rowH, wavelet, mode, 1))

    H = []
    if HL is None and HH is None:
        H = None
    else:
        if HL is None:
            # IDWT can handle None input values - equals to zero-array
            HL = cycle([None])
        if HH is None:
            # IDWT can handle None input values - equals to zero-array
            HH = cycle([None])
        for rowL, rowH in zip(HL, HH):
            H.append(idwt(rowL, rowH, wavelet, mode, 1))

    if L is not None:
        L = np.transpose(L)
    if H is not None:
        H = np.transpose(H)

    # idwt rows
    data = []
    if L is None:
        # IDWT can handle None input values - equals to zero-array
        L = cycle([None])
    if H is None:
        # IDWT can handle None input values - equals to zero-array
        H = cycle([None])
    for rowL, rowH in zip(L, H):
        data.append(idwt(rowL, rowH, wavelet, mode, 1))

    return np.array(data, np.float64)


def dwtn(data, wavelet, mode='sym'):
    """
    Single-level n-dimensional Discrete Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        n-dimensional array with input data.
    wavelet : Wavelet object or name string
        Wavelet to use.
    mode : str, optional
        Signal extension mode, see `MODES`.  Default is 'sym'.

    Returns
    -------
    coeffs : dict
        Results are arranged in a dictionary, where key specifies
        the transform type on each dimension and value is a n-dimensional
        coefficients array.

        For example, for a 2D case the result will look something like this::

            {'aa': <coeffs>  # A(LL) - approx. on 1st dim, approx. on 2nd dim
             'ad': <coeffs>  # V(LH) - approx. on 1st dim, det. on 2nd dim
             'da': <coeffs>  # H(HL) - det. on 1st dim, approx. on 2nd dim
             'dd': <coeffs>  # D(HH) - det. on 1st dim, det. on 2nd dim
            }

    """
    data = np.asarray(data)
    dim = data.ndim
    if dim < 1:
        raise ValueError("Input data must be at least 1D")
    coeffs = [('', data)]

    def _downcoef(data, wavelet, mode, type):
        """Adapts pywt.downcoef call for apply_along_axis"""
        return downcoef(type, data, wavelet, mode, level=1)

    for axis in range(dim):
        new_coeffs = []
        for subband, x in coeffs:
            new_coeffs.extend([
                (subband + 'a', np.apply_along_axis(_downcoef, axis, x,
                                                    wavelet, mode, 'a')),
                (subband + 'd', np.apply_along_axis(_downcoef, axis, x,
                                                    wavelet, mode, 'd'))])

        coeffs = new_coeffs

    return dict(coeffs)


def idwtn(coeffs, wavelet, mode='sym', take=None):
    """
    Single-level n-dimensional Discrete Wavelet Transform.

    Parameters
    ----------
    coeffs: dict
        Dictionary as in output of `dwtn`. Missing or None items
        will be treated as zeroes.
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode used in the decomposition,
        see MODES (default: 'sym'). Overridden by `take`.
    take : int or iterable of int or None, optional
        Number of values to take from the center of the idwtn for each axis.
        If 0, the entire reverse transformation will be used, including
        parts generated from padding in the forward transform.
        If None (default), will be calculated from `mode` to be the size of the
        original data, rounded up to the nearest multiple of 2.
        Passed to `upcoef`.

    Returns
    -------
    data: ndarray
        Original signal reconstructed from input data.

    """
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    mode = MODES.from_object(mode)

    # Ignore any invalid keys
    coeffs = dict((k, v) for k, v in coeffs.items() if set(k) <= set('ad'))
    dims = max(len(key) for key in coeffs.keys())

    try:
        coeff_shapes = (v.shape for k, v in coeffs.items()
                        if v is not None and len(k) == dims)
        coeff_shape = next(coeff_shapes)
    except StopIteration:
        raise ValueError("`coeffs` must contain at least one non-null wavelet "
                         "band")
    if any(s != coeff_shape for s in coeff_shapes):
        raise ValueError("`coeffs` must all be of equal size (or None)")

    if take is not None:
        try:
            takes = list(islice(take, dims))
            takes.reverse()
        except TypeError:
            takes = repeat(take, dims)
    else:
        # As in src/common.c
        if mode == MODES.per:
            takes = [2*s for s in reversed(coeff_shape)]
        else:
            takes = [2*s - wavelet.rec_len + 2 for s in reversed(coeff_shape)]

    def _upcoef(coeffs, wavelet, take, type):
        """Adapts pywt.upcoef call for apply_along_axis"""
        return upcoef(type, coeffs, wavelet, level=1, take=take)

    for axis, take in zip(reversed(range(dims)), takes):
        new_coeffs = {}
        new_keys = [''.join(coeff) for coeff in product('ad', repeat=axis)]

        for key in new_keys:
            L = coeffs.get(key + 'a')
            H = coeffs.get(key + 'd')

            if L is not None:
                L = np.apply_along_axis(_upcoef, axis, L, wavelet, take, 'a')

            if H is not None:
                H = np.apply_along_axis(_upcoef, axis, H, wavelet, take, 'd')

            if H is None and L is None:
                new_coeffs[key] = None
            elif H is None:
                new_coeffs[key] = L
            elif L is None:
                new_coeffs[key] = H
            else:
                new_coeffs[key] = L + H

        coeffs = new_coeffs

    return coeffs['']


def swt2(data, wavelet, level, start_level=0):
    """
    2D Stationary Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        2D array with input data
    wavelet : Wavelet object or name string
        Wavelet to use
    level : int
        How many decomposition steps to perform
    start_level : int, optional
        The level at which the decomposition will start (default: 0)

    Returns
    -------
    coeffs : list
        Approximation and details coefficients::

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
    data = np.asarray(data)
    if data.ndim != 2:
        raise ValueError("Expected 2D data array")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    ret = []
    for i in range(start_level, start_level + level):
        # filter rows
        H, L = [], []
        for row in data:
            cA, cD = swt(row, wavelet, level=1, start_level=i)[0]
            L.append(cA)
            H.append(cD)

        # filter columns
        H = np.transpose(H)
        L = np.transpose(L)

        LL, LH = [], []
        for row in L:
            cA, cD = swt(
                np.array(row, np.float64), wavelet, level=1, start_level=i
            )[0]
            LL.append(cA)
            LH.append(cD)

        HL, HH = [], []
        for row in H:
            cA, cD = swt(
                np.array(row, np.float64), wavelet, level=1, start_level=i
            )[0]
            HL.append(cA)
            HH.append(cD)

        # build result structure: (approx, (horizontal, vertical, diagonal))
        approx = np.transpose(LL)
        ret.append((approx,
                    (np.transpose(LH), np.transpose(HL), np.transpose(HH))))

        # for next iteration
        data = approx

    return ret
