.. _ref-wp:

.. currentmodule:: pywt
.. include:: ../substitutions.rst

===============
Wavelet Packets
===============

PyWavelets implements one-dimensional, two-dimensional and n-dimensional
wavelet packet transform structures. The higher dimensional structures almost
completely sharing programming interface with the one-dimensional tree
structure.

In order to achieve this simplification, a new inheritance scheme was used
in which a :class:`~pywt.BaseNode` base node class is a superclass for the
:class:`~pywt.Node`,  :class:`~pywt.Node2D` and :class:`~pywt.NodeND`
classes.

The node classes are used as data wrappers and can be organized in trees (
binary trees for 1D transform case, quad-trees for the 2D one and 2**N-ary
trees in ND). They are also superclasses to the :class:`~pywt.WaveletPacket`,
:class:`~pywt.WaveletPacket2D` and :class:`~pywt.WaveletPacketND` classes that
are used as the decomposition tree roots and contain a couple additional
methods.

Here 1D, 2D and ND refer to the number of axes of the data to be transformed.
All wavelet packet objects can operate on general n-dimensional arrays, but the
1D or 2D classes apply transforms along only 1 or 2 dimensions. The ND classes
allow transforms over an arbtirary number of axes of n-dimensional data.

The below diagram illustrates the inheritance tree:

  - :class:`~pywt.BaseNode` - common interface for 1D and 2D nodes:

    - :class:`~pywt.Node` - data carrier node in a 1D decomposition tree

      - :class:`~pywt.WaveletPacket` - 1D decomposition tree root node

    - :class:`~pywt.Node2D` - data carrier node in a 2D decomposition tree

      - :class:`~pywt.WaveletPacket2D` - 2D decomposition tree root node

    - :class:`~pywt.NodeND` - data carrier node in a ND decomposition tree

      - :class:`~pywt.WaveletPacketND` - ND decomposition tree root node


