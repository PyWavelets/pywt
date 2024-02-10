.. _dev-building-on-windows:


Preparing Windows build environment
===================================

To start developing PyWavelets code on Windows you will have to install a C
compiler and prepare the build environment. PyWavelets can be built with all
commonly used compilers on Windows (MSVC, Clang-cl, MinGW-w64, Intel C
compilers). PyWavelets' own CI jobs use MSVC; the ``appveyor.yml``
configuration file may be a helpful reference if you want to use MSVC locally.

After completing these steps continue with
:ref:`Installing build dependencies <dev-installing-build-dependencies>`.


.. _Python: http://python.org/
.. _numpy: http://numpy.org/
.. _Cython: http://cython.org/
.. _Sphinx: http://sphinx.pocoo.org/
.. _MinGW C compiler: http://sourceforge.net/projects/mingwbuilds/
