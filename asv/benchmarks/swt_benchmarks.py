import numpy as np
import pywt


class SwtTimeSuiteBase(object):
    """
    Set-up for (I)DWT timing.
    """
    params = ([16, 32, 64, 128, 256],
              ['haar', 'db4', 'sym20'],)
    param_names = ('n', 'wavelet')

    def setup(self, n, wavelet):
        self.data = np.ones(n, dtype='float')


class SwtTimeSuite(SwtTimeSuiteBase):
    def time_swt(self, n, wavelet):
        pywt.swt(self.data, wavelet)


class IswtTimeSuite(SwtTimeSuiteBase):
    def setup(self, n, wavelet):
        super(IswtTimeSuite, self).setup(n, wavelet)
        self.coeffs = pywt.swt(self.data, wavelet)

    def time_iswt(self, n, wavelet):
        pywt.iswt(self.coeffs, wavelet)
