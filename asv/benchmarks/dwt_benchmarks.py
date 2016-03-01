import numpy as np
import pywt


class DwtTimeSuiteBase(object):
    """
    Set-up for (I)DWT timing.
    """
    params = ([16, 100, 101, 256, 490, 491, 512],
              ['haar', 'db4', 'sym20'],
              pywt.Modes.modes)
    param_names = ('n', 'wavelet', 'modes')

    def setup(self, n, wavelet, mode):
        self.data = np.ones(n, dtype='float')
        self.wavelet = pywt.Wavelet(wavelet)
        self.mode = pywt.Modes.from_object(mode)


class DwtTimeSuite(DwtTimeSuiteBase):
    def time_dwt(self, n, wavelet, mode):
        pywt.dwt(self.data, wavelet, mode)

    def time_dwt_ext(self, n, wavelet, mode):
        pywt._extensions._dwt.dwt_single(self.data, self.wavelet, self.mode)


class IdwtTimeSuite(DwtTimeSuiteBase):
    def setup(self, n, wavelet, mode):
        super(IdwtTimeSuite, self).setup(n, wavelet, mode)
        self.cA, self.cD = pywt.dwt(self.data, wavelet, mode)

    def time_idwt(self, n, wavelet, mode):
        pywt.idwt(self.cA, self.cD, wavelet, mode)

    def time_idwt_ext(self, n, wavelet, mode):
        pywt._extensions._dwt.idwt_single(self.cA, self.cD, self.wavelet, self.mode)


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
