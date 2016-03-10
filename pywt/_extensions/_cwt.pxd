from ._pywt cimport Wavelet, data_t

cpdef cwt_psi_single(data_t[::1] data, Wavelet wavelet, size_t output_len)
cpdef cwt_conv_real(data_t[::1] data, data_t[::1]  psi, size_t output_len)
cpdef cwt_conv(data_t[::1] data, data_t[::1] in_filter, size_t output_len)