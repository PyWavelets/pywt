from ._pywt cimport DiscreteWavelet, data_t

cpdef upcoef(bint do_rec_a, data_t[::1] coeffs, DiscreteWavelet wavelet, int level, int take)
