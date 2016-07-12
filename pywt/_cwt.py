import numpy as np

from ._extensions._pywt import ContinuousWavelet, Modes, _check_dtype
from ._extensions._cwt import (cwt_psi_single)
from ._functions import integrate_wavelet, scale2frequency

__all__ = ["cwt", "morlet", "gauswavf", "mexihat","cmorwavf", "shanwavf", "fbspwavf", "cgauwavf"]


def cwt(data, scales, wavelet, sampling_period=1.):
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
    sampling_period : float
        Sampling period for frequencies output (optional)

    Returns
    -------
    coefs : array_like
        Continous wavelet transform of the input signal for the given scales and wavelet
    frequencies : array_like
        if the unit of sampling period are seconds and given, than frequencies are in hertz. Otherwise Sampling period of 1 is assumed.

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
    if not isinstance(wavelet, ContinuousWavelet):
        wavelet = ContinuousWavelet(wavelet)
    if np.isscalar(scales):
        scales = np.array([scales])
    if data.ndim == 1:
        if wavelet.complex_cwt:
            out = np.zeros((np.size(scales),data.size),dtype=complex)
        else:
            out = np.zeros((np.size(scales),data.size))
        for i in np.arange(np.size(scales)):
            precision = 10
            int_psi, x = integrate_wavelet(wavelet,precision=precision)
            step = x[1]-x[0]
            j = np.floor(np.arange(scales[i]*(x[-1]-x[0])+1)/(scales[i]*step))
            if np.max(j) >= np.size(int_psi):
                j = np.delete(j,np.where((j >= np.size(int_psi)))[0])
            coef = -np.sqrt(scales[i])*np.diff(np.convolve(data,int_psi[j.astype(np.int)][::-1]))
            d = (coef.size-data.size)/2.
            out[i,:] = coef[int(np.floor(d)):int(-np.ceil(d))]
        frequencies = scale2frequency(wavelet,scales,precision)
        if np.isscalar(frequencies):
            frequencies = np.array([frequencies])
        for i in np.arange(len(frequencies)):
            frequencies[i] /= sampling_period
        return out, frequencies
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
    >>> plt.plot(xval,psi) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Morlet Wavelet") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.show() # doctest: +SKIP
    """
    wavelet = ContinuousWavelet("morl")
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
    >>> plt.plot(xval,psi) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Gaussian Wavelet of order 8") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.show() # doctest: +SKIP
    """
    if isinstance(p,(int, float, complex, np.int64, np.int32)):
        wavelet = ContinuousWavelet("gaus"+str(p))
    else:
        wavelet = ContinuousWavelet(p)
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
    >>> plt.plot(xval,psi) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Mexican Hat Wavelet") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.show() # doctest: +SKIP
    """
    wavelet = ContinuousWavelet("mexh")
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
    >>> plt.subplot(211) # doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at ...>
    >>> plt.plot(xval,np.real(psi)) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Real part") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.subplot(212) # doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at ...>
    >>> plt.plot(xval,np.imag(psi)) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Imaginary part") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.show() # doctest: +SKIP
    """
    wavelet = ContinuousWavelet("cmor")
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
    >>> plt.subplot(211) # doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at ...>
    >>> plt.plot(xval,np.real(psi)) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Real part") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.subplot(212) # doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at ...>
    >>> plt.plot(xval,np.imag(psi)) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Imaginary part") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.show() # doctest: +SKIP
    """
    wavelet = ContinuousWavelet("shan")
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
    >>> plt.subplot(211) # doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at ...>
    >>> plt.plot(xval,np.real(psi)) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Real part") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.subplot(212) # doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at ...>
    >>> plt.plot(xval,np.imag(psi)) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Imaginary part") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.show() # doctest: +SKIP
    """
    wavelet = ContinuousWavelet("fbsp")
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
    >>> plt.subplot(211) # doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at ...>
    >>> plt.plot(xval,np.real(psi)) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Real part") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.subplot(212) # doctest: +ELLIPSIS
    <matplotlib.axes._subplots.AxesSubplot object at ...>
    >>> plt.plot(xval,np.imag(psi)) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.title("Imaginary part") # doctest: +ELLIPSIS
    <matplotlib.text.Text object at ...>
    >>> plt.show() # doctest: +SKIP
    """
    if isinstance(p,(int, float, complex, np.int64, np.int32)):
        wavelet = ContinuousWavelet("cgau"+str(p))
    else:
        wavelet = ContinuousWavelet(p)
    wavelet.upper_bound = ub
    wavelet.lower_bound = lb
    psi, x = wavelet.wavefun(length=n)
    return psi, x
