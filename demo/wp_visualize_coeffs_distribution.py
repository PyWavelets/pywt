#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywt import WaveletPacket
import pylab
import numpy

x = numpy.arange(612-80, 20, -0.5)/150.
data = numpy.sin(20*pylab.log(x)) * numpy.sign((pylab.log(x)))
from sample_data import ecg as data

wp = WaveletPacket(data, 'sym5', maxlevel=4)

pylab.bone()
pylab.subplot(wp.maxlevel+1, 1, 1)
pylab.plot(data, 'k')
pylab.xlim(0, len(data)-1)
pylab.title("Wavelet packet coefficients")

for i in range(1, wp.maxlevel+1):
    ax = pylab.subplot(wp.maxlevel+1,1,i+1)
    nodes = wp.get_level(i, "freq")
    nodes.reverse()
    labels = [n.path for n in nodes]
    values = -abs(numpy.array([n.data for n in nodes]))
    pylab.imshow(values, interpolation='nearest', aspect='auto')
    pylab.yticks(numpy.arange(len(labels)-0.5, -0.5, -1), labels)
    pylab.setp(ax.get_xticklabels(), visible=False)


pylab.show()
