"""
Demo: Parallel processing accross images

Multithreading can be used to run transforms on a set of images in parallel.
This will give a net performance benefit if the images to be transformed are
sufficiently large.

This demo runs a multilevel wavelet decomposition on a list of 32 images,
each of size (512, 512).  Computations are repeated sequentially and in
parallel and the runtimes compared.

In general, multithreading will be more beneficial for larger images and for
wavelets with a larger filter size.

One can also change ``ndim`` to 3 in the code below to use a set of 3D volumes
instead.
"""

import time
from functools import partial
from multiprocessing import cpu_count

try:
    from concurrent import futures
except ImportError:
    raise ImportError(
        "This demo requires concurrent.futures.  It can be installed for "
        "for python 2.x via:  pip install futures")

import numpy as np
from numpy.testing import assert_array_equal

import pywt

# the test image
cam = pywt.data.camera().astype(float)

ndim = 2                   # dimension of images to transform (2 or 3)
num_images = 32            # number of images to transform
max_workers = cpu_count()  # max number of available threads
nrepeat = 5                # averages used in the benchmark

# create a list of num_images images
if ndim == 2:
    imgs = [cam, ] * num_images
    wavelet = 'db8'
elif ndim == 3:
    # stack image along 3rd dimension to create a [512 x 512 x 16] 3D volume
    im3 = np.concatenate([cam[:, :, np.newaxis], ]*16, axis=-1)
    # create multiple copies of the volume
    imgs = [im3, ] * num_images
    wavelet = 'db1'
else:
    ValueError("Only 2D and 3D test cases implemented")

# define a function to apply to each image
wavedecn_func = partial(pywt.wavedecn, wavelet=wavelet, mode='periodization',
                        level=3)


def concurrent_transforms(func, imgs, max_workers=None):
    """Call func on each img in imgs using a ThreadPoolExecutor."""
    executor = futures.ThreadPoolExecutor
    if max_workers is None:
        # default to as many workers as available cpus
        max_workers = cpu_count()
    results = []
    with executor(max_workers=max_workers) as execute:
        for result in execute.map(func, imgs):
            results.append(result)
    return results


print("Processing {} images of shape {}".format(len(imgs), imgs[0].shape))

# Sequential computation via a list comprehension
tstart = time.time()
for n in range(nrepeat):
    results = [wavedecn_func(img) for img in imgs]
t = (time.time()-tstart)/nrepeat
print("\nSequential Case")
print("\tElapsed time: {:0.2f} ms".format(1000*t))


# Concurrent computation via concurrent.futures
tstart = time.time()
for n in range(nrepeat):
    results_concurrent = concurrent_transforms(wavedecn_func, imgs,
                                               max_workers=max_workers)
t2 = (time.time()-tstart)/nrepeat
print("\nMultithreaded Case")
print("\tNumber of concurrent workers: {}".format(max_workers))
print("\tElapsed time: {:0.2f} ms".format(1000*t2))
print("\nRelative speedup with concurrent = {}".format(t/t2))

# check a couple of the coefficient arrays to verify matching results for
# sequential and multithreaded computation
assert_array_equal(results[-1][0],
                   results_concurrent[-1][0])
assert_array_equal(results[-1][1]['d' + 'a'*(ndim-1)],
                   results_concurrent[-1][1]['d' + 'a'*(ndim-1)])
