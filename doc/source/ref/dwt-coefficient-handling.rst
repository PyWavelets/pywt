.. _ref-dwt-coef:

=========================
Handling DWT Coefficients
=========================

Convenience routines are available for converting the outputs of the multilevel
dwt functions (``wavedec``, ``wavedec2`` and ``wavedecn``) to and from a
single, concatenated coefficient array.

.. currentmodule:: pywt

Concatenating all coefficients into a single n-d array
------------------------------------------------------
.. autofunction:: coeffs_to_array

Splitting concatenated coefficient array back into its components
-----------------------------------------------------------------
.. autofunction:: array_to_coeffs

Raveling and unraveling coefficients to/from a 1D array
-------------------------------------------------------
.. autofunction:: ravel_coeffs
.. autofunction:: unravel_coeffs

Multilevel: Total size of all coefficients - ``wavedecn_size``
--------------------------------------------------------------
.. autofunction:: wavedecn_size

Multilevel: n-d coefficient shapes - ``wavedecn_shapes``
--------------------------------------------------------
.. autofunction:: wavedecn_shapes
