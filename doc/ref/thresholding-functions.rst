.. _ref-thresholding:

.. module:: pywt.thresholding
.. include:: ../substitutions.rst


Thresholding functions
======================

The :mod:`~pywt.thresholding` helper module implements the most popular signal
thresholding functions.


Hard thresholding
-----------------

.. function:: hard(data, value[, substitute=0])

   Hard thresholding. Replace all *data* values with *substitute* where their
   absolute value is less than the *value* param.

   *Data* values with absolute value greater or equal to the thresholding
   *value* stay untouched.

   :param data: numeric data
   :param value: thresholding value
   :param substitute: substitute value
   :returns: array


Soft thresholding
-----------------
.. function:: soft(data, value[, substitute=0])

   Soft thresholding.

   :param data: numeric data
   :param value: thresholding value
   :param substitute: substitute value
   :returns: array

Greater
-------

.. function:: greater(data, value[, substitute=0])

   Replace *data* with *substitute* where *data* is below the thresholding
   *value*.

   `Greater` *data* values pass untouched.

   :param data: numeric data
   :param value: thresholding value
   :param substitute: substitute value
   :returns: array

Less
----

.. function:: less(data, value[, substitute=0])

   Replace *data* with *substitute* where *data* is above the thresholding
   *value*.

   `Less` *data* values pass untouched.

   :param data: numeric data
   :param value: thresholding value
   :param substitute: substitute value
   :returns: array
