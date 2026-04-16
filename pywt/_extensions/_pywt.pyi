from enum import IntEnum
from typing import Any, Literal, Optional, TypeAlias, TypeVar

import numpy as np

_WaveletFamily = Literal[
    "haar",
    "db",
    "sym",
    "coif",
    "bior",
    "rbio",
    "dmey",
    "gaus",
    "mexh",
    "morl",
    "cgau",
    "shan",
    "fbsp",
    "cmor",
]

DataT = TypeVar("DataT", bound=np.float32 | np.float64)

CDataT = TypeVar(
    "CDataT", bound=np.float32 | np.float64 | np.complex64 | np.complex128
)

_Kind: TypeAlias = Literal["all", "continuous", "discrete"]

_Symmetry = Literal[
    "asymmetric",
    "near symmetric",
    "symmetric",
    "anti-symmetric",
    "unknown",
]

class MODE(IntEnum):
    MODE_INVALID = -1
    MODE_ZEROPAD = 0
    MODE_SYMMETRIC = 1
    MODE_CONSTANT_EDGE = 2
    MODE_SMOOTH = 3
    MODE_PERIODIC = 4
    MODE_PERIODIZATION = 5
    MODE_REFLECT = 6
    MODE_ANTISYMMETRIC = 7
    MODE_ANTIREFLECT = 8
    MODE_MAX = 9

ModeInt = MODE | Literal[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

ModeName = Literal[
    "zero",
    "constant",
    "symmetric",
    "reflect",
    "periodic",
    "smooth",
    "periodization",
    "antisymmetric",
    "antireflect",
]

Mode = MODE | ModeName

class _Modes:
    zero: int
    constant: int
    symmetric: int
    reflect: int
    periodic: int
    smooth: int
    periodization: int
    antisymmetric: int
    antireflect: int

    modes: list[ModeName]

    def from_object(self, mode: Mode) -> int: ...

Modes = _Modes()

def wavelist(family: _WaveletFamily | None = None, kind: _Kind = "all") -> list[str]: ...
def families(short: bool = True) -> list[str]: ...

class Wavelet:
    def __init__(self, name: str = "", filter_bank: Any = None) -> None: ...
    def __len__(self) -> int: ...
    @property
    def name(self) -> str: ...
    @property
    def dec_lo(self) -> list[float]: ...
    @property
    def dec_hi(self) -> list[float]: ...
    @property
    def rec_lo(self) -> list[float]: ...
    @property
    def rec_hi(self) -> list[float]: ...
    @property
    def rec_len(self) -> int: ...
    @property
    def dec_len(self) -> int: ...
    @property
    def family_number(self) -> int: ...
    @property
    def family_name(self) -> str: ...
    @property
    def short_family_name(self) -> str: ...
    @property
    def orthogonal(self) -> bool: ...
    @orthogonal.setter
    def orthogonal(self, value: bool) -> None: ...
    @property
    def biorthogonal(self) -> bool: ...
    @biorthogonal.setter
    def biorthogonal(self, value: bool) -> None: ...
    @property
    def symmetry(self) -> _Symmetry: ...
    @property
    def vanishing_moments_psi(self) -> int | None: ...
    @property
    def vanishing_moments_phi(self) -> int | None: ...
    @property
    def filter_bank(
        self,
    ) -> tuple[list[float], list[float], list[float], list[float]]: ...
    def get_filters_coeffs(
        self,
    ) -> tuple[list[float], list[float], list[float], list[float]]: ...
    @property
    def inverse_filter_bank(
        self,
    ) -> tuple[list[float], list[float], list[float], list[float]]: ...
    def get_reverse_filters_coeffs(
        self,
    ) -> tuple[list[float], list[float], list[float], list[float]]: ...

class ContinuousWavelet:
    def __init__(self, name: str = "", dtype: DataT = np.float64) -> None: ...
    @property
    def family_number(self) -> int: ...
    @property
    def family_name(self) -> str: ...
    @property
    def short_family_name(self) -> str: ...
    @property
    def orthogonal(self) -> bool: ...
    @orthogonal.setter
    def orthogonal(self, value: bool) -> None: ...
    @property
    def biorthogonal(self) -> bool: ...
    @biorthogonal.setter
    def biorthogonal(self, value: bool) -> None: ...
    @property
    def complex_cwt(self) -> bool: ...
    @complex_cwt.setter
    def complex_cwt(self, value: bool) -> None: ...
    @property
    def lower_bound(self) -> float | None: ...
    @lower_bound.setter
    def lower_bound(self, value: float) -> None: ...
    @property
    def upper_bound(self) -> float | None: ...
    @upper_bound.setter
    def upper_bound(self, value: float) -> None: ...
    @property
    def center_frequency(self) -> float | None: ...
    @center_frequency.setter
    def center_frequency(self, value: float) -> None: ...
    @property
    def bandwidth_frequency(self) -> float | None: ...
    @bandwidth_frequency.setter
    def bandwidth_frequency(self, value: float) -> None: ...
    @property
    def fbsp_order(self) -> int | None: ...
    @fbsp_order.setter
    def fbsp_order(self, value: int) -> None: ...
    @property
    def symmetry(self) -> _Symmetry: ...

def DiscreteContinuousWavelet(
    name: str = "", filter_bank: Any = None
) -> Wavelet | ContinuousWavelet: ...
