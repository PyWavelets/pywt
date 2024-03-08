from itertools import product

import numpy as np
from matplotlib import pyplot as plt

from pywt._doc_utils import (
    draw_2d_fswavedecn_basis,
    draw_2d_wp_basis,
    wavedec2_keys,
    wavedec_keys,
)

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
axes[0].set_title(f'wavedec2 ({max_lev} level)')

# plot for the fully separable case
draw_2d_fswavedecn_basis(shape, max_lev, ax=axes[1], label_levels=label_levels)
axes[1].set_title(f'fswavedecn ({max_lev} level)')

# get all keys corresponding to a full wavelet packet decomposition
wp_keys = list(product(['a', 'd', 'h', 'v'], repeat=max_lev))
draw_2d_wp_basis(shape, wp_keys, ax=axes[2])
axes[2].set_title(f'wavelet packet\n(full: {max_lev} level)')

# plot an example of a custom wavelet packet basis
keys = ['aaaa', 'aaad', 'aaah', 'aaav', 'aad', 'aah', 'aava', 'aavd',
        'aavh', 'aavv', 'ad', 'ah', 'ava', 'avd', 'avh', 'avv', 'd', 'h',
        'vaa', 'vad', 'vah', 'vav', 'vd', 'vh', 'vv']
draw_2d_wp_basis(shape, keys, ax=axes[3], label_levels=label_levels)
axes[3].set_title('wavelet packet\n(custom)')

plt.tight_layout()
plt.show()
