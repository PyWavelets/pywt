from ._pywt cimport Wavelet, data_t
cimport numpy as np
import numpy as np

cpdef cwt_psi_single(data_t[::1] data, Wavelet wavelet, size_t output_len)
cpdef cwt_wkeep_1D_center64(np.ndarray data, size_t output_len)
cpdef cwt_wkeep_1D_center32(np.ndarray data, size_t output_len)
cpdef cwt_conv_real(data_t[::1] data, np.ndarray  psi, size_t output_len)
cpdef cwt_conv(data_t[::1] data, np.ndarray in_filter, size_t output_len)
