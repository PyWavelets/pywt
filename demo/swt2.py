#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
import numpy
import Image # PIL
import pywt

im = Image.open("data/aero.png").convert('L')
arr = numpy.fromstring(im.tostring(), numpy.uint8)
arr.shape = (im.size[1], im.size[0])

pylab.imshow(arr, interpolation="nearest", cmap=pylab.cm.gray)

for LL, (LH, HL, HH) in pywt.swt2(arr, 'bior1.3', level=3, start_level=0):
    pylab.figure()
    for i,a in enumerate([LL, LH, HL, HH]):
        pylab.subplot(2,2,i+1)
        pylab.imshow(a, origin='image', interpolation="nearest", cmap=pylab.cm.gray)

pylab.show()
