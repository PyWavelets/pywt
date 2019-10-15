import numpy as np
import pywt


class CwtTimeSuiteBase(object):
    """
    Set-up for CWT timing.
    """
    params = ([32, 128, 512, 2048],
              ['cmor', 'cgau4', 'fbsp', 'gaus4', 'mexh', 'morl', 'shan'],
              [16, 64, 256],
              [np.float32, np.float64],
              ['conv', 'fft'],
              )
    param_names = ('n', 'wavelet', 'max_scale', 'dtype', 'method')

    def setup(self, n, wavelet, max_scale, dtype, method):
        try:
            from pywt import cwt
        except ImportError:
            raise NotImplementedError("cwt not available")
        self.data = np.ones(n, dtype=dtype)
        self.batch_data = np.ones((5, n), dtype=dtype)
        self.scales = np.arange(1, max_scale + 1)


class CwtTimeSuite(CwtTimeSuiteBase):
    def time_cwt(self, n, wavelet, max_scale, dtype, method):
        try:
            pywt.cwt(self.data, self.scales, wavelet, method=method)
        except TypeError:
            # older PyWavelets does not support use of the method argument
            if method == 'fft':
                raise NotImplementedError(
                    "fft-based convolution not available.")
            pywt.cwt(self.data, self.scales, wavelet)

    def time_cwt_batch(self, n, wavelet, max_scale, dtype, method):
        try:
            pywt.cwt(self.batch_data, self.scales, wavelet, method=method,
                     axis=-1)
        except TypeError:
            # older PyWavelets does not support the axis argument
            raise NotImplementedError(
                "axis argument not available.")
