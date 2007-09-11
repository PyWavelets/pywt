# Copyright (c) 2006-2007 Filip Wasilewski <filip.wasilewski@gmail.com>
# See COPYING for license details.

__id__ = "$Id$"
__doc__ = """Pyrex wrapper for low-level C wavelet transform implementation."""

###############################################################################
# imports

cimport c_python
cimport c_wt
cimport c_array_interface
cimport c_math

ctypedef Py_ssize_t index_t

cdef extern from "common.h":
    ctypedef float FILTER_TYPE

from wnames import wavelist

###############################################################################
# array handling stuff here
cdef contiguous_float64_array_from_any, float32_memory_buffer_object, float64_memory_buffer_object

from numerix import contiguous_float64_array_from_any
from numerix import float32_memory_buffer_object
from numerix import float64_memory_buffer_object
from numerix import concatenate, zeros, linspace, keep

include "arraytools.pxi"

###############################################################################
# MODES

cdef c_wt.MODE c_mode_from_object(mode) except c_wt.MODE_INVALID:
    cdef c_wt.MODE m
    cdef c_python.PyObject* co
    cdef object o
    if c_python.PyInt_Check(mode):
        m = mode
        if m <= c_wt.MODE_INVALID or m >= c_wt.MODE_MAX:
            raise ValueError("Invalid mode.")
            return c_wt.MODE_INVALID
    else:
        co = c_python.PyObject_GetAttrString(MODES, mode)
        if co != NULL:
            o = <object>co
            c_python.Py_DECREF(o) # decref above extra ref inc
            m = <object>co
        else:
            c_python.PyErr_Clear()
            raise ValueError("Unknown mode name.")
            return c_wt.MODE_INVALID
    return m

def __from_object(mode):
    return c_mode_from_object(mode)
    
class MODES(object):
    """
    Different ways of dealing with border distortion problem while performing
    Discrete Wavelet Transform analysis.
    
    To reduce this effect the signal or image can be extended by adding extra samples.
    
    zpd - zero-padpadding                0  0 | x1 x2 ... xn | 0  0
    cpd - constant-padding              x1 x1 | x1 x2 ... xn | xn xn
    sym - symmetric-padding             x2 x1 | x1 x2 ... xn | xn xn-1
    ppd - periodic-padding            xn-1 xn | x1 x2 ... xn | x1 x2
    sp1 - smooth-padding               (1st derivative interpolation)
    
    DWT performed for these extension modes is slightly redundant, but ensure
    a perfect reconstruction for IDWT.

    per - periodization - like periodic-padding but gives the smallest number
          of decomposition coefficients. IDWT must be performed with the same mode.
          
    """
    
    zpd = c_wt.MODE_ZEROPAD
    cpd = c_wt.MODE_CONSTANT_EDGE
    sym = c_wt.MODE_SYMMETRIC
    ppd = c_wt.MODE_PERIODIC
    sp1 = c_wt.MODE_SMOOTH
    per = c_wt.MODE_PERIODIZATION
    
    _asym = c_wt.MODE_ASYMMETRIC
    
    modes = ["zpd", "cpd", "sym", "ppd", "sp1", "per"]

    from_object = staticmethod(__from_object)

###############################################################################
# Wavelet

cdef object wname_to_code(char* name):
    cdef object name_ "name_"
    cdef int length "length"
    cdef int i "i"
    cdef number "number"
    
    name_ = name.lower()
    length = len(name_)
    
    if length == 0:
        raise ValueError("Invalid wavelet name.")

    for n, code in (("db", c"d"), ("sym", c"s"), ("coif", c"c")):
        i = len(n)
        if name_[:i] == n:
            try:
                number = int(name_[i:])
                return (code, number)
            except ValueError:
                break

    if name_[:4] == "bior":
        if length == 7 and name_[-2] == '.':
            try:
                number = int(name_[-3])*10 + int(name_[-1])
                return (c'b', number)
            except ValueError:
                pass
    elif name_[:4] == "rbio":
        if length == 7 and name_[-2] == '.':
            try:
                number = int(name_[-3])*10 + int(name_[-1])
                return (c'r', number)
            except ValueError:
                pass
    elif name_ == "haar":
        return c'h', 0

    elif name_ == "dmey":
        return c'm', 0

    if name_ in wavelist():
        raise RuntimeError("Wavelet '%s' does not exist but is listed on wavelist() builtin wavelets list." % name)
    else:
        raise ValueError("Unknown wavelet name '%s', check wavelist() for the list of available builtin wavelets." % name)


