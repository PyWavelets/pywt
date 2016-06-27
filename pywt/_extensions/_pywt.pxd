cimport wavelet
cimport numpy as np

ctypedef Py_ssize_t pywt_index_t

ctypedef fused data_t:
    np.float32_t
    np.float64_t

cdef public class Wavelet [type WaveletType, object WaveletObject]:
    cdef wavelet.DiscreteWavelet* dw
    cdef wavelet.ContinuousWavelet* cw

    cdef readonly name
    cdef readonly number

cpdef np.dtype _check_dtype(data)

# FIXME: To be removed
cdef c_wavelet_from_object(wavelet)
