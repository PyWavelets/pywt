.. _ref-other:

.. currentmodule:: pywt

===============
Other functions
===============


Integrating wavelet functions
-----------------------------

.. autofunction:: integrate_wavelet

The result of the call depends on the ``wavelet`` argument:

* for orthogonal and continuous wavelets - an integral of the
  wavelet function specified on an x-grid::

    [int_psi, x_grid] = integrate_wavelet(wavelet, precision)

* for other wavelets - integrals of decomposition and
  reconstruction wavelet functions and a corresponding x-grid::

    [int_psi_d, int_psi_r, x_grid] = integrate_wavelet(wavelet, precision)


Central frequency of ``psi`` wavelet function
---------------------------------------------

.. autofunction:: central_frequency

.. autofunction:: scale2frequency


Quadrature Mirror Filter
------------------------

.. autofunction:: qmf

Orthogonal Filter Banks
-----------------------

.. autofunction:: orthogonal_filter_bank


Example Datasets
----------------

The following example datasets are available in the module ``pywt.data``:

  ============  =======================================
    **name**               **description**
  ============  =======================================
   ecg           ECG waveform (1024 samples)
   aero          grayscale image (512x512)
   ascent        grayscale image (512x512)
   camera        grayscale image (512x512)
   nino          sea surface temperature (264 samples)
   demo_signal   various synthetic 1d test signals
  ============  =======================================

Each can be loaded via a function of the same name.

.. currentmodule:: pywt.data
.. autofunction:: demo_signal

**Example:**

.. sourcecode:: python

    >>> import pywt
    >>> camera = pywt.data.camera()
    >>> doppler = pywt.data.demo_signal('doppler', 1024)
    >>> available_signals = pywt.data.demo_signal('list')