cdef public class Wavelet [type WaveletType, object WaveletObject]:
    """
    Wavelet(name, filter_bank=None) object describe properties of
    a wavelet identified by name.
    
    In order to use a built-in wavelet the parameter name must be
    a valid name from wavelist() list.
    To create a custom wavelet object, filter_bank parameter must
    be specified. It can be either a list of four filters or
    an object defining the `get_filters_coeffs` mehod that return
    a list of four filters - just like the Wavelet instances.
    """
    
    cdef c_wt.Wavelet* w
    
    cdef readonly name
    cdef readonly number
    
    #cdef readonly properties
 
    def __new__(self, char* name="", object filter_bank=None):
        cdef filters, c, nr, max_length
        cdef dec_lo, dec_hi, rec_lo, rec_hi
        
        if not name and filter_bank is None:
            raise TypeError("Wavelet name or filter bank must be specified.")
        #print wname_to_code(name, number)

        if filter_bank is None:
            # builtin wavelet
            c, nr = wname_to_code(name)
            self.w = <c_wt.Wavelet*> c_wt.wavelet(c, nr)

            if self.w == NULL:
                raise ValueError("Invalid wavelet name.")

            self.name = name.lower()
            self.number = nr

        else:
            if hasattr(filter_bank, "get_filters_coeffs"):
                filters = filter_bank.get_filters_coeffs()
                if len(filters) != 4:
                    raise ValueError("Expected filter bank with 4 filters, got filter bank with %d filters." % len(filters))
            else:
                filters = filter_bank
                if len(filters) != 4:
                    raise ValueError("Expected list of 4 filters coefficients, got %d filters." % len(filters))
                
            try:
                dec_lo = map(float, filters[0])
                dec_hi = map(float, filters[1])
                rec_lo = map(float, filters[2])
                rec_hi = map(float, filters[3])
            except TypeError:
                raise TypeError("Filter bank with float or int values required.")

            max_length = max(len(dec_lo), len(dec_hi), len(rec_lo), len(rec_hi))
            if max_length == 0:
                raise ValueError("Filter bank can not be zero-length.")

            self.w = <c_wt.Wavelet*> c_wt.blank_wavelet(max_length)
            if self.w == NULL:
                raise MemoryError("Could not allocate memory for given filter bank.")

            # copy values to struct
            copy_object_to_float_array(dec_lo, self.w.dec_lo)
            copy_object_to_float_array(dec_hi, self.w.dec_hi)
            copy_object_to_float_array(rec_lo, self.w.rec_lo)
            copy_object_to_float_array(rec_hi, self.w.rec_hi)
            
            self.name = name

    def __dealloc__(self):
        if self.w != NULL:
            c_wt.free_wavelet(self.w) # if w._builtin is 0, it frees also the filter arrays
            self.w = NULL

    def __len__(self): #assume
        return self.w.dec_len

    property dec_lo:
        "Lowpass decomposition filter"
        def __get__(self):
            return float_array_to_list(self.w.dec_lo, self.w.dec_len)

    property dec_hi:
        "Highpass decomposition filter"
        def __get__(self):
            return float_array_to_list(self.w.dec_hi, self.w.dec_len)

    property rec_lo:
        "Lowpass reconstruction filter"
        def __get__(self):
            return float_array_to_list(self.w.rec_lo, self.w.rec_len)

    property rec_hi:
        "Highpass reconstruction filter"
        def __get__(self):
            return float_array_to_list(self.w.rec_hi, self.w.rec_len)

    property rec_len:
        "Reconstruction filters length"
        def __get__(self):
            return self.w.rec_len

    property dec_len:
        "Decomposition filters length"
        def __get__(self):
            return self.w.dec_len

    property family_name:
        "Wavelet family name"
        def __get__(self):
            return self.w.family_name

    property short_family_name:
        "Short wavelet family name"
        def __get__(self):
            return self.w.short_name

    property orthogonal:
        "Is orthogonal"
        def __get__(self):
            return bool(self.w.orthogonal)
        def __set__(self, int value):
            self.w.orthogonal = (value != 0)

    property biorthogonal:
        "Is biorthogonal"
        def __get__(self):
            return bool(self.w.biorthogonal)
        def __set__(self, int value):
            self.w.biorthogonal = (value != 0)
    
    property symmetry:
        "Wavelet symmetry"
        def __get__(self):
            if self.w.symmetry == c_wt.ASYMMETRIC:
                return "asymmetric"
            elif self.w.symmetry == c_wt.NEAR_SYMMETRIC:
                return "near symmetric"
            elif self.w.symmetry == c_wt.SYMMETRIC:
                return "symmetric"
            else:
                return "unknown"

    property vanishing_moments_psi:
        "Number of vanishing moments for wavelet function"
        def __get__(self):
            if self.w.vanishing_moments_psi >= 0:
                return self.w.vanishing_moments_psi

    property vanishing_moments_phi:
        "Number of vanishing moments for scaling function"
        def __get__(self):
            if self.w.vanishing_moments_phi >= 0:
                return self.w.vanishing_moments_phi

    property _builtin:
        "Returns True if the wavelet is built-in one (not created with custom filter bank)"
        def __get__(self):
            return bool(self.w._builtin)

    property filters_coeffs:
        def __get__(self):
            return self.get_filters_coeffs()
            
    def get_filters_coeffs(self):
        """Returns tuple of wavelet filters coefficients
        (dec_lo, dec_hi, rec_lo, rec_hi)
        """
        return (self.dec_lo, self.dec_hi, self.rec_lo, self.rec_hi)

    property reverse_filters_coeffs:
        def __get__(self):
            return self.get_reverse_filters_coeffs()

    def get_reverse_filters_coeffs(self):
        """Tuple of reverse wavelet filters coefficients
        (rec_lo[::-1], rec_hi[::-1], dec_lo[::-1], dec_hi[::-1])
        """
        return (self.rec_lo[::-1], self.rec_hi[::-1], self.dec_lo[::-1], self.dec_hi[::-1])

    def wavefun(self, int level=8):
        """wavefun(int level=8)
        
        Calculates aproximations of scaling function (*phi*) and wavelet
        function (*psi*) on xgrid (*x*) at a given level of refinement.

        For orthogonal wavelets returns scaling function, wavelet function
        and xgrid - [phi, psi, x].
        
        For biorthogonal wavelets returns scaling and wavelet function both
        for decomposition and reconstruction and xgrid
        - [phi_d, psi_d, phi_r, psi_r, x].
        """

        cdef index_t filter_length "filter_length"
        cdef index_t right_extent_length "right_extent_length"
        cdef index_t output_length "output_length"
        cdef index_t keep_length "keep_length"
        cdef double n "n"
        cdef double p "p"
        cdef double mul "mul"
        cdef Wavelet other "other"
        cdef phi_d, psi_d, phi_r, psi_r
        
        n = c_math.pow(c_math.sqrt(2.), <double>level)
        p = (c_math.pow(2., <double>level))
        
        if self.w.orthogonal:
            filter_length = self.w.dec_len
            output_length = <index_t> ((filter_length-1) * p + 1)
            keep_length = get_keep_length(output_length,level,filter_length)
            output_length = fix_output_length(output_length,keep_length)
                
            right_extent_length = get_right_extent_length(output_length, keep_length)
            
            return [
                    concatenate(([0.], keep(upcoef('a', [n], self, level), keep_length), zeros(right_extent_length))), # phi
                    concatenate(([0.], keep(upcoef('d', [n], self, level), keep_length), zeros(right_extent_length))), # psi
                    linspace(0.0,(output_length-1)/p,output_length)                                                    # x
                ]
        else:
            mul = 1
            if self.w.biorthogonal:
                if (self.w.vanishing_moments_psi % 4) != 1:
                    mul = -1

            other = Wavelet(filter_bank=self.reverse_filters_coeffs)
            
            filter_length  = other.w.dec_len
            output_length = <index_t> ((filter_length-1) * p)
            keep_length = get_keep_length(output_length,level,filter_length)
            output_length = fix_output_length(output_length,keep_length)
            right_extent_length = get_right_extent_length(output_length, keep_length)

            phi_d  = concatenate(([0.], keep(upcoef('a', [n], other, level), keep_length), zeros(right_extent_length)))
            psi_d  = concatenate(([0.], keep(upcoef('d', [mul*n], other, level), keep_length), zeros(right_extent_length)))

            filter_length = self.w.dec_len
            output_length = <index_t> ((filter_length-1) * p)
            keep_length = get_keep_length(output_length,level,filter_length)
            output_length = fix_output_length(output_length,keep_length)
            right_extent_length = get_right_extent_length(output_length, keep_length)
            
            phi_r  = concatenate(([0.], keep(upcoef('a', [n], self, level), keep_length), zeros(right_extent_length)))
            psi_r  = concatenate(([0.], keep(upcoef('d', [mul*n], self, level), keep_length), zeros(right_extent_length)))

            return  [phi_d, psi_d, phi_r, psi_r, linspace(0.0,(output_length-1)/p, output_length)]

    def __str__(self):
        return "Wavelet %s\n" \
        "  Family name:    %s\n" \
        "  Short name:     %s\n" \
        "  Filters length: %d\n" \
        "  Orthogonal:     %s\n" \
        "  Biorthogonal:   %s\n" \
        "  Symmetry:       %s" % \
        (self.name, self.family_name, self.short_family_name, self.dec_len, self.orthogonal, self.biorthogonal, self.symmetry)

