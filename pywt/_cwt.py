import numpy as np

from ._extensions._pywt import Wavelet, Modes, _check_dtype
from ._extensions._cwt import (cwt_psi_single, cwt_conv, cwt_conv_real)

__all__ = ["cwt"]


def cwt(data, scales, wavelet):
    """
    cwt(data, scales, wavelet)

    One dimensional Continuous Wavelet Transform.

    Parameters
    ----------
    data : array_like
        Input signal
    scales : array_like
        scales to use
    wavelet : Wavelet object or name
        Wavelet to use

    Returns
    -------
    coefs : array_like
        Continous wavelet transform of the input signal for the given scales and wavelet

    Notes
    -----
    Size of coefficients arrays depends on the length of the input array and the length of given scales.

    Examples
    --------
    >>> import pywt
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> x = np.arange(512)
    >>> y = np.sin(2*np.pi*x/32)
    >>> coef=pywt.cwt(y,np.arange(1,129),'gaus1')
    >>> plt.matshow(coef.T)
    ----------
    >>> import pywt
    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> t = np.linspace(-1, 1, 200, endpoint=False)
    >>> sig  = np.cos(2 * np.pi * 7 * t) + signal.gausspulse(t - 0.4, fc=2)
    >>> widths = np.arange(1, 31)
    >>> cwtmatr = pywt.cwt(sig, widths, 'mexh').T
    >>> plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
    ...            vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
    >>> plt.show()
    """

    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(data)
    data = np.array(data, dtype=dt)
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    if data.ndim == 1:
        if wavelet.complex_cwt:
            out = np.zeros((data.size,scales.size),dtype=complex)
        else:
            out = np.zeros((data.size,scales.size))
        for i in np.arange(scales.size):
            plen = np.floor((wavelet.upper_bound-wavelet.lower_bound)*scales[i])+1
            if (plen < 3):
                plen = 3
            if wavelet.complex_cwt:
                psi_r, psi_i, x = wavelet.wavefun(length=plen.astype(np.int))
                coef_r = cwt_conv_real(data,psi_r,data.size)
                coef_i = cwt_conv_real(data,psi_i,data.size)
                out
                out[:,i] = coef_r.astype(np.complex)+1j*coef_i.astype(np.complex)
            else:
                psi, x = wavelet.wavefun(length=plen.astype(np.int))
                coef = cwt_conv_real(data,psi,data.size)
                out[:,i] = coef
        return out
    else:
        raise ValueError("Only dim == 1 supportet")
