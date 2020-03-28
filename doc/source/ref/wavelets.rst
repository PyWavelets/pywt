.. _ref-wavelets:

.. currentmodule:: pywt

========
Wavelets
========

Wavelet ``families()``
----------------------

.. autofunction:: families


Built-in wavelets - ``wavelist()``
----------------------------------

.. autofunction:: wavelist

Custom discrete wavelets are also supported through the
:class:`Wavelet` object constructor as described below.


``Wavelet`` object
------------------

.. class:: Wavelet(name[, filter_bank=None])

  Describes properties of a discrete wavelet identified by the specified
  wavelet ``name``. For continuous wavelets see :class:`pywt.ContinuousWavelet`
  instead. In order to use a built-in wavelet the ``name`` parameter must be a
  valid wavelet name from the :func:`pywt.wavelist` list.

  Custom Wavelet objects can be created by passing a user-defined filters set
  with the ``filter_bank`` parameter.

  :param name: Wavelet name
  :param filter_bank: Use a user supplied filter bank instead of a built-in :class:`Wavelet`.

  The filter bank object can be a list of four filters coefficients or an object
  with :attr:`~Wavelet.filter_bank` attribute, which returns a list of such
  filters in the following order::

    [dec_lo, dec_hi, rec_lo, rec_hi]

  Wavelet objects can also be used as a base filter banks. See section on
  :ref:`using custom wavelets <custom-wavelets>` for more information.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet = pywt.Wavelet('db1')

  .. attribute:: name

      Wavelet name.

  .. attribute:: short_name

      Short wavelet name.

  .. attribute:: dec_lo

      Decomposition filter values.

  .. attribute:: dec_hi

      Decomposition filter values.

  .. attribute:: rec_lo

      Reconstruction filter values.

  .. attribute:: rec_hi

      Reconstruction filter values.

  .. attribute:: dec_len

      Decomposition filter length.

  .. attribute:: rec_len

      Reconstruction filter length.

  .. attribute:: filter_bank

      Returns filters list for the current wavelet in the following order::

        [dec_lo, dec_hi, rec_lo, rec_hi]

  .. attribute:: inverse_filter_bank

      Returns list of reverse wavelet filters coefficients. The mapping from
      the ``filter_coeffs`` list is as follows::

        [rec_lo[::-1], rec_hi[::-1], dec_lo[::-1], dec_hi[::-1]]

  .. attribute:: short_family_name

      Wavelet short family name

  .. attribute:: family_name

      Wavelet family name

  .. attribute:: orthogonal

      Set if wavelet is orthogonal

  .. attribute:: biorthogonal

      Set if wavelet is biorthogonal

  .. attribute:: symmetry

      ``asymmetric``, ``near symmetric``, ``symmetric``

  .. attribute:: vanishing_moments_psi

      Number of vanishing moments for the wavelet function

  .. attribute:: vanishing_moments_phi

      Number of vanishing moments for the scaling function

  **Example:**

  .. sourcecode:: python

    >>> def format_array(arr):
    ...     return "[%s]" % ", ".join(["%.14f" % x for x in arr])

    >>> import pywt
    >>> wavelet = pywt.Wavelet('db1')
    >>> print(wavelet)
    Wavelet db1
      Family name:    Daubechies
      Short name:     db
      Filters length: 2
      Orthogonal:     True
      Biorthogonal:   True
      Symmetry:       asymmetric
      DWT:            True
      CWT:            False
    >>> print(format_array(wavelet.dec_lo), format_array(wavelet.dec_hi))
    [0.70710678118655, 0.70710678118655] [-0.70710678118655, 0.70710678118655]
    >>> print(format_array(wavelet.rec_lo), format_array(wavelet.rec_hi))
    [0.70710678118655, 0.70710678118655] [0.70710678118655, -0.70710678118655]


Approximating wavelet and scaling functions - ``Wavelet.wavefun()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. method:: Wavelet.wavefun(level)

  .. versionchanged:: 0.2
    The time (space) localisation of approximation function points was
    added.

  The :meth:`~Wavelet.wavefun` method can be used to calculate approximations of
  scaling function (``phi``) and wavelet function (``psi``) at the given level
  of refinement.

  For :attr:`orthogonal <Wavelet.orthogonal>` wavelets returns approximations of
  scaling function and wavelet function with corresponding x-grid coordinates::

    [phi, psi, x] = wavelet.wavefun(level)

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet = pywt.Wavelet('db2')
    >>> phi, psi, x = wavelet.wavefun(level=5)

  For other (:attr:`biorthogonal <Wavelet.biorthogonal>` but not
  :attr:`orthogonal <Wavelet.orthogonal>`) wavelets returns approximations of
  scaling and wavelet function both for decomposition and reconstruction and
  corresponding x-grid coordinates::

    [phi_d, psi_d, phi_r, psi_r, x] = wavelet.wavefun(level)

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet = pywt.Wavelet('bior3.5')
    >>> phi_d, psi_d, phi_r, psi_r, x = wavelet.wavefun(level=5)

  .. See also plots of Daubechies and Symlets wavelet families generated using
     the :meth:`~Wavelet.wavefun` function:

    - `db.png`_
    - `sym.png`_

  .. seealso::
      You can find live examples of :meth:`~Wavelet.wavefun` usage and
      images of all the built-in wavelets on the
      `Wavelet Properties Browser <http://wavelets.pybytes.com>`_ page.
      However, **this website is no longer actively maintained** and does not
      include every wavelet present in PyWavelets. The precision of the wavelet
      coefficients at that site is also lower than those included in
      PyWavelets.

