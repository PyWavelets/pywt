# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""
Multilevel 1D and 2D Discrete Wavelet Transform
and Inverse Discrete Wavelet Transform.
"""

from __future__ import division, print_function, absolute_import

import numpy as np

from ._extensions._pywt import Wavelet
from ._extensions._dwt import dwt_max_level
from ._dwt import dwt, idwt
from ._multidim import dwt2, idwt2, dwtn, idwtn, _fix_coeffs

__all__ = ['wavedec', 'waverec', 'wavedec2', 'waverec2', 'wavedecn',
           'waverecn', 'iswt', 'iswt2']


def _check_level(size, dec_len, level):
    """
    Set the default decomposition level or check if requested level is valid.
    """
    if level is None:
        level = dwt_max_level(size, dec_len)
    elif level < 0:
        raise ValueError(
            "Level value of %d is too low . Minimum level is 0." % level)
    else:
        max_level = dwt_max_level(size, dec_len)
        if level > max_level:
            raise ValueError(
                "Level value of %d is too high.  Maximum allowed is %d." % (
                    level, max_level))
    return level


def wavedec(data, wavelet, mode='symmetric', level=None):
    """
    Multilevel 1D Discrete Wavelet Transform of data.

    Parameters
    ----------
    data: array_like
        Input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')
    level : int, optional
        Decomposition level (must be >= 0). If level is None (default) then it
        will be calculated using the ``dwt_max_level`` function.

    Returns
    -------
    [cA_n, cD_n, cD_n-1, ..., cD2, cD1] : list
        Ordered list of coefficients arrays
        where `n` denotes the level of decomposition. The first element
        (`cA_n`) of the result is approximation coefficients array and the
        following elements (`cD_n` - `cD_1`) are details coefficients arrays.

    Examples
    --------
    >>> from pywt import wavedec
    >>> coeffs = wavedec([1,2,3,4,5,6,7,8], 'db1', level=2)
    >>> cA2, cD2, cD1 = coeffs
    >>> cD1
    array([-0.70710678, -0.70710678, -0.70710678, -0.70710678])
    >>> cD2
    array([-2., -2.])
    >>> cA2
    array([  5.,  13.])

    """
    data = np.asarray(data)

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    level = _check_level(min(data.shape), wavelet.dec_len, level)

    coeffs_list = []

    a = data
    for i in range(level):
        a, d = dwt(a, wavelet, mode)
        coeffs_list.append(d)

    coeffs_list.append(a)
    coeffs_list.reverse()

    return coeffs_list


def waverec(coeffs, wavelet, mode='symmetric'):
    """
    Multilevel 1D Inverse Discrete Wavelet Transform.

    Parameters
    ----------
    coeffs : array_like
        Coefficients list [cAn, cDn, cDn-1, ..., cD2, cD1]
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')

    Examples
    --------
    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db1', level=2)
    >>> pywt.waverec(coeffs, 'db1')
    array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.])
    """

    if not isinstance(coeffs, (list, tuple)):
        raise ValueError("Expected sequence of coefficient arrays.")

    if len(coeffs) < 1:
        raise ValueError(
            "Coefficient list too short (minimum 1 arrays required).")
    elif len(coeffs) == 1:
        # level 0 transform (just returns the approximation coefficients)
        return coeffs[0]

    a, ds = coeffs[0], coeffs[1:]

    for d in ds:
        if (a is not None) and (d is not None) and (len(a) == len(d) + 1):
            a = a[:-1]
        a = idwt(a, d, wavelet, mode)

    return a


def wavedec2(data, wavelet, mode='symmetric', level=None):
    """
    Multilevel 2D Discrete Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        2D input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')
    level : int, optional
        Decomposition level (must be >= 0). If level is None (default) then it
        will be calculated using the ``dwt_max_level`` function.

    Returns
    -------
    [cAn, (cHn, cVn, cDn), ... (cH1, cV1, cD1)] : list
        Coefficients list

    Examples
    --------
    >>> import pywt
    >>> import numpy as np
    >>> coeffs = pywt.wavedec2(np.ones((4,4)), 'db1')
    >>> # Levels:
    >>> len(coeffs)-1
    2
    >>> pywt.waverec2(coeffs, 'db1')
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

    level = _check_level(min(data.shape), wavelet.dec_len, level)

    coeffs_list = []

    a = data
    for i in range(level):
        a, ds = dwt2(a, wavelet, mode)
        coeffs_list.append(ds)

    coeffs_list.append(a)
    coeffs_list.reverse()

    return coeffs_list


