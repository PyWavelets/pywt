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

The most recent *development* version can be found in Git and Hg repositories at:

  * Github - https://github.com/nigma/pywt
  * Bitbucket - https://bitbucket.org/nigma/pywt

Latest release (not always up-to-date), including source and binary package for Windows,
is available for download from the Python Package Index at http://pypi.python.org/pypi/PyWavelets.

Note: The old SVN repository at http://wavelets.scipy.org/svn/multiresolution/pywt/trunk is
not updated anymore and you should switch to one of the new ones.

Install
-------

In order to build PyWavelets from source, a working C compiler (GCC or MinGW) 
and a recent version of Cython (http://cython.org/) is required.

After completing the build environment, open the shell prompt, go to the
PyWavelets source code directory and type::

    python setup.py install

Prebuilt Windows binaries and source code packages are also
available from http://pypi.python.org/pypi/PyWavelets.

Documentation
-------------

Documentation and links to more resources is available online
at http://www.pybytes.com/pywavelets/.

Project wiki and trac system are hosted at http://wavelets.scipy.org/.

For examples see `demo` directories in the source package.


License
-------

PyWavelets is distributed under MIT license terms (see COPYING).
