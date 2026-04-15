# flake8: noqa

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# Copyright (c) 2012-     The PyWavelets Developers
#                         <https://github.com/PyWavelets/pywt>
# See LICENSE for more details.

"""
Discrete forward and inverse wavelet transform, stationary wavelet transform,
wavelet packets signal decomposition and reconstruction module.
"""

from ._extensions._pywt import Modes, ContinuousWavelet, families, Wavelet, wavelist, DiscreteContinuousWavelet
from ._functions import integrate_wavelet, central_frequency, scale2frequency, frequency2scale, qmf, orthogonal_filter_bank, intwave, centrfrq, scal2frq, orthfilt
from ._multilevel import wavedec, waverec, wavedec2, waverec2, wavedecn, waverecn, coeffs_to_array, array_to_coeffs, ravel_coeffs, unravel_coeffs, dwtn_max_level, wavedecn_size, wavedecn_shapes, fswavedecn, fswaverecn, FswavedecnResult
from ._multidim import dwt2, idwt2, dwtn, idwtn
from ._thresholding import threshold, threshold_firm
from ._wavelet_packets import BaseNode, Node, WaveletPacket, Node2D, WaveletPacket2D, NodeND, WaveletPacketND
from ._dwt import dwt, idwt, downcoef, upcoef, dwt_max_level, dwt_coeff_len, pad
from ._swt import swt, swt_max_level, iswt, swt2, iswt2, swtn, iswtn
from ._cwt import cwt
from ._mra import mra, mra2, mran, imra, imra2, imran
from .data import aero, ascent, camera, ecg, nino, demo_signal

__all__ = ["ContinuousWavelet", "families", "Modes", "Wavelet", "wavelist",
           "DiscreteContinuousWavelet", "integrate_wavelet",
           "central_frequency", "scale2frequency", "frequency2scale", "qmf",
           "orthogonal_filter_bank", "intwave", "centrfrq", "scal2frq",
           "orthfilt", "wavedec", "waverec", "wavedec2", "waverec2",
           "wavedecn", "waverecn", "coeffs_to_array", "array_to_coeffs",
           "ravel_coeffs", "unravel_coeffs", "dwtn_max_level",
           "wavedecn_size", "wavedecn_shapes", "fswavedecn", "fswaverecn",
           "FswavedecnResult", "dwt2", "idwt2", "dwtn", "idwtn", "threshold",
           "threshold_firm", "BaseNode", "Node", "WaveletPacket", "Node2D",
           "WaveletPacket2D", "NodeND", "WaveletPacketND", "dwt", "idwt",
           "downcoef", "upcoef", "dwt_max_level", "dwt_coeff_len", "pad",
           "swt", "swt_max_level", "iswt", "swt2", "iswt2", "swtn", "iswtn",
           "cwt", "mra", "mra2", "mran", "imra", "imra2", "imran", "aero",
           "ascent", "camera", "ecg", "nino", "demo_signal"]

from pywt.version import version as __version__

from ._pytesttester import PytestTester
test = PytestTester(__name__)
del PytestTester
