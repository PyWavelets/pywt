#!/usr/bin/env python
from __future__ import division, print_function, absolute_import


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    import numpy as np

    config = Configuration('pywt', parent_package, top_path)

    config.add_data_dir('tests')

    # add main PyWavelets module
    config.add_extension(
        '_pywt',
        sources=["src/_pywt.c", "src/common.c", "src/convolution.c",
                 "src/wavelets.c", "src/wt.c"],
        include_dirs=["src", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.make_config_py()
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
