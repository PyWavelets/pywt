import sys, os.path
import pywt
import pylab

usage = """Usage:\n %s wavelet [refinement level]""" % os.path.basename(sys.argv[0])

try:
    wavelet = pywt.Wavelet(sys.argv[1])
    try:
        level = int(sys.argv[2])
    except IndexError, e:
        level = 10
except ValueError, e:
    print "Unknown wavelet"
    raise SystemExit
except IndexError, e:
    print usage
    raise SystemExit

print wavelet

data = wavelet.wavefun(level)
funcs, x = data[:-1], data[-1]

n = (len(data)-1) // 2
labels = ("scaling function (phi)", "wavelet function (psi)", "r. scaling function (phi)", "r. wavelet function (psi)")
colours = ("r", "g", "r", "g")
for i, (d, label, colour) in enumerate(zip(funcs, labels, colours)):
    mi, ma = d.min(), d.max()
    margin = (ma - mi)*0.05
    ax = pylab.subplot(n, 2, 1+i)
    
    pylab.plot(x, d, colour)
    pylab.title(label)
    pylab.ylim(mi-margin, ma+margin)
    pylab.xlim(x[0], x[-1])
    
pylab.show()
