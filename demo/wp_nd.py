#!/usr/bin/env python
# Note: This demo is a repeat of wp_2d, but using WaveletPacketND instead

import numpy as np
import matplotlib.pyplot as plt

from pywt import WaveletPacketND
import pywt.data


arr = pywt.data.aero()

maxlevel = 2
wp2 = WaveletPacketND(arr, 'db2', 'symmetric', maxlevel=maxlevel)

# Show original figure
plt.imshow(arr, interpolation="nearest", cmap=plt.cm.gray)

# path = ['aa', 'ad', 'da', 'dd']

# # Show level 1 nodes
# fig = plt.figure()
# for i, p2 in enumerate(path):
#     ax = fig.add_subplot(2, 2, i + 1)
#     ax.imshow(np.sqrt(np.abs(wp2[p2].data)), origin='image',
#               interpolation="nearest", cmap=plt.cm.gray)
#     ax.set_title(p2)

# # Show level 2 nodes
# for p1 in path:
#     fig = plt.figure()
#     for i, p2 in enumerate(path):
#         ax = fig.add_subplot(2, 2, i + 1)
#         p1p2 = p1 + p2
#         ax.imshow(np.sqrt(np.abs(wp2[p1p2].data)), origin='image',
#                   interpolation="nearest", cmap=plt.cm.gray)
#         ax.set_title(p1p2)

fig = plt.figure()
i = 1
nsubplots = len(wp2.get_level(maxlevel, 'natural'))
nrows = int(np.floor(np.sqrt(nsubplots)))
ncols = int(np.ceil(nsubplots/nrows))
for node in wp2.get_level(maxlevel, 'natural'):
    ax = fig.add_subplot(nrows, ncols, i)
    ax.set_title("%s" % (node.pretty_path, ))
    ax.imshow(np.sqrt(np.abs(node.data)), origin='image',
              interpolation="nearest", cmap=plt.cm.gray)
    ax.set_axis_off()
    i += 1

plt.show()
