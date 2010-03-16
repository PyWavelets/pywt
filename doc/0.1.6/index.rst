=================================================
PyWavelets - Discrete Wavelet Transform in Python
=================================================

User Guide
==========

:Author: Filip Wasilewski
:Contact: filip.wasilewski@gmail.com
:Version: 0.1.6
:Status: alpha
:Date: |date|
:License: `MIT`_

:Abstract: |pywt| is a `Python`_ module for computing forward and inverse
  1D and 2D Discrete Wavelet Transform, Stationary Wavelet Transform and Wavelet Packets
  decomposition and reconstruction.
  This document is a User Guide to |pywt|.

.. |date| date:: %Y-%m-%d %H:%M
.. _MIT: COPYING.txt

.. meta::
   :keywords: pywavelets wavelets discrete wavelet transform Python module dwt idwt swt wavelet packets
   :description lang=en: Python discrete wavelet transform module

.. contents:: Table of Contents
    :local:
    :depth: 2

.. section-numbering:: 
    :depth: 3
    :suffix: .
    
Introduction
------------

Requirements
~~~~~~~~~~~~

|pywt| was originally developed using `MinGW`_ C compiler, `Pyrex`_ and
`Python`_ 2.4 on 32-bit WindowsXP platform. Recent release adds support
for Python 2.5. 

The only external requirement is a recent version of
`NumPy`_ numeric array module.

.. _Pyrex: http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/
.. _MinGW: http://www.mingw.org/
.. _NumPy: http://www.scipy.org/
.. _Python: http://python.org/ 


Download
~~~~~~~~

Current release, including source and binary versions for Windows, is available
for download from Python Cheese Shop directory at:

    http://cheeseshop.python.org/pypi/PyWavelets/

The latest *development* version can be downloaded from
`wavelets.scipy.org`_ SVN `repository`_::

    svn co http://wavelets.scipy.org/svn/multiresolution/pywt/trunk pywt

.. _`wavelets.scipy.org`: http://wavelets.scipy.org
.. _`repository`: http://wavelets.scipy.org/svn/multiresolution/pywt/trunk


Install
~~~~~~~

The most convenient way to install PyWavelets is to use setuptools_
`Easy Install`_ manager::

    easy_install PyWavelets==0.1.6

.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools
.. _`Easy Install`: http://peak.telecommunity.com/DevCenter/EasyInstall#using-easy-install

Please note that in order to build |pywt| from source code you will
need a working C compiler and, in case of source code modifications,
an *updated* version of Pyrex from

    http://codespeak.net/svn/lxml/pyrex/

SVN repository, which includes features and bug fixes not yet available
in the regular Pyrex distribution.

Then in the shell prompt in the |pywt| source code directory type::

    python setupegg.py install

or if using the default distutils manager::

    python setup.py install

For Windows users there is also standard binary installer available
in the Cheese Shop repository. Just download and execute it.

To verify the installation process try running tests and examples
from `tests` and `demo` directories included in the source distribution.
Note that some examples need `matplotlib`_ installed.

.. _matplotlib: http://matplotlib.sourceforge.net


License
~~~~~~~

|pywt| is free Open Source software available under `MIT license`_. Just do no evil.

.. _MIT license: COPYING.txt

Contact
~~~~~~~

Feel free to contact me directly at filip.wasilewski@gmail.com.
Comments, bug reports and fixes are welcome.

You can also use the wiki and trac system available at `wavelets.scipy.org`_
to improve documentation, post cookbook recipes or submit enhancement proposals
or bug reports.


Wavelets
--------

Wavelet ``families``
~~~~~~~~~~~~~~~~~~~~

The ``families()`` function returns names of available built-in wavelet families.
Currently the following wavelet families with over seventy wavelets are available:

