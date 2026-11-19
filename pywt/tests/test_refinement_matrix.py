import numpy as np
import pytest
from numpy.testing import assert_allclose

import pywt


@pytest.mark.parametrize('name', ['haar', 'db4', 'bior2.2', 'bior3.3', 'rbio4.4'])
@pytest.mark.parametrize('dual', [False, True])
def test_refinement_operator(name, dual):
    wavelet = pywt.Wavelet(name)
    h = wavelet.inverse_filter_bank[2] if dual else wavelet.rec_lo
    x = np.arange(1, len(h) + 1, dtype=float)
    expected = np.sqrt(2) * np.convolve(h, x)[::2]
    assert_allclose(pywt.refinement_matrix(name, dual=dual) @ x, expected)


def test_cardinal_cubic_spline():
    # The cubic B-spline mask, padded to an even filter length.
    h = np.array([1, 4, 6, 4, 1, 0]) / (8 * np.sqrt(2))
    zeros = np.zeros_like(h)
    wavelet = pywt.Wavelet('spline', filter_bank=[h[::-1], zeros, h, zeros])
    matrix = pywt.refinement_matrix(wavelet)
    phi = np.array([0, 1, 4, 1, 0, 0]) / 6
    derivative = np.array([0, 1, 0, -1, 0, 0]) / 2
    assert_allclose(matrix @ phi, phi)
    assert_allclose(matrix @ derivative, derivative / 2, atol=1e-15)


def test_refinement_requires_discrete_wavelet():
    with pytest.raises(TypeError, match='discrete wavelet'):
        pywt.refinement_matrix(pywt.ContinuousWavelet('mexh'))
