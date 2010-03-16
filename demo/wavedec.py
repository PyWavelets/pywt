#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pywt

data = range(16)
wavelet = 'db4'
level = 2
mode = 'cpd'

print "original data:"
print data
print

# dec = [cA(n-1) cD(n-1) cD(n-2) ... cD(2) cD(1)]
dec = pywt.wavedec(data, wavelet, mode, level)

print "decomposition:"

print "cA%d:" % (len(dec)-1)
print ' '.join([("%.3f" % val) for val in dec[0]])

for i,d in enumerate(dec[1:]):
	print "cD%d:" % (len(dec)-1-i)
	print ' '.join([("%.3f" % val) for val in d])

print
print "reconstruction:"

print ' '.join([("%.3f" % val) for val in pywt.waverec(dec, wavelet, mode)])
