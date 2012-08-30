# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

cdef enum DTYPE: # itemsize
    FLOAT32 = 4
    FLOAT64 = 8

cdef struct Buffer:
    void* data
    index_t len
    DTYPE dtype
    
cdef object memory_buffer_object(Py_ssize_t length, DTYPE dtype):
    if dtype == FLOAT64:
        return float64_memory_buffer_object(length)
    elif dtype == FLOAT32:
        return float32_memory_buffer_object(length)
    else:
        raise ValueError("dtype must be in (%s, %s), not %s." % (FLOAT32, FLOAT64, dtype))

###############################################################################
# buffer objects handling

#void** buffer_addr, index_t* buffer_len, unsigned int* itemsize

cdef int array_object_as_float_buffer(object source, Buffer* buffer, char rwmode) except -1:
    # Get object buffer for reading (rwmode = 'r') or writing (rwmode = 'w')
    #
    # source      - source object exposing array interface
    # buffer_addr - will be set on success to 
    # buffer_len  - set to buffer length
    # itemsize    - set to item size (4 for float32, 8 for float 64)
    # rwmode      - read/write mode
    # 
    # returns     -  0 - ok
    #             - -1 - no __array_struct__ attr
    #             - -2, -3, -4 - other errors 
    
    # TODO: extract and create object wrapper?
    # TODO: raise exceptions instead of return negative values?

    cdef c_array_interface.PyGenericArrayInterface* array_struct
    cdef object cobject
    cdef void* data
    cdef index_t data_len

    if hasattr(source, '__array_struct__'):
        cobject = source.__array_struct__
        if c_python.PyCObject_Check(cobject):
            array_struct = <c_array_interface.PyGenericArrayInterface*> c_python.PyCObject_AsVoidPtr(cobject)
            if not (c_array_interface.PyArrayInterface_CHECK_1D(array_struct)):
                raise ValueError("1D array expected.")
                return -1
            data_len = c_array_interface.PyArrayInterface_SHAPE(array_struct, 0)
            if data_len < 1:
                raise ValueError("invalid data size - %s." % data_len)
                return -1
            buffer.len = data_len

            if rwmode == c'w':
                data = c_array_interface.PyArrayInterface_DATA_AS_FLOAT_C_ARRAY(array_struct)
            elif rwmode == c'r':
                data = c_array_interface.PyArrayInterface_DATA_AS_FLOAT_C_ARRAY_RO(array_struct)
            else:
                raise ValueError("rwmode value not in (c'r', c'w').")
                return -1
            
            if data is NULL:
                return -2 # not C contiguous array or data type is not double or float, fail silently

            buffer.data = data
            buffer.dtype = <DTYPE> c_array_interface.PyArrayInterface_ITEMSIZE(array_struct)
            assert buffer.dtype == FLOAT32 or buffer.dtype == FLOAT64
            
            return 0 # ok
        return -2 # not cobject, fail silently
    return -2 # no __array_struct__ attr, fail silently

cdef object array_as_buffer(object input, Buffer* buffer, char mode):
    cdef object alt_input
    if array_object_as_float_buffer(input, buffer, mode) < 0:
        # try to convert the input
        alt_input = contiguous_float64_array_from_any(input)
        if array_object_as_float_buffer(alt_input, buffer, mode) < 0:
            raise TypeError("Invalid data type. 1D array or list object required.")
        return alt_input # return reference to the new object. This reference must
                         # be kept until processing is finished!
    return input

cdef object float64_array_to_list(double* data, index_t n):
    cdef index_t i
    cdef object app
    cdef object ret
    ret = []
    app = ret.append
    for i from 0 <= i < n:
        app(data[i])
    return ret


#cdef int copy_object_to_float32_array(source, float* dest) except -1:
    #cdef index_t i
    #cdef index_t n
    #try:
        #n = len(source)
        #for i from 0 <= i < n:
            #dest[i] = source[i]
    #except Exception, e:
        #raise
        #return -1
    #return 0


cdef void copy_object_to_float64_array(source, double* dest) except *:
    cdef index_t i
    cdef double x
    i = 0
    for x in source:
        dest[i] = x
        i = i + 1

cdef void copy_object_to_float32_array(source, float* dest) except *:
    cdef index_t i
    cdef float x
    i = 0
    for x in source:
        dest[i] = x
        i = i + 1
