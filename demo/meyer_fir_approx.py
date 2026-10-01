# Filterbank Implementation of Meyer’s Wavelet

import numpy as np
from scipy.integrate import quad
from matplotlib import pyplot as plt

import pywt


def beta1(x):
    """A function that transitions from 0 to 1 on the interval [0, 1]."""
    return x


def beta4(x):
    """A function that transitions from 0 to 1 on the interval [0, 1].

    References
    ----------
    .. [1] I. Daubechies. Ten Lectures on Wavelets. SIAM, 1992.
    """
    x2 = x*x
    x4 = x2*x2
    return x4*(35 - 84*x + 70*x2 - 20*x2*x)


def beta5(x):
    """

    References
    ----------
    .. [1] J. Dattorio.  Filterbank Implementation of Meyer’s Wavelet.
        Stanford EE392G, Class Project, June 10, 1998.
    """
    x2 = x*x
    x4 = x2*x2
    return x*x4*(126 - 420*x + 540*x2 - 315*x2*x + 70*x4)


def Phi(w, beta):
    """Meyer scaling function as defined in the frequency domain.

    Parameters
    ----------
    w : float
        frequency (radians)
    beta : function
        A transition function that smoothly increases from 0 to 1 over the
        interval [0, 1].

    Returns
    -------
    p : float
        Phi evaluated at frequency, ``w``.

    Notes
    -----
    See Ch. 7, Eq. 7.89 of [1]_.

    References
    ----------
    .. [1] S. Mallat.  A Wavelet Tour of Singal Processing The Sparse Way,
    3rd. Ed. Elsevier, 2009.
    """
    aw = np.abs(w)
    if aw <= np.pi/3:
        return np.sqrt(2)
    elif aw > 2*np.pi/3:
        return 0
    else:
        return np.sqrt(2) * np.cos(np.pi/2*beta(3*aw/np.pi - 1))


def _Phi_term(w, t, beta):
    # due to even symmetry of Phi(w), the inverse cosine transform can be used
    # rather than the Fourier transform
    # integrate this term from 0 to pi to get the Fourier transform
    return Phi(w, beta) * np.cos(w*t)


def phi(t, beta):
    """Meyer scaling function.

    Parameters
    ----------
    w : float
        frequency (radians)
    beta : function
        A transition function that smoothly increases from 0 to 1 over the
        interval [0, 1].

    Returns
    -------
    p : float
        phi evaluated at time t.

    This is determined numerically via inverse Fourier transform of Phi.
    """
    eps = 1.5e-10
    p = 1 / np.pi * quad(_Phi_term, 0, 2*np.pi/3, args=(t, beta), epsabs=eps,
                         epsrel=eps)[0]
    return p


def meyer_filterbank(N=66, asynchronous=True, transition_func=beta5):
    """Design an FIR filterbank approximation to the Meyer wavelet.

    Parameters
    ----------
    N : int
        The filter length (must be even).
    asynchronous : bool, optional
        Whether to use asynchronous sampling. If True, the Shah function used
        to sample the continuous function is non-zero at half-integer rather
        than integer sampling locations.
    transition_func : function
        The transition function used in the frequency domain definition of the
        Meyer wavelet (see the ``Phi`` docstring).

    Returns
    -------
    filterbank : list of ndarray
        The four filters needed to define a discrete wavelet transform::

        filterbank = [dec_lo, dec_hi, rec_lo, rec_hi].

    Notes
    -----
    The Meyer wavelet is defined over a finite interval in the frequency
    domain and is therefore infinite in extent in the time domain.  Any
    discrete FIR implementation is an approximation.
    """
    if N % 2 != 0:
        raise ValueError("N must be even")
    K = N // 2

    # discrete sampling locations
    n = np.arange(-K, K)
    if asynchronous:
        n = n + 0.5

    # FIR filter corresponding to the scaling function
    dec_lo = np.asarray([phi(t, beta=transition_func) for t in n])
    # dec_lo /= np.sum(dec_lo**2)

    # generate the other filters based on the standard symmetry rules for
    # orthogonal wavelets.
    dec_hi = dec_lo[::-1].copy()
    dec_hi[1::2] *= -1
    rec_lo = dec_lo[::-1]
    rec_hi = dec_hi[::-1]
    return [dec_lo, dec_hi, rec_lo, rec_hi]


