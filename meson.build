project(
  'PyWavelets',
  'c', 'cython',
  version: '1.5.0.dev0',
  license: 'MIT',
  meson_version: '>= 1.0.1',
  default_options: [
    'buildtype=debugoptimized',
    'b_ndebug=if-release',
    'c_std=c99',
  ],
)

cython = find_program('cython')

# https://mesonbuild.com/Python-module.html
py_mod = import('python')
py = py_mod.find_installation(pure: false)
py_dep = py.dependency()

subdir('pywt')
