.. _ref-cwt:

.. currentmodule:: pywt

==================================
Continuous Wavelet Transform (CWT)
==================================

This section focuses on the one-dimensional Continuous Wavelet Transform. It
introduces the main function ``cwt`` alongside several helper function, and
also gives an overview over the available wavelets for this transfom.

.. note::

    ``cwt`` and related functions in PyWavelets have some known issues;
    you may be interested in trying the ``cwt`` implementation in
    `ssqueezepy <https://pypi.org/project/ssqueezepy/>`__,
    which is substantially faster and may also be more accurate.


Introduction
------------

In simple terms, the Continuous Wavelet Transform is an analysis tool similar
to the Fourier Transform, in that it takes a time-domain signal and returns
the signal's components in the frequency domain. However, in contrast to the
Fourier Transform, the Continuous Wavelet Transform returns a two-dimensional
result, providing information in the frequency- as well as in time-domain.
Therefore, it is useful for periodic signals which change over time, such as
audio, seismic signals and many others (see below for examples).

For more background and an in-depth guide to the application of the Continuous
Wavelet Transform, including topics such as statistical significance, the
following well-known article is highly recommended:

`C. Torrence and G. Compo: "A Practical Guide to Wavelet Analysis", Bulletin of the American Meteorological Society, vol. 79, no. 1, pp. 61-78, January 1998 <https://paos.colorado.edu/research/wavelets/bams_79_01_0061.pdf>`_


The ``cwt`` Function
----------------------

This is the main function, which calculates the Continuous Wavelet Transform
of a one-dimensional signal.

.. autofunction:: cwt

A comprehensive example of the CWT
----------------------------------

Here is a simple end-to-end example of how to calculate the CWT of a simple
signal, and how to plot it using ``matplotlib``.

First, we generate an artificial signal to be analyzed. We are
using the sum of two sine functions with increasing frequency, known as "chirp".
For reference, we also generate a plot of the signal and the two time-dependent
frequency components it contains.

We then apply the Continuous Wavelet Transform
using a complex Morlet wavlet with a given center frequency and bandwidth
(namely ``cmor1.5-1.0``). We then plot the so-called "scaleogram", which is the
2D plot of the signal strength vs. time and frequency.

.. plot:: pyplots/plot_cwt_scaleogram.py

The Continuous Wavelet Transform can resolve the two frequency components clearly,
which is an obvious advantage over the Fourier Transform in this case. The scales
(widths) are given on a logarithmic scale in the example. The scales determine the
frequency resolution of the scaleogram. However, it is not straightforward to
convert them to frequencies, but luckily, ``cwt`` calculates the correct frequencies
for us. There are also helper functions, that perform this conversion in both ways.
For more information, see :ref:`Choosing scales` and :ref:`Converting frequency`.

Also note, that the raw output of ``cwt`` is complex if a complex wavelet is used.
For visualization, it is therefore necessary to use the absolute value.


Wavelet bandwidth and center frequencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example shows how the Complex Morlet Wavelet can be configured for optimum
results using the ``center_frequency`` and ``bandwidth_frequency`` parameters,
which can simply be appended to the wavelet's string identifier ``cmor`` for
convenience. It also demonstrates the importance of choosing appropriate values
for the wavelet's center frequency and bandwidth. The right values will depend
on the signal being analyzed. As shown below, bad values may lead to poor
resolution or artifacts.

.. plot:: pyplots/cwt_wavelet_frequency_bandwidth_demo.py
.. Sphinx seems to take a long time to generate this plot, even though the
.. corresponding script is relatively fast when run on its own.


Continuous Wavelet Families
---------------------------

A variety of continuous wavelets have been implemented. A list of the available
wavelet names compatible with ``cwt`` can be obtained by:

.. try_examples::

  >>> import pywt
  >>> wavelist = pywt.wavelist(kind='continuous')

Here is an overview of all available wavelets for ``cwt``. Note, that they can be
customized by passing parameters such as ``center_frequency`` and ``bandwidth_frequency``
(see :ref:`ContinuousWavelet` for details).

.. plot:: pyplots/plot_wavelets.py


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
The frequency B-spline wavelets (``"fbspM-B-C"`` with integer M and floating
point B, C) correspond to the following wavelets:

.. math::
    \psi(t) = \sqrt{B}
              \left[\frac{\sin(\pi B \frac{t}{M})}{\pi B \frac{t}{M}}\right]^M
              \exp^{2\mathrm{j} \pi C t}

where :math:`M` is the spline order, :math:`B` is the bandwidth and :math:`C` is
the center frequency.


.. _Choosing scales:

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

.. try_examples::

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

.. _Converting frequency:

Converting frequency to scale for ``cwt``
-----------------------------------------

To convert frequency to scale for use in the wavelet transform the function
:func:`pywt.frequency2scale` can be used. This is the complement of the
:func:`pywt.scale2frequency` function as seen in the previous section. Note that
the input frequency in this function is normalized by 1/dt, or the sampling
frequency fs. This function is useful for specifying the transform as a function
of frequency directly.

.. try_examples::

  >>> import numpy as np
  >>> import pywt
  >>> dt = 0.01  # 100 Hz sampling
  >>> fs = 1 / dt
  >>> frequencies = np.array([100, 50, 33.33333333, 25]) / fs # normalize
  >>> scale = pywt.frequency2scale('cmor1.5-1.0', frequencies)
  >>> scale
  array([ 1.,  2.,  3.,  4.])


.. plot:: pyplots/cwt_scaling_demo.py


.. _CWT normalization:

Normalization of the CWT coefficients
-------------------------------------

``cwt`` works entirely in units of samples. Writing :math:`x[n]` for the input
signal and taking both the scale :math:`a` and the translation :math:`b` to be
expressed in samples, the returned coefficients are

