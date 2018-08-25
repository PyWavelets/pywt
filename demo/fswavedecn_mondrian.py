"""Using the FSWT to process anistropic images.

In this demo, an anisotropic piecewise-constant image is transformed by the
standard DWT and the fully-separable DWT. The 'Haar' wavelet gives a sparse
representation for such piecewise constant signals (detail coefficients are
only non-zero near edges).

For such anistropic signals, the number of non-zero coefficients will be lower
for the fully separable DWT than for the isotropic one.

This example is inspired by the following publication where it is proven that
the FSWT gives a sparser representation than the DWT for this class of
anistropic images:

.. V Velisavljevic, B Beferull-Lozano, M Vetterli and PL Dragotti.
   Directionlets: Anisotropic Multidirectional Representation With
   Separable Filtering. IEEE Transactions on Image Processing, Vol. 15,
   No. 7, July 2006.

"""

import numpy as np
import pywt

from matplotlib import pyplot as plt


def mondrian(shape=(256, 256), nx=5, ny=8, seed=4):
    """ Piecewise-constant image (reminiscent of Dutch painter Piet Mondrian's
    geometrical period).
    """
    rstate = np.random.RandomState(seed)
    min_dx = 0
    while(min_dx < 3):
        xp = np.sort(np.round(rstate.rand(nx-1)*shape[0]).astype(np.int))
        xp = np.concatenate(((0, ), xp, (shape[0], )))
        min_dx = np.min(np.diff(xp))
    min_dy = 0
    while(min_dy < 3):
        yp = np.sort(np.round(rstate.rand(ny-1)*shape[1]).astype(np.int))
        yp = np.concatenate(((0, ), yp, (shape[1], )))
        min_dy = np.min(np.diff(yp))
    img = np.zeros(shape)
    for ix, x in enumerate(xp[:-1]):
        for iy, y in enumerate(yp[:-1]):
            slices = [slice(x, xp[ix+1]), slice(y, yp[iy+1])]
            val = rstate.rand(1)[0]
            img[slices] = val
    return img


# create an anisotropic piecewise constant image
img = mondrian((128, 128))

# perform DWT
coeffs_dwt = pywt.wavedecn(img, wavelet='db1', level=None)

# convert coefficient dictionary to a single array
coeff_array_dwt, _ = pywt.coeffs_to_array(coeffs_dwt)

# perform fully seperable DWT
fswavedecn_result = pywt.fswavedecn(img, wavelet='db1')

nnz_dwt = np.sum(coeff_array_dwt != 0)
nnz_fswavedecn = np.sum(fswavedecn_result.coeffs != 0)

print("Number of nonzero wavedecn coefficients = {}".format(np.sum(nnz_dwt)))
print("Number of nonzero fswavedecn coefficients = {}".format(np.sum(nnz_fswavedecn)))

img = mondrian()
fig, axes = plt.subplots(1, 3)
imshow_kwargs = dict(cmap=plt.cm.gray, interpolation='nearest')
axes[0].imshow(img, **imshow_kwargs)
axes[0].set_title('Anisotropic Image')
axes[1].imshow(coeff_array_dwt != 0, **imshow_kwargs)
axes[1].set_title('Nonzero DWT\ncoefficients\n(N={})'.format(nnz_dwt))
axes[2].imshow(fswavedecn_result.coeffs != 0, **imshow_kwargs)
axes[2].set_title('Nonzero FSWT\ncoefficients\n(N={})'.format(nnz_fswavedecn))
for ax in axes:
    ax.set_axis_off()

plt.show()
