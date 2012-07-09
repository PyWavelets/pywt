#!/usr/bin/env python

import os
import glob
import doctest

docs_base = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, "doc", "source"))
files = glob.glob(os.path.join(docs_base, "regression", "*.rst"))

assert files

for path in files:
    print "testing %s" % path
    doctest.testfile(path)
