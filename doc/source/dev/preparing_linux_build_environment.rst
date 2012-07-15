.. _dev-preparing-linux-build-environment:

.. module:: pywt
.. include:: ../substitutions.rst

Prepare Linux build environment
===============================

There is a good chance that you already have a working build environment.
Just skip steps that you don't need to execute.


Install basic build tools
-------------------------

Note that the example below uses ``aptitude`` package manager, which is
specific to Debian and Ubuntu Linux distributions. Use your favourite package
manager to install these packages on your OS.

::

    aptitude install build-essential gcc python-dev git-core


Next steps
----------

After completing these steps continue with
:ref:`Installing build dependencies <dev-installing-build-dependencies>`.
