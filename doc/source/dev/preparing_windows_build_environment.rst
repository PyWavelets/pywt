.. _dev-building-on-windows:


Preparing Windows build environment
===================================

To start developing PyWavelets code on Windows you will have to install
a C compiler and prepare the build environment.

Installing Windows SDK C/C++ compiler
-------------------------------------

Microsoft Visual C++ 2008 (Microsoft Visual Studio 9.0) is the compiler that
is suitable for building extensions for Python 2.6, 2.7, 3.0, 3.1 and 3.2
(both 32 and 64 bit).

.. note:: For reference:

     - the *MSC v.1500* in the Python version string is Microsoft Visual
       C++ 2008 (Microsoft Visual Studio 9.0 with msvcr90.dll runtime)
     - *MSC v.1600* is MSVC 2010 (10.0 with msvcr100.dll runtime)
     - *MSC v.1700* is MSVC 2011 (11.0)

     ::

        Python 2.7.3 (default, Apr 10 2012, 23:31:26) [MSC v.1500 32 bit (Intel)] on win32
        Python 3.2 (r32:88445, Feb 20 2011, 21:30:00) [MSC v.1500 64 bit (AMD64)] on win32


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
.. _numpy: http://numpy.scipy.org/
.. _Cython: http://cython.org/
.. _Sphinx: http://sphinx.pocoo.org/
.. _MinGW C compiler: http://sourceforge.net/projects/mingwbuilds/
