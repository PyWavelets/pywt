from ._pywt cimport data_t, index_t, Wavelet
cimport numpy as np

# Used in _pywt (Wavelet.wavefun), so must be exported
cpdef _upcoef(part, np.ndarray[data_t, ndim=1, mode="c"] coeffs,
              Wavelet wavelet, int level, int take)
