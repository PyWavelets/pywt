# -*- coding: utf-8 -*-

# Copyright (c) 2006-2007 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

# $Id$

"""Wavelet packet transform"""

from _pywt import MODES, Wavelet, dwt, idwt, dwt_max_level

class Node(object):
    """
    WaveletPacket tree node.
    Subnodes are called 'a' and 'd', like approximation and detail coefficients
    in Discrete Wavelet Transform
    """
    def __init__(self, parent, data, nodeName):
        self.parent = parent
        if parent is not None:
            self.wavelet = parent.wavelet
            self.mode = parent.mode
            self.level = parent.level + 1
            self.maxlevel = parent.maxlevel
            self.path = parent.path + nodeName
        else:
            self.path = ""

        # data - signal on level 0, coeffs on higher levels
        self.data = data

        # children
        self.a = None
        self.d = None

        # other attributes
        self._isZeroTree = False

    def createChild(self, part, data=None):
        #print "create", part, self.path
        if part in ("a", "d"):
            if getattr(self, part) is not None:
                print "replacing node", part, getattr(self, part).path, getattr(self, part).data, data
                raise Warning
            setattr(self, part, Node(self, data, part))
        else:
            raise ValueError
                        
    def decompose(self):
        """
        Decompose node data creating two subnodes with DWT coefficients"
        """
        if self.level < self.maxlevel:
            a, d = dwt(self.data, self.wavelet, self.mode)
            self.createChild("a", a)
            self.createChild("d", d)
            return self.a, self.d
        else:
            raise ValueError("Maximum level value reached")
        
    def reconstruct(self, update=False):
        """
        Reconstruct node's data value using coefficients from subnodes.
        If update param is True, then reconstructed data replaces node's data.

        Returns None if node is marked as ZeroTree.
        Returns original node data if all subnodes are None or are marked as ZeroTrees.
        Returns IDWT reconstructed data returned by reconstruct() method of two nodes otherwise.
        """
        if self.isZeroTree:
            return None
        
        elif (self.a is None or self.a.isZeroTree) and (self.d is None or self.d.isZeroTree):
            return self.data

        else:
            data_a = None
            data_d = None
            if self.a is not None:
                data_a = self.a.reconstruct()
            if self.d is not None:
                data_d = self.d.reconstruct()
                
            if data_a is None and data_d is None:
                raise ValueError, "Can not reconstruct. Tree is missing data"
            else:
                rec = idwt(data_a, data_d, self.wavelet, self.mode, correct_size=True)
                if update:                    
                    self.data = rec
                return rec

    def markZeroTree(self, flag=True, remove_sub=True):
        """
        Mark node as ZeroTree.

        If flag equals True, node will be marked as ZT.
        If remove_sub is True, subnodes will be removed from tree.
        """
        if not flag:
            if not self._isZeroTree:
                self._isZeroTree = False
                self.decompose()
        else:
            self._isZeroTree = True

            if remove_sub:
                self.a = None
                self.d = None

    isZeroTree = property(lambda self: self._isZeroTree, markZeroTree)
    
    def getChild(self, part, decompose=True):
        """
        Returns subnode 'a' or 'd'.

        part - subnode name ('a' or 'd')
        decompose - if True and subnodes do not exist, they will be created with
            values from decomposition of current node (some lazy evaluation here)
        """
        if part in ("a", "d"):
            if not self.isZeroTree:
                child = getattr(self, part)
                if decompose and child is None:
                    self.decompose()
                    child = getattr(self, part)
                return child
            else:
                return None
        else:
            raise ValueError("Child node can only have 'a' or 'd' name, not '%s'" % part)
    def __getitem__(self, path):
        return self.get_node(path).data
    
    def get_node(self, path):
        """
        Find node of given path in tree.

        path - string composed of "a" and "d", of total length not greater than maxlevel.

        If node does not exist yet, it will be created by decomposition of its
        parent node.
        """
        if isinstance(path, basestring):
            if(len(path)):
                return self.getChild(path[0], True)[path[1:]]
            else:
                return self
        else:
            raise IndexError("Invalid path")

    def __setitem__(self, path, data):
        self.set_node(path, data)
        
    def set_node(self, path, data):
        if isinstance(path, basestring):
            if(len(path)):
                child = self.getChild(path[0], False)
                if child is None:
                    self.createChild(path[0], data)
                    child = self.getChild(path[0], False)
                child[path[1:]] = data
            else:
                self.data = data
        else:
            raise IndexError("Invalid path")

    def walk(self, func, args=tuple()):
        """
        Walk tree and call func on every node -> func(node, *args)
        If func returns True, descending to subnodes will be proceeded.
        
        func - callable object
        args - additional func parms
        """
        if func(self, *args) and self.level < self.maxlevel:
            a = self.getChild("a")
            d = self.getChild("d")
            a.walk(func, args)    
            d.walk(func, args)
            
    def walk_depth(self, func, args=tuple()):
        """
        Walk tree and call func on every node starting from bottom most nodes.
       
        func - callable object
        args - additional func parms
        """
        if self.level < self.maxlevel:
            a = self.getChild("a")
            d = self.getChild("d")
            a.walk_depth(func, args)
            d.walk_depth(func, args)
        func(self, *args)

    # other methods
    def energy(self):
        """sum of squared data values"""
        return sum(self.data*self.data)
    
    def __str__(self):
        return str(self.data)
    