BaseNode - a common interface of WaveletPacket, WaveletPacket2D and WaveletPacketND
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: BaseNode

  .. note:: The BaseNode is a base class for :class:`Node`, :class:`Node2D`,
            and :class:`NodeND`. It should not be used directly unless creating
            a new transformation type. It is included here to document the
            common interface of the node and wavelet packet transform classes.

  .. method:: __init__(parent, data, node_name)

    :param parent:    parent node. If parent is ``None`` then the node is
                      considered detached.

    :param data:      The data associated with the node. An n-dimensional
                      numeric array.

    :param node_name: a name identifying the coefficients type.
                      See :attr:`Node.node_name` and :attr:`Node2D.node_name`
                      for information on the accepted subnodes names.

  .. attribute:: data

     Data associated with the node. An n-dimensional numeric array.

  .. attribute:: parent

     Parent node. Used in tree navigation. ``None`` for root node.

  .. attribute:: wavelet

     :class:`~pywt.Wavelet` used for decomposition and reconstruction. Inherited
     from parent node.

  .. attribute:: axes

     A tuple of ints containing the axes along which the wavelet packet
     transform is to be applied.

  .. attribute:: mode

     Signal extension :ref:`mode <ref-modes>` for the :func:`dwt` (:func:`dwt2`)
     and :func:`idwt` (:func:`idwt2`) decomposition and reconstruction
     functions. Inherited from parent node.

  .. attribute:: level

     Decomposition level of the current node. ``0`` for root (original data),
     ``1`` for the first decomposition level, etc.

  .. attribute:: path

     Path string defining position of the node in the decomposition tree.

  .. attribute:: path_tuple

     A version of :attr:`path`, but in tuple form rather than as a single
     string. The tuple form is easier to work with for n-dimensional transforms.
     The length of the tuple will be equal to the number of levels of
     decomposition at the current node.

  .. attribute:: node_name

     Node name describing :attr:`~BaseNode.data` coefficients type of the
     current subnode.

     See :attr:`Node.node_name` and :attr:`Node2D.node_name`.

  .. attribute:: maxlevel

     Maximum allowed level of decomposition. Evaluated from parent or child
     nodes.

  .. attribute:: is_empty

     Checks if :attr:`~BaseNode.data` attribute is ``None``.

  .. attribute:: has_any_subnode

     Checks if node has any subnodes (is not a leaf node).

  .. method:: decompose()

     Performs Discrete Wavelet Transform on the :attr:`~BaseNode.data` and
     returns transform coefficients.

  .. method:: reconstruct([update=False])

     Performs Inverse Discrete Wavelet Transform on subnodes coefficients and
     returns reconstructed data for the current level.

     :param update: If set, the :attr:`~BaseNode.data` attribute will be
                    updated with the reconstructed value.

     .. note:: Descends to subnodes and recursively
               calls :meth:`~BaseNode.reconstruct` on them.

  .. method:: get_subnode(part[, decompose=True])

     Returns subnode or None (see *decomposition* flag description).

     :param part: Subnode name

     :param decompose: If True and subnode does not exist, it will be created
                       using coefficients from the DWT decomposition of the
                       current node.

  .. method:: __getitem__(path)

     Used to access nodes in the decomposition tree by string ``path``.

     :param path: Path string composed from valid node names. See
                  :attr:`Node.node_name` and :attr:`Node2D.node_name` for node
                  naming convention.

     Similar to :meth:`~BaseNode.get_subnode` method with `decompose=True`, but
     can access nodes on any level in the decomposition tree.

     If node does not exist yet, it will be created by decomposition of its
     parent node.

  .. method:: __setitem__(path, data)

     Used to set node or node's data in the decomposition tree. Nodes are
     identified by string ``path``.

     :param path: Path string composed from valid node names.
                  See :attr:`Node.node_name` and :attr:`Node2D.node_name` for
                  node naming convention.

     :param data: numeric array or :class:`~BaseNode` subclass.

  .. method:: __delitem__(path)

     Used to delete node from the decomposition tree.

     :param path: Path string composed from valid node names.
                  See :attr:`Node.node_name` and :attr:`Node2D.node_name` for
                  node naming convention.

  .. method:: get_leaf_nodes([decompose=False])

     Traverses through the decomposition tree and collects leaf nodes (nodes
     without any subnodes).

     :param decompose: If ``decompose`` is ``True``, the method will try to
                       decompose the tree up to the
                       :attr:`maximum level <BaseNode.maxlevel>`.

  .. method:: walk(self, func, [args=(), [kwargs={}, [decompose=True]]])

     Traverses the decomposition tree and calls ``func(node, *args, **kwargs)``
     on every node. If `func` returns ``True``, descending to subnodes will
     continue.

     :param func: callable accepting :class:`BaseNode` as the first param and
                  optional positional and keyword arguments::

                    func(node, *args, **kwargs)

     :args: arguments to pass to the ``func``

     :kwargs: keyword arguments to pass to the ``func``

     :param decompose: If ``decompose`` is ``True`` (default), the method will
                       also try to decompose the tree up to the
                       :attr:`maximum level <BaseNode.maxlevel>`.

  .. method:: walk_depth(self, func, [args=(), [kwargs={}, [decompose=False]]])

     Similar to :meth:`~BaseNode.walk` but traverses the tree in depth-first
     order.

     :param func: callable accepting :class:`BaseNode` as the first param and
                  optional positional and keyword arguments::

                    func(node, *args, **kwargs)

     :args: arguments to pass to the ``func``

     :kwargs: keyword arguments to pass to the ``func``

     :param decompose: If ``decompose`` is ``True``, the method will also try
                       to decompose the tree up to the
                       :attr:`maximum level <BaseNode.maxlevel>`.


WaveletPacket and Node
~~~~~~~~~~~~~~~~~~~~~~

.. class:: Node(BaseNode)

  .. attribute:: node_name

     Node name describing :attr:`~BaseNode.data` coefficients type of the
     current subnode.

     For :class:`WaveletPacket` case it is just as in :func:`dwt`:
        - ``a`` - approximation coefficients
        - ``d`` - details coefficients

  .. method:: decompose()

     .. seealso::

        :func:`dwt` for 1D Discrete Wavelet Transform output coefficients.

  .. method:: reconstruct()

     .. seealso::

        :func:`idwt` for 1D Inverse Discrete Wavelet Transform


.. class:: WaveletPacket(Node)

  .. method:: __init__(data, wavelet, [mode='symmetric', [maxlevel=None, [axis=-1]]])

     :param data: data associated with the node. N-dimensional numeric array.

     :param wavelet: |wavelet|

     :param mode: Signal extension :ref:`mode <ref-modes>` for the :func:`dwt`
                  and :func:`idwt` decomposition and reconstruction functions.

     :param maxlevel: Maximum allowed level of decomposition. If not specified
                      it will be calculated based on the ``wavelet`` and
                      ``data`` length using :func:`pywt.dwt_max_level`.

     :param axis: The axis of the array that is to be transformed.

  .. method:: get_level(level, [order="natural", [decompose=True]])

     Collects nodes from the given level of decomposition.

     :param level: Specifies decomposition ``level`` from which the nodes will
                   be collected.

     :param order: Specifies nodes order - natural (``natural``) or frequency
                   (``freq``).

     :param decompose: If set then the method will try to decompose the data up
                       to the specified ``level``.

     If nodes at the given level are missing (i.e. the tree is partially
     decomposed) and the ``decompose`` is set to ``False``, only existing nodes
     will be returned.

  .. method:: reconstruct([update=True])

     Reconstruct data from the subnodes.

     :param update: A boolean indicating whether the coefficients of the
                    current node and its subnodes will be replaced with values
                    from the reconstruction.


