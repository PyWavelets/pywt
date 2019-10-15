.. _ref-cwt:

.. currentmodule:: pywt

==================================
Continuous Wavelet Transform (CWT)
==================================

This section describes functions used to perform single continuous wavelet
transforms.

Single level - ``cwt``
----------------------

.. autofunction:: cwt


Continuous Wavelet Families
---------------------------

A variety of continuous wavelets have been implemented. A list of the available
wavelet names compatible with ``cwt`` can be obtained by:

.. sourcecode:: python

    wavlist = pywt.wavelist(kind='continuous')


Mexican Hat Wavelet
^^^^^^^^^^^^^^^^^^^
The mexican hat wavelet ``"mexh"`` is given by:

.. math::
    \psi(t) = \frac{2}{\sqrt{3} \sqrt[4]{\pi}} \exp^{-\frac{t^2}{2}}
              \left( 1 - t^2 \right)

where the constant out front is a normalization factor so that the wavelet has
unit energy.


Morlet Wavelet
^^^^^^^^^^^^^^
The Morlet wavelet ``"morl"`` is given by:

.. math::
    \psi(t) = \exp^{-\frac{t^2}{2}} \cos(5t)


Complex Morlet Wavelets
^^^^^^^^^^^^^^^^^^^^^^^

The complex Morlet wavelet (``"cmorB-C"`` with floating point values B, C) is
given by:

.. math::
    \psi(t) = \frac{1}{\sqrt{\pi B}} \exp^{-\frac{t^2}{B}}
              \exp^{\mathrm{j} 2\pi C t}

where :math:`B` is the bandwidth and :math:`C` is the center frequency.


Gaussian Derivative Wavelets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Gaussian wavelets (``"gausP"`` where P is an integer between 1 and and 8)
correspond to the Pth order derivatives of the function:

.. math::
    \psi(t) = C \exp^{-t^2}

where :math:`C` is an order-dependent normalization constant.

Complex Gaussian Derivative Wavelets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The complex Gaussian wavelets (``"cgauP"`` where P is an integer between 1 and
8) correspond to the Pth order derivatives of the function:

.. math::
    \psi(t) = C \exp^{-\mathrm{j} t}\exp^{-t^2}

where :math:`C` is an order-dependent normalization constant.

Shannon Wavelets
^^^^^^^^^^^^^^^^
The Shannon wavelets (``"shanB-C"`` with floating point values B and C)
correspond to the following wavelets:

.. math::
    \psi(t) = \sqrt{B} \frac{\sin(\pi B t)}{\pi B t} \exp^{\mathrm{j}2 \pi C t}

where :math:`B` is the bandwidth and :math:`C` is the center frequency.


Frequency B-Spline Wavelets
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The frequency B-spline wavelets (``"fpspM-B-C"`` with integer M and floating
point B, C) correspond to the following wavelets:

.. math::
    \psi(t) = \sqrt{B}
              \left[\frac{\sin(\pi B \frac{t}{M})}{\pi B \frac{t}{M}}\right]^M
              \exp^{2\mathrm{j} \pi C t}

where :math:`M` is the spline order, :math:`B` is the bandwidth and :math:`C` is
the center frequency.


Choosing the scales for ``cwt``
-------------------------------

For each of the wavelets described below, the implementation in PyWavelets
evaluates the wavelet function for :math:`t` over the range
``[wavelet.lower_bound, wavelet.upper_bound]`` (with default range
:math:`[-8, 8]`). ``scale = 1`` corresponds to the case where the extent of the
wavelet is ``(wavelet.upper_bound - wavelet.lower_bound + 1)`` samples of the
digital signal being analyzed. Larger scales correspond to stretching of the
wavelet. For example, at ``scale=10`` the wavelet is stretched by a factor of
10, making it sensitive to lower frequencies in the signal.

To relate a given scale to a specific signal frequency, the sampling period
of the signal must be known. :func:`pywt.scale2frequency` can be used to
convert a list of scales to their corresponding frequencies. The proper choice
of scales depends on the chosen wavelet, so :func:`pywt.scale2frequency` should
be used to get an idea of an appropriate range for the signal of interest.

For the ``cmor``, ``fbsp`` and ``shan`` wavelets, the user can specify a
specific a normalized center frequency. A value of 1.0 corresponds to 1/dt
where dt is the sampling period. In other words, when analyzing a signal
sampled at 100 Hz, a center frequency of 1.0 corresponds to ~100 Hz at
``scale = 1``. This is above the Nyquist rate of 50 Hz, so for this
particular wavelet, one would analyze a signal using ``scales >= 2``.

.. sourcecode:: python

    >>> import numpy as np
    >>> import pywt
    >>> dt = 0.01  # 100 Hz sampling
    >>> frequencies = pywt.scale2frequency('cmor1.5-1.0', [1, 2, 3, 4]) / dt
    >>> frequencies
    array([ 100.        ,   50.        ,   33.33333333,   25.        ])

The CWT in PyWavelets is applied to discrete data by convolution with samples
of the integral of the wavelet. If ``scale`` is too low, this will result in
a discrete filter that is inadequately sampled leading to aliasing as shown
in the example below. Here the wavelet is ``'cmor1.5-1.0'``. The left column of
the figure shows the discrete filters used in the convolution at various
scales. The right column are the corresponding Fourier power spectra of each
filter.. For scales 1 and 2 it can be seen that aliasing due to violation of
the Nyquist limit occurs.

.. plot:: pyplots/cwt_scaling_demo.py
