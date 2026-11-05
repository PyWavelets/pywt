#!/usr/bin/env python
import os
import pickle
from itertools import product

import numpy as np
import pytest
from numpy.testing import (
    assert_allclose,
    assert_almost_equal,
    assert_equal,
    assert_raises,
)

import pywt


def ref_gaus(LB, UB, N, num):
    X = np.linspace(LB, UB, N)
    F0 = (2./np.pi)**(1./4.)*np.exp(-(X**2))
    if (num == 1):
        psi = -2.*X*F0
    elif (num == 2):
        psi = -2/(3**(1/2))*(-1 + 2*X**2)*F0
    elif (num == 3):
        psi = -4/(15**(1/2))*X*(3 - 2*X**2)*F0
    elif (num == 4):
        psi = 4/(105**(1/2))*(3 - 12*X**2 + 4*X**4)*F0
    elif (num == 5):
        psi = 8/(3*(105**(1/2)))*X*(-15 + 20*X**2 - 4*X**4)*F0
    elif (num == 6):
        psi = -8/(3*(1155**(1/2)))*(-15 + 90*X**2 - 60*X**4 + 8*X**6)*F0
    elif (num == 7):
        psi = -16/(3*(15015**(1/2)))*X*(105 - 210*X**2 + 84*X**4 - 8*X**6)*F0
    elif (num == 8):
        psi = 16/(45*(1001**(1/2)))*(105 - 840*X**2 + 840*X**4 -
                                     224*X**6 + 16*X**8)*F0
    return (psi, X)


def ref_cgau(LB, UB, N, num):
    X = np.linspace(LB, UB, N)
    F0 = np.exp(-X**2)
    F1 = np.exp(-1j*X)
    F2 = (F1*F0)/(np.exp(-1/2)*2**(1/2)*np.pi**(1/2))**(1/2)
    if (num == 1):
        psi = F2*(-1j - 2*X)*2**(1/2)
    elif (num == 2):
        psi = 1/3*F2*(-3 + 4j*X + 4*X**2)*6**(1/2)
    elif (num == 3):
        psi = 1/15*F2*(7j + 18*X - 12j*X**2 - 8*X**3)*30**(1/2)
    elif (num == 4):
        psi = 1/105*F2*(25 - 56j*X - 72*X**2 + 32j*X**3 + 16*X**4)*210**(1/2)
    elif (num == 5):
        psi = 1/315*F2*(-81j - 250*X + 280j*X**2 + 240*X**3 -
                        80j*X**4 - 32*X**5)*210**(1/2)
    elif (num == 6):
        psi = 1/3465*F2*(-331 + 972j*X + 1500*X**2 - 1120j*X**3 - 720*X**4 +
                         192j*X**5 + 64*X**6)*2310**(1/2)
    elif (num == 7):
        psi = 1/45045*F2*(
            1303j + 4634*X - 6804j*X**2 - 7000*X**3 + 3920j*X**4 + 2016*X**5 -
            448j*X**6 - 128*X**7)*30030**(1/2)
    elif (num == 8):
        psi = 1/45045*F2*(
            5937 - 20848j*X - 37072*X**2 + 36288j*X**3 + 28000*X**4 -
            12544j*X**5 - 5376*X**6 + 1024j*X**7 + 256*X**8)*2002**(1/2)

    psi = psi/np.real(np.sqrt(np.real(np.sum(psi*np.conj(psi)))*(X[1] - X[0])))
    return (psi, X)


def sinc2(x):
    y = np.ones_like(x)
    k = np.where(x)[0]
    y[k] = np.sin(np.pi*x[k])/(np.pi*x[k])
    return y


def ref_shan(LB, UB, N, Fb, Fc):
    x = np.linspace(LB, UB, N)
    psi = np.sqrt(Fb)*(sinc2(Fb*x)*np.exp(2j*np.pi*Fc*x))
    return (psi, x)


def ref_fbsp(LB, UB, N, m, Fb, Fc):
    x = np.linspace(LB, UB, N)
    psi = np.sqrt(Fb)*((sinc2(Fb*x/m)**m)*np.exp(2j*np.pi*Fc*x))
    return (psi, x)


def ref_cmor(LB, UB, N, Fb, Fc):
    x = np.linspace(LB, UB, N)
    psi = ((np.pi*Fb)**(-0.5))*np.exp(2j*np.pi*Fc*x)*np.exp(-(x**2)/Fb)
    return (psi, x)


