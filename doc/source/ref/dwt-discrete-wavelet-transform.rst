.. _ref-dwt:

.. currentmodule:: pywt

================================
Discrete Wavelet Transform (DWT)
================================

Wavelet transform has recently become a very popular when it comes to analysis,
de-noising and compression of signals and images. This section describes
functions used to perform single- and multilevel Discrete Wavelet Transforms.


Single level ``dwt``
--------------------

.. autofunction:: dwt

See the :ref:`signal extension modes <ref-modes>` section for the list of
available options and the :func:`dwt_coeff_len` function for information on
getting the expected result length.

The transform can be performed over one axis of multi-dimensional
data. By default this is the last axis. For multi-dimensional transforms
see the :ref:`2D transforms <ref-dwt2>` section.


Multilevel decomposition using ``wavedec``
------------------------------------------

.. autofunction:: wavedec


Partial Discrete Wavelet Transform data decomposition ``downcoef``
------------------------------------------------------------------

.. autofunction:: downcoef


Maximum decomposition level - ``dwt_max_level``, ``dwtn_max_level``
-------------------------------------------------------------------

.. autofunction:: dwt_max_level
.. autofunction:: dwtn_max_level


.. _`dwt_coeff_len`:

Result coefficients length - ``dwt_coeff_len``
----------------------------------------------

.. autofunction:: dwt_coeff_len

Based on the given input data length (``data_len``), wavelet decomposition
filter length (``filter_len``) and :ref:`signal extension mode <Modes>`, the
:func:`dwt_coeff_len` function calculates the length of the resulting
coefficients arrays that would be created while performing :func:`dwt`
transform.

``filter_len`` can be either an ``int`` or :class:`Wavelet` object for
convenience.
