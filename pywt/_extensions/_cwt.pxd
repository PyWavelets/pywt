from ._pywt cimport ContinuousWavelet, data_t
cimport numpy as np
import numpy as np

cpdef cwt_psi_single(data_t[::1] data, ContinuousWavelet wavelet, size_t output_len)

