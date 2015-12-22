def dwt_max_level(data_len, filter_len):
    """
    dwt_max_level(data_len, filter_len)

    Compute the maximum useful level of decomposition.

    Parameters
    ----------
    data_len : int
        Input data length.
    filter_len : int
        Wavelet filter length.

    Returns
    -------
    max_level : int
        Maximum level.

    Examples
    --------
    >>> import pywt
    >>> w = pywt.Wavelet('sym5')
    >>> pywt.dwt_max_level(data_len=1000, filter_len=w.dec_len)
    6
    >>> pywt.dwt_max_level(1000, w)
    6
    """
    if isinstance(filter_len, Wavelet):
        return common.dwt_max_level(data_len, filter_len.dec_len)
    else:
        return common.dwt_max_level(data_len, filter_len)


def dwt_coeff_len(data_len, filter_len, mode='symmetric'):
    """
    dwt_coeff_len(data_len, filter_len, mode='symmetric')

    Returns length of dwt output for given data length, filter length and mode

    Parameters
    ----------
    data_len : int
        Data length.
    filter_len : int
        Filter length.
    mode : str, optional (default: 'symmetric')
        Signal extension mode, see Modes

    Returns
    -------
    len : int
        Length of dwt output.

    Notes
    -----
    For all modes except periodization::

        len(cA) == len(cD) == floor((len(data) + wavelet.dec_len - 1) / 2)

    for periodization mode ("per")::

        len(cA) == len(cD) == ceil(len(data) / 2)

    """
    cdef index_t filter_len_

    if isinstance(filter_len, Wavelet):
        filter_len_ = filter_len.dec_len
    else:
        filter_len_ = filter_len

    if data_len < 1:
        raise ValueError("Value of data_len value must be greater than zero.")
    if filter_len_ < 1:
        raise ValueError("Value of filter_len must be greater than zero.")

    return common.dwt_buffer_length(data_len, filter_len_, _try_mode(mode))


def dwt_single(np.ndarray[data_t, ndim=1] data, object wavelet,
                                                object mode='symmetric'):
    cdef np.ndarray[data_t, ndim=1, mode="c"] cA, cD
    cdef Wavelet w = c_wavelet_from_object(wavelet)
    cdef common.MODE mode_ = _try_mode(mode)

    cdef size_t output_len

    data = data.astype(_check_dtype(data), copy=True)

    output_len = common.dwt_buffer_length(data.size, w.dec_len, mode_)
    if output_len < 1:
        raise RuntimeError("Invalid output length.")

    cA = np.zeros(output_len, data.dtype)
    cD = np.zeros(output_len, data.dtype)

    if data_t == np.float64_t:
        if (c_wt.double_dec_a(&data[0], data.size, w.w,
                              &cA[0], cA.size, mode_) < 0
            or
            c_wt.double_dec_d(&data[0], data.size, w.w,
                              &cD[0], cD.size, mode_) < 0):
            raise RuntimeError("C dwt failed.")
    elif data_t == np.float32_t:
        if (c_wt.float_dec_a(&data[0], data.size, w.w,
                             &cA[0], cA.size, mode_) < 0
            or
            c_wt.float_dec_d(&data[0], data.size, w.w,
                             &cD[0], cD.size, mode_) < 0):
            raise RuntimeError("C dwt failed.")
    else:
        raise RuntimeError("Invalid data type.")

    return (cA, cD)


cpdef dwt_axis(np.ndarray data, object wavelet, object mode='symmetric', unsigned int axis=0):
    cdef Wavelet w = c_wavelet_from_object(wavelet)
    cdef common.MODE _mode = _try_mode(mode)
    cdef common.ArrayInfo data_info, output_info
    cdef np.ndarray cD, cA
    cdef size_t[::1] output_shape

    data = data.astype(_check_dtype(data), copy=False)

    output_shape = (<size_t [:data.ndim]> <size_t *> data.shape).copy()
    output_shape[axis] = common.dwt_buffer_length(data.shape[axis], w.dec_len, _mode)

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
                                     w.w, axis, common.COEF_APPROX, _mode):
            raise RuntimeError("C wavelet transform failed")
        if c_wt.double_downcoef_axis(<double *> data.data, data_info,
                                     <double *> cD.data, output_info,
                                     w.w, axis, common.COEF_DETAIL, _mode):
            raise RuntimeError("C wavelet transform failed")
    elif data.dtype == np.float32:
        if c_wt.float_downcoef_axis(<float *> data.data, data_info,
                                    <float *> cA.data, output_info,
                                    w.w, axis, common.COEF_APPROX, _mode):
            raise RuntimeError("C wavelet transform failed")
        if c_wt.float_downcoef_axis(<float *> data.data, data_info,
                                    <float *> cD.data, output_info,
                                    w.w, axis, common.COEF_DETAIL, _mode):
            raise RuntimeError("C wavelet transform failed")
    else:
        raise TypeError("Array must be floating point, not {}"
                        .format(data.dtype))
    return (cA, cD)


