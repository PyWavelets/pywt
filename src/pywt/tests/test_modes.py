#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import assert_raises, run_module_suite

import pywt


def test_invalid_modes():
    x = np.arange(4)
    assert_raises(TypeError, pywt.dwt, x, 'db2', -1)
    assert_raises(TypeError, pywt.dwt, x, 'db2', 7)
    assert_raises(TypeError, pywt.dwt, x, 'db2', None)


if __name__ == '__main__':
    run_module_suite()
