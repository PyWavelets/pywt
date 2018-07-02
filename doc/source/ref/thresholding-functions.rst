.. _ref-thresholding:
.. currentmodule:: pywt

Thresholding functions
======================

The :mod:`~pywt.thresholding` helper module implements the most popular signal
thresholding functions.

Thresholding
------------

.. autofunction:: threshold
.. autofunction:: threshold_firm

The left panel of the figure below illustrates that non-negative Garotte
thresholding is intermediate between soft and hard thresholding.  Firm
thresholding transitions between soft and hard thresholding behavior. It
requires a pair of threshold values that define the width of the transition
region.

.. plot:: pyplots/plot_thresholds.py

.. include:: ../common_refs.rst
