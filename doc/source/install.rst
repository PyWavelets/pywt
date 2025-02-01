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
(any common one will work) installed on your system.  Navigate to the
PyWavelets source code directory (containing ``pyproject.toml.py``) and type::

    pip install .

For the requirements needed to build from source are (Python, NumPy and Cython
minimum versions in particular), see ``pyproject.toml``.

To run all the tests for PyWavelets, you will also need to install the
Matplotlib_ package.

.. seealso::  The :ref:`Development guide <dev-index>` section contains more
              information on building and installing from source code.

.. include:: common_refs.rst
