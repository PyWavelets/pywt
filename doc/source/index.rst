PyWavelets - Wavelet Transforms in Python
=========================================

PyWavelets is open source wavelet transform software for Python_. It combines
a simple high level interface with low level C and Cython performance.

PyWavelets is very easy to use and get started with. Just install the package,
open the Python interactive shell and type:

  .. sourcecode:: python

    >>> import pywt
    >>> cA, cD = pywt.dwt([1, 2, 3, 4], 'db1')

Voilà! Computing wavelet transforms has never been so simple :)

Here is a slightly more involved example of applying a digital wavelet
transform to an image:

.. plot:: pyplots/camera_approx_detail.py

Main features
-------------

The main features of PyWavelets are:

  * 1D, 2D and nD Forward and Inverse Discrete Wavelet Transform (DWT and IDWT)
  * 1D, 2D and nD Multilevel DWT and IDWT
  * 1D, 2D and nD Stationary Wavelet Transform (Undecimated Wavelet Transform)
  * 1D and 2D Wavelet Packet decomposition and reconstruction
  * 1D Continuous Wavelet Transform
  * Computing Approximations of wavelet and scaling functions
  * Over 100 `built-in wavelet filters`_ and support for custom wavelets
  * Single and double precision calculations
  * Real and complex calculations
  * Results compatible with Matlab Wavelet Toolbox (TM)


Getting help
------------

Use `GitHub Issues`_, `StackOverflow`_, or the `PyWavelets discussions group`_
to post your comments or questions.

License
-------

PyWavelets is a free Open Source software released under the MIT license.

Citing
------

If you use PyWavelets in a scientific publication, we would appreciate
citations of the project:

    Lee G, Gommers R, Wasilewski F, Wohlfahrt K, O'Leary A, Nahrstaedt H,
    and Contributors, "PyWavelets - Wavelet Transforms in Python", 2006-,
    https://github.com/PyWavelets/pywt [Online; accessed 2018-MM-DD].


Contents
--------

.. toctree::
   :maxdepth: 1

   install
   ref/index
   regression/index
   contributing
   dev/index
   releasenotes

.. include:: common_refs.rst
