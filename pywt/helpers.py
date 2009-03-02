# -*- coding: utf-8 -*-

# Copyright (c) 2006-2008 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

# $Id: $

"""
"""


from _pywt import Wavelet
from cwt import CWavelet

def wavelet_for_name(name):
    if not isinstance(name, basestring):
        raise TypeError("Wavelet name must be a string, not %s" % type(name))
    try:
        wavelet = Wavelet(name)
    except ValueError:
        try:
            wavelet = CWavelet(name)
        except:
            raise
            #raise ValueError("Invalid wavelet name - %s." % name)
    return wavelet
