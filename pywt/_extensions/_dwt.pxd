from ._pywt cimport data_t, index_t, Wavelet
cimport numpy as np

cpdef _dwt(np.ndarray[data_t, ndim=1] data, object wavelet, object mode)

cpdef _downcoef(part, np.ndarray[data_t, ndim=1, mode="c"] data,
                object wavelet, object mode, int level)

cpdef dwt_axis(np.ndarray data, object wavelet, object mode, unsigned int axis)

cpdef _idwt(np.ndarray[data_t, ndim=1, mode="c"] cA,
            np.ndarray[data_t, ndim=1, mode="c"] cD,
            object wavelet, object mode)

cpdef _upcoef(part, np.ndarray[data_t, ndim=1, mode="c"] coeffs, wavelet,
              int level, int take)

cpdef idwt_axis(np.ndarray coefs_a, np.ndarray coefs_d, object wavelet,
                object mode, unsigned int axis)
