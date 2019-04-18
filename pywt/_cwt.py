from math import floor, ceil

from ._extensions._pywt import (DiscreteContinuousWavelet, ContinuousWavelet,
                                Wavelet, _check_dtype)
from ._functions import integrate_wavelet, scale2frequency


__all__ = ["cwt"]


import numpy as np

try:
    from scipy.fftpack import next_fast_len
except ImportError:
    # Do provide a fallback so scipy is an optional requirement
    def next_fast_len(n):
        """Given a number of samples `n`, returns the next power of two
        following this numbe to take advantage of FFT speedup.
        This fallback is less efficient as `scipy.fftpack.next_fast_len`
        """
        return 2**ceil(np.log2(n))


def cwt(data, scales, wavelet, sampling_period=1., method='conv'):
    """
    cwt(data, scales, wavelet)

    One dimensional Continuous Wavelet Transform.

    Parameters
    ----------
    data : array_like
        Input signal
    scales : array_like
        The wavelet scales to use. One can use
        ``f = scale2frequency(scale, wavelet)/sampling_period`` to determine
        what physical frequency, ``f``. Here, ``f`` is in hertz when the
        ``sampling_period`` is given in seconds.
    wavelet : Wavelet object or name
        Wavelet to use
    sampling_period : float
        Sampling period for the frequencies output (optional).
        The values computed for ``coefs`` are independent of the choice of
        ``sampling_period`` (i.e. ``scales`` is not scaled by the sampling
        period).
    method : {'conv', 'fft'}, optional
        The method used to compute the CWT. Can be any of:
            - ``conv`` uses ``numpy.convolve``.
            - ``fft`` uses frequency domain convolution via ``numpy.fft.fft``.
            - ``auto`` uses automatic selection based on an estimate of the
              computational complexity at each scale.
        The ``conv`` method complexity is ``O(len(scale) * len(data))``.
        The ``fft`` method is ``O(N * log2(N))`` with
        ``N = len(scale) + len(data) - 1``. It is well suited for large size
        signals but slightly slower than ``conv`` on small ones.

    Returns
    -------
    coefs : array_like
        Continuous wavelet transform of the input signal for the given scales
        and wavelet
    frequencies : array_like
        If the unit of sampling period are seconds and given, than frequencies
        are in hertz. Otherwise, a sampling period of 1 is assumed.

    Notes
    -----
    Size of coefficients arrays depends on the length of the input array and
    the length of given scales.

    Examples
    --------
    >>> import pywt
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> x = np.arange(512)
    >>> y = np.sin(2*np.pi*x/32)
    >>> coef, freqs=pywt.cwt(y,np.arange(1,129),'gaus1')
    >>> plt.matshow(coef) # doctest: +SKIP
    >>> plt.show() # doctest: +SKIP
    ----------
    >>> import pywt
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> t = np.linspace(-1, 1, 200, endpoint=False)
    >>> sig  = np.cos(2 * np.pi * 7 * t) + np.real(np.exp(-7*(t-0.4)**2)*np.exp(1j*2*np.pi*2*(t-0.4)))
    >>> widths = np.arange(1, 31)
    >>> cwtmatr, freqs = pywt.cwt(sig, widths, 'mexh')
    >>> plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
    ...            vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())  # doctest: +SKIP
    >>> plt.show() # doctest: +SKIP
    """

    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(data)
    data = np.array(data, dtype=dt)
    if not isinstance(wavelet, (ContinuousWavelet, Wavelet)):
        wavelet = DiscreteContinuousWavelet(wavelet)
    if np.isscalar(scales):
        scales = np.array([scales])
    dt_out = None  # TODO: fix in/out dtype consistency in a subsequent PR
    if data.ndim == 1:
        if wavelet.complex_cwt:
            dt_out = complex
        out = np.empty((np.size(scales), data.size), dtype=dt_out)
        precision = 10
        int_psi, x = integrate_wavelet(wavelet, precision=precision)

        if method == 'fft':
            size_scale0 = -1
            fft_data = None
        elif not method == 'conv':
            raise ValueError("method must be 'conv' or 'fft'")

        for i, scale in enumerate(scales):
            step = x[1] - x[0]
            j = np.arange(scale * (x[-1] - x[0]) + 1) / (scale * step)
            j = j.astype(int)  # floor
            if j[-1] >= int_psi.size:
                j = np.extract(j < int_psi.size, j)
            int_psi_scale = int_psi[j][::-1]

            if method == 'conv':
                conv = np.convolve(data, int_psi_scale)
            else:
                # the padding is selected for
                # - optimal FFT complexity
                # - to be larger than the two signals length to avoid circular
                #   convolution
                size_scale = next_fast_len(data.size + int_psi_scale.size - 1)
                if size_scale != size_scale0:
                    # the fft of data changes when padding size changes thus
                    # it has to be recomputed
                    fft_data = np.fft.fft(data, size_scale)
                size_scale0 = size_scale
                fft_wav = np.fft.fft(int_psi_scale, size_scale)
                conv = np.fft.ifft(fft_wav * fft_data)
                conv = conv[:data.size + int_psi_scale.size - 1]

            coef = - np.sqrt(scale) * np.diff(conv)
            if not np.iscomplexobj(out):
                coef = np.real(coef)
            d = (coef.size - data.size) / 2.
            if d > 0:
                out[i, :] = coef[floor(d):-ceil(d)]
            elif d == 0.:
                out[i, :] = coef
            else:
                raise ValueError(
                    "Selected scale of {} too small.".format(scale))
        frequencies = scale2frequency(wavelet, scales, precision)
        if np.isscalar(frequencies):
            frequencies = np.array([frequencies])
        frequencies /= sampling_period
        return out, frequencies
    else:
        raise ValueError("Only dim == 1 supported")