* Haar (``haar``)
* Daubechies (``db``)
* Symlets (``sym``)
* Coiflets (``coif``)
* Biorthogonal (``bior``)
* Reverse biorthogonal (``rbio``)
* `"Discrete"` FIR approximation of Meyer wavelet (``dmey``)

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> print pywt.families()
    ['haar', 'db', 'sym', 'coif', 'bior', 'rbio', 'dmey']

.. _`wavelist()`:

Built-in wavelets - ``wavelist``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``wavelist(short_name=None)`` function returns list of available
wavelet names.

If ``short_name`` is None, then names of all implemented wavelets is returned,
otherwise the function returns names of wavelets from given family name.

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> print pywt.wavelist('coif')
    ['coif1', 'coif2', 'coif3', 'coif4', 'coif5']


.. _Wavelet:

``Wavelet`` object
~~~~~~~~~~~~~~~~~~~~

``Wavelet(name, filter_bank=None)`` object describe properties of a wavelet
identified by ``name``. 
In order to use a built-in wavelet the parameter ``name`` must be a valid
name from `wavelist()`_ list. Otherwise a `filter_bank`_ argument must be provided.

name
  Wavelet name

.. _`filter_bank`:

filter_bank
  Use user supplied filter bank instead of built-in ``Wavelet``.
  The filter bank object must implement the
  `get_filters_coeffs()`_ method,
  which returns a list of filters (dec_lo, dec_hi, rec_lo, rec_hi).
  Other Wavelet object can also be used as a filter bank. See section
  on `using custom wavelets`_ for more information.
  
dec_lo, dec_hi
  Decomposition filters values.

rec_lo, rec_hi
  Reconstruction filters values.

dec_len
  Decomposition filter length.

rec_len
  Reconstruction filter length.

.. _`get_filters_coeffs()`:

get_filters_coeffs()
  Returns quadrature mirror filters list for current wavelet (dec_lo, dec_hi, rec_lo, rec_hi)

other properties:
  - family_name
  - short_name
  - orthogonal
  - biorthogonal
  - symmetry - ``asymmetric``, ``near symmetric``, ``symmetric``
  - vanishing_moments_psi
  - vanishing_moments_phi

.. class:: example

  Example:

  .. code-block:: Python

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


``wavefun``
""""""""""""

The ``wavefun(level)`` function can be used to calculates approximations of wavelet function (*psi*)
and associated scaling function (*phi*) at given level of refinement.

For orthogonal wavelet returns scaling and wavelet function.

.. class:: example

  .. code-block:: Python

    >>> import pywt
    >>> wavelet = pywt.Wavelet('db2')
    >>> phi, psi = wavelet.wavefun(level=5)

For biorthogonal wavelet returns scaling and wavelet function both for decomposition
and reconstruction.

.. class:: example

  .. code-block:: Python

    >>> import pywt
    >>> wavelet = pywt.Wavelet('bior1.1')
    >>> phi_d, psi_d, phi_r, psi_r = wavelet.wavefun(level=5)

.. See also plots of Daubechies and Symlets wavelet familes generated with ``wavefun`` function:

    - `db.png`_
    - `sym.png`_


.. _`using custom wavelets`:

Using custom wavelets
~~~~~~~~~~~~~~~~~~~~~~

|pywt| comes with `long list`_ of the most popular wavelets built-in and ready to use.
If there is a need of using a specific wavelet which is not included in the list it is
very easy to create one.
Just pass an object of a class implementing ``get_filters_coeffs()`` method
as a `filter_bank`_ argument of Wavelet_ constructor.

.. _`long list`: `wavelist()`_

The ``get_filters_coeffs()`` method must return a list of four filters:
lowpass decomposition, highpass decomposition, lowpass reconstruction and
highpass reconstruction filter, just as the `get_filters_coeffs()`_ method 
of the Wavelet_ class.

A Wavelet object created in this way is a standard Wavelet_ object and can be used
as any other Wavelet_ object.

