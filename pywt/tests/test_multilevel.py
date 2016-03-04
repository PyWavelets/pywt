#!/usr/bin/env python

from __future__ import division, print_function, absolute_import

import os
import numpy as np
from numpy.testing import (run_module_suite, assert_almost_equal,
                           assert_allclose, assert_, assert_equal,
                           assert_raises, dec)

import pywt

# Check that float32 and complex64 are preserved.  Other real types get
# converted to float64.
dtypes_in = [np.int8, np.float32, np.float64, np.complex64, np.complex128]
dtypes_out = [np.float64, np.float32, np.float64, np.complex64, np.complex128]


# tolerances used in accuracy comparisons
tol_single = 1e-6
tol_double = 1e-13
dtypes_and_tolerances = [(np.float32, tol_single), (np.float64, tol_double),
                         (np.int8, tol_double), (np.complex64, tol_single),
                         (np.complex128, tol_double)]

# determine which wavelets to test
wavelist = pywt.wavelist()
if 'dmey' in wavelist:
    # accuracy is very low for dmey, so omit it
    wavelist.remove('dmey')


####
# 1d multilevel dwt tests
####

def test_wavedec():
    x = [3, 7, 1, 1, -2, 5, 4, 6]
    db1 = pywt.Wavelet('db1')
    cA3, cD3, cD2, cD1 = pywt.wavedec(x, db1)
    assert_almost_equal(cA3, [8.83883476])
    assert_almost_equal(cD3, [-0.35355339])
    assert_allclose(cD2, [4., -3.5])
    assert_allclose(cD1, [-2.82842712, 0, -4.94974747, -1.41421356])
    assert_(pywt.dwt_max_level(len(x), db1) == 3)


def test_waverec_accuracies():
    rstate = np.random.RandomState(1234)
    x0 = rstate.randn(8)
    for dt, tol in dtypes_and_tolerances:
        x = x0.astype(dt)
        if np.iscomplexobj(x):
            x += 1j*rstate.randn(8).astype(x.real.dtype)
        coeffs = pywt.wavedec(x, 'db1')
        assert_allclose(pywt.waverec(coeffs, 'db1'), x, atol=tol, rtol=tol)


def test_waverec_none():
    x = [3, 7, 1, 1, -2, 5, 4, 6]
    coeffs = pywt.wavedec(x, 'db1')

    # set some coefficients to None
    coeffs[2] = None
    coeffs[0] = None
    assert_(pywt.waverec(coeffs, 'db1').size, len(x))


def test_waverec_odd_length():
    x = [3, 7, 1, 1, -2, 5]
    coeffs = pywt.wavedec(x, 'db1')
    assert_allclose(pywt.waverec(coeffs, 'db1'), x, rtol=1e-12)


def test_waverec_complex():
    x = np.array([3, 7, 1, 1, -2, 5, 4, 6])
    x = x + 1j
    coeffs = pywt.wavedec(x, 'db1')
    assert_allclose(pywt.waverec(coeffs, 'db1'), x, rtol=1e-12)


def test_multilevel_dtypes_1d():
    # only checks that the result is of the expected type
    wavelet = pywt.Wavelet('haar')
    for dt_in, dt_out in zip(dtypes_in, dtypes_out):
        # wavedec, waverec
        x = np.ones(8, dtype=dt_in)
        errmsg = "wrong dtype returned for {0} input".format(dt_in)

        coeffs = pywt.wavedec(x, wavelet, level=2)
        for c in coeffs:
            assert_(c.dtype == dt_out, "wavedec: " + errmsg)
        x_roundtrip = pywt.waverec(coeffs, wavelet)
        assert_(x_roundtrip.dtype == dt_out, "waverec: " + errmsg)


def test_waverec_all_wavelets_modes():
    # test 2D case using all wavelets and modes
    rstate = np.random.RandomState(1234)
    r = rstate.randn(80)
    for wavelet in wavelist:
        for mode in pywt.Modes.modes:
            coeffs = pywt.wavedec(r, wavelet, mode=mode)
            assert_allclose(pywt.waverec(coeffs, wavelet, mode=mode),
                            r, rtol=tol_single, atol=tol_single)

