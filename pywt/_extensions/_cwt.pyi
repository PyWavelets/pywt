from _pywt import ContinuousWavelet, DataT
from numpy.typing import NDArray

def cwt_psi_single(data: NDArray[DataT], wavelet: ContinuousWavelet, output_len: int) -> NDArray[DataT] | tuple[NDArray[DataT], NDArray[DataT]]: ...
