Test 2D Wavelet Packets
=======================

Import pywt
-----------

>>> import pywt
>>> import numpy


Create 2D Wavelet Packet structure
----------------------------------

Start with preparing test data:

    >>> x = numpy.array([[1, 2, 3, 4, 5, 6, 7, 8]] * 8, 'd')
    >>> print x
    [[ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]]

Now create a 2D Wavelet Packet object:

    >>> wp = pywt.WaveletPacket2D(data=x, wavelet='db1', mode='sym')

The input data and decomposition coefficients are stored in the `data`
attribute:

    >>> print wp.data
    [[ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]]

Nodes are identified by paths. For the root node the path is '' and the
decomposition level is 0.

    >>> print repr(wp.path)
    ''
    >>> print wp.level
    0

The maxlevel, if not given in the constructor, is automatically computed based
on the data size:

    >>> print wp.maxlevel
    3


Traversing WP tree:
-------------------

Wavelet Packet nides are arranged in a tree. Each node in a WP tree is uniquely
identified and addressed by a path string.

In 1D WaveletPackets case nodes were accessed using `a` (approximation)
and `d` (details) path names (each node has two 1D children).

Because now we deal with a bit more complex structure (each node has four children),
we have four basic path names based on the dwt 2D output convention to address
the WP2D structure:

    * `a` - LL, low-low coefficients
    * `h` - LH, low-high coefficients
    * `v` - HL, high-low coefficients
    * `d` - HH, high-high coefficients

In other words, subnode naming corresponds to the `dwt2` function output naming
convention (as wavelet packet transform is based on dwt2 transform)::

                                -------------------
                                |        |        |
                                | cA(LL) | cH(LH) |
                                |        |        |
    (cA, (cH, cV, cD))  <--->   -------------------
                                |        |        |
                                | cV(HL) | cD(HH) |
                                |        |        |
                                -------------------

       (fig.1: DWT 2D output and interpretation)


Knowing what the nodes names are, we can now access them using indexing operator ([x]):

    >>> print wp['a'].data
    [[  3.   7.  11.  15.]
     [  3.   7.  11.  15.]
     [  3.   7.  11.  15.]
     [  3.   7.  11.  15.]]
    >>> print wp['h'].data
    [[ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]]
    >>> print wp['v'].data
    [[-1. -1. -1. -1.]
     [-1. -1. -1. -1.]
     [-1. -1. -1. -1.]
     [-1. -1. -1. -1.]]
    >>> print wp['d'].data
    [[ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]]

Similarly, a subnode of a subnode can be accessed:

    >>> print wp['aa'].data
    [[ 10.  26.]
     [ 10.  26.]]

Indexing base WaveletPacket2D (as well as 1D WaveletPacket) using compound path is just the same
as indexing WP subnode:

    >>> node = wp['a']
    >>> print node['a'].data
    [[ 10.  26.]
     [ 10.  26.]]
    >>> print wp['a']['a'].data is wp['aa'].data
    True

Following down the decomposition path:

    >>> print wp['aaa'].data
    [[ 36.]]


    >>> print wp['aaaa'].data
    Traceback (most recent call last):
    ...
    IndexError: Path length is out of range.

Ups, we have reached the maximum level of decomposition for the 'aaaa' path, which btw. was:

    >>> print wp.maxlevel
    3


Now try some invalid path:

    >>> print wp['f']
    Traceback (most recent call last):
    ...
    ValueError: Subnode name must be in ['a', 'h', 'v', 'd'], not 'f'.


Accessing Node2D's attributes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

WaveletPacket2D is a tree data structure, which evaluates to a set
of Node2D objects. WaveletPacket2D is just a special subclass of Node2D
class (which in turn inherits from a BaseNode, just like with Node
and WaveletPacket for the 1D case.)

    >>> print wp['av'].data
    [[-4. -4.]
     [-4. -4.]]

    >>> print wp['av'].path
    av

    >>> print wp['av'].node_name
    v

    >>> print wp['av'].parent.path
    a

    >>> print wp['av'].parent.data
    [[  3.   7.  11.  15.]
     [  3.   7.  11.  15.]
     [  3.   7.  11.  15.]
     [  3.   7.  11.  15.]]

    >>> print wp['av'].level
    2

    >>> print wp['av'].maxlevel
    3

    >>> print wp['av'].mode
    sym


Collecting nodes
~~~~~~~~~~~~~~~~

We can get all nodes on the particular level using the `get_level` method:

    * 0 level - the root `wp` node:

        >>> len(wp.get_level(0))
        1
        >>> print [node.path for node in wp.get_level(0)]
        ['']

    * 1st level of decomposition:

        >>> len(wp.get_level(1))
        4
        >>> print [node.path for node in wp.get_level(1)]
        ['a', 'h', 'v', 'd']

    * 2nd level of decomposition:

        >>> len(wp.get_level(2))
        16
        >>> paths = [node.path for node in wp.get_level(2)]
        >>> for i, path in enumerate(paths):
        ...     print path,
        ...     if (i+1) % 4 == 0: print
        aa ah av ad
        ha hh hv hd
        va vh vv vd
        da dh dv dd

    * 3rd level of decomposition:

        >>> print len(wp.get_level(3))
        64
        >>> paths = [node.path for node in wp.get_level(3)]
        >>> for i, path in enumerate(paths):
        ...     print path,
        ...     if (i+1) % 8 == 0: print
        aaa aah aav aad aha ahh ahv ahd
        ava avh avv avd ada adh adv add
        haa hah hav had hha hhh hhv hhd
        hva hvh hvv hvd hda hdh hdv hdd
        vaa vah vav vad vha vhh vhv vhd
        vva vvh vvv vvd vda vdh vdv vdd
        daa dah dav dad dha dhh dhv dhd
        dva dvh dvv dvd dda ddh ddv ddd

