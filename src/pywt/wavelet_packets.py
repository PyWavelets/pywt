# -*- coding: utf-8 -*-

# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

"""1D and 2D Wavelet packet transform module."""

__all__ = ["BaseNode", "Node", "WaveletPacket", "Node2D", "WaveletPacket2D"]

import numerix
from _pywt import Wavelet, dwt, idwt, dwt_max_level
from multidim import dwt2, idwt2


def get_graycode_order(level, x='a', y='d'):
    graycode_order = [x, y]
    for i in range(level - 1):
        graycode_order = [x + path for path in graycode_order] + \
                         [y + path for path in graycode_order[::-1]]
    return graycode_order


class BaseNode(object):
    """
    BaseNode for wavelet packet 1D and 2D tree nodes.
    """

    # PART_LEN and PARTS attributes that define path tokens for node[] lookup
    # must be defined in subclasses.
    PART_LEN = None
    PARTS = None

    def __init__(self, parent, data, node_name):
        self.parent = parent
        if parent is not None:
            self.wavelet = parent.wavelet
            self.mode = parent.mode
            self.level = parent.level + 1
            self._maxlevel = parent.maxlevel
            self.path = parent.path + node_name
        else:
            self.wavelet = None
            self.mode = None
            self.path = ""
            self.level = 0

        # data - signal on level 0, coeffs on higher levels
        self.data = data

        self._init_subnodes()

    def _init_subnodes(self):
        for part in self.PARTS:
            self._set_node(part, None)

    def _create_subnode(self, part, data=None, overwrite=True):
        raise NotImplementedError()

    def _create_subnode_base(self, node_cls, part, data=None, overwrite=True):
        self._validate_node_name(part)
        if not overwrite and self._get_node(part) is not None:
            return self._get_node(part)
        node = node_cls(self, data, part)
        self._set_node(part, node)
        return node

    def _get_node(self, part):
        return getattr(self, part)

    def _set_node(self, part, node):
        setattr(self, part, node)

    def _delete_node(self, part):
        self._set_node(part, None)

    def _validate_node_name(self, part):
        if part not in self.PARTS:
            raise ValueError("Subnode name must be in [%s], not '%s'." %
                             (', '.join("'%s'" % p for p in self.PARTS), part))

    def _evaluate_maxlevel(self, evaluate_from='parent'):
        """
        Try to find the value of maximum decomposition level if it is not
        specified explicitly.
        """
        assert evaluate_from in ('parent', 'subnodes')

        if self._maxlevel is not None:
            return self._maxlevel
        elif self.data is not None:
            return self.level + dwt_max_level(
                min(self.data.shape), self.wavelet)

        if evaluate_from == 'parent':
            if self.parent is not None:
                return self.parent._evaluate_maxlevel(evaluate_from)
        elif evaluate_from == 'subnodes':
            for node_name in self.PARTS:
                node = getattr(self, node_name, None)
                if node is not None:
                    level = node._evaluate_maxlevel(evaluate_from)
                    if level is not None:
                        return level
        return None

    @property
    def maxlevel(self):
        if self._maxlevel is not None:
            return self._maxlevel

        # Try getting the maxlevel from parents first
        self._maxlevel = self._evaluate_maxlevel(evaluate_from='parent')

        # If not found, check whether it can be evaluated from subnodes
        if self._maxlevel is None:
            self._maxlevel = self._evaluate_maxlevel(evaluate_from='subnodes')
        return self._maxlevel

    @property
    def node_name(self):
        return self.path[-self.PART_LEN:]

    def decompose(self):
        """
        Decompose node data creating DWT coefficients subnodes."
        """
        if self.level < self.maxlevel:
            return self._decompose()
        else:
            raise ValueError("Maximum decomposition level reached.")

    def _decompose(self):
        raise NotImplementedError()

    def reconstruct(self, update=False):
        """
        Reconstruct node from subnodes.
        If update param is True, then reconstructed data replaces the current
        node data.

        Returns:
            - original node data if subnodes do not exist
            - IDWT of subnodes otherwise.
        """
        if not self.has_any_subnode:
            return self.data
        return self._reconstruct(update)

    def _reconstruct(self):
        raise NotImplementedError()  # override this in subclasses

    def get_subnode(self, part, decompose=True):
        """
        Returns subnode.

        part      - subnode name
        decompose - if the param is True and corresponding subnode does not
                    exist, the subnode will be created using coefficients
                    from the DWT decomposition of the current node.
        """
        self._validate_node_name(part)
        subnode = self._get_node(part)
        if subnode is None and decompose and not self.is_empty:
            self.decompose()
            subnode = self._get_node(part)
        return subnode

    def __getitem__(self, path):
        """
        Find node represented by the given path.

        path - string composed of node names.

        If node does not exist yet, it will be created by decomposition of its
        parent node.
        """
        if isinstance(path, basestring):
            if (self.maxlevel is not None
                and len(path) > self.maxlevel * self.PART_LEN):
                raise IndexError("Path length is out of range.")
            if path:
                return self.get_subnode(path[0:self.PART_LEN], True)[
                       path[self.PART_LEN:]]
            else:
                return self
        else:
            raise TypeError("Invalid path parameter type - expected string but"
                            " got %s." % type(path))

    def __setitem__(self, path, data):
        """
        Set node represented by the given path with a new value.

        path - string composed of node names.
        data - array or BaseNode subclass.
        """

        if isinstance(path, basestring):
            if (
                self.maxlevel is not None
                and len(self.path) + len(path) > self.maxlevel * self.PART_LEN
            ):
                raise IndexError("Path length out of range.")
            if path:
                subnode = self.get_subnode(path[0:self.PART_LEN], False)
                if subnode is None:
                    self._create_subnode(path[0:self.PART_LEN], None)
                    subnode = self.get_subnode(path[0:self.PART_LEN], False)
                subnode[path[self.PART_LEN:]] = data
            else:
                if isinstance(data, BaseNode):
                    self.data = numerix.as_float_array(data.data)
                else:
                    self.data = numerix.as_float_array(data)
        else:
            raise TypeError("Invalid path parameter type - expected string but"
                            " got %s." % type(path))

    def __delitem__(self, path):
        """
        Remove node from the tree.
        """
        node = self[path]
        # don't clear node value and subnodes (node may still exist outside
        # the tree)
        ## node._init_subnodes()
        ## node.data = None
        parent = node.parent
        node.parent = None  # TODO
        if parent and node.node_name:
            parent._delete_node(node.node_name)

    def is_empty(self):
        return self.data is None
    is_empty = property(is_empty)

    def has_any_subnode(self):
        for part in self.PARTS:
            if self._get_node(part) is not None:  # and not .is_empty
                return True
        return False
    has_any_subnode = property(has_any_subnode)

    def get_leaf_nodes(self, decompose=False):
        """
        Returns leaf nodes.
        """
        result = []

        def collect(node):
            if node.level == node.maxlevel and not node.is_empty:
                result.append(node)
                return False
            if not decompose and not node.has_any_subnode:
                result.append(node)
                return False
            return True
        self.walk(collect, decompose=decompose)
        return result

    def walk(self, func, args=(), kwargs=None, decompose=True):
        """
        Walk tree and call func on every node -> func(node, *args)
        If func returns True, descending to subnodes will continue.

        func - callable
        args - func params
        kwargs - func keyword params
        """
        if kwargs is None:
            kwargs = {}
        if func(self, *args, **kwargs) and self.level < self.maxlevel:
            for part in self.PARTS:
                subnode = self.get_subnode(part, decompose)
                if subnode is not None:
                    subnode.walk(func, args, kwargs, decompose)

    def walk_depth(self, func, args=(), kwargs=None, decompose=False):
        """
        Walk tree and call func on every node starting from the bottom-most
        nodes.

        func - callable
        args - func params
        kwargs - func keyword params
        """
        if kwargs is None:
            kwargs = {}
        if self.level < self.maxlevel:
            for part in self.PARTS:
                subnode = self.get_subnode(part, decompose)
                if subnode is not None:
                    subnode.walk_depth(func, args, kwargs, decompose)
        func(self, *args, **kwargs)

    def __str__(self):
        return self.path + ": " + str(self.data)


