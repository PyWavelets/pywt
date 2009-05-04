.. _ref-other:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

===============
Other functions
===============

Integrating wavelet functions - ``intwave()``
---------------------------------------------

  .. function:: intwave(wavelet[, precision=8])

  Integration of wavelet function approximations as well as any other signals
  can be performed using the :func:`pywt.intwave` function.

  The result of the call depends on the *wavelet* argument:

  * for orthogonal wavelets - an integral of the wavelet function specified
    on an x-grid::

      [int_psi, x] = intwave(wavelet, precision)

  * for other wavelets - integrals of decomposition and reconstruction
    wavelet functions and a corresponding x-grid::

      [int_psi_d, int_psi_r, x] = intwave(wavelet, precision)

  * for a tuple of coefficients data and a x-grid - an integral of function
    and the given x-grid is returned (the x-grid is used for computations).::

      [int_function, x] = intwave((data, x), precision)


  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet1 = pywt.Wavelet('db2')
    >>> [int_psi, x] = pywt.intwave(wavelet1, precision=5)
    >>> wavelet2 = pywt.Wavelet('bior1.3')
    >>> [int_psi_d, int_psi_r, x] = pywt.intwave(wavelet, precision=5)
