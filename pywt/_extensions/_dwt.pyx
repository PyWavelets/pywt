cimport common, c_wt
from common cimport index_t, MODE
from ._pywt cimport _check_dtype

cimport numpy as np
import numpy as np


cpdef dwt_max_level(size_t data_len, size_t filter_len):
    return common.dwt_max_level(data_len, filter_len)


cpdef dwt_coeff_len(size_t data_len, size_t filter_len, MODE mode):
    if data_len < 1:
        raise ValueError("Value of data_len must be greater than zero.")
    if filter_len < 1:
        raise ValueError("Value of filter_len must be greater than zero.")

    return common.dwt_buffer_length(data_len, filter_len, mode)


cpdef dwt_single(data_t[::1] data, Wavelet wavelet, MODE mode):
    cdef size_t output_len = dwt_coeff_len(data.size, wavelet.dec_len, mode)
    cdef np.ndarray cA, cD
    if output_len < 1:
        raise RuntimeError("Invalid output length.")

    if data_t is np.float64_t:
        # TODO: Don't think these have to be 0-initialized
        # TODO: Check other methods of allocating (e.g. Cython/CPython arrays)
        cA = np.zeros(output_len, np.float64)
        cD = np.zeros(output_len, np.float64)

        if (c_wt.double_dec_a(&data[0], data.size, wavelet.w,
                              <double *>cA.data, cA.size, mode) < 0
            or
            c_wt.double_dec_d(&data[0], data.size, wavelet.w,
                              <double *>cD.data, cD.size,
                              mode) < 0):
            raise RuntimeError("C dwt failed.")
    elif data_t is np.float32_t:
        cA = np.zeros(output_len, np.float32)
        cD = np.zeros(output_len, np.float32)

        if (c_wt.float_dec_a(&data[0], data.size, wavelet.w,
                             <float *>cA.data, cA.size, mode) < 0
            or
            c_wt.float_dec_d(&data[0], data.size, wavelet.w,
                             <float *>cD.data, cD.size, mode) < 0):
            raise RuntimeError("C dwt failed.")

    return (cA, cD)


cpdef dwt_axis(np.ndarray data, Wavelet wavelet, MODE mode, unsigned int axis=0):
    # memory-views do not support n-dimensional arrays, use np.ndarray instead
    cdef common.ArrayInfo data_info, output_info
    cdef np.ndarray cD, cA
    cdef size_t[::1] output_shape

    data = data.astype(_check_dtype(data), copy=False)

    output_shape = (<size_t [:data.ndim]> <size_t *> data.shape).copy()
    output_shape[axis] = common.dwt_buffer_length(data.shape[axis], wavelet.dec_len, mode)

    cA = np.empty(output_shape, data.dtype)
    cD = np.empty(output_shape, data.dtype)

    data_info.ndim = data.ndim
    data_info.strides = <index_t *> data.strides
    data_info.shape = <size_t *> data.shape

    output_info.ndim = cA.ndim
    output_info.strides = <index_t *> cA.strides
    output_info.shape = <size_t *> cA.shape

    if data.dtype == np.float64:
        if c_wt.double_downcoef_axis(<double *> data.data, data_info,
                                     <double *> cA.data, output_info,
                                     wavelet.w, axis, common.COEF_APPROX, mode):
            raise RuntimeError("C wavelet transform failed")
        if c_wt.double_downcoef_axis(<double *> data.data, data_info,
                                     <double *> cD.data, output_info,
                                     wavelet.w, axis, common.COEF_DETAIL, mode):
            raise RuntimeError("C wavelet transform failed")
    elif data.dtype == np.float32:
        if c_wt.float_downcoef_axis(<float *> data.data, data_info,
                                    <float *> cA.data, output_info,
                                    wavelet.w, axis, common.COEF_APPROX, mode):
            raise RuntimeError("C wavelet transform failed")
        if c_wt.float_downcoef_axis(<float *> data.data, data_info,
                                    <float *> cD.data, output_info,
                                    wavelet.w, axis, common.COEF_DETAIL, mode):
            raise RuntimeError("C wavelet transform failed")
    else:
        raise TypeError("Array must be floating point, not {}"
                        .format(data.dtype))
    return (cA, cD)


