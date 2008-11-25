#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
import numpy
import Image # PIL
import pywt
from pywt import WaveletPacket2D

im = Image.open("data/aero.png").convert('L')
arr = numpy.fromstring(im.tostring(), numpy.uint8)
arr.shape = (im.size[1], im.size[0])

wp2 = WaveletPacket2D(arr, 'db2', 'sym', maxlevel=2)

pylab.imshow(arr, interpolation="nearest", cmap=pylab.cm.gray)

path = ['d', 'v', 'h', 'a']

#mod = lambda x: x
#mod = lambda x: abs(x)
mod = lambda x: numpy.sqrt(abs(x))

pylab.figure()
for i,p2 in enumerate(path):
    pylab.subplot(2,2,i+1)
    p1p2 = p2
    pylab.imshow(mod(wp2[p1p2].data), origin='image', interpolation="nearest", cmap=pylab.cm.gray)
    pylab.title(p1p2)


for p1 in path:
    pylab.figure()
    for i,p2 in enumerate(path):
        pylab.subplot(2,2,i+1)
        p1p2 = p1+p2
        pylab.imshow(mod(wp2[p1p2].data), origin='image', interpolation="nearest", cmap=pylab.cm.gray)
        pylab.title(p1p2)

pylab.show()
