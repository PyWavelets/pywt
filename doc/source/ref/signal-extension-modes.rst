.. _ref-modes:

.. currentmodule:: pywt


======================
Signal extension modes
======================

.. _Modes:

Because the most common and practical way of representing digital signals
in computer science is with finite arrays of values, some extrapolation
of the input data has to be performed in order to extend the signal before
computing the :ref:`Discrete Wavelet Transform <ref-dwt>` using the cascading
filter banks algorithm.

Depending on the extrapolation method, significant artifacts at the signal's
borders can be introduced during that process, which in turn may lead to
inaccurate computations of the :ref:`DWT <ref-dwt>` at the signal's ends.

PyWavelets provides several methods of signal extrapolation that can be used to
minimize this negative effect:

  .. _`Modes.zero`:

  * ``zero`` - **zero-padding** - signal is extended by adding zero samples::

      ... 0  0 | x1 x2 ... xn | 0  0 ...

  .. _`Modes.constant`:

  * ``constant`` - **constant-padding** - border values are replicated::

      ... x1 x1 | x1 x2 ... xn | xn xn ...

  .. _`Modes.symmetric`:

  * ``symmetric`` - **symmetric-padding** - signal is extended by *mirroring*
    samples. This mode is also known as half-sample symmetric.::

      ... x2 x1 | x1 x2 ... xn | xn xn-1 ...

  .. _`Modes.reflect`:

  * ``reflect`` - **reflect-padding** - signal is extended by *reflecting*
    samples. This mode is also known as whole-sample symmetric.::

      ... x3 x2 | x1 x2 ... xn | xn-1 xn-2 ...

  .. _`Modes.periodic`:
  .. _`periodic-padding`:

  * ``periodic`` - **periodic-padding** - signal is treated as a periodic one::

      ... xn-1 xn | x1 x2 ... xn | x1 x2 ...

  .. _`Modes.smooth`:

  * ``smooth`` - **smooth-padding** - signal is extended according to the first
    derivatives calculated on the edges (straight line)

  .. _`Modes.antisymmetric`:

  * ``antisymmetric`` - **anti-symmetric padding** - signal is extended by
    *mirroring* and negating samples. This mode is also known as half-sample
    anti-symmetric::

      ... -x2 -x1 | x1 x2 ... xn | -xn -xn-1 ...

  .. _`Modes.antireflect`:

  * ``antireflect`` - **anti-symmetric-reflect padding** - signal is extended by
    *reflecting* anti-symmetrically about the edge samples. This mode is also
    known as whole-sample anti-symmetric::

      ... (2*x1 - x3) (2*x1 - x2) | x1 x2 ... xn | (2*xn - xn-1) (2*xn - xn-2) ...

:ref:`DWT <ref-dwt>` performed for these extension modes is slightly redundant, but ensures
perfect reconstruction. To receive the smallest possible number of coefficients,
computations can be performed with the `periodization`_ mode:

  .. _`periodization`:
  .. _`Modes.periodization`:

  * ``periodization`` - **periodization** - is like `periodic-padding`_ but gives the
    smallest possible number of decomposition coefficients. :ref:`IDWT <ref-idwt>` must be
    performed with the same mode.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> print(pywt.Modes.modes)
    ['zero', 'constant', 'symmetric', 'periodic', 'smooth', 'periodization', 'reflect', 'antisymmetric', 'antireflect']

The following figure illustrates how a short signal (red) gets extended (black)
outside of its original extent. Note that periodization first extends the
signal to an even length prior to using periodic boundary conditions.

.. plot:: pyplots/plot_boundary_modes.py

Notice that you can use any of the following ways of passing wavelet and mode
parameters:

.. sourcecode:: python

  >>> import pywt
  >>> (a, d) = pywt.dwt([1,2,3,4,5,6], 'db2', 'smooth')
  >>> (a, d) = pywt.dwt([1,2,3,4,5,6], pywt.Wavelet('db2'), pywt.Modes.smooth)

.. note::
    Extending data in context of PyWavelets does not mean reallocation of the
    data in the computer's physical memory and copying values, but rather
    computing the extra values only when they are needed.
    This feature saves extra memory and CPU resources and helps to avoid page
    swapping when handling relatively big data arrays on computers with low
    physical memory.

Naming Conventions
------------------
The correspondence between PyWavelets edge modes and the extension modes
available in Matlab's dwtmode and numpy's pad are tabulated here for reference.

================== ============= ===========================
**PyWavelets**     **Matlab**    **numpy.pad**
================== ============= ===========================
symmetric          sym, symh     symmetric
reflect            symw          reflect
smooth             spd, sp1      N/A
constant           sp0           edge
zero               zpd           constant, cval=0
periodic           ppd           wrap
periodization      per           N/A
antisymmetric      asym, asymh   N/A
antireflect        asymw         reflect, reflect_type='odd'
================== ============= ===========================

Padding using PyWavelets Signal Extension Modes - ``pad``
---------------------------------------------------------

.. autofunction:: pad

Pywavelets provides a function, :func:`pad`, that operate like
:func:`numpy.pad`, but supporting the PyWavelets signal extension modes
discussed above. For efficiency, the DWT routines in PyWavelets do not
expclitly create padded signals using this function. It can be used to manually
prepad signals to reduce boundary effects in functions such as :func:`cwt` and
:func:`swt` that do not currently support all of these signal extension modes.