####
# 1d multilevel swt tests
####


def test_swt_decomposition():
    x = [3, 7, 1, 3, -2, 6, 4, 6]
    db1 = pywt.Wavelet('db1')
    (cA2, cD2), (cA1, cD1) = pywt.swt(x, db1, level=2)
    expected_cA1 = [7.07106781, 5.65685425, 2.82842712, 0.70710678,
                    2.82842712, 7.07106781, 7.07106781, 6.36396103]
    assert_allclose(cA1, expected_cA1)
    expected_cD1 = [-2.82842712, 4.24264069, -1.41421356, 3.53553391,
                    -5.65685425, 1.41421356, -1.41421356, 2.12132034]
    assert_allclose(cD1, expected_cD1)
    expected_cA2 = [7, 4.5, 4, 5.5, 7, 9.5, 10, 8.5]
    assert_allclose(cA2, expected_cA2, rtol=tol_double)
    expected_cD2 = [3, 3.5, 0, -4.5, -3, 0.5, 0, 0.5]
    assert_allclose(cD2, expected_cD2, rtol=tol_double, atol=1e-14)

    # level=1, start_level=1 decomposition should match level=2
    res = pywt.swt(cA1, db1, level=1, start_level=1)
    cA2, cD2 = res[0]
    assert_allclose(cA2, expected_cA2, rtol=tol_double)
    assert_allclose(cD2, expected_cD2, rtol=tol_double, atol=1e-14)

    coeffs = pywt.swt(x, db1)
    assert_(len(coeffs) == 3)
    assert_(pywt.swt_max_level(len(x)) == 3)


def test_swt_iswt_integration():
    # This function performs a round-trip swt/iswt transform test on
    # all available types of wavelets in PyWavelets - except the
    # 'dmey' wavelet. The latter has been excluded because it does not
    # produce very precise results. This is likely due to the fact
    # that the 'dmey' wavelet is a discrete approximation of a
    # continuous wavelet. All wavelets are tested up to 3 levels. The
    # test validates neither swt or iswt as such, but it does ensure
    # that they are each other's inverse.

    max_level = 3
    wavelets = pywt.wavelist()
    if 'dmey' in wavelets:
        # The 'dmey' wavelet seems to be a bit special - disregard it for now
        wavelets.remove('dmey')
    for current_wavelet_str in wavelets:
        current_wavelet = pywt.Wavelet(current_wavelet_str)
        input_length_power = int(np.ceil(np.log2(max(
            current_wavelet.dec_len,
            current_wavelet.rec_len))))
        input_length = 2**(input_length_power + max_level - 1)
        X = np.arange(input_length)
        coeffs = pywt.swt(X, current_wavelet, max_level)
        Y = pywt.iswt(coeffs, current_wavelet)
        assert_allclose(Y, X, rtol=1e-5, atol=1e-7)


def test_swt_dtypes():
    wavelet = pywt.Wavelet('haar')
    for dt_in, dt_out in zip(dtypes_in, dtypes_out):
        errmsg = "wrong dtype returned for {0} input".format(dt_in)

        # swt
        x = np.ones(8, dtype=dt_in)
        (cA2, cD2), (cA1, cD1) = pywt.swt(x, wavelet, level=2)
        assert_(cA2.dtype == cD2.dtype == cA1.dtype == cD1.dtype == dt_out,
                "swt: " + errmsg)

        # swt2
        x = np.ones((8, 8), dtype=dt_in)
        cA, (cH, cV, cD) = pywt.swt2(x, wavelet, level=1)[0]
        assert_(cA.dtype == cH.dtype == cV.dtype == cD.dtype == dt_out,
                "swt2: " + errmsg)


