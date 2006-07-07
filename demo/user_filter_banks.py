#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pywt

class FilterBank(object):
    """Sample filter bank with Quadrature Mirror Filters for Haar wavelet"""
    dec_lo = [0.70710678118654757, 0.70710678118654757]
    dec_hi = [-0.70710678118654757, 0.70710678118654757]
    rec_lo = [0.70710678118654757, 0.70710678118654757]
    rec_hi = [0.70710678118654757, -0.70710678118654757]
    def get_filters_coeffs(self):
        return self.dec_lo, self.dec_hi, self.rec_lo, self.rec_hi

data = [1,2,3,4,5,6]

############################################################################
print "Case 1 (custom filter bank - Haar wavelet)"

myBank = FilterBank()
# pass the user supplied filter bank as argument
myWavelet = pywt.Wavelet(name="UserSuppliedWavelet", filter_bank=myBank)
#print myWavelet.get_filters_coeffs()

print "data:", data
a, d = pywt.dwt(data, myWavelet)
print "a:", a
print "d:", d
print "rec:", pywt.idwt(a, d, myWavelet)

############################################################################
print "-" * 75
print "Case 2 (Wavelet object as filter bank - db2 wavelet)"

# builtin wavelets can also be treated as filter banks with theirs
# get_filters_coeffs() method

builtinWavelet = pywt.Wavelet('db2')
myWavelet = pywt.Wavelet(name="UserSuppliedWavelet", filter_bank=builtinWavelet)

print "data:", data
a, d = pywt.dwt(data, myWavelet)
print "a:", a
print "d:", d
print "rec:", pywt.idwt(a, d, myWavelet)

############################################################################
# and if you happen to have installed wavelet module from wavelets.scipy.org
# SVN trunk you may also do this:
try:
    from wavelets import fwt
except:
    raise SystemExit

print "-" * 75
print "Case 3 (Cooperating with wavelets.scipy.org filter banks - db2 wavelet)"

myBank = fwt.DaubechiesFilterBank(4) # == 'db2'
myWavelet = pywt.Wavelet(name="UserSuppliedWavelet", filter_bank=builtinWavelet)

print "data:", data
a, d = pywt.dwt(data, myWavelet)
print "a:", a
print "d:", d
print "rec:", pywt.idwt(a, d, myWavelet)
