import numpy
import pywt


def rescale_filter_bank(filter_bank, scale):
    return [[int(round(x * scale)) for x in arr] for arr in filter_bank]

wavelet = pywt.Wavelet('db1')

wavelet2 = pywt.Wavelet(name="rescaled db1",
    filter_bank=rescale_filter_bank(wavelet.filter_bank, 10))

data = [1,2,3,4,5,6]
data2 = numpy.array(data, numpy.short)


print "data:", data

a, d = pywt.dwt(data, 'db1')
print "a:", a
print "d:", d
print pywt.idwt(a, d, wavelet)

a, d = pywt.dwt(data2, wavelet2)
print "a:", a
print "d:", d
print pywt.idwt(a, d, wavelet2)