class Node(BaseNode):
    """
    WaveletPacket tree node.

    Subnodes are called ``a`` and ``d``, just like approximation
    and detail coefficients in the Discrete Wavelet Transform.
    """

    A = 'a'
    D = 'd'
    PARTS = A, D
    PART_LEN = 1

    def _create_subnode(self, part, data=None, overwrite=True):
        return self._create_subnode_base(node_cls=Node, part=part, data=data,
            overwrite=overwrite)

    def _decompose(self):
        if self.is_empty:
            data_a, data_d = None, None
            if self._get_node(self.A) is None:
                self._create_subnode(self.A, data_a)
            if self._get_node(self.D) is None:
                self._create_subnode(self.D, data_d)
        else:
            data_a, data_d = dwt(self.data, self.wavelet, self.mode)
            self._create_subnode(self.A, data_a)
            self._create_subnode(self.D, data_d)
        return self._get_node(self.A), self._get_node(self.D)

    def _reconstruct(self, update):
        data_a, data_d = None, None
        node_a, node_d = self._get_node(self.A), self._get_node(self.D)

        if node_a is not None:
            data_a = node_a.reconstruct()  # TODO: (update) ???
        if node_d is not None:
            data_d = node_d.reconstruct()  # TODO: (update) ???

        if data_a is None and data_d is None:
            raise ValueError("Node is a leaf node and cannot be reconstructed"
                             " from subnodes.")
        else:
            rec = idwt(data_a, data_d, self.wavelet, self.mode,
                       correct_size=True)
            if update:
                self.data = rec
            return rec


