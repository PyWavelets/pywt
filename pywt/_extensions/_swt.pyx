#cython: boundscheck=False, wraparound=False
cimport common
cimport c_wt

import numpy as np
cimport numpy as np

from common cimport pywt_index_t
from ._pywt cimport c_wavelet_from_object, data_t, Wavelet, _check_dtype


def swt_max_level(size_t input_len):
    """
    swt_max_level(input_len)

    Calculates the maximum level of Stationary Wavelet Transform for data of
    given length.

    Parameters
    ----------
    input_len : int
        Input data length.

    Returns
    -------
    max_level : int
        Maximum level of Stationary Wavelet Transform for data of given length.

    """
    return common.swt_max_level(input_len)


def swt(data_t[::1] data, Wavelet wavelet, size_t level, size_t start_level):
    cdef data_t[::1] cA, cD
    cdef Wavelet w
    cdef int i, retval
    cdef size_t end_level = start_level + level
    cdef size_t data_size, output_len

    if data.size % 2:
        raise ValueError("Length of data must be even.")

    if level < 1:
        raise ValueError("Level value must be greater than zero.")
    if start_level >= common.swt_max_level(data.size):
        raise ValueError("start_level must be less than %d." %
                         common.swt_max_level(data.size))

    if end_level > common.swt_max_level(data.size):
        msg = ("Level value too high (max level for current data size and "
               "start_level is %d)." % (swt_max_level(data.size) - start_level))
        raise ValueError(msg)

    output_len = common.swt_buffer_length(data.size)
    if output_len < 1:
        raise RuntimeError("Invalid output length.")

    ret = []
    for i in range(start_level+1, end_level+1):
        data_size = data.size
        # alloc memory, decompose D
        if data_t is np.float64_t:
            cD = np.zeros(output_len, dtype=np.float64)
            with nogil:
                retval = c_wt.double_swt_d(&data[0], data_size, wavelet.w,
                                 &cD[0], output_len, i)
            if retval < 0:
                raise RuntimeError("C swt failed.")
        elif data_t is np.float32_t:
            cD = np.zeros(output_len, dtype=np.float32)
            with nogil:
                retval = c_wt.float_swt_d(&data[0], data_size, wavelet.w,
                                &cD[0], output_len, i)
            if retval < 0:
                raise RuntimeError("C swt failed.")

        # alloc memory, decompose A
        if data_t is np.float64_t:
            cA = np.zeros(output_len, dtype=np.float64)
            with nogil:
                retval = c_wt.double_swt_a(&data[0], data_size, wavelet.w,
                                 &cA[0], output_len, i)
            if retval < 0:
                raise RuntimeError("C swt failed.")
        elif data_t is np.float32_t:
            cA = np.zeros(output_len, dtype=np.float32)
            with nogil:
                retval = c_wt.float_swt_a(&data[0], data_size, wavelet.w,
                                &cA[0], output_len, i)
            if retval < 0:
                raise RuntimeError("C swt failed.")

        data = cA
        ret.append((cA, cD))

    ret.reverse()
    return ret


cpdef swt_axis(np.ndarray data, Wavelet wavelet, size_t level,
               size_t start_level, unsigned int axis=0):
    # memory-views do not support n-dimensional arrays, use np.ndarray instead
    cdef common.ArrayInfo data_info, output_info
    cdef np.ndarray cD, cA
    # Explicit input_shape necessary to prevent memory leak
    cdef size_t[::1] input_shape, output_shape
    cdef size_t end_level = start_level + level
    cdef int i, retval

    if data.size % 2:
        raise ValueError("Length of data must be even.")

    if level < 1:
        raise ValueError("Level value must be greater than zero.")
    if start_level >= common.swt_max_level(data.shape[axis]):
        raise ValueError("start_level must be less than %d." %
                         common.swt_max_level(data.shape[axis]))

    if end_level > common.swt_max_level(data.shape[axis]):
        msg = ("Level value too high (max level for current data size and "
               "start_level is %d)." % (swt_max_level(data.shape[axis]) - start_level))
        raise ValueError(msg)

    data = data.astype(_check_dtype(data), copy=False)

    input_shape = <size_t [:data.ndim]> <size_t *> data.shape
    output_shape = input_shape.copy()
    output_shape[axis] = common.swt_buffer_length(data.shape[axis])
    if output_shape[axis] != input_shape[axis]:
        raise RuntimeError("swt_axis assumes output_shape is the same as "
                           "input_shape")

    data_info.ndim = data.ndim
    data_info.strides = <pywt_index_t *> data.strides
    data_info.shape = <size_t *> data.shape

    cA = np.empty(output_shape, data.dtype)
    output_info.ndim = cA.ndim
    output_info.strides = <pywt_index_t *> cA.strides
    output_info.shape = <size_t *> cA.shape

    ret = []
    for i in range(start_level+1, end_level+1):

        if data.dtype == np.float64:
            cA = np.zeros(output_shape, dtype=np.float64)
            with nogil:
                retval = c_wt.double_downcoef_axis(
                    <double *> data.data, data_info,
                    <double *> cA.data, output_info,
                    wavelet.w, axis,
                    common.COEF_APPROX, common.MODE_PERIODIZATION,
                    i, common.SWT_TRANSFORM)
            if retval:
                raise RuntimeError("C wavelet transform failed")
            cD = np.zeros(output_shape, dtype=np.float64)
            with nogil:
                retval = c_wt.double_downcoef_axis(
                    <double *> data.data, data_info,
                    <double *> cD.data, output_info,
                    wavelet.w, axis,
                    common.COEF_DETAIL, common.MODE_PERIODIZATION,
                    i, common.SWT_TRANSFORM)
            if retval:
                raise RuntimeError("C wavelet transform failed")
        elif data.dtype == np.float32:
            cA = np.zeros(output_shape, dtype=np.float32)
            with nogil:
                retval = c_wt.float_downcoef_axis(
                    <float *> data.data, data_info,
                    <float *> cA.data, output_info,
                    wavelet.w, axis,
                    common.COEF_APPROX, common.MODE_PERIODIZATION,
                    i, common.SWT_TRANSFORM)
            if retval:
                raise RuntimeError("C wavelet transform failed")
            cD = np.zeros(output_shape, dtype=np.float32)
            with nogil:
                retval = c_wt.float_downcoef_axis(
                    <float *> data.data, data_info,
                    <float *> cD.data, output_info,
                    wavelet.w, axis,
                    common.COEF_DETAIL, common.MODE_PERIODIZATION,
                    i, common.SWT_TRANSFORM)
            if retval:
                raise RuntimeError("C wavelet transform failed")
        else:
            raise TypeError("Array must be floating point, not {}"
                            .format(data.dtype))
        ret.append((cA, cD))

        # previous approx coeffs are the data for the next level
        data = cA
        data_info = output_info

    ret.reverse()
    return ret
