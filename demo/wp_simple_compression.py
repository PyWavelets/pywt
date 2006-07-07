#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywt import WaveletPacket
import pylab
import math
import numpy

x = pylab.arrayrange(612-80, 20, -0.5)/150.
data = pylab.sin(20*pylab.log(x)) * pylab.sign((pylab.log(x)))

#from sample_data import ecg as data
#data = numpy.array(data, numpy.float64) / 100.

## simple energy based criteria, not very efficient
def select(node, min_energy):
    if node.energy() < math.log(min_energy):
        print node.path, "marked as ZT", len(node.data)
        node.markZeroTree()
        return False # stop processing child nodes
    return True

## create our tree
wp = WaveletPacket(data, wavelet='sym3', mode='sp1', maxlevel=6)

treshold = 0.0021
base_energy = wp.energy()
wp.walk(select, (treshold*base_energy,))


print "Non-zero trees:"
for node in wp.get_nonzero():
    print node.path, len(node.data)

new_data = wp.reconstruct()
print "Reconstructing %d samples using %d coefficients" % (wp.data_size, sum([len(node.data) for node in wp.get_nonzero()]))
print "Mean difference:", sum(abs(new_data - data))/len(data)
print "Retaining %.2f%% energy" % (100-(base_energy-wp.energy())*100./base_energy)

pylab.plot(x, data, label="orig")
pylab.plot(x, wp.data, label="rec")
pylab.xlim(min(x), max(x))

#pylab.plot(data, label="orig")
#pylab.plot(wp.data, label="rec")
#pylab.xlim(0, len(data)-1)

pylab.legend()
pylab.show()
