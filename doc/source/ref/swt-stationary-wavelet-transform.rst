.. _ref-swt:

.. currentmodule:: pywt

Stationary Wavelet Transform
----------------------------

`Stationary Wavelet Transform (SWT)
<http://en.wikipedia.org/wiki/Stationary_wavelet_transform>`_,
also known as *Undecimated wavelet transform* or *Algorithme à trous* is a translation-invariance modification of the *Discrete Wavelet Transform* that
does not decimate coefficients at every transformation level.

Multilevel 1D ``swt``
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: swt

Multilevel 2D ``swt2``
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: swt2

Multilevel n-dimensional ``swtn``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: swtn

Maximum decomposition level - ``swt_max_level``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: swt_max_level
