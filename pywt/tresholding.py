# -*- coding: utf-8 -*-

# Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
# See COPYING for license details.

# $Id: tresholding.py 49 2006-07-06 22:45:04Z Filip $

"""Tresholding routines"""

import numpy

def soft(data, value, substitute=0):
    mvalue = -value
    
    cond_less = numpy.less(data, value)
    cond_greater = numpy.greater(data, mvalue)

    data = numpy.where(cond_less & cond_greater, substitute, data)
    data = numpy.where(cond_less, data + value, data)
    data = numpy.where(cond_greater, data - value, data)
    
    return data

def hard(data, value, substitute=0):
    mvalue = -value
    
    cond = numpy.less(data, value)
    cond &= numpy.greater(data, mvalue)
    
    return numpy.where(cond, substitute, data)
    
def greater(data, value, substitute=0):
    return numpy.where(numpy.less(data, value), substitute, data)

def less(data, value, substitute=0):
    return numpy.where(numpy.greater(data, value), substitute, data)

def zero(data, *args):
    return numpy.zeros(len(data), 'd')

def copy(data, *args):
    return numpy.array(data, 'd')
