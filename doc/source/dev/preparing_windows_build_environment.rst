.. _dev-building-on-windows:


Preparing Windows build environment
===================================

To start developing PyWavelets code on Windows you will have to install
a C compiler and prepare the build environment.

Installing Windows SDK C/C++ compiler
-------------------------------------

Depending on your Python version, a different version of the Microsoft Visual
C++ compiler will be required to build extensions. The same compiler that was
used to build Python itself should be used.

For Python 3.7 or 3.8 it will be MSVC 2015.

The MSVC version should be printed when starting a Python REPL, and can be
checked against the note below:

.. note:: For reference:

     - the *MSC v.1500* in the Python version string is Microsoft Visual
       C++ 2008 (Microsoft Visual Studio 9.0 with msvcr90.dll runtime)
     - *MSC v.1600* is MSVC 2010 (10.0 with msvcr100.dll runtime)
     - *MSC v.1700* is MSVC 2012 (11.0)
     - *MSC v.1800* is MSVC 2013 (12.0)
     - *MSC v.1900* is MSVC 2015 (14.0)

     ::

        Python 3.5.5 (default, Feb 13 2018, 06:15:35) [MSC v.1900 64 bit (AMD64)] on win32

To get started first download, extract and install *Microsoft Windows SDK for
Windows 7 and .NET Framework 3.5 SP1* from
http://www.microsoft.com/downloads/en/details.aspx?familyid=71DEB800-C591-4F97-A900-BEA146E4FAE1&displaylang=en.

There are several ISO images on the site, so just grab the one that is suitable
for your platform:

  - ``GRMSDK_EN_DVD.iso`` for 32-bit x86 platform
  - ``GRMSDKX_EN_DVD.iso`` for 64-bit AMD64 platform (AMD64 is the codename for
    64-bit CPU architecture, not the processor manufacturer)

After installing the SDK and before compiling the extension you have
to configure some environment variables.

For 32-bit build execute the ``util/setenv_build32.bat`` script in the cmd
window:

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

MinGW distribution can be downloaded from
http://sourceforge.net/projects/mingwbuilds/.

In order to change the settings and use MinGW as the default compiler,
edit or create a Distutils configuration file
``c:\Python2*\Lib\distutils\distutils.cfg`` and place the following
entry in it::

    [build]
    compiler = mingw32

You can also take a look at Cython's "Installing MinGW on Windows"
page at http://wiki.cython.org/InstallingOnWindows for more info.


.. note::

    Python 2.7/3.2 distutils package is incompatible with the current version
    (4.7+) of MinGW (MinGW dropped the ``-mno-cygwin`` flag, which is still
    passed by distutils).

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
.. _numpy: http://numpy.org/
.. _Cython: http://cython.org/
.. _Sphinx: http://sphinx.pocoo.org/
.. _MinGW C compiler: http://sourceforge.net/projects/mingwbuilds/
