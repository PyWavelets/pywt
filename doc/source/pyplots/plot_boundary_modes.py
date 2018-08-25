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
from pywt._doc_utils import boundary_mode_subplot

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
