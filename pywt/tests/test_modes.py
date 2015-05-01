#!/usr/bin/env python
from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import (assert_raises, run_module_suite,
                           assert_equal, assert_allclose)

import pywt


def test_available_modes():
    modes = ['zpd', 'cpd', 'sym', 'ppd', 'sp1', 'per']
    assert_equal(pywt.MODES.modes, modes)
    assert_equal(pywt.MODES.from_object('cpd'), 2)


def test_invalid_modes():
    x = np.arange(4)
    assert_raises(ValueError, pywt.dwt, x, 'db2', 'unknown')
    assert_raises(TypeError, pywt.dwt, x, 'db2', -1)
    assert_raises(TypeError, pywt.dwt, x, 'db2', 7)
    assert_raises(TypeError, pywt.dwt, x, 'db2', None)

    assert_raises(ValueError, pywt.MODES.from_object, 'unknown')
    assert_raises(ValueError, pywt.MODES.from_object, -1)
    assert_raises(ValueError, pywt.MODES.from_object, 7)
    assert_raises(TypeError, pywt.MODES.from_object, None)


def test_dwt_idwt_allmodes():
    # Test that :func:`dwt` and :func:`idwt` can be performed using every mode
    x = [1, 2, 1, 5, -1, 8, 4, 6]
    dwt_result_modes = {
        'zpd': ([-0.03467518, 1.73309178, 3.40612438, 6.32928585, 6.95094948],
                [-0.12940952, -2.15599552, -5.95034847, -1.21545369,
                 -1.8625013]),
        'cpd': ([1.28480404, 1.73309178, 3.40612438, 6.32928585, 7.51935555],
                [-0.48296291, -2.15599552, -5.95034847, -1.21545369,
                 0.25881905]),
        'sym': ([1.76776695, 1.73309178, 3.40612438, 6.32928585, 7.77817459],
                [-0.61237244, -2.15599552, -5.95034847, -1.21545369,
                 1.22474487]),
        'ppd': ([6.9162743, 1.73309178, 3.40612438, 6.32928585, 6.9162743],
                [-1.99191082, -2.15599552, -5.95034847, -1.21545369,
                 -1.99191082]),
        'sp1': ([-0.51763809, 1.73309178, 3.40612438, 6.32928585, 7.45000519],
                [0, -2.15599552, -5.95034847, -1.21545369, 0]),
        'per': ([4.053172, 3.05257099, 2.85381112, 8.42522221],
                [0.18946869, 4.18258152, 4.33737503, 2.60428326])
    }
    for mode in pywt.MODES.modes:
        cA, cD = pywt.dwt(x, 'db2', mode)
        assert_allclose(cA, dwt_result_modes[mode][0], rtol=1e-7, atol=1e-8)
        assert_allclose(cD, dwt_result_modes[mode][1], rtol=1e-7, atol=1e-8)
        assert_allclose(pywt.idwt(cA, cD, 'db2', mode), x, rtol=1e-10)


def test_default_mode():
    # The default mode should be 'sym'
    x = [1, 2, 1, 5, -1, 8, 4, 6]
    cA, cD = pywt.dwt(x, 'db2')
    cA2, cD2 = pywt.dwt(x, 'db2', mode='sym')
    assert_allclose(cA, cA2)
    assert_allclose(cD, cD2)
    assert_allclose(pywt.idwt(cA, cD, 'db2'), x)


if __name__ == '__main__':
    run_module_suite()
