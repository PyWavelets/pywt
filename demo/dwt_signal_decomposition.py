#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pywt
import time
import numpy
import pylab

data1 = pylab.array(range(1,400) + range(398, 600) + range(601, 1024))
x = pylab.arange(612-80, 20, -0.5)/250.
data2 = pylab.sin(40*pylab.log(x)) * pylab.sign((pylab.log(x)))

from sample_data import ecg as data3

mode = pywt.MODES.sp1
def plot(data, w, title):
	print title
	w = pywt.Wavelet(w)
	a = data
	ca = []
	cd = []
        for i in xrange(5):
                (a, d) = pywt.dwt(a, w, mode)
                ca.append(a)
                cd.append(d)

	rec_a = []
	rec_d = []

	for i, coeff in enumerate(ca):
            coeff_list = [coeff, None] + [None]*i
            rec_a.append(pywt.waverec(coeff_list, w))
            
	for i, coeff in enumerate(cd):
            coeff_list = [None, coeff] + [None]*i
            rec_d.append(pywt.waverec(coeff_list, w))
			
	pylab.figure()
	ax_main = pylab.subplot(len(rec_a)+1,1,1)
	pylab.title(title)
	ax_main.plot(data)
	pylab.xlim(0, len(data)-1)

	for i, y in enumerate(rec_a):
		#print len(data), len(x), len(data) / (2**(i+1))
		ax = pylab.subplot(len(rec_a)+1, 2, 3+i*2)
		ax.plot(y, 'r')
		pylab.xlim(0, len(y)-1)
		pylab.ylabel("A%d" % (i+1))

	for i, y in enumerate(rec_d):
		ax = pylab.subplot(len(rec_d)+1, 2, 4+i*2)
		ax.plot(y, 'g')
		pylab.xlim(0, len(y)-1)
		#pylab.ylim(min(0,1.4*min(x)), max(0,1.4*max(x)))
		pylab.ylabel("D%d" % (i+1))


print "Signal decomposition (S = An + Dn + Dn-1 + ... + D1)"
plot(data1, 'coif5', "DWT: Signal irregularity")
plot(data2, 'sym5', "DWT: Frequency and phase change - Symmlets5")
plot(data3, 'sym5', "DWT: Ecg sample - Symmlets5")

pylab.show()