def ref_morl(LB, UB, N):
    x = np.linspace(LB, UB, N)
    psi = np.exp(-(x**2)/2)*np.cos(5*x)
    return (psi, x)


def ref_mexh(LB, UB, N):
    x = np.linspace(LB, UB, N)
    psi = (2/(np.sqrt(3)*np.pi**0.25))*np.exp(-(x**2)/2)*(1 - (x**2))
    return (psi, x)


def test_gaus():
    LB = -5
    UB = 5
    N = 1000
    for num in np.arange(1, 9):
        [psi, x] = ref_gaus(LB, UB, N, num)
        w = pywt.ContinuousWavelet("gaus" + str(num))
        PSI, X = w.wavefun(length=N)

        assert_allclose(np.real(PSI), np.real(psi))
        assert_allclose(np.imag(PSI), np.imag(psi))
        assert_allclose(X, x)


@pytest.mark.parametrize('dtype', [np.float32, np.float64])
def test_continuous_wavelet_dtype(dtype):
    wavelet = pywt.ContinuousWavelet('cmor1.5-1.0', dtype)
    int_psi, x = pywt.integrate_wavelet(wavelet)
    assert int_psi.real.dtype == dtype
    assert x.dtype == dtype


def test_continuous_wavelet_invalid_dtype():
    with pytest.raises(ValueError):
        pywt.ContinuousWavelet('gaus5', np.complex64)
    with pytest.raises(ValueError):
        pywt.ContinuousWavelet('gaus5', np.int_)


def test_cgau():
    LB = -5
    UB = 5
    N = 1000
    for num in np.arange(1, 9):
        [psi, x] = ref_cgau(LB, UB, N, num)
        w = pywt.ContinuousWavelet("cgau" + str(num))
        PSI, X = w.wavefun(length=N)

        assert_allclose(np.real(PSI), np.real(psi))
        assert_allclose(np.imag(PSI), np.imag(psi))
        assert_allclose(X, x)


def test_shan():
    LB = -20
    UB = 20
    N = 1000
    Fb = 1
    Fc = 1.5

    [psi, x] = ref_shan(LB, UB, N, Fb, Fc)
    w = pywt.ContinuousWavelet(f"shan{Fb}-{Fc}")
    assert_almost_equal(w.center_frequency, Fc)
    assert_almost_equal(w.bandwidth_frequency, Fb)
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi), atol=1e-15)
    assert_allclose(np.imag(PSI), np.imag(psi), atol=1e-15)
    assert_allclose(X, x, atol=1e-15)

    LB = -20
    UB = 20
    N = 1000
    Fb = 1.5
    Fc = 1

    [psi, x] = ref_shan(LB, UB, N, Fb, Fc)
    w = pywt.ContinuousWavelet(f"shan{Fb}-{Fc}")
    assert_almost_equal(w.center_frequency, Fc)
    assert_almost_equal(w.bandwidth_frequency, Fb)
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi), atol=1e-15)
    assert_allclose(np.imag(PSI), np.imag(psi), atol=1e-15)
    assert_allclose(X, x, atol=1e-15)


def test_cmor():
    LB = -20
    UB = 20
    N = 1000
    Fb = 1
    Fc = 1.5

    [psi, x] = ref_cmor(LB, UB, N, Fb, Fc)
    w = pywt.ContinuousWavelet(f"cmor{Fb}-{Fc}")
    assert_almost_equal(w.center_frequency, Fc)
    assert_almost_equal(w.bandwidth_frequency, Fb)
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi), atol=1e-15)
    assert_allclose(np.imag(PSI), np.imag(psi), atol=1e-15)
    assert_allclose(X, x, atol=1e-15)

    LB = -20
    UB = 20
    N = 1000
    Fb = 1.5
    Fc = 1

    [psi, x] = ref_cmor(LB, UB, N, Fb, Fc)
    w = pywt.ContinuousWavelet(f"cmor{Fb}-{Fc}")
    assert_almost_equal(w.center_frequency, Fc)
    assert_almost_equal(w.bandwidth_frequency, Fb)
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi), atol=1e-15)
    assert_allclose(np.imag(PSI), np.imag(psi), atol=1e-15)
    assert_allclose(X, x, atol=1e-15)


