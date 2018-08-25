from itertools import product
import numpy as np
from matplotlib import pyplot as plt
from pywt._doc_utils import (wavedec_keys, wavedec2_keys, draw_2d_wp_basis,
                             draw_2d_fswavedecn_basis)


def _2d_fswavedecn_coords(shape, levels):
    coords = []
    centers = {}  # retain center of boxes for use in labeling
    for key in product(wavedec_keys(levels), repeat=2):
        (key0, key1) = key
        offsets = [0, 0]
        widths = list(shape)
        for n0, char in enumerate(key0):
            if char in ['d']:
                offsets[0] += shape[0] // 2**(n0 + 1)
        for n1, char in enumerate(key1):
            if char in ['d']:
                offsets[1] += shape[1] // 2**(n1 + 1)
        widths[0] = shape[0] // 2**(n0 + 1)
        widths[1] = shape[1] // 2**(n1 + 1)
        xc, yc = _box((offsets[0], -offsets[1]),
                      (offsets[0] + widths[0], -offsets[1] - widths[1]))
        coords.append((xc, yc))
        centers[(key0, key1)] = (offsets[0] + widths[0] / 2,
                                 -offsets[1] - widths[1] / 2)
    return coords, centers


def draw_2d_fswavedecn_basis(shape, levels, fmt='k', plot_kwargs={}, ax=None,
                             label_levels=0):
    """Plot a 2D representation of a WaveletPacket2D basis."""
    coords, centers = _2d_fswavedecn_coords(shape, levels)
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    else:
        fig = ax.get_figure()
    for coord in coords:
        ax.plot(coord[0], coord[1], fmt)
    ax.set_axis_off()
    ax.axis('square')
    if label_levels > 0:
        for key, c in centers.items():
            lev = np.max([len(k) for k in key])
            if lev <= label_levels:
                ax.text(c[0], c[1], key,
                        horizontalalignment='center',
                        verticalalignment='center')
    return fig, ax


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
