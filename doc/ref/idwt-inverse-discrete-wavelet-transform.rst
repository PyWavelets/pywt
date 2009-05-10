.. _ref-idwt:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

=========================================
Inverse Discrete Wavelet Transform (IDWT)
=========================================


Single level ``idwt``
---------------------

.. function:: idwt(cA, cD, wavelet[, mode='sym'[, correct_size=0]])

  The :func:`idwt` function reconstructs data from the given coefficients by
  performing single level Inverse Discrete Wavelet Transform.

  :param cA: Approximation coefficients.

  :param cD: Detail coefficients.

  :param wavelet: |wavelet_arg|

  :param mode: |mode| This is only important when DWT was performed in
               :ref:`periodization <MODES.per>` mode.

  :param correct_size: Typically, *cA* and *cD* coefficients lists must have
                       equal lengths in order to perform IDWT. Setting
                       *correct_size* to `True` allows *cA* to be greater in
                       size by one element compared to the *cD* size. This
                       option is very useful when doing multilevel decomposition
                       and reconstruction (as for example with the
                       :func:`wavedec` function) of non-dyadic length signals
                       when such minor differences can occur at various levels
                       of IDWT.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> print pywt.idwt(cA, cD, 'db2', 'sp1')
    [ 1.  2.  3.  4.  5.  6.]

  One of the neat features of :func:`idwt` is that one of the *cA* and *cD*
  arguments can be set to ``None``. In that situation the reconstruction will be
  performed using only the other one. Mathematically speaking, this is
  equivalent to passing a zero-filled array as one of the arguments.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> A = pywt.idwt(cA, None, 'db2', 'sp1')
    >>> D = pywt.idwt(None, cD, 'db2', 'sp1')
    >>> print A + D
    [ 1.  2.  3.  4.  5.  6.]



Multilevel reconstruction using ``waverec``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: waverec(coeffs, wavelet[, mode='sym'])

  Performs multilevel reconstruction of signal from the given list of
  coefficients.

  :param coeffs: Coefficients list must be in the form like returned by :func:`wavedec` decomposition function, which is::

      [cAn, cDn, cDn-1, ..., cD2, cD1]

  :param wavelet: |wavelet_arg|

  :param mode: |mode|

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db2', level=2)
    >>> print pywt.waverec(coeffs, 'db2')
    [ 1.  2.  3.  4.  5.  6.  7.  8.]


Direct reconstruction with ``upcoef``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: upcoef(part, coeffs, wavelet[, level=1[, take=0]])

  Direct reconstruction from coefficients.

  :param part: Defines the input coefficients type:
  
      - **'a'** - approximations reconstruction is performed
      - **'d'** - details reconstruction is performed

  :param coeffs: Coefficients array to reconstruct.

  :param wavelet: |wavelet_arg|

  :param level: If *level* value is specified then a multilevel reconstruction is
                performed (first reconstruction is of type specified by *part*
                and all the following ones with *part* type ``a``)

  :param take: If *take* is specified then only the central part of length equal
               to the *take* parameter value is returned.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> data = [1,2,3,4,5,6]
    >>> (cA, cD) = pywt.dwt(data, 'db2', 'sp1')
    >>> print pywt.upcoef('a', cA, 'db2') + pywt.upcoef('d', cD, 'db2')
    [-0.25       -0.4330127   1.          2.          3.          4.          5.
      6.          1.78589838 -1.03108891]
    >>> n = len(data)
    >>> print pywt.upcoef('a',cA,'db2',take=n) + pywt.upcoef('d',cD,'db2',take=n)
    [ 1.  2.  3.  4.  5.  6.]