def test_fbsp():
    LB = -20
    UB = 20
    N = 1000
    M = 2
    Fb = 1
    Fc = 1.5

    [psi, x] = ref_fbsp(LB, UB, N, M, Fb, Fc)

    w = pywt.ContinuousWavelet(f"fbsp{M}-{Fb}-{Fc}")
    assert_almost_equal(w.center_frequency, Fc)
    assert_almost_equal(w.bandwidth_frequency, Fb)
    w.fbsp_order = M
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi), atol=1e-15)
    assert_allclose(np.imag(PSI), np.imag(psi), atol=1e-15)
    assert_allclose(X, x, atol=1e-15)

    LB = -20
    UB = 20
    N = 1000
    M = 2
    Fb = 1.5
    Fc = 1

    [psi, x] = ref_fbsp(LB, UB, N, M, Fb, Fc)
    w = pywt.ContinuousWavelet(f"fbsp{M}-{Fb}-{Fc}")
    assert_almost_equal(w.center_frequency, Fc)
    assert_almost_equal(w.bandwidth_frequency, Fb)
    w.fbsp_order = M
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi), atol=1e-15)
    assert_allclose(np.imag(PSI), np.imag(psi), atol=1e-15)
    assert_allclose(X, x, atol=1e-15)

    LB = -20
    UB = 20
    N = 1000
    M = 3
    Fb = 1.5
    Fc = 1.2

    [psi, x] = ref_fbsp(LB, UB, N, M, Fb, Fc)
    w = pywt.ContinuousWavelet(f"fbsp{M}-{Fb}-{Fc}")
    assert_almost_equal(w.center_frequency, Fc)
    assert_almost_equal(w.bandwidth_frequency, Fb)
    w.fbsp_order = M
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)
    # TODO: investigate why atol = 1e-5 is necessary
    assert_allclose(np.real(PSI), np.real(psi), atol=1e-5)
    assert_allclose(np.imag(PSI), np.imag(psi), atol=1e-5)
    assert_allclose(X, x, atol=1e-15)


def test_morl():
    LB = -5
    UB = 5
    N = 1000

    [psi, x] = ref_morl(LB, UB, N)
    w = pywt.ContinuousWavelet("morl")
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi))
    assert_allclose(np.imag(PSI), np.imag(psi))
    assert_allclose(X, x)


def test_mexh():
    LB = -5
    UB = 5
    N = 1000

    [psi, x] = ref_mexh(LB, UB, N)
    w = pywt.ContinuousWavelet("mexh")
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi))
    assert_allclose(np.imag(PSI), np.imag(psi))
    assert_allclose(X, x)

    LB = -5
    UB = 5
    N = 1001

    [psi, x] = ref_mexh(LB, UB, N)
    w = pywt.ContinuousWavelet("mexh")
    w.upper_bound = UB
    w.lower_bound = LB
    PSI, X = w.wavefun(length=N)

    assert_allclose(np.real(PSI), np.real(psi))
    assert_allclose(np.imag(PSI), np.imag(psi))
    assert_allclose(X, x)


def test_cwt_parameters_in_names():

    for func in [pywt.ContinuousWavelet, pywt.DiscreteContinuousWavelet]:
        for name in ['fbsp', 'cmor', 'shan']:
            # additional parameters should be specified within the name
            with pytest.warns(FutureWarning):
                func(name)

        for name in ['cmor', 'shan']:
            # valid names
            func(name + '1.5-1.0')
            func(name + '1-4')

            # invalid names
            assert_raises(ValueError, func, name + '1.0')
            assert_raises(ValueError, func, name + 'B-C')
            assert_raises(ValueError, func, name + '1.0-1.0-1.0')

        # valid names
        func('fbsp1-1.5-1.0')
        func('fbsp1.0-1.5-1')
        func('fbsp2-5-1')

        # invalid name (non-integer order)
        assert_raises(ValueError, func, 'fbsp1.5-1-1')
        assert_raises(ValueError, func, 'fbspM-B-C')

        # invalid name (too few or too many params)
        assert_raises(ValueError, func, 'fbsp1.0')
        assert_raises(ValueError, func, 'fbsp1.0-0.4')
        assert_raises(ValueError, func, 'fbsp1-1-1-1')


