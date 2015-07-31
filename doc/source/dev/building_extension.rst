.. _dev-building-extension:

Building and installing PyWavelets
==================================

Installing from source code
---------------------------

Go to https://github.com/PyWavelets/pywt GitHub project page, fork and clone the
repository or use the upstream repository to get the source code::

    git clone https://github.com/PyWavelets/pywt.git PyWavelets

Activate your Python virtual environment, go to the cloned source directory
and type the following commands to build and install the package::

    python setup.py build
    python setup.py install

To verify the installation run the following command::

    python setup.py test

To build docs::

    cd doc
    make html

Installing a development version
--------------------------------

You can also install directly from the source repository::

    pip install -e git+https://github.com/PyWavelets/pywt.git#egg=PyWavelets

or::

    pip install PyWavelets==dev


Installing a regular release from PyPi
--------------------------------------

A regular release can be installed with pip or easy_install::

    pip install PyWavelets

