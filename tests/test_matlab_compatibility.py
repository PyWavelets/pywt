#!/usr/bin/env python

"""
Test used to verify PyWavelets Discrete Wavelet Transform computation
accuracy against MathWorks Wavelet Toolbox.

This way you can be perfectly sure about PyWavelets' results quality
and reproducibility.
"""

try:
    from mlabwrap import mlab 
except:
    print "To run this test you need to have MathWorks MATLAB, MathWorks " \
           "Wavelet Toolbox and mlabwrap Python extension installed."
    raise SystemExit
    
import math
import numpy
import pywt
from numpy import asarray, float64

def mse(ar1, ar2):
    """Mean squared error"""
    ar1 = asarray(ar1, dtype=float64)
    ar2 = asarray(ar2, dtype=float64)
    dif = ar1 - ar2
    dif *= dif
    return dif.sum()/len(ar1)

def rms(ar1, ar2):
    """Root mean squared error"""
    return math.sqrt(mse(ar1, ar2))

def test_accuracy(families, wavelets, modes, epsilon=1.0e-10):
    print "Testing decomposition".upper()
    
    for pmode, mmode in modes:
        for wavelet in wavelets:
            print "Wavelet: %-8s Mode: %s" % (wavelet, pmode)
        
            w = pywt.Wavelet(wavelet)
            data_size = range(w.dec_len, 40) + [100, 200, 500, 1000, 50000]
            
            for N in data_size:
                data = numpy.random.random(N)
                
                # PyWavelets result
                pa, pd = pywt.dwt(data, wavelet, pmode)
                
                # Matlab result
                ma, md = mlab.dwt(data, wavelet, 'mode', mmode, nout=2)
                ma = ma.flat; md = md.flat

                # calculate error measures
                mse_a, mse_d = mse(pa, ma), mse(pd, md)
                rms_a, rms_d = math.sqrt(mse_a), math.sqrt(mse_d)

                if rms_a > epsilon:
                    print '[RMS_A > EPSILON] for Mode: %s, Wavelet: %s, Length: %d, rms=%.3g' % (pmode, wavelet, len(data), rms_a)
                    
                if rms_d > epsilon:
                    print '[RMS_D > EPSILON] for Mode: %s, Wavelet: %s, Length: %d, rms=%.3g' % (pmode, wavelet, len(data), rms_d)


if __name__ == '__main__':

    families = ('db', 'sym', 'coif', 'bior', 'rbio')
    wavelets = sum([pywt.wavelist(name) for name in families], [])
    # list of mode names in pywt and matalb
    modes = [('zpd', 'zpd'), ('cpd', 'sp0'), ('sym', 'sym'),
             ('ppd', 'ppd'), ('sp1', 'sp1'), ('per', 'per')] 
    # max RMSE
    epsilon = 1.0e-10
    
    test_accuracy(families, wavelets, modes, epsilon)
