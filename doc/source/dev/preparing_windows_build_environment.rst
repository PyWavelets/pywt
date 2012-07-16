.. _dev-building-on-windows:


Preparing Windows build environment
===================================

To start developing PyWavelets code on Windows you will have to install
a C compiler and prepare the build environment.

Installing Windows SDK C/C++ compiler
-------------------------------------

Download Microsoft Windows SDK for Windows 7 and .NET Framework 3.5 SP1
from http://www.microsoft.com/downloads/en/details.aspx?familyid=71DEB800-C591-4F97-A900-BEA146E4FAE1&displaylang=en.
Download, extract and install the version that is suitable for your platform:

  - ``GRMSDK_EN_DVD.iso`` for 32-bit x86 platform
  - ``GRMSDKX_EN_DVD.iso`` for 64-bit AMD64 platform

Before compiling a Python extension you have to configure some environment
variables.

For 32-bit build execute ``util/setenv_build32.bat`` script in the cmd window:

  .. sourcecode:: bat

    rem Configure the environment for 32-bit builds.
    rem Use "vcvars32.bat" for a 32-bit build.
    "C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\bin\vcvars32.bat"
    rem Convince setup.py to use the SDK tools.
    set MSSdk=1
    setenv /x86 /release
    set DISTUTILS_USE_SDK=1

For 64-bit use ``util/setenv_build64.bat``:

  .. sourcecode:: bat

    rem Configure the environment for 64-bit builds.
    rem Use "vcvars32.bat" for a 32-bit build.
    "C:\Program Files (x86)\Microsoft Visual Studio 9.0\VC\bin\vcvars64.bat"
    rem Convince setup.py to use the SDK tools.
    set MSSdk=1
    setenv /x64 /release
    set DISTUTILS_USE_SDK=1

See also http://wiki.cython.org/64BitCythonExtensionsOnWindows.

MinGW C/C++ compiler
--------------------

MinGW distribution can be downloaded from http://sourceforge.net/projects/mingwbuilds/.

In order to change the settings and use MinGW as the default compiler,
edit or create a Distutils configuration file
``c:\Python2*\Lib\distutils\distutils.cfg`` and place the following
entry in it::

    [build]
    compiler = mingw32

You can also take a look at Cython's "Installing MinGW on Windows"
page at http://wiki.cython.org/InstallingOnWindows for more info.


.. note::

    Python 2.7/3.2 distutils package is incompatible with current version
    of MinGW (4.7+) after MinGW dropped the `-mno-cygwin` flag.

    To use MinGW to compile Python extensions you have to patch the
    ``distutils/cygwinccompiler.py`` library module and remove every occurrence
    of ``-mno-cygwin``.

    See http://bugs.python.org/issue12641 bug report for more information
    on the issue.


Next steps
----------

After completing these steps continue with
:ref:`Installing build dependencies <dev-installing-build-dependencies>`.


.. _Python: http://python.org/
.. _numpy: http://numpy.scipy.org/
.. _Cython: http://cython.org/
.. _Sphinx: http://sphinx.pocoo.org/
.. _MinGW C compiler: http://sourceforge.net/projects/mingwbuilds/
