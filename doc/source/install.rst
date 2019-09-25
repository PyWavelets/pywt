Installing
==========

The latest release, including binary packages for Windows, macOS and Linux,
is available for download from `PyPI`_.  You can also find source releases at
the `Releases Page`_.

You can install PyWavelets with::

    pip install PyWavelets

Users of the Anaconda_ Python distribution may wish to obtain pre-built
Windows, Intel Linux or macOS / OSX binaries from the main or conda-forge
channel::

    conda install pywavelets

Several Linux distributions have their own packages for PyWavelets, but these
tend to be moderately out of date.  Query your Linux package manager tool for
``python-pywavelets``, ``python-wavelets``, ``python-pywt`` or a similar
package name.


Building from source
--------------------

The most recent *development* version can be found on GitHub at
https://github.com/PyWavelets/pywt.

The latest release, is available for download from `PyPI`_ or on the
`Releases Page`_.

If you want or need to install from source, you will need a working C compiler
(any common one will work) and a recent version of `Cython`_.  Navigate to the
PyWavelets source code directory (containing ``setup.py``) and type::

    pip install .

The requirements needed to build from source are:

 - Python_ 2.7 or >=3.4
 - NumPy_ >= 1.13.3
 - Cython_ >= 0.23.5  (if installing from git, not from a PyPI source release)

To run all the tests for PyWavelets, you will also need to install the
Matplotlib_ package. If SciPy_ is available, FFT-based continuous wavelet
transforms will use the FFT implementation from SciPy instead of NumPy.

.. seealso::  :ref:`Development guide <dev-index>` section contains more
              information on building and installing from source code.

.. include:: common_refs.rst
