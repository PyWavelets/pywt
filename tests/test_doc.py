#!/usr/bin/env python

import doctest
import glob

files = glob.glob("../doc/source/*.rst") + glob.glob("../doc/source/ref/*.rst")
for path in files:
    print "testing %s" % path
    doctest.testfile(path)