cdef index_t get_keep_length(index_t output_length, int level, index_t filter_length):
    cdef index_t lplus "lplus"
    cdef index_t keep_length "keep_length"
    cdef int i "i"
    lplus = filter_length - 2
    keep_length = 1
    for i from 0 <= i < level:
        keep_length = 2*keep_length+lplus
    return keep_length

cdef index_t fix_output_length(index_t output_length, index_t keep_length):
    if output_length-keep_length-2 < 0:
        output_length = keep_length+2
    return output_length

cdef index_t get_right_extent_length(index_t output_length, index_t keep_length):
     return output_length - keep_length - 1

def wavelet_from_object(wavelet):
    return c_wavelet_from_object(wavelet)

cdef c_wavelet_from_object(wavelet):
    if c_python.PyObject_IsInstance(wavelet, Wavelet):
        return wavelet
    else:
        return Wavelet(wavelet)

###############################################################################
# DWT

def dwt_max_level(data_len, filter_len):
    """
    dwt_max_level(int data_len, int filter_len) -> int
    
    Compute the maximum usefull level of decomposition
    for given input data length and wavelet filter length.
    """
    if c_python.PyObject_IsInstance(filter_len, Wavelet):
        return c_wt.dwt_max_level(data_len, filter_len.dec_len)
    else:
        return c_wt.dwt_max_level(data_len, filter_len)

