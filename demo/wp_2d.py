#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from pywt import WaveletPacket2D
import pywt.data


arr = pywt.data.aero()

wp2 = WaveletPacket2D(arr, 'db2', 'symmetric', maxlevel=2)

# Show original figure
plt.imshow(arr, interpolation="nearest", cmap=plt.cm.gray)

path = ['d', 'v', 'h', 'a']

# Show level 1 nodes
fig = plt.figure()
for i, p2 in enumerate(path):
    ax = fig.add_subplot(2, 2, i + 1)
    ax.imshow(np.sqrt(np.abs(wp2[p2].data)), origin='image',
              interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(p2)

# Show level 2 nodes
for p1 in path:
    fig = plt.figure()
    for i, p2 in enumerate(path):
        ax = fig.add_subplot(2, 2, i + 1)
        p1p2 = p1 + p2
        ax.imshow(np.sqrt(np.abs(wp2[p1p2].data)), origin='image',
                  interpolation="nearest", cmap=plt.cm.gray)
        ax.set_title(p1p2)

fig = plt.figure()
i = 1
for row in wp2.get_level(2, 'freq'):
    for node in row:
        ax = fig.add_subplot(len(row), len(row), i)
        ax.set_title("%s=(%s row, %s col)" % (
                     (node.path,) + wp2.expand_2d_path(node.path)))
        ax.imshow(np.sqrt(np.abs(node.data)), origin='image',
                  interpolation="nearest", cmap=plt.cm.gray)
        i += 1

plt.show()
