#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pywt
import pylab
import itertools

for family in ('db', 'sym'):

    f = pylab.figure()
    f.subplots_adjust(hspace=0.2, wspace=0.04, bottom=.02, left=.06, right=.97, top=.94)
    
    
    colors = itertools.cycle('bgrcmyk')
    iterations = 5
    wnames = pywt.wavelist(family)
    rows, cols = (4, 3)
    i = iter(wnames)
    for col in xrange(cols):
        for row in xrange(rows):
            wavelet = pywt.Wavelet(i.next())
            phi, psi = wavelet.wavefun(iterations)
    
            color = colors.next()
            ax = pylab.subplot(rows, 2*cols, 1 + 2*(col + row*cols))
            pylab.title(wavelet.name + " phi")
            pylab.plot(phi, color)
            pylab.ylim(-1.74, 1.74)
            pylab.xlim(0, len(phi)-1)
            pylab.setp(ax.get_xticklabels(), visible=False)
            if col > 0:
                pylab.setp(ax.get_yticklabels(), visible=False) 
    
            ax = pylab.subplot(rows, 2*cols, 1 + 2*(col + row*cols) + 1)
            pylab.title(wavelet.name + " psi")
            pylab.plot(psi, color)
            pylab.ylim(-1.74, 1.74)
            pylab.xlim(0, len(psi)-1)
            pylab.setp(ax.get_xticklabels(), visible=False)
            pylab.setp(ax.get_yticklabels(), visible=False) 

pylab.show()

