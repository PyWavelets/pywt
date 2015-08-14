from numpy.testing import assert_warns

import pywt


def test_intwave_deprecation():
    wavelet = pywt.Wavelet('db3')
    assert_warns(DeprecationWarning, pywt.intwave, wavelet)


def test_centrfrq_deprecation():
    wavelet = pywt.Wavelet('db3')
    assert_warns(DeprecationWarning, pywt.centrfrq, wavelet)


def test_scal2frq_deprecation():
    wavelet = pywt.Wavelet('db3')
    assert_warns(DeprecationWarning, pywt.scal2frq, wavelet, 1)


def test_orthfilt_deprecation():
    assert_warns(DeprecationWarning, pywt.orthfilt, range(6))