def dwt(object data, object wavelet, object mode='sym'):
    """
    (cA, cD) = dwt(data, wavelet, mode='sym')

    Single level Discrete Wavelet Transform

    data    - input signal
    wavelet - wavelet to use (Wavelet object or name)
    mode    - signal extension mode, see MODES

    Returns approximation (cA) and detail (cD) coefficients.

    Length of coefficient arrays depends on the selected mode:

        for all modes except periodization:
            len(cA) == len(cD) == floor((len(data) + wavelet.dec_len - 1) / 2)

        for periodization mode ("per"):
            len(cA) == len(cD) == ceil(len(data) / 2)
    """

    cdef Buffer input, output_a, output_d
    cdef object cA, cD
        
    cdef Wavelet w
    cdef c_wt.MODE mode_
    
    w = c_wavelet_from_object(wavelet)
    mode_ = c_mode_from_object(mode)
    
    # input as C array
    data = array_as_buffer(data, &input, c'r')
    #assert input.len > 0
    
    output_len = c_wt.dwt_buffer_length(input.len, w.dec_len, mode_)
    if output_len < 1:
        raise RuntimeError("Invalid output length.")

    cA = memory_buffer_object(output_len, input.dtype)
    cD = memory_buffer_object(output_len, input.dtype)
    
    cA = array_as_buffer(cA, &output_a, c'w')
    cD = array_as_buffer(cD, &output_d, c'w')
    
    assert input.dtype == output_a.dtype == output_d.dtype
    
    if input.dtype == FLOAT64:
        if c_wt.double_dec_a(<double*>input.data, input.len, w.w, <double*>output_a.data, output_a.len, mode_) < 0 or \
           c_wt.double_dec_d(<double*>input.data, input.len, w.w, <double*>output_d.data, output_d.len, mode_) < 0:
            raise RuntimeError("C dwt failed.")
    else:
        if c_wt.float_dec_a(<float*>input.data, input.len, w.w, <float*>output_a.data, output_a.len, mode_) < 0 or \
           c_wt.float_dec_d(<float*>input.data, input.len, w.w, <float*>output_d.data, output_d.len, mode_) < 0:
            raise RuntimeError("C dwt failed.")

    return (cA, cD)

