cimport common, c_wt
from common cimport pywt_index_t, MODE
from ._pywt cimport _check_dtype

cimport numpy as np
import numpy as np




cpdef cwt_psi_single(data_t[::1] data, Wavelet wavelet, size_t output_len):
    cdef np.ndarray psi, psi_r, psi_i
    if output_len < 1:
        raise RuntimeError("Invalid output length.")

    #if data_t is np.float64_t:
        # TODO: Don't think these have to be 0-initialized
        # TODO: Check other methods of allocating (e.g. Cython/CPython arrays)
    if data_t is np.float64_t:
        if wavelet.short_family_name == "gaus":
            psi = np.zeros(output_len, np.float64)
            c_cwt.double_gaus(&data[0], <double *>psi.data, data.size, wavelet.family_number)
            return psi
        elif wavelet.short_family_name == "mexh":
            psi = np.zeros(output_len, np.float64)
            c_cwt.double_mexh(&data[0], <double *>psi.data, data.size)
            return psi
        elif wavelet.short_family_name == "morl":
            psi = np.zeros(output_len, np.float64)
            c_cwt.double_morl(&data[0], <double *>psi.data, data.size)
            return psi
        elif wavelet.short_family_name == "cgau":
            psi_r = np.zeros(output_len, np.float64)
            psi_i = np.zeros(output_len, np.float64)
            c_cwt.double_cgau(&data[0], <double *>psi_r.data, <double *>psi_i.data, data.size, wavelet.family_number)
            return (psi_r, psi_i)
        elif wavelet.short_family_name == "shan":
            psi_r = np.zeros(output_len, np.float64)
            psi_i = np.zeros(output_len, np.float64)
            c_cwt.double_shan(&data[0], <double *>psi_r.data, <double *>psi_i.data, data.size, wavelet.bandwidth_frequency, wavelet.center_frequency)
            return (psi_r, psi_i)
        elif wavelet.short_family_name == "fbsp":
            psi_r = np.zeros(output_len, np.float64)
            psi_i = np.zeros(output_len, np.float64)
            c_cwt.double_fbsp(&data[0], <double *>psi_r.data, <double *>psi_i.data, data.size, wavelet.fbsp_order, wavelet.bandwidth_frequency, wavelet.center_frequency)
            return (psi_r, psi_i)
        elif wavelet.short_family_name == "cmor":
            psi_r = np.zeros(output_len, np.float64)
            psi_i = np.zeros(output_len, np.float64)
            c_cwt.double_cmor(&data[0], <double *>psi_r.data, <double *>psi_i.data, data.size, wavelet.bandwidth_frequency, wavelet.center_frequency)
            return (psi_r, psi_i)
            
    elif data_t is np.float32_t:
        if wavelet.short_family_name == "gaus":
            psi = np.zeros(output_len, np.float32)
            c_cwt.float_gaus(&data[0], <float *>psi.data, data.size, wavelet.family_number)
            return psi
        elif wavelet.short_family_name == "mexh":
            psi = np.zeros(output_len, np.float32)
            c_cwt.float_mexh(&data[0], <float *>psi.data, data.size)
            return psi
        elif wavelet.short_family_name == "morl":
            psi = np.zeros(output_len, np.float32)
            c_cwt.float_morl(&data[0], <float *>psi.data, data.size)
            return psi
        elif wavelet.short_family_name == "cgau":
            psi_r = np.zeros(output_len, np.float32)
            psi_i = np.zeros(output_len, np.float32)
            c_cwt.float_cgau(&data[0], <float *>psi_r.data, <float *>psi_i.data, data.size, wavelet.family_number)
            return (psi_r, psi_i)
        elif wavelet.short_family_name == "shan":
            psi_r = np.zeros(output_len, np.float32)
            psi_i = np.zeros(output_len, np.float32)
            c_cwt.float_shan(&data[0], <float *>psi_r.data, <float *>psi_i.data, data.size, wavelet.bandwidth_frequency, wavelet.center_frequency)
            return (psi_r, psi_i)
        elif wavelet.short_family_name == "fbsp":
            psi_r = np.zeros(output_len, np.float32)
            psi_i = np.zeros(output_len, np.float32)
            c_cwt.float_fbsp(&data[0], <float *>psi_r.data, <float *>psi_i.data, data.size, wavelet.fbsp_order, wavelet.bandwidth_frequency, wavelet.center_frequency)
            return (psi_r, psi_i)
        elif wavelet.short_family_name == "cmor":
            psi_r = np.zeros(output_len, np.float32)
            psi_i = np.zeros(output_len, np.float32)
            c_cwt.float_cmor(&data[0], <float *>psi_r.data, <float *>psi_i.data, data.size, wavelet.bandwidth_frequency, wavelet.center_frequency)
            return (psi_r, psi_i)

