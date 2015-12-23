cimport common
cimport c_wt

import numpy as np
cimport numpy as np

from ._pywt cimport c_wavelet_from_object, data_t, Wavelet

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


def swt(np.ndarray[data_t, ndim=1, mode="c"] data, object wavelet,
        object level=None, int start_level=0):
    """See `swt` for details."""
    cdef np.ndarray[data_t, ndim=1, mode="c"] cA, cD
    cdef Wavelet w
    cdef int i, end_level, level_

    if data.size % 2:
        raise ValueError("Length of data must be even.")

    w = c_wavelet_from_object(wavelet)

    if level is None:
        level_ = common.swt_max_level(data.size)
    else:
        level_ = level

    end_level = start_level + level_

    if level_ < 1:
        raise ValueError("Level value must be greater than zero.")
    if start_level < 0:
        raise ValueError("start_level must be greater than zero.")
    if start_level >= common.swt_max_level(data.size):
        raise ValueError("start_level must be less than %d." %
                         common.swt_max_level(data.size))

    if end_level > common.swt_max_level(data.size):
        msg = ("Level value too high (max level for current data size and "
               "start_level is %d)." % (common.swt_max_level(data.size) -
                                        start_level))
        raise ValueError(msg)

    # output length
    output_len = common.swt_buffer_length(data.size)
    if output_len < 1:
        raise RuntimeError("Invalid output length.")

    ret = []
    for i in range(start_level+1, end_level+1):
        # alloc memory, decompose D
        cD = np.zeros(output_len, dtype=data.dtype)

        if data_t is np.float64_t:
            if c_wt.double_swt_d(&data[0], data.size, w.w,
                                 &cD[0], cD.size, i) < 0:
                raise RuntimeError("C swt failed.")
        elif data_t is np.float32_t:
            if c_wt.float_swt_d(&data[0], data.size, w.w,
                                &cD[0], cD.size, i) < 0:
                raise RuntimeError("C swt failed.")
        else:
            raise RuntimeError("Invalid data type.")

        # alloc memory, decompose A
        cA = np.zeros(output_len, dtype=data.dtype)

        if data_t is np.float64_t:
            if c_wt.double_swt_a(&data[0], data.size, w.w,
                                 &cA[0], cA.size, i) < 0:
                raise RuntimeError("C swt failed.")
        elif data_t is np.float32_t:
            if c_wt.float_swt_a(&data[0], data.size, w.w,
                                &cA[0], cA.size, i) < 0:
                raise RuntimeError("C swt failed.")
        else:
            raise RuntimeError("Invalid data type.")

        data = cA
        ret.append((cA, cD))

    ret.reverse()
    return ret
