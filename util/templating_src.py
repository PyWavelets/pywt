#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Ralf Gommers
# Date: 1 Oct 2013


import glob
import os

from numpy.distutils.conv_template import process_str


def needs_update(src_path, dst_path):
    # No update if .c file exists and is newer than last template change.
    if not os.path.exists(dst_path):
        return True
    if os.path.getmtime(dst_path) < os.path.getmtime(src_path):
        return True

    return False


def expand_files(glob_pattern):
    files = glob.glob(glob_pattern)
    for src_path in files:
        dst_path = os.path.splitext(src_path)[0]
        if needs_update(src_path, dst_path):
            print("expanding template: %s -> %s" % (src_path, dst_path))
            content = process_str(open(src_path, "rb").read().decode('utf-8'))
            new_file = open(dst_path, "wb")
            new_file.write(content.encode('utf-8'))
            new_file.close()


if __name__ == '__main__':
    cwd = os.path.abspath(os.path.dirname(__file__))
    templates_glob = os.path.join(cwd, '..', 'pywt', "src", "*.[ch].src")
    expand_files(templates_glob)

