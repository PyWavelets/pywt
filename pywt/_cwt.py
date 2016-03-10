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
        out = np.zeros((data.size,scales.size))
        for i in np.arange(scales.size):
            plen=np.floor((wavelet.upper_bound-wavelet.lower_bound)*scales[i])+1
            if (plen < 3):
                plen = 3
            psi, x = wavelet.wavefun(length = plen.astype(np.int))
            coef = cwt_conv_real(data,psi,data.size)
            coef = np.asarray(coef, dt)
            out[:,i] = coef
        return out
    else:
        raise ValueError("Only dim == 1 supportet")
