.. _reg-wp:

.. currentmodule:: pywt

Wavelet Packets
===============

Import pywt
-----------

    >>> import pywt

    >>> def format_array(a):
    ...     """Consistent array representation across different systems"""
    ...     import numpy
    ...     a = numpy.where(numpy.abs(a) < 1e-5, 0, a)
    ...     return numpy.array2string(a, precision=5, separator=' ', suppress_small=True)


Create Wavelet Packet structure
-------------------------------

Ok, let's create a sample :class:`WaveletPacket`:

    >>> x = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='sym')

The input *data* and decomposition coefficients are stored in the
:attr:`WaveletPacket.data` attribute:

    >>> print wp.data
    [1, 2, 3, 4, 5, 6, 7, 8]

:class:`Nodes <Node>` are identified by :attr:`paths <~Node.path>`. For the root
node the path is ``''`` and the decomposition level is ``0``.

    >>> print repr(wp.path)
    ''
    >>> print wp.level
    0

The *maxlevel*, if not given as param in the constructor, is automatically
computed:

    >>> print wp['ad'].maxlevel
    3


Traversing WP tree:
-------------------

Accessing subnodes:
~~~~~~~~~~~~~~~~~~~

>>> x = [1, 2, 3, 4, 5, 6, 7, 8]
>>> wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='sym')

First check what is the maximum level of decomposition:

    >>> print wp.maxlevel
    3

and try accessing subnodes of the WP tree:

    * 1st level:

        >>> print wp['a'].data
        [  2.12132034   4.94974747   7.77817459  10.60660172]
        >>> print wp['a'].path
        a

    * 2nd level:

        >>> print wp['aa'].data
        [  5.  13.]
        >>> print wp['aa'].path
        aa


    * 3rd level:

        >>> print wp['aaa'].data
        [ 12.72792206]
        >>> print wp['aaa'].path
        aaa


      Ups, we have reached the maximum level of decomposition and got an
      :exc:`IndexError`:

        >>> print wp['aaaa'].data
        Traceback (most recent call last):
        ...
        IndexError: Path length is out of range.

Now try some invalid path:

    >>> print wp['ac']
    Traceback (most recent call last):
    ...
    ValueError: Subnode name must be in ['a', 'd'], not 'c'.

which just yielded a :exc:`ValueError`.


Accessing Node's attributes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`WaveletPacket` object is a tree data structure, which evaluates to a set
of :class:`Node` objects. :class:`WaveletPacket` is just a special subclass
of the :class:`Node` class (which in turn inherits from the :class:`BaseNode`).

Tree nodes can be accessed using the *obj[x]* (:meth:`Node.__getitem__`) operator.
Each tree node has a set of attributes: :attr:`~Node.data`, :attr:`~Node.path`,
:attr:`~Node.node_name`, :attr:`~Node.parent`, :attr:`~Node.level`,
:attr:`~Node.maxlevel` and :attr:`~Node.mode`.

>>> x = [1, 2, 3, 4, 5, 6, 7, 8]
>>> wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='sym')

>>> print wp['ad'].data
[-2. -2.]

>>> print wp['ad'].path
ad

>>> print wp['ad'].node_name
d

>>> print wp['ad'].parent.path
a

>>> print wp['ad'].level
2

>>> print wp['ad'].maxlevel
3

>>> print wp['ad'].mode
sym


Collecting nodes
~~~~~~~~~~~~~~~~

>>> x = [1, 2, 3, 4, 5, 6, 7, 8]
>>> wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='sym')


We can get all nodes on the particular level either in ``natural`` order:

    >>> print [node.path for node in wp.get_level(3, 'natural')]
    ['aaa', 'aad', 'ada', 'add', 'daa', 'dad', 'dda', 'ddd']

or sorted based on the band frequency (``freq``):

    >>> print [node.path for node in wp.get_level(3, 'freq')]
    ['aaa', 'aad', 'add', 'ada', 'dda', 'ddd', 'dad', 'daa']

Note that :meth:`WaveletPacket.get_level` also performs automatic decomposition
until it reaches the specified *level*.