cpdef idwt_single(np.ndarray cA, np.ndarray cD, Wavelet wavelet, MODE mode):
    cdef size_t input_len, rec_len
    cdef np.ndarray rec

    # check for size difference between arrays
    if cA.size != cD.size:
        raise ValueError("Coefficients arrays must have the same size.")
    else:
        input_len = cA.size

    if cA.dtype != cD.dtype:
        raise ValueError("Coefficients arrays must have the same dtype.")

    # find reconstruction buffer length
    rec_len = common.idwt_buffer_length(input_len, wavelet.rec_len, mode)
    if rec_len < 1:
        msg = ("Invalid coefficient arrays length for specified wavelet. "
               "Wavelet and mode must be the same as used for decomposition.")
        raise ValueError(msg)

        # call idwt func.  one of cA/cD can be None, then only
    # reconstruction of non-null part will be performed
    if cA.dtype == np.float64:
        rec = np.zeros(rec_len, dtype=np.float64)
        if c_wt.double_idwt(<double *>cA.data, cA.size,
                            <double *>cD.data, cD.size,
                            <double *>rec.data, rec.size,
                            wavelet.w, mode) < 0:
            raise RuntimeError("C idwt failed.")
    elif cA.dtype == np.float32:
        rec = np.zeros(rec_len, dtype=np.float32)
        if c_wt.float_idwt(<float *>cA.data, cA.size,
                           <float *>cD.data, cD.size,
                           <float *>rec.data, rec.size,
                           wavelet.w, mode) < 0:
            raise RuntimeError("C idwt failed.")

    return rec


cpdef idwt_axis(np.ndarray coefs_a, np.ndarray coefs_d,
                Wavelet wavelet, MODE mode, unsigned int axis=0):
    cdef common.ArrayInfo a_info, d_info, output_info
    cdef np.ndarray output
    cdef np.dtype output_dtype
    cdef size_t[::1] output_shape

    if coefs_a is not None:
        if coefs_d is not None and coefs_d.dtype.itemsize > coefs_a.dtype.itemsize:
            coefs_a = coefs_a.astype(_check_dtype(coefs_d), copy=False)
        else:
            coefs_a = coefs_a.astype(_check_dtype(coefs_a), copy=False)
        a_info.ndim = coefs_a.ndim
        a_info.strides = <index_t *> coefs_a.strides
        a_info.shape = <size_t *> coefs_a.shape
    if coefs_d is not None:
        if coefs_a is not None and coefs_a.dtype.itemsize > coefs_d.dtype.itemsize:
            coefs_d = coefs_d.astype(_check_dtype(coefs_a), copy=False)
        else:
            coefs_d = coefs_d.astype(_check_dtype(coefs_d), copy=False)
        d_info.ndim = coefs_d.ndim
        d_info.strides = <index_t *> coefs_d.strides
        d_info.shape = <size_t *> coefs_d.shape

    if coefs_a is not None:
        output_shape = (<size_t [:coefs_a.ndim]> <size_t *> coefs_a.shape).copy()
        output_shape[axis] = common.idwt_buffer_length(coefs_a.shape[axis],
                                                       wavelet.rec_len, mode)
        output_dtype = coefs_a.dtype
    elif coefs_d is not None:
        output_shape = (<size_t [:coefs_d.ndim]> <size_t *> coefs_d.shape).copy()
        output_shape[axis] = common.idwt_buffer_length(coefs_d.shape[axis],
                                                       wavelet.rec_len, mode)
        output_dtype = coefs_d.dtype
    else:
        return None;

    output = np.empty(output_shape, output_dtype)

    output_info.ndim = output.ndim
    output_info.strides = <index_t *> output.strides
    output_info.shape = <size_t *> output.shape

    if output.dtype == np.float64:
        if c_wt.double_idwt_axis(<double *> coefs_a.data if coefs_a is not None else NULL,
                                 &a_info if coefs_a is not None else NULL,
                                 <double *> coefs_d.data if coefs_d is not None else NULL,
                                 &d_info if coefs_d is not None else NULL,
                                 <double *> output.data, output_info,
                                 wavelet.w, axis, mode):
            raise RuntimeError("C inverse wavelet transform failed")
    elif output.dtype == np.float32:
        if c_wt.float_idwt_axis(<float *> coefs_a.data if coefs_a is not None else NULL,
                                &a_info if coefs_a is not None else NULL,
                                <float *> coefs_d.data if coefs_d is not None else NULL,
                                &d_info if coefs_d is not None else NULL,
                                <float *> output.data, output_info,
                                wavelet.w, axis, mode):
            raise RuntimeError("C inverse wavelet transform failed")
    else:
        raise TypeError("Array must be floating point, not {}"
                        .format(output.dtype))

    return output


