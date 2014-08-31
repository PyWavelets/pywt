.. _ref-other:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

===============
Other functions
===============


Single-level n-dimensional Discrete Wavelet Transform.
------------------------------------------------------

.. function:: dwtn(data, wavelet[, mode='symmetric'])

   Performs single-level n-dimensional Discrete Wavelet Transform.

   :param data: n-dimensional array
   :param wavelet: |wavelet|
   :param mode: |mode|

   Results are arranged in a dictionary, where key specifies
   the transform type on each dimension and value is a n-dimensional
   coefficients array.
    
   For example, for a 2D case the result will look something like this::

      {
          'aa': <coeffs>  # A(LL) - approx. on 1st dim, approx. on 2nd dim
          'ad': <coeffs>  # H(LH) - approx. on 1st dim, det. on 2nd dim
          'da': <coeffs>  # V(HL) - det. on 1st dim, approx. on 2nd dim
          'dd': <coeffs>  # D(HH) - det. on 1st dim, det. on 2nd dim
      }


Integrating wavelet functions - :func:`integrate_wavelet`
-----------------------------------------------

.. function:: integrate_wavelet(wavelet[, precision=8])

  Integration of wavelet function approximations can be performed
  using the :func:`pywt.integrate_wavelet` function.

  The result of the call depends on the *wavelet* argument:

  * for orthogonal and continuous wavelets - an integral of the
    wavelet function specified on an x-grid::

      [int_psi, x_grid] = integrate_wavelet(wavelet, precision)

  * for other wavelets - integrals of decomposition and
    reconstruction wavelet functions and a corresponding x-grid::

      [int_psi_d, int_psi_r, x_grid] = integrate_wavelet(wavelet, precision)

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet1 = pywt.Wavelet('db2')
    >>> [int_psi, x] = pywt.integrate_wavelet(wavelet1, precision=5)
    >>> wavelet2 = pywt.Wavelet('bior1.3')
    >>> [int_psi_d, int_psi_r, x] = pywt.integrate_wavelet(wavelet2, precision=5)


Central frequency of *psi* wavelet function
-------------------------------------------

.. function:: central_frequency(wavelet[, precision=8])
              central_frequency((function_approx, x))

   :param wavelet: :class:`Wavelet`, wavelet name string or
                   `(wavelet function approx., x grid)` pair

   :param precision:  Precision that will be used for wavelet function
                      approximation computed with the :meth:`Wavelet.wavefun`
                      method.
