.. _ref-modes:

.. currentmodule:: pywt
.. include:: ../substitutions.rst


======================
Signal extension modes
======================

.. _MODES:

Because the most common and practical way of representing digital signals
in computer science is with finite arrays of values, some extrapolation
of the input data has to be performed in order to extend the signal before
computing the :ref:`Discrete Wavelet Transform <ref-dwt>` using the cascading
filter banks algorithm.

Depending on the extrapolation method, significant artifacts at the signal's
borders can be introduced during that process, which in turn may lead to
inaccurate computations of the :ref:`DWT <ref-dwt>` at the signal's ends.

|pywt| provides several methods of signal extrapolation that can be used to
minimize this negative effect:

  .. _`MODES.zpd`:

  * ``zpd`` - **zero-padding** - signal is extended by adding zero samples::

      ... 0  0 | x1 x2 ... xn | 0  0 ...

  .. _`MODES.cpd`:

  * ``cpd`` - **constant-padding** - border values are replicated::

      ... x1 x1 | x1 x2 ... xn | xn xn ...

  .. _`MODES.sym`:

  * ``sym`` - **symmetric-padding** - signal is extended by *mirroring*
    samples::

      ... x2 x1 | x1 x2 ... xn | xn xn-1 ...

  .. _`MODES.ppd`:
  .. _`periodic-padding`:

  * ``ppd`` - **periodic-padding** - signal is treated as a periodic one::

      ... xn-1 xn | x1 x2 ... xn | x1 x2 ...

  .. _`MODES.sp1`:

  * ``sp1`` - **smooth-padding** - signal is extended according to the first
    derivatives calculated on the edges (straight line)

:ref:`DWT <ref-dwt>` performed for these extension modes is slightly redundant, but ensures
perfect reconstruction. To receive the smallest possible number of coefficients,
computations can be performed with the `periodization`_ mode:

  .. _`periodization`:
  .. _`MODES.per`:

  * ``per`` - **periodization** - is like `periodic-padding`_ but gives the
    smallest possible number of decomposition coefficients. :ref:`IDWT <ref-idwt>` must be
    performed with the same mode.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> print pywt.MODES.modes
    ['zpd', 'cpd', 'sym', 'ppd', 'sp1', 'per']


Notice that you can use any of the following ways of passing wavelet and mode
parameters:

.. sourcecode:: python

  >>> import pywt
  >>> (a, d) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
  >>> (a, d) = pywt.dwt([1,2,3,4,5,6], pywt.Wavelet('db2'), pywt.MODES.sp1)

.. note::
    Extending data in context of |pywt| does not mean reallocation of the data
    in computer's physical memory and copying values, but rather computing
    the extra values only when they are needed.
    This feature saves extra memory and CPU resources and helps to avoid page
    swapping when handling relatively big data arrays on computers with low
    physical memory.
