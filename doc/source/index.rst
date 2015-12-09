PyWavelets - Discrete Wavelet Transform in Python
=================================================

PyWavelets is a free Open Source wavelet transform software for the Python_
programming language. It is written in Python, Cython and C for a mix of easy
and powerful high-level interface and the best performance.

PyWavelets is very easy to start with and use. Just install the package, open
the Python interactive shell and type:

  .. sourcecode:: python

    >>> import pywt
    >>> cA, cD = pywt.dwt([1, 2, 3, 4], 'db1')

Voilà! Computing wavelet transforms never before has been so simple :)

Main features
-------------

The main features of PyWavelets are:

  * 1D, 2D and nD Forward and Inverse Discrete Wavelet Transform (DWT and IDWT)
  * 1D, 2D and nD Multilevel DWT and IDWT
  * 1D and 2D Stationary Wavelet Transform (Undecimated Wavelet Transform)
  * 1D and 2D Wavelet Packet decomposition and reconstruction
  * Approximating wavelet and scaling functions
  * Over seventy `built-in wavelet filters`_
    and custom wavelets supported
  * Single and double precision calculations
  * Real and complex calculations
  * Results compatible with Matlab Wavelet Toolbox (TM)

Requirements
------------

PyWavelets is a package for the Python programming language. It requires:

 - Python_ 2.6, 2.7 or >=3.3
 - Numpy_ >= 1.6.2

Download
--------

The most recent *development* version can be found on GitHub at
https://github.com/PyWavelets/pywt.

Latest release, including source and binary package for Windows, is available
for download from the `Python Package Index`_ or on the `Releases Page`_.

Install
-------

In order to build PyWavelets from source, a working C compiler (GCC or MSVC)
and a recent version of Cython_ is required.

 - Install PyWavelets with ``pip install PyWavelets``.

 - To build and install from source, navigate to downloaded PyWavelets source
   code directory and type ``python setup.py install``.

Prebuilt Windows binaries and source code packages are also
available from `Python Package Index`_.

Binary packages for several Linux distributors are maintained by Open Source
community contributors. Query your Linux package manager tool for
`python-pywavelets`, `python-wavelets`, `python-pywt` or similar package name.

.. seealso::  :ref:`Development notes <dev-index>` section contains more
              information on building and installing from source code.

Documentation
-------------

Documentation with detailed examples and links to more resources is available
online at http://pywavelets.readthedocs.org.

For more usage examples see the `demo`_ directory in the source package.

State of development & Contributing
-----------------------------------

PyWavelets started in 2006 as an academic project for a master thesis
on `Analysis and Classification of Medical Signals using Wavelet Transforms`
and was maintained until 2012 by its `original developer`_.  In 2013
maintenance was taken over in a `new repo <https://github.com/PyWavelets/pywt>`_)
by a larger development team - a move supported by the original developer.
The repo move doesn't mean that this is a fork - the package continues to be
developed under the name "PyWavelets", and released on PyPi and Github (see
`this issue <https://github.com/nigma/pywt/issues/13>`_ for the discussion
where that was decided).

All contributions including bug reports, bug fixes, new feature implementations
and documentation improvements are welcome.  Moreover, developers with an
interest in PyWavelets are very welcome to join the development team!


Python 3
--------

Python 3.x is fully supported from release v0.3.0 on.

Contact
-------

Use `GitHub Issues`_ or the `PyWavelets discussions group`_ to post your
comments or questions.

License
-------

PyWavelets is a free Open Source software released under the MIT license.

Contents
--------

.. toctree::
   :maxdepth: 1

   ref/index
   regression/index
   dev/index
   resources
   contents


.. _built-in wavelet filters: http://wavelets.pybytes.com/
.. _Cython: http://cython.org/
.. _demo: https://github.com/PyWavelets/pywt/tree/master/demo
.. _GitHub: https://github.com/PyWavelets/pywt
.. _GitHub Issues: https://github.com/PyWavelets/pywt/issues
.. _Numpy: http://www.numpy.org
.. _original developer: http://en.ig.ma
.. _Python: http://python.org/
.. _Python Package Index: http://pypi.python.org/pypi/PyWavelets/
.. _PyWavelets discussions group: http://groups.google.com/group/pywavelets
.. _Releases Page: https://github.com/PyWavelets/pywt/releases
