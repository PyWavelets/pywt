import numpy as np
import pywt


class SwtTimeSuiteBase(object):
    """
    Set-up for (I)SWT timing.
    """
    params = ([16, 64, 256, 1024, 4096],
              ['haar', 'db4', 'sym8'],)
    param_names = ('n', 'wavelet')

    def setup(self, n, wavelet):
        self.data = np.ones(n, dtype='float')


class SwtTimeSuite(SwtTimeSuiteBase):
    def time_swt(self, n, wavelet):
        pywt.swt(self.data, wavelet)


class IswtTimeSuite(SwtTimeSuiteBase):
    def setup(self, n, wavelet):
        try:
            from pywt import iswt
        except ImportError:
            raise NotImplementedError("iswt not available")
        super(IswtTimeSuite, self).setup(n, wavelet)
        self.coeffs = pywt.swt(self.data, wavelet)

    def time_iswt(self, n, wavelet):
        pywt.iswt(self.coeffs, wavelet)


class Swt2TimeSuiteBase(object):
    """
    Set-up for (I)SWT2 timing.
    """
    params = ([16, 64, 256],
              ['haar', 'db4'],)
    param_names = ('n', 'wavelet')

    def setup(self, n, wavelet):
        try:
            from pywt import swt2
        except ImportError:
            raise NotImplementedError("swt2 not available")
        self.data = np.ones((n, n), dtype='float')
        self.level = pywt.swt_max_level(n)


class Swt2TimeSuite(Swt2TimeSuiteBase):
    def time_swt2(self, n, wavelet):
        pywt.swt2(self.data, wavelet, self.level)


class Iswt2TimeSuite(Swt2TimeSuiteBase):
    def setup(self, n, wavelet):
        try:
            from pywt import iswt2
        except ImportError:
            raise NotImplementedError("iswt2 not available")
        super(Iswt2TimeSuite, self).setup(n, wavelet)
        self.data = pywt.swt2(self.data, wavelet, self.level)

    def time_iswt2(self, n, wavelet):
        pywt.iswt2(self.data, wavelet)


class SwtnTimeSuiteBase(object):
    """
    Set-up for (I)SWTN timing.
    """
    params = ([1, 2, 3],
              [16, 64],
              ['haar', 'db4'],
              [np.float32, np.float64, np.complex64])
    param_names = ('D', 'n', 'wavelet', 'dtype')

    def setup(self, D, n, wavelet, dtype):
        try:
            from pywt import swtn
        except ImportError:
            raise NotImplementedError("swtn not available")
        self.data = np.ones((n,) * D, dtype=dtype)
        self.level = 4  # run 4 levels in all cases


class SwtnTimeSuite(SwtnTimeSuiteBase):
    def time_swtn(self, D, n, wavelet, dtype):
        pywt.swtn(self.data, wavelet, self.level)


class IswtnTimeSuite(SwtnTimeSuiteBase):
    def setup(self, D, n, wavelet, dtype):
        try:
            from pywt import iswtn
        except ImportError:
            raise NotImplementedError("iswtn not available")
        super(IswtnTimeSuite, self).setup(D, n, wavelet, dtype)
        self.data = pywt.swtn(self.data, wavelet, self.level)

    def time_iswtn(self, D, n, wavelet, dtype):
        pywt.iswtn(self.data, wavelet)
