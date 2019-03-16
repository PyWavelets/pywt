from functools import partial, reduce

import numpy as np

from ._swt import swt, iswt, swt2, iswt2, swtn, iswtn
from ._multilevel import (wavedec, waverec, wavedec2, waverec2, wavedecn,
                          waverecn, _prep_axes_wavedecn)
from ._utils import _wavelets_per_axis, _modes_per_axis


__all__ = ["mra", "mra2", "mran"]


def mra(data, wavelet, level=None, axis=-1, transform='swt',
        mode='periodization'):

    if transform == 'swt':
        if mode != 'periodization':
            raise ValueError(
                "transform swt only supports mode='periodization'")
        kwargs = dict(wavelet=wavelet, norm=True)
        forward = partial(swt, level=level, trim_approx=True, **kwargs)
        if axis % data.ndim != data.ndim - 1:
            raise ValueError("swt only supports axis=-1")
        inverse = partial(iswt, **kwargs)
    elif transform == 'dwt':
        kwargs = dict(wavelet=wavelet, mode=mode, axis=axis)
        forward = partial(wavedec, level=level, **kwargs)
        inverse = partial(waverec, **kwargs)
    else:
        raise ValueError("unrecognized transform: {}".format(transform))

    wav_coeffs = forward(data)

    mra_coeffs = []
    nc = len(wav_coeffs)
    z = np.zeros_like(wav_coeffs[0])
    tmp = [z, ] * nc
    for j in range(nc):
        # tmp has arrays of zeros except for the jth entry
        tmp[j] = wav_coeffs[j]

        # reconstruct
        rec = inverse(tmp)
        if rec.shape != data.shape:
            # trim any excess coefficients
            rec = rec[tuple([slice(sz) for sz in data.shape])]
        mra_coeffs.append(rec)

        # restore zeros
        tmp[j] = z
    return mra_coeffs


def imra(mra_coeffs):
    """Inverse 1D multiresolution analysis via summation.

    Parameters
    ----------
    mra_coeffs : list of ndarray
        Multiresolution analysis coefficients as returned by `mra`.

    Returns
    -------
    rec : ndarray
        The reconstructed signal.
    """
    return reduce(lambda x, y: x + y, mra_coeffs)


def mra2(data, wavelet, level=None, axes=(-2, -1), transform='swt2',
         mode='periodization'):

    if transform == 'swt2':
        if mode != 'periodization':
            raise ValueError(
                "transform swt only supports mode='periodization'")
        if axes != (-2, -1):
            raise ValueError("axes argument not supported for mode swt2")
        kwargs = dict(wavelet=wavelet, norm=True)
        forward = partial(swt2, level=level, trim_approx=True, **kwargs)
        inverse = partial(iswt2, **kwargs)
    elif transform == 'dwt2':
        kwargs = dict(wavelet=wavelet, mode=mode, axes=axes)
        forward = partial(wavedec2, level=level, **kwargs)
        inverse = partial(waverec2, **kwargs)
    else:
        raise ValueError("unrecognized transform: {}".format(transform))

    wav_coeffs = forward(data)

    mra_coeffs = []
    nc = len(wav_coeffs)
    z = np.zeros_like(wav_coeffs[0])
    tmp = [z]
    for j in range(1, nc):
        tmp.append([np.zeros_like(c) for c in wav_coeffs[j]])

    # tmp has arrays of zeros except for the jth entry
    tmp[0] = wav_coeffs[0]
    # reconstruct
    rec = inverse(tmp)
    if rec.shape != data.shape:
        # trim any excess coefficients
        rec = rec[tuple([slice(sz) for sz in data.shape])]
    mra_coeffs.append(rec)
    # restore zeros
    tmp[0] = z

    for j in range(1, nc):
        dcoeffs = []
        for n in range(3):
            # tmp has arrays of zeros except for the jth entry
            z = tmp[j][n]
            tmp[j][n] = wav_coeffs[j][n]
            # reconstruct
            rec = inverse(tmp)
            if rec.shape != data.shape:
                # trim any excess coefficients
                rec = rec[tuple([slice(sz) for sz in data.shape])]
            dcoeffs.append(rec)
            # restore zeros
            tmp[j][n] = z
        mra_coeffs.append(tuple(dcoeffs))
    return mra_coeffs