def waverec2(coeffs, wavelet, mode='symmetric'):
    """
    Multilevel 2D Inverse Discrete Wavelet Transform.

    coeffs : list or tuple
        Coefficients list [cAn, (cHn, cVn, cDn), ... (cH1, cV1, cD1)]
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')

    Returns
    -------
    2D array of reconstructed data.

    Examples
    --------
    >>> import pywt
    >>> import numpy as np
    >>> coeffs = pywt.wavedec2(np.ones((4,4)), 'db1')
    >>> # Levels:
    >>> len(coeffs)-1
    2
    >>> pywt.waverec2(coeffs, 'db1')
    array([[ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.],
           [ 1.,  1.,  1.,  1.]])
    """

    if not isinstance(coeffs, (list, tuple)):
        raise ValueError("Expected sequence of coefficient arrays.")

    if len(coeffs) < 1:
        raise ValueError(
            "Coefficient list too short (minimum 1 array required).")
    elif len(coeffs) == 1:
        # level 0 transform (just returns the approximation coefficients)
        return coeffs[0]

    a, ds = coeffs[0], coeffs[1:]
    a = np.asarray(a)

    for d in ds:
        d = tuple(np.asarray(coeff) if coeff is not None else None
                  for coeff in d)
        d_shapes = (coeff.shape for coeff in d if coeff is not None)
        try:
            d_shape = next(d_shapes)
        except StopIteration:
            idxs = slice(None), slice(None)
        else:
            if not all(s == d_shape for s in d_shapes):
                raise ValueError("All detail shapes must be the same length.")
            idxs = tuple(slice(None, -1 if a_len == d_len + 1 else None)
                         for a_len, d_len in zip(a.shape, d_shape))
        a = idwt2((a[idxs], d), wavelet, mode)

    return a


def iswt(coeffs, wavelet):
    """
    Multilevel 1D Inverse Discrete Stationary Wavelet Transform.

    Parameters
    ----------
    coeffs : array_like
        Coefficients list of tuples::

            [(cA1, cD1), (cA2, cD2), ..., (cAn, cDn)]

        where cA is approximation, cD is details, and n is start_level.
    wavelet : Wavelet object or name string
        Wavelet to use

    Returns
    -------
    1D array of reconstructed data.

    Examples
    --------
    >>> import pywt
    >>> coeffs = pywt.swt([1,2,3,4,5,6,7,8], 'db2', level=2)
    >>> pywt.iswt(coeffs, 'db2')
    array([ 1.,  2.,  3.,  4.,  5.,  6.,  7.,  8.])
    """

    output = coeffs[0][0].copy()  # Avoid modification of input data

    # num_levels, equivalent to the decomposition level, n
    num_levels = len(coeffs)
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    for j in range(num_levels, 0, -1):
        step_size = int(pow(2, j-1))
        last_index = step_size
        _, cD = coeffs[num_levels - j]
        for first in range(last_index):  # 0 to last_index - 1

            # Getting the indices that we will transform
            indices = np.arange(first, len(cD), step_size)

            # select the even indices
            even_indices = indices[0::2]
            # select the odd indices
            odd_indices = indices[1::2]

            # perform the inverse dwt on the selected indices,
            # making sure to use periodic boundary conditions
            x1 = idwt(output[even_indices], cD[even_indices],
                      wavelet, 'periodization')
            x2 = idwt(output[odd_indices], cD[odd_indices],
                      wavelet, 'periodization')

            # perform a circular shift right
            x2 = np.roll(x2, 1)

            # average and insert into the correct indices
            output[indices] = (x1 + x2)/2.

    return output


