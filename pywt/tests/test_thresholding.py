from __future__ import division, print_function, absolute_import
import numpy as np
from numpy.testing import assert_allclose, run_module_suite, assert_raises

import pywt


def _sign(x):
    # Matlab-like sign function (numpy uses a different convention).
    return x / np.abs(x)


def _soft(x, thresh):
    """soft thresholding supporting complex values.

    Notes
    -----
    This version is not robust to zeros in x.
    """
    return _sign(x) * np.maximum(np.abs(x) - thresh, 0)


def test_threshold():
    data = np.linspace(1, 4, 7)

    # soft
    soft_result = [0., 0., 0., 0.5, 1., 1.5, 2.]
    assert_allclose(pywt.threshold(data, 2, 'soft'),
                    np.array(soft_result), rtol=1e-12)
    assert_allclose(pywt.threshold(-data, 2, 'soft'),
                    -np.array(soft_result), rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 1, 'soft'),
                    [[0, 1]] * 2, rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 2, 'soft'),
                    [[0, 0]] * 2, rtol=1e-12)

    # soft thresholding complex values
    assert_allclose(pywt.threshold([[1j, 2j]] * 2, 1, 'soft'),
                    [[0j, 1j]] * 2, rtol=1e-12)
    assert_allclose(pywt.threshold([[1+1j, 2+2j]] * 2, 6, 'soft'),
                    [[0, 0]] * 2, rtol=1e-12)
    complex_data = [[1+2j, 2+2j]]*2
    for thresh in [1, 2]:
        assert_allclose(pywt.threshold(complex_data, thresh, 'soft'),
                        _soft(complex_data, thresh), rtol=1e-12)

    # test soft thresholding with non-default substitute argument
    s = 5
    assert_allclose(pywt.threshold([[1j, 2]] * 2, 1.5, 'soft', substitute=s),
                    [[s, 0.5]] * 2, rtol=1e-12)

    # soft: no divide by zero warnings when input contains zeros
    assert_allclose(pywt.threshold(np.zeros(16), 2, 'soft'),
                    np.zeros(16), rtol=1e-12)

    # hard
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
    greater_result = [0., 0., 2., 2.5, 3., 3.5, 4.]
    assert_allclose(pywt.threshold(data, 2, 'greater'),
                    np.array(greater_result), rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 1, 'greater'),
                    [[1, 2]] * 2, rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 2, 'greater'),
                    [[0, 2]] * 2, rtol=1e-12)

    # less
    assert_allclose(pywt.threshold(data, 2, 'less'),
                    np.array([1., 1.5, 2., 0., 0., 0., 0.]), rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 1, 'less'),
                    [[1, 0]] * 2, rtol=1e-12)
    assert_allclose(pywt.threshold([[1, 2]] * 2, 2, 'less'),
                    [[1, 2]] * 2, rtol=1e-12)

    # invalid
    assert_raises(ValueError, pywt.threshold, data, 2, 'foo')


if __name__ == '__main__':
    run_module_suite()
