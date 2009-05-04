Modes test
==========

Import pywt first

    >>> import pywt

List of availble signal extension modes:

    >>> print pywt.MODES.modes
    ['zpd', 'cpd', 'sym', 'ppd', 'sp1', 'per']


Test that dwt and idwt can be performed using every mode:

    >>> x = [1,2,1,5,-1,8,4,6]
    >>> for mode in pywt.MODES.modes:
    ...     cA, cD = pywt.dwt(x, 'db2', mode)
    ...     print "Mode:", mode
    ...     print "cA:", cA
    ...     print "cD:", cD
    ...     print "Reconstruction:", pywt.idwt(cA, cD, 'db2', mode)
    Mode: zpd
    cA: [-0.03467518  1.73309178  3.40612438  6.32928585  6.95094948]
    cD: [-0.12940952 -2.15599552 -5.95034847 -1.21545369 -1.8625013 ]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: cpd
    cA: [ 1.28480404  1.73309178  3.40612438  6.32928585  7.51935555]
    cD: [-0.48296291 -2.15599552 -5.95034847 -1.21545369  0.25881905]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: sym
    cA: [ 1.76776695  1.73309178  3.40612438  6.32928585  7.77817459]
    cD: [-0.61237244 -2.15599552 -5.95034847 -1.21545369  1.22474487]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: ppd
    cA: [ 6.9162743   1.73309178  3.40612438  6.32928585  6.9162743 ]
    cD: [-1.99191082 -2.15599552 -5.95034847 -1.21545369 -1.99191082]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: sp1
    cA: [-0.51763809  1.73309178  3.40612438  6.32928585  7.45000519]
    cD: [ -9.90069138e-13  -2.15599552e+00  -5.95034847e+00  -1.21545369e+00
      -1.98063788e-12]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: per
    cA: [ 4.053172    3.05257099  2.85381112  8.42522221]
    cD: [ 0.18946869  4.18258152  4.33737503  2.60428326]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]


Invalid mode name should rise an error:

    >>> pywt.dwt([1,2,3,4], 'db2', 'invalid')
    Traceback (most recent call last):
    ...
    ValueError: Unknown mode name 'invalid'.


You can also refer to modes via MODES class attributes:

    >>> for mode_name in ['zpd', 'cpd', 'sym', 'ppd', 'sp1', 'per']:
    ...     mode = getattr(pywt.MODES, mode_name)
    ...     cA, cD = pywt.dwt([1,2,1,5,-1,8,4,6], 'db2', mode)
    ...     print "Mode:", mode, "(%s)" % mode_name
    ...     print "cA:", cA
    ...     print "cD:", cD
    ...     print "Reconstruction:", pywt.idwt(cA, cD, 'db2', mode)
    Mode: 0 (zpd)
    cA: [-0.03467518  1.73309178  3.40612438  6.32928585  6.95094948]
    cD: [-0.12940952 -2.15599552 -5.95034847 -1.21545369 -1.8625013 ]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 2 (cpd)
    cA: [ 1.28480404  1.73309178  3.40612438  6.32928585  7.51935555]
    cD: [-0.48296291 -2.15599552 -5.95034847 -1.21545369  0.25881905]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 1 (sym)
    cA: [ 1.76776695  1.73309178  3.40612438  6.32928585  7.77817459]
    cD: [-0.61237244 -2.15599552 -5.95034847 -1.21545369  1.22474487]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 4 (ppd)
    cA: [ 6.9162743   1.73309178  3.40612438  6.32928585  6.9162743 ]
    cD: [-1.99191082 -2.15599552 -5.95034847 -1.21545369 -1.99191082]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 3 (sp1)
    cA: [-0.51763809  1.73309178  3.40612438  6.32928585  7.45000519]
    cD: [ -9.90069138e-13  -2.15599552e+00  -5.95034847e+00  -1.21545369e+00
      -1.98063788e-12]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]
    Mode: 5 (per)
    cA: [ 4.053172    3.05257099  2.85381112  8.42522221]
    cD: [ 0.18946869  4.18258152  4.33737503  2.60428326]
    Reconstruction: [ 1.  2.  1.  5. -1.  8.  4.  6.]

Some invalid mode values:

    >>> pywt.dwt(x, 'db2', -1)
    Traceback (most recent call last):
    ...
    ValueError: Invalid mode.
    >>> pywt.dwt(x, 'db2', 7)
    Traceback (most recent call last):
    ...
    ValueError: Invalid mode.
    
    >>> pywt.dwt(x, 'db2', None)
    Traceback (most recent call last):
    ...
    TypeError: expected string or Unicode object, NoneType found


The default mode is 'sym':

    >>> cA, cD = pywt.dwt(x, 'db2')
    >>> print cA
    [ 1.76776695  1.73309178  3.40612438  6.32928585  7.77817459]
    >>> print cD
    [-0.61237244 -2.15599552 -5.95034847 -1.21545369  1.22474487]
    >>> print pywt.idwt(cA, cD, 'db2')
    [ 1.  2.  1.  5. -1.  8.  4.  6.]


And using a keyword argument:

    >>> cA, cD = pywt.dwt(x, 'db2', mode='sym')
    >>> print cA
    [ 1.76776695  1.73309178  3.40612438  6.32928585  7.77817459]
    >>> print cD
    [-0.61237244 -2.15599552 -5.95034847 -1.21545369  1.22474487]
    >>> print pywt.idwt(cA, cD, 'db2')
    [ 1.  2.  1.  5. -1.  8.  4.  6.]
 
 