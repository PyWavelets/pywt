import numpy as np

from ._extensions._pywt import Wavelet, Modes, _check_dtype
from ._extensions._cwt import (cwt_psi_single, cwt_conv, cwt_conv_real)

__all__ = ["cwt"]


def cwt(data, scales, wavelet):
    """
    cwt(data, scales, wavelet)
    Examples
    --------
    >>> import pywt
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> x = np.arange(512)
    >>> y = np.sin(2*np.pi*x/32)
    >>> coef=pywt.cwt(y,np.arange(1,129),'gauss1')
    >>> plt.matshow(coef.T)
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
                coef_r = np.asarray(coef_r, dt)
                coef_i = np.asarray(coef_i, dt)
                out
                out[:,i] = coef_r.astype(np.complex)+1j*coef_i.astype(np.complex)
            else:
                psi, x = wavelet.wavefun(length=plen.astype(np.int))
                coef = cwt_conv_real(data,psi,data.size)
                coef = np.asarray(coef, dt)
                out[:,i] = coef
        return out
    else:
        raise ValueError("Only dim == 1 supportet")
