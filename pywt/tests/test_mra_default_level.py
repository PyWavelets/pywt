import numpy as np
import pytest
from numpy.testing import assert_allclose

import pywt


@pytest.mark.parametrize('nd', [False, True])
@pytest.mark.parametrize('batch_size', [1, 2, 3])
@pytest.mark.parametrize('batch_axis', [0, 1, 2])
def test_default_swt_mra_level_uses_only_transformed_axes(nd, batch_size, batch_axis):
    image = np.arange(128, dtype=float).reshape(16, 8)
    data = np.stack([image + i for i in range(batch_size)], axis=batch_axis)
    axes = tuple(i for i in range(3) if i != batch_axis)
    # Negative axes should select the same spatial dimensions.
    axes = tuple(i - data.ndim for i in axes)
    forward = pywt.mran if nd else pywt.mra2
    actual = forward(data, 'db1', axes=axes)
    expected = forward(image, 'db1')
    assert len(actual) == len(expected) == 4
    for i in range(batch_size):
        single = forward(image + i, 'db1')
        assert_allclose(np.take(actual[0], i, axis=batch_axis), single[0])
        for got_details, expected_details in zip(actual[1:], single[1:]):
            if nd:
                got_details = got_details.values()
                expected_details = expected_details.values()
            for got, expected_array in zip(got_details, expected_details):
                assert_allclose(np.take(got, i, axis=batch_axis), expected_array)
