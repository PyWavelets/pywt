#!/usr/bin/env python

import doctest
import glob

files = glob.glob("../doc/regression/*.rst")

for path in files:
    print "testing %s" % path
    doctest.testfile(path)
