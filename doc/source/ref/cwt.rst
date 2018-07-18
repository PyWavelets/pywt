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

where :math:`B` is the bandwith and :math:`C` is the center frequency.


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

where :math:`B` is the bandwith and :math:`C` is the center frequency.


Freuqency B-Spline Wavelets
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The frequency B-spline wavelets (``"fpspM-B-C"`` with integer M and floating
point B, C) correspond to the following wavelets:

.. math::
    \psi(t) = \sqrt{B}
              \left[\frac{\sin(\pi B \frac{t}{M})}{\pi B \frac{t}{M}}\right]^M
              \exp^{2\mathrm{j} \pi C t}

where :math:`M` is the spline order, :math:`B` is the bandwith and :math:`C` is
the center frequency.

