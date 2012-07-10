.. _dev-building-on-linux:

.. module:: pywt
.. include:: ../substitutions.rst

=================
Building on Linux
=================


Prepare build environment
~~~~~~~~~~~~~~~~~~~~~~~~~

There is a good chance that you already have a working build environment.
Just skip steps that you don't need to execute.


Install basic build tools
~~~~~~~~~~~~~~~~~~~~~~~~~

Note that the example below uses ``aptitude`` package manager, which is
specific to Debian and Ubuntu Linux distributions. Use your favourite package
manager to install these packages on your OS.

::

    aptitude install build-essential gcc python-dev git-core


Setup Python virtualenv
~~~~~~~~~~~~~~~~~~~~~~~

A good practice is to create a separate Python virtual environment for each
project. If you don't have `virtualenv <http://pypi.python.org/pypi/virtualenv>`_
yet, install and activate it using::

    curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py <name_of_the_venv>
    . <name_of_the_venv>/bin/activate


Setup build dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

Use ``pip`` (http://pypi.python.org/pypi/pip) to install necessary Python
packages::

    pip install Cython numpy

Install Sphinx
~~~~~~~~~~~~~~

Sphinx is a documentation tool that convert reStructuredText files into
nice looking html documentation. It is only required to rebuild |pywt|
documentation, not the package itself.

Get Sphinx from the Python Package Index (http://pypi.python.org/pypi/Sphinx),
or install it with::

    pip install Sphinx


Install PyWavelets
~~~~~~~~~~~~~~~~~~

Installing from PyPi
--------------------

::

    pip install PyWavelets


Installing a development version
--------------------------------

::

    pip install -e git+https://github.com/nigma/pywt.git#egg=PyWavelets

or::

    pip install PyWavelets==dev


Installing from source code
---------------------------

Go to https://github.com/nigma/pywt GitHub project page, fork and clone the
repository or use the upstream repository to get the source code::

    git clone https://github.com/nigma/pywt.git PyWavelets

Activate your Python virtual env, go to the cloned source directory
and type the following commands to build and install the package::

    python setup.py build
    python setup.py install

To verify the installation go to the ``tests`` directory and run the following
commands::

    python test_regression.py
    python test_doc.py
    python test_perfect_reconstruction.py

