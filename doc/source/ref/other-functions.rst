.. _ref-other:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

===============
Other functions
===============


Single-level n-dimensional Discrete Wavelet Transform.
------------------------------------------------------

.. function:: dwtn(data, wavelet[, mode='sym'])

   Performs single-level n-dimensional Discrete Wavelet Transform.

   :param data: n-dimensional array
   :param wavelet: wavelet to use (Wavelet object or name string)
   :param mode: signal extension mode, see MODES

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


Integrating wavelet functions - :func:`intwave`
-----------------------------------------------

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
    >>> [int_psi_d, int_psi_r, x] = pywt.intwave(wavelet2, precision=5)


Central frequency of *psi* wavelet function
-------------------------------------------

.. function:: centfrq(wavelet[, precision=8])
              centfrq((function_aprox, x))

   :param wavelet: :class:`Wavelet`, wavelet name string or
                   `(wavelet function approx., x grid)` pair

   :param precision:  Precision that will be used for wavelet function
                      approximation computed with the :meth:`Wavelet.wavefun`
                      method.
