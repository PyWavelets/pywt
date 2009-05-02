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

The most convenient way to install PyWavelets is to use Easy Install
packet manager, which will connect to Cheese Shop repository and
automatically download PyWavelets::

    easy_install PyWavelets

If you want to build and install the project from source code there
are two possibilities:

  * using setuptools Eggs system::
  
      python setupegg.py install 

  * or with standard distutils manager::
  
      python setup.py install

.. note::

    If you want to install PyWavelets from SVN repository source code
    or made changes to the Pyrex/Cython wrapper code you need a current
    version of Cython from http://www.cython.org/ in order to
    rebuild the project.


Documentation
-------------

Documentation is available in online at http://www.pybytes.com/pywavelets/,
as well as in the project's source code `doc` directory.

Project wiki and trac system are hosted at http://wavelets.scipy.org/.

For examples see `demo` and `tests` directories.

License
-------

PyWavelets is distributed under MIT license (see COPYING).
