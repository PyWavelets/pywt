cimport wavelet
cimport numpy as np

ctypedef Py_ssize_t pywt_index_t

ctypedef fused data_t:
    np.float32_t
    np.float64_t

cdef public class DiscreteWavelet [type DiscreteWaveletType, object DiscreteWaveletObject]:
    cdef wavelet.DiscreteWavelet* w

    cdef readonly name
    cdef readonly number

cdef public class ContinuousWavelet [type ContinuousWaveletType, object ContinuousWaveletObject]:
    cdef wavelet.ContinuousWavelet* w

    cdef readonly name
    cdef readonly number

cpdef np.dtype _check_dtype(data)

# FIXME: To be removed
cdef c_wavelet_from_object(wavelet)
