
Overview of multilevel wavelet decompositions
=============================================

There are a number of different ways a wavelet decomposition can be performed
for multiresolution analysis of n-dimensional data. Here we will review the
three approaches currently implemented in PyWavelets. 2D cases are
illustrated, but each of the approaches extends to the n-dimensional case in a
straightforward manner.


Multilevel Discrete Wavelet Transform
-------------------------------------

The most common approach to the multilevel discrete wavelet transform involves
further decomposition of only the approximation subband at each subsequent
level. This is also sometimes referred to as the Mallat decomposition
[Mall89]_. In 2D, the discrete wavelet transform produces four sets of
coefficients corresponding to the four possible compinations of the wavelet
decomposition filters over the two separate axes. (In n-dimensions, there
are ``2**n`` sets of coefficients). For subsequent levels of decomposition,
only the approximation coefficients (the lowpass subband) are further
decomposed.

In PyWavelets, this decomposition is implemented for n-dimensional data by
:func:`~pywt.wavedecn` and the inverse by :func:`~pywt.waverecn`. 1D and 2D
versions of these routines also exist. It is illustrated in the figure below.
The top row indicates the coefficient names as used by :func:`~pywt.wavedec2`
after each level of decomposition. The bottom row shows wavelet coefficients
for the camerman image (with each subband independently normalized for easier
visualization).

.. plot:: pyplots/plot_mallat_2d.py

It can be seen that many of the coefficients are near zero (gray). This ability
of the wavelet transform to sparsely represent natural images is a key
property that makes it desirable in applications such as image compression and
restoration.

Fully Seperable Discrete Wavelet Transform
------------------------------------------
An alternative decomposition results in first fully decomposing one axis of the
data prior to moving onto each additional axis in turn. This is illustrated
for the 2D case in the upper right panel of the figure below. This approach has
a factor of two higher computational cost as compared to the Mallat approach,
but has advantages in compactly representing anisotropic data. A demo of this
is `available <https://github.com/PyWavelets/pywt/tree/master/demo/fswavedecn_mondrian.py>`_).

This form of the DWT is also sometimes referred to as the tensor wavelet
transform or the hyperbolic wavelet transform. In PyWavelets it is implemented
for n-dimensional data by :func:`~pywt.fswavedecn` and the inverse by
:func:`~pywt.fswaverecn`.

Wavelet Packet Transform
------------------------

Another possible choice is to apply additional levels of decomposition to all
wavelet subbands from the first level as opposed to only the approximation
subband. This is known as the wavelet packet transform and is illustrated in
2D in the lower left panel of the figure. It is also possible to only perform
any subset of the decompositions, resulting in a wide number of potential
wavelet packet bases. An arbitrary example is shown in the lower right panel
of the figure below.

A further description is available in the
:ref:`wavelet packet documentation<ref-wp>`.

For the wavelet packets, the plots below use "natural" ordering for simplicity,
but this does not directly match the "frequency" ordering for these wavelet
packets. It is possible to rearrange the coefficients into frequency ordering
(see the ``get_level`` method of :class:`~pywt.WaveletPacket2D` and [Wick94]_
for more details).

.. plot:: pyplots/plot_2d_bases.py


.. rubric:: References

.. [Mall89] Mallat, S.G. "A Theory for Multiresolution Signal Decomposition: The Wavelet Representation" IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 2, no. 7. July 1989. DOI: 10.1109/34.192463

.. [Wick94] Wickerhauser, M.V. "Adapted Wavelet Analysis from Theory to Software" Wellesley. Massachusetts: A K Peters. 1994.
