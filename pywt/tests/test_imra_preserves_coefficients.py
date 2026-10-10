import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

import pywt


@pytest.mark.parametrize('nd', [False, True])
@pytest.mark.parametrize('stationary', [False, True])
@pytest.mark.parametrize('readonly', [False, True])
@pytest.mark.parametrize('dtype', ['float32', 'float64', 'complex64', 'complex128'])
def test_inverse_mra_preserves_coefficients(nd, stationary, readonly, dtype):
    x = np.arange(64).reshape(8, 8).astype(dtype)
    if x.dtype.kind == 'c':
        x.imag = x[::-1].real
    forward, inverse = (pywt.mran, pywt.imran) if nd else (pywt.mra2, pywt.imra2)
    transform = ('swt' if stationary else 'dwt') + ('n' if nd else '2')
    coeffs = forward(x, 'db1', level=2, transform=transform)
    arrays = [coeffs[0]]
    for details in coeffs[1:]:
        arrays.extend(details.values() if nd else details)
    original = [a.copy() for a in arrays]
    if readonly:
        for a in arrays:
            a.flags.writeable = False

    first = inverse(coeffs)
    for actual, expected in zip(arrays, original):
        assert_array_equal(actual, expected)
    second = inverse(coeffs)
    assert_allclose(first, x, rtol=1e-5, atol=1e-5)
    assert_array_equal(first, second)
