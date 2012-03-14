.. _ref-overview:

.. module:: pywt
.. include:: substitutions.rst

========
Overview
========

|pywt| is a free Open Source wavelet transform software for Python_
programming language. It is written in Python, Pyrex/Cython and C for a mix
of easy and powerful high-level interface and the best performance.

|pywt| is very easy to start with and use. Just install the package, open
the Python interactive shell and type:

  .. sourcecode:: python

    >>> import pywt
    >>> cA, cD = pywt.dwt([1, 2, 3, 4], 'db1')

Voilà! Computing wavelet transforms never before has been so simple :)

Main features
-------------

The main features of |pywt| are:

  * 1D and 2D Forward and Inverse Discrete Wavelet Transform (DWT and IDWT)
  * 1D and 2D Stationary Wavelet Transform (Undecimated Wavelet Transform)
  * 1D and 2D Wavelet Packet decomposition and reconstruction
  * Approximating wavelet and scaling functions
  * Over seventy built-in wavelet filters and custom wavelets supported
  * Single and double precision calculations supported
  * Results compatibility with Matlab Wavelet Toolbox |tm|

Requirements
------------

|pywt| is a Python programming language package and requires `Python <http://python.org/>`_
2.5-2.7 installed. The only external requirement is a recent version of
`NumPy <http://numpy.scipy.org/>`_ numeric array module.

Download
--------

The most recent *development* version can be found in Git and Hg repositories at:

  * Github - https://github.com/nigma/pywt
  * Bitbucket - https://bitbucket.org/nigma/pywt

Latest release (not always up-to-date), including source and binary package for Windows,
is available for download from the Python Package Index at http://pypi.python.org/pypi/PyWavelets/.

Install
-------

In order to build |pywt| from source, a working C compiler and a recent version
of `Cython <http://www.cython.org/>`_ and `Numpy <http://numpy.scipy.org/>`_ is required.

After completing the build environment, open the shell prompt, go to the
|pywt| source code directory and type::

    python setup.py install

.. seealso::  :ref:`Development notes <dev-index>` section contains more
              information on building from source code.

For Windows users there is a standard binary installer available for
download from the `Python Package Index <http://pypi.python.org/pypi/PyWavelets/>`_.
Just execute it to install the package on your computer.

Binary packages for several Linux distributors are
`maintained <http://wavelets.scipy.org/moin/Download>`_ by
Open Source community contributors. Query your favourite package
manager tool for `python-wavelets`, `python-pywt` or similar package name.

To verify the installation process try running tests and examples from the
`tests <http://projects.scipy.org/wavelets/browser/pywt/trunk/tests/>`_
and `demo <http://projects.scipy.org/wavelets/browser/pywt/trunk/demo/>`_
directories included in the source distribution.
Note that most of the examples relies on the
`matplotlib <http://matplotlib.sourceforge.net>`_ plotting package.

License
-------

|pywt| is a free Open Source software available under the
:download:`MIT license terms <COPYING.txt>`.

Contact
-------

Post your suggestions and guestions to `PyWavelets discussions
group <http://groups.google.com/group/pywavelets>`_ (pywavelets@googlegroups.com).

Comments, bug reports and fixes are welcome through `Github <https://github.com/nigma/pywt>`_ and `Bitbucket <https://bitbucket.org/nigma/pywt>`_ project sites.

You can try to reach me directly at en@ig.ma but I can't promise I will get back to you in a reasonable time.
