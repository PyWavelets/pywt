#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os, sys
from distutils.core import setup, Extension

from util import commands

if sys.platform == "darwin":
    # Don't create resource files on OS X tar.
    os.environ["COPY_EXTENDED_ATTRIBUTES_DISABLE"] = "true"
    os.environ["COPYFILE_DISABLE"] = "true"

dwt = Extension("pywt._pywt",
    sources=["src/_pywt.pyx", "src/common.c", "src/convolution.c",
             "src/wavelets.c", "src/wt.c"],
    include_dirs=["src"],
    define_macros=[("PY_EXTENSION", None)],
)

ext_modules = [dwt]
packages = ["pywt"]
package_dir = {"pywt": "pywt"}

cmdclass={
    "build_ext": commands.BuildExtCommand,
    "sdist": commands.SdistCommand,
}

setup(
    name="PyWavelets",
    version="0.2.0",
    author="Filip Wasilewski",
    author_email="filip.wasilewski@gmail.com",
    url="http://www.pybytes.com/pywavelets/",
    download_url="http://pypi.python.org/pypi/PyWavelets/",
    license="MIT",
    description="PyWavelets, wavelet transform module.",
    long_description="""\
    PyWavelets is a Python wavelet transforms module that includes:
    * 1D and 2D Forward and Inverse Discrete Wavelet Transform (DWT and IDWT)
    * 1D and 2D Stationary Wavelet Transform (Undecimated Wavelet Transform)
    * 1D and 2D Wavelet Packet decomposition and reconstruction
    * Computing Approximations of wavelet and scaling functions
    * Over seventy built-in wavelet filters and support for custom wavelets
    * Single and double precision calculations
    * Results compatibility with Matlab Wavelet Toolbox (tm)
    """,
    keywords=["wavelets", "wavelet transform", "DWT", "SWT", "scientific",
              "NumPy"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    ext_modules=ext_modules,
    packages=packages,
    package_dir=package_dir,
    cmdclass=cmdclass,
    zip_safe=False,
)