.. _using-custom-wavelets:
.. _custom-wavelets:

Using custom wavelets
---------------------

PyWavelets comes with a :func:`long list <pywt.wavelist>` of the most popular
wavelets built-in and ready to use. If you need to use a specific wavelet which
is not included in the list it is very easy to do so. Just pass a list of four
filters or an object with a :attr:`~Wavelet.filter_bank` attribute as a
``filter_bank`` argument to the :class:`Wavelet` constructor.

.. compound::

    The filters list, either in a form of a simple Python list or returned via
    the :attr:`~Wavelet.filter_bank` attribute, must be in the following order:

      * lowpass decomposition filter
      * highpass decomposition filter
      * lowpass reconstruction filter
      * highpass reconstruction filter

    just as for the :attr:`~Wavelet.filter_bank` attribute of the
    :class:`Wavelet` class.

The Wavelet object created in this way is a standard :class:`Wavelet` instance.

The following example illustrates the way of creating custom Wavelet objects
from plain Python lists of filter coefficients and a *filter bank-like* object.

  **Example:**

  .. sourcecode:: python

    >>> import pywt, math
    >>> c = math.sqrt(2)/2
    >>> dec_lo, dec_hi, rec_lo, rec_hi = [c, c], [-c, c], [c, c], [c, -c]
    >>> filter_bank = [dec_lo, dec_hi, rec_lo, rec_hi]
    >>> myWavelet = pywt.Wavelet(name="myHaarWavelet", filter_bank=filter_bank)
    >>>
    >>> class HaarFilterBank(object):
    ...     @property
    ...     def filter_bank(self):
    ...         c = math.sqrt(2)/2
    ...         dec_lo, dec_hi, rec_lo, rec_hi = [c, c], [-c, c], [c, c], [c, -c]
    ...         return [dec_lo, dec_hi, rec_lo, rec_hi]
    >>> filter_bank = HaarFilterBank()
    >>> myOtherWavelet = pywt.Wavelet(name="myHaarWavelet", filter_bank=filter_bank)


``ContinuousWavelet`` object
----------------------------

.. class:: ContinuousWavelet(name, dtype=np.float64)

  Describes properties of a continuous wavelet identified by the specified wavelet ``name``.
  In order to use a built-in wavelet the ``name`` parameter must be a valid
  wavelet name from the :func:`pywt.wavelist` list.

  :param name: Wavelet name
  :param dtype: numpy.dtype to use for the wavelet. Can be numpy.float64 or numpy.float32.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet = pywt.ContinuousWavelet('gaus1')

  .. attribute:: name

      Continuous Wavelet name.

  .. attribute:: short_family_name

      Wavelet short family name

  .. attribute:: family_name

      Wavelet family name

  .. attribute:: orthogonal

      Set if wavelet is orthogonal

  .. attribute:: biorthogonal

      Set if wavelet is biorthogonal

  .. attribute:: complex_cwt

      Returns if wavelet is complex

  .. attribute:: lower_bound

      Set the lower bound of the effective support

  .. attribute:: upper_bound

      Set the upper bound of the effective support

  .. attribute:: center_frequency

      Set the center frequency for the shan, fbsp and cmor wavelets

  .. attribute:: bandwidth_frequency

      Set the bandwidth frequency for the shan, fbsp and cmor wavelets

  .. attribute:: fbsp_order

      Set the order for the fbsp wavelet

  .. attribute:: symmetry

      ``asymmetric``, ``near symmetric``, ``symmetric``, ``anti-symmetric``

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet = pywt.ContinuousWavelet('gaus1')
    >>> print(wavelet)
    ContinuousWavelet gaus1
      Family name:    Gaussian
      Short name:     gaus
      Symmetry:       anti-symmetric
      DWT:            False
      CWT:            True
      Complex CWT:    False

Approximating wavelet functions - ``ContinuousWavelet.wavefun()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. method:: ContinuousWavelet.wavefun(level, length = None)


  The :meth:`~ContinuousWavelet.wavefun` method can be used to calculate approximations of
  scaling function (``psi``) with grid (``x``). The vector length is set by ``length``.
  The vector length can also be defined by ``2**level`` if ``length`` is not set.

  For :attr:`complex_cwt <ContinuousWavelet.complex_cwt>` wavelets returns a complex approximations of
  wavelet function with corresponding x-grid coordinates::

    [psi, x] = wavelet.wavefun(level)

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet = pywt.ContinuousWavelet('gaus1')
    >>> psi, x = wavelet.wavefun(level=5)

Approximating wavelet functions - ``ContinuousWavelet.wavefun()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. method:: DiscreteContinuousWavelet(name, [filter_bank = None])


  The :meth:`~DiscreteContinuousWavelet` returns a
    Wavelet or a ContinuousWavelet object depending on the given name.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> wavelet = pywt.DiscreteContinuousWavelet('db1')
    >>> print(wavelet)
    Wavelet db1
      Family name:    Daubechies
      Short name:     db
      Filters length: 2
      Orthogonal:     True
      Biorthogonal:   True
      Symmetry:       asymmetric
      DWT:            True
      CWT:            False
    >>> wavelet = pywt.DiscreteContinuousWavelet('gaus1')
    >>> print(wavelet)
    ContinuousWavelet gaus1
      Family name:    Gaussian
      Short name:     gaus
      Symmetry:       anti-symmetric
      DWT:            False
      CWT:            True
      Complex CWT:    False
