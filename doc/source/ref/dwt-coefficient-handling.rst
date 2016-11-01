.. _ref-dwt-coef:

=========================
Handling DWT Coefficients
=========================

Convenience routines are available for converting the outputs of the multilevel
dwt functions (``wavedec``, ``wavedec2`` and ``wavedecn``) to and from a
single, concatenated coefficient array.

.. currentmodule:: pywt

Concatenating all coefficients into a single array
--------------------------------------------------
.. autofunction:: coeffs_to_array

Splitting concatenated coefficient array back into its components
-----------------------------------------------------------------
.. autofunction:: array_to_coeffs
