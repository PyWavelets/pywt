#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Plot scaling and wavelet functions for db, sym, coif, bior and rbio families

import pywt
import pylab
import itertools

iterations = 5

for family, (rows,cols) in [('db', (4,3)), ('sym', (4,3)), ('coif', (3, 2))]:

    f = pylab.figure()
    f.subplots_adjust(hspace=0.2, wspace=0.2, bottom=.02, left=.06, right=.97, top=.94)
    colors = itertools.cycle('bgrcmyk')
    
    wnames = pywt.wavelist(family)
    print wnames
    i = iter(wnames)
    for col in xrange(cols):
        for row in xrange(rows):
            try:
                wavelet = pywt.Wavelet(i.next())
            except StopIteration:
                break
            phi, psi, x = wavelet.wavefun(iterations)
    
            color = colors.next()
            ax = pylab.subplot(rows, 2*cols, 1 + 2*(col + row*cols))
            pylab.title(wavelet.name + " phi")
            pylab.plot(x, phi, color)
            pylab.xlim(min(x), max(x))
    
            ax = pylab.subplot(rows, 2*cols, 1 + 2*(col + row*cols) + 1)
            pylab.title(wavelet.name + " psi")
            pylab.plot(x, psi, color)
            pylab.xlim(min(x), max(x))

for family, (rows, cols) in [('bior', (4, 3)), ('rbio', (4, 3))]:

    f = pylab.figure()
    f.subplots_adjust(hspace=0.5, wspace=0.2, bottom=.02, left=.06, right=.97, top=.94)
    
    colors = itertools.cycle('bgrcmyk')
    wnames = pywt.wavelist(family)
    i = iter(wnames)
    for col in xrange(cols):
        for row in xrange(rows):
            try:
                wavelet = pywt.Wavelet(i.next())
            except StopIteration:
                break
            phi, psi, phi_r, psi_r, x = wavelet.wavefun(iterations)
            row *= 2
            
            color = colors.next()
            ax = pylab.subplot(2*rows, 2*cols, 1 + 2*(col + row*cols))
            pylab.title(wavelet.name + " phi")
            pylab.plot(x, phi, color)
            pylab.xlim(min(x), max(x))
    
            ax = pylab.subplot(2*rows, 2*cols, 1 + 2*(col + row*cols) + 1)
            pylab.title(wavelet.name + " psi")
            pylab.plot(x, psi, color)
            pylab.xlim(min(x), max(x))

            row += 1
            ax = pylab.subplot(2*rows, 2*cols, 1 + 2*(col + row*cols))
            pylab.title(wavelet.name + " phi_r")
            pylab.plot(x, phi_r, color)
            pylab.xlim(min(x), max(x))
    
            ax = pylab.subplot(2*rows, 2*cols, 1 + 2*(col + row*cols) + 1)
            pylab.title(wavelet.name + " psi_r")
            pylab.plot(x, psi_r, color)
            pylab.xlim(min(x), max(x))

pylab.show()

