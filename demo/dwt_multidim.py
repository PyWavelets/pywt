#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint

import numpy

import pywt

data = numpy.ones((4, 4, 4, 4))  # 4D array
result = pywt.dwtn(data, 'db1')  # sixteen 4D coefficient arrays
pprint.pprint(result)
