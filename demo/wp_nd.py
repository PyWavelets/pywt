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

fig = plt.figure()
i = 1
nsubplots = len(wp2.get_level(maxlevel, 'natural'))
nrows = int(np.floor(np.sqrt(nsubplots)))
ncols = int(np.ceil(nsubplots/nrows))
for node in wp2.get_level(maxlevel, 'natural'):
    ax = fig.add_subplot(nrows, ncols, i)
    ax.set_title("%s" % (node.path_tuple, ))
    ax.imshow(np.sqrt(np.abs(node.data)), origin='upper',
              interpolation="nearest", cmap=plt.cm.gray)
    ax.set_axis_off()
    i += 1

plt.show()
