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

    >>> print pywt.Modes.modes
    ['zero', 'constant', 'symmetric', 'periodic', 'smooth', 'periodization']


Test that :func:`dwt` and :func:`idwt` can be performed using every mode:

    >>> x = [1,2,1,5,-1,8,4,6]
    >>> for mode in pywt.Modes.modes:
    ...     cA, cD = pywt.dwt(x, 'db2', mode)
    ...     print "Mode:", mode
    ...     print "cA:", format_array(cA)
    ...     print "cD:", format_array(cD)
    ...     print "Reconstruction:", pywt.idwt(cA, cD, 'db2', mode)
    Mode: zero
    cA: [-0.03468  1.73309  3.40612  6.32929  6.95095]
    cD: [-0.12941 -2.156   -5.95035 -1.21545 -1.8625 ]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: constant
    cA: [ 1.2848   1.73309  3.40612  6.32929  7.51936]
    cD: [-0.48296 -2.156   -5.95035 -1.21545  0.25882]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: symmetric
    cA: [ 1.76777  1.73309  3.40612  6.32929  7.77817]
    cD: [-0.61237 -2.156   -5.95035 -1.21545  1.22474]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: periodic
    cA: [ 6.91627  1.73309  3.40612  6.32929  6.91627]
    cD: [-1.99191 -2.156   -5.95035 -1.21545 -1.99191]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: smooth
    cA: [-0.51764  1.73309  3.40612  6.32929  7.45001]
    cD: [ 0.      -2.156   -5.95035 -1.21545  0.     ]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: periodization
    cA: [ 4.05317  3.05257  2.85381  8.42522]
    cD: [ 0.18947  4.18258  4.33738  2.60428]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]


Invalid mode name should rise a :exc:`ValueError`:

    >>> pywt.dwt([1,2,3,4], 'db2', 'invalid')
    Traceback (most recent call last):
    ...
    ValueError: Unknown mode name 'invalid'.


You can also refer to modes via :ref:`Modes <Modes>` class attributes:

    >>> for mode_name in ['zero', 'constant', 'symmetric', 'periodic', 'smooth', 'periodization']:
    ...     mode = getattr(pywt.Modes, mode_name)
    ...     cA, cD = pywt.dwt([1,2,1,5,-1,8,4,6], 'db2', mode)
    ...     print "Mode:", mode, "(%s)" % mode_name
    ...     print "cA:", format_array(cA)
    ...     print "cD:", format_array(cD)
    ...     print "Reconstruction:", pywt.idwt(cA, cD, 'db2', mode)
    Mode: 0 (zero)
    cA: [-0.03468  1.73309  3.40612  6.32929  6.95095]
    cD: [-0.12941 -2.156   -5.95035 -1.21545 -1.8625 ]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 2 (constant)
    cA: [ 1.2848   1.73309  3.40612  6.32929  7.51936]
    cD: [-0.48296 -2.156   -5.95035 -1.21545  0.25882]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 1 (symmetric)
    cA: [ 1.76777  1.73309  3.40612  6.32929  7.77817]
    cD: [-0.61237 -2.156   -5.95035 -1.21545  1.22474]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 4 (periodic)
    cA: [ 6.91627  1.73309  3.40612  6.32929  6.91627]
    cD: [-1.99191 -2.156   -5.95035 -1.21545 -1.99191]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 3 (smooth)
    cA: [-0.51764  1.73309  3.40612  6.32929  7.45001]
    cD: [ 0.      -2.156   -5.95035 -1.21545  0.     ]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 5 (periodization)
    cA: [ 4.05317  3.05257  2.85381  8.42522]
    cD: [ 0.18947  4.18258  4.33738  2.60428]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]


The default mode is :ref:`symmetric <Modes.symmetric>`:

    >>> cA, cD = pywt.dwt(x, 'db2')
    >>> print cA
    [ 1.76776695  1.73309178  3.40612438  6.32928585  7.77817459]
    >>> print cD
    [-0.61237244 -2.15599552 -5.95034847 -1.21545369  1.22474487]
    >>> print pywt.idwt(cA, cD, 'db2')
    [ 1.  2.  1.  5. -1.  8.  4.  6.]


And using a keyword argument:

    >>> cA, cD = pywt.dwt(x, 'db2', mode='symmetric')
    >>> print cA
    [ 1.76776695  1.73309178  3.40612438  6.32928585  7.77817459]
    >>> print cD
    [-0.61237244 -2.15599552 -5.95034847 -1.21545369  1.22474487]
    >>> print pywt.idwt(cA, cD, 'db2')
    [ 1.  2.  1.  5. -1.  8.  4.  6.]
