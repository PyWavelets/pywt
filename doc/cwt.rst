Continuous Wavelet Transform (CWT)
----------------------------------

cwavelist()
~~~~~~~~~~~


.. _`CWavelet`:

Continuous Wavelet - ``CWavelet``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    CWavelet(name, psi=None, properties={})


Continuous Wavelet Transform with ``cwt``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1D Continuous Wavelet Transform

::

    coeffs = cwt(data, wavelet, scales, data_step=1.0, precision=10)

data
  1D input data

wavelet
  Wavelet *name*, CWavelet_ object or Wavelet_ object.

  For convenience, a pair of `(function_approximation, x_grid)` arrays can aslo
  be used here::

    coeffs cwt(data, (psi, x_grid), scales, data_step=1.0, precision=10)

scales
  A list of scales at which to perform the CWT.

data_step
  The distance between two neighbour points on the x-axis.

precision
 Applicable only when wavelet *name*, *CWavelet* object or *Wavelet* object is
 passed as the *wavelet* parameter and is used to calculate the wavelet function
 approximation.

The function returns a list of coefficients arrays, one for every scale value
in *scales*.

