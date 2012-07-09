#-*- coding: utf-8 -*-
# Copyright Filip Wasilewski <en@ig.ma>. All rights reserved.

from __future__ import print_function

import os
import sys
from distutils.command.build_ext import build_ext as build_ext_distutils
from distutils.command.sdist import sdist as sdist_distutils

from util import templating

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")

def replace_extension(path, newext):
    return os.path.splitext(path)[0] + newext


class SdistCommand(sdist_distutils):
    def run(self):
        self.force_manifest = 1
        sdist_distutils.run(self)


class BuildExtCommand(build_ext_distutils):
    templates_force_update = False
    templates_glob = os.path.join(base_dir, "src", "*.template.*")

    pyx_compile = True # enable Cython files compilation
    pyx_force_compile = False # always compile Cython files

    extra_compile_flags = {}

    def get_extra_compile_args(self):
        compiler_type = self.compiler.compiler_type
        return self.extra_compile_flags.get(compiler_type, [])

    def should_compile(self, source_file, compiled_file):
        if self.pyx_force_compile:
            return True
        if not os.path.exists(compiled_file):
            return True
        if os.path.getmtime(source_file) > os.path.getmtime(compiled_file):
            return True
        return False

    def compile_cython_file(self, extension, pyx_source_file):
        c_source_file = replace_extension(pyx_source_file, ".c")

        if not self.pyx_compile:
            print("Cython compilation disabled. Using compiled file:", c_source_file)
            return c_source_file

        try:
            from Cython.Compiler.Main import compile
        except ImportError:
            print("Cython is not installed. Using compiled file:", pyx_source_file)
            return c_source_file

        if not self.should_compile(pyx_source_file, c_source_file):
            print("Generated Cython file is up-to-date.")
            return c_source_file

        print("Compiling Cython file:", pyx_source_file)
        result = compile(pyx_source_file, full_module_name=extension.name)

        if result.c_file:
            c_source_file = result.c_file
            # Py2 distutils can't handle unicode file paths
            if sys.version_info[0] < 3:
                filename_encoding = sys.getfilesystemencoding()
                if filename_encoding is None:
                    filename_encoding = sys.getdefaultencoding()
                c_source_file = c_source_file.encode(filename_encoding)
        else:
            print("Compilation failed:", pyx_source_file)
        return c_source_file

    def compile_sources(self, extension, sources):
        for i, source in enumerate(sources):
            base, ext = os.path.splitext(source)
            if ext == ".pyx":
                c_source_file = self.compile_cython_file(extension, source)
                # substitute .pyx file with compiled .c file
                sources[i] = c_source_file

    def build_extensions(self):
        templating.expand_files(self.templates_glob,
            force_update=self.templates_force_update)
        build_ext_distutils.build_extensions(self)

    def build_extension(self, ext):
        ext.extra_compile_args += self.get_extra_compile_args()
        self.compile_sources(ext, ext.sources)
        build_ext_distutils.build_extension(self, ext)