.. class:: example

  Example:

  .. code-block:: Python
  
    >>> import pywt, math
    >>> class HaarFilterBank(object):
    ...     def get_filters_coeffs(self):
    ...         c = math.sqrt(2)/2
    ...         dec_lo, dec_hi, rec_lo, rec_hi = [c, c], [-c, c], [c, c], [c, -c]
    ...         return [dec_lo, dec_hi, rec_lo, rec_hi]
    >>> myWavelet = pywt.Wavelet(name="myHaarWavelet", filter_bank=HaarFilterBank())


Discrete Wavelet Transform (DWT)
----------------------------------

Wavelet transform has recently became very popular 
when it comes to analysis, denoising and compression of
signals and images.


.. _dwt:

Single level ``dwt``
~~~~~~~~~~~~~~~~~~~~

The ``dwt`` function is used to perform single level,
one dimensional Discrete Wavelet Transform.
::

  (cA, cD) = dwt(data, wavelet, mode='sym')
  
data
  |data|

wavelet
  |wavelet_arg|

mode
  |mode|

The transform coefficients are returned as two arrays containing
approximation (cA) and detail (cD) coefficients respectively.
Length of returned arrays depends on selected `mode`_ - see `dwt_coeff_len`_:

* for all modes_ except `periodization`_::

    len(cA) == len(cD) == floor((len(data) + wavelet.dec_len - 1) / 2)

* for `periodization`_ mode (`"per"`)::
  
    len(cA) == len(cD) == ceil(len(data) / 2)

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db1')
    >>> print cA
    [ 2.12132034  4.94974747  7.77817459]
    >>> print cD
    [-0.70710678 -0.70710678 -0.70710678]

.. _wavedec:

Multilevel decomposition using ``wavedec``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`(Please note the mode and level arguments order change in 0.1.6 version.)`

The ``wavedec`` function performs 1D multilevel Discrete Wavelet Transform
decomposition of given signal and returns ordered list of coefficients arrays
``[cAn, cDn, cDn-1, ..., cD2, cD1]``, where ``n`` denotes the level of decomposition.
The first element (``cAn``) of the result is approximation coefficients array and
the following elements (``cDn`` - ``cD1``) are details coefficients arrays.

::

  wavedec(data, wavelet, mode='sym', level=None)

data
  |data|

wavelet
  |wavelet_arg|

mode
  |mode|

level
  Decomposition levels count. 
  If the level is None, then full decomposition up to 
  level computed with `dwt_max_level`_ function for corresponding
  data and wavelet lengths is performed. 

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db1', level=2)
    >>> cA2, cD2, cD1 = coeffs
    >>> print cD1
    [-0.70710678 -0.70710678 -0.70710678 -0.70710678]
    >>> print cD2
    [-2. -2.]
    >>> print cA2
    [  5.  13.]
 
.. _`dwt_max_level`:

Maximum decomposition level - ``dwt_max_level``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``dwt_max_level`` function can be used to
compute the maximum useful level of decomposition
for given ``input data length`` and ``wavelet filter length``.

::

  dwt_max_level(data_len, filter_len)

The returned value equals to::

  floor(log(data_len/(filter_len-1))/log(2))

Although the maximum decomposition level can be quite high for long signals,
usually smaller values are chosen.

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> w = pywt.Wavelet('sym5')
    >>> print pywt.dwt_max_level(data_len = 1000, filter_len = w.dec_len)
    6

.. _`dwt_coeff_len`:

Result coefficients length - ``dwt_coeff_len``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Based on input data length, Wavelet decomposition filter length and signal extension `mode`_,
the ``dwt_coeff_len`` function calculates length of result coefficients arrays after `dwt`_.

::

  dwt_coeff_len(data_len, filter_len, mode)

For `periodization`_ mode this equals::

  ceil(data_len / 2)

which is the lowest possible length guaranteeing perfect reconstruction.

For other `modes`_::

  floor((data_len + filter_len - 1) / 2)

.. _mode:
.. _MODES:

Signal extension modes - ``MODES``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To handle problem of border distortion while performing DWT_,
one of several signal extension modes can be selected.