cpdef upcoef(bint do_rec_a, data_t[::1] coeffs, Wavelet wavelet, int level, int take):
    cdef data_t[::1] rec
    cdef int i
    cdef size_t rec_len, left_bound, right_bound

    rec_len = 0

    if level < 1:
        raise ValueError("Value of level must be greater than 0.")

    for i in range(level):
        # output len
        rec_len = common.reconstruction_buffer_length(coeffs.size, wavelet.dec_len)
        if rec_len < 1:
            raise RuntimeError("Invalid output length.")

        # To mirror multi-level wavelet reconstruction behaviour, when detail
        # reconstruction is requested, the dec_d variant is only called at the
        # first level to generate the approximation coefficients at the second
        # level.  Subsequent levels apply the reconstruction filter.
        if data_t is np.float64_t:
            rec = np.zeros(rec_len, dtype=np.float64)
            if do_rec_a or i > 0:
                if c_wt.double_rec_a(&coeffs[0], coeffs.size, wavelet.w,
                                     &rec[0], rec.size) < 0:
                    raise RuntimeError("C rec_a failed.")
            else:
                if c_wt.double_rec_d(&coeffs[0], coeffs.size, wavelet.w,
                                     &rec[0], rec.size) < 0:
                    raise RuntimeError("C rec_d failed.")
        elif data_t is np.float32_t:
            rec = np.zeros(rec_len, dtype=np.float32)
            if do_rec_a or i > 0:
                if c_wt.float_rec_a(&coeffs[0], coeffs.size, wavelet.w,
                                    &rec[0], rec.size) < 0:
                    raise RuntimeError("C rec_a failed.")
            else:
                if c_wt.float_rec_d(&coeffs[0], coeffs.size, wavelet.w,
                                    &rec[0], rec.size) < 0:
                    raise RuntimeError("C rec_d failed.")
        # TODO: this algorithm needs some explaining
        coeffs = rec

    if take > 0 and take < rec_len:
        left_bound = right_bound = (rec_len-take) // 2
        if (rec_len-take) % 2:
            # right_bound must never be zero for indexing to work
            right_bound = right_bound + 1

        return rec[left_bound:-right_bound]

    return rec


cpdef downcoef(bint do_dec_a, data_t[::1] data, Wavelet wavelet, MODE mode, int level):
    cdef data_t[::1] coeffs
    cdef int i
    cdef size_t output_len

    if level < 1:
        raise ValueError("Value of level must be greater than 0.")

    for i in range(level):
        output_len = common.dwt_buffer_length(data.size, wavelet.dec_len, mode)
        if output_len < 1:
            raise RuntimeError("Invalid output length.")

        # To mirror multi-level wavelet decomposition behaviour, when detail
        # coefficients are requested, the dec_d variant is only called at the
        # final level.  All prior levels use dec_a.  In other words, the detail
        # coefficients at level n are those produced via the operation of the
        # detail filter on the approximation coefficients of level n-1.
        if data_t is np.float64_t:
            coeffs = np.zeros(output_len, dtype=np.float64)
            if do_dec_a or (i < level - 1):
                if c_wt.double_dec_a(&data[0], data.size, wavelet.w,
                                     &coeffs[0], coeffs.size, mode) < 0:
                    raise RuntimeError("C dec_a failed.")
            else:
                if c_wt.double_dec_d(&data[0], data.size, wavelet.w,
                                     &coeffs[0], coeffs.size, mode) < 0:
                    raise RuntimeError("C dec_d failed.")
        elif data_t is np.float32_t:
            coeffs = np.zeros(output_len, dtype=np.float32)
            if do_dec_a or (i < level - 1):
                if c_wt.float_dec_a(&data[0], data.size, wavelet.w,
                                    &coeffs[0], coeffs.size, mode) < 0:
                    raise RuntimeError("C dec_a failed.")
            else:
                if c_wt.float_dec_d(&data[0], data.size, wavelet.w,
                                    &coeffs[0], coeffs.size, mode) < 0:
                    raise RuntimeError("C dec_d failed.")
        data = coeffs

    return coeffs
