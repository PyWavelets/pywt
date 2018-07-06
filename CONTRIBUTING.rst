==================================
PyWavelets pull request guidelines
==================================

Pull requests are always welcome, and the PyWavelets community appreciates
any help you give.

When submitting a pull request, we ask you check the following:

1. **Unit tests**, **documentation**, and **code style** are in order.
   See below for details.

   It's also OK to submit work in progress if you're unsure of what
   this exactly means, in which case you'll likely be asked to make
   some further changes.

2. The contributed code will be **licensed under PyWavelets's license**,
   (the MIT license, https://github.com/PyWavelets/pywt/blob/master/LICENSE).
   If you did not write the code yourself, you ensure the existing
   license is compatible and include the license information in the
   contributed files, or obtain a permission from the original
   author to relicense the contributed code.


Coding guidelines
=================

1. Unit tests
    In principle you should aim to create unit tests that exercise all the code
    that you are adding.  This gives some degree of confidence that your code
    runs correctly, also on Python versions and hardware or OSes that you don't
    have available yourself.  An extensive description of how to write unit
    tests is given in the NumPy `testing guidelines`_.

2. Documentation
    Clear and complete documentation is essential in order for users to be able
    to find and understand the code.  Documentation for individual functions
    and classes -- which includes at least a basic description, type and
    meaning of all parameters and returns values, and usage examples in
    `doctest`_ format -- is put in docstrings.  Those docstrings can be read
    within the interpreter, and are compiled into a reference guide in html and
    pdf format.  Higher-level documentation for key (areas of) functionality is
    provided in tutorial format and/or in module docstrings.  A guide on how to
    write documentation is given in the `numpydoc docstring guide`_.

3. Code style
    Uniformity of style in which code is written is important to others trying
    to understand the code.  PyWavelets follows the standard Python guidelines
    for code style, `PEP8`_.  In order to check that your code conforms to
    PEP8, you can use the `pep8 package`_ style checker.  Most IDEs and text
    editors have settings that can help you follow PEP8, for example by
    translating tabs by four spaces.  Using `pyflakes`_ to check your code is
    also a good idea.


.. _PEP8: http://www.python.org/dev/peps/pep-0008/

.. _pep8 package: http://pypi.python.org/pypi/pep8

.. _numpydoc docstring guide: https://numpydoc.readthedocs.io/en/latest/

.. _doctest: http://www.doughellmann.com/PyMOTW/doctest/

.. _pyflakes: http://pypi.python.org/pypi/pyflakes

.. _testing guidelines: https://github.com/numpy/numpy/blob/master/doc/TESTS.rst.txt
