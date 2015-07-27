#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import (run_module_suite, assert_allclose, assert_,
                           assert_raises)

import pywt


def test_dwt_idwt_basic():
    x = [3, 7, 1, 1, -2, 5, 4, 6]
    cA, cD = pywt.dwt(x, 'db2')
    cA_expect = [5.65685425, 7.39923721, 0.22414387, 3.33677403, 7.77817459]
    cD_expect = [-2.44948974, -1.60368225, -4.44140056, -0.41361256,
                 1.22474487]
    assert_allclose(cA, cA_expect)
    assert_allclose(cD, cD_expect)

    x_roundtrip = pywt.idwt(cA, cD, 'db2')
    assert_allclose(x_roundtrip, x, rtol=1e-10)


def test_dwt_input_error():
    data = np.ones((16, 1))
    assert_raises(ValueError, pywt.dwt, data, 'haar')

    cA, cD = pywt.dwt(data[:, 0], 'haar')
    assert_raises(ValueError, pywt.idwt, cA[:, np.newaxis], cD, 'haar')


def test_dwt_wavelet_kwd():
    x = np.array([3, 7, 1, 1, -2, 5, 4, 6])
    w = pywt.Wavelet('sym3')
    cA, cD = pywt.dwt(x, wavelet=w, mode='cpd')
    cA_expect = [4.38354585, 3.80302657, 7.31813271, -0.58565539, 4.09727044,
                 7.81994027]
    cD_expect = [-1.33068221, -2.78795192, -3.16825651, -0.67715519,
                 -0.09722957, -0.07045258]
    assert_allclose(cA, cA_expect)
    assert_allclose(cD, cD_expect)


def test_dwt_coeff_len():
    x = np.array([3, 7, 1, 1, -2, 5, 4, 6])
    w = pywt.Wavelet('sym3')
    ln = pywt.dwt_coeff_len(data_len=len(x), filter_len=w.dec_len, mode='sym')
    assert_(ln == 6)
    ln_modes = [pywt.dwt_coeff_len(len(x), w.dec_len, mode) for mode in
                pywt.MODES.modes]
    assert_allclose(ln_modes, [6, 6, 6, 6, 6, 4])


def test_idwt_none_input():
    # None input equals arrays of zeros of the right length
    res1 = pywt.idwt([1, 2, 0, 1], None, 'db2', 'sym')
    res2 = pywt.idwt([1, 2, 0, 1], [0, 0, 0, 0], 'db2', 'sym')
    assert_allclose(res1, res2, rtol=1e-15, atol=1e-15)

    res1 = pywt.idwt(None, [1, 2, 0, 1], 'db2', 'sym')
    res2 = pywt.idwt([0, 0, 0, 0], [1, 2, 0, 1], 'db2', 'sym')
    assert_allclose(res1, res2, rtol=1e-15, atol=1e-15)

    # Only one argument at a time can be None
    assert_raises(ValueError, pywt.idwt, None, None, 'db2', 'sym')


def test_idwt_correct_size_kw():
    res = pywt.idwt([1, 2, 3, 4, 5], [1, 2, 3, 4], 'db2', 'sym',
                    correct_size=True)
    expected = [1.76776695, 0.61237244, 3.18198052, 0.61237244, 4.59619408,
                0.61237244]
    assert_allclose(res, expected)

    assert_raises(ValueError, pywt.idwt,
                  [1, 2, 3, 4, 5], [1, 2, 3, 4], 'db2', 'sym')
    assert_raises(ValueError, pywt.idwt, [1, 2, 3, 4], [1, 2, 3, 4, 5], 'db2',
                  'sym', correct_size=True)


def test_idwt_invalid_input():
    # Too short, min length is 4 for 'db4':
    assert_raises(ValueError, pywt.idwt, [1, 2, 4], [4, 1, 3], 'db4', 'sym')


if __name__ == '__main__':
    run_module_suite()
