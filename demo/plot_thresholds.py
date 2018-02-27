import numpy as np
import matplotlib.pyplot as plt
import pywt

s = np.linspace(-4, 4, 1000)

s_soft = pywt.threshold(s, value=0.5, mode='soft')
s_hard = pywt.threshold(s, value=0.5, mode='hard')
s_garotte = pywt.threshold(s, value=0.5, mode='garotte')
s_firm1 = pywt.threshold_firm(s, value_low=0.5, value_high=1)
s_firm2 = pywt.threshold_firm(s, value_low=0.5, value_high=2)
s_firm3 = pywt.threshold_firm(s, value_low=0.5, value_high=4)

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(s, s_soft)
ax[0].plot(s, s_hard)
ax[0].plot(s, s_garotte)
ax[0].legend(['soft (0.5)', 'hard (0.5)', 'non-neg. garotte (0.5)'])
ax[0].set_xlabel('input value')
ax[0].set_ylabel('thresholded value')

ax[1].plot(s, s_soft)
ax[1].plot(s, s_hard)
ax[1].plot(s, s_firm1)
ax[1].plot(s, s_firm2)
ax[1].plot(s, s_firm3)
ax[1].legend(['soft (0.5)', 'hard (0.5)', 'firm(0.5, 1)', 'firm(0.5, 2)',
              'firm(0.5, 4)'])
ax[1].set_xlabel('input value')
ax[1].set_ylabel('thresholded value')
plt.show()
