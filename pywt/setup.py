#!/usr/bin/env python
from __future__ import division, print_function, absolute_import


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    import numpy as np

    config = Configuration('pywt', parent_package, top_path)

    config.add_data_dir('tests')

    sources = ["_pywt", "common", "convolution", "wavelets", "wt"]
    source_templates = ["convolution", "wt"]
    headers = ["templating", "wavelets_coeffs"]
    header_templates = ["convolution", "wt", "wavelets_coeffs"]

    # add main PyWavelets module
    config.add_extension(
        '_pywt',
        sources=["src/{0}.c".format(s) for s in sources],
        depends=(["src/{0}.template.c".format(s) for s in source_templates]
                 + ["src/{0}.template.h".format(s) for s in header_templates]
                 + ["src/{0}.h".format(s) for s in headers]
                 + ["src/{0}.h".format(s) for s in sources]),
        include_dirs=["src", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.make_config_py()
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
