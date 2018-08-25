import numpy as np
import pywt
from matplotlib import pyplot as plt


def wavedec2_keys(level):
    """Subband keys corresponding to a wavedec2 decomposition."""
    approx = ''
    coeffs = {}
    for lev in range(level):
        for k in ['a', 'h', 'v', 'd']:
            coeffs[approx + k] = None
        approx = 'a' * (lev + 1)
        if lev < level - 1:
            coeffs.pop(approx)
    return list(coeffs.keys())


def _box(bl, ur):
    """(x, y) coordinates for the 4 lines making up a rectangular box.

    Parameters
    ==========
    bl : float
        The bottom left corner of the box
    ur : float
        The upper right corner of the box

    Returns
    =======
    coords : 2-tuple
        The first and second elements of the tuple are the x and y coordinates
        of the box.
    """
    xl, xr = bl[0], ur[0]
    yb, yt = bl[1], ur[1]
    box_x = [xl, xr,
             xr, xr,
             xr, xl,
             xl, xl]
    box_y = [yb, yb,
             yb, yt,
             yt, yt,
             yt, yb]
    return (box_x, box_y)


def _2d_wp_basis_coords(shape, keys):
    # Coordinates of the lines to be drawn by draw_2d_wp_basis
    coords = []
    centers = {}  # retain center of boxes for use in labeling
    for key in keys:
        offset_x = offset_y = 0
        for n, char in enumerate(key):
            if char in ['h', 'd']:
                offset_x += shape[0]//2**(n+1)
            if char in ['v', 'd']:
                offset_y += shape[1]//2**(n+1)
        sx = shape[0]//2**(n+1)
        sy = shape[1]//2**(n+1)
        xc, yc = _box((offset_x, -offset_y),
                      (offset_x + sx, -offset_y - sy))
        coords.append((xc, yc))
        centers[key] = (offset_x + sx//2, -offset_y - sy//2)
    return coords, centers


def draw_2d_wp_basis(shape, keys, fmt='k', plot_kwargs={}, ax=None,
                     label_levels=0):
    """Plot a 2D representation of a WaveletPacket2D basis."""
    coords, centers = _2d_wp_basis_coords(shape, keys)
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
            if len(key) <= label_levels:
                ax.text(c[0], c[1], key,
                        horizontalalignment='center',
                        verticalalignment='center')
    return fig, ax


x = pywt.data.camera().astype(np.float32)
shape = x.shape

max_lev = 3       # how many levels of decomposition to draw
label_levels = 3  # how many levels to explicitly label on the plots

fig, axes = plt.subplots(2, 4, figsize=[14, 8])
for level in range(0, max_lev + 1):
    if level == 0:
        # show the original image before decomposition
        axes[0, 0].set_axis_off()
        axes[1, 0].imshow(x, cmap=plt.cm.gray)
        axes[1, 0].set_title('Image')
        axes[1, 0].set_axis_off()
        continue

    # plot subband boundaries of a standard DWT basis
    draw_2d_wp_basis(shape, wavedec2_keys(level), ax=axes[0, level],
                     label_levels=label_levels)
    axes[0, level].set_title('{} level\ndecomposition'.format(level))

    # compute the 2D DWT
    c = pywt.wavedec2(x, 'db2', mode='periodization', level=level)
    # normalize each coefficient array independently for better visibility
    c[0] /= np.abs(c[0]).max()
    for detail_level in range(level):
        c[detail_level + 1] = [d/np.abs(d).max() for d in c[detail_level + 1]]
    # show the normalized coefficients
    arr, slices = pywt.coeffs_to_array(c)
    axes[1, level].imshow(arr, cmap=plt.cm.gray)
    axes[1, level].set_title('Coefficients\n({} level)'.format(level))
    axes[1, level].set_axis_off()

plt.tight_layout()
plt.show()
