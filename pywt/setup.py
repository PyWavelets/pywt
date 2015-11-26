#!/usr/bin/env python
from __future__ import division, print_function, absolute_import


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    import numpy as np

    config = Configuration('pywt', parent_package, top_path)

    config.add_data_dir('tests')

    sources = ["c/common", "c/convolution", "c/wavelets", "c/wt"]
    source_templates = ["c/convolution", "c/wt"]
    headers = ["c/templating", "c/wavelets_coeffs"]
    header_templates = ["c/convolution", "c/wt", "c/wavelets_coeffs"]

    c_files = ["_extensions/{0}.c".format(s) for s in sources]
    depends = (["_extensions/{0}.template.c".format(s) for s in source_templates]
               + ["_extensions/{0}.template.h".format(s) for s in header_templates]
               + ["_extensions/{0}.h".format(s) for s in headers]
               + ["_extensions/{0}.h".format(s) for s in sources])

    config.add_subpackage(
        '_extensions',
        subpackage_path="_extensions",
    )

    config.add_extension(
        '_extensions._pywt',
        sources=["_extensions/_pywt.c"] + c_files,
        depends=depends,
        include_dirs=["_extensions", "_extensions/c", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.add_extension(
        '_extensions._dwt',
        sources=["_extensions/_dwt.c"] + c_files,
        depends=depends,
        include_dirs=["_extensions", "_extensions/c", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.add_extension(
        '_extensions._swt',
        sources=["_extensions/_swt.c"] + c_files,
        depends=depends,
        include_dirs=["_extensions", "_extensions/c", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.make_config_py()
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
