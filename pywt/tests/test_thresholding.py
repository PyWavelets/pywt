from __future__ import division, print_function, absolute_import
import numpy as np
from numpy.testing import assert_allclose, run_module_suite

import pywt


def test_threshold():
    # soft
    data = np.linspace(1, 4, 7)
    soft_result = [0., 0., 0., 0.5, 1., 1.5, 2.]
    assert_allclose(pywt.threshold(data, 2, 'soft'),
                    np.array(soft_result), rtol=1e-12)
    assert_allclose(pywt.threshold(-data, 2, 'soft'),
                    -np.array(soft_result), rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 1, 'soft'),
                    [[0, 1]] * 2, rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 2, 'soft'),
                    [[0, 0]] * 2, rtol=1e-12)

    # hard
    data = np.linspace(1, 4, 7)
    hard_result = [0., 0., 2., 2.5, 3., 3.5, 4.]
    assert_allclose(pywt.threshold(data, 2, 'hard'),
                    np.array(hard_result), rtol=1e-12)
    assert_allclose(pywt.threshold(-data, 2, 'hard'),
                    -np.array(hard_result), rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 1, 'hard'),
                    [[1, 2]] * 2, rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 2, 'hard'),
                    [[0, 2]] * 2, rtol=1e-12)

    # greater
    data = np.linspace(1, 4, 7)
    assert_allclose(pywt.threshold(data, 2, 'greater'),
                    np.array([0., 0., 2., 2.5, 3., 3.5, 4.]), rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 1, 'greater'),
                    [[1, 2]] * 2, rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 2, 'greater'),
                    [[0, 2]] * 2, rtol=1e-12)

    # less
    data = np.linspace(1, 4, 7)
    assert_allclose(pywt.threshold(data, 2, 'less'),
                    np.array([1., 1.5, 2., 0., 0., 0., 0.]), rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 1, 'less'),
                    [[1, 0]] * 2, rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 2, 'less'),
                    [[1, 2]] * 2, rtol=1e-12)


if __name__ == '__main__':
    run_module_suite()
