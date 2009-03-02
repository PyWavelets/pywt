import pywt, numpy, pylab, time
import sample_data

interpolation = 'nearest' #'bilinear'
cmap = pylab.cm.jet

absolute_values = 0
normalize = 0

scales = range(4, 129, 2)
sample = 1

if sample == 1:
    x = numpy.linspace(-300, 1300, 1024*1)
    data = 2*numpy.sin(2*numpy.pi/4 * x) * numpy.exp(-(x-400)**2/(2*300**2)) + \
           numpy.sin(2*numpy.pi/32*x) * numpy.exp(-(x-700)**2/(2*100**2)) + \
           numpy.sin(2*numpy.pi/32 * (x/(1+x/1000)) )
elif sample == 2:
    data = sample_data.cuspamax
    data = data
    x = range(len(data))
elif sample == 3:
    data = sample_data.linchirp
    x = range(len(data))
elif sample == 4:
    data = sample_data.ecg
    x = range(len(data))

wavelets = ['db1', 'sym5', 'coif3', 'bior1.5', 'bior3.3', 'bior4.4'][:2]
#, pywt.cwt.morlet(len(data)), pywt.cwt.mexican_hat(len(data))]#[:4]#[-1:]
wavelets = [pywt.cwt.cmorlet(len(data)/4, 1.0, 1.0),
            pywt.cwt.cmorlet(len(data)/4, 4.0, 1.0),
            pywt.cwt.cmorlet(len(data)/4, 1.0, 4.0)]#, pywt.cwt.gauss1(len(data))] #, 'coif3', 'bior1.5', 'bior3.3', 'bior4.4', pywt.cwt.morlet(len(data)), pywt.cwt.mexican_hat(len(data))]#[:4]#[-1:]
#wavelets = [pywt.cwt.morlet(len(data)), pywt.cwt.mexican_hat(len(data)), pywt.cwt.gauss1(len(data)), pywt.cwt.gauss2(len(data)), pywt.cwt.gauss3(len(data))]
#wavelets = ['cmorlet2-2', 'cmorlet1-1']
#wavelets = ['mexican_hat', 'cmorlet2-2', 'cmorlet1-1']
#wavelets = ['cfbsp4-0.7-1', pywt.cwt.cfbsp(len(data), 4, 0.7, 1)]#, 'cmorlet1-1']
#wavelets = [pywt.cwt.cmorlet(2**8, 2, 2)]

for name in ['mexican_hat', 'morlet', 'gauss1', 'gauss2', 'gauss3', 'cfbsp1-1-1', 'cmorlet1-1', 'cshannon1-1']:
    print name,
    t = time.clock()
    #pywt.cwt.CWavelet(name).wavefun(19)
    print time.clock() - t

#p,x = pywt.cwt.CWavelet('cfbsp1-1-1').wavefun()
#pylab.plot(x,p.real)
#pylab.plot(x,p.imag)
#pylab.show()


for wavelet in wavelets:
    #print wavelet
    pylab.figure()
    pylab.subplot(3,1,1)
    t = time.clock()
    print len(data), len(scales)
    c = pywt.cwt.cwt(data, wavelet=wavelet, scales=scales, data_step=x[1]-x[0], precision=16)
    print "%.4f" % (time.clock()-t)

    if absolute_values:
        c = numpy.abs(numpy.asarray(c).real)
    if normalize:
        for y in c:
            y *= 1.0 / max(abs(y.max()), abs(y.min()))

    c = numpy.asarray(c).real
    pylab.imshow(c, origin='image', interpolation=interpolation, aspect='auto', cmap=cmap)
    pylab.subplot(3,1,2)
    pylab.plot(x, data)
    pylab.xlim(x[0], x[-1])

    pylab.subplot(3,1,3)
    for i in [j for j in (4, 16, 32, 64, 128) if j <= max(scales) and j in scales]:
        pylab.plot(x, c[scales.index(i)], label= ("scale a = %d" % i))
    pylab.legend()
    pylab.xlim(x[0], x[-1])
pylab.show()

