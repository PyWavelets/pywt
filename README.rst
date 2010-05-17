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


Download
--------

This package can be downloaded from Python Package Index at:

    http://pypi.python.org/pypi/PyWavelets

Latest development version is available from the SVN source code repository:

    ``svn co http://wavelets.scipy.org/svn/multiresolution/pywt/trunk pywt``


Install
-------

The most convenient way to install PyWavelets is to use the
Easy Install manager from setuptools:

    easy_install -U PyWavelets

In order to build PyWavelets from source, a working C compiler and a recent version
of Cython is required.

After completing the build environment, open the shell prompt, go to the
PyWavelets source code directory and type::

    python setup.py install

Documentation
-------------

Documentation and links to more resources is available online
at http://www.pybytes.com/pywavelets/.

Project wiki and trac system are hosted at http://wavelets.scipy.org/.

For examples see `demo` directories in the source package.


License
-------

PyWavelets is distributed under MIT license terms (see COPYING).
