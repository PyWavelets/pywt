.. _ref-iswt:

.. currentmodule:: pywt
.. include:: ../substitutions.rst


Inverse Stationary Wavelet Transform
------------------------------------

Inverse :ref:`stationary wavelet transforms <ref-swt>` are provided for 1D and
2D data.

**Note**: These inverse transforms are not yet optimized for speed and only
support a subset of the forward transform features.  Specifically, there is not
yet a general n-dimensional inverse transform and these routines do not yet
have general ``axis``/``axes`` support.

Multilevel 1D ``iswt``
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: iswt

Multilevel 2D ``iswt2``
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: iswt2
