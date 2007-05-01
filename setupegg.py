#!/usr/bin/env python
#-*- coding: utf-8 -*-

import ez_setup
ez_setup.use_setuptools()

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from setuptools import setup

from setup import *

do_setup(zip_safe=False,
         #install_requires=["numpy >=0.9.8"],
        )