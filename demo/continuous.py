import pywt
import pywt.cwt as c
import pylab

psi, x = c.mexican_hat(1000)
pylab.plot(x, psi)
pylab.show()
