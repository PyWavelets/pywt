#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import run_module_suite, assert_almost_equal, assert_, dec

import pywt



def test_centrfreq():
    # db1 is Haar function, frequency=1
    w = pywt.Wavelet('db1')
    expected = 1
    result = pywt.centfrq(w, precision=12)
    assert_almost_equal(result, expected)


def test_scal2frq_scale():
    scale = 2
    delta = 1
    w = pywt.Wavelet('db1')
    expected = 1. / scale
    result = pywt.scal2frq(w, scale, delta, precision=8)
    assert_almost_equal(result, expected)

def test_scal2frq_delta():
    scale = 1
    delta = 2
    w = pywt.Wavelet('db1')
    expected = 1. / delta
    result = pywt.scal2frq(w, scale, delta, precision=8)
    assert_almost_equal(result, expected)


if __name__ == '__main__':
    run_module_suite()
