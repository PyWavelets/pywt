.. _ref-idwt:

.. currentmodule:: pywt

=========================================
Inverse Discrete Wavelet Transform (IDWT)
=========================================


Single level ``idwt``
---------------------

.. autofunction:: idwt

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'smooth')
    >>> print pywt.idwt(cA, cD, 'db2', 'smooth')
    array([ 1.,  2.,  3.,  4.,  5.,  6.])

  One of the neat features of :func:`idwt` is that one of the ``cA`` and ``cD``
  arguments can be set to ``None``. In that situation the reconstruction will be
  performed using only the other one. Mathematically speaking, this is
  equivalent to passing a zero-filled array as one of the arguments.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'smooth')
    >>> A = pywt.idwt(cA, None, 'db2', 'smooth')
    >>> D = pywt.idwt(None, cD, 'db2', 'smooth')
    >>> print A + D
    array([ 1.,  2.,  3.,  4.,  5.,  6.])


Multilevel reconstruction using ``waverec``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: waverec


Direct reconstruction with ``upcoef``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: upcoef
