#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywt import WaveletPacket

wp = WaveletPacket(range(16), 'db2', maxlevel=3)
print [node.path for node in wp.get_leaf_nodes(decompose=False)]
print [node.path for node in wp.get_leaf_nodes(decompose=True)]
coeffs = [(node.path, node.data) for node in wp.get_leaf_nodes(decompose=True)]
print coeffs

wp2 = WaveletPacket(None, 'db2', maxlevel=3)
for path, data in coeffs:
    wp2[path] = data
#print wp["a"]
print [node.path for node in wp2.get_leaf_nodes(decompose=False)]
print wp2.reconstruct()
