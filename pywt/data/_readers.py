import os

import numpy as np


def ascent():
    """
    Get an 8-bit grayscale bit-depth, 512 x 512 derived image for
    easy use in demos

    The image is derived from accent-to-the-top.jpg at
    http://www.public-domain-image.com/people-public-domain-images-pictures/

    Parameters
    ----------
    None

    Returns
    -------
    ascent : ndarray
       convenient image to use for testing and demonstration

    Examples
    --------
    >>> import pywt.data
    >>> ascent = pywt.data.ascent()
    >>> ascent.shape == (512, 512)
    True
    >>> ascent.max()
    255

    >>> import matplotlib.pyplot as plt
    >>> plt.gray()
    >>> plt.imshow(ascent) # doctest: +ELLIPSIS
    <matplotlib.image.AxesImage object at ...>
    >>> plt.show() # doctest: +SKIP

    """
    fname = os.path.join(os.path.dirname(__file__), 'ascent.npz')
    ascent = np.load(fname)['data']
    return ascent


def aero():
    """
    Get an 8-bit grayscale bit-depth, 512 x 512 derived image for
    easy use in demos

    Parameters
    ----------
    None

    Returns
    -------
    aero : ndarray
       convenient image to use for testing and demonstration

    Examples
    --------
    >>> import pywt.data
    >>> aero = pywt.data.ascent()
    >>> aero.shape == (512, 512)
    True
    >>> aero.max()
    255

    >>> import matplotlib.pyplot as plt
    >>> plt.gray()
    >>> plt.imshow(aero) # doctest: +ELLIPSIS
    <matplotlib.image.AxesImage object at ...>
    >>> plt.show() # doctest: +SKIP

    """
    fname = os.path.join(os.path.dirname(__file__), 'aero.npz')
    aero = np.load(fname)['data']
    return aero


def camera():
    """
    Get an 8-bit grayscale bit-depth, 512 x 512 derived image for
    easy use in demos

    Parameters
    ----------
    None

    Returns
    -------
    camera : ndarray
       convenient image to use for testing and demonstration

    Examples
    --------
    >>> import pywt.data
    >>> camera = pywt.data.ascent()
    >>> camera.shape == (512, 512)
    True

    >>> import matplotlib.pyplot as plt
    >>> plt.gray()
    >>> plt.imshow(camera) # doctest: +ELLIPSIS
    <matplotlib.image.AxesImage object at ...>
    >>> plt.show() # doctest: +SKIP

    """
    fname = os.path.join(os.path.dirname(__file__), 'camera.npz')
    camera = np.load(fname)['data']
    return camera


def ecg():
    """
    Get 1024 points of an ECG timeseries.

    Parameters
    ----------
    None

    Returns
    -------
    ecg : ndarray
       convenient timeseries to use for testing and demonstration

    Examples
    --------
    >>> import pywt.data
    >>> ecg = pywt.data.ecg()
    >>> ecg.shape == (1024,)
    True

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(ecg) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.show() # doctest: +SKIP
    """
    fname = os.path.join(os.path.dirname(__file__), 'ecg.npy')
    ecg = np.load(fname)
    return ecg


def nino():
    """
    NINO3 sea surface temperature 1871-1996 (in C; from the UKMO GISST2.3):
    Seasonally-averaged, minus the annual cycle

    Parameters
    ----------
    None

    Returns
    -------
    time : ndarray
       convenient timeseries to use for testing and demonstration
    sst : ndarray
       convenient timeseries to use for testing and demonstration

    Examples
    --------
    >>> import pywt.data
    >>> time, sst = pywt.data.nino()
    >>> sst.shape == (504,)
    True

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(time,sst) # doctest: +ELLIPSIS
    [<matplotlib.lines.Line2D object at ...>]
    >>> plt.show() # doctest: +SKIP
    """
    fname = os.path.join(os.path.dirname(__file__), 'sst_nino3.dat')
    sst = np.loadtxt(fname)
    # taken from
    # http://paos.colorado.edu/research/wavelets/wave_python/
    variance = np.std(sst, ddof=1) ** 2
    sst = (sst - np.mean(sst)) / np.std(sst, ddof=1)
    n = len(sst)
    dt = 0.25
    time = np.arange(len(sst)) * dt + 1871.0  # construct time array
    return time, sst