class Node2D(BaseNode):
    """
    WaveletPacket tree node.

    Subnodes are called 'a' (LL), 'h' (LH), 'v' (HL) and  'd' (HH), like
    approximation and detail coefficients in the 2D Discrete Wavelet Transform
    """

    LL = 'a'
    LH = 'h'
    HL = 'v'
    HH = 'd'

    PARTS = LL, LH, HL, HH
    PART_LEN = 1

    def _create_subnode(self, part, data=None, overwrite=True):
        return self._create_subnode_base(node_cls=Node2D, part=part, data=data,
            overwrite=overwrite)

    def _decompose(self):
        if self.is_empty:
            data_ll, data_lh, data_hl, data_hh = None, None, None, None
        else:
            data_ll, (data_lh, data_hl, data_hh) =\
                dwt2(self.data, self.wavelet, self.mode)
        self._create_subnode(self.LL, data_ll)
        self._create_subnode(self.LH, data_lh)
        self._create_subnode(self.HL, data_hl)
        self._create_subnode(self.HH, data_hh)
        return self._get_node(self.LL), self._get_node(self.LH),\
               self._get_node(self.HL), self._get_node(self.HH)

    def _reconstruct(self, update):
        data_ll, data_lh, data_hl, data_hh = None, None, None, None

        node_ll, node_lh, node_hl, node_hh =\
            self._get_node(self.LL), self._get_node(self.LH),\
            self._get_node(self.HL), self._get_node(self.HH)

        if node_ll is not None:
            data_ll = node_ll.reconstruct()
        if node_lh is not None:
            data_lh = node_lh.reconstruct()
        if node_hl is not None:
            data_hl = node_hl.reconstruct()
        if node_hh is not None:
            data_hh = node_hh.reconstruct()

        if (data_ll is None and data_lh is None
            and data_hl is None and data_hh is None):
            raise ValueError(
                "Tree is missing data - all subnodes of `%s` node "
                "are None. Cannot reconstruct node." % self.path
            )
        else:
            coeffs = data_ll, (data_lh, data_hl, data_hh)
            rec = idwt2(coeffs, self.wavelet, self.mode)
            if update:
                self.data = rec
            return rec

    def expand_2d_path(self, path):
        expanded_paths = {
            self.HH: 'hh',
            self.HL: 'hl',
            self.LH: 'lh',
            self.LL: 'll'
        }
        return (''.join([expanded_paths[p][0] for p in path]),
                ''.join([expanded_paths[p][1] for p in path]))


