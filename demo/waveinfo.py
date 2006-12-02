import sys, os.path
import pywt
import pylab

usage = """Usage:\n %s wavelet [refinement level]""" % os.path.basename(sys.argv[0])

try:
    wavelet = pywt.Wavelet(sys.argv[1])
    try:
        level = int(sys.argv[2])
    except IndexError, e:
        level = 5
except ValueError, e:
    print "Unknown wavelet"
    raise SystemExit
except IndexError, e:
    print usage
    raise SystemExit

print wavelet

data = wavelet.wavefun(level)

y = len(data) // 2

labels = ("wavelet function", "scaling function", "r. wavelet function", "r. scaling function")

for i, (d, label) in enumerate(zip(data, labels)):
    mi, ma = d.min(), d.max()
    margin = (ma - mi)*0.05
    ax = pylab.subplot(y, 2, 1+i)
    
    pylab.plot(d)
    pylab.title(label)
    pylab.ylim(mi-margin, ma+margin)
    pylab.xlim(0, len(d)-1)
    pylab.setp(ax.get_xticklabels(), visible=False)
    
pylab.show()
