from ._extensions._pywt import _check_dtype, Wavelet, Modes
from ._extensions._dwt import _dwt, _idwt, _upcoef, _downcoef

import numpy as np


def dwt(data, wavelet, mode='symmetric'):
    """
    (cA, cD) = dwt(data, wavelet, mode='symmetric')

    Single level Discrete Wavelet Transform.

    Parameters
    ----------
    data : array_like
        Input signal
    wavelet : Wavelet object or name
        Wavelet to use
    mode : str, optional (default: 'symmetric')
        Signal extension mode, see Modes

    Returns
    -------
    (cA, cD) : tuple
        Approximation and detail coefficients.

    Notes
    -----
    Length of coefficients arrays depends on the selected mode:
    for all modes except periodization:
        len(cA) == len(cD) == floor((len(data) + wavelet.dec_len - 1) / 2)
    for periodization mode ("per"):
        len(cA) == len(cD) == ceil(len(data) / 2)

    Examples
    --------
    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1, 2, 3, 4, 5, 6], 'db1')
    >>> cA
    [ 2.12132034  4.94974747  7.77817459]
    >>> cD
    [-0.70710678 -0.70710678 -0.70710678]

    """
    if np.iscomplexobj(data):
        data = np.asarray(data)
        cA_r, cD_r = dwt(data.real, wavelet, mode)
        cA_i, cD_i = dwt(data.imag, wavelet, mode)
        return (cA_r + 1j*cA_i, cD_r + 1j*cD_i)
    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(data)
    data = np.array(data, dtype=dt)
    if data.ndim != 1:
        raise ValueError("dwt requires a 1D data array.")

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    mode = Modes.from_object(mode)

    cA, cD = _dwt(data, wavelet, mode)
    return np.asarray(cA), np.asarray(cD)


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

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    mode = Modes.from_object(mode)
    return _downcoef(part, data, wavelet, mode, level)


def idwt(cA, cD, wavelet, mode='symmetric'):
    """
    idwt(cA, cD, wavelet, mode='symmetric')

    Single level Inverse Discrete Wavelet Transform

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
        if cA.ndim != 1:
            raise ValueError("idwt requires 1D coefficient arrays.")
    if cD is not None:
        dt = _check_dtype(cD)
        cD = np.array(cD, dtype=dt)
        if cD.ndim != 1:
            raise ValueError("idwt requires 1D coefficient arrays.")

    if cA is not None and cD is not None:
        if cA.dtype != cD.dtype:
            # need to upcast to common type
            cA = cA.astype(np.float64)
            cD = cD.astype(np.float64)
    elif cA is None:
        cA = np.zeros_like(cD)
    elif cD is None:
        cD = np.zeros_like(cA)

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    mode = Modes.from_object(mode)

    rec =  _idwt(cA, cD, wavelet, mode)
    return np.asarray(rec)


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
    [-0.25       -0.4330127   1.          2.          3.          4.          5.
      6.          1.78589838 -1.03108891]
    >>> n = len(data)
    >>> pywt.upcoef('a', cA, 'db2', take=n) + pywt.upcoef('d', cD, 'db2', take=n)
    [ 1.  2.  3.  4.  5.  6.]

    """
    if np.iscomplexobj(coeffs):
        return (upcoef(part, coeffs.real, wavelet, level, take) +
                1j*upcoef(part, coeffs.imag, wavelet, level, take))
    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(coeffs)
    coeffs = np.array(coeffs, dtype=dt)

    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    return _upcoef(part, coeffs, wavelet, level, take)
