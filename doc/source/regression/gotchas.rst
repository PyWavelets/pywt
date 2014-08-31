.. _reg-gotchas:

.. currentmodule:: pywt


=======
Gotchas
=======

PyWavelets utilizes ``NumPy`` under the hood. That's why handling the data
containing ``None`` values can be surprising. ``None`` values are converted to
'not a number' (``numpy.NaN``) values:

    >>> import numpy, pywt
    >>> x = [None, None]
    >>> mode = 'symmetric'
    >>> wavelet = 'db1'
    >>> cA, cD = pywt.dwt(x, wavelet, mode)
    >>> numpy.all(numpy.isnan(cA))
    True
    >>> numpy.all(numpy.isnan(cD))
    True
    >>> rec = pywt.idwt(cA, cD, wavelet, mode)
    >>> numpy.all(numpy.isnan(rec))
    True