def imra2(mra_coeffs):
    """Inverse 2D multiresolution analysis via summation.

    Parameters
    ----------
    mra_coeffs : list
        Multiresolution analysis coefficients as returned by `mra2`.

    Returns
    -------
    rec : ndarray
        The reconstructed signal.
    """
    rec = mra_coeffs[0]
    for j in range(1, len(mra_coeffs)):
        for n in range(3):
            rec += mra_coeffs[j][n]
    return rec


def mran(data, wavelet, level=None, axes=None, transform='swtn',
         mode='periodization'):
    """
    Multilevel nD Discrete Wavelet Transform.

    Parameters
    ----------
    data : ndarray
        nD input data
    wavelet : Wavelet object or name string, or tuple of wavelets
        Wavelet to use.  This can also be a tuple containing a wavelet to
        apply along each axis in `axes`.
    level : int, optional
        Decomposition level (must be >= 0). If level is None (default) then it
        will be calculated using the `dwt_max_level` function.
    axes : sequence of ints, optional
        Axes over which to compute the DWT. Axes may not be repeated. The
        default is None, which means transform all axes
        (``axes = range(data.ndim)``).
    transform : {'swtn', 'dwtn'}
    mode : str or tuple of str, optional
        Signal extension mode, see `Modes` (default: 'symmetric').  This can
        also be a tuple containing a mode to apply along each axis in `axes`.

    Returns
    -------
    mra_coeffs : list
        Coefficients are organized exactly like `wavedecn`.

    """
    axes, axes_shapes, ndim_transform = _prep_axes_wavedecn(data.shape, axes)
    wavelets = _wavelets_per_axis(wavelet, axes)

    if transform == 'swtn':
        if mode != 'periodization':
            raise ValueError(
                "transform swt only supports mode='periodization'")
        kwargs = dict(wavelet=wavelets, axes=axes, norm=True)
        forward = partial(swtn, level=level, trim_approx=True, **kwargs)
        inverse = partial(iswtn, **kwargs)
    elif transform == 'dwtn':
        modes = _modes_per_axis(mode, axes)
        kwargs = dict(wavelet=wavelets, mode=modes, axes=axes)
        forward = partial(wavedecn, level=level, **kwargs)
        inverse = partial(waverecn, **kwargs)
    else:
        raise ValueError("unrecognized transform: {}".format(transform))

    wav_coeffs = forward(data)

    mra_coeffs = []
    nc = len(wav_coeffs)
    z = np.zeros_like(wav_coeffs[0])
    tmp = [z]
    for j in range(1, nc):
        tmp.append({k: np.zeros_like(v) for k, v in wav_coeffs[j].items()})

    # tmp has arrays of zeros except for the jth entry
    tmp[0] = wav_coeffs[0]
    # reconstruct
    rec = inverse(tmp)
    if rec.shape != data.shape:
        # trim any excess coefficients
        rec = rec[tuple([slice(sz) for sz in data.shape])]
    mra_coeffs.append(rec)
    # restore zeros
    tmp[0] = z

    for j in range(1, nc):
        dcoeffs = {}
        dkeys = list(wav_coeffs[j].keys())
        for k in dkeys:
            # tmp has arrays of zeros except for the jth entry
            z = tmp[j][k]
            tmp[j][k] = wav_coeffs[j][k]
            # tmp[j]['a' * len(k)] = z
            # reconstruct
            rec = inverse(tmp)
            if rec.shape != data.shape:
                # trim any excess coefficients
                rec = rec[tuple([slice(sz) for sz in data.shape])]
            dcoeffs[k] = rec
            # restore zeros
            tmp[j][k] = z
            # tmp[j].pop('a' * len(k))
        mra_coeffs.append(dcoeffs)
    return mra_coeffs


def imran(mra_coeffs):
    """Inverse nD multiresolution analysis via summation.

    Parameters
    ----------
    mra_coeffs : list
        Multiresolution analysis coefficients as returned by `mra2`.

    Returns
    -------
    rec : ndarray
        The reconstructed signal.
    """
    rec = mra_coeffs[0]
    for j in range(1, len(mra_coeffs)):
        for k, v in mra_coeffs[j].items():
            rec += v
    return rec
