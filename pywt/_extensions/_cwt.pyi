from typing import TypeVar

import numpy as np
from _pywt import ContinuousWavelet
from numpy.typing import NDArray

_DataT = TypeVar("_DataT", bound=np.float32 | np.float64)

def cwt_psi_single(
    data: NDArray[_DataT], wavelet: ContinuousWavelet, output_len: int
) -> NDArray[_DataT] | tuple[NDArray[_DataT], NDArray[_DataT]]: ...
