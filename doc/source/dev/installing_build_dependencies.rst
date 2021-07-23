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


    pip install Cython


Installing numpy
----------------

Use ``pip`` to install numpy_::

    pip install numpy

Numpy can also be obtained via scientific python distributions such as:

- Anaconda_
- `Enthought Canopy`_
- `Python(x,y) <http://python-xy.github.io/>`_

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
.. _Anaconda: https://www.continuum.io/downloads
.. _Enthought Canopy: https://www.enthought.com/products/canopy/
