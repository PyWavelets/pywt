#!/usr/bin/env python
#-*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
import glob, os, os.path

if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

try:
    from Pyrex.Distutils import build_ext
    has_pyrex = True
except ImportError:
    has_pyrex = False

if has_pyrex:
    source_ext = '.pyx'
    cmdclass    = {'build_ext': build_ext}
else:
    source_ext = '.c'
    cmdclass    = {}

# gather the release details
release = {}
execfile(os.path.join(os.path.dirname(__file__), 'pywt','release_details.py'), {}, release)

# tune the C compiler settings
extra_compile_args = ['-Wno-uninitialized', '-Wno-unused', '-O2']
#extra_compile_args += ['-march=pentium3',  '-mtune=pentium3', '-msse', '-mmmx']


dwt = Extension("pywt._pywt",
        sources = [(n + source_ext) for n in ['src/_pywt']] + ["src/common.c", "src/convolution.c", "src/wavelets.c", "src/wt.c"], 
        include_dirs = ['src'],
        library_dirs = [],
        runtime_library_dirs = [],
        libraries = [],
        extra_compile_args = extra_compile_args,
		extra_link_args = [],
		export_symbols = [],
    )
 
ext_modules = [dwt]
packages =  ['pywt']
package_dir = {'pywt':'pywt'}

    
def do_setup(**extra_kwds):
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
        
        packages = packages,
        package_dir = package_dir,
        #script_args = ["build_ext"],
        
        cmdclass = cmdclass,
        **extra_kwds
    )

if __name__ == '__main__':
    do_setup()