WaveletPacket2D and Node2D
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: Node2D(BaseNode)

  .. attribute:: node_name

     For :class:`WaveletPacket2D` case it is just as in :func:`dwt2`:
        - ``a`` - approximation coefficients (`LL`)
        - ``h`` - horizontal detail coefficients (`LH`)
        - ``v`` - vertical detail coefficients (`HL`)
        - ``d`` - diagonal detail coefficients (`HH`)

  .. method:: decompose()

     .. seealso::

        :func:`dwt2` for 2D Discrete Wavelet Transform output coefficients.

  .. method:: reconstruct()

     .. seealso::

        :func:`idwt2` for 2D Inverse Discrete Wavelet Transform

  .. method:: expand_2d_path(self, path):


.. class:: WaveletPacket2D(Node2D)

  .. method:: __init__(data, wavelet, [mode='symmetric', [maxlevel=None, [axes=(-2, -1)]]])

     :param data: data associated with the node. N-dimensional numeric array.

     :param wavelet: |wavelet|

     :param mode: Signal extension :ref:`mode <ref-modes>` for the :func:`dwt`
                  and :func:`idwt` decomposition and reconstruction functions.

     :param maxlevel: Maximum allowed level of decomposition. If not specified
                      it will be calculated based on the ``wavelet`` and
                      ``data`` length using :func:`pywt.dwt_max_level`.

     :param axes: The axes of the array that are to be transformed.

  .. method:: get_level(level, [order="natural", [decompose=True]])

     Collects nodes from the given level of decomposition.

     :param level: Specifies decomposition ``level`` from which the nodes will
                   be collected.

     :param order: Specifies nodes order - natural (``natural``) or frequency
                   (``freq``).

     :param decompose: If set then the method will try to decompose the data up
                       to the specified ``level``.

     If nodes at the given level are missing (i.e. the tree is partially
     decomposed) and the ``decompose`` is set to ``False``, only existing nodes
     will be returned.

  .. method:: reconstruct([update=True])

     Reconstruct data from the subnodes.

     :param update: A boolean indicating whether the coefficients of the
                    current node and its subnodes will be replaced with values
                    from the reconstruction.

WaveletPacketND and NodeND
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: NodeND(BaseNode)

  .. attribute:: node_name

     For :class:`WaveletPacketND` case it is just as in :func:`dwtn`:
         - in 1D it has keys 'a' and 'd'
         - in 2D it has keys 'aa', 'ad', 'da', 'dd'
         - in 3D it has keys 'aaa', 'aad', 'ada', 'daa', ..., 'ddd'

  .. method:: decompose()

     .. seealso::

        :func:`dwtn` for ND Discrete Wavelet Transform output coefficients.

  .. method:: reconstruct()

     .. seealso::

        :func:`idwtn` for ND Inverse Discrete Wavelet Transform


.. class:: WaveletPacketND(NodeND)

  .. method:: __init__(data, wavelet, [mode='symmetric', [maxlevel=None, [axes=None]]])

     :param data: data associated with the node. N-dimensional numeric array.

     :param wavelet: |wavelet|

     :param mode: Signal extension :ref:`mode <ref-modes>` for the :func:`dwt`
                  and :func:`idwt` decomposition and reconstruction functions.

     :param maxlevel: Maximum allowed level of decomposition. If not specified
                      it will be calculated based on the ``wavelet`` and
                      ``data`` length using :func:`pywt.dwt_max_level`.

     :param axes: The axes of the array that are to be transformed.

  .. method:: get_level(level, [decompose=True])

     Collects nodes from the given level of decomposition.

     :param level: Specifies decomposition ``level`` from which the nodes will
                   be collected.

     :param decompose: If set then the method will try to decompose the data up
                       to the specified ``level``.

     If nodes at the given level are missing (i.e. the tree is partially
     decomposed) and the ``decompose`` is set to ``False``, only existing nodes
     will be returned.

  .. method:: reconstruct([update=True])

     Reconstruct data from the subnodes.

     :param update: A boolean indicating whether the coefficients of the
                    current node and its subnodes will be replaced with values
                    from the reconstruction.
