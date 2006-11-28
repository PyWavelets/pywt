cdef object double_array_to_list(double* data, index_t n):
    cdef index_t i
    cdef object app
    ret = []
    app = ret.append
    for i from 0 <= i < n:
        app(data[i])
    return ret

cdef int copy_object_to_double_array(source, double* dest) except -1:
    cdef index_t i
    cdef index_t n
    try:
        n = len(source)
        for i from 0 <= i < n:
            dest[i] = source[i]
    except Exception, e:
        raise
        return -1
    return 0

###############################################################################
# buffer objects handling

cdef int array_interface_as_double_array_ptr(object source, unsigned int min_dims, double** buffer_addr, index_t* buffer_len, char rwmode):
    # Get object buffer for reading (rwmode = 'r') or writing (rwmode = 'w')
    #
    # source      - source object exposing array interfce
    # buffer_addr - will be set on success
    # buffer_len    - buffer length
    # rwmode        - read/write mode
    # 
    # returns     -  0 - ok
    #             - -1 - no __array_struct__ attr
    #             - -2, -3, -4 - other errors 
    
    # TODO: extract and create object wrapper?
    # TODO: raise exceptions instead of return negative values?

    cdef double* data
    cdef index_t dim1_len, dim2_len
    cdef c_array_interface.PyGenericArrayInterface* array_struct
    cdef object cobject

    if hasattr(source, '__array_struct__'):
        cobject = source.__array_struct__
        if c_python.PyCObject_Check(cobject):
            array_struct = <c_array_interface.PyGenericArrayInterface*> c_python.PyCObject_AsVoidPtr(cobject)

            if min_dims == 1:
                if not (c_array_interface.PyArrayInterface_CHECK_1D(array_struct)):
                    #print "not 1D"
                    return -3
                dim1_len = c_array_interface.PyArrayInterface_SHAPE(array_struct, 0)
                if dim1_len < 1:
                    #print "data len < 1"
                    return -5
                buffer_len[0] = dim1_len
            elif min_dims == 2:
                if not (c_array_interface.PyArrayInterface_CHECK_2D(array_struct)):
                    #print "not 2D"
                    return -3
                dim1_len = c_array_interface.PyArrayInterface_SHAPE(array_struct, 0)
                dim2_len = c_array_interface.PyArrayInterface_SHAPE(array_struct, 1)
                if dim1_len < 1 or dim2_len < 1:
                    #print "dim1_len or dim2_len < 1"
                    return -5
                buffer_len[0] = dim1_len
                buffer_len[1] = dim2_len
            else:
                #print "invalid min dim"
                return -4

            #print "C_RO", c_array_interface.PyArrayInterface_IS_C_ARRAY_RO(array_struct)

            if rwmode == c'w':
                data = c_array_interface.PyArrayInterface_DATA_AS_DOUBLE_C_ARRAY(array_struct)
            elif rwmode == c'r':
                data = c_array_interface.PyArrayInterface_DATA_AS_DOUBLE_C_ARRAY_RO(array_struct)
            else:
                #print "invalid rwmode"
                return -6

            if data != NULL:
                buffer_addr[0] = data
                return 0
            else:
                #print "not C double array" # type is not double, array is not c-contiguous or data is NULL
                #print <int> array_struct.data
                #print array_struct.nd
                #print array_struct.typekind
                #print array_struct.itemsize
                #print array_struct.flags
                return -7

        #print "not cobject"
        return -2
    #print "no __array_struct__ attr"
    return -1

cdef int object_as_buffer(object source, double** buffer_addr, index_t* buffer_len, char mode):
    return array_interface_as_double_array_ptr(source, 1, buffer_addr, buffer_len, mode)

