import numpy as np

from ._extensions._pywt import Wavelet, Modes, _check_dtype
from ._extensions._cwt import (cwt_psi_single, cwt_conv, cwt_conv_real)

__all__ = ["cwt", "morlet", "gauswavf", "mexihat","cmorwavf", "shanwavf", "fbspwavf", "cgauwavf"]


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
    >>> plt.matshow(coef)
    ----------
    >>> import pywt
    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> t = np.linspace(-1, 1, 200, endpoint=False)
    >>> sig  = np.cos(2 * np.pi * 7 * t) + signal.gausspulse(t - 0.4, fc=2)
    >>> widths = np.arange(1, 31)
    >>> cwtmatr = pywt.cwt(sig, widths, 'mexh')
    >>> plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
    ...            vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
    >>> plt.show()
    """

    # accept array_like input; make a copy to ensure a contiguous array
    dt = _check_dtype(data)
    data = np.array(data, dtype=dt)
    if not isinstance(wavelet, Wavelet):
        wavelet = Wavelet(wavelet)
    if np.isscalar(scales):
        scales = np.array([scales])
    if data.ndim == 1:
        if wavelet.complex_cwt:
            out = np.zeros((data.size,np.size(scales)),dtype=complex)
        else:
            out = np.zeros((data.size,np.size(scales)))
        for i in np.arange(np.size(scales)):
            plen = 1024
            if (plen < 3):
                plen = 3
            if wavelet.complex_cwt:
                psi, x = wavelet.wavefun(length=plen)
                step = x[1]-x[0]
                outWav = np.cumsum(psi)*step
                x = x-x[0]
                j = np.floor(np.arange(scales[i]*x[-1])/(scales[i]*step))                  
                coef = -np.sqrt(scales[i])*np.diff(np.convolve(data,outWav[j.astype(np.int)][::-1]))
                d = (coef.size-data.size)/2.
                out[:,i] = coef[np.floor(d)-1:-np.ceil(d)+1]                
                #psi = psi / np.sqrt(scales[i])
                #coef_r = cwt_conv_real(data,np.real(psi),data.size)
                #coef_i = cwt_conv_real(data,np.imag(psi),data.size)
                #out[:,i] = coef_r.astype(np.complex)+1j*coef_i.astype(np.complex)
            else:
                psi, x = wavelet.wavefun(length=plen)
                step = x[1]-x[0]
                outWav = np.cumsum(psi)*step
                x = x-x[0]
                j = np.floor(np.arange(scales[i]*x[-1])/(scales[i]*step))     
                #psi = psi / np.sqrt(scales[i])
                #coef = cwt_conv_real(data,psi,data.size)
                
                coef = -np.sqrt(scales[i])*np.diff(np.convolve(data,outWav[j.astype(np.int)][::-1]))
                d = (coef.size-data.size)/2.
                out[:,i] = coef[np.floor(d-1.):-(np.ceil(d+1.))]
        return out.T
    else:
        raise ValueError("Only dim == 1 supportet")


def morlet(lb,ub,n):
    """
    morlet(lower_bound,upper_bound,n)

    Morlet wavelet

    Parameters
    ----------
    lower_bound : float
        lower bound of support
    upper_bound : float
        upper bound of support
    n : int
        number of samples

    Returns
    -------
    psi : array_like
        Wavelet function computed for grid xval
    xval : array_like
        grid

    Notes
    -----
    Morlet wavelet for effective support of [lower_bound, upper_bound].

    Examples
    --------
    >>> import pywt
    >>> import matplotlib.pyplot as plt
    >>> lb = -4
    >>> ub = 4
    >>> n = 1000
    >>> [psi,xval] = pywt.morlet(lb,ub,n)
    >>> plt.plot(xval,psi)
    >>> plt.title("Morlet Wavelet")
    """
    wavelet = Wavelet("morl")
    wavelet.upper_bound = ub
    wavelet.lower_bound = lb
    psi, x = wavelet.wavefun(length=n)
    return psi, x


def gauswavf(lb,ub,n,p=1):
    """
    gauswavf(lower_bound,upper_bound,n)
    gauswavf(lower_bound,upper_bound,n,p)
    gauswavf(lower_bound,upper_bound,n,wavename)

    Gaussian wavelet

    Parameters
    ----------
    lower_bound : float
        lower bound of support
    upper_bound : float
        upper bound of support
    n : int
        number of samples
    p : int
        order

    Returns
    -------
    psi : array_like
        Wavelet function computed for grid xval
    xval : array_like
        grid

    Notes
    -----
    Gaussian wavelet for effective support of [lower_bound, upper_bound].

    Examples
    --------
    >>> import pywt
    >>> import matplotlib.pyplot as plt
    >>> lb = -5
    >>> ub = 5
    >>> n = 1000
    >>> [psi,xval] = pywt.gauswavf(lb,ub,n,8)
    >>> plt.plot(xval,psi)
    >>> plt.title("Gaussian Wavelet of order 8")
    """
    if isinstance(p,(int, float, complex, np.int64)):
        wavelet = Wavelet("gaus"+str(p))
    else:
        wavelet = Wavelet(p)
    wavelet.upper_bound = ub
    wavelet.lower_bound = lb
    psi, x = wavelet.wavefun(length=n)
    return psi, x


def mexihat(lb,ub,n):
    """
    mexihat(lower_bound,upper_bound,n)

    Mexican Hat wavelet

    Parameters
    ----------
    lower_bound : float
        lower bound of support
    upper_bound : float
        upper bound of support
    n : int
        number of samples

    Returns
    -------
    psi : array_like
        Wavelet function computed for grid xval
    xval : array_like
        grid

    Notes
    -----
    Mexican Hat wavelet for effective support of [lower_bound, upper_bound].

    Examples
    --------
    >>> import pywt
    >>> import matplotlib.pyplot as plt
    >>> lb = -5
    >>> ub = 5
    >>> n = 1000
    >>> [psi,xval] = pywt.mexihat(lb,ub,n)
    >>> plt.plot(xval,psi)
    >>> plt.title("Mexican Hat Wavelet")
    """
    wavelet = Wavelet("mexh")
    wavelet.upper_bound = ub
    wavelet.lower_bound = lb
    psi, x = wavelet.wavefun(length=n)
    return psi, x


def cmorwavf(lb,ub,n,fb,fc):
    """
    cmorwavf(lower_bound,upper_bound,n,fb,fc)

    Complex Morlet wavelet

    Parameters
    ----------
    lower_bound : float
        lower bound of support
    upper_bound : float
        upper bound of support
    n : int
        number of samples
    fb : float
        bandwidth
    fc : float
        center frequency

    Returns
    -------
    psi : array_like
        Complex Wavelet function computed for grid xval
    xval : array_like
        grid

    Notes
    -----
    Complex Morlet wavelet for effective support of [lower_bound, upper_bound].

    Examples
    --------
    >>> import pywt
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> lb = -8
    >>> ub = 8
    >>> n = 1000
    >>> fb = 1.5
    >>> fc = 1
    >>> [psi,xval] = pywt.cmorwavf(lb,ub,n,fb,fc)
    >>> plt.subplot(211)
    >>> plt.plot(xval,np.real(psi))
    >>> plt.title("Real part")
    >>> plt.subplot(212)
    >>> plt.plot(xval,np.imag(psi))
    >>> plt.title("Imaginary part)
    """
    wavelet = Wavelet("cmor")
    wavelet.upper_bound = ub
    wavelet.lower_bound = lb
    wavelet.bandwidth_frequency = fb
    wavelet.center_frequency = fc
    psi, x = wavelet.wavefun(length=n)
    return psi, x


def shanwavf(lb,ub,n,fb,fc):
    """
    shanwavf(lower_bound,upper_bound,n,fb,fc)

    Complex Shannon wavelet

    Parameters
    ----------
    lower_bound : float
        lower bound of support
    upper_bound : float
        upper bound of support
    n : int
        number of samples
    fb : float
        bandwidth
    fc : float
        center frequency

    Returns
    -------
    psi : array_like
        Complex Wavelet function computed for grid xval
    xval : array_like
        grid

    Notes
    -----
    Complex Shannon wavelet for effective support of [lower_bound, upper_bound].

    Examples
    --------
    >>> import pywt
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> lb = -20
    >>> ub = 20
    >>> n = 1000
    >>> fb = 1
    >>> fc = 1.5
    >>> [psi,xval] = pywt.shanwavf(lb,ub,n,fb,fc)
    >>> plt.subplot(211)
    >>> plt.plot(xval,np.real(psi))
    >>> plt.title("Real part")
    >>> plt.subplot(212)
    >>> plt.plot(xval,np.imag(psi))
    >>> plt.title("Imaginary part)
    """
    wavelet = Wavelet("shan")
    wavelet.upper_bound = ub
    wavelet.lower_bound = lb
    wavelet.bandwidth_frequency = fb
    wavelet.center_frequency = fc
    psi, x = wavelet.wavefun(length=n)
    return psi, x


def fbspwavf(lb,ub,n,m,fb,fc):
    """
    fbspwavf(lower_bound,upper_bound,n,m,fb,fc)

    Complex frequency B-spline  wavelet

    Parameters
    ----------
    lower_bound : float
        lower bound of support
    upper_bound : float
        upper bound of support
    n : int
        number of samples
    m : int
        order
    fb : float
        bandwidth
    fc : float
        center frequency

    Returns
    -------
    psi : array_like
        Complex Wavelet function computed for grid xval
    xval : array_like
        grid

    Notes
    -----
    Complex frequency B-spline  wavelet for effective support of [lower_bound, upper_bound].

    Examples
    --------
    >>> import pywt
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> lb = -20
    >>> ub = 20
    >>> n = 1000
    >>> m = 2
    >>> fb = 0.5
    >>> fc = 1
    >>> [psi,xval] = pywt.fbspwavf(lb,ub,n,m,fb,fc)
    >>> plt.subplot(211)
    >>> plt.plot(xval,np.real(psi))
    >>> plt.title("Real part")
    >>> plt.subplot(212)
    >>> plt.plot(xval,np.imag(psi))
    >>> plt.title("Imaginary part)
    """
    wavelet = Wavelet("fbsp")
    wavelet.upper_bound = ub
    wavelet.lower_bound = lb
    wavelet.fbsp_order = m
    wavelet.bandwidth_frequency = fb
    wavelet.center_frequency = fc
    psi, x = wavelet.wavefun(length=n)
    return psi, x


def cgauwavf(lb,ub,n,p=1):
    """
    cgauwavf(lower_bound,upper_bound,n)
    cgauwavf(lower_bound,upper_bound,n,p)
    cgauwavf(lower_bound,upper_bound,n,wavename)

    Complex Gaussian wavelet

    Parameters
    ----------
    lower_bound : float
        lower bound of support
    upper_bound : float
        upper bound of support
    n : int
        number of samples
    p : int
        order

    Returns
    -------
    psi : array_like
        Complex Wavelet function computed for grid xval
    xval : array_like
        grid

    Notes
    -----
    Complex Gaussian wavelet for effective support of [lower_bound, upper_bound].

    Examples
    --------
    >>> import pywt
    >>> import matplotlib.pyplot as plt
    >>> lb = -5
    >>> ub = 5
    >>> n = 1000
    >>> order = 4
    >>> [psi,xval] = pywt.cgauwavf(lb,ub,n,order)
    >>> plt.subplot(211)
    >>> plt.plot(xval,np.real(psi))
    >>> plt.title("Real part")
    >>> plt.subplot(212)
    >>> plt.plot(xval,np.imag(psi))
    >>> plt.title("Imaginary part)
    """
    if isinstance(p,(int, float, complex, np.int64)):
        wavelet = Wavelet("cgau"+str(p))
    else:
        wavelet = Wavelet(p)
    wavelet.upper_bound = ub
    wavelet.lower_bound = lb
    psi, x = wavelet.wavefun(length=n)
    return psi, x
