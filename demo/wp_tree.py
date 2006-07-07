#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywt import WaveletPacket

wp = WaveletPacket(range(16), 'db1', maxlevel=3)
    
print [node.path for node in wp.get_nonzero(False)]
print [node.path for node in wp.get_nonzero(True)]
coeffs = [(node.path, node.data) for node in wp.get_nonzero(True)]
print coeffs
wp = WaveletPacket(None, 'db1', maxlevel=3)
for path, data in coeffs:
    wp[path] = data
#print wp["a"]
print [node.path for node in wp.get_nonzero()]
print wp.reconstruct()
