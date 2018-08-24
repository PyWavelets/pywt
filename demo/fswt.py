import numpy as np
from matplotlib import pyplot as plt
import pywt

img = pywt.data.camera().astype(float)

# Fully separable transform
fswavedecn_result = pywt.fswavedecn(img, 'db2', 'periodization', levels=4)

# Standard DWT
coefs = pywt.wavedec2(img, 'db2', 'periodization', level=4)
# convert DWT coefficients to a 2D array
mallat_array, mallat_slices = pywt.coeffs_to_array(coefs)


fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.imshow(np.abs(mallat_array)**0.25,
           cmap=plt.cm.gray,
           interpolation='nearest')
ax1.set_axis_off()
ax1.set_title('Mallat decomposition\n(wavedec2)')

ax2.imshow(np.abs(fswavedecn_result.coeffs)**0.25,
           cmap=plt.cm.gray,
           interpolation='nearest')
ax2.set_axis_off()
ax2.set_title('Fully separable decomposition\n(fswt)')

plt.show()
