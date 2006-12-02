PyWavelets Intro
----------------

PyWavelets is a Python wavelet transforms module that can perform:

  * Discrete Wavelet Transform (1D and 2D)
  * Inverse Discrete Wavelet Transform (1D and 2D)
  * Stationary Wavelet Transform
  * Wavelet Packets decomposition and reconstruction


Download
--------

This package can be downloaded from Cheese Shop repository:

    http://cheeseshop.python.org/pypi/PyWavelets

Latest development version is available from SVN source code repository:

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
    or made changes to the Pyrex wrapper code you need an updated version
    of Pyrex from http://codespeak.net/svn/lxml/pyrex/ in order to
    rebuild the project.


Documentation
-------------

Documentation is available in `doc` directory as well as
online at 

  http://www.pybytes.com/pywavelets/

Project wiki and trac system are located at

  http://wavelets.scipy.org/

For examples see `demo` and `tests` directories.


License
-------

PyWavelets is distributed under MIT license (see COPYING).