# Plot the continuous Meyer scaling function
ws = np.linspace(-np.pi, np.pi, 1000)
P = np.asarray([Phi(w, beta5) for w in ws])
P_shift1 = np.asarray([Phi(w+np.pi, beta5) for w in ws])
P_shift2 = np.asarray([Phi(w-np.pi, beta5) for w in ws])
fig, axes = plt.subplots(1, 3)

axes[0].plot(ws, P)
axes[0].set_xlabel('$\omega$ (rad)')
axes[0].set_title('$\Phi(\omega)$')
axes[1].plot(ws, P, label='$\Phi(\omega)$')
axes[1].plot(ws, P_shift1, label='$\Phi(\omega+\pi)$')
axes[1].plot(ws, P_shift2, label='$\Phi(\omega-\pi)$')
axes[1].plot(ws, P**2 + P_shift1**2 + P_shift2**2, label='sum of squares')
axes[1].legend(loc='upper center')
axes[1].set_ylim([0, 3.5])

# time domain
ts = np.linspace(-40, 40, 1000)
p = np.asarray([phi(t, beta5) for t in ts])

axes[2].plot(ts, p)
axes[2].set_xlabel('t (s)')
axes[2].set_title('$\phi(t)$')

# Generate a Meyer filterbank very similar to Matlab's
dmey_matlab_fb = meyer_filterbank(102, asynchronous=False,
                                  transition_func=beta4)

# Generate a Meyer filterbank as described in J. Dattorio.
# Filterbank Implementation of Meyer’s Wavelet.
# Stanford EE392G, Class Project, June 10, 1998.
dmey_dattorio_fb = meyer_filterbank(66, asynchronous=True,
                                    transition_func=beta5)

dmey_async102_fb = meyer_filterbank(102, asynchronous=True,
                                    transition_func=beta5)

# Plot these two discrete filterbanks
for fb in [dmey_dattorio_fb, dmey_matlab_fb]:
    fig, ((ax00, ax01), (ax10, ax11)) = plt.subplots(
        2, 2, gridspec_kw=dict(hspace=0.35, wspace=0.35))
    ax00.plot(fb[0], 'k.-', markersize=2, linewidth=0.5)
    ax00.set_title('dec_lo (N={})'.format(len(fb[0])))
    ax01.plot(fb[1], 'k.-', markersize=2, linewidth=0.5)
    ax01.set_title('dec_hi (N={})'.format(len(fb[1])))
    ax10.plot(fb[2], 'k.-', markersize=2, linewidth=0.5)
    ax10.set_title('rec_lo (N={})'.format(len(fb[2])))
    ax11.plot(fb[3], 'k.-', markersize=2, linewidth=0.5)
    ax11.set_title('rec_hi (N={})'.format(len(fb[3])))

# create Wavelets corresponding to these filterbanks
w102 = pywt.Wavelet('dmey102', filter_bank=dmey_matlab_fb)
w102b = pywt.Wavelet('dmey102b', filter_bank=dmey_async102_fb)
w66 = pywt.Wavelet('dmey66', filter_bank=dmey_dattorio_fb)

cam = pywt.data.camera().astype(np.float64)

w = pywt.Wavelet('dmey')
c = pywt.wavedecn(cam, wavelet=w)
r = pywt.waverecn(c, wavelet=w)
print("Error (pywt dmey) = {}".format(
    np.linalg.norm(cam-r)/np.linalg.norm(cam)))

c = pywt.wavedecn(cam, wavelet=w102, level=2)
r = pywt.waverecn(c, wavelet=w102)
print("Error (dmey102) = {}".format(
    np.linalg.norm(cam-r)/np.linalg.norm(cam)))

c = pywt.wavedecn(cam, wavelet=w66, level=2)
r = pywt.waverecn(c, wavelet=w66)
print("Error (dmey66_async) = {}".format(
    np.linalg.norm(cam-r)/np.linalg.norm(cam)))

c = pywt.wavedecn(cam, wavelet=w102b, level=2)
r = pywt.waverecn(c, wavelet=w102b)
print("Error (dmey102_async) = {}".format(
    np.linalg.norm(cam-r)/np.linalg.norm(cam)))

plt.show()
