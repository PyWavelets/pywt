from itertools import product
import numpy as np
from matplotlib import pyplot as plt
from pywt._doc_utils import (wavedec_keys, wavedec2_keys, draw_2d_wp_basis,
                             draw_2d_fswavedecn_basis)

shape = (512, 512)

max_lev = 4       # how many levels of decomposition to draw
label_levels = 2  # how many levels to explicitly label on the plots

if False:
    fig, axes = plt.subplots(1, 4, figsize=[16, 4])
    axes = axes.ravel()
else:
    fig, axes = plt.subplots(2, 2, figsize=[8, 8])
    axes = axes.ravel()

# plot a 5-level standard DWT basis
draw_2d_wp_basis(shape, wavedec2_keys(max_lev), ax=axes[0],
                 label_levels=label_levels)
axes[0].set_title('wavedec2 ({} level)'.format(max_lev))

# plot for the fully separable case
draw_2d_fswavedecn_basis(shape, max_lev, ax=axes[1], label_levels=label_levels)
axes[1].set_title('fswavedecn ({} level)'.format(max_lev))

# get all keys corresponding to a full wavelet packet decomposition
wp_keys = list(product(['a', 'd', 'h', 'v'], repeat=max_lev))
draw_2d_wp_basis(shape, wp_keys, ax=axes[2])
axes[2].set_title('wavelet packet\n(full: {} level)'.format(max_lev))

# plot an example of a custom wavelet packet basis
keys = ['aaaa', 'aaad', 'aaah', 'aaav', 'aad', 'aah', 'aava', 'aavd',
        'aavh', 'aavv', 'ad', 'ah', 'ava', 'avd', 'avh', 'avv', 'd', 'h',
        'vaa', 'vad', 'vah', 'vav', 'vd', 'vh', 'vv']
draw_2d_wp_basis(shape, keys, ax=axes[3], label_levels=label_levels)
axes[3].set_title('wavelet packet\n(custom)'.format(max_lev))

plt.tight_layout()
plt.show()
