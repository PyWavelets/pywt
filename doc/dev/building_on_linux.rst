.. _dev-building-on-linux:

.. module:: pywt
.. include:: ../substitutions.rst

=================
Building on Linux
=================


Prepare build environment
~~~~~~~~~~~~~~~~~~~~~~~~~

There is a good chance that you already have a working build envoronment.
Just skip steps that you don't need to execute.

Note that the examples below use ``aptitude`` package manager, which might
be specific to only some Linux distributions like Ubuntu. Use your
favourite package manager to install these packages on your OS.


Install basic build tools
~~~~~~~~~~~~~~~~~~~~~~~~~

::

    aptitude install build-essential gcc


Setup Python environment
~~~~~~~~~~~~~~~~~~~~~~~~

::

    aptitude install python python-dev python-setuptools


Setup Python virtualenv (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you wish to create a completely separate Python environment
for the development purposes, you can use virtualenv
(http://pypi.python.org/pypi/virtualenv).

Just install it from the OS package repository::

    aptitude install python-virtualenv

or get it from PyPI::

    easy_install -U virtualenv

Now in the directory where you want to store the build environment execute::

    virtualenv --no-site-packages <name_of_the_venv>

To activate the newly created environment type::

    source ./<name_of_the_venv>/bin/activate


Setup build dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

If you have created a virtual Python environment in the previus step
remember to activate it before executing the following commands.

Use ``pip`` (http://pypi.python.org/pypi/pip) or ``easy_install`` to install
Python packages::

    pip install Cython numpy

or::

    easy_install -U Cython
    easy_install numpy

.. Note:: In case you want to use the OS package manager to install ``numpy``,
          don't specify the ``--no-site-packages`` virtualenv option.
          Otherwise the global package won't be visible to the Python
          interpreter in the development environment.

Install Sphinx
~~~~~~~~~~~~~~

Sphinx is a documentation tool that convert reStructuredText files into
nice looking html documentation. It is only required to rebuild |pywt|
documentation, not the package itself.

Get Sphinx from the Python Package Index (http://pypi.python.org/pypi/Sphinx),
or install it with::

    easy_install -U Sphinx


Build PyWavelets
~~~~~~~~~~~~~~~~

Activate your Python virtual env, go to the pywt source directory
and type the following to build and install the package::

    python setup.py build
    python setup.py install


Go to the ``tests`` directory and run some tests to verify
the installation::

    cd tests
    python test_regression.py
    python test_doc.py
    python test_perfect_reconstruction.py

