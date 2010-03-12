.. _ref-dwt2:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

=================================================
2D Forward and Inverse Discrete Wavelet Transform
=================================================


Single level ``dwt2``
~~~~~~~~~~~~~~~~~~~~~

.. function:: dwt2(data, wavelet[, mode='sym'])

  The :func:`dwt2` function performs single level 2D Discrete Wavelet Transform.

  :param data: 2D input data.

  :param wavelet: |wavelet_arg|

  :param mode: |mode| This is only important when DWT was performed
               in :ref:`periodization <MODES.per>` mode.

  .. compound::

    Returns one average and three details 2D coefficients arrays. The
    coefficients arrays are organized in tuples in the following form:

      ::

      (cA, (cH, cV, cD))

    where *cA*, *cH*, *cV*, *cD* denote approximation, horizontal
    detail, vertical detail and diagonal detail coefficients respectively.

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

|pywt| does not follow this pattern because of pure practical reasons of simple
access to particular type of the output coefficients.

  **Example:**

  .. sourcecode:: python

    >>> import pywt, numpy
    >>> data = numpy.ones((4,4), dtype=numpy.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> cA, (cH, cV, cD) = coeffs
    >>> print cA
    [[ 2.  2.]
     [ 2.  2.]]
    >>> print cV
    [[ 0.  0.]
     [ 0.  0.]]


Single level ``idwt2``
~~~~~~~~~~~~~~~~~~~~~~

.. function:: idwt2(coeffs, wavelet[, mode='sym'])

  The :func:`idwt2` function reconstructs data from the given coefficients
  set by performing single level 2D Inverse Discrete Wavelet Transform.

  :param coeffs: A tuple with approximation coefficients and three details
                 coefficients 2D arrays like from :func:`dwt2`::

                    (cA, (cH, cV, cD))

  :param wavelet: |wavelet_arg|

  :param mode: |mode| This is only important when the :func:`dwt` was performed
               in the :ref:`periodization <MODES.per>` mode.

  **Example:**

  .. sourcecode:: python

    >>> import pywt, numpy
    >>> data = numpy.array([[1,2], [3,4]], dtype=numpy.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> print pywt.idwt2(coeffs, 'haar')
    [[ 1.  2.]
     [ 3.  4.]]


2D multilevel decomposition using ``wavedec2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: wavedec2(data, wavelet[, mode='sym'[, level=None]])

  .. compound::

      Performs multilevel 2D Discrete Wavelet Transform decomposition and
      returns coefficients list::

        [cAn, (cHn, cVn, cDn), ..., (cH1, cV1, cD1)]

      where *n* denotes the level of decomposition and *cA*, *cH*, *cV* and *cD*
      are approximation, horizontal detail, vertical detail and diagonal detail
      coefficients arrays respectively.

  :param data: |data|

  :param wavelet: |wavelet_arg|

  :param mode: |mode|

  :param level: Decomposition level. This should not be greater than the
                reasonable maximum value computed with the :func:`dwt_max_level`
                function for the smaller dimension of the input data.

  **Example:**

  .. sourcecode:: python

    >>> import pywt, numpy
    >>> coeffs = pywt.wavedec2(numpy.ones((8,8)), 'db1', level=2)
    >>> cA2, (cH2, cV2, cD2), (cH1, cV1, cD1) = coeffs
    >>> print cA2
    [[ 4.  4.]
     [ 4.  4.]]


2D multilevel reconstruction using ``waverec2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: waverec2(coeffs, wavelet[, mode='sym'])

  Performs multilevel reconstruction from the given coefficients set.

  :param coeffs: Coefficients set must be in the form like that
                 from :func:`wavedec2` decomposition::

                    [cAn, (cHn, cVn, cDn), ..., (cH1, cV1, cD1)]

  :param wavelet: |wavelet_arg|

  :param mode: |mode|

  **Example:**

  .. sourcecode:: python

    >>> import pywt, numpy
    >>> coeffs = pywt.wavedec2(numpy.ones((4,4)), 'db1')
    >>> print "levels:", len(coeffs)-1
    levels: 2
    >>> print pywt.waverec2(coeffs, 'db1')
    [[ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]]
