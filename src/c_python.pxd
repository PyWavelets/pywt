# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

cdef extern from "Python.h":

    # typedefs
    ctypedef long size_t 
    ctypedef int Py_intptr_t

    # structs
    ctypedef struct _typeobject:
        pass

    ctypedef struct PyObject:
        _typeobject* ob_type

    # memory
    void* PyMem_Malloc(size_t n) 
    void PyMem_Free(void* mem) 
    void Py_DECREF(object)

    # cobject
    int PyCObject_Check(object p) 
    void* PyCObject_AsVoidPtr(object cobj)

    PyObject* PyObject_GetAttrString(object, char*)
    
    # errors
    void PyErr_Clear()
