#!/usr/bin/env python

"""Helper script for creating image .dat files by pickling.

Usage:

    python create_dat.py <name of image file> <name of dat file>

Example (to create aero.dat):

    python create_dat.py aero.png aero.dat

Requires Scipy and PIL.
"""

from __future__ import print_function

import pickle
import sys

from scipy.misc import imread

if len(sys.argv) != 3:
    print(__doc__)
    exit()

image_fname = sys.argv[1]
dat_fname = sys.argv[2]

data = imread(image_fname)

with open(dat_fname, 'w') as dat_file:
    pickle.dump(data, dat_file)