Reconstructing data from Wavelet Packets:
-----------------------------------------

>>> x = [1, 2, 3, 4, 5, 6, 7, 8]
>>> wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='sym')


Now create a new :class:`Wavelet Packet <WaveletPacket>` and set it's nodes with
some data.

    >>> new_wp = pywt.WaveletPacket(data=None, wavelet='db1', mode='sym')

    >>> new_wp['aa'] = wp['aa'].data
    >>> new_wp['ad'] = [-2., -2.]

For convenience, :attr:`Node.data` gets automatically extracted from the
:class:`Node` object:

    >>> new_wp['d'] = wp['d']

And reconstruct the data from the ``aa``, ``ad`` and ``d`` packets.

    >>> print new_wp.reconstruct(update=False)
    [ 1.  2.  3.  4.  5.  6.  7.  8.]

If the *update* param in the reconstruct method is set to ``False``, the node's
:attr:`~Node.data` will not be updated.

    >>> print new_wp.data
    None

Otherwise, the :attr:`~Node.data` attribute will be set to the reconstructed
value.

    >>> print new_wp.reconstruct(update=True)
    [ 1.  2.  3.  4.  5.  6.  7.  8.]
    >>> print new_wp.data
    [ 1.  2.  3.  4.  5.  6.  7.  8.]


>>> print [n.path for n in new_wp.get_leaf_nodes(False)]
['aa', 'ad', 'd']

>>> print [n.path for n in new_wp.get_leaf_nodes(True)]
['aaa', 'aad', 'ada', 'add', 'daa', 'dad', 'dda', 'ddd']


Removing nodes from Wavelet Packet tree:
----------------------------------------

Let's create a sample data:

    >>> x = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='sym')

First, start with a tree decomposition at level 2. Leaf nodes in the tree are:

    >>> dummy = wp.get_level(2)
    >>> for n in wp.get_leaf_nodes(False):
    ...     print n.path, format_array(n.data)
    aa [  5.  13.]
    ad [-2. -2.]
    da [-1. -1.]
    dd [ 0.  0.]

    >>> node = wp['ad']
    >>> print node
    ad: [-2. -2.]

To remove a node from the WP tree, use Python's `del obj[x]`
(:class:`Node.__delitem__`):

    >>> del wp['ad']

The leaf nodes that left in the tree are:

    >>> for n in wp.get_leaf_nodes():
    ...     print n.path, format_array(n.data)
    aa [  5.  13.]
    da [-1. -1.]
    dd [ 0.  0.]

And the reconstruction is:

    >>> print wp.reconstruct()
    [ 2.  3.  2.  3.  6.  7.  6.  7.]

Now restore the deleted node value.

    >>> wp['ad'].data = node.data

Printing leaf nodes and tree reconstruction confirms the original state of the
tree:

    >>> for n in wp.get_leaf_nodes(False):
    ...     print n.path, format_array(n.data)
    aa [  5.  13.]
    ad [-2. -2.]
    da [-1. -1.]
    dd [ 0.  0.]

    >>> print wp.reconstruct()
    [ 1.  2.  3.  4.  5.  6.  7.  8.]


Lazy eveluation:
----------------

.. note:: This section is for demonstration of pywt internals purposes
          only. Do not rely on the attribute access to nodes as presented in
          this example.

>>> x = [1, 2, 3, 4, 5, 6, 7, 8]
>>> wp = pywt.WaveletPacket(data=x, wavelet='db1', mode='sym')

1) At first the wp's attribute `a` is None

   >>> print wp.a
   None

   **Remember that you should not rely on the attribute access.**

2) At first attempt to access the node it is computed via decomposition
   of it's parent node (the wp object itself).

   >>> print wp['a']
   a: [  2.12132034   4.94974747   7.77817459  10.60660172]

3) Now the `wp.a` is set to the newly created node:

   >>> print wp.a
   a: [  2.12132034   4.94974747   7.77817459  10.60660172]

   And so is `wp.d`:

   >>> print wp.d
   d: [-0.70710678 -0.70710678 -0.70710678 -0.70710678]
