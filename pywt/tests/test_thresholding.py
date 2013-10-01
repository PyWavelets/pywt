from __future__ import division, print_function, absolute_import
import numpy as np
from numpy.testing import assert_, assert_allclose, run_module_suite

from pywt import thresholding


def test_soft():
    data = np.linspace(1, 4, 7)
    assert_allclose(thresholding.soft(data, 2),
                    np.array([0., 0., 0., 0.5, 1., 1.5, 2.]), rtol=1e-12)


def test_hard():
    data = np.linspace(1, 4, 7)
    assert_allclose(thresholding.hard(data, 2),
                    np.array([0., 0., 2., 2.5, 3., 3.5, 4.]), rtol=1e-12)


def test_greater():
    data = np.linspace(1, 4, 7)
    assert_allclose(thresholding.greater(data, 2),
                    np.array([0., 0., 2., 2.5, 3., 3.5, 4.]), rtol=1e-12)


def test_less():
    data = np.linspace(1, 4, 7)
    assert_allclose(thresholding.less(data, 2),
                    np.array([1., 1.5, 2., 0., 0., 0., 0.]), rtol=1e-12)

if __name__ == '__main__':
    run_module_suite()