def iswt2(coeffs, wavelet):
    """
    Multilevel 2D Inverse Discrete Stationary Wavelet Transform.

    Parameters
    ----------
    coeffs : list
        Approximation and details coefficients::

            [
                (cA_1,
                    (cH_1, cV_1, cD_1)
                ),
                (cA_2,
                    (cH_2, cV_2, cD_2)
                ),
                ...,
                (cA_n
                    (cH_n, cV_n, cD_n)
                )
            ]

        where cA is approximation, cH is horizontal details, cV is
        vertical details, cD is diagonal details and n is number of
        levels.
    wavelet : Wavelet object or name string
        Wavelet to use

    Returns
    -------
    2D array of reconstructed data.

    Examples
    --------
    >>> import pywt
    >>> coeffs = pywt.swt2([[1,2,3,4],[5,6,7,8],
                            [9,10,11,12],[13,14,15,16]],
                           'db1', level=2)
    >>> pywt.iswt2(coeffs, 'db1')
    array([[  1.,   2.,   3.,   4.],
           [  5.,   6.,   7.,   8.],
           [  9.,  10.,  11.,  12.],
           [ 13.,  14.,  15.,  16.]])

    """

    output = coeffs[-1][0].copy()  # Avoid modification of input data

    # num_levels, equivalent to the decomposition level, n
    num_levels = len(coeffs)
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    for j in range(num_levels, 0, -1):
        step_size = int(pow(2, j-1))
        last_index = step_size
        _, (cH, cV, cD) = coeffs[j-1]
        # We are going to assume cH, cV, and cD are square and of equal size
        if (cH.shape != cV.shape) or (cH.shape != cD.shape) or (
                cH.shape[0] != cH.shape[1]):
            raise RuntimeError(
                "Mismatch in shape of intermediate coefficient arrays")
        for first_h in range(last_index):  # 0 to last_index - 1
            for first_w in range(last_index):  # 0 to last_index - 1
                # Getting the indices that we will transform
                indices_h = slice(first_h, cH.shape[0], step_size)
                indices_w = slice(first_w, cH.shape[1], step_size)

                even_idx_h = slice(first_h, cH.shape[0], 2*step_size)
                even_idx_w = slice(first_w, cH.shape[1], 2*step_size)
                odd_idx_h = slice(first_h + step_size, cH.shape[0], 2*step_size)
                odd_idx_w = slice(first_w + step_size, cH.shape[1], 2*step_size)

                # perform the inverse dwt on the selected indices,
                # making sure to use periodic boundary conditions
                x1 = idwt2((output[even_idx_h, even_idx_w],
                           (cH[even_idx_h, even_idx_w],
                            cV[even_idx_h, even_idx_w],
                            cD[even_idx_h, even_idx_w])),
                           wavelet, 'periodization')
                x2 = idwt2((output[even_idx_h, odd_idx_w],
                           (cH[even_idx_h, odd_idx_w],
                            cV[even_idx_h, odd_idx_w],
                            cD[even_idx_h, odd_idx_w])),
                           wavelet, 'periodization')
                x3 = idwt2((output[odd_idx_h, even_idx_w],
                           (cH[odd_idx_h, even_idx_w],
                            cV[odd_idx_h, even_idx_w],
                            cD[odd_idx_h, even_idx_w])),
                           wavelet, 'periodization')
                x4 = idwt2((output[odd_idx_h, odd_idx_w],
                           (cH[odd_idx_h, odd_idx_w],
                            cV[odd_idx_h, odd_idx_w],
                            cD[odd_idx_h, odd_idx_w])),
                           wavelet, 'periodization')

                # perform a circular shifts
                x2 = np.roll(x2, 1, axis=1)
                x3 = np.roll(x3, 1, axis=0)
                x4 = np.roll(x4, 1, axis=0)
                x4 = np.roll(x4, 1, axis=1)
                output[indices_h, indices_w] = (x1 + x2 + x3 + x4) / 4

    return output


