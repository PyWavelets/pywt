from ._pywt cimport data_t, index_t, Wavelet
cimport numpy as np

# Used in _pywt (Wavelet.wavefun), so must be exported
cpdef _upcoef(bint do_rec_a, data_t[::1] coeffs,
              Wavelet wavelet, unsigned int level, unsigned int take)
