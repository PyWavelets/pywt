cimport wavelet
cimport numpy as np

ctypedef Py_ssize_t Index_t

ctypedef fused data_t:
    np.float32_t
    np.float64_t

cdef public class Wavelet [type WaveletType, object WaveletObject]:
    cdef wavelet.Wavelet* w

    cdef readonly name
    cdef readonly number

cpdef np.dtype _check_dtype(data)

# FIXME: To be removed
cdef c_wavelet_from_object(wavelet)