def idwt_single(np.ndarray[data_t, ndim=1, mode="c"] cA,
                np.ndarray[data_t, ndim=1, mode="c"] cD,
                object wavelet, object mode='symmetric'):

    cdef Wavelet w = c_wavelet_from_object(wavelet)
    cdef common.MODE mode_ = _try_mode(mode)

    cdef np.ndarray[data_t, ndim=1, mode="c"] rec
    cdef index_t input_len
    cdef index_t rec_len

    # check for size difference between arrays
    if cA.size != cD.size:
        raise ValueError("Coefficients arrays must have the same size.")
    else:
        input_len = cA.size

    # find reconstruction buffer length
    rec_len = common.idwt_buffer_length(input_len, w.rec_len, mode_)
    if rec_len < 1:
        msg = ("Invalid coefficient arrays length for specified wavelet. "
               "Wavelet and mode must be the same as used for decomposition.")
        raise ValueError(msg)

    # allocate buffer
    if cA is not None:
        rec = np.zeros(rec_len, dtype=cA.dtype)
    else:
        rec = np.zeros(rec_len, dtype=cD.dtype)

    # call idwt func.  one of cA/cD can be None, then only
    # reconstruction of non-null part will be performed
    if data_t is np.float64_t:
        if c_wt.double_idwt(&cA[0], cA.size,
                            &cD[0], cD.size,
                            &rec[0], rec.size,
                            w.w, mode_) < 0:
            raise RuntimeError("C idwt failed.")
    elif data_t == np.float32_t:
        if c_wt.float_idwt(&cA[0], cA.size,
                           &cD[0], cD.size,
                           &rec[0], rec.size,
                           w.w, mode_) < 0:
            raise RuntimeError("C idwt failed.")
    else:
        raise RuntimeError("Invalid data type.")

    return rec


cpdef idwt_axis(np.ndarray coefs_a, np.ndarray coefs_d, object wavelet,
                object mode='symmetric', unsigned int axis=0):
    cdef Wavelet w = c_wavelet_from_object(wavelet)
    cdef common.ArrayInfo a_info, d_info, output_info
    cdef np.ndarray output
    cdef np.dtype output_dtype
    cdef size_t[::1] output_shape
    cdef common.MODE _mode = _try_mode(mode)

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
                                                       w.rec_len, _mode)
        output_dtype = coefs_a.dtype
    elif coefs_d is not None:
        output_shape = (<size_t [:coefs_d.ndim]> <size_t *> coefs_d.shape).copy()
        output_shape[axis] = common.idwt_buffer_length(coefs_d.shape[axis],
                                                       w.rec_len, _mode)
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
                                 w.w, axis, _mode):
            raise RuntimeError("C inverse wavelet transform failed")
    elif output.dtype == np.float32:
        if c_wt.float_idwt_axis(<float *> coefs_a.data if coefs_a is not None else NULL,
                                &a_info if coefs_a is not None else NULL,
                                <float *> coefs_d.data if coefs_d is not None else NULL,
                                &d_info if coefs_d is not None else NULL,
                                <float *> output.data, output_info,
                                w.w, axis, _mode):
            raise RuntimeError("C inverse wavelet transform failed")
    else:
        raise TypeError("Array must be floating point, not {}"
                        .format(output.dtype))

    return output


