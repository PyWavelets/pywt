.. _dev-testing:

Testing
=======

Continous integration with Travis-CI
------------------------------------

The project is using `Travis-CI <https://travis-ci.org/PyWavelets/pywt>`_ service
for continuous integration and testing.

Current build status is:

.. image::
    https://secure.travis-ci.org/PyWavelets/pywt.png?branch=master
    :alt: Build Status
    :target: https://secure.travis-ci.org/PyWavelets/pywt

If you are submitting a patch or pull request please make sure it
does not break the build.


Running tests locally
---------------------

Tests are implemented with `pytest`_, so use one of:

    $ pytest --pyargs pywt -v

There are also older doctests that can be run by performing the following from
the root of the project source.

    $ python pywt/tests/test_doc.py
    $ cd doc
    $ make doctest

Additionally the examples in the demo subfolder can be checked by running:

    $ python util/refguide_check.py

Note: doctests require `Matplotlib`_ in addition to the usual dependencies.


Running tests with Tox
----------------------

There's also a config file for running tests with `Tox`_ (``pip install tox``).
To for example run tests for Python 3.7 and 3.8 use::

  tox -e py37,py38

For more information see the `Tox`_ documentation.


.. _pytest: https://pytest.org
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Matplotlib: https://matplotlib.org
