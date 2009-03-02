import pywt, numpy
#, pylab, time
import sample_data

#interpolation = 'nearest' #'bilinear'
#cmap = pylab.cm.jet

from pywt.functions import centfrq, orthfilt
print centfrq('db1', 8)
print centfrq('db2', 8)
print centfrq(pywt.cwt.morlet(256))
print centfrq(pywt.cwt.mexican_hat(256))
#print pywt.cwt.mexican_hat(256)[0]

import pylab
pylab.plot(*pywt.cwt.cgauss1(256)[::-1])
pylab.show()

#for i in pywt.wavelist():
#    print "%s = %s" % (i.replace('.', '_'), centfrq(i, 8))


#print orthfilt([1,2,3,4,5,6])
