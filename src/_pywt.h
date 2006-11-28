#ifndef __HAS_PYX__pywt
#define __HAS_PYX__pywt
#ifdef __cplusplus
#define __PYX_EXTERN_C extern "C"
#else
#define __PYX_EXTERN_C extern
#endif
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) WaveletType;

struct WaveletObject {
  PyObject_HEAD
  Wavelet (*w);
  PyObject *name;
  PyObject *number;
};
PyMODINIT_FUNC init_pywt(void);
#endif /* __HAS_PYX__pywt */
