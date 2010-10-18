#!/usr/bin/env python
#-*- coding: utf-8 -*-

import glob, os, os.path, sys, warnings
from distutils.core import setup
from distutils.extension import Extension

import util.templating

if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

try:
    from Cython.Distutils import build_ext as build_ext_orig 
except ImportError:
    print "A recent version of Cython is required to build PyWavelets. Get Cython from http://www.cython.org/!"
    sys.exit(1)

# tune the C compiler settings
extra_compile_args = ['-fwrapv', '-O2', '-Wall', '-fno-strict-aliasing', '-finline-limit=1',] # '-msse2'] #, '-ftree-vectorize', '-ftree-vectorizer-verbose=7']
#extra_compile_args += ['-march=pentium4',  '-mtune=pentium4']
#extra_compile_args += ['-Wno-long-long', '-Wno-uninitialized', '-Wno-unused']

macros = [('PY_EXTENSION', None),
          #('OPT_UNROLL2', None), # enable some manual unroll loop optimizations
          #('OPT_UNROLL4', None)  # enable more manual unroll loop optimizations
         ]

source_ext = '.pyx'
setup_args = {}
if 'setuptools' in sys.modules:
    setup_args['zip_safe'] = False

class build_ext(build_ext_orig):
    def build_extension(self, ext, *args, **kargs):
        # Expand templates
        templates = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src/*.template')
        util.templating.expand_files(templates, False)
        build_ext_orig.build_extension(self, ext, *args, **kargs)

cmdclass    = {'build_ext': build_ext}

dwt = Extension("pywt._pywt",
        sources = [(n + source_ext) for n in ['src/_pywt']] + \
            ["src/common.c", "src/convolution.c", "src/wavelets.c", "src/wt.c"],
        include_dirs = ['src'],
        library_dirs = [],
        runtime_library_dirs = [],
        libraries = [],
        define_macros = macros,
        extra_compile_args = extra_compile_args,
        extra_link_args = [],
        export_symbols = [],
)

ext_modules = [dwt]
packages =  ['pywt',]
package_dir = {'pywt':'pywt',}

setup(
    name = "PyWavelets",
    version = "0.2.0",
    author = "Filip Wasilewski",
    author_email = "filip.wasilewski@gmail.com",
    url = "http://www.pybytes.com/pywavelets/",
    download_url = "http://pypi.python.org/pypi/PyWavelets/",
    license = "MIT",
    description  = "PyWavelets, wavelet transform module.",
    long_description = """\
    PyWavelets is a Python wavelet transforms module that includes:
    * 1D and 2D Forward and Inverse Discrete Wavelet Transform (DWT and IDWT)
    * 1D and 2D Stationary Wavelet Transform (Undecimated Wavelet Transform)
    * 1D and 2D Wavelet Packet decomposition and reconstruction
    * Computing Approximations of wavelet and scaling functions
    * Over seventy built-in wavelet filters and support for custom wavelets
    * Single and double precision calculations
    * Results compatibility with Matlab Wavelet Toolbox (tm)
    """,
    keywords = ['wavelets', 'wavelet transform', 'DWT', 'SWT', 'scientific', 'NumPy'],
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
    ],
    ext_modules = ext_modules,
    packages = packages,
    package_dir = package_dir,
    cmdclass = cmdclass,
    **setup_args
)
