#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
import glob, os, os.path

if os.path.exists('MANIFEST'): os.remove('MANIFEST')

try:
    from Pyrex.Distutils import build_ext
    has_pyrex = True
except ImportError:
    has_pyrex = False

if has_pyrex:
    pyx_sources = ['src/_pywt.pyx']
    cmdclass    = {'build_ext': build_ext}
else:
    pyx_sources = ['src/_pywt.c']
    cmdclass    = {}

release = {}
execfile(os.path.join('pywt','release_details.py'), {}, release)

extra_compile_args = ['-Wno-uninitialized', '-Wno-unused']

ext_modules=[ 
    Extension("pywt._pywt",
        sources = pyx_sources + ["src/common.c", "src/convolution.c", "src/wavelets.c", "src/wt.c"], 
        include_dirs = ['src'],
        library_dirs = [],
        runtime_library_dirs = [],
        libraries = [],
        extra_compile_args = extra_compile_args,
		extra_link_args = [],
		export_symbols = [],
    ),
]

setup(
    name = release["name"],
    version = release["version"],
    description = release["description"],
    long_description = release["long_description"],
    author = release["author"],
    author_email = release["author_email"], 
    url = release["url"],
    download_url = release["download_url"],
    license = release["license"],
    keywords = release["keywords"],
    platforms = release["platforms"],
    classifiers = release["classifiers"],
    
    ext_modules = ext_modules,
    
    packages = ['pywt'],
    package_dir = {'pywt':'pywt'},
    #script_args = ["build_ext"],
    
    cmdclass = cmdclass
)
