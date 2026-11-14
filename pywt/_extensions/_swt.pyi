from typing import Literal, TypeVar, overload

import numpy as np
from numpy.typing import NDArray

from ._pywt import Wavelet

_CDataT = TypeVar(
    "_CDataT", bound=np.float32 | np.float64 | np.complex64 | np.complex128
)

def swt_max_level(input_len: int) -> int: ...
@overload
def swt(data: NDArray[_CDataT], wavelet: Wavelet, level: int, start_level: int, trim_approx: Literal[False] = False) -> list[tuple[NDArray[_CDataT], NDArray[_CDataT]]]: ...
@overload
def swt(data: NDArray[_CDataT], wavelet: Wavelet, level: int, start_level: int, trim_approx: Literal[True]) -> list[NDArray[_CDataT]]: ...
@overload
def swt(data: NDArray[_CDataT], wavelet: Wavelet, level: int, start_level: int, trim_approx: bool = False) -> list[tuple[NDArray[_CDataT], NDArray[_CDataT]]] | list[NDArray[_CDataT]]: ...
@overload
def swt_axis(data: NDArray[_CDataT], wavelet: Wavelet, level: int, start_level: int, axis: int = 0, trim_approx: Literal[False] = False) -> list[tuple[NDArray[_CDataT], NDArray[_CDataT]]]: ...
@overload
def swt_axis(data: NDArray[_CDataT], wavelet: Wavelet, level: int, start_level: int, axis: int = 0, *, trim_approx: Literal[True]) -> list[NDArray[_CDataT]]: ...
@overload
def swt_axis(data: NDArray[_CDataT], wavelet: Wavelet, level: int, start_level: int, axis: int = 0, trim_approx: bool = False) -> list[tuple[NDArray[_CDataT], NDArray[_CDataT]]] | list[NDArray[_CDataT]]: ...
