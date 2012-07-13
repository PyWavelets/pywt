#-*- coding: utf-8 -*-
# Copyright Filip Wasilewski <en@ig.ma>. All rights reserved.

from __future__ import print_function

import os
import sys
from distutils import dir_util
from distutils.cmd import Command
from distutils.command.build_ext import build_ext as build_ext_distutils
from distutils.command.sdist import sdist as sdist_distutils
from distutils.errors import DistutilsClassError

from util import templating

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")

def replace_extension(path, newext):
    return os.path.splitext(path)[0] + newext


def is_newer(file, than_file):
    return os.path.getmtime(file) > os.path.getmtime(than_file)


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        self.base_roots = ["demo", "doc", "pywt", "src", "tests", "util"]
        self.files = []
        self.dirs = ["build", "dist"]

    def finalize_options(self):
        for base_root in self.base_roots:
            if os.path.exists(base_root):
                for root, dirs, files in os.walk(base_root):
                    for f in files:
                        if os.path.splitext(f)[-1] in (".pyc", ".so", ".o", ".pyd"):
                            self.files.append(os.path.join(root, f))

                    for d in dirs:
                        if d == "__pycache__":
                            self.dirs.append(os.path.join(root, d))

    def run(self):
        for path in self.files:
            print("removing '{0}'".format(path))
            if not self.dry_run:
                os.remove(path)

        for d in self.dirs:
            dir_util.remove_tree(d, dry_run=self.dry_run)


class SdistCommand(sdist_distutils):

    def initialize_options(self):
        sdist_distutils.initialize_options(self)
        self._pyx = []
        for root, dirs, files in os.walk("src"):
            for f in files:
                if f.endswith(".pyx"):
                    self._pyx.append(os.path.join(root, f))

    def run(self):
        self.force_manifest = 1
        for pyx_file in self._pyx:
            c_file = replace_extension(pyx_file, ".c")

            if not os.path.exists(c_file):
                raise DistutilsClassError(
                    "C-source file '{0}' not found.".format(c_file))

            if is_newer(pyx_file, c_file):
                raise DistutilsClassError(
                    "C-source file '{0}' seems out of date compared to '{1}'.".format(
                        c_file, pyx_file))

        sdist_distutils.run(self)


class BuildExtCommand(build_ext_distutils):
    templates_glob = os.path.join(base_dir, "src", "*.template.*")

    extra_compile_flags = {
        #"msvc": ["/W4", "/wd4127", "/wd4702", "/wd4100"]
    }

    user_options = build_ext_distutils.user_options + [
        ("force-pyx-compile", None, "always compile Cython files"),
        ("force-template-update", None, "always expand templates"),
    ]

    boolean_options = build_ext_distutils.boolean_options + [
        "force-pyx-compile", "force-template-update"
    ]

    def initialize_options(self):
        build_ext_distutils.initialize_options(self)
        self.pyx_compile = True
        self.force_pyx_compile = False
        self.force_template_update = False

    def finalize_options(self):
        build_ext_distutils.finalize_options(self)

        self.set_undefined_options("build",
            ("force_pyx_compile", "force_pyx_compile"),
            ("force_template_update", "force_template_update")
        )

    def get_extra_compile_args(self):
        compiler_type = self.compiler.compiler_type
        return self.extra_compile_flags.get(compiler_type, [])

    def should_compile(self, source_file, compiled_file):
        if self.force_pyx_compile:
            return True
        if not os.path.exists(compiled_file):
            return True
        if is_newer(source_file, compiled_file):
            return True
        return False

    def compile_cython_file(self, extension, pyx_source_file):
        c_source_file = replace_extension(pyx_source_file, ".c")

        if not self.pyx_compile:
            print("Cython compilation disabled. Using compiled file:",
                c_source_file)
            return c_source_file

        try:
            from Cython.Compiler.Main import compile
        except ImportError:
            print("Cython is not installed. Using compiled file:",
                pyx_source_file)
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
            force_update=self.force_template_update)
        build_ext_distutils.build_extensions(self)

    def build_extension(self, ext):
        ext.extra_compile_args += self.get_extra_compile_args()
        self.compile_sources(ext, ext.sources)
        build_ext_distutils.build_extension(self, ext)


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import subprocess
        raise SystemExit(
            subprocess.call([sys.executable, "tests/test_doc.py"]))
