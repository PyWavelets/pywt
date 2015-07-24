#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import (run_module_suite, assert_allclose, assert_,
                           assert_raises, assert_equal)

import pywt


def test_dwtn_input_error():
    data = dict()
    assert_raises(ValueError, pywt.dwtn, data, 'haar')


def test_3D_reconstruct():
    # All dimensions even length so `take` does not need to be specified
    data = np.array([
        [[0, 4, 1, 5, 1, 4],
         [0, 5, 26, 3, 2, 1],
         [5, 8, 2, 33, 4, 9],
         [2, 5, 19, 4, 19, 1]],
        [[1, 5, 1, 2, 3, 4],
         [7, 12, 6, 52, 7, 8],
         [2, 12, 3, 52, 6, 8],
         [5, 2, 6, 78, 12, 2]]])

    wavelet = pywt.Wavelet('haar')
    d = pywt.dwtn(data, wavelet)
    # idwtn creates even-length shapes (2x dwtn size)
    original_shape = [slice(None, s) for s in data.shape]
    assert_allclose(data, pywt.idwtn(d, wavelet)[original_shape],
                    rtol=1e-13, atol=1e-13)


def test_idwtn_idwt2():
    data = np.array([
        [0, 4, 1, 5, 1, 4],
        [0, 5, 6, 3, 2, 1],
        [2, 5, 19, 4, 19, 1]])

    wavelet = pywt.Wavelet('haar')

    LL, (HL, LH, HH) = pywt.dwt2(data, wavelet)
    d = {'aa': LL, 'da': HL, 'ad': LH, 'dd': HH}

    for mode in pywt.MODES.modes:
        assert_allclose(pywt.idwt2((LL, (HL, LH, HH)), wavelet, mode=mode),
                        pywt.idwtn(d, wavelet, mode=mode),
                        rtol=1e-14, atol=1e-14)


def test_idwtn_missing():
    # Test to confirm missing data behave as zeroes
    data = np.array([
        [0, 4, 1, 5, 1, 4],
        [0, 5, 6, 3, 2, 1],
        [2, 5, 19, 4, 19, 1]])

    wavelet = pywt.Wavelet('haar')

    LL, (HL, _, HH) = pywt.dwt2(data, wavelet)
    d = {'aa': LL, 'da': HL, 'dd': HH}

    assert_allclose(pywt.idwt2((LL, (HL, None, HH)), wavelet),
                    pywt.idwtn(d, 'haar'), atol=1e-15)


def test_idwtn_take():
    data = np.array([
        [[1, 4, 1, 5, 1, 4],
         [0, 5, 6, 3, 2, 1],
         [2, 5, 19, 4, 19, 1]],
        [[1, 5, 1, 2, 3, 4],
         [7, 12, 6, 52, 7, 8],
         [5, 2, 6, 78, 12, 2]]])
    wavelet = pywt.Wavelet('haar')
    d = pywt.dwtn(data, wavelet)

    assert_(data.shape != pywt.idwtn(d, wavelet).shape)
    assert_allclose(data, pywt.idwtn(d, wavelet, take=data.shape), atol=1e-15)

    # Check shape for take not equal to data.shape
    data = np.random.randn(51, 17, 68)
    d = pywt.dwtn(data, wavelet)
    assert_equal((2, 2, 2), pywt.idwtn(d, wavelet, take=2).shape)
    assert_equal((52, 18, 68), pywt.idwtn(d, wavelet, take=0).shape)


def test_ignore_invalid_keys():
    data = np.array([
        [0, 4, 1, 5, 1, 4],
        [0, 5, 6, 3, 2, 1],
        [2, 5, 19, 4, 19, 1]])

    wavelet = pywt.Wavelet('haar')

    LL, (HL, LH, HH) = pywt.dwt2(data, wavelet)
    d = {'aa': LL, 'da': HL, 'ad': LH, 'dd': HH,
         'foo': LH, 'a': HH}

    assert_allclose(pywt.idwt2((LL, (HL, LH, HH)), wavelet),
                    pywt.idwtn(d, wavelet), atol=1e-15)


def test_error_mismatched_size():
    data = np.array([
        [0, 4, 1, 5, 1, 4],
        [0, 5, 6, 3, 2, 1],
        [2, 5, 19, 4, 19, 1]])

    wavelet = pywt.Wavelet('haar')

    LL, (HL, LH, HH) = pywt.dwt2(data, wavelet)

    # Pass/fail depends on first element being shorter than remaining ones so
    # set 3/4 to an incorrect size to maximize chances. Order of dict items
    # is random so may not trigger on every test run. Dict is constructed
    # inside idwtn function so no use using an OrderedDict here.
    LL = LL[:, :-1]
    LH = LH[:, :-1]
    HH = HH[:, :-1]
    d = {'aa': LL, 'da': HL, 'ad': LH, 'dd': HH}

    assert_raises(ValueError, pywt.idwtn, d, wavelet)


if __name__ == '__main__':
    run_module_suite()
