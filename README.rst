+---------------+-----------------+
| Service       | Master branch   |
+===============+=================+
| GitHub        | |ghactions_ci|  |
+---------------+-----------------+
| Appveyor      | |appveyor_ci|   |
+---------------+-----------------+
| Read the Docs | |read_the_docs| |
+---------------+-----------------+


.. |ghactions_ci| image:: https://github.com/PyWavelets/pywt/actions/workflows/tests.yml/badge.svg?branch=main
   :alt: Build Status
   :target: https://github.com/PyWavelets/pywt/actions/workflows/tests.yml?query=branch%3Amain

.. |appveyor_ci| image:: https://ci.appveyor.com/api/projects/status/github/PyWavelets/pywt
   :align: middle
   :target: https://ci.appveyor.com/project/PyWavelets/pywt
   :alt: Appveyor Status

.. |read_the_docs| image:: https://readthedocs.org/projects/pywavelets/badge/?version=latest
   :align: middle
   :target: https://pywavelets.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


PyWavelets
==========

.. contents::

What is PyWavelets
------------------

PyWavelets is a free Open Source library for wavelet transforms in Python.
Wavelets are mathematical basis functions that are localized in both time and
frequency.  Wavelet transforms are time-frequency transforms employing
wavelets.  They are similar to Fourier transforms, the difference being that
Fourier transforms are localized only in frequency instead of in time and
frequency.

The main features of PyWavelets are:

  * 1D, 2D and nD Forward and Inverse Discrete Wavelet Transform (DWT and IDWT)
  * 1D, 2D and nD Multilevel DWT and IDWT
  * 1D and 2D Stationary Wavelet Transform (Undecimated Wavelet Transform)
  * 1D and 2D Wavelet Packet decomposition and reconstruction
  * 1D Continuous Wavelet Transform
  * Computing Approximations of wavelet and scaling functions
  * Over 100 `built-in wavelet filters`_ and support for custom wavelets
  * Single and double precision calculations
  * Real and complex calculations
  * Results compatible with Matlab Wavelet Toolbox (TM)


Documentation
-------------

Documentation with detailed examples and links to more resources is available
online at http://pywavelets.readthedocs.org.

For more usage examples see the `demo`_ directory in the source package.


Installation
------------

PyWavelets supports `Python`_ >=3.10, and is only dependent on `NumPy`_
(supported versions are currently ``>= 1.23.0``). To pass all of the tests,
`Matplotlib`_ is also required.

There are binary wheels for Intel Linux, Windows and macOS / OSX on PyPi.  If
you are on one of these platforms, you should get a binary (precompiled)
installation with::

    pip install PyWavelets

Users of the Anaconda_ Python distribution may wish to obtain pre-built
Windows, Intel Linux or macOS / OSX binaries from the conda-forge channel.
This can be done via::

    conda install -c conda-forge pywavelets

Several Linux distributions have their own packages for PyWavelets, but these
tend to be moderately out of date.  Query your Linux package manager tool for
``python-pywavelets``, ``python-wavelets``, ``python-pywt`` or a similar
package name.

If you want or need to install from source, you will need a working C compiler
(any common one will work) and a recent version of `Cython`_.  Navigate to the
PyWavelets source code directory (containing ``pyproject.toml``) and type::

    pip install .

The most recent *development* version can be found on GitHub at
https://github.com/PyWavelets/pywt.

The latest release, including source and binary packages for Intel Linux,
macOS and Windows, is available for download from the `Python Package Index`_.
You can find source releases at the `Releases Page`_.

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

As of 2019, PyWavelets development is supported in part by Tidelift.
`Help support PyWavelets with the Tidelift Subscription <https://tidelift.com/subscription/pkg/pypi-pywavelets?utm_source=pypi-pywavelets&utm_medium=referral&utm_campaign=readme>`_


Contact
-------

Use `GitHub Issues`_ or the `mailing list`_ to post your comments or questions.

**Report a security vulnerability:** https://tidelift.com/security

License
-------

PyWavelets is a free Open Source software released under the MIT license.

If you wish to cite PyWavelets in a publication, please use the following
JOSS publication.

.. image:: http://joss.theoj.org/papers/10.21105/joss.01237/status.svg
   :target: https://doi.org/10.21105/joss.01237

Specific releases can also be cited via Zenodo. The DOI below will correspond
to the most recent release. DOIs for past versions can be found by following
the link in the badge below to Zenodo:

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1407171.svg
   :target: https://doi.org/10.5281/zenodo.1407171

.. _built-in wavelet filters: http://wavelets.pybytes.com/
.. _Cython: http://cython.org/
.. _demo: https://github.com/PyWavelets/pywt/tree/main/demo
.. _Anaconda: https://www.continuum.io
.. _GitHub: https://github.com/PyWavelets/pywt
.. _GitHub Issues: https://github.com/PyWavelets/pywt/issues
.. _NumPy: https://www.numpy.org
.. _SciPy: https://www.scipy.org
.. _original developer: http://en.ig.ma
.. _Python: http://python.org/
.. _Python Package Index: http://pypi.python.org/pypi/PyWavelets/
.. _mailing list: http://groups.google.com/group/pywavelets
.. _Releases Page: https://github.com/PyWavelets/pywt/releases
.. _Matplotlib: http://matplotlib.org
