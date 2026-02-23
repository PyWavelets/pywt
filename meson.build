project(
  'PyWavelets',
  'c', 'cython',
  version: '1.10.0.dev0',
  license: 'MIT',
  meson_version: '>= 1.5.0',
  default_options: [
    'buildtype=debugoptimized',
    'b_ndebug=if-release',
    'c_std=c17',
    # We default to false here (so produce wheels like cp314), and can opt into
    # producing abi3 wheels. The setting in pyproject.toml is
    # `limited-api=true`, but this default will ensure it is opt-in:
    'python.allow_limited_api=true',  #FIXME: set to true only for testing
    #'python.allow_limited_api=false',
  ],
)

cython = find_program('cython')

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

subdir('pywt')