@pytest.mark.parametrize('dtype, tol, method',
                         [(np.float32, 1e-5, 'conv'),
                          (np.float32, 1e-5, 'fft'),
                          (np.float64, 1e-13, 'conv'),
                          (np.float64, 1e-13, 'fft')])
def test_cwt_complex(dtype, tol, method):
    time, sst = pywt.data.nino()
    sst = np.asarray(sst, dtype=dtype)
    dt = time[1] - time[0]
    wavelet = 'cmor1.5-1.0'
    scales = np.arange(1, 32)

    # real-valued tranfsorm as a reference
    [cfs, f] = pywt.cwt(sst, scales, wavelet, dt, method=method)

    # verify same precision
    assert_equal(cfs.real.dtype, sst.dtype)

    # complex-valued transform equals sum of the transforms of the real
    # and imaginary components
    sst_complex = sst + 1j*sst
    [cfs_complex, f] = pywt.cwt(sst_complex, scales, wavelet, dt,
                                method=method)
    assert_allclose(cfs + 1j*cfs, cfs_complex, atol=tol, rtol=tol)
    # verify dtype is preserved
    assert_equal(cfs_complex.dtype, sst_complex.dtype)


@pytest.mark.parametrize('axis, method', list(product([0, 1], ['conv', 'fft'])))
def test_cwt_batch(axis, method):
    dtype = np.float64
    time, sst = pywt.data.nino()
    n_batch = 8
    batch_axis = 1 - axis
    sst1 = np.asarray(sst, dtype=dtype)
    sst = np.stack((sst1, ) * n_batch, axis=batch_axis)
    dt = time[1] - time[0]
    wavelet = 'cmor1.5-1.0'
    scales = np.arange(1, 32)

    # non-batch transform as reference
    [cfs1, f] = pywt.cwt(sst1, scales, wavelet, dt, method=method, axis=axis)

    shape_in = sst.shape
    [cfs, f] = pywt.cwt(sst, scales, wavelet, dt, method=method, axis=axis)

    # shape of input is not modified
    assert_equal(shape_in, sst.shape)

    # verify same precision
    assert_equal(cfs.real.dtype, sst.dtype)

    # verify expected shape
    assert_equal(cfs.shape[0], len(scales))
    assert_equal(cfs.shape[1 + batch_axis], n_batch)
    assert_equal(cfs.shape[1 + axis], sst.shape[axis])

    # batch result on stacked input is the same as stacked 1d result
    assert_almost_equal(cfs, np.stack((cfs1,) * n_batch, axis=batch_axis + 1),
                        decimal=12)


def test_cwt_small_scales():
    data = np.zeros(32)

    # A scale of 0.1 was chosen specifically to give a filter of length 2 for
    # mexh.  This corner case should not raise an error.
    cfs, f = pywt.cwt(data, scales=0.1, wavelet='mexh')
    assert_allclose(cfs, np.zeros_like(cfs))

    # extremely short scale factors raise a ValueError
    assert_raises(ValueError, pywt.cwt, data, scales=0.01, wavelet='mexh')

def test_cwt_zero_scale():
    data = np.zeros(32)
    scales = np.arange(0, 4)

    # scale that includes 0 throws ValueError to prevent IndexError
    assert_raises(ValueError, pywt.cwt, data, scales=scales, wavelet='morl')

def test_cwt_negative_scale():
    data = np.zeros(32)
    scales = np.asarray([-1, -2, -3])

    # scale that includes negative values throws ValueError to prevent IndexError
    assert_raises(ValueError, pywt.cwt, data, scales=scales, wavelet='morl')


def test_cwt_method_fft():
    rstate = np.random.RandomState(1)
    data = rstate.randn(50)
    data[15] = 1.
    scales = np.arange(1, 64)
    wavelet = 'cmor1.5-1.0'

    # build a reference cwt with the legacy np.conv() method
    cfs_conv, _ = pywt.cwt(data, scales, wavelet, method='conv')

    # compare with the fft based convolution
    cfs_fft, _ = pywt.cwt(data, scales, wavelet, method='fft')
    assert_allclose(cfs_conv, cfs_fft, rtol=0, atol=1e-13)


@pytest.mark.parametrize('dtype, tol', [(np.float32, 1e-5),
                                        (np.float64, 1e-13)])
@pytest.mark.parametrize('shape, axis', [((49,), -1),
                                         ((3, 50), 1),
                                         ((49, 3), 0)])
