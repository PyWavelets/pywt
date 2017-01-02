from ._pywt cimport Wavelet, data_t

cpdef upcoef(bint do_rec_a, data_t[::1] coeffs, Wavelet wavelet, int level,
             size_t take)
