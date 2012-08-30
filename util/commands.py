#-*- coding: utf-8 -*-
# Copyright Filip Wasilewski <en@ig.ma>. All rights reserved.

from __future__ import print_function

import os
import sys

try:
    from setuptools import Command
    from setuptools.command.build_ext import build_ext as _build_ext
    from setuptools.command.sdist import sdist as _sdist
    from setuptools.extension import Extension as _Extension
    has_setuptools = True
except ImportError:
    from distutils.cmd import Command # noqa
    from distutils.command.build_ext import build_ext as _build_ext
    from distutils.command.sdist import sdist as _sdist
    from distutils.core import Extension
    has_setuptools = False

from distutils import dir_util
from distutils.errors import DistutilsClassError

import templating

base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")

if has_setuptools:
    # Remove special handling of .pyx files from class patched by setuptools
    class Extension(_Extension):
        def __init__(self, name, sources, *args, **kwargs):
            _Extension.__init__(self, name, sources, *args, **kwargs)
            self.sources = sources


def replace_extension(path, newext):
    return os.path.splitext(path)[0] + newext


def is_newer(file, than_file):
    return os.path.getmtime(file) > os.path.getmtime(than_file)


class CleanCommand(Command):
    user_options = []

    def initialize_options(self):
        self.base_roots = ["demo", "doc", "pywt", "src", "tests", "util"]
        self.dirty = [".pyc", ".so", ".o", ".pyd"]
        self.files = []
        self.dirs = ["build", "dist"]

    def finalize_options(self):
        for base_root in self.base_roots:
            if os.path.exists(base_root):
                for root, dirs, files in os.walk(base_root):
                    for f in files:
                        if os.path.splitext(f)[-1] in self.dirty:
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
            if os.path.exists(d):
                dir_util.remove_tree(d, dry_run=self.dry_run)


class SdistCommand(_sdist):

    def initialize_options(self):
        _sdist.initialize_options(self)
        self._pyx = []
        self._templates = []
        for root, dirs, files in os.walk("src"):
            for f in files:
                if f.endswith(".pyx"):
                    self._pyx.append(os.path.join(root, f))
                elif ".template" in f:
                    self._templates.append(os.path.join(root, f))

    def validate_templates_expanded(self):
        for template_file in self._templates:
            destination_file = templating.get_destination_filepath(
                template_file)

            if not os.path.exists(destination_file):
                raise DistutilsClassError(
                    "Expanded file '{0}' not found. "
                    "Run build first.".format(destination_file))

            if templating.needs_update(template_file, destination_file):
                raise DistutilsClassError(
                    "Expanded file '{0}' seems out of date compared to '{1}'. "
                    "Run build first.".format(destination_file, template_file))

    def validate_pyx_expanded(self):
        for pyx_file in self._pyx:
            c_file = replace_extension(pyx_file, ".c")

            if not os.path.exists(c_file):
                raise DistutilsClassError(
                    "C-source file '{0}' not found. "
                    "Run build first.".format(c_file))

            if is_newer(pyx_file, c_file):
                raise DistutilsClassError(
                    "C-source file '{0}' seems out of date compared to '{1}'. "
                    "Run build first.".format(c_file, pyx_file))

    def run(self):
        self.force_manifest = 1
        self.validate_templates_expanded()
        self.validate_pyx_expanded()
        _sdist.run(self)


class BuildExtCommand(_build_ext):
    templates_glob = os.path.join(base_dir, "src", "*.template.*")

    extra_compile_flags = {
        #"msvc": ["/W4", "/wd4127", "/wd4702", "/wd4100"]
    }

    user_options = _build_ext.user_options + [
        ("force-pyx-compile", None, "always compile Cython files"),
        ("force-template-update", None, "always expand templates"),
    ]

    boolean_options = _build_ext.boolean_options + [
        "force-pyx-compile", "force-template-update"
    ]

    def initialize_options(self):
        _build_ext.initialize_options(self)
        self.pyx_compile = True
        self.force_pyx_compile = False
        self.force_template_update = False

    def finalize_options(self):
        _build_ext.finalize_options(self)

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
        _build_ext.build_extensions(self)

    def build_extension(self, ext):
        ext.extra_compile_args += self.get_extra_compile_args()
        self.compile_sources(ext, ext.sources)
        _build_ext.build_extension(self, ext)


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
