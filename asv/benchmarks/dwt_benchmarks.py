import numpy as np
import pywt


class DwtTimeSuiteBase(object):
    """
    Set-up for (I)DWT timing.
    """
    params = ([16, 100, 101, 256, 490, 491, 512],
              ['haar', 'db4', 'sym20'],)
    param_names = ('n', 'wavelet')

    def setup(self, n, wavelet):
        self.data = np.ones(n, dtype='float')


class DwtTimeSuite(DwtTimeSuiteBase):
    def time_dwt(self, n, wavelet):
        pywt.dwt(self.data, wavelet)


class IdwtTimeSuite(DwtTimeSuiteBase):
    def setup(self, n, wavelet):
        super(IdwtTimeSuite, self).setup(n, wavelet)
        self.cA, self.cD = pywt.dwt(self.data, wavelet)


    def time_idwt(self, n, wavelet):
        pywt.idwt(self.cA, self.cD, wavelet)


class DwtnTimeSuiteBase(object):
    """
    Set-up for (I)DWTN timing.
    """
    params = ([1, 2, 3],
              [16, 100, 101, 256],
              ['haar', 'db4', 'sym20'],)
    param_names = ('D', 'n', 'wavelet')

    def setup(self, D, n, wavelet):
        self.data = np.ones((n,) * D, dtype='float')


class DwtnTimeSuite(DwtnTimeSuiteBase):
    def time_dwtn(self, D, n, wavelet):
        pywt.dwtn(self.data, wavelet)


class IdwtnTimeSuite(DwtnTimeSuiteBase):
    def setup(self, D, n, wavelet):
        super(IdwtnTimeSuite, self).setup(D, n, wavelet)
        self.data = pywt.dwtn(self.data, wavelet)


    def time_idwtn(self, D, n, wavelet):
        pywt.idwtn(self.data, wavelet)
