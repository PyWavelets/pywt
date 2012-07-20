.. _dev-testing:

Testing
=======

Continous integration with Travis-CI
------------------------------------

The project is using `Travis-CI <http://travis-ci.org/#!/nigma/pywt>`_ service
for continous integration and testing.

Current build status is:

.. image::
    https://secure.travis-ci.org/nigma/pywt.png?branch=develop
    :alt: Build Status
    :target: https://secure.travis-ci.org/nigma/pywt


If you are submitting a patch or pull request please make sure it
does not break the build.


Running tests locally
---------------------

Simply::

  python setup.py test


Running tests with Tox
----------------------

There's also a config file for running tests with Tox (``pip install tox``)::

  tox

It is not however very convenient at the moment because Tox recreates
the test environment (which is a good thing) and builds numpy from
source on every run (which takes a lot of time).
