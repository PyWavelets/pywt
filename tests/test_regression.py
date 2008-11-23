#!/usr/bin/env python

import doctest
import glob

files = glob.glob("./regression/*.txt")

for path in files:
    print "testing %s" % path
    doctest.testfile(path)
