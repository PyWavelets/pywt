"""
Test used to verify PyWavelets Discrete Wavelet Transform computation
accuracy against MathWorks Wavelet Toolbox.
"""

from __future__ import division, print_function, absolute_import

import math

import numpy as np
from numpy.testing import assert_, dec, run_module_suite

import pywt


_has_matlab = False
try:
    from mlabwrap import mlab
except ImportError:
    print("To run Matlab compatibility tests you need to have MathWorks "
          "MATLAB, MathWorks Wavelet Toolbox and mlabwrap Python extension "
          "installed.")
    _has_matlab = True


def mse(ar1, ar2):
    """Mean squared error"""
    ar1 = np.asarray(ar1, dtype=np.float64)
    ar2 = np.asarray(ar2, dtype=np.float64)
    dif = (ar1 - ar2)**2
    return dif.sum() / ar1.size


def rms(ar1, ar2):
    """Root mean squared error"""
    return math.sqrt(mse(ar1, ar2))


@dec.skipif(_has_matlab)
def test_accuracy():
    # list of mode names in pywt and matlab
    modes = [('zpd', 'zpd'), ('cpd', 'sp0'), ('sym', 'sym'),
             ('ppd', 'ppd'), ('sp1', 'sp1'), ('per', 'per')]

    families = ('db', 'sym', 'coif', 'bior', 'rbio')
    wavelets = sum([pywt.wavelist(name) for name in families], [])
    for pmode, mmode in modes:
        for wavelet in wavelets:
            yield check_accuracy, pmode, mmode, wavelet


def check_accuracy(pmode, mmode, wavelet):
    # max RMSE
    epsilon = 1.0e-10

    w = pywt.Wavelet(wavelet)
    data_size = range(w.dec_len, 40) + [100, 200, 500, 1000, 50000]
    np.random.seed(1234)

    for N in data_size:
        data = np.random.random(N)

        # PyWavelets result
        pa, pd = pywt.dwt(data, wavelet, pmode)

        # Matlab result
        ma, md = mlab.dwt(data, wavelet, 'mode', mmode, nout=2)
        ma = ma.flat
        md = md.flat

        # calculate error measures
        mse_a, mse_d = mse(pa, ma), mse(pd, md)
        rms_a, rms_d = math.sqrt(mse_a), math.sqrt(mse_d)

        msg = ('[RMS_A > EPSILON] for Mode: %s, Wavelet: %s, '
              'Length: %d, rms=%.3g' % (pmode, wavelet, len(data), rms_a))
        assert_(rms_a < epsilon, msg=msg)

        msg = ('[RMS_D > EPSILON] for Mode: %s, Wavelet: %s, '
               'Length: %d, rms=%.3g' % (pmode, wavelet, len(data), rms_d))
        assert_(rms_d < epsilon, msg=msg)


if __name__ == '__main__':
    run_module_suite()
