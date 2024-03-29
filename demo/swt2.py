#!/usr/bin/env python

import matplotlib.pyplot as plt

import pywt
import pywt.data

arr = pywt.data.aero()

plt.imshow(arr, interpolation="nearest", cmap=plt.cm.gray)

level = 0
titles = ['Approximation', ' Horizontal detail',
          'Vertical detail', 'Diagonal detail']
for LL, (LH, HL, HH) in pywt.swt2(arr, 'bior1.3', level=3, start_level=0):
    fig = plt.figure()
    for i, a in enumerate([LL, LH, HL, HH]):
        ax = fig.add_subplot(2, 2, i + 1)
        ax.imshow(a, origin='upper', interpolation="nearest", cmap=plt.cm.gray)
        ax.set_title(titles[i], fontsize=12)

    fig.suptitle(f"SWT2 coefficients, level {level}", fontsize=14)
    level += 1


plt.show()