def dwt_coeff_len(data_len, filter_len, mode):
    """
    dwt_coeff_len(int data_len, int filter_len, mode) -> int

    Returns length of dwt output for given data length, filter length and mode:

        * for all modes except periodization:
            len(cA) == len(cD) == floor((len(data) + wavelet.dec_len - 1) / 2)

        * for periodization mode ("per"):
            len(cA) == len(cD) == ceil(len(data) / 2)
    """
    cdef index_t filter_len_
    if c_python.PyObject_IsInstance(filter_len, Wavelet):
        filter_len_ = filter_len.dec_len
    else:
        filter_len_ = filter_len

    if data_len < 1:
        raise ValueError("Value of data_len value must be greater than zero.")
    if filter_len_ < 1:
        raise ValueError("Value of filter_len must be greater than zero.")

    return c_wt.dwt_buffer_length(data_len, filter_len_, c_mode_from_object(mode))
    

###############################################################################
# idwt

def idwt(object cA, object cD, object wavelet, object mode = 'sym', int correct_size = 0):
    """
    A = idwt(cA, cD, wavelet, mode='sym', correct_size=0)

    Single level Inverse Discrete Wavelet Transform

    cA      - approximation coefficients
    cD      - detail coefficients
    wavelet - wavelet to use (Wavelet object or name)
    mode    - signal extension mode, see MODES

    correct_size - under normal conditions (all data lengths dyadic) Ca and cD
                   coefficients lists must have the same lengths. With correct_size
                   set to True, length of cA may be greater by one than length of cA.
                   Useful when doing multilevel decomposition and reconstruction of
                   non-dyadic length signals.
    
    Returns single level reconstruction of signal from given coefficients.
    """

    cdef Buffer input_a, input_d, output
    cdef index_t input_len

    cdef Wavelet w
    cdef c_wt.MODE mode_

    w = c_wavelet_from_object(wavelet)
    mode_ = c_mode_from_object(mode)

    cdef object rec
    cdef index_t rec_len
    cdef index_t size_diff
    
    if cA is None and cD is None:
        raise ValueError("At least one coefficient parameter must be specified.")
        
    # get data pointer and size
    if cA is not None:
        cA = array_as_buffer(cA, &input_a, c'r')
        assert input_a.len > 0, "Length of cA must be greater than zero."
    else:
        input_a.data = NULL
        input_a.len = 0
        input_a.dtype = <DTYPE>0

    if cD is not None:
        cD = array_as_buffer(cD, &input_d, c'r')
        assert input_d.len > 0, "Length of cA must be greater than zero."
    else:
        input_d.data = NULL
        input_d.len = 0
        input_d.dtype = <DTYPE>0
        
    if input_a.data != NULL and input_d.data != NULL:
        if input_a.dtype != input_d.dtype:
            # need to upcast to common type
            if input_a.dtype == FLOAT32:
                cA = array_as_buffer(contiguous_float64_array_from_any(cA), &input_a, c'r')
            else:
                cD = array_as_buffer(contiguous_float64_array_from_any(cD), &input_d, c'r')

    # check for sizes difference
    if input_a.data != NULL:
        if input_d.data != NULL:
            size_diff = input_a.len - input_d.len
            if size_diff:
                if correct_size:
                    if size_diff < 0 or size_diff > 1:
                        raise ValueError("Coefficients arrays must satisfy (0 <= len(cA) - len(cD) <= 1).")
                    input_len = input_a.len - size_diff
                else:
                    raise ValueError("Coefficients arrays must have the same size.")
            else:
                input_len = input_d.len
        else:
            input_len = input_a.len
    else:
        input_len = input_d.len

    # find reconstruction buffer length
    rec_len = c_wt.idwt_buffer_length(input_len, w.rec_len, mode_)
    if rec_len < 1:
        raise ValueError("Invalid coefficient arrays length for specified wavelet. Wavelet and mode must be the same as used for decomposition.")

    # allocate buffer
    rec = memory_buffer_object(rec_len, <DTYPE>(input_a.dtype | input_d.dtype))
    rec = array_as_buffer(rec, &output, c'w')

    assert output.dtype == FLOAT64 or output.dtype == FLOAT32

    # call idwt func
    # one of input_data_a/input_data_d can be NULL, then only reconstruction of non-null part will be performed
    if output.dtype == FLOAT64:
        if c_wt.double_idwt(<double*>input_a.data, input_a.len, <double*>input_d.data, input_d.len, w.w, <double*>output.data, output.len, mode_, correct_size) < 0:
            raise RuntimeError("C idwt failed.")
    else:
        if c_wt.float_idwt(<float*>input_a.data, input_a.len, <float*>input_d.data, input_d.len, w.w, <float*>output.data, output.len, mode_, correct_size) < 0:
            raise RuntimeError("C idwt failed.")
    return rec

