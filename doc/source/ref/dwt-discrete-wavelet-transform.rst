.. _ref-dwt:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

================================
Discrete Wavelet Transform (DWT)
================================

Wavelet transform has recently become a very popular when it comes to analysis,
de-noising and compression of signals and images. This section describes
functions used to perform single- and multilevel Discrete Wavelet Transforms.


Single level ``dwt``
--------------------

.. function:: dwt(data, wavelet[, mode='sym'])

  The :func:`dwt` function is used to perform single level, one dimensional
  Discrete Wavelet Transform.

  ::

    (cA, cD) = dwt(data, wavelet, mode='sym')

  :param data: |data|

  :param wavelet: |wavelet_arg|

  :param mode: |mode|

  The transform coefficients are returned as two arrays containing
  approximation (*cA*) and detail (*cD*) coefficients respectively. Length
  of returned arrays depends on the selected signal extension *mode* - see
  the :ref:`signal extension modes <ref-modes>` section for the list of
  available options and the :func:`dwt_coeff_len` function for information on
  getting the expected result length:

  * for all :ref:`modes <ref-modes>` except :ref:`periodization <MODES.per>`::

      len(cA) == len(cD) == floor((len(data) + wavelet.dec_len - 1) / 2)

  * for :ref:`periodization <MODES.per>` mode (``"per"``)::

      len(cA) == len(cD) == ceil(len(data) / 2)

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db1')
    >>> print cA
    [ 2.12132034  4.94974747  7.77817459]
    >>> print cD
    [-0.70710678 -0.70710678 -0.70710678]


Multilevel decomposition using ``wavedec``
------------------------------------------

.. function:: wavedec(data, wavelet, mode='sym', level=None)

  .. compound::

    The :func:`wavedec` function performs 1D multilevel Discrete Wavelet
    Transform decomposition of given signal and returns ordered list of
    coefficients arrays in the form:

      ::

      [cA_n, cD_n, cD_n-1, ..., cD2, cD1],

    where *n* denotes the level of decomposition. The first element (*cA_n*) of
    the result is approximation coefficients array and the following elements
    (*cD_n* - *cD_1*) are details coefficients arrays.

  :param data: |data|

  :param wavelet: |wavelet_arg|

  :param mode: |mode|

  :param level: Number of decomposition steps to performe. If the level is
                ``None``, then the full decomposition up to the level computed
                with :func:`dwt_max_level` function for the given data and
                wavelet lengths is performed.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db1', level=2)
    >>> cA2, cD2, cD1 = coeffs
    >>> print cD1
    [-0.70710678 -0.70710678 -0.70710678 -0.70710678]
    >>> print cD2
    [-2. -2.]
    >>> print cA2
    [  5.  13.]


Partial Discrete Wavelet Transform data decomposition ``downcoef``
------------------------------------------------------------------

.. function:: downcoef(part, data, wavelet[, mode='sym'[, level=1]])

   Similar to :func:`~pywt.dwt`, but computes only one set of coefficients.
   Useful when you need only approximation or only details at the given level.

   :param part: decomposition type. For ``a`` computes approximation
                coefficients, for ``d`` - details coefficients.

   :param data: |data|

   :param wavelet: |wavelet_arg|

   :param mode: |mode|

   :param level: Number of decomposition steps to perform.



Maximum decomposition level - ``dwt_max_level``
-----------------------------------------------

.. function:: dwt_max_level(data_len, filter_len)

  The :func:`~pywt.dwt_max_level` function can be used to compute the maximum
  *useful* level of decomposition for the given *input data length* and *wavelet
  filter length*.

  The returned value equals to::

    floor( log(data_len/(filter_len-1)) / log(2) )

  Although the maximum decomposition level can be quite high for long signals,
  usually smaller values are chosen depending on the application.

  The *filter_len* can be either an ``int`` or :class:`Wavelet` object for
  convenience.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> w = pywt.Wavelet('sym5')
    >>> print pywt.dwt_max_level(data_len=1000, filter_len=w.dec_len)
    6
    >>> print pywt.dwt_max_level(1000, w)
    6

.. _`dwt_coeff_len`:


Result coefficients length - ``dwt_coeff_len``
----------------------------------------------

.. function:: dwt_coeff_len(data_len, filter_len, mode)

Based on the given *input data length*, Wavelet *decomposition filter length*
and :ref:`signal extension mode <MODES>`, the :func:`dwt_coeff_len` function
calculates length of resulting coefficients arrays that would be created while
performing :func:`dwt` transform.

For :ref:`periodization <MODES.per>` mode this equals::

  ceil(data_len / 2)

which is the lowest possible length guaranteeing perfect reconstruction.

For other :ref:`modes <ref-modes>`::

  floor((data_len + filter_len - 1) / 2)

The *filter_len* can be either an *int* or :class:`Wavelet` object for
convenience.
