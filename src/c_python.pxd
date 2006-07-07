cdef extern from "Python.h":

    # typedefs
    ctypedef long size_t 
    ctypedef int Py_intptr_t

    # structs
    cdef struct _typeobject:
        pass
    cdef struct PyObject:
        _typeobject* ob_type

    # memory
    void* PyMem_Malloc(size_t n) 
    void PyMem_Free(void* mem) 
    object PyErr_NoMemory()
    
    void Py_DECREF(object obj)
    void Py_XDECREF(object obj)
    void Py_INCREF(object obj)
    void Py_XINCREF(object obj)

    # bool
    object PyBool_FromLong(long)

    # int
    #PyObject* PyInt_FromLong(long v)
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
    int PyTuple_Check(object p)
    int PyTuple_Size(object p) 
    PyObject* PyTuple_GET_ITEM(object p, int pos)               # notice PyObject*
    object PyTuple_GetItem(object p, int pos) 

    # cobject
    int PyCObject_Check(object p) 
    object PyCObject_FromVoidPtrAndDesc(void* cobj, void* desc, void (*destr)(void *, void *))
    void* PyCObject_AsVoidPtr(object cobj)


    # c buffer
    int PyObject_AsReadBuffer(object, void **rbuf, int *len)
    int PyObject_AsWriteBuffer(object, void **rbuf, int *len)






