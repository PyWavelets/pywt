# -*- coding: utf-8 -*-

# Copyright (c) 2006-2008 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

# $Id$

"""Lists builtin wavelet families and names"""

__all__ = ["families", "wavelist"]

# reflects wavelets_coeffs.h

bior_n = [(1,1), (1,3), (1,5),
          (2,2), (2,4), (2,6), (2,8),
          (3,1), (3,3), (3,5), (3,7), (3,9),
          (4,4),
          (5,5),
          (6,8)
]

rbio_n = bior_n[:]

sym_n = range(2, 21)
db_n = range(1, 21)
coif_n = range(1, 6)

__daubechies = [("db%d" % n) for n in db_n]
__symlets = [("sym%d" % n) for n in sym_n]
__coiflets = [("coif%d" % n) for n in coif_n]
__haar = ["haar"]
__bior = [("bior%d.%d" % (n, m)) for n, m in bior_n]
__rbio = [("rbio%d.%d" % (n, m)) for n, m in rbio_n]
__dmey = ["dmey"]

del bior_n, sym_n, db_n, coif_n, rbio_n, n, m

__wavelet_names = __haar + __daubechies + __symlets + __coiflets + __bior + __rbio + __dmey


def families(short=True):
    if short:
        return ["haar", "db", "sym", "coif", "bior", "rbio", "dmey"]
    else:
        return ["Haar", "Daubechies", "Symlets", "Coiflets", "Biorthogonal", "Reverse biorthogonal", "Discrete Meyer (FIR Approximation)"]

def wavelist(short_name=None):
    """
    Returns list of available wavelet names from given family.

    short_name - short family name ("haar", "db", "sym", "coif", "bior", "rbio" or "dmey")
    """

    names = {"db": __daubechies,
             "sym": __symlets,
             "coif": __coiflets,
             "haar": __haar,
             "bior": __bior,
             "rbio": __rbio,
             "dmey": __dmey,
             }
        
    if short_name is None:
        return __wavelet_names[:]
    elif short_name in names:
        return names[short_name][:]
    else:
        raise ValueError("Invalid short family name '%s'" % short_name)

if __name__ == "__main__":
    print wavelist()
    for n in families():
        print wavelist(n)

    import pywt

    for n in wavelist():
        print pywt.Wavelet(n)