###############################################################################
# upcoef

def upcoef(part, coeffs, wavelet, int level=1, take=0):
    """upcoef(part, coeffs, wavelet, level=1, take=0)
    
    Direct reconstruction from cefficients.

    part    - coefficients type:
      'a' - approximations reconstruction is performed
      'd' - details reconstruction is performed
    coeffs  - coefficients array
    wavelet - wavelet to use (Wavelet object or name)
    level   - multilevel reconstruction level
    take    - take central part of length equal to 'take' from the result
    """
    cdef Buffer input
    cdef Buffer output
 
    cdef Wavelet w
    
    cdef object data, rec
    cdef int i, rec_a
    cdef index_t left_bound, right_bound

    if part not in ('a', 'd'):
        raise ValueError("Argument 1 must be 'a' or 'd', not '%s'." % part)
    rec_a = (part == 'a')

    w = c_wavelet_from_object(wavelet)

    if level < 1:
        raise ValueError("Value of level must be greater than 0.")

    # input as array
    coeffs = array_as_buffer(coeffs, &input, c'r')
    assert input.len > 0, "Invalid input length (len(coeffs) < 1)."

    for i from 0 <= i < level:
        # output len
        rec_len = c_wt.reconstruction_buffer_length(input.len, w.dec_len)
        if rec_len < 1:
            raise RuntimeError("Invalid output length.")

        # reconstruct
        rec = memory_buffer_object(rec_len, input.dtype)
        rec = array_as_buffer(rec, &output, c'w')
        
        assert input.dtype == output.dtype

        if rec_a:
            if input.dtype == FLOAT64:
                if c_wt.double_rec_a(<double*>input.data, input.len, w.w, <double*>output.data, output.len) < 0:
                    raise RuntimeError("C rec_a failed.")
            else:
                if c_wt.float_rec_a(<float*>input.data, input.len, w.w, <float*>output.data, output.len) < 0:
                    raise RuntimeError("C rec_a failed.")
        else:
            if input.dtype == FLOAT64:
                if c_wt.double_rec_d(<double*>input.data, input.len, w.w, <double*>output.data, output.len) < 0:
                    raise RuntimeError("C rec_a failed.")
            else:
                if c_wt.float_rec_d(<float*>input.data, input.len, w.w, <float*>output.data, output.len) < 0:
                    raise RuntimeError("C rec_a failed.")
            rec_a = 1

        data = rec # keep reference
        input.len = output.len
        input.data = output.data

    if take > 0:
        if take < rec_len:
            left_bound = right_bound = (rec_len-take)/2
            if (rec_len-take)%2:
                left_bound = left_bound + 1

            return rec[left_bound:-right_bound]
    return rec

