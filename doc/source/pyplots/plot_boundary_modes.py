"""A visual illustration of the various signal extension modes supported in
PyWavelets. For efficiency, in the C routines the array is not actually
extended as is done here. This is just a demo for easier visual explanation of
the behavior of the various boundary modes.

In practice, which signal extension mode is beneficial will depend on the
signal characteristics.  For this particular signal, some modes such as
"periodic",  "antisymmetric" and "zeros" result in large discontinuities that
would lead to large amplitude boundary coefficients in the detail coefficients
of a discrete wavelet transform.
"""
import numpy as np
from matplotlib import pyplot as plt


def pad(x, pad_widths, mode):
    """Extend a 1D signal using a given boundary mode.

    Like numpy.pad but supports all PyWavelets boundary modes.
    """
    if np.isscalar(pad_widths):
        pad_widths = (pad_widths, pad_widths)

    if x.ndim > 1:
        raise ValueError("This padding function is only for 1D signals.")

    if mode in ['symmetric', 'reflect']:
        xp = np.pad(x, pad_widths, mode=mode)
    elif mode in ['periodic', 'periodization']:
        if mode == 'periodization' and x.size % 2 == 1:
            raise ValueError("periodization expects an even length signal.")
        xp = np.pad(x, pad_widths, mode='wrap')
    elif mode == 'zeros': 
        xp = np.pad(x, pad_widths, mode='constant', constant_values=0)
    elif mode == 'constant':
        xp = np.pad(x, pad_widths, mode='edge')
    elif mode == 'smooth':
        xp = np.pad(x, pad_widths, mode='linear_ramp',
                    end_values=(x[0] + pad_widths[0]*(x[0] - x[1]),
                                x[-1] + pad_widths[1]*(x[-1] - x[-2])))
    elif mode == 'antisymmetric':
        # implement by flipping portions symmetric padding
        npad_l, npad_r = pad_widths
        xp = np.pad(x, pad_widths, mode='symmetric')
        r_edge = npad_l + x.size - 1
        l_edge = npad_l
        # width of each reflected segment
        seg_width = x.size
        # flip reflected segments on the right of the original signal
        n = 1
        while r_edge <= xp.size:
            segment_slice = slice(r_edge + 1,
                                  min(r_edge + 1 + seg_width, xp.size))
            if n % 2:
                xp[segment_slice] *= -1
            r_edge += seg_width
            n += 1

        # flip reflected segments on the left of the original signal
        n = 1
        while l_edge >= 0:
            segment_slice = slice(max(0, l_edge - seg_width), l_edge)
            if n % 2:
                xp[segment_slice] *= -1
            l_edge -= seg_width
            n += 1
    elif mode == 'antireflect':
        npad_l, npad_r = pad_widths
        # pad with zeros to get final size
        xp = np.pad(x, pad_widths, mode='constant', constant_values=0)

        # right and left edge of the original signal within the padded one
        r_edge = npad_l + x.size - 1
        l_edge = npad_l
        # values of the right and left edge of the original signal
        rv1 = x[-1]
        lv1 = x[0]
        # width of each reflected segment
        seg_width = x.size - 1

        # Generate all reflected segments on the right of the signal.
        # odd reflections of the signal involve these coefficients
        xr_odd = x[-2::-1]
        # even reflections of the signal involve these coefficients
        xr_even = x[1:]
        n = 1
        while r_edge <= xp.size:
            segment_slice = slice(r_edge + 1, min(r_edge + 1 + seg_width, xp.size))
            orig_sl = slice(segment_slice.stop-segment_slice.start)
            rv = xp[r_edge]
            if n % 2:
                xp[segment_slice] = rv - (xr_odd[orig_sl] - rv1)
            else:
                xp[segment_slice] = rv + (xr_even[orig_sl] - lv1)
            r_edge += seg_width
            n += 1

        # Generate all reflected segments on the left of the signal.
        # odd reflections of the signal involve these coefficients
        xl_odd = x[-1:0:-1]
        # even reflections of the signal involve these coefficients
        xl_even = x[:-1]
        n = 1
        while l_edge >= 0:
            segment_slice = slice(max(0, l_edge - seg_width), l_edge)
            orig_sl = slice(segment_slice.start - segment_slice.stop, None)
            lv = xp[l_edge]
            if n % 2:
                xp[segment_slice] = lv - (xl_odd[orig_sl] - lv1)
            else:
                xp[segment_slice] = lv + (xl_even[orig_sl] - rv1)
            l_edge -= seg_width
            n += 1
    return xp


def boundary_mode_subplot(x, mode, ax, symw=True):
    """Plot an illustration of the boundary mode in a subplot axis."""

    # if odd-length, periodization replicates the last sample to make it even
    if mode == 'periodization' and len(x) % 2 == 1:
        x = np.concatenate((x, (x[-1], )))

    npad = 2*len(x)
    t = np.arange(len(x) + 2*npad)
    xp = pad(x, (npad, npad), mode=mode)

    ax.plot(t, xp, 'k.')
    ax.set_title(mode)

    # plot the original signal in red
    if mode == 'periodization':
        ax.plot(t[npad:npad + len(x) - 1], x[:-1], 'r.')
    else:
        ax.plot(t[npad:npad + len(x)], x, 'r.')

    # add vertical bars indicating points of symmetry or boundary extension
    o2 = np.ones(2)
    left = npad
    if symw:
        step = len(x) - 1
        rng = range(-2, 4)
    else:
        left -= 0.5
        step = len(x)
        rng = range(-2, 4)
    if mode in ['smooth', 'constant', 'zeros']:
        rng = range(0, 2)
    for rep in rng:
        ax.plot((left+rep*step)*o2, [xp.min()-.5, xp.max()+.5], 'k-')


# synthetic test signal
x = 5 - np.linspace(-1.9, 1.1, 9)**2

# Create a figure with one subplots per boundary mode
fig, axes = plt.subplots(3, 3, figsize=(10, 6))
plt.subplots_adjust(hspace=0.5)
axes = axes.ravel()
boundary_mode_subplot(x, 'symmetric', axes[0], symw=False)
boundary_mode_subplot(x, 'reflect', axes[1], symw=True)
boundary_mode_subplot(x, 'periodic', axes[2], symw=False)
boundary_mode_subplot(x, 'antisymmetric', axes[3], symw=False)
boundary_mode_subplot(x, 'antireflect', axes[4], symw=True)
boundary_mode_subplot(x, 'periodization', axes[5], symw=False)
boundary_mode_subplot(x, 'smooth', axes[6], symw=False)
boundary_mode_subplot(x, 'constant', axes[7], symw=False)
boundary_mode_subplot(x, 'zeros', axes[8], symw=False)
plt.show()
