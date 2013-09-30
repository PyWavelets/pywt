#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import (run_module_suite, assert_almost_equal,
                           assert_array_almost_equal)

import pywt


def test_centrfreq():
    # db1 is Haar function, frequency=1
    w = pywt.Wavelet('db1')
    expected = 1
    result = pywt.centfrq(w, precision=12)
    assert_almost_equal(result, expected, decimal=3)
    # db2, frequency=2/3
    w = pywt.Wavelet('db2')
    expected = 2/3.
    result = pywt.centfrq(w, precision=12)
    assert_almost_equal(result, expected)


def test_scal2frq_scale():
    scale = 2
    delta = 1
    w = pywt.Wavelet('db1')
    expected = 1. / scale
    result = pywt.scal2frq(w, scale, delta, precision=12)
    assert_almost_equal(result, expected, decimal=3)


def test_scal2frq_delta():
    scale = 1
    delta = 2
    w = pywt.Wavelet('db1')
    expected = 1. / delta
    result = pywt.scal2frq(w, scale, delta, precision=12)
    assert_almost_equal(result, expected, decimal=3)


def test_intwave_orthogonal():
    w = pywt.Wavelet('db1')
    res = pywt.intwave(w, precision=12)
    res = np.row_stack(pywt.intwave(w, precision=12))
    part_1 = res[:, res[1,:]<0.5]
    part_2 = res[:, res[1,:]>0.5]
    # part_1: the integral is equal to x
    assert_array_almost_equal(part_1[0], part_1[1])
    # part_2: the integral is equal to 1 - x
    # last point ignored because of the singularity
    assert_array_almost_equal(part_2[0][:-1], 1 - part_2[1][:-1])


if __name__ == '__main__':
    run_module_suite()
