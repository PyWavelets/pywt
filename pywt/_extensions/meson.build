m_dep = cc.find_library('m', required : false)
if m_dep.found()
  add_project_link_arguments('-lm', language : 'c')
endif

# Uses the `numpy-config` executable (or a user's numpy.pc pkg-config file).
_numpy_dep = dependency('numpy', version: ['>=2.0', '<3'])
np_dep = declare_dependency(
  dependencies: _numpy_dep,
  # Don't use the deprecated NumPy C API. Define this to a fixed version
  # instead of NPY_API_VERSION in order not to break compilation for released
  # PyWavelets versions when NumPy introduces a new deprecation.
  compile_args: ['-DNPY_NO_DEPRECATED_API=NPY_2_0_API_VERSION'],
)

sources = [
  'c/common.c',
  'c/convolution.c',
  'c/cwt.c',
  'c/wavelets.c',
  'c/wt.c',
]

# No generated Cython sources are involved anymore, but these copies are
# still needed for correct rebuilds: the `depends: _cython_tree` on the
# generator is what re-cythonizes the .pyx files when a .pxd changes.
# Cython's own depfile output (`cython -M`, used by Meson's native Cython
# support) omits module-namespace cimports like `from . cimport c_wt`
# (seen with Cython 3.2.9), so switching to it would cause stale builds.
_cython_tree = [
  fs.copyfile('__init__.py'),
  fs.copyfile('common.pxd'),
  fs.copyfile('_cwt.pxd'),
  fs.copyfile('c_wt.pxd'),
  fs.copyfile('_dwt.pxd'),
  fs.copyfile('_pywt.pxd'),
  fs.copyfile('wavelet.pxd'),
  fs.copyfile('wavelets_list.pxi'),
]

c_args = ['-DPY_EXTENSION', '-D_USE_MATH_DEFINES']

libc_wt = static_library('c_wt',
  sources,
  c_args : c_args,
  include_directories : 'c',
  dependencies : py_dep,
)

cy = meson.get_compiler('cython')
cython_args = ['-3', '--fast-fail', '--output-file', '@OUTPUT@', '--include-dir', '@BUILD_ROOT@', '@INPUT@']
if cy.version().version_compare('>=3.1.0')
  cython_args += ['-Xfreethreading_compatible=True']
endif

cython_gen = generator(cython,
  arguments : cython_args,
  output : '@BASENAME@.c',
  depends : _cython_tree
)

pyx_files = [
  ['_cwt', fs.copyfile('_cwt.pyx')],
  ['_dwt', fs.copyfile('_dwt.pyx')],
  ['_swt', fs.copyfile('_swt.pyx')],
  ['_pywt', fs.copyfile('_pywt.pyx')],
]

cy_deps = declare_dependency(sources: [__init__py, _cython_tree])
foreach pyx_file: pyx_files
  py.extension_module(pyx_file[0],
    [cython_gen.process(pyx_file[1])],
    c_args : c_args,
    include_directories : 'c',
    dependencies : [np_dep, cy_deps],
    link_with : libc_wt,
    install: true,
    subdir: 'pywt/_extensions',
  )
endforeach
