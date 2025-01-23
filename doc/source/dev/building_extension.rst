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

    pip install .

To verify the installation run the following command::

    pytest .


Installing a development version
--------------------------------

You can also install directly from the source repository::

    pip install -e git+https://github.com/PyWavelets/pywt.git#egg=PyWavelets

or::

    pip install PyWavelets==dev


Installing a regular release from PyPi
--------------------------------------

A regular release can be installed with pip::

    pip install PyWavelets
