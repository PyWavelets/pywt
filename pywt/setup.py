#!/usr/bin/env python
from __future__ import division, print_function, absolute_import


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    import numpy as np

    config = Configuration('pywt', parent_package, top_path)

    config.add_data_dir('tests')

    sources = ["_pywt", "_dwt",
               "c/common", "c/convolution", "c/wavelets", "c/wt"]
    source_templates = ["c/convolution", "c/wt"]
    headers = ["c/templating", "c/wavelets_coeffs"]
    header_templates = ["c/convolution", "c/wt", "c/wavelets_coeffs"]

    config.add_extension(
        '_extensions._pywt',
        sources=["src/{0}.c".format(s) for s in sources],
        depends=(["src/{0}.template.c".format(s) for s in source_templates]
                 + ["src/{0}.template.h".format(s) for s in header_templates]
                 + ["src/{0}.h".format(s) for s in headers]
                 + ["src/{0}.h".format(s) for s in sources]),
        include_dirs=["src", "src/c", np.get_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.make_config_py()
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
