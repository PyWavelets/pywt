// Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
// See COPYING for license details.

// Based on http://numeric.scipy.org/array_interface.html by Travis E. Oliphant
// See http://new.scipy.org/Wiki/Cookbook/ArrayStruct_and_Pyrex 

// Array interface (__array_struct__) constants and helpers

#ifndef _ARRAY_INTERFACE_H_
#define _ARRAY_INTERFACE_H_

#include "Python.h"

#define __PY_ARRAY_INTERFACE_VERSION__ 0x0002 // TODO: update for SVN's 0x0003 compatibility

typedef Py_intptr_t intp;

enum PyGenericArray_KINDS {
    PyArrayKind_BOOL    = 'b',
    PyArrayKind_INT     = 'i',
    PyArrayKind_UINT    = 'u',
    PyArrayKind_FLOAT   = 'f',
    PyArrayKind_COMPLEX = 'c',
    PyArrayKind_STRING  = 'S',
    PyArrayKind_UNICODE = 'U',
    PyArrayKind_OBJECT  = 'O',
    PyArrayKind_RECORD  = 'R',
    PyArrayKind_VOID    = 'V',
    PyArrayKind_BIT     = 't',
    PyArrayKind_OTHER   = 'X'
};

enum {
	GA_CONTIGUOUS      =0x001,
	GA_FORTRAN         =0x010,
	GA_ALIGNED         =0x100,
	GA_NOTSWAPPED      =0x200,
	GA_WRITEABLE       =0x400,
	GA_ARR_HAS_DESCR   =0x800
	};

typedef struct  {
    int two;                         // equals 2, sanity check
    int nd;                          // number of dimensions
    char typekind;                   // elements kind - PyDimArray_KINDS
    int itemsize;                    // size of each element
    int flags;                       // flags indicating how the data should be interpreted
    intp *shape;                     // A length-nd array of shape information
    intp *strides;                   // A length-nd array of stride information
    void *data;                      // A pointer to the first element of the array
    PyObject *descr;                 // NULL or data-description -- must set ARR_HAS_DESCR flag
} PyGenericArrayInterface;

#define GA_CONTINUOUS_C_RO    (GA_CONTIGUOUS | GA_ALIGNED)
#define GA_CONTINUOUS_C       (GA_CONTIGUOUS | GA_ALIGNED | GA_WRITEABLE)

#define PyArrayInterface_IS_KIND(ai, kind)  ((ai->typekind) == kind)

#define PyArrayInterface_IS_C_ARRAY(ai)     ((((ai)->flags) & GA_CONTINUOUS_C) == GA_CONTINUOUS_C)
#define PyArrayInterface_IS_C_ARRAY_RO(ai)  ((((ai)->flags) & GA_CONTINUOUS_C_RO) == GA_CONTINUOUS_C_RO)

#define PyArrayInterface_IS_CONTIGUOUS(ai)  (((ai)->flags) & GA_CONTIGUOUS)
#define PyArrayInterface_IS_FORTRAN(ai)     (((ai)->flags) & GA_FORTRAN)
#define PyArrayInterface_IS_WRITABLE(ai)    (((ai)->flags) & GA_WRITABLE)
#define PyArrayInterface_IS_ALIGNED(ai)     (((ai)->flags) & GA_ALIGNED)
#define PyArrayInterface_HAS_DESCR(ai)      (((ai)->flags) & GA_ARR_HAS_DESCR)

#define PyArrayInterface_TWO(ai)            ((ai)->two)
#define PyArrayInterface_ND(ai)             ((ai)->nd)
#define PyArrayInterface_TYPEKIND(ai)       ((ai)->typekind)
#define PyArrayInterface_ITEMSIZE(ai)       ((ai)->itemsize)
#define PyArrayInterface_FLAGS(ai)          ((ai)->flags)
#define PyArrayInterface_SHAPES(ai)         ((ai)->shape)
#define PyArrayInterface_SHAPE(ai, n)       ((ai)->shape[n])
#define PyArrayInterface_STRIDES(ai)        ((ai)->strides)
#define PyArrayInterface_STRIDE(ai, n)      ((ai)->strides[n])
#define PyArrayInterface_DATA(ai)           ((ai)->data)
#define PyArrayInterface_DESCR(ai)          (PyArrayInterface_HAS_DESCR(ai) ? ((ai)->descr) : NULL)

#define PyArrayInterface_DATA_AS_FLOAT64_C_ARRAY(ai)     ( \
            (PyArrayInterface_IS_C_ARRAY(ai) && PyArrayInterface_IS_KIND(ai, PyArrayKind_FLOAT) && (PyArrayInterface_ITEMSIZE(ai) == 8)) \
                ? ((double*)(ai)->data) : NULL )

#define PyArrayInterface_DATA_AS_FLOAT64_C_ARRAY_RO(ai)  ( \
            (PyArrayInterface_IS_C_ARRAY_RO(ai) && PyArrayInterface_IS_KIND(ai, PyArrayKind_FLOAT) && (PyArrayInterface_ITEMSIZE(ai) == 8)) \
                ? ((double*)(ai)->data) : NULL )

#define PyArrayInterface_DATA_AS_FLOAT32_C_ARRAY(ai)     ( \
            (PyArrayInterface_IS_C_ARRAY(ai) && PyArrayInterface_IS_KIND(ai, PyArrayKind_FLOAT) && (PyArrayInterface_ITEMSIZE(ai) == 4)) \
                ? ((float*)(ai)->data) : NULL )

#define PyArrayInterface_DATA_AS_FLOAT32_C_ARRAY_RO(ai)  ( \
            (PyArrayInterface_IS_C_ARRAY_RO(ai) && PyArrayInterface_IS_KIND(ai, PyArrayKind_FLOAT) && (PyArrayInterface_ITEMSIZE(ai) == 4)) \
                ? ((float*)(ai)->data) : NULL )


#define PyArrayInterface_DATA_AS_FLOAT_C_ARRAY_RO(ai)  ( \
            (PyArrayInterface_IS_C_ARRAY_RO(ai) && PyArrayInterface_IS_KIND(ai, PyArrayKind_FLOAT) \
              && ((PyArrayInterface_ITEMSIZE(ai) == 4) || (PyArrayInterface_ITEMSIZE(ai) == 8))) \
                ? ((void*)(ai)->data) : NULL )

#define PyArrayInterface_DATA_AS_FLOAT_C_ARRAY(ai)     ( \
            (PyArrayInterface_IS_C_ARRAY(ai) && PyArrayInterface_IS_KIND(ai, PyArrayKind_FLOAT) \
              && ((PyArrayInterface_ITEMSIZE(ai) == 4) || (PyArrayInterface_ITEMSIZE(ai) == 8))) \
                ? ((void*)(ai)->data) : NULL )


#define PyArrayInterface_CHECK(ai)      (PyArrayInterface_TWO(ai) == 2)
#define PyArrayInterface_CHECK_1D(ai)   (PyArrayInterface_CHECK(ai) && PyArrayInterface_ND(ai) == 1)
#define PyArrayInterface_CHECK_2D(ai)   (PyArrayInterface_CHECK(ai) && PyArrayInterface_ND(ai) == 2)

#endif