def wavedecn(data, wavelet, mode='symmetric', level=None):
    """
    Multilevel nD Discrete Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        nD input data
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')
    level : int, optional
        Dxecomposition level (must be >= 0). If level is None (default) then it
        will be calculated using the ``dwt_max_level`` function.

    Returns
    -------
    [cAn, {details_level_n}, ... {details_level_1}] : list
        Coefficients list

    Examples
    --------
    >>> import numpy as np
    >>> from pywt import wavedecn, waverecn
    >>> coeffs = wavedecn(np.ones((4, 4, 4)), 'db1')
    >>> # Levels:
    >>> len(coeffs)-1
    2
    >>> waverecn(coeffs, 'db1')  # doctest: +NORMALIZE_WHITESPACE
    array([[[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]]])

    """
    data = np.asarray(data)

    if len(data.shape) < 1:
        raise ValueError("Expected at least 1D input data.")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)

    level = _check_level(min(data.shape), wavelet.dec_len, level)
    coeffs_list = []

    a = data
    for i in range(level):
        coeffs = dwtn(a, wavelet, mode)
        a = coeffs.pop('a' * data.ndim)
        coeffs_list.append(coeffs)

    coeffs_list.append(a)
    coeffs_list.reverse()

    return coeffs_list


def _match_coeff_dims(a_coeff, d_coeff_dict):
    # For each axis, compare the approximation coeff shape to one of the
    # stored detail coeffs and truncate the last element along the axis
    # if necessary.
    if a_coeff is None:
        return None
    if not d_coeff_dict:
        return a_coeff
    d_coeff = d_coeff_dict[next(iter(d_coeff_dict))]
    size_diffs = np.subtract(a_coeff.shape, d_coeff.shape)
    if np.any((size_diffs < 0) | (size_diffs > 1)):
        raise ValueError("incompatible coefficient array sizes")
    return a_coeff[[slice(s) for s in d_coeff.shape]]


def waverecn(coeffs, wavelet, mode='symmetric'):
    """
    Multilevel nD Inverse Discrete Wavelet Transform.

    coeffs : array_like
        Coefficients list [cAn, {details_level_n}, ... {details_level_1}]
    wavelet : Wavelet object or name string
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes (default: 'symmetric')

    Returns
    -------
    nD array of reconstructed data.

    Examples
    --------
    >>> import numpy as np
    >>> from pywt import wavedecn, waverecn
    >>> coeffs = wavedecn(np.ones((4, 4, 4)), 'db1')
    >>> # Levels:
    >>> len(coeffs)-1
    2
    >>> waverecn(coeffs, 'db1')  # doctest: +NORMALIZE_WHITESPACE
    array([[[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]],
           [[ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.],
            [ 1.,  1.,  1.,  1.]]])

    """
    if len(coeffs) < 1:
        raise ValueError(
            "Coefficient list too short (minimum 1 array required).")

    a, ds = coeffs[0], coeffs[1:]

    # Raise error for invalid key combinations
    ds = list(map(_fix_coeffs, ds))

    if not ds:
        # level 0 transform (just returns the approximation coefficients)
        return coeffs[0]
    if a is None and not any(ds):
        raise ValueError("At least one coefficient must contain a valid value.")

    coeff_ndims = []
    if a is not None:
        a = np.asarray(a)
        coeff_ndims.append(a.ndim)
    for d in ds:
        coeff_ndims += [v.ndim for k, v in d.items()]

    # test that all coefficients have a matching number of dimensions
    unique_coeff_ndims = np.unique(coeff_ndims)
    if len(unique_coeff_ndims) == 1:
        ndim = unique_coeff_ndims[0]
    else:
        raise ValueError(
            "All coefficients must have a matching number of dimensions")

    for idx, d in enumerate(ds):
        if a is None and not d:
            continue
        # The following if statement handles the case where the approximation
        # coefficient returned at the previous level may exceed the size of the
        # stored detail coefficients by 1 on any given axis.
        if idx > 0:
            a = _match_coeff_dims(a, d)
        d['a' * ndim] = a
        a = idwtn(d, wavelet, mode)

    return a
