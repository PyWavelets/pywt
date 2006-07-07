# Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
# See COPYING for license details.

# see http://numeric.scipy.org/array_interface.html
# see http://new.scipy.org/Wiki/Cookbook/ArrayStruct_and_Pyrex

# $Id: c_array_interface.pxd 53 2006-07-07 15:59:33Z Filip $

cimport c_python

cdef extern from "array_interface.h":

    ctypedef struct PyGenericArrayInterface:
        int version                     # contains array interace version number (min. 2)
        int nd                          # number of dimensions
        char typekind                   # kind in array --- character code of typestr
        int itemsize                    # size of each element
        int flags                       # flags indicating how the data should be interpreted
        c_python.Py_intptr_t *shape     # A length-nd array of shape information
        c_python.Py_intptr_t *strides   # A length-nd array of stride information
        void *data                      # A pointer to the first element of the array

    ctypedef enum PyGenericArray_KINDS:
        PyArrayKind_BOOL
        PyArrayKind_INT
        PyArrayKind_UINT
        PyArrayKind_FLOAT
        PyArrayKind_COMPLEX
        PyArrayKind_STRING
        PyArrayKind_UNICODE
        PyArrayKind_OBJECT
        PyArrayKind_RECORD
        PyArrayKind_VOID
        PyArrayKind_BIT
        PyArrayKind_OTHER

    ctypedef enum PyArray_FLAGS:
        CONTIGUOUS
        FORTRAN
        ALIGNED
        NOTSWAPPED
        WRITEABLE

    cdef double* PyArrayInterface_DATA_AS_DOUBLE_C_ARRAY(PyGenericArrayInterface* )
    cdef double* PyArrayInterface_DATA_AS_DOUBLE_C_ARRAY_RO(PyGenericArrayInterface* )

    cdef int PyArrayInterface_IS_C_ARRAY(PyGenericArrayInterface* )
    cdef int PyArrayInterface_IS_C_ARRAY_RO(PyGenericArrayInterface* )

    cdef int PyArrayInterface_CHECK(PyGenericArrayInterface* )
    cdef int PyArrayInterface_CHECK_1D(PyGenericArrayInterface* )
    cdef int PyArrayInterface_CHECK_2D(PyGenericArrayInterface* )

    cdef int PyArrayInterface_SHAPE(PyGenericArrayInterface*, int)
