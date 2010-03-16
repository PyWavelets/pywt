.. _ref-swt:

.. currentmodule:: pywt
.. include:: ../substitutions.rst


Stationary Wavelet Transform
----------------------------

`Stationary Wavelet Transform (SWT) <http://en.wikipedia.org/wiki/Stationary_wavelet_transform>`_,
also known as *Undecimated wavelet transform* or *Algorithme à trous* is a translation-invariance
modification of the *Discrete Wavelet Transform* that does not decimate coefficients at every
transformation level.

Multilevel ``swt``
~~~~~~~~~~~~~~~~~~

.. function:: swt(data, wavelet, level[, start_level=0])

  Performs multilevel Stationary Wavelet Transform.

  :param data: |data|

  :param wavelet: |wavelet_arg|

  :param level: Required transform level. See the :func:`swt_max_level` function.

  .. compound::

      Returned list of coefficient pairs is in the form::

        [(cA1, cD1), (cA2, cD2), ..., (cAn, cDn)]

      where *n* is the *level* value.


Multilevel ``swt2``
~~~~~~~~~~~~~~~~~~~~~

.. function:: swt2(data, wavelet, level[, start_level=0])

  Performs multilevel 2D Stationary Wavelet Transform.

  :param data: 2D array with input data.

  :param wavelet: |wavelet_arg|

  :param level: Number of decomposition steps to perform.

  :param start_level: The level at which the decomposition will begin.

  .. compound::

      The result is a set of coefficients arrays over the range of decomposition
      levels::

        [
            (cA_n,
                (cH_n, cV_n, cD_n)
            ),
            (cA_n+1,
                (cH_n+1, cV_n+1, cD_n+1)
            ),
            ...,
            (cA_n+level,
                (cH_n+level, cV_n+level, cD_n+level)
            )
        ]

      where *cA* is approximation, *cH* is horizontal details, *cV* is vertical
      details, *cD* is diagonal details, *n* is *start_level* and *m* equals
      *n+level*.


Maximum decomposition level - ``swt_max_level``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: swt_max_level(input_len)

  Calculates the maximum level of Stationary Wavelet Transform for data of
  given length.

  :param input_len: Input data length.
