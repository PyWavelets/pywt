#-*- coding: utf-8 -*-

# Release details for package

name         = "PyWavelets"
version      = "0.2.0"
author       = "Filip Wasilewski"
author_email = "filip.wasilewski@gmail.com"
url          = "http://www.pybytes.com/pywavelets/"
download_url = "http://pypi.python.org/pypi/PyWavelets/"
license      = "MIT"
description  = "PyWavelets, wavelet transform module."
keywords     = ['wavelets', 'wavelet transform', 'DWT', 'SWT', 'scientific', 'NumPy']
platforms    = ['Linux', 'Mac OSX', 'Windows XP/2000/NT']
svn          = "http://wavelets.scipy.org/svn/multiresolution/pywt/trunk"


long_description = \
"""
PyWavelets is a Python wavelet transforms module that includes:

  * 1D and 2D Forward and Inverse Discrete Wavelet Transform (DWT and IDWT)
  * 1D and 2D Stationary Wavelet Transform (Undecimated Wavelet Transform)
  * 1D and 2D Wavelet Packet decomposition and reconstruction
  * Computing Approximations of wavelet and scaling functions
  * Over seventy built-in wavelet filters and support for custom wavelets
  * Single and double precision calculations
  * Results compatibility with Matlab Wavelet Toolbox (tm)
"""

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: C',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]