###############################################################################
# swt

def swt_max_level(input_len):
    """
    swt_max_level(int input_len)

    Returns maximum level of Stationary Wavelet Transform for data of given length.
    """
    return c_wt.swt_max_level(input_len)

def swt(object data, object wavelet, object level=None, int start_level=0):
    """
    swt(object data, object wavelet, int level)
    
    Performs multilevel Stationary Wavelet Transform.

    data    - input signal
    wavelet - wavelet to use (Wavelet object or name)
    level   - transform level

    Returns list of approximation and details coefficients pairs in form
        [(cAn, cDn), ..., (cA2, cD2), (cA1, cD1)], where n = level
    """
    cdef Buffer input, output
    cdef object cA, cD

    cdef Wavelet w
    
    cdef int i, end_level, level_
    
    # input
    data = array_as_buffer(data, &input, c'r')
    if input.len < 1:
        raise ValueError("Invalid input data length.")
    if input.len % 2:
        raise ValueError("Length of data must be even.")

    # wavelet
    w = c_wavelet_from_object(wavelet)
    
    # level
    if level is None:
        level_ = c_wt.swt_max_level(input.len)
    else:
        level_ = level

    end_level = start_level + level_
        
    if level_ < 1:
        raise ValueError("Level value must be greater than zero.")
    if start_level < 0:
        raise ValueError("start_level must be greater than zero.")
    if start_level >= c_wt.swt_max_level(input.len):
        raise ValueError("start_level must be less than %d." % c_wt.swt_max_level(input.len))
    
    if end_level > c_wt.swt_max_level(input.len):
        raise ValueError("Level value too high (max level for current input len and start_level is %d)." % (c_wt.swt_max_level(input.len)-start_level))

    # output length
    output_len = c_wt.swt_buffer_length(input.len)
    if output_len < 1:
        raise RuntimeError("Invalid output length.")
    
    ret = []
    for i from start_level < i <= end_level:
        # alloc memory, decompose D
        cD = memory_buffer_object(output_len, input.dtype)
        cD = array_as_buffer(cD, &output, c'w')
        
        if input.dtype == FLOAT64:
            if c_wt.double_swt_d(<double*>input.data, input.len, w.w, <double*>output.data, output.len, i) < 0:
                raise RuntimeError("C swt failed.")
        else:
            if c_wt.float_swt_d(<float*>input.data, input.len, w.w, <float*>output.data, output.len, i) < 0:
                raise RuntimeError("C swt failed.")
        
        # alloc memory, decompose A
        cA = memory_buffer_object(output_len, input.dtype)
        cA = array_as_buffer(cA, &output, c'w')

        if input.dtype == FLOAT64:
            if c_wt.double_swt_a(<double*>input.data, input.len, w.w, <double*>output.data, output.len, i) < 0:
                raise RuntimeError("C swt failed.")
        else:
            if c_wt.float_swt_a(<float*>input.data, input.len, w.w, <float*>output.data, output.len, i) < 0:
                raise RuntimeError("C swt failed.")

        input.data = output.data # a -> input
        input.len = output.len

        ret.append((cA, cD))
    ret.reverse()
    return ret

###############################################################################

__all__ = ['MODES', 'Wavelet', 'dwt', 'dwt_coeff_len', 'dwt_max_level',
           'idwt', 'swt', 'swt_max_level', 'upcoef', ]