def test_swt2_iswt2_integration():
    # This function performs a round-trip swt2/iswt2 transform test on
    # all available types of wavelets in PyWavelets - except the
    # 'dmey' wavelet. The latter has been excluded because it does not
    # produce very precise results. This is likely due to the fact
    # that the 'dmey' wavelet is a discrete approximation of a
    # continuous wavelet. All wavelets are tested up to 3 levels. The
    # test validates neither swt2 or iswt2 as such, but it does ensure
    # that they are each other's inverse.

    max_level = 3
    wavelets = pywt.wavelist()
    if 'dmey' in wavelets:
        # The 'dmey' wavelet seems to be a bit special - disregard it for now
        wavelets.remove('dmey')
    for current_wavelet_str in wavelets:
        current_wavelet = pywt.Wavelet(current_wavelet_str)
        input_length_power = int(np.ceil(np.log2(max(
            current_wavelet.dec_len,
            current_wavelet.rec_len))))
        input_length = 2**(input_length_power + max_level - 1)
        X = np.arange(input_length**2).reshape(input_length, input_length)
        coeffs = pywt.swt2(X, current_wavelet, max_level)
        Y = pywt.iswt2(coeffs, current_wavelet)
        assert_allclose(Y, X, rtol=1e-5, atol=1e-5)

####
# 2d multilevel dwt function tests
####


def test_waverec2_accuracies():
    rstate = np.random.RandomState(1234)
    x0 = rstate.randn(4, 4)
    for dt, tol in dtypes_and_tolerances:
        x = x0.astype(dt)
        if np.iscomplexobj(x):
            x += 1j*rstate.randn(4, 4).astype(x.real.dtype)
        coeffs = pywt.wavedec2(x, 'db1')
        assert_(len(coeffs) == 3)
        assert_allclose(pywt.waverec2(coeffs, 'db1'), x, atol=tol, rtol=tol)


def test_multilevel_dtypes_2d():
    wavelet = pywt.Wavelet('haar')
    for dt_in, dt_out in zip(dtypes_in, dtypes_out):
        # wavedec2, waverec2
        x = np.ones((8, 8), dtype=dt_in)
        errmsg = "wrong dtype returned for {0} input".format(dt_in)
        cA, coeffsD2, coeffsD1 = pywt.wavedec2(x, wavelet, level=2)
        assert_(cA.dtype == dt_out, "wavedec2: " + errmsg)
        for c in coeffsD1:
            assert_(c.dtype == dt_out, "wavedec2: " + errmsg)
        for c in coeffsD2:
            assert_(c.dtype == dt_out, "wavedec2: " + errmsg)
        x_roundtrip = pywt.waverec2([cA, coeffsD2, coeffsD1], wavelet)
        assert_(x_roundtrip.dtype == dt_out, "waverec2: " + errmsg)


@dec.slow
def test_waverec2_all_wavelets_modes():
    # test 2D case using all wavelets and modes
    rstate = np.random.RandomState(1234)
    r = rstate.randn(80, 96)
    for wavelet in wavelist:
        for mode in pywt.Modes.modes:
            coeffs = pywt.wavedec2(r, wavelet, mode=mode)
            assert_allclose(pywt.waverec2(coeffs, wavelet, mode=mode),
                            r, rtol=tol_single, atol=tol_single)


def test_wavedec2_complex():
    data = np.ones((4, 4)) + 1j
    coeffs = pywt.wavedec2(data, 'db1')
    assert_(len(coeffs) == 3)
    assert_allclose(pywt.waverec2(coeffs, 'db1'), data, rtol=1e-12)


def test_waverec2_odd_length():
    x = np.ones((10, 6))
    coeffs = pywt.wavedec2(x, 'db1')
    assert_allclose(pywt.waverec2(coeffs, 'db1'), x, rtol=1e-12)


def test_waverec2_none_coeffs():
    x = np.arange(24).reshape(6, 4)
    coeffs = pywt.wavedec2(x, 'db1')
    coeffs[1] = (None, None, None)
    assert_(x.shape == pywt.waverec2(coeffs, 'db1').shape)