.. math::

    C[a, b] = \frac{1}{\sqrt{a}}\sum_n x[n]\,
              \psi^*\!\left(\frac{n - b}{a}\right).

No sampling interval appears in this expression. In particular, the
``sampling_period`` argument of :func:`pywt.cwt` rescales only the returned
``frequencies``; the coefficients themselves do not depend on it.

Relation to the continuous-time transform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The continuous-time definition of the CWT, with a scale :math:`a_s` and a
translation :math:`b_s` in seconds, is

.. math::

    W_x(a_s, b_s) = \frac{1}{\sqrt{a_s}}
        \int x(t)\,\psi^*\!\left(\frac{t - b_s}{a_s}\right)\,\mathrm{d}t.

For data sampled at :math:`t_n = n\,\mathrm{d}t`, approximating that integral by
a Riemann sum introduces a factor :math:`\mathrm{d}t`. Substituting
:math:`a_s = a\,\mathrm{d}t` and :math:`b_s = b\,\mathrm{d}t` then gives

.. math::

    W_x(a_s, b_s) \approx \frac{\mathrm{d}t}{\sqrt{a\,\mathrm{d}t}}
        \sum_n x[n]\,\psi^*\!\left(\frac{n - b}{a}\right)
        = \sqrt{\mathrm{d}t}\, C[a, b].

So the coefficients returned by ``cwt`` have to be **multiplied** by
:math:`\sqrt{\mathrm{d}t}` (equivalently, divided by :math:`\sqrt{f_s}`) to be
expressed in physical-time units. PyWavelets does not apply that factor,
because doing so would make the coefficients depend on ``sampling_period``.

A common source of confusion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A frequent mistake when comparing a hand-written convolution against ``cwt`` is
to *mix* the two conventions above: to use a scale in seconds,
:math:`a_s = a\,\mathrm{d}t`, in the :math:`1/\sqrt{a_s}` prefactor, while
summing over raw samples without the :math:`\mathrm{d}t` coming from the
integral. Such a result is too large by a factor
:math:`1/\sqrt{\mathrm{d}t} = \sqrt{f_s}`, and an otherwise unexplained factor
:math:`1/\sqrt{f_s}` then has to be inserted by hand to make the amplitudes
agree with ``cwt``. Either keep everything in samples, as :math:`C[a, b]` does,
or write out the full Riemann sum including :math:`\mathrm{d}t` — but do not
combine the two.

The example below evaluates :math:`C[a, b]` directly and compares it to
``cwt``:

.. try_examples::

  >>> import numpy as np
  >>> import pywt
  >>> fs = 3000.0  # sampling rate in Hz
  >>> t = np.arange(3000) / fs
  >>> x = np.sin(2 * np.pi * 40 * t)
  >>> wavelet = pywt.ContinuousWavelet('cmor14-2')
  >>> a = pywt.frequency2scale(wavelet, 40 / fs)  # scale, in samples
  >>> coefs, freqs = pywt.cwt(x, a, wavelet, sampling_period=1 / fs)

  Now the same transform, written out as a convolution over samples. ``Fb`` and
  ``Fc`` are the bandwidth and center frequency of ``'cmor14-2'``:

  >>> Fb, Fc = 14.0, 2.0
  >>> lb, ub = wavelet.lower_bound, wavelet.upper_bound
  >>> k = np.arange(int(a * (ub - lb)) + 1)
  >>> u = lb + (k + 0.5) / a
  >>> psi = np.exp(2j*np.pi*Fc*u) * np.exp(-u**2 / Fb) / np.sqrt(np.pi * Fb)
  >>> conv = np.convolve(x, np.conj(psi)[::-1]) / np.sqrt(a)
  >>> trim = (conv.size - x.size) // 2
  >>> manual = conv[trim:trim + x.size]
  >>> rel = np.max(np.abs(manual - coefs[0])) / np.max(np.abs(coefs[0]))
  >>> bool(rel < 1e-3)
  True

Note that :math:`\psi` is conjugated *and* reversed before the convolution, and
that it is evaluated at bin midpoints, ``(k + 0.5) / a``. The half-sample offset
is there because ``cwt`` convolves with the integral of :math:`\psi` and then
differences the result, which effectively averages :math:`\psi` over each
sample bin rather than sampling it pointwise.

Limits of the agreement
~~~~~~~~~~~~~~~~~~~~~~~

:math:`C[a, b]` is what ``cwt`` computes in the limit of a finely sampled
wavelet. Two discretization effects prevent an analytic implementation from
reproducing it exactly:

* :math:`\psi` is only evaluated over
  ``[wavelet.lower_bound, wavelet.upper_bound]``, so its tails are truncated
  (see :ref:`Choosing scales`). With the default bounds of :math:`[-8, 8]`,
  ``cmor14-2`` still retains about 1% of its peak amplitude at the edges, and
  that truncation dominates the residual in the example above.
* ``cwt`` resamples the precomputed integral of :math:`\psi` onto the grid for a
  given scale by truncated indexing rather than by interpolation. The resulting
  jitter grows with the scale and is reduced by raising ``precision``; it is the
  "zipper-like" effect mentioned in the ``precision`` documentation of
  :func:`pywt.cwt`. It largely averages out for narrowband signals such as the
  one above, but is clearly visible for broadband input.

Finally, note that the amplitude of the wavelets themselves does not follow a
single convention across families — ``mexh`` and ``gaus`` are normalized to unit
energy, ``morl`` carries no normalization constant at all, and ``cmor``,
``shan`` and ``fbsp`` use yet other conventions (see the formulas above). CWT
coefficient magnitudes are therefore not directly comparable between wavelet
families.
