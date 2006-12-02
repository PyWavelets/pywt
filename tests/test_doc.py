#!/usr/bin/env python

# Doctest for doc\index.rst document

def test_1_on_line_147():
    """
    >>> import pywt
    >>> print pywt.families()
    ['haar', 'db', 'sym', 'coif', 'bior', 'rbio', 'dmey']
    """


def test_2_on_line_168():
    """
    >>> import pywt
    >>> print pywt.wavelist('coif')
    ['coif1', 'coif2', 'coif3', 'coif4', 'coif5']
    """


def test_3_on_line_228():
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
      Symmetry:       asymmetric
    >>> print wavelet.dec_lo, wavelet.dec_hi
    [0.70710678118654757, 0.70710678118654757] [-0.70710678118654757, 0.70710678118654757]
    >>> print wavelet.rec_lo, wavelet.rec_hi
    [0.70710678118654757, 0.70710678118654757] [0.70710678118654757, -0.70710678118654757]
    """


def test_4_on_line_256():
    """
    >>> import pywt
    >>> wavelet = pywt.Wavelet('db2')
    >>> phi, psi = wavelet.wavefun(level=5)
    """


def test_5_on_line_267():
    """
    >>> import pywt
    >>> wavelet = pywt.Wavelet('bior1.1')
    >>> phi_d, psi_d, phi_r, psi_r = wavelet.wavefun(level=5)
    """


def test_6_on_line_304():
    """
    >>> import pywt, math
    >>> class HaarFilterBank(object):
    ...     def get_filters_coeffs(self):
    ...         c = math.sqrt(2)/2
    ...         dec_lo, dec_hi, rec_lo, rec_hi = [c, c], [-c, c], [c, c], [c, -c]
    ...         return [dec_lo, dec_hi, rec_lo, rec_hi]
    >>> myWavelet = pywt.Wavelet(name="myHaarWavelet", filter_bank=HaarFilterBank())
    """


def test_7_on_line_359():
    """
    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db1')
    >>> print cA
    [ 2.12132034  4.94974747  7.77817459]
    >>> print cD
    [-0.70710678 -0.70710678 -0.70710678]
    """


def test_8_on_line_402():
    """
    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db1', level=2)
    >>> cA2, cD2, cD1 = coeffs
    >>> print cD1
    [-0.70710678 -0.70710678 -0.70710678 -0.70710678]
    >>> print cD2
    [-2. -2.]
    >>> print cA2
    [  5.  13.]
    """


def test_9_on_line_438():
    """
    >>> import pywt
    >>> w = pywt.Wavelet('sym5')
    >>> print pywt.dwt_max_level(data_len = 1000, filter_len = w.dec_len)
    6
    """


def test_10_on_line_512():
    """
    >>> import pywt
    >>> print pywt.MODES.modes
    ['zpd', 'cpd', 'sym', 'ppd', 'sp1', 'per']
    """


def test_11_on_line_521():
    """
    >>> import pywt
    >>> (a, d) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> (a, d) = pywt.dwt([1,2,3,4,5,6], pywt.Wavelet('db2'), pywt.MODES.sp1)
    """


def test_12_on_line_571():
    """
    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> print pywt.idwt(cA, cD, 'db2', 'sp1')
    [ 1.  2.  3.  4.  5.  6.]
    """


def test_13_on_line_585():
    """
    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> A = pywt.idwt(cA, None, 'db2', 'sp1')
    >>> D = pywt.idwt(None, cD, 'db2', 'sp1')
    >>> print A + D
    [ 1.  2.  3.  4.  5.  6.]
    """


def test_14_on_line_621():
    """
    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db2', level=2)
    >>> print pywt.waverec(coeffs, 'db2')
    [ 1.  2.  3.  4.  5.  6.  7.  8.]
    """


def test_15_on_line_659():
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


def test_16_on_line_708():
    """
    >>> import pywt, numpy
    >>> data = numpy.ones((4,4), dtype=numpy.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> cA, (cH, cV, cD) = coeffs
    >>> print cA
    [[ 2.  2.]
     [ 2.  2.]]
    >>> print cV
    [[ 0.  0.]
     [ 0.  0.]]
    """


def test_17_on_line_750():
    """
    >>> import pywt, numpy
    >>> data = numpy.array([[1,2], [3,4]], dtype=numpy.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> print pywt.idwt2(coeffs, 'haar')
    [[ 1.  2.]
     [ 3.  4.]]
    """


def test_18_on_line_791():
    """
    >>> import pywt, numpy
    >>> coeffs = pywt.wavedec2(numpy.ones((8,8)), 'db1', level=2)
    >>> cA2, (cH2, cV2, cD2), (cH1, cV1, cD1) = coeffs
    >>> print cA2
    [[ 4.  4.]
     [ 4.  4.]]
    """


def test_19_on_line_825():
    """
    >>> import pywt, numpy
    >>> coeffs = pywt.wavedec2(numpy.ones((4,4)), 'db1')
    >>> print "levels:", len(coeffs)-1
    levels: 2
    >>> print pywt.waverec2(coeffs, 'db1')
    [[ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]]
    """


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