class WaveletPacket(Node):
    """
    Data structure representing Wavelet Packet decomposition of signal.

    data     - original data (signal)
    wavelet  - wavelet used in DWT decomposition and reconstruction
    mode     - signal extension mode - see MODES
    maxlevel - maximum level of decomposition (will be computed if not
               specified)
    """
    def __init__(self, data, wavelet, mode='sym', maxlevel=None):
        super(WaveletPacket, self).__init__(None, data, "")

        if not isinstance(wavelet, Wavelet):
            wavelet = Wavelet(wavelet)
        self.wavelet = wavelet
        self.mode = mode

        if data is not None:
            data = numerix.as_float_array(data)
            assert len(data.shape) == 1
            self.data_size = data.shape[0]
            if maxlevel is None:
                maxlevel = dwt_max_level(self.data_size, self.wavelet)
        else:
            self.data_size = None

        self._maxlevel = maxlevel

    def reconstruct(self, update=True):
        """
        Reconstruct data value using coefficients from subnodes.

        If update is True, then data values will be replaced by
        reconstruction values, also in subnodes.
        """
        if self.has_any_subnode:
            data = super(WaveletPacket, self).reconstruct(update)
            if self.data_size is not None and len(data) > self.data_size:
                data = data[:self.data_size]
            if update:
                self.data = data
            return data
        return self.data  # return original data

    def get_level(self, level, order="natural", decompose=True):
        """
        Returns all nodes on the specified level.

        order - "natural" - left to right in tree
              - "freq" - band ordered
        """
        assert order in ["natural", "freq"]
        if level > self.maxlevel:
            raise ValueError("The level cannot be greater than the maximum"
                             " decomposition level value (%d)" % self.maxlevel)

        result = []

        def collect(node):
            if node.level == level:
                result.append(node)
                return False
            return True

        self.walk(collect, decompose=decompose)
        if order == "natural":
            return result
        elif order == "freq":
            result = dict((node.path, node) for node in result)
            graycode_order = get_graycode_order(level)
            return [result[path] for path in graycode_order if path in result]
        else:
            raise ValueError("Invalid order name - %s." % order)


class WaveletPacket2D(Node2D):
    """
    Data structure representing 2D Wavelet Packet decomposition of signal.

    data     - original data (signal)
    wavelet  - wavelet used in DWT decomposition and reconstruction
    mode     - signal extension mode - see MODES
    maxlevel - maximum level of decomposition (will be computed if not
               specified)
    """
    def __init__(self, data, wavelet, mode='sp1', maxlevel=None):
        super(WaveletPacket2D, self).__init__(None, data, "")

        if not isinstance(wavelet, Wavelet):
            wavelet = Wavelet(wavelet)
        self.wavelet = wavelet
        self.mode = mode

        if data is not None:
            data = numerix.as_float_array(data)
            assert len(data.shape) == 2
            self.data_size = data.shape
            if maxlevel is None:
                maxlevel = dwt_max_level(min(self.data_size), self.wavelet)
        else:
            self.data_size = None
        self._maxlevel = maxlevel

    def reconstruct(self, update=True):
        """
        Reconstruct data using coefficients from subnodes.

        If update is set to True then the coefficients of the current node
        and its subnodes will be replaced with values from reconstruction.
        """
        if self.has_any_subnode:
            data = super(WaveletPacket2D, self).reconstruct(update)
            if self.data_size is not None and (data.shape != self.data_size):
                data = data[:self.data_size[0], :self.data_size[1]]
            if update:
                self.data = data
            return data
        return self.data  # return original data

    def get_level(self, level, order="natural", decompose=True):
        """
        Returns all nodes from specified level.

        If order is `natural`, a flat list is returned.

        If order is `freq`, a 2d structure with rows and cols
        sorted by corresponding dimension frequency of 2d
        coefficient array (adapted from 1d case).
        """
        assert order in ["natural", "freq"]
        if level > self.maxlevel:
            raise ValueError("The level cannot be greater than the maximum"
                             " decomposition level value (%d)" % self.maxlevel)

        result = []

        def collect(node):
            if node.level == level:
                result.append(node)
                return False
            return True

        self.walk(collect, decompose=decompose)

        if order == "freq":
            nodes = {}
            for (row_path, col_path), node in [
                (self.expand_2d_path(node.path), node) for node in result
            ]:
                nodes.setdefault(row_path, {})[col_path] = node
            graycode_order = get_graycode_order(level, x='l', y='h')
            nodes = [nodes[path] for path in graycode_order if path in nodes]
            result = []
            for row in nodes:
                result.append(
                    [row[path] for path in graycode_order if path in row]
                )
        return result