* ``zpd`` - **zero-padding** - signal is extended by adding zero samples::

    0  0 | x1 x2 ... xn | 0  0

* ``cpd`` - **constant-padding** - edge values are used::
  
    x1 x1 | x1 x2 ... xn | xn xn


* ``sym`` - **symmetric-padding** - signal is extended by *mirroring* samples::

    x2 x1 | x1 x2 ... xn | xn xn-1

.. _`periodic-padding`:

* ``ppd`` - **periodic-padding** - signal is treated as periodic::
  
    xn-1 xn | x1 x2 ... xn | x1 x2

* ``sp1`` - **smooth-padding** - signal is extended according to first derivatives
  calculated on the edges
  
DWT_ performed for these extension modes is slightly redundant, but ensure
the perfect reconstruction. To receive the smallest number of coefficients,
DWT_ can be computed with `periodization`_ mode

.. _`periodization`:

* ``per`` - **periodization** - is like `periodic-padding`_ but gives the smallest possible
  number of decomposition coefficients. IDWT_ must be performed with the same mode to
  ensure perfect reconstruction.

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> print pywt.MODES.modes
    ['zpd', 'cpd', 'sym', 'ppd', 'sp1', 'per']


Notice that you can use either of the following forms:  

.. code-block:: Python

  >>> import pywt
  >>> (a, d) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
  >>> (a, d) = pywt.dwt([1,2,3,4,5,6], pywt.Wavelet('db2'), pywt.MODES.sp1)

Note that extending data in context of |pywt| does not really mean reallocating
memory and copying values. Instead of that the extra values are computed only
when needed. This feature saves extra memory and CPU resources and helps to avoid
page swapping when handling relatively big data arrays on computers with low
physical memory.

Inverse Discrete Wavelet Transform (IDWT)
------------------------------------------

.. _idwt:

Single level ``idwt``
~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``idwt`` function reconstructs data from given coefficients by performing
single level Inverse Discrete Wavelet Transform.

::

  idwt(cA, cD, wavelet, mode='sym', correct_size=0)

cA
  approximation coefficients.

cD
  detail coefficients.

wavelet
  |wavelet_arg|

mode
  |mode| This is only important when DWT was performed in `periodization`_ mode.

correct_size
  additional option. Under normal conditions (all data lengths dyadic) Ca and cD
  coefficients lists must have the same lengths. With correct_size set to True,
  length of cA may be greater by one than length of cA.
  This option is very useful when doing multilevel decomposition and reconstruction
  of non-dyadic length signals.

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> print pywt.idwt(cA, cD, 'db2', 'sp1')
    [ 1.  2.  3.  4.  5.  6.]

One of the *cA* and *cD* arguments can be *None*. In that situation
the reconstruction will be performed using only the other one.

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> (cA, cD) = pywt.dwt([1,2,3,4,5,6], 'db2', 'sp1')
    >>> A = pywt.idwt(cA, None, 'db2', 'sp1')
    >>> D = pywt.idwt(None, cD, 'db2', 'sp1')
    >>> print A + D
    [ 1.  2.  3.  4.  5.  6.]


.. _waverec:


Multilevel reconstruction using ``waverec``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Performs multilevel reconstruction of signal from given coefficient list.

::

  waverec(coeffs, wavelet, mode='sym')

coeffs
  coefficients list must be in the form like returned from `wavedec`_ decomposition::
  
  [cAn, cDn, cDn-1, ..., cD2, cD1]

wavelet
  |wavelet_arg|
mode
  |mode|

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> coeffs = pywt.wavedec([1,2,3,4,5,6,7,8], 'db2', level=2)
    >>> print pywt.waverec(coeffs, 'db2')
    [ 1.  2.  3.  4.  5.  6.  7.  8.]

.. _upcoef:

Direct reconstruction with ``upcoef``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Direct reconstruction from coefficients.

