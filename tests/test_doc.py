#!/usr/bin/env python
# -*- coding: utf-8 -*-

import doctest
import glob
import os
import unittest

docs_base = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.path.pardir, "doc", "source"))

files = glob.glob(os.path.join(docs_base, "*.rst"))\
        + glob.glob(os.path.join(docs_base, "*", "*.rst"))

assert files

suite = doctest.DocFileSuite(*files, module_relative=False, encoding="utf-8")

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite)
