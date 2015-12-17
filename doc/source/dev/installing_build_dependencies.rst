.. _dev-installing-build-dependencies:

Installing build dependencies
=============================

Setting up Python virtual environment
-------------------------------------

A good practice is to create a separate Python virtual environment for each
project. If you don't have `virtualenv`_ yet, install and activate it using::

    curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    python virtualenv.py <name_of_the_venv>
    . <name_of_the_venv>/bin/activate


Installing Cython
-----------------

Use ``pip`` (http://pypi.python.org/pypi/pip) to install Cython_::


    pip install Cython>=0.16


Installing numpy
----------------

Use ``pip`` to install numpy_::

    pip install numpy

It takes some time to compile numpy, so it might be more convenient to install
it from a binary release.

.. note::

  Installing numpy in a virtual environment on Windows is not straightforward.

  It is recommended to download a suitable binary ``.exe`` release from
  http://www.scipy.org/Download/ and install it using ``easy_install``
  (i.e. ``easy_install numpy-1.6.2-win32-superpack-python2.7.exe``).

.. note::

  You can find binaries for 64-bit Windows on http://www.lfd.uci.edu/~gohlke/pythonlibs/.


Installing Sphinx
-----------------

Sphinx_ is a documentation tool that converts reStructuredText files into
nicely looking html documentation. Install it with::

    pip install Sphinx

numpydoc_ is used to format the API docmentation appropriately.  Install it
via::

    pip install numpydoc


.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _numpy: http://numpy.org/
.. _Cython: http://cython.org/
.. _Sphinx: http://sphinx.pocoo.org
.. _numpydoc: https://github.com/numpy/numpydoc
