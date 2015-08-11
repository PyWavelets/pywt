"""
Test used to verify PyWavelets Discrete Wavelet Transform computation
accuracy against MathWorks Wavelet Toolbox.
"""

from __future__ import division, print_function, absolute_import

import numpy as np
from numpy.testing import assert_, dec, run_module_suite

import pywt


_has_matlab = False
try:
    from pymatbridge import Matlab
    mlab = Matlab()
except ImportError:
    print("To run Matlab compatibility tests you need to have MathWorks "
          "MATLAB, MathWorks Wavelet Toolbox and the pymatbridge Python "
          "package installed.")
    _has_matlab = True


@dec.skipif(_has_matlab)
def test_accuracy():

    # list of mode names in pywt and matlab
    modes = [('zpd', 'zpd'), ('cpd', 'sp0'), ('sym', 'sym'),
             ('ppd', 'ppd'), ('sp1', 'sp1'), ('per', 'per')]

    families = ('db', 'sym', 'coif', 'bior', 'rbio')
    wavelets = sum([pywt.wavelist(name) for name in families], [])
    mlab.start()
    try:
        for pmode, mmode in modes:
            for wavelet in wavelets:
                yield check_accuracy, pmode, mmode, wavelet
    finally:
        mlab.stop()


def check_accuracy(pmode, mmode, wavelet):
    # max RMSE
    epsilon = 1.0e-10

    w = pywt.Wavelet(wavelet)
    data_size = [w.dec_len, w.dec_len + 1]
    np.random.seed(1234)

    for N in data_size:
        data = np.random.random(N)

        # PyWavelets result
        pa, pd = pywt.dwt(data, wavelet, pmode)

        # Matlab result
        mlab.set_variable('data', data)
        mlab.set_variable('wavelet', wavelet)
        mlab_code = "[ma, md] = dwt(data, wavelet, 'mode', '%s');" % mmode
        res = mlab.run_code(mlab_code)
        # need np.asarray because sometimes the output is type float
        ma = np.asarray(mlab.get_variable('ma')).flat
        md = np.asarray(mlab.get_variable('md')).flat

        # calculate error measures
        rms_a = np.sqrt(np.mean((pa-ma)**2))
        rms_d = np.sqrt(np.mean((pd-md)**2))

        msg = ('[RMS_A > EPSILON] for Mode: %s, Wavelet: %s, '
               'Length: %d, rms=%.3g' % (pmode, wavelet, len(data), rms_a))
        assert_(rms_a < epsilon, msg=msg)

        msg = ('[RMS_D > EPSILON] for Mode: %s, Wavelet: %s, '
               'Length: %d, rms=%.3g' % (pmode, wavelet, len(data), rms_d))
        assert_(rms_d < epsilon, msg=msg)


if __name__ == '__main__':
    run_module_suite()
