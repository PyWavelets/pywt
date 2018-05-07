.. _ref-thresholding:
.. currentmodule:: pywt

Thresholding functions
======================

The :mod:`~pywt.thresholding` helper module implements the most popular signal
thresholding functions. The left panel of the figure below illustrates that
non-negative Garotte thresholding is intermediate between soft and hard
thresholding.  Firm thresholding transitions between soft and hard thresholding
behavior. It requires a pair of threshold values that define the width of the
transition region. This figure was generated using `plot_thresholds.py` within
the `demo`_ directory.

.. image:: ../_static/threshold_types.png

Thresholding
------------

.. autofunction:: threshold
.. autofunction:: threshold_firm

.. include:: ../common_refs.rst