::
  
  upcoef(part, coeffs, wavelet, level=1, take=0)

part
  defines coefficients type:

  - **'a'** - approximations reconstruction is performed
  - **'d'** - details reconstruction is performed

coeffs
  coefficients array.
wavele
  |wavelet|
level
  if *level* is specified then multilevel reconstruction is performed
take
  if *take* is specified then only the central part of length equal to
  *'take'* is returned.
  
.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt
    >>> data = [1,2,3,4,5,6]
    >>> (cA, cD) = pywt.dwt(data, 'db2', 'sp1')
    >>> print pywt.upcoef('a', cA, 'db2') + pywt.upcoef('d', cD, 'db2')
    [-0.25       -0.4330127   1.          2.          3.          4.          5.
      6.          1.78589838 -1.03108891]
    >>> n = len(data)
    >>> print pywt.upcoef('a',cA,'db2',take=n) + pywt.upcoef('d',cD,'db2',take=n)
    [ 1.  2.  3.  4.  5.  6.]


2D DWT and IDWT
---------------

.. _dwt2:

Single level ``dwt2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``dwt2`` function performs single level 2D Discrete Wavelet Transform.

::

  dwt2(data, wavelet, mode='sym')

data
  2D input data 

wavelet
  |wavelet_arg|

mode
  |mode| This is only important when DWT was performed in `periodization`_ mode.

Returns one average and three details 2D coefficients arrays. The coefficients
arrays are organized in tuples in the following form::

  (cA, (cH, cV, cD)),

where ``cA``, ``cH``, ``cV``, ``cD`` denotes approximation,
horizontal detail, vertical detail
and diagonal detail coefficients respectively.

