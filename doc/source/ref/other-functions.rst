.. _ref-other:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

===============
Other functions
===============


Single-level n-dimensional Discrete Wavelet Transform.
------------------------------------------------------

.. autofunction:: dwtn


Integrating wavelet functions
-----------------------------

.. autofunction:: integrate_wavelet

The result of the call depends on the *wavelet* argument:

* for orthogonal and continuous wavelets - an integral of the
  wavelet function specified on an x-grid::

    [int_psi, x_grid] = integrate_wavelet(wavelet, precision)

* for other wavelets - integrals of decomposition and
  reconstruction wavelet functions and a corresponding x-grid::

    [int_psi_d, int_psi_r, x_grid] = integrate_wavelet(wavelet, precision)


Central frequency of *psi* wavelet function
-------------------------------------------

.. autofunction:: central_frequency

.. autofunction:: scale2frequency


Quadrature Mirror Filter
------------------------

.. autofunction:: qmf

Orthogonal Filter Banks
-----------------------

.. autofunction:: orthogonal_filter_bank
