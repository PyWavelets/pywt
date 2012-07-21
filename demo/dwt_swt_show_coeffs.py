#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pywt
import pylab

data1 = pylab.array(range(1, 400) + range(398, 600) + range(601, 1024)) / 1024.
data2 = pylab.arange(612 - 80, 20, -0.5) / 250.
data2 = pylab.sin(40 * pylab.log(data2)) * pylab.sign((pylab.log(data2)))
from sample_data import ecg as data3

mode = pywt.MODES.sp1
DWT = 1


def plot(data, w, title):
    w = pywt.Wavelet(w)
    a = data
    ca = []
    cd = []

    if DWT:
        for i in xrange(5):
            (a, d) = pywt.dwt(a, w, mode)
            ca.append(a)
            cd.append(d)
    else:
        coeffs = pywt.swt(data, w, 5)  # [(cA5, cD5), ..., (cA1, cD1)]
        for a, d in reversed(coeffs):
            ca.append(a)
            cd.append(d)

    pylab.figure()
    ax_main = pylab.subplot(len(ca) + 1, 1, 1)
    pylab.title(title)
    ax_main.plot(data)
    pylab.xlim(0, len(data) - 1)

    for i, x in enumerate(ca):
        ax = pylab.subplot(len(ca) + 1, 2, 3 + i * 2)
        ax.plot(x, 'r')
        if DWT:
            pylab.xlim(0, len(x) - 1)
        else:
            pylab.xlim(w.dec_len * i, len(x) - 1 - w.dec_len * i)
        pylab.ylabel("A%d" % (i + 1))

    for i, x in enumerate(cd):
        ax = pylab.subplot(len(cd) + 1, 2, 4 + i * 2)
        ax.plot(x, 'g')
        pylab.xlim(0, len(x) - 1)
        if DWT:
            pylab.ylim(min(0, 1.4 * min(x)), max(0, 1.4 * max(x)))
        else:  # SWT
            pylab.ylim(
                min(0, 2 * min(
                    x[w.dec_len * (1 + i):len(x) - w.dec_len * (1 + i)])),
                max(0, 2 * max(
                    x[w.dec_len * (1 + i):len(x) - w.dec_len * (1 + i)]))
            )
        pylab.ylabel("D%d" % (i + 1))


DWT = 1
plot(data1, 'db1', "DWT: Signal irregularity shown in D1 - Haar wavelet")
plot(data2, 'sym5', "DWT: Frequency and phase change - Symmlets5")
plot(data3, 'sym5', "DWT: Ecg sample - Symmlets5")

DWT = 0  # SWT
plot(data1, 'db1', "SWT: Signal irregularity detection - Haar wavelet")
plot(data2, 'sym5', "SWT: Frequency and phase change - Symmlets5")
plot(data3, 'sym5', "SWT: Ecg sample - simple QRS detection - Symmlets5")

pylab.show()