def _upcoef(part, np.ndarray[data_t, ndim=1, mode="c"] coeffs, wavelet,
            int level=1, int take=0):
    cdef Wavelet w
    cdef np.ndarray[data_t, ndim=1, mode="c"] rec
    cdef int i, do_rec_a
    cdef index_t rec_len, left_bound, right_bound

    rec_len = 0

    if part not in ('a', 'd'):
        raise ValueError("Argument 1 must be 'a' or 'd', not '%s'." % part)
    do_rec_a = (part == 'a')

    w = c_wavelet_from_object(wavelet)

    if level < 1:
        raise ValueError("Value of level must be greater than 0.")

    for i in range(level):
        # output len
        rec_len = common.reconstruction_buffer_length(coeffs.size, w.dec_len)
        if rec_len < 1:
            raise RuntimeError("Invalid output length.")

        # reconstruct
        rec = np.zeros(rec_len, dtype=coeffs.dtype)

        # To mirror multi-level wavelet reconstruction behaviour, when detail
        # reconstruction is requested, the dec_d variant is only called at the
        # first level to generate the approximation coefficients at the second
        # level.  Subsequent levels apply the reconstruction filter.
        if do_rec_a:
            if data_t is np.float64_t:
                if c_wt.double_rec_a(&coeffs[0], coeffs.size, w.w,
                                     &rec[0], rec.size) < 0:
                    raise RuntimeError("C rec_a failed.")
            elif data_t is np.float32_t:
                if c_wt.float_rec_a(&coeffs[0], coeffs.size, w.w,
                                    &rec[0], rec.size) < 0:
                    raise RuntimeError("C rec_a failed.")
            else:
                raise RuntimeError("Invalid data type.")
        else:
            if data_t is np.float64_t:
                if c_wt.double_rec_d(&coeffs[0], coeffs.size, w.w,
                                     &rec[0], rec.size) < 0:
                    raise RuntimeError("C rec_d failed.")
            elif data_t is np.float32_t:
                if c_wt.float_rec_d(&coeffs[0], coeffs.size, w.w,
                                    &rec[0], rec.size) < 0:
                    raise RuntimeError("C rec_d failed.")
            else:
                raise RuntimeError("Invalid data type.")
            # switch to approximation filter for subsequent levels
            do_rec_a = 1

        # TODO: this algorithm needs some explaining
        coeffs = rec

    if take > 0 and take < rec_len:
        left_bound = right_bound = (rec_len-take) // 2
        if (rec_len-take) % 2:
            # right_bound must never be zero for indexing to work
            right_bound = right_bound + 1

        return rec[left_bound:-right_bound]

    return rec


def _downcoef(part, np.ndarray[data_t, ndim=1, mode="c"] data,
              object wavelet, object mode='symmetric', int level=1):
    cdef np.ndarray[data_t, ndim=1, mode="c"] coeffs
    cdef int i, do_dec_a
    cdef index_t dec_len
    cdef Wavelet w
    cdef common.MODE mode_

    w = c_wavelet_from_object(wavelet)
    mode_ = _try_mode(mode)

    if part not in ('a', 'd'):
        raise ValueError("Argument 1 must be 'a' or 'd', not '%s'." % part)
    do_dec_a = (part == 'a')

    if level < 1:
        raise ValueError("Value of level must be greater than 0.")

    for i in range(level):
        output_len = common.dwt_buffer_length(data.size, w.dec_len, mode_)
        if output_len < 1:
            raise RuntimeError("Invalid output length.")
        coeffs = np.zeros(output_len, dtype=data.dtype)

        # To mirror multi-level wavelet decomposition behaviour, when detail
        # coefficients are requested, the dec_d variant is only called at the
        # final level.  All prior levels use dec_a.  In other words, the detail
        # coefficients at level n are those produced via the operation of the
        # detail filter on the approximation coefficients of level n-1.
        if do_dec_a or (i < level - 1):
            if data_t is np.float64_t:
                if c_wt.double_dec_a(&data[0], data.size, w.w,
                                     &coeffs[0], coeffs.size, mode_) < 0:
                    raise RuntimeError("C dec_a failed.")
            elif data_t is np.float32_t:
                if c_wt.float_dec_a(&data[0], data.size, w.w,
                                    &coeffs[0], coeffs.size, mode_) < 0:
                    raise RuntimeError("C dec_a failed.")
            else:
                raise RuntimeError("Invalid data type.")
        else:
            if data_t is np.float64_t:
                if c_wt.double_dec_d(&data[0], data.size, w.w,
                                     &coeffs[0], coeffs.size, mode_) < 0:
                    raise RuntimeError("C dec_d failed.")
            elif data_t is np.float32_t:
                if c_wt.float_dec_d(&data[0], data.size, w.w,
                                    &coeffs[0], coeffs.size, mode_) < 0:
                    raise RuntimeError("C dec_d failed.")
            else:
                raise RuntimeError("Invalid data type.")
        data = coeffs

    return coeffs
