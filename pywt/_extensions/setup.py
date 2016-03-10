#!/usr/bin/env python
from __future__ import division, print_function, absolute_import


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    from numpy import get_include as get_numpy_include

    config = Configuration('_extensions', parent_package, top_path)

    sources = ["c/common.c", "c/convolution.c", "c/wt.c", "c/cwt.c", "c/wavelets.c"]
    source_templates = ["c/convolution.template.c", "c/wt.template.c", "c/cwt.template.c"]
    headers = ["c/templating.h", "c/wavelets_coeffs.h",
               "c/common.h", "c/convolution.h", "c/wt.h", "c/cwt.h", "c/wavelets.h"]
    header_templates = ["c/convolution.template.h", "c/wt.template.h", "c/cwt.template.h",
                        "c/wavelets_coeffs.template.h"]

    config.add_extension(
        '_pywt', sources=["_pywt.c"] + sources,
        depends=source_templates + header_templates + headers,
        include_dirs=["c", get_numpy_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.add_extension(
        '_dwt', sources=["_dwt.c"] + sources,
        depends=source_templates + header_templates + headers,
        include_dirs=["c", get_numpy_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.add_extension(
        '_cwt', sources=["_cwt.c"] + sources,
        depends=source_templates + header_templates + headers,
        include_dirs=["c", get_numpy_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.add_extension(
        '_swt', sources=["_swt.c"] + sources,
        depends=source_templates + header_templates + headers,
        include_dirs=["c", get_numpy_include()],
        define_macros=[("PY_EXTENSION", None)],
    )

    config.make_config_py()
    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
