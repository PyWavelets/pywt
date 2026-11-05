fs = import('fs')

py.install_sources(
  [
    '__init__.py',
    '_cwt.py',
    '_doc_utils.py',
    '_dwt.py',
    '_functions.py',
    '_mra.py',
    '_multidim.py',
    '_multilevel.py',
    '_pytest.py',
    '_pytesttester.py',
    '_swt.py',
    '_thresholding.py',
    '_utils.py',
    '_wavelet_packets.py',
    'conftest.py',
  ],
  subdir: 'pywt'
)

generate_version = custom_target(
  'generate-version',
  install: true,
  build_always_stale: true,
  build_by_default: true,
  output: 'version.py',
  input: '../util/version_utils.py',
  command: [py, '@INPUT@', '--source-root', '@SOURCE_ROOT@'],
  install_dir: py.get_install_dir() / 'pywt',
  install_tag: 'python-runtime',
)

cc = meson.get_compiler('c')

# Check for complex support (same check as numpy/_core/meson.build; MSVC has
# no C99 complex and provides struct-based types instead, see
# pywt/_extensions/c/common.h)
if not cc.has_header('complex.h')
  error('"complex.h" header not found')
endif

if cc.get_id() == 'msvc' or cc.get_id() == 'clang-cl'
  complex_types_to_check = [
    ['PYWT_SIZEOF_COMPLEX_FLOAT', '_Fcomplex'],
    ['PYWT_SIZEOF_COMPLEX_DOUBLE', '_Dcomplex'],
  ]
else
  complex_types_to_check = [
    ['PYWT_SIZEOF_COMPLEX_FLOAT', 'complex float'],
    ['PYWT_SIZEOF_COMPLEX_DOUBLE', 'complex double'],
  ]
endif
cdata = configuration_data()
foreach symbol_type: complex_types_to_check
  if not cc.has_type(symbol_type[1], prefix: '#include <complex.h>')
    t = symbol_type[1]
    error(f'"complex.h" header does not include complex type @t@')
  endif
  cdata.set(symbol_type[0], cc.sizeof(symbol_type[1], prefix: '#include <complex.h>'))
endforeach

install_subdir('data', install_dir: py.get_install_dir() / 'pywt')
install_subdir('tests', install_dir:  py.get_install_dir() / 'pywt')

# Copy needed for Cython code in _extensions
__init__py = fs.copyfile('__init__.py')

subdir('_extensions')
