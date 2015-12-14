.. _ref-dwt2:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

=================================================
2D Forward and Inverse Discrete Wavelet Transform
=================================================


Single level ``dwt2``
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: dwt2

The relation to the other common data layout where all the approximation and
details coefficients are stored in one big 2D array is as follows:

  ::

                                -------------------
                                |        |        |
                                | cA(LL) | cH(LH) |
                                |        |        |
    (cA, (cH, cV, cD))  <--->   -------------------
                                |        |        |
                                | cV(HL) | cD(HH) |
                                |        |        |
                                -------------------

PyWavelets does not follow this pattern because of pure practical reasons of simple
access to particular type of the output coefficients.


Single level ``idwt2``
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: idwt2

2D multilevel decomposition using ``wavedec2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: wavedec2

2D multilevel reconstruction using ``waverec2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: waverec2
