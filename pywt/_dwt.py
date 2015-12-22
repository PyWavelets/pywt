import numpy as np

from ._extensions._pywt import _check_dtype
from ._extensions._dwt import (dwt_single, dwt_axis, idwt_single, idwt_axis,
                               _upcoef, _downcoef, dwt_max_level, dwt_coeff_len)

__all__ = ["dwt", "idwt", "downcoef", "upcoef", "dwt_max_level", "dwt_coeff_len"]

def dwt(data, wavelet, mode='symmetric', axis=-1):
    """
    dwt(data, wavelet, mode='symmetric', axis=-1)

    Single level Discrete Wavelet Transform.

    Parameters
    ----------
    data : array_like
        Input signal
    wavelet : Wavelet object or name
        Wavelet to use
    mode : str, optional
        Signal extension mode, see Modes
    axis: int, optional
        Axis over which to compute the DWT. If not given, the
        last axis is used.


    Returns
    -------
    (cA, cD) : tuple
        Approximation and detail coefficients.

    Notes
    -----
    Length of coefficients arrays depends on the selected mode.
    For all modes except periodization:

        ``len(cA) == len(cD) == floor((len(data) + wavelet.dec_len - 1) / 2)``

    For periodization mode ("per"):

        ``len(cA) == len(cD) == ceil(len(data) / 2)``

    Examples
    --------
    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1, 2, 3, 4, 5, 6], 'db1')
    >>> cA
    array([ 2.12132034,  4.94974747,  7.77817459])
    >>> cD
    array([-0.70710678, -0.70710678, -0.70710678])

    """
    if np.iscomplexobj(data):
        data = np.asarray(data)
        cA_r, cD_r = dwt(data.real, wavelet, mode)
        cA_i, cD_i = dwt(data.imag, wavelet, mode)
        return  (cA_r + 1j*cA_i, cD_r + 1j*cD_i)

    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(data)
    data = np.array(data, dtype=dt)

    if axis >= data.ndim or abs(axis) > data.ndim:
        raise ValueError("Axis greater than data dimensions")

    # convert negative axes
    axis = axis % data.ndim

    if data.ndim == 1:
        cA, cD = dwt_single(data, wavelet, mode)
    else:
        cA, cD = dwt_axis(data, wavelet, mode, axis=axis)

    return (cA, cD)


def idwt(cA, cD, wavelet, mode='symmetric', axis=-1):
    """
    idwt(cA, cD, wavelet, mode='symmetric', axis=-1)

    Single level Inverse Discrete Wavelet Transform.

    Parameters
    ----------
    cA : array_like or None
        Approximation coefficients.  If None, will be set to array of zeros
        with same shape as `cD`.
    cD : array_like or None
        Detail coefficients.  If None, will be set to array of zeros
        with same shape as `cA`.
    wavelet : Wavelet object or name
        Wavelet to use
    mode : str, optional (default: 'symmetric')
        Signal extension mode, see Modes
    axis: int, optional
        Axis over which to compute the inverse DWT. If not given, the
        last axis is used.


    Returns
    -------
    rec: array_like
        Single level reconstruction of signal from given coefficients.

    """
    # accept array_like input; make a copy to ensure a contiguous array

    if cA is None and cD is None:
        raise ValueError("At least one coefficient parameter must be "
                         "specified.")

    # for complex inputs: compute real and imaginary separately then combine
    if ((cA is not None) and np.iscomplexobj(cA)) or ((cD is not None) and
            np.iscomplexobj(cD)):
        if cA is None:
            cD = np.asarray(cD)
            cA = np.zeros_like(cD)
        elif cD is None:
            cA = np.asarray(cA)
            cD = np.zeros_like(cA)
        return (idwt(cA.real, cD.real, wavelet, mode) +
                1j*idwt(cA.imag, cD.imag, wavelet, mode))

    if cA is not None:
        dt = _check_dtype(cA)
        cA = np.array(cA, dtype=dt)
    if cD is not None:
        dt = _check_dtype(cD)
        cD = np.array(cD, dtype=dt)

    if cA is not None and cD is not None:
        if cA.dtype != cD.dtype:
            # need to upcast to common type
            cA = cA.astype(np.float64)
            cD = cD.astype(np.float64)
    elif cA is None:
        cA = np.zeros_like(cD)
    elif cD is None:
        cD = np.zeros_like(cA)

    # cA and cD should be same dimension by here
    ndim = cA.ndim

    if axis >= ndim or abs(axis) > ndim:
        raise ValueError("Axis greater than coefficient dimensions")

    # convert negative axes
    axis = axis % ndim

    if ndim == 1:
        rec = idwt_single(cA, cD, wavelet, mode)
    else:
        rec = idwt_axis(cA, cD, wavelet, mode, axis=axis)

    return rec


def downcoef(part, data, wavelet, mode='symmetric', level=1):
    """
    downcoef(part, data, wavelet, mode='symmetric', level=1)

    Partial Discrete Wavelet Transform data decomposition.

    Similar to `pywt.dwt`, but computes only one set of coefficients.
    Useful when you need only approximation or only details at the given level.

    Parameters
    ----------
    part : str
        Coefficients type:

        * 'a' - approximations reconstruction is performed
        * 'd' - details reconstruction is performed

    data : array_like
        Input signal.
    wavelet : Wavelet object or name
        Wavelet to use
    mode : str, optional
        Signal extension mode, see `Modes`.  Default is 'symmetric'.
    level : int, optional
        Decomposition level.  Default is 1.

    Returns
    -------
    coeffs : ndarray
        1-D array of coefficients.

    See Also
    --------
    upcoef

    """
    if np.iscomplexobj(data):
        return (downcoef(part, data.real, wavelet, mode, level) +
                1j*downcoef(part, data.imag, wavelet, mode, level))
    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(data)
    data = np.array(data, dtype=dt)
    return _downcoef(part, data, wavelet, mode, level)


def upcoef(part, coeffs, wavelet, level=1, take=0):
    """
    upcoef(part, coeffs, wavelet, level=1, take=0)

    Direct reconstruction from coefficients.

    Parameters
    ----------
    part : str
        Coefficients type:
        * 'a' - approximations reconstruction is performed
        * 'd' - details reconstruction is performed
    coeffs : array_like
        Coefficients array to recontruct
    wavelet : Wavelet object or name
        Wavelet to use
    level : int, optional
        Multilevel reconstruction level.  Default is 1.
    take : int, optional
        Take central part of length equal to 'take' from the result.
        Default is 0.

    Returns
    -------
    rec : ndarray
        1-D array with reconstructed data from coefficients.

    See Also
    --------
    downcoef

    Examples
    --------
    >>> import pywt
    >>> data = [1,2,3,4,5,6]
    >>> (cA, cD) = pywt.dwt(data, 'db2', 'smooth')
    >>> pywt.upcoef('a', cA, 'db2') + pywt.upcoef('d', cD, 'db2')
    array([-0.25      , -0.4330127 ,  1.        ,  2.        ,  3.        ,
            4.        ,  5.        ,  6.        ,  1.78589838, -1.03108891])
    >>> n = len(data)
    >>> pywt.upcoef('a', cA, 'db2', take=n) + pywt.upcoef('d', cD, 'db2', take=n)
    array([ 1.,  2.,  3.,  4.,  5.,  6.])

    """
    if np.iscomplexobj(coeffs):
        return (upcoef(part, coeffs.real, wavelet, level, take) +
                1j*upcoef(part, coeffs.imag, wavelet, level, take))
    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(coeffs)
    coeffs = np.array(coeffs, dtype=dt)
    return _upcoef(part, coeffs, wavelet, level, take)