.. class:: example

  Example:

  .. code-block:: Python
  
    >>> import pywt, numpy
    >>> data = numpy.ones((4,4), dtype=numpy.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> cA, (cH, cV, cD) = coeffs
    >>> print cA
    [[ 2.  2.]
     [ 2.  2.]]
    >>> print cV
    [[ 0.  0.]
     [ 0.  0.]]


.. _idwt2:

Single level ``idwt2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``idwt2`` function reconstructs data from given coefficients by performing
single level 2D Inverse Discrete Wavelet Transform.

::

  idwt2(coeffs, wavelet, mode='sym')

coeffs
  A tuple with approximation coefficients and three details coefficients 2D arrays
  like from `dwt2`_::

    (cA, (cH, cV, cD))

wavelet
  |wavelet_arg|

mode
  |mode| This is only important when DWT was performed in `periodization`_ mode.

.. class:: example

  Example:

  .. code-block:: Python
  
    >>> import pywt, numpy
    >>> data = numpy.array([[1,2], [3,4]], dtype=numpy.float64)
    >>> coeffs = pywt.dwt2(data, 'haar')
    >>> print pywt.idwt2(coeffs, 'haar')
    [[ 1.  2.]
     [ 3.  4.]]

   
.. _wavedec2:

2D multilevel decomposition using ``wavedec2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Performs multilevel 2D Discrete Wavelet Transform decomposition 
and returns coefficients list ``[cAn, (cHn, cVn, cDn), ..., (cH1, cV1, cD1)]``,
where ``n`` denotes the level of decomposition and cA, cH, cV and cD are 
approximation, horizontal detail, vertical detail and diagonal detail coefficients arrays.

::

  wavedec2(data, wavelet, mode='sym', level=None)

data
  |data|

wavelet
  |wavelet_arg|

level
  Decomposition level. This should not be greater than value 
  from the `dwt_max_level`_ function for smallest dimension.

mode
  |mode|

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt, numpy
    >>> coeffs = pywt.wavedec2(numpy.ones((8,8)), 'db1', level=2)
    >>> cA2, (cH2, cV2, cD2), (cH1, cV1, cD1) = coeffs
    >>> print cA2
    [[ 4.  4.]
     [ 4.  4.]]

.. _waverec2:

2D multilevel reconstruction using ``waverec2``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Performs multilevel reconstruction from given coefficient list.

::

  waverec2(coeffs, wavelet, mode='sym')

coeffs
  coefficients list must be in form like that from `wavedec2`_ decomposition::
  
  [cAn, (cHn, cVn, cDn), ..., (cH1, cV1, cD1)]

wavelet
  |wavelet_arg|
mode
  |mode|

.. class:: example

  Example:

  .. code-block:: Python

    >>> import pywt, numpy
    >>> coeffs = pywt.wavedec2(numpy.ones((4,4)), 'db1')
    >>> print "levels:", len(coeffs)-1
    levels: 2
    >>> print pywt.waverec2(coeffs, 'db1')
    [[ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]
     [ 1.  1.  1.  1.]]    
    
Wavelet Packets
---------------

Wavelet Packet
~~~~~~~~~~~~~~

Tree structure simplifying operations on Wavelet Packet decomposition coefficients.
It consists of `Node`_ elements.

::

    WaveletPacket(data, wavelet, mode='sp1', maxlevel=None)

data
  |data|

wavelet
  |wavelet_arg|

mode
  |mode|

maxlevel 
  Maximum level of decomposition. If *maxlevel* is None it will be computed with
  `dwt_max_level`_ function.

wp = WaveletPacket(range(16), 'db1', maxlevel=3)

.. _get_node(path):

Access nodes - ``get_node(path)``
""""""""""""""""""""""""""""""""""""

Find node of given path in tree.

path 
  string composed of "a" and "d", of total length not greater than maxlevel.

If node does not exist yet, it will be created by decomposition of its
parent node.


Access node data - ``wp[path]``
""""""""""""""""""""""""""""""""""""""""""

Calls `get_node(path)`_ and returns data associated with node under given path.

Set node data - ``wp[path] = data``
"""""""""""""""""""""""""""""""""""""""""""

Calls `get_node(path)`_ and sets data of node under given path.

Delete node - ``del wp[path]``
""""""""""""""""""""""""""""""""""""

Marks node under given path in tree as ZeroTree root.

path 
  string composed of "a" and "d", of total length not greater than maxlevel.

If node does not exist yet, it will be created by decomposition of its
parent node.


Reconstruct signal - ``reconstruct(update=True)``
"""""""""""""""""""""""""""""""""""""""""""""""""

Returns data reconstruction using coefficients from subnodes.

If update is True, then node's data values will be replaced by
reconstruction values (also in subnodes).

Get nodes by level - ``get_level(level, order="natural")``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Returns all nodes from specified level.

order 
  - "natural" - left to right in tree
  - "freq" - frequency ordered nodes

Get terminal nodes - ``get_nonzero(decompose=False)``
""""""""""""""""""""""""""""""""""""""""""""""""""""""

Returns non-zero terminal nodes.
        

Walk tree - ``walk(func, args=tuple())``
""""""""""""""""""""""""""""""""""""""""""

Walks tree and calls func on every node - ``func(node, *args)``.
If func returns True, descending to subnodes will proceed.

func 
  callable object
args
  additional func parms

Walk tree postorder - ``walk_depth(func, args=tuple())``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Walks tree and calls func on every node starting from bottom most nodes.

func 
  callable object
args 
  additional func parms


Node
~~~~
WaveletPacket tree node.

Subnodes are called **'a'** and **'d'**, like approximation and detail coefficients
in Discrete Wavelet Transform

``path``
""""""""

Path under node is accessible in Wavelet Packet tree.

``data``
""""""""

Data associated with node.

``markZeroTree(flag=True, remove_sub=True)``
""""""""""""""""""""""""""""""""""""""""""""

Mark *node* as root of ZeroTree, which means that current node and all subnodes
don't take part in reconstruction (all coefficients equals 0).

flag
  True/False - mark/unmark node.
remove_sub
  If remove_sub and flag is True, subnodes of current node will be removed.

``isZeroTree``
""""""""""""""
Field - like markZeroTree.

``getChild(part, decompose=True)``
""""""""""""""""""""""""""""""""""""

Returns chosen subnode.

part
  subnode name ('a' or 'd')

decompose
  if True and subnodes don't exist, they will be created by 
  decomposition of current node (lazy evaluation).


Stationary Wavelet Transform
----------------------------

Multilevel ``swt``
~~~~~~~~~~~~~~~~~~

Performs multilevel Stationary Wavelet Transform.

::

  swt(data, wavelet, level)
    
data
  |data| Data length must be divisible by ``2^level``.

wavelet
  |wavelet_arg|
  
level
  Required transform level. See `swt_max_level`_.

Returned list of coefficient pairs is in form
``[(cA1, cD1), (cA2, cD2), ..., (cAn, cDn)]``, where n = level

.. _swt_max_level:

Maximum decomposition level - ``swt_max_level``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns maximum level of Stationary Wavelet Transform for data of given length.

::

  swt_max_level(input_len)


input_len
  input data length.  


Demo
----

* Multilevet wavelet decomposition and reconstruction - `wavedec.py`_
* Plot wavelet families - `plot_wavelets.py`_ - `db.png`_ `sym.png`_
* Plot wavelet and scaling functions - `waveinfo.py`_
* Plot coefficients from DWT and SWT for 3 different signals - `dwt_swt_show_coeffs.py`_
* Multilevel signal decomposition with DWT - `dwt_signal_decomposition.py`_
* Simple compression with Wavelet Packet - `wp_simple_compression.py`_
* Coefficient distribution for several Wavelet Packet Transform levels - `wp_visualize_coeffs_distribution.py`_ - `wp_distrib.png`_
* Signal frequency analysis using Wavelet Packet - `wp_scalogram.py`_ - `linchirp.png`_. See also output of some orca sound scalogram with WP - `orca.png`_.
* Benchmark `dwt`_ and `idwt`_ computation - `benchmark.py`_ - results achieved on Centrino 1,8GHz laptop - `benchmark_dwt.png`_, `benchmark_idwt.png`_
* Creating Wavelet objects from user supplied filter banks - `user_filter_banks.py`_
* Blending image textures in wavelet space - `image_blender.py`_

.. _wavedec.py: ./demo/wavedec.py
.. _plot_wavelets.py: ./demo/plot_wavelets.py
.. _dwt_swt_show_coeffs.py: ./demo/dwt_swt_show_coeffs.py
.. _dwt_signal_decomposition.py: ./demo/dwt_signal_decomposition.py
.. _wp_simple_compression.py: ./demo/wp_simple_compression.py
.. _wp_visualize_coeffs_distribution.py: ./demo/wp_visualize_coeffs_distribution.py
.. _wp_scalogram.py: ./demo/wp_scalogram.py
.. _benchmark.py: ./demo/benchmark.py
.. _user_filter_banks.py: ./demo/user_filter_banks.py
.. _`image_blender.py`: ./demo/image_blender.py
.. _`waveinfo.py`: ./demo/waveinfo.py

.. _db.png: ./img/db.png
.. _sym.png: ./img/sym.png
.. _linchirp.png: ./img/linchirp.png
.. _benchmark_dwt.png: ./img/benchmark_dwt.png
.. _benchmark_idwt.png: ./img/benchmark_idwt.png
.. _wp_distrib.png: ./img/wp_distrib.png
.. _orca.png: ./img/orca.png


.. |mode| replace:: Signal extension mode, see `MODES`_.

.. |data| replace::
    Input signal can be numeric array, python list or other iterable object.
    If data is not in *double* format it will be converted to that type
    before performing computation.

.. |wavelet_arg| replace:: Wavelet to use in transform. This can be name of wavelet from `wavelist()`_ or Wavelet_ object.

.. |pywt| replace:: `PyWavelets`

.. |Wavelet| replace:: ``Wavelet``

