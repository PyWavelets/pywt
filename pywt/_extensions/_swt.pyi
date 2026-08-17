from typing import TypeVar

import numpy as np
from numpy.typing import NDArray

from ._pywt import Wavelet

_CDataT = TypeVar(
    "_CDataT", bound=np.float32 | np.float64 | np.complex64 | np.complex128
)

def swt_max_level(input_len: int) -> int: ...
def swt(data: NDArray[_CDataT], wavelet: Wavelet, level: int, start_level: int, trim_approx: bool = False) -> NDArray[_CDataT]: ...
def swt_axis(data: NDArray[_CDataT], wavelet: Wavelet, level: int, start_level: int, axis: int = 0, trim_approx: bool = False) -> NDArray[_CDataT]: ...
