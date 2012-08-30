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
        #pass

    # memory
    void* PyMem_Malloc(size_t n) 
    void PyMem_Free(void* mem) 
    object PyErr_NoMemory()
    
    void Py_DECREF(object)
    void Py_XDECREF(object)
    void Py_INCREF(object obj)
    void Py_XINCREF(object obj)

    # bool
    object PyBool_FromLong(long)

    # int
    object PyInt_FromLong(long v)
    long PyInt_AsLong(object io) 

    # float
    #PyObject* PyFloat_FromDouble(double v) 
    double PyFloat_AsDouble(PyObject*  pyfloat) except? -1      # notice PyObject*
    # string
    object PyString_FromString(char*)
    object PyString_FromStringAndSize(char *v, int len) 

    # list
    int PyList_Check(object p) 
    int PyList_CheckExact(object p) 
    object PyList_New( int len) 
    int PyList_Size(object list) 
    object PyList_GetItem(object list, int index) 
    PyObject* PyList_GET_ITEM(object list, int index)           # notice PyObject*
    int PyList_SetItem(object list, int index, PyObject* item)  # notice PyObject*
    int PyList_Append(object list, object item) 

    # tuple
    object PyTuple_New(int len)
    int PyTuple_Check(object p)
    int PyTuple_Size(object p) 
    PyObject* PyTuple_GET_ITEM(object p, int pos)               # notice PyObject*
    object PyTuple_GetItem(object p, int pos) 
    void PyTuple_SET_ITEM(object p, int pos, object o) 




    # cobject
    int PyCObject_Check(object p) 
    object PyCObject_FromVoidPtrAndDesc(void* cobj, void* desc, void (*destr)(void *, void *))
    void* PyCObject_AsVoidPtr(object cobj)


    # c buffer
    int PyObject_AsReadBuffer(object, void **rbuf, int *len)
    int PyObject_AsWriteBuffer(object, void **rbuf, int *len)


    PyObject* PyObject_GetAttrString(object, char*)
    object PyObject_GetAttr(object, char*)
    int PyObject_HasAttrString(object, char*)
    
    ctypedef struct PyTypeObject:
        pass
    ctypedef PyTypeObject PyInt_Type
    
    int PyObject_IsInstance(object inst, object cls) 
    int PyObject_TypeCheck(object obj, PyTypeObject* type)

    int PyInt_Check(object o) 


    PyObject* PyErr_Occurred()
    void PyErr_Print()
    void PyErr_Clear()
    
            

