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


def swt(data_t[::1] data, Wavelet wavelet, size_t level, size_t start_level):
    cdef data_t[::1] cA, cD
    cdef Wavelet w
    cdef int i
    cdef size_t end_level = start_level + level

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
        # alloc memory, decompose D
        if data_t is np.float64_t:
            cD = np.zeros(output_len, dtype=np.float64)
            if c_wt.double_swt_d(&data[0], data.size, wavelet.w,
                                 &cD[0], cD.size, i) < 0:
                raise RuntimeError("C swt failed.")
        elif data_t is np.float32_t:
            cD = np.zeros(output_len, dtype=np.float32)
            if c_wt.float_swt_d(&data[0], data.size, wavelet.w,
                                &cD[0], cD.size, i) < 0:
                raise RuntimeError("C swt failed.")

        # alloc memory, decompose A
        if data_t is np.float64_t:
            cA = np.zeros(output_len, dtype=np.float64)
            if c_wt.double_swt_a(&data[0], data.size, wavelet.w,
                                 &cA[0], cA.size, i) < 0:
                raise RuntimeError("C swt failed.")
        elif data_t is np.float32_t:
            cA = np.zeros(output_len, dtype=np.float32)
            if c_wt.float_swt_a(&data[0], data.size, wavelet.w,
                                &cA[0], cA.size, i) < 0:
                raise RuntimeError("C swt failed.")

        data = cA
        ret.append((cA, cD))

    ret.reverse()
    return ret
