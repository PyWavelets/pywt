.. _ref-dwt2:

.. currentmodule:: pywt

=================================================
2D Forward and Inverse Discrete Wavelet Transform
=================================================


Single level ``dwt2``
~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: dwt2

The following diagram shows the coefficients packed into a single array
with the default axes. This matches :func:`coeffs_to_array` applied to the
output of :func:`wavedec2` with ``level=1``:

  ::

                                -------------------
                                |        |        |
                                | cA(LL) | cV(LH) |
                                |        |        |
    (cA, (cH, cV, cD))  <--->   -------------------
                                |        |        |
                                | cH(HL) | cD(HH) |
                                |        |        |
                                -------------------

:func:`dwt2` returns separate arrays for direct access to each subband.


Single level ``idwt2``
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: idwt2

2D multilevel decomposition using ``wavedec2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: wavedec2

2D multilevel reconstruction using ``waverec2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: waverec2


2D coordinate conventions
~~~~~~~~~~~~~~~~~~~~~~~~~

The labels for "horizontal" and "vertical" used by ``dwt2`` and ``idwt2``
follow the common mathematical convention that coordinate axis 0
is horizontal while axis 1 is vertical::

    dwt2, idwt2 convention
    ----------------------

    axis 1 ^
           |
           |
           |
           |--------->
                   axis 0

Note that this is different from another common convention used in computer
graphics and image processing (e.g. by matplotlib's ``imshow`` and functions in
``scikit-image``).  In those packages axis 0 is a vertical axis and axis 1 is
horizontal as follows::

     imshow convention
    -------------------
                 axis 1
           |--------->
           |
           |
           |
    axis 0 v
