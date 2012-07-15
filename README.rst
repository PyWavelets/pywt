PyWavelets Intro
----------------

PyWavelets is a Python wavelet transforms module that can do:

  * 1D and 2D Forward and Inverse Discrete Wavelet Transform (DWT and IDWT)
  * 1D and 2D Stationary Wavelet Transform (Undecimated Wavelet Transform)
  * 1D and 2D Wavelet Packet decomposition and reconstruction
  * Computing Approximations of wavelet and scaling functions
  * Over seventy built-in wavelet filters and support for custom wavelets
  * Single and double precision calculations
  * Results compatibility with Matlab Wavelet Toolbox (tm)

.. image::
    https://secure.travis-ci.org/nigma/pywt.png?branch=develop
    :alt: Build Status
        :target: https://secure.travis-ci.org/nigma/pywt

Download
--------

The most recent *development* version can be found on GitHub at
https://github.com/nigma/pywt.

Latest release (not always up-to-date), including source and binary package for Windows,
is available for download from the
`Python Package Index <http://pypi.python.org/pypi/PyWavelets>`_.

Install
-------

In order to build PyWavelets from source, a working C compiler (GCC or MSVC)
and a recent version of Cython (http://cython.org/) is required.

 - To install PyWavelets open shell prompt and type ``pip install PyWavelets``
   or ``easy_install PyWavelets``.

 - To build and install from source, navigate to downloaded PyWavelets source
   code directory and type ``python setup.py install``.

 - The `in-development version <https://github.com/nigma/pywt/tarball/develop#egg=PyWavelets-dev>`_
   of PyWavelets can be installed with ``pip install PyWavelets==dev``
   or ``easy_install PyWavelets==dev``.

Prebuilt Windows binaries and source code packages are also
available from http://pypi.python.org/pypi/PyWavelets.

Documentation
-------------

Documentation and links to more resources is available online
at http://www.pybytes.com/pywavelets/.

For more usage examples see `demo <https://github.com/nigma/pywt/tree/master/demo>`_
directory in the source package.

Python 3
--------

Python 3 development branch is at https://github.com/nigma/pywt/tree/py-3.
Check out the `changelog <https://github.com/nigma/pywt/commits/py-3>`_ for
info. Currently the code and examples are ported to work on Python 2.7 and 3.2
from the same codebase.

License
-------

PyWavelets is distributed under MIT license terms (see COPYING).
