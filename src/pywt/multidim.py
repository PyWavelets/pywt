# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
2D Discrete Wavelet Transform and Inverse Discrete Wavelet Transform.
"""

__all__ = ['dwt2', 'idwt2', 'swt2', 'dwtn']

from itertools import izip, cycle

from _pywt import Wavelet, MODES
from _pywt import dwt, idwt, swt, downcoef
from numerix import transpose, array, as_float_array, default_dtype,\
    apply_along_axis


def dwt2(data, wavelet, mode='sym'):
    """
    2D Discrete Wavelet Transform.

    Parameters
    ----------
    data : array
        2D array with input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional (default: 'sym')
        Signal extension mode, see MODES

    Returns
    -------
    (cA, (cH, cV, cD)) : tuple
        approximation, horizontal detail, vertical detail and diagonal
        detail coefficients respectively.

    Examples
    --------
    >>> import numpy as np
    >>> data = np.ones((4,4), dtype=np.float64)
    >>> coeffs = dwt2(data, 'haar')
    >>> cA, (cH, cV, cD) = coeffs
    >>> print(cA)
    [[ 2.  2.]
     [ 2.  2.]]
    >>> print(cV)
    [[ 0.  0.]
     [ 0.  0.]]
    """

    data = as_float_array(data)
    if len(data.shape) != 2:
        raise ValueError("Expected 2D data array")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    mode = MODES.from_object(mode)

    # filter rows
    H, L = [], []
    for row in data:
        cA, cD = dwt(row, wavelet, mode)
        L.append(cA)
        H.append(cD)
    del data

    # filter columns
    H = transpose(H)
    L = transpose(L)

    LL, LH = [], []
    for row in L:
        cA, cD = dwt(array(row, default_dtype), wavelet, mode)
        LL.append(cA)
        LH.append(cD)
    del L

    HL, HH = [], []
    for row in H:
        cA, cD = dwt(array(row, default_dtype), wavelet, mode)
        HL.append(cA)
        HH.append(cD)
    del H

    # build result structure
    #     (approx.,        (horizontal,    vertical,       diagonal))
    ret = (transpose(LL), (transpose(LH), transpose(HL), transpose(HH)))

    return ret


def idwt2(coeffs, wavelet, mode='sym'):
    """
    2D Inverse Discrete Wavelet Transform. Reconstruct data from coefficients
    arrays.

    Parameters
    ----------
    coeffs : tuple
        (cA, (cH, cV, cD)) A tuple with approximation coefficients and three
        details coefficients 2D arrays like from `dwt2()`
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional (default: 'sym')
        Signal extension mode, see MODES

    Examples
    --------
    >>> import numpy as np
    >>> data = np.array([[1,2], [3,4]], dtype=np.float64)
    >>> coeffs = dwt2(data, 'haar')
    >>> print(idwt2(coeffs, 'haar'))
    [[ 1.  2.]
     [ 3.  4.]]
    """

    if len(coeffs) != 2 or len(coeffs[1]) != 3:
        raise ValueError("Invalid coeffs param")

    # L -low-pass data, H - high-pass data
    LL, (LH, HL, HH) = coeffs

    if LL is not None:
        LL = transpose(LL)
    if LH is not None:
        LH = transpose(LH)
    if HL is not None:
        HL = transpose(HL)
    if HH is not None:
        HH = transpose(HH)

    all_none = True
    for arr in (LL, LH, HL, HH):
        if arr is not None:
            all_none = False
            if len(arr.shape) != 2:
                raise TypeError("All input coefficients arrays must be 2D.")
    del arr
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
        for rowL, rowH in izip(LL, LH):
            L.append(idwt(rowL, rowH, wavelet, mode, 1))
    del LL, LH

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
        for rowL, rowH in izip(HL, HH):
            H.append(idwt(rowL, rowH, wavelet, mode, 1))
    del HL, HH

    if L is not None:
        L = transpose(L)
    if H is not None:
        H = transpose(H)

    # idwt rows
    data = []
    if L is None:
        # IDWT can handle None input values - equals to zero-array
        L = cycle([None])
    if H is None:
        # IDWT can handle None input values - equals to zero-array
        H = cycle([None])
    for rowL, rowH in izip(L, H):
        data.append(idwt(rowL, rowH, wavelet, mode, 1))

    return array(data, default_dtype)


def _downcoef(data, wavelet, mode, type):
    """Adapts pywt.downcoef call for apply_along_axis"""
    return downcoef(type, data, wavelet, mode, level=1)


def dwtn(data, wavelet, mode='sym'):
    """
    Single-level n-dimensional Discrete Wavelet Transform.

    Parameters
    ----------
    data : array
        nD array with input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional (default: 'sym')
        Signal extension mode, see MODES

    Returns
    -------
    [cAn, (cHn, cVn, cDn), ..., (cH1, cV1, cD1)] : array
    where n denotes the level of decomposition and cA, cH, cV and cD are
    approximation, horizontal detail, vertical detail and diagonal detail
    coefficients arrays respectively.

    Examples
    --------
    >>> import numpy as np
    >>> coeffs = wavedec2(np.ones((8,8)), 'db1', level=2)
    >>> cA2, (cH2, cV2, cD2), (cH1, cV1, cD1) = coeffs
    >>> print(cA2)
    [[ 4.  4.]
     [ 4.  4.]]

    Notes
    -----
    Results are arranged in a dictionary, where key specifies
    the transform type on each dimension and value is a n-dimensional
    coefficients array.

    For example, for a 2D case the result will look something like this:
        {
            'aa': <coeffs>  # A(LL) - approx. on 1st dim, approx. on 2nd dim
            'ad': <coeffs>  # H(LH) - approx. on 1st dim, det. on 2nd dim
            'da': <coeffs>  # V(HL) - det. on 1st dim, approx. on 2nd dim
            'dd': <coeffs>  # D(HH) - det. on 1st dim, det. on 2nd dim
        }
    """
    data = as_float_array(data)
    dim = len(data.shape)
    coeffs = [('', data)]
    for axis in range(dim):
        new_coeffs = []
        for subband, x in coeffs:
            new_coeffs.extend([
                (subband + 'a', apply_along_axis(_downcoef, axis,
                 x, wavelet, mode, 'a')),
                (subband + 'd', apply_along_axis(_downcoef, axis,
                 x, wavelet, mode, 'd'))
            ])
        coeffs = new_coeffs
    return dict(coeffs)


def swt2(data, wavelet, level, start_level=0):
    """
    2D Stationary Wavelet Transform.

    Parameters
    ----------
    data : array
        2D array with input data
    wavelet : Wavelet object or name string
        Wavelet to use
    level : int
        How many decomposition steps to perform
    start_level : int
        The level at which the decomposition will start

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
    for i in range(start_level, start_level + level):
        # filter rows
        H, L = [], []
        for row in data:
            cA, cD = swt(row, wavelet, level=1, start_level=i)[0]
            L.append(cA)
            H.append(cD)
        del data

        # filter columns
        H = transpose(H)
        L = transpose(L)

        LL, LH = [], []
        for row in L:
            cA, cD = swt(
                array(row, default_dtype), wavelet, level=1, start_level=i
            )[0]
            LL.append(cA)
            LH.append(cD)
        del L

        HL, HH = [], []
        for row in H:
            cA, cD = swt(
                array(row, default_dtype), wavelet, level=1, start_level=i
            )[0]
            HL.append(cA)
            HH.append(cD)
        del H

        # build result structure
        #     (approx.,        (horizontal,    vertical,       diagonal))
        approx = transpose(LL)
        ret.append((approx, (transpose(LH), transpose(HL), transpose(HH))))

        # for next iteration
        data = approx  # noqa

    return ret
