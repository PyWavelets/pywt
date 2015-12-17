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
    >>> ascent.shape
    (512, 512)
    >>> ascent.max()
    255

    >>> import matplotlib.pyplot as plt
    >>> plt.gray()
    >>> plt.imshow(ascent)
    >>> plt.show()

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
    >>> aero.shape
    (512, 512)
    >>> aero.max()
    255

    >>> import matplotlib.pyplot as plt
    >>> plt.gray()
    >>> plt.imshow(aero)
    >>> plt.show()

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
    >>> camera.shape
    (512, 512)

    >>> import matplotlib.pyplot as plt
    >>> plt.gray()
    >>> plt.imshow(camera)
    >>> plt.show()

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
    >>> ecg.shape
    (1024,)

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(ecg)
    >>> plt.show()
    """
    fname = os.path.join(os.path.dirname(__file__), 'ecg.npy')
    ecg = np.load(fname)
    return ecg