Note that `get_level` performs automatic decomposition until it
reaches the given level.


Reconstructing data from Wavelet Packets:
-----------------------------------------

Let's create a new empty 2D Wavelet Packet structure and set its nodes
values with known data from the previous examples:

    >>> new_wp = pywt.WaveletPacket2D(data=None, wavelet='db1', mode='sym')

    >>> new_wp['vh'] = wp['vh'].data # [[0.0, 0.0], [0.0, 0.0]]
    >>> new_wp['vv'] = wp['vh'].data # [[0.0, 0.0], [0.0, 0.0]]
    >>> new_wp['vd'] = [[0.0, 0.0], [0.0, 0.0]]

    >>> new_wp['a'] = [[3.0, 7.0, 11.0, 15.0], [3.0, 7.0, 11.0, 15.0], 
    ...                [3.0, 7.0, 11.0, 15.0], [3.0, 7.0, 11.0, 15.0]]
    >>> new_wp['d'] = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], 
    ...                [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]

    For convenience, 'data' gets automatically extracted from the base Node object:

    >>> new_wp['h'] = wp['h'] # all zeros

    Note: just remember to not assign to the node.data parameter directly (todo).

And reconstruct the data from the `a`, `d`, `vh`, `vv`, `vd` and `h` packets
(Note that `va` node was not set and the WP tree is "not complete"
- the `va` branch will be treated as zero-array):

    >>> print new_wp.reconstruct(update=False)
    [[ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]]

Now set the `va` node with the known values and do the reconstruction again:

    >>> new_wp['va'] = wp['va'].data # [[-2.0, -2.0], [-2.0, -2.0]]
    >>> print new_wp.reconstruct(update=False)
    [[ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]]

which is just the same as the base sample data `x`.

Of course we can go the other way and remove nodes from the tree.
If we delete the `va` node, again, we get the "not complete" tree
from one of the previous examples:

    >>> del new_wp['va']
    >>> print new_wp.reconstruct(update=False)
    [[ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]
     [ 1.5  1.5  3.5  3.5  5.5  5.5  7.5  7.5]]

Just restore the node before next examples.
    >>> new_wp['va'] = wp['va'].data

If the `update` param in the `reconstruct` method is set to False, the node's
`data` attribute will not be updated.

    >>> print new_wp.data
    None

Otherwise, the `data` attribute will be set to the reconstructed value.

    >>> print new_wp.reconstruct(update=True)
    [[ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]]
    >>> print new_wp.data
    [[ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]
     [ 1.  2.  3.  4.  5.  6.  7.  8.]]

Since we have an interesting WP structure built, it is a good occasion to
present the `get_leaf_nodes` method, which just collects non-zero leaf nodes
from the WP tree:

    >>> print [n.path for n in new_wp.get_leaf_nodes()]
    ['a', 'h', 'va', 'vh', 'vv', 'vd', 'd']

Passing the `decompose=True` parameter to the method will force the WP object
to do a full decomposition up to the maximum level of decomposition:

    >>> paths = [n.path for n in new_wp.get_leaf_nodes(decompose=True)]
    >>> len(paths)
    64
    >>> for i, path in enumerate(paths):
    ...     print path,
    ...     if (i+1) % 8 == 0: print
    aaa aah aav aad aha ahh ahv ahd
    ava avh avv avd ada adh adv add
    haa hah hav had hha hhh hhv hhd
    hva hvh hvv hvd hda hdh hdv hdd
    vaa vah vav vad vha vhh vhv vhd
    vva vvh vvv vvd vda vdh vdv vdd
    daa dah dav dad dha dhh dhv dhd
    dva dvh dvv dvd dda ddh ddv ddd

Lazy eveluation:
----------------

.. note:: This section is for demonstration of pywt internals purposes
    only. Do not rely on the attribute access to nodes as presented in this
    example.

>>> x = numpy.array([[1, 2, 3, 4, 5, 6, 7, 8]] * 8)
>>> wp = pywt.WaveletPacket2D(data=x, wavelet='db1', mode='sym')

1) At first the wp's attribute `a` is None

   >>> print wp.a
   None

2) During the first attempt to access the node it is computed
   via decomposition of its parent node (the wp object itself).

   >>> print wp['a']
   a: [[  3.   7.  11.  15.]
    [  3.   7.  11.  15.]
    [  3.   7.  11.  15.]
    [  3.   7.  11.  15.]]

3) Now the `wp.a` is set to the newly created node:

    >>> print wp.a
    a: [[  3.   7.  11.  15.]
     [  3.   7.  11.  15.]
     [  3.   7.  11.  15.]
     [  3.   7.  11.  15.]]

   And so is `wp.d`:

    >>> print wp.d
    d: [[ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]]
