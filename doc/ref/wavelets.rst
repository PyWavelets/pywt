.. _ref-wavelets:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

========
Wavelets
========

Wavelet ``families()``
----------------------

.. function:: families()

  Returns a list of available built-in wavelet families. Currently the built-in
  families are:

  * Haar (``haar``)
  * Daubechies (``db``)
  * Symlets (``sym``)
  * Coiflets (``coif``)
  * Biorthogonal (``bior``)
  * Reverse biorthogonal (``rbio``)
  * `"Discrete"` FIR approximation of Meyer wavelet (``dmey``)

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> print pywt.families()
    ['haar', 'db', 'sym', 'coif', 'bior', 'rbio', 'dmey']


Built-in wavelets - ``wavelist()``
----------------------------------

.. function:: wavelist([family])

  The :func:`wavelist` function returns a list of names of the built-in
  wavelets.

  If the *family* name is ``None`` then names of all the built-in wavelets
  are returned. Otherwise the function returns names of wavelets that belong
  to the given family.

  **Example:**

  .. sourcecode:: python

    >>> import pywt
    >>> print pywt.wavelist('coif')
    ['coif1', 'coif2', 'coif3', 'coif4', 'coif5']

  Custom user wavelets are also supported through the :class:`Wavelet` object
  constructor as described below.


``Wavelet`` object
------------------

.. class:: Wavelet(name[, filter_bank=None])

  Describes properties of a wavelet identified by the specified wavelet *name*.
  In order to use a built-in wavelet the *name* parameter must be a valid
  wavelet name from the :func:`pywt.wavelist` list.

  Custom Wavelet objects can be created by passing a user-defined filters set
  with the *filter_bank* parameter.

  :param name: Wavelet name
  :param filter_bank: Use a user supplied filter bank instead of a built-in :class:`Wavelet`.

  The filter bank object can be a list of four filters coefficients or an object
  with :attr:`~Wavelet.filter_bank` attribute, which returns a list of such
  filters in the following order::

    [dec_lo, dec_hi, rec_lo, rec_hi]

  .. note::

    The :meth:`~Wavelet.get_filters_coeffs` method is kept for compatibility
    with the previous versions of |pywt|, but may be removed in a future version
    of the package.

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

      The :meth:`~Wavelet.get_filters_coeffs` method is deprecated.

  .. attribute:: inverse_filter_bank

      Returns list of reverse wavelet filters coefficients. The mapping from the
      `filter_coeffs` list is as follows::

        [rec_lo[::-1], rec_hi[::-1], dec_lo[::-1], dec_hi[::-1]]

      The :meth:`~Wavelet.get_reverse_filters_coeffs` method is deprecated.

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

    >>> import pywt
    >>> wavelet = pywt.Wavelet('db1')
    >>> print wavelet
    Wavelet db1
      Family name:    Daubechies
      Short name:     db
      Filters length: 2
      Orthogonal:     True
      Biorthogonal:   True
      Symmetry:       asymmetric
    >>> print wavelet.dec_lo, wavelet.dec_hi
    [0.70710678118654757, 0.70710678118654757] [-0.70710678118654757, 0.70710678118654757]
    >>> print wavelet.rec_lo, wavelet.rec_hi
    [0.70710678118654757, 0.70710678118654757] [0.70710678118654757, -0.70710678118654757]


Approximating wavelet and scaling functions - ``Wavelet.wavefun()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. method:: Wavelet.wavefun(level)

  .. versionchanged:: 0.2
    The time (space) localisation of approximation function points was
    added.

  The :meth:`~Wavelet.wavefun` method can be used to calculate approximations of
  scaling function (*phi*) and wavelet function (*psi*) at the given level of
  refinement.

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

  .. seealso:: You can find live examples of :meth:`~Wavelet.wavefun` usage and
               images of all the built-in wavelets on the
               `Wavelet Properties Browser <http://wavelets.pybytes.com>`_ page.

.. _using-custom-wavelets:
.. _custom-wavelets:

Using custom wavelets
---------------------

|pywt| comes with a :func:`long list <pywt.wavelist>` of the most popular
wavelets built-in and ready to use. If you need to use a specific wavelet which
is not included in the list it is very easy to do so. Just pass a list of four
filters or an object with a :attr:`~Wavelet.filter_bank` attribute as a
*filter_bank* argument to the :class:`Wavelet` constructor.

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
from plain Python lists of filter coefficients and a *filter bank-like* objects.

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
