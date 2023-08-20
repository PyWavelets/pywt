import numpy as np
import pywt
import matplotlib.pyplot as plt

wavlist = pywt.wavelist(kind="continuous")
cols = 4
rows = (len(wavlist) + cols - 1) // cols
fig, axs = plt.subplots(rows, cols, figsize=(10, 10), sharex=True, sharey=True)
for ax, wavelet in zip(axs.flatten(), wavlist):
    [psi, x] = pywt.ContinuousWavelet(wavelet).wavefun(10)
    ax.plot(x, np.real(psi), label="real")
    ax.plot(x, np.imag(psi), label="imag")
    ax.set_title(wavelet)
    ax.set_xlim([-5, 5])
    ax.set_ylim([-0.8, 1])
ax.legend(loc="upper right")
plt.suptitle("Available wavlets for CWT")
plt.tight_layout()
plt.show()
