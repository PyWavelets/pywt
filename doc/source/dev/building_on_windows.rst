.. _dev-building-on-windows:

.. module:: pywt
.. include:: ../substitutions.rst

===================
Building on Windows
===================


Prepare build environment
~~~~~~~~~~~~~~~~~~~~~~~~~

To start developing |pywt| code on Windows you will have to prepare build
environment first. This will include installing a couple components like
Python, MinGW C compiler, Cython, Numpy and Sphinx.


Install Python
~~~~~~~~~~~~~~

Go to the Python download site http://python.org/download/ and get
the recent 2.x Python for Windows version (Python 2.6 recommended).
Install it.


Install MinGW C compiler
~~~~~~~~~~~~~~~~~~~~~~~~

Take a look at http://www.mingw.org/wiki/Getting_Started
and http://www.mingw.org/wiki/HOWTO_Install_the_MinGW_GCC_Compiler_Suite.
Follow the instructions there to set up the compiler.

You can also take a look at Cython's "Installing MinGW on Windows"
page at http://docs.cython.org/src/tutorial/appendix.html.


Configure Distutils
~~~~~~~~~~~~~~~~~~~

Distutils is a standard Python build system. By default it relies
on Microsoft Visual C compiler, but it is recommended to use
MinGW GCC compiler instead (|pywt| is developed and tested using GCC).

In order to change the settings and use MinGW as the default compiler,
edit or create a Distutils configuration file
``c:\Python26\Lib\distutils\distutils.cfg`` and place the following
entry in it::

    [build]
    compiler = mingw32


Install Cython
~~~~~~~~~~~~~~

Instructions on installing recent Cython version are
on http://docs.cython.org/src/quickstart/install.html.


Install Numpy
~~~~~~~~~~~~~

Fetch and install a recent Numpy binary
from http://new.scipy.org/download.html.


Install Sphinx
~~~~~~~~~~~~~~

Sphinx is a documentation tool that convert reStructuredText files into
nice looking html documentation. It is only required to rebuild |pywt|
documentation, not the package itself.

Get Sphinx from the Python Package Index (http://pypi.python.org/pypi/Sphinx),
or install it with::

    easy_install -U Sphinx


Ready to go
~~~~~~~~~~~

At this point you should be ready to go. Open command line and go to
|pywt| source code directory.

To build the project issue::

    python setup.py build

To install::

    python setup.py install

To build docs::

    cd doc
    doc2html.bat

To run some tests::

    cd tests
    python test_regression.py
    python test_doc.py
    python test_perfect_reconstruction.py
