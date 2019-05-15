..  -*- rst -*-

=====================
PyWavelets benchmarks
=====================

Benchmarking PyWavelets with Airspeed Velocity.


Usage
-----

Airspeed Velocity manages building and Python virtualenvs (or conda
environments) by itself, unless told otherwise. To run the benchmarks, you do
not need to install a development version of PyWavelets to your current Python environment.

First navigate to the benchmarks subfolder of the repository.

    cd benchmarks

To run all benchmarks against the current build of PyWavelets::

    asv run --python=same --quick

The following notation (tag followed by ^!) can be used to run only on a
specific tag or commit.  (In this case, a python version for the virtualenv
must be provided)

    asv run --python=3.5 --quick v0.4.0^!

To record the results use:

    asv publish

And to see the results via a web browser, run:

    asv preview

More on how to use ``asv`` can be found in `ASV documentation`_
Command-line help is available as usual via ``asv --help`` and
``asv run --help``.

.. _ASV documentation: https://asv.readthedocs.io/


Writing benchmarks
------------------

See `ASV documentation`_ for basics on how to write benchmarks.

Some things to consider:

-   The benchmark files need to be importable when benchmarking old versions
  of PyWavelets. So if anything from PyWavelets is imported at the top level,
  it should be done as:

      try:
          from pywt import cwt
      except ImportError:
          pass

  The benchmarks themselves don't need any guarding against missing features
  --- only the top-level imports.

  To allow tests of newer functions to be marked as "n/a" (not available)
  rather than "failed" for older versions, the setup method itself can raise a NotImplemented error.  See the following example for the CWT:

      try:
          from pywt import cwt
      except ImportError:
          raise NotImplementedError("cwt not available")

- Try to keep the runtime of the benchmark reasonable.

- Use ASV's ``time_`` methods for benchmarking times rather than cooking up
  time measurements via ``time.clock``, even if it requires some juggling when
  writing the benchmark.

- Preparing arrays etc. should generally be put in the ``setup`` method rather
  than the ``time_`` methods, to avoid counting preparation time together with
  the time of the benchmarked operation.