####
# nd multilevel dwt function tests
####


def test_waverecn():
    rstate = np.random.RandomState(1234)
    # test 1D through 4D cases
    for nd in range(1, 5):
        x = rstate.randn(*(4, )*nd)
        coeffs = pywt.wavedecn(x, 'db1')
        assert_(len(coeffs) == 3)
        assert_allclose(pywt.waverecn(coeffs, 'db1'), x, rtol=tol_double)


def test_waverecn_empty_coeff():
    coeffs = [np.ones((2, 2, 2)), {}, {}]
    assert_equal(pywt.waverecn(coeffs, 'db1').shape, (8, 8, 8))

    assert_equal(pywt.waverecn(coeffs, 'db1').shape, (8, 8, 8))
    coeffs = [np.ones((2, 2, 2)), {}, {'daa': np.ones((4, 4, 4))}]

    coeffs = [np.ones((2, 2, 2)), {}, {}, {'daa': np.ones((8, 8, 8))}]
    assert_equal(pywt.waverecn(coeffs, 'db1').shape, (16, 16, 16))


def test_waverecn_invalid_coeffs():
    # approximation coeffs as None and no valid detail oeffs
    coeffs = [None, {}]
    assert_raises(ValueError, pywt.waverecn, coeffs, 'db1')

    # use of None for a coefficient value
    coeffs = [np.ones((2, 2, 2)), {}, {'daa': None}, ]
    assert_raises(ValueError, pywt.waverecn, coeffs, 'db1')

    # invalid key names in coefficient list
    coeffs = [np.ones((4, 4, 4)), {'daa': np.ones((4, 4, 4)),
                                   'foo': np.ones((4, 4, 4))}]
    assert_raises(ValueError, pywt.waverecn, coeffs, 'db1')

    # mismatched key name lengths
    coeffs = [np.ones((4, 4, 4)), {'daa': np.ones((4, 4, 4)),
                                   'da': np.ones((4, 4, 4))}]
    assert_raises(ValueError, pywt.waverecn, coeffs, 'db1')

    # key name lengths don't match the array dimensions
    coeffs = [[[[1.0]]], {'ad': [[[0.0]]], 'da': [[[0.0]]], 'dd': [[[0.0]]]}]
    assert_raises(ValueError, pywt.waverecn, coeffs, 'db1')


def test_waverecn_lists():
    # support coefficient arrays specified as lists instead of arrays
    coeffs = [[[1.0]], {'ad': [[0.0]], 'da': [[0.0]], 'dd': [[0.0]]}]
    assert_equal(pywt.waverecn(coeffs, 'db1').shape, (2, 2))


def test_waverecn_invalid_coeffs2():
    # shape mismatch should raise an error
    coeffs = [np.ones((4, 4, 4)), {'ada': np.ones((4, 4))}]
    assert_raises(ValueError, pywt.waverecn, coeffs, 'db1')


def test_waverecn_accuracies():
    # testing 3D only here
    rstate = np.random.RandomState(1234)
    x0 = rstate.randn(4, 4, 4)
    for dt, tol in dtypes_and_tolerances:
        x = x0.astype(dt)
        if np.iscomplexobj(x):
            x += 1j*rstate.randn(4, 4, 4).astype(x.real.dtype)
        coeffs = pywt.wavedecn(x.astype(dt), 'db1')
        assert_allclose(pywt.waverecn(coeffs, 'db1'), x, atol=tol, rtol=tol)


def test_multilevel_dtypes_nd():
    wavelet = pywt.Wavelet('haar')
    for dt_in, dt_out in zip(dtypes_in, dtypes_out):
        # wavedecn, waverecn
        x = np.ones((8, 8), dtype=dt_in)
        errmsg = "wrong dtype returned for {0} input".format(dt_in)
        cA, coeffsD2, coeffsD1 = pywt.wavedecn(x, wavelet, level=2)
        assert_(cA.dtype == dt_out, "wavedecn: " + errmsg)
        for key, c in coeffsD1.items():
            assert_(c.dtype == dt_out, "wavedecn: " + errmsg)
        for key, c in coeffsD2.items():
            assert_(c.dtype == dt_out, "wavedecn: " + errmsg)
        x_roundtrip = pywt.waverecn([cA, coeffsD2, coeffsD1], wavelet)
        assert_(x_roundtrip.dtype == dt_out, "waverecn: " + errmsg)


