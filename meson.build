project(
  'PyWavelets',
  'c', 'cython',
  version: '1.9.0',
  license: 'MIT',
  meson_version: '>= 1.1.0',
  default_options: [
    'buildtype=debugoptimized',
    'b_ndebug=if-release',
    'c_std=c17',
  ],
)

cython = find_program('cython')

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

subdir('pywt')
