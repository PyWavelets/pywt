#!/usr/bin/env python

import matplotlib.pyplot as plt

import pywt
import pywt.data

camera = pywt.data.camera()

wavelet = pywt.Wavelet('sym2')
level = 5
# Note: Running with transform="dwtn" is faster, but the resulting images will
#       look substantially worse.
coeffs = pywt.mran(camera, wavelet=wavelet, level=level, transform='swtn')
ca = coeffs[0]
details = coeffs[1:]

# Plot all coefficient subbands and the original
gridspec_kw = dict(hspace=0.1, wspace=0.1)
fontdict = dict(verticalalignment='center', horizontalalignment='center',
                color='k')
fig, axes = plt.subplots(len(details) + 1, 3, figsize=[5, 8], sharex=True,
                         sharey=True, gridspec_kw=gridspec_kw)
imshow_kw = dict(interpolation='nearest', cmap=plt.cm.gray)
for i, x in enumerate(details):
    axes[i][0].imshow(details[-i - 1]['ad'], **imshow_kw)

    axes[i][1].imshow(details[-i - 1]['da'], **imshow_kw)
    axes[i][2].imshow(details[-i - 1]['dd'], **imshow_kw)
    axes[i][0].text(256, 50, 'ad%d' % (i + 1), fontdict=fontdict)
    axes[i][1].text(256, 50, 'da%d' % (i + 1), fontdict=fontdict)
    axes[i][2].text(256, 50, 'dd%d' % (i + 1), fontdict=fontdict)

axes[-1][0].imshow(ca, **imshow_kw)
axes[-1][0].text(256, 50, 'approx.', fontdict=fontdict)
axes[-1][1].imshow(camera, **imshow_kw)
axes[-1][1].text(256, 50, 'original', fontdict=fontdict)

for ax in axes.ravel():
    ax.set_axis_off()
