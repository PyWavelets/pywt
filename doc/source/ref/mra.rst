.. _ref-mra:

.. currentmodule:: pywt

Multiresolution Analysis
------------------------

The functions in this module can be used to project a signal onto wavelet
subspaces and an approximation subspace. This is an additive decomposition such
that the sum of the coefficients equals the original signal. The projected
signal coefficients remains temporally aligned with the original, regardless
of the symmetry of the wavelet used for the analysis.

Multilevel 1D ``mra``
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: mra

Multilevel 2D ``mra2``
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: mra2

Multilevel n-dimensional ``mran``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: mran

Inverse Multilevel 1D ``imra``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: imra

Inverse Multilevel 2D ``imra2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: imra2

Inverse Multilevel n-dimensional ``imran``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: imran

