#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gc
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

import pywt


if sys.platform == 'win32':
    clock = time.clock
else:
    clock = time.time

sizes = [20, 50, 100, 120, 150, 200, 250, 300, 400, 500, 600, 750,
         1000, 2000, 3000, 4000, 5000, 6000, 7500,
         10000, 15000, 20000, 25000, 30000, 40000, 50000, 75000,
         100000, 150000, 200000, 250000, 300000, 400000, 500000,
         600000, 750000, 1000000, 2000000, 5000000][:-4]

wavelet_names = ['db1', 'db2', 'db3', 'db4', 'db5', 'db6', 'db7',
                 'db8', 'db9', 'db10', 'sym10', 'coif1', 'coif2',
                 'coif3', 'coif4', 'coif5']


wavelets = [pywt.Wavelet(n) for n in wavelet_names]
mode = pywt.Modes.zero

times_dwt = [[] for i in range(len(wavelets))]
times_idwt = [[] for i in range(len(wavelets))]

for j, size in enumerate(sizes):
    data = np.ones((size,), dtype=np.float64)
    print((("%d/%d" % (j + 1, len(sizes))).rjust(6), str(size).rjust(9)))
    for i, w in enumerate(wavelets):
        min_t1, min_t2 = 9999., 9999.
        for _ in range(5):
            # Repeat timing 5 times to reduce run-to-run variation
            t1 = clock()
            (a, d) = pywt.dwt(data, w, mode)
            t1 = clock() - t1
            min_t1 = min(t1, min_t1)

            t2 = clock()
            a0 = pywt.idwt(a, d, w, mode)
            t2 = clock() - t2
            min_t2 = min(t2, min_t2)

        times_dwt[i].append(min_t1)
        times_idwt[i].append(min_t2)

    gc.collect()


for j, (times, name) in enumerate([(times_dwt, 'dwt'), (times_idwt, 'idwt')]):
    fig = plt.figure(j)
    ax = fig.add_subplot(111)
    ax.set_title(name)

    for i, n in enumerate(wavelet_names):
        ax.loglog(sizes, times[i], label=n)

    ax.legend(loc='best')
    ax.set_xlabel('len(x)')
    ax.set_ylabel('time [s]')


plt.show()