def test_wavedecn_complex():
    data = np.ones((4, 4, 4)) + 1j
    coeffs = pywt.wavedecn(data, 'db1')
    assert_allclose(pywt.waverecn(coeffs, 'db1'), data, rtol=1e-12)


def test_waverecn_dtypes():
    x = np.ones((4, 4, 4))
    for dt, tol in dtypes_and_tolerances:
        coeffs = pywt.wavedecn(x.astype(dt), 'db1')
        assert_allclose(pywt.waverecn(coeffs, 'db1'), x, atol=tol, rtol=tol)


@dec.slow
def test_waverecn_all_wavelets_modes():
    # test 2D case using all wavelets and modes
    rstate = np.random.RandomState(1234)
    r = rstate.randn(80, 96)
    for wavelet in wavelist:
        for mode in pywt.Modes.modes:
            coeffs = pywt.wavedecn(r, wavelet, mode=mode)
            assert_allclose(pywt.waverecn(coeffs, wavelet, mode=mode),
                            r, rtol=tol_single, atol=tol_single)


def test_coeffs_to_array():
    # single element list returns just the first element
    a_coeffs = [np.arange(8).reshape(2, 4), ]
    arr = pywt.coeffs_to_array(a_coeffs)
    assert_allclose(arr, a_coeffs[0])

    assert_raises(ValueError, pywt.coeffs_to_array, [])
    # invalid second element (not a dictionary of detail coeffs)
    assert_raises(ValueError, pywt.coeffs_to_array, [a_coeffs[0], ] * 2)


def test_wavedecn_coeff_reshape_even():
    # verify round trip is correct:
    #   wavedecn - >coeffs_to_array-> array_to_coeffs -> waverecn
    rng = np.random.RandomState(1234)
    x1 = rng.randn(48, 32, 16)
    for mode in pywt.Modes.modes:
        for wave in wavelist:
            w = pywt.Wavelet(wave)
            maxlevel = pywt.dwt_max_level(np.min(x1.shape), w.dec_len)
            if maxlevel == 0:
                continue
            coeffs = pywt.wavedecn(x1, w, mode=mode)
            coeff_arr, coeff_slices = pywt.coeffs_to_array(coeffs)
            coeffs2 = pywt.array_to_coeffs(coeff_arr, coeff_slices)
            x1r = pywt.waverecn(coeffs2, w, mode=mode)
            assert_allclose(x1, x1r, rtol=1e-4, atol=1e-4)


def test_waverecn_coeff_reshape_odd():
    # verify round trip is correct:
    #   wavedecn - >coeffs_to_array-> array_to_coeffs -> waverecn
    rng = np.random.RandomState(1234)
    x1 = rng.randn(35, 33)
    for mode in pywt.Modes.modes:
        for wave in ['haar', ]:
            w = pywt.Wavelet(wave)
            maxlevel = pywt.dwt_max_level(np.min(x1.shape), w.dec_len)
            if maxlevel == 0:
                continue
            coeffs = pywt.wavedecn(x1, w, mode=mode)
            coeff_arr, coeff_slices = pywt.coeffs_to_array(coeffs)
            coeffs2 = pywt.array_to_coeffs(coeff_arr, coeff_slices)
            x1r = pywt.waverecn(coeffs2, w, mode=mode)
            # truncate reconstructed values to original shape
            x1r = x1r[[slice(s) for s in x1.shape]]
            assert_allclose(x1, x1r, rtol=1e-4, atol=1e-4)


if __name__ == '__main__':
    run_module_suite()
