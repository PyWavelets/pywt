import numpy as np
import pywt

try:
    Modes = pywt.Modes
except AttributeError:
    # old v0.3.0 API
    Modes = pywt.MODES


class DwtTimeSuiteBase(object):
    """
    Set-up for (I)DWT timing.
    """
    params = ([16, 100, 101, 256, 512, 2048],
              ['haar', 'db4', 'sym8'],
              Modes.modes)
    param_names = ('n', 'wavelet', 'modes')

    def setup(self, n, wavelet, mode):
        self.data = np.ones(n, dtype='float')


class DwtTimeSuite(DwtTimeSuiteBase):
    def time_dwt(self, n, wavelet, mode):
        pywt.dwt(self.data, wavelet, mode)


class IdwtTimeSuite(DwtTimeSuiteBase):
    def setup(self, n, wavelet, mode):
        super(IdwtTimeSuite, self).setup(n, wavelet, mode)
        self.cA, self.cD = pywt.dwt(self.data, wavelet, mode)

    def time_idwt(self, n, wavelet, mode):
        pywt.idwt(self.cA, self.cD, wavelet, mode)


class Dwt2TimeSuiteBase(object):
    """
    Set-up for (I)DWT2 timing.
    """
    params = ([16, 256],
              ['haar', 'db4', ],)
    param_names = ('n', 'wavelet')

    def setup(self, n, wavelet):
        self.data = np.ones((n, n), dtype='float')


class Dwt2TimeSuite(Dwt2TimeSuiteBase):
    def time_dwt2(self, n, wavelet):
        pywt.dwt2(self.data, wavelet)


class Idwt2TimeSuite(Dwt2TimeSuiteBase):
    def setup(self, n, wavelet):
        super(Idwt2TimeSuite, self).setup(n, wavelet)
        self.data = pywt.dwt2(self.data, wavelet)

    def time_idwt2(self, n, wavelet):
        pywt.idwt2(self.data, wavelet)


class DwtnTimeSuiteBase(object):
    """
    Set-up for (I)DWTN timing.
    """
    params = ([1, 2, 3],
              [16, 64, 256],
              ['haar', 'db4', 'sym8'],)
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


"""
Multilevel DWT benchmarks
"""


class WavedecTimeSuiteBase(object):
    """
    Set-up for wavedec, waverec timing.
    """
    params = ([16, 64, 256, 1024],
              ['haar', 'db4'],
              [np.float32, np.float64, np.complex64])
    param_names = ('n', 'wavelet', 'dtype')

    def setup(self, n, wavelet, dtype):
        self.data = np.ones((n, ), dtype=dtype)


class WavedecTimeSuite(WavedecTimeSuiteBase):
    def time_wavedec(self, n, wavelet, dtype):
        pywt.wavedec(self.data, wavelet)


class WaverecTimeSuite(WavedecTimeSuiteBase):
    def setup(self, n, wavelet, dtype):
        super(WaverecTimeSuite, self).setup(n, wavelet, dtype)
        self.data = pywt.wavedec(self.data, wavelet)

    def time_waverec(self, n, wavelet, dtype):
        pywt.waverec(self.data, wavelet)


class Wavedec2TimeSuiteBase(object):
    """
    Set-up for wavedec2, waverec2 timing.
    """
    params = ([16, 64, 256],
              ['haar', 'db4'],
              [np.float32, np.float64, np.complex64])
    param_names = ('n', 'wavelet', 'dtype')

    def setup(self, n, wavelet, dtype):
        self.data = np.ones((n, n), dtype=dtype)


class Wavedec2TimeSuite(Wavedec2TimeSuiteBase):
    def time_wavedec2(self, n, wavelet, dtype):
        pywt.wavedec2(self.data, wavelet)


class Waverec2TimeSuite(Wavedec2TimeSuiteBase):
    def setup(self, n, wavelet, dtype):
        super(Waverec2TimeSuite, self).setup(n, wavelet, dtype)
        self.data = pywt.wavedec2(self.data, wavelet)

    def time_waverec2(self, n, wavelet, dtype):
        pywt.waverec2(self.data, wavelet)


class WavedecnTimeSuiteBase(object):
    """
    Set-up for wavedecn, waverecn timing.
    """
    params = ([1, 2, 3],
              [16, 64, 256],
              ['haar', 'db4'],
              [np.float32, np.float64, np.complex64])
    param_names = ('D', 'n', 'wavelet', 'dtype')

    def setup(self, D, n, wavelet, dtype):
        try:
            from pywt import wavedecn
        except ImportError:
            raise NotImplementedError("wavedecn not available")
        self.data = np.ones((n,) * D, dtype=dtype)


class WavedecnTimeSuite(WavedecnTimeSuiteBase):
    def time_wavedecn(self, D, n, wavelet, dtype):
        pywt.wavedecn(self.data, wavelet)


class WaverecnTimeSuite(WavedecnTimeSuiteBase):
    def setup(self, D, n, wavelet, dtype):
        try:
            from pywt import waverecn
        except ImportError:
            raise NotImplementedError("waverecn not available")
        super(WaverecnTimeSuite, self).setup(D, n, wavelet, dtype)
        self.data = pywt.wavedecn(self.data, wavelet)

    def time_waverecn(self, D, n, wavelet, dtype):
        pywt.waverecn(self.data, wavelet)
