.. _reg-modes:

.. currentmodule:: pywt


Signal Extension Modes
======================

Import :mod:`pywt` first

    >>> import pywt

    >>> def format_array(a):
    ...     """Consistent array representation across different systems"""
    ...     import numpy
    ...     a = numpy.where(numpy.abs(a) < 1e-5, 0, a)
    ...     return numpy.array2string(a, precision=5, separator=' ', suppress_small=True)

List of available signal extension :ref:`modes <Modes>`:

    >>> print(pywt.Modes.modes)
    ['zero', 'constant', 'symmetric', 'periodic', 'smooth', 'periodization', 'reflect', 'antisymmetric', 'antireflect']


Invalid mode name should rise a :exc:`ValueError`:

    >>> pywt.dwt([1,2,3,4], 'db2', 'invalid')
    Traceback (most recent call last):
    ...
    ValueError: Unknown mode name 'invalid'.


You can also refer to modes via :ref:`Modes <Modes>` class attributes:

    >>> x = [1, 2, 1, 5, -1, 8, 4, 6]
    >>> for mode_name in ['zero', 'constant', 'symmetric', 'reflect', 'periodic', 'smooth', 'periodization']:
    ...     mode = getattr(pywt.Modes, mode_name)
    ...     cA, cD = pywt.dwt(x, 'db2', mode)
    ...     print("Mode: %d (%s)" % (mode, mode_name))
    Mode: 0 (zero)
    Mode: 2 (constant)
    Mode: 1 (symmetric)
    Mode: 6 (reflect)
    Mode: 4 (periodic)
    Mode: 3 (smooth)
    Mode: 5 (periodization)


The default mode is :ref:`symmetric <Modes.symmetric>`:

    >>> cA, cD = pywt.dwt(x, 'db2')
    >>> print(cA)
    [ 1.76776695  1.73309178  3.40612438  6.32928585  7.77817459]
    >>> print(cD)
    [-0.61237244 -2.15599552 -5.95034847 -1.21545369  1.22474487]
    >>> print(pywt.idwt(cA, cD, 'db2'))
    [ 1.  2.  1.  5. -1.  8.  4.  6.]


And using a keyword argument:

    >>> cA, cD = pywt.dwt(x, 'db2', mode='symmetric')
    >>> print(cA)
    [ 1.76776695  1.73309178  3.40612438  6.32928585  7.77817459]
    >>> print(cD)
    [-0.61237244 -2.15599552 -5.95034847 -1.21545369  1.22474487]
    >>> print(pywt.idwt(cA, cD, 'db2'))
    [ 1.  2.  1.  5. -1.  8.  4.  6.]