class WaveletPacket(Node):
    """
    WaveletPacket(data, wavelet, mode'sp1', maxlevel=None)
    Data structure representing Wavelet Packet decomposition of signal.

    data - original data (signal)
    wavelet - wavelet used in DWT decomposition and reconstruction
    mode - signal extension mode - see MODES
    maxlevel - maximum level of decomposition
    """
    def __init__(self, data, wavelet, mode='sp1', maxlevel=None):
        Node.__init__(self, None, data, "")

        if not isinstance(wavelet, Wavelet):
            wavelet = Wavelet(wavelet)
        self.wavelet = wavelet
        self.mode = mode

        if data is not None:
            self.data_size = len(data)
            if maxlevel is None:
                maxlevel = dwt_max_level(self.data_size, self.wavelet.dec_len)
        else:
            self.data_size = None
        
        self.maxlevel = maxlevel
        self.level = 0
        self.frequency = (0., 1.)

    def __getitem__(self, path):
        return self.get_node(path).data
    
    def get_node(self, path):
        """
        Find node of given path in tree.

        path - string composed of "a" and "d", of total length not greater than maxlevel.

        If node does not exist yet, it will be created by decomposition of its
        parent node.
        """
        if len(path) > self.maxlevel:
            raise IndexError("Path length out of range")
        else:
            return Node.get_node(self, path)

    def __setitem__(self, path, value):
        if len(path) > self.maxlevel:
            raise IndexError, "path length out of range"
        else:
            return Node.__setitem__(self, path, value)

    def __delitem__(self, path):
        """
        Mark node of given path in tree as ZeroTree.

        path - string composed of "a" and "d", of total length not greater than maxlevel.

        If node does not exist yet, it will be created by decomposition of its
        parent node.
        """
        if len(path) > 0:
            self.get_node(path).markZeroTree(True, remove_sub=True)
        else:
            raise IndexError("Invalid path")

    #def decompose(self, level):
    #    def f(node, maxlevel):
    #        return node.level < maxlevel
    #    self.walk(f, (self.maxlevel,))
        
    def reconstruct(self, update=True):
        """
        Reconstruct data value using coefficients from subnodes.
        
        If update is True, then data values will be replaced by
        reconstruction values, also in subnodes.
        """
        if self.a is not None or self.d is not None:
            data = Node.reconstruct(self, update)
            if self.data_size is not None and len(data) > self.data_size:
                data = data[:self.data_size]
            if update:
                self.data = data
            return data
        return self.data # return original data
    
    def walk(self, func, args=tuple()):
        self.getChild("a").walk(func, args)
        self.getChild("d").walk(func, args)
    walk.__doc__ = Node.walk.__doc__

    def walk_depth(self, func, args=tuple()):
        self.getChild("a").walk_depth(func, args)
        self.getChild("d").walk_depth(func, args)
    walk_depth.__doc__ = Node.walk_depth.__doc__
    
    def get_level(self, level, order="natural"):
        """
        Returns all nodes from specified level.

        order - "natural" - left to right in tree
              - "freq" - frequency ordered
        """
        if level > self.maxlevel:
            raise ValueError, ("Specified level is greater than maximum level number (%d > %d)" % (level, self.maxlevel))

        result = []

        def collect(node):
            if node.level == level:
                result.append(node)
                return False
            return True

        self.walk(collect)
        if order == "natural":
            return result
        elif order == "freq":
            graycode = ["0", "1"]
            for i in range(level-1):
                graycode = [("0" + c) for c in graycode] + [("1" + c) for c in graycode[::-1]]
            order = [int(c, 2) for c in graycode]
            return [result[i] for i in order]
            
        else:
            raise ValueError("wrong order name %s" % order)
        
    def get_nonzero(self, decompose=False):
        """
        Returns leaf nodes not belonging to any zero tree.
        """
        result = []
        
        def collect(node):
            if node.isZeroTree:
                return False

            if node.level == node.maxlevel:
                result.append(node)
                return False
            if decompose:
                if node.a is None and node.d is None:
                    #self.decompose()
                    return True
                if node.a.isZeroTree and node.d.isZeroTree:
                    result.append(node)
                    return False
                return True
            else:
                if (node.a is None or node.a.isZeroTree) and (node.d is None or node.d.isZeroTree):
                    result.append(node)
                    return False
                return True
                
        self.walk(collect)
        return result

__all__ = [Node, WaveletPacket]
