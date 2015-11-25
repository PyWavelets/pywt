#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import run_module_suite, assert_allclose, assert_

import pywt


def test_upcoef_docstring():
    data = [1, 2, 3, 4, 5, 6]
    (cA, cD) = pywt.dwt(data, 'db2', 'smooth')
    rec = pywt.upcoef('a', cA, 'db2') + pywt.upcoef('d', cD, 'db2')
    expect = [-0.25, -0.4330127, 1., 2., 3., 4., 5.,
              6., 1.78589838, -1.03108891]
    assert_allclose(rec, expect)
    n = len(data)
    rec = (pywt.upcoef('a', cA, 'db2', take=n) +
           pywt.upcoef('d', cD, 'db2', take=n))
    assert_allclose(rec, data)


def test_upcoef_reconstruct():
    data = np.arange(3)
    a = pywt.downcoef('a', data, 'haar')
    d = pywt.downcoef('d', data, 'haar')

    rec = (pywt.upcoef('a', a, 'haar', take=3) +
           pywt.upcoef('d', d, 'haar', take=3))
    assert_allclose(rec, data)


def test_downcoef_multilevel():
    rstate = np.random.RandomState(1234)
    r = rstate.randn(16)
    nlevels = 3
    # calling with level=1 nlevels times
    a1 = r.copy()
    for i in range(nlevels):
        a1 = pywt.downcoef('a', a1, 'haar', level=1)
    # call with level=nlevels once
    a3 = pywt.downcoef('a', r, 'haar', level=nlevels)
    assert_allclose(a1, a3)


def test_compare_downcoef_coeffs():
    rstate = np.random.RandomState(1234)
    r = rstate.randn(16)
    # compare downcoef against wavedec outputs
    for nlevels in [1, 2, 3]:
        for wavelet in pywt.wavelist():
            wavelet = pywt.Wavelet(wavelet)
            max_level = pywt.dwt_max_level(r.size, wavelet.dec_len)
            if nlevels <= max_level:
                a = pywt.downcoef('a', r, wavelet, level=nlevels)
                d = pywt.downcoef('d', r, wavelet, level=nlevels)
                coeffs = pywt.wavedec(r, wavelet, level=nlevels)
                assert_allclose(a, coeffs[0])
                assert_allclose(d, coeffs[1])


def test_upcoef_multilevel():
    rstate = np.random.RandomState(1234)
    r = rstate.randn(4)
    nlevels = 3
    # calling with level=1 nlevels times
    a1 = r.copy()
    for i in range(nlevels):
        a1 = pywt.upcoef('a', a1, 'haar', level=1)
    # call with level=nlevels once
    a3 = pywt.upcoef('a', r, 'haar', level=nlevels)
    assert_allclose(a1, a3)


def test_wavelet_repr():
    from pywt import _pywt
    wavelet = _pywt.Wavelet('sym8')

    repr_wavelet = eval(wavelet.__repr__())

    assert_(wavelet.__repr__() == repr_wavelet.__repr__())


def test_dwt_max_level():
    assert_(pywt.dwt_max_level(16, 2) == 4)
    assert_(pywt.dwt_max_level(16, 8) == 1)
    assert_(pywt.dwt_max_level(16, 9) == 1)
    assert_(pywt.dwt_max_level(16, 10) == 0)
    assert_(pywt.dwt_max_level(16, 18) == 0)


if __name__ == '__main__':
    run_module_suite()
