#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import matplotlib.pyplot as plt
import numpy as np
import pywt


usage = """
Usage:
    python waveinfo.py waveletname

    Example: python waveinfo.py 'sym5'
"""

try:
    wavelet = pywt.Wavelet(sys.argv[1])
    try:
        level = int(sys.argv[2])
    except IndexError as e:
        level = 10
except ValueError as e:
    print("Unknown wavelet")
    raise SystemExit
except IndexError as e:
    print(usage)
    raise SystemExit


data = wavelet.wavefun(level)
if len(data) == 2:
    x = data[1]
    psi = data[0]
    fig = plt.figure()
    if wavelet.complex_cwt:
        plt.subplot(211)
        plt.title(wavelet.name+' real part')
        mi, ma = np.real(psi).min(), np.real(psi).max()
        margin = (ma - mi) * 0.05
        plt.plot(x,np.real(psi))
        plt.ylim(mi - margin, ma + margin)
        plt.xlim(x[0], x[-1])
        plt.subplot(212)
        plt.title(wavelet.name+' imag part')
        mi, ma = np.imag(psi).min(), np.imag(psi).max()
        margin = (ma - mi) * 0.05
        plt.plot(x,np.imag(psi))
        plt.ylim(mi - margin, ma + margin)
        plt.xlim(x[0], x[-1])
    else:
        mi, ma = psi.min(), psi.max()
        margin = (ma - mi) * 0.05
        plt.plot(x,psi)
        plt.title(wavelet.name)
        plt.ylim(mi - margin, ma + margin)
        plt.xlim(x[0], x[-1])
else:
    funcs, x = data[:-1], data[-1]
    labels = ["scaling function (phi)", "wavelet function (psi)",
              "r. scaling function (phi)", "r. wavelet function (psi)"]
    colors = ("r", "g", "r", "g")
    fig = plt.figure()
    for i, (d, label, color) in enumerate(zip(funcs, labels, colors)):
        mi, ma = d.min(), d.max()
        margin = (ma - mi) * 0.05
        ax = fig.add_subplot((len(data) - 1) // 2, 2, 1 + i)

        ax.plot(x, d, color)
        ax.set_title(label)
        ax.set_ylim(mi - margin, ma + margin)
        ax.set_xlim(x[0], x[-1])

plt.show()
