#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import subprocess


try:
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False



if sys.platform == "darwin":
    # Don't create resource files on OS X tar.
    os.environ["COPY_EXTENDED_ATTRIBUTES_DISABLE"] = "true"
    os.environ["COPYFILE_DISABLE"] = "true"


setup_args = {}


def expand_templates():
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Expanding templates")
    p = subprocess.call([sys.executable,
                          os.path.join(cwd, 'util', 'templating.py'),
                          'pywt'],
                         cwd=cwd)
    if p != 0:
        raise RuntimeError("Expanding templates failed!")


def generate_cython():
    cwd = os.path.abspath(os.path.dirname(__file__))
    print("Cythonizing sources")
    p = subprocess.call([sys.executable,
                          os.path.join(cwd, 'util', 'cythonize.py'),
                          'pywt'],
                         cwd=cwd)
    if p != 0:
        raise RuntimeError("Running cythonize failed!")


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('pywt')
    return config


if has_setuptools:
    setup_args["zip_safe"] = False
    if not os.path.exists(os.path.join("pywt", "_pywt.c")):
        setup_args["setup_requires"] = ["Cython >= 0.17.1"]


def setup_package():
    metadata = dict(
        name="PyWavelets",
        version="0.2.2",
        author="Filip Wasilewski",
        author_email="en@ig.ma",
        url="http://www.pybytes.com/pywavelets/",
        download_url="http://pypi.python.org/pypi/PyWavelets/",
        license="MIT",
        description="PyWavelets, wavelet transform module",
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
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Topic :: Software Development :: Libraries :: Python Modules"
        ],
        platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
        test_suite='nose.collector',
        cmdclass={},
        **setup_args
    )
    if len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
            sys.argv[1] in ('--help-commands', 'egg_info', '--version',
                            'clean')):
        # For these actions, NumPy is not required.
        #
        # They are required to succeed without Numpy for example when
        # pip is used to install PyWavelets when Numpy is not yet present in
        # the system.
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup
    else:
        from numpy.distutils.core import setup

        cwd = os.path.abspath(os.path.dirname(__file__))
        if not os.path.exists(os.path.join(cwd, 'PKG-INFO')):
            # Generate Cython sources, unless building from source release
            expand_templates()
            generate_cython()

    metadata['configuration'] = configuration

    setup(**metadata)


if __name__ == '__main__':
    setup_package()