def test_cwt_method_fft_real(dtype, tol, shape, axis):
    rstate = np.random.RandomState(1)
    data = rstate.randn(*shape).astype(dtype)
    scales = np.r_[1.0625, np.arange(1, 64)]

    cfs_conv, _ = pywt.cwt(
        data, scales, 'morl', method='conv', axis=axis
    )
    cfs_fft, _ = pywt.cwt(
        data, scales, 'morl', method='fft', axis=axis
    )

    assert_equal(cfs_fft.dtype, dtype)
    assert_allclose(cfs_conv, cfs_fft, rtol=tol, atol=tol)


@pytest.mark.parametrize('dtype, tol', [(np.complex64, 1e-5),
                                        (np.complex128, 1e-13)])
def test_cwt_method_fft_complex_data_real_wavelet(dtype, tol):
    rstate = np.random.RandomState(1)
    data = (rstate.randn(49) + 1j * rstate.randn(49)).astype(dtype)
    scales = np.r_[1.0625, np.arange(1, 16)]

    cfs_conv, _ = pywt.cwt(data, scales, 'morl', method='conv')
    cfs_fft, _ = pywt.cwt(data, scales, 'morl', method='fft')

    assert_equal(cfs_fft.dtype, dtype)
    assert_allclose(cfs_conv, cfs_fft, rtol=tol, atol=tol)


def test_cwt_normalization_convention():
    # cwt works in units of samples: with the scale a and the shift b both
    # given in samples, coefs[a, b] == 1/sqrt(a) * sum_n x[n] conj(psi((n-b)/a))
    # and no sampling interval enters.
    fs = 3000.
    Fb, Fc = 14., 2.
    wavelet = pywt.ContinuousWavelet(f'cmor{Fb:g}-{Fc:g}')
    x = np.sin(2 * np.pi * 40 * np.arange(3000) / fs)
    scale = pywt.frequency2scale(wavelet, 40 / fs)

    cfs, freqs = pywt.cwt(x, scale, wavelet, sampling_period=1 / fs)
    assert_allclose(freqs, [40.], rtol=1e-12)

    # psi is sampled at bin midpoints because cwt convolves with the integral
    # of psi and then differences it, which averages psi over each sample bin.
    lb, ub = wavelet.lower_bound, wavelet.upper_bound
    k = np.arange(int(scale * (ub - lb)) + 1)
    psi, _ = ref_cmor(lb + 0.5 / scale, ub + 0.5 / scale, k.size, Fb, Fc)
    # the filter is conjugated *and* reversed; convolving with conj(psi) alone
    # gives the complex conjugate of the correct result, which an abs()
    # comparison would not catch
    conv = np.convolve(x, np.conj(psi)[::-1]) / np.sqrt(scale)
    trim = (conv.size - x.size) // 2
    manual = conv[trim:trim + x.size]

    assert_allclose(manual, cfs[0], atol=1e-3 * np.max(np.abs(cfs[0])))

    # the coefficients themselves are unaffected by sampling_period
    cfs_unit, freqs_unit = pywt.cwt(x, scale, wavelet, sampling_period=1.)
    assert_allclose(cfs_unit, cfs, rtol=0, atol=0)
    assert_allclose(freqs_unit * fs, freqs, rtol=1e-12)


def test_continuous_wavelet_pickle(tmpdir):
    wavelet = pywt.ContinuousWavelet('cmor1.5-1.0')
    filename = os.path.join(tmpdir, 'cwav.pickle')
    with open(filename, 'wb') as f:
        pickle.dump(wavelet, f)
    with open(filename, 'rb') as f:
        wavelet2 = pickle.load(f)
    assert isinstance(wavelet2, pywt.ContinuousWavelet)
    assert wavelet2.name == wavelet.name


def test_cwt_discrete_wavelet_raises():
    # A discrete wavelet such as 'coif1' has no continuous form; cwt should
    # raise a clear error rather than an opaque AttributeError (gh-776).
    data = np.ones(100)
    for bad in ['coif1', 'db2', pywt.Wavelet('coif1')]:
        with pytest.raises(ValueError, match='continuous wavelet'):
            pywt.cwt(data, [1, 2], bad)

    # a continuous wavelet still works
    out, _ = pywt.cwt(data, [1, 2], 'morl')
    assert out.shape == (2, 100)
