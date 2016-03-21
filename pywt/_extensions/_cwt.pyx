cimport common, c_cwt
from common cimport index_t, MODE
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
            c_cwt.double_gaus(&data[0], <double *>psi.data, data.size, wavelet.number)
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
            c_cwt.double_cgau(&data[0], <double *>psi_r.data, <double *>psi_i.data, data.size, wavelet.number)
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
            c_cwt.float_gaus(&data[0], <float *>psi.data, data.size, wavelet.number)
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
            c_cwt.float_cgau(&data[0], <float *>psi_r.data, <float *>psi_i.data, data.size, wavelet.number)
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


cpdef cwt_conv(data_t[::1] data, np.ndarray in_filter, size_t output_len):
    cdef size_t N, F, O
    cdef np.ndarray output, pBuf
    cdef size_t i, j
    N = data.size
    F = in_filter.size
    O = output_len
    if data_t is np.float64_t:
        output = np.zeros(O, dtype=np.float64)
        pBuf = np.zeros(N + 2 *(F-1), dtype=np.float64)
        for i in np.arange(F-1):
            pBuf[i] = 0
            pBuf[i + N +F -1] = 0
        for i in np.arange(N):
            pBuf[i+F-1] = data[i]
        for i in np.arange(O):
            output[i] = 0
            for j in np.arange(F-1,-1,-1):
                output[i] += in_filter[j] * pBuf[i+F-j-1]
        return output
    else:
        output = np.zeros(O, dtype=np.float32)
        pBuf = np.zeros(N + 2 *(F-1), dtype=np.float32)
        for i in np.arange(F-1):
            pBuf[i] = 0
            pBuf[i + N +F -1] = 0
        for i in np.arange(N):
            pBuf[i+F-1] = data[i]
        for i in np.arange(O):
            output[i] = 0
            for j in np.arange(F-1,-1,-1):
                output[i] += in_filter[j] * pBuf[i+F-j-1]
        return output

cpdef cwt_conv_real(data_t[::1] data, np.ndarray  psi, size_t output_len):
    cdef size_t N, F, O, buf_len
    cdef np.ndarray output, buf, fTemp
    cdef size_t i, j
    N = data.size
    F = psi.size
    O = output_len
    if data_t is np.float64_t:
        output = np.zeros(O, dtype=np.float64)
        buf_len = N+F-1
        buf = np.zeros(buf_len, dtype=np.float64)
        fTemp = np.zeros_like(psi, dtype=np.float64)
        for i in np.arange(F):
            fTemp[i] = psi[F-i-1]
        buf = cwt_conv(data,fTemp,buf_len)
        for i in np.arange(O):
            output[i] = buf[(buf_len - O)/2 +i]
        return output
    else:
        output = np.zeros(O, dtype=np.float32)
        buf_len = N+F-1
        buf = np.zeros(buf_len, dtype=np.float32)
        fTemp = np.zeros_like(psi, dtype=np.float32)
        for i in np.arange(F):
            fTemp[i] = psi[F-i-1]
        buf = cwt_conv(data,fTemp,buf_len)
        for i in np.arange(O):
            output[i] = buf[(buf_len - O)/2 +i]
        return output