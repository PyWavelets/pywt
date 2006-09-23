#!/usr/bin/env python

# Doctest for ../doc/index.rst document

def test_1_on_line_125():
    """
    >>> import pywt
    >>> print pywt.families()
    ['haar', 'db', 'sym', 'coif', 'bior', 'rbio', 'dmey']
    """


def test_2_on_line_146():
    """
    >>> import pywt
    >>> print pywt.wavelist('coif')
    ['coif1', 'coif2', 'coif3', 'coif4', 'coif5']
    """


def test_3_on_line_203():
    """
    >>> import pywt
    >>> wavelet = pywt.Wavelet('db1')
    >>> print wavelet
    Wavelet db1
      Family name:    Daubechies
      Short name:     db
      Filters length: 2
      Orthogonal:     True
      Biorthogonal:   True
      Orthonormal:    False
      Symmetry:       asymmetric
    >>> print wavelet.dec_lo, wavelet.dec_hi
    [0.70710678118654757, 0.70710678118654757] [-0.70710678118654757, 0.70710678118654757]
    >>> print wavelet.rec_lo, wavelet.rec_hi
    [0.70710678118654757, 0.70710678118654757] [0.70710678118654757, -0.70710678118654757]
    """


def test_4_on_line_232():
    """
    >>> import pywt
    >>> wavelet = pywt.Wavelet('db2')
    >>> phi, psi = wavelet.wavefun(level=5)
    """


def test_5_on_line_243():
    """
    >>> import pywt
    >>> wavelet = pywt.Wavelet('bior1.1')
    >>> phi_d, psi_d, phi_r, psi_r = wavelet.wavefun(level=5)
    """


def test_6_on_line_299():
    """
    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db1')
    >>> print cA
    [ 2.12132034  4.94974747  7.77817459]
    >>> print cD
    [-0.70710678 -0.70710678 -0.70710678]
    """


def test_7_on_line_337():
    """
    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db1', level=2)
    >>> a2, d2, d1 = coeffs
    >>> print d1
    [-0.70710678 -0.70710678 -0.70710678 -0.70710678]
    >>> print d2
    [-2. -2.]
    >>> print a2
    [  5.  13.]
    """


def test_8_on_line_373():
    """
    >>> import pywt
    >>> w = pywt.Wavelet('sym5')
    >>> print pywt.dwt_max_level(data_len = 1000, filter_len = w.dec_len)
    6
    """


def test_9_on_line_443():
    """
    >>> import pywt
    >>> print pywt.MODES.modes
    ['zpd', 'cpd', 'sym', 'ppd', 'sp1', 'per']
    """


def test_10_on_line_452():
    """
    >>> import pywt
    >>> (a, d) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> (a, d) = pywt.dwt([1,2,3,4,5,6], pywt.Wavelet('db2'), pywt.MODES.sp1)
    """


def test_11_on_line_499():
    """
    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> print pywt.idwt(cA, cD, 'db2', 'sp1')
    [ 1.  2.  3.  4.  5.  6.]
    """


def test_12_on_line_513():
    """
    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> A = pywt.idwt(cA, None, 'db2', 'sp1')
    >>> D = pywt.idwt(None, cD, 'db2', 'sp1')
    >>> print A + D
    [ 1.  2.  3.  4.  5.  6.]
    """


def test_13_on_line_546():
    """
    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db2', level=2)
    >>> print pywt.waverec(coeffs, 'db2')
    [ 1.  2.  3.  4.  5.  6.  7.  8.]
    """


def test_14_on_line_583():
    """
    >>> import pywt
    >>> data = [1,2,3,4,5,6]
    >>> (cA, cD) = pywt.dwt(data, 'db2', 'sp1')
    >>> print pywt.upcoef('a', cA, 'db2') + pywt.upcoef('d', cD, 'db2')
    [-0.25       -0.4330127   1.          2.          3.          4.          5.
      6.          1.78589838 -1.03108891]
    >>> n = len(data)
    >>> print pywt.upcoef('a',cA,'db2',take=n) + pywt.upcoef('d',cD,'db2',take=n)
    [ 1.  2.  3.  4.  5.  6.]
    """


def test_15_on_line_627():
    """
    >>> import pywt, numpy
    >>> data = numpy.ones((4,4), dtype=numpy.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> (cA, cH), (cV, cD) = coeffs
    >>> print cA
    [[ 2.  2.]
     [ 2.  2.]]
    >>> print cV
    [[ 0.  0.]
     [ 0.  0.]]
    """


def test_16_on_line_667():
    """
    >>> import pywt, numpy
    >>> data = numpy.array([[1,2], [3,4]], dtype=numpy.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> print pywt.idwt2(coeffs, 'haar')
    [[ 1.  2.]
     [ 3.  4.]]
    """


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
