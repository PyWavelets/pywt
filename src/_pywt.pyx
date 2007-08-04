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

from numerix import contiguous_array_from_any, memory_buffer_object


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
    name_ = name.lower()
    
    if len(name_) == 0:
        raise ValueError("Invalid wavelet name.")

    for n, code in (("db", c"d"), ("sym", c"s"), ("coif", c"c")):
        if name_[:len(n)] == n:
            try:
                number = int(name_[len(n):])
                return (code, number)
            except ValueError:
                break

    if name_[:4] == "bior":
        if len(name_) == 7 and name_[-2] == '.':
            try:
                number = int(name_[-3])*10 + int(name_[-1])
                return (c'b', number)
            except ValueError:
                pass
    elif name_[:4] == "rbio":
        if len(name_) == 7 and name_[-2] == '.':
            try:
                number = int(name_[-3])*10 + int(name_[-1])
                return (c'r', number)
            except ValueError:
                pass
    elif name_ == "haar":
        return c'h', 0

    elif name_ == "dmey":
        return c'm', 0

    raise ValueError("Unknown wavelet name, '%s' not in wavelist()." % name)


cdef public class Wavelet [type WaveletType, object WaveletObject]:
    """
    Wavelet(name, filter_bank=None) object describe properties of
    a wavelet identified by name. In order to use a built-in wavelet
    the parameter name must be a valid name from wavelist() list.
    Otherwise a filter_bank argument must be provided.
    """
    
    cdef c_wt.Wavelet* w
    
    cdef readonly name
    cdef readonly number
    
    #cdef readonly properties
 
    def __new__(self, char* name="", object filter_bank=None):

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
            filters = filter_bank.get_filters_coeffs()
            if len(filters) != 4:
                raise ValueError("Expected filter bank with 4 filters, got filter bank with %d filters." % len(filters))
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
            copy_object_to_double_array(dec_lo, self.w.dec_lo)
            copy_object_to_double_array(dec_hi, self.w.dec_hi)
            copy_object_to_double_array(rec_lo, self.w.rec_lo)
            copy_object_to_double_array(rec_hi, self.w.rec_hi)
            
            self.name = name

    def __dealloc__(self):
        if self.w != NULL:
            c_wt.free_wavelet(self.w) # if w._builtin is 0, it frees also the filter arrays
            self.w = NULL

    def __len__(self): #assume
        return self.dec_len

    property dec_lo:
        "Lowpass decomposition filter"
        def __get__(self):
            return double_array_to_list(self.w.dec_lo, self.w.dec_len)

    property dec_hi:
        "Highpass decomposition filter"
        def __get__(self):
            return double_array_to_list(self.w.dec_hi, self.w.dec_len)

    property rec_lo:
        "Lowpass reconstruction filter"
        def __get__(self):
            return double_array_to_list(self.w.rec_lo, self.w.rec_len)

    property rec_hi:
        "Highpass reconstruction filter"
        def __get__(self):
            return double_array_to_list(self.w.rec_hi, self.w.rec_len)

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

    property short_name:
        "Short wavelet family name"
        def __get__(self):
            return self.w.short_name

    property orthogonal:
        "Is orthogonal"
        def __get__(self):
            return bool(self.w.orthogonal)

    property biorthogonal:
        "Is biorthogonal"
        def __get__(self):
            return bool(self.w.biorthogonal)
    
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
            if self.w.vanishing_moments_psi > 0:
                return self.w.vanishing_moments_psi

    property vanishing_moments_phi:
        "Number of vanishing moments for scaling function"
        def __get__(self):
            if self.w.vanishing_moments_phi > 0:
                return self.w.vanishing_moments_phi

    property _builtin:
        "Returns True if the wavelet is built-in one (not created with custom filter bank)"
        def __get__(self):
            return bool(self.w._builtin)

            
    def get_filters_coeffs(self):
        """Returns tuple of wavelet filters coefficients
        (dec_lo, dec_hi, rec_lo, rec_hi)
        """
        return (self.dec_lo, self.dec_hi, self.rec_lo, self.rec_hi)

    def wavefun(self, int level=3):
        """wavefun(level)
        
        Calculates aproximations of wavelet function (psi) and associated
        scaling function (*phi*) at given level of refinement.

        For orthogonal wavelet returns scaling and wavelet function.
        For biorthogonal wavelet returns scaling and wavelet function both
        for decomposition and reconstruction.
        """
        cdef double coef "coef"
        cdef double pas "pas"
        
        coef = c_math.pow(c_math.sqrt(2.), <double>level)
        pas  = 1./(c_math.pow(2., <double>level))
        
        if self.short_name == "sym" or self.short_name == "coif":
            return upcoef('a', [coef], self, level), upcoef('d', [-coef], self, level)
            
        elif self.short_name in ("bior", "rbio"):
            if self.short_name == "bior":
                other_name = "rbio" + self.name[4:]
            elif self.short_name == "rbio":
                other_name = "bior" + self.name[4:]
            other = Wavelet(other_name)
            return upcoef('a', [1], self, level), upcoef('d', [1], self, level), upcoef('a', [1], other, level), upcoef('d', [1], other, level)
        
        else:
            return upcoef('a', [coef], self, level), upcoef('d', [coef], self, level)

    def __str__(self):
        return "Wavelet %s\n" \
        "  Family name:    %s\n" \
        "  Short name:     %s\n" \
        "  Filters length: %d\n" \
        "  Orthogonal:     %s\n" \
        "  Biorthogonal:   %s\n" \
        "  Symmetry:       %s" % \
        (self.name, self.family_name, self.short_name, self.dec_len, self.orthogonal, self.biorthogonal, self.symmetry)

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

    cdef double* input_data
    cdef double* output_data
    
    cdef index_t input_len
    cdef index_t output_len
    cdef c_wt.MODE mode_
    cdef Wavelet w
    
    cdef alternative_data
    cdef object cA
    cdef object cD

    # mode
    mode_ = c_mode_from_object(mode)
    
    # input as array
    if object_as_buffer(data, &input_data, &input_len, c'r') < 0:
        alternative_data = contiguous_array_from_any(data)
        if object_as_buffer(alternative_data, &input_data, &input_len, c'r'):
            raise TypeError("Invalid data type, 1D array or iterable object required.")
    if input_len < 1:
        raise ValueError("Invalid input length (len(data) < 1).")

    w = c_wavelet_from_object(wavelet)
    
    # output len
    output_len = c_wt.dwt_buffer_length(input_len, w.dec_len, mode_)
    if output_len < 1:
        raise RuntimeError("Invalid output length.")

    # decompose A
    cA = memory_buffer_object(output_len)
    if object_as_buffer(cA, &output_data, &output_len, c'w') < 0:
        raise RuntimeError("Getting data pointer for buffer failed.")
    if c_wt.d_dec_a(input_data, input_len, w.w, output_data, output_len, mode_) < 0:
        raise RuntimeError("C dwt failed.")
   
    # decompose D
    cD = memory_buffer_object(output_len)
    if object_as_buffer(cD, &output_data, &output_len, c'w') < 0:
        raise RuntimeError("Getting data pointer for buffer failed.")
    if c_wt.d_dec_d(input_data, input_len, w.w, output_data, output_len, mode_) < 0:
        raise RuntimeError("C dwt failed.")
 
    # return
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
    if data_len < 1:
        raise ValueError("Value of data_len value must be greater than zero.")
    if filter_len < 1:
        raise ValueError("Value of filter_len must be greater than zero.")

    mode = c_mode_from_object(mode)
   
    return c_wt.dwt_buffer_length(data_len, filter_len, <c_wt.MODE>mode)

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

    cdef double *input_data_a, *input_data_d
    cdef double* reconstruction_data
 
    cdef index_t input_len_a, input_len_d, input_len
    cdef index_t reconstruction_len

    cdef Wavelet w
    
    cdef object alternative_data_a, alternative_data_d, reconstruction

    cdef c_wt.MODE mode_

    input_data_a = input_data_d = NULL
    input_len_a = input_len_d = 0

    mode_ = c_mode_from_object(mode)

    w = c_wavelet_from_object(wavelet)

    if cA is None and cD is None:
        raise ValueError("At least one coefficient parameter must be specified.")

    # get data pointer and size
    if cA is not None:
        if object_as_buffer(cA, &input_data_a, &input_len_a, c'r') < 0:
            alternative_data_a = contiguous_array_from_any(cA)
            if object_as_buffer(alternative_data_a, &input_data_a, &input_len_a, c'r'):
                raise TypeError("Invalid cA type.")
        if input_len_a < 1:
            raise ValueError("Length of cA must be greater than zero.")

    # get data pointer and size
    if cD is not None:
        if object_as_buffer(cD, &input_data_d, &input_len_d, c'r') < 0:
            alternative_data_d = contiguous_array_from_any(cD)
            if object_as_buffer(alternative_data_d, &input_data_d, &input_len_d, c'r'):
                raise TypeError("Invalid cD type.")
        if input_len_d < 1:
            raise ValueError("Length of cD must be greater than zero.")

    # check if sizes differ
    cdef index_t diff
    if input_len_a > 0:
        if input_len_d > 0:
            diff = input_len_a - input_len_d
            if correct_size:
                if diff < 0 or diff > 1:
                    raise ValueError("Coefficients arrays lengths must satisfy (0 <= len(cA) - len(cD) <= 1).")
                input_len = input_len_a -diff
            elif diff:
                raise ValueError("Coefficients arrays must have the same size.")
            else:
                input_len = input_len_d
        else:
            input_len = input_len_a
    else:
        input_len = input_len_d

    # find buffer length
    reconstruction_len = c_wt.idwt_buffer_length(input_len, w.rec_len, mode_)
    if reconstruction_len < 1:
        raise ValueError("Invalid coefficient arrays length for specified wavelet. Wavelet and mode must be the same as used for decomposition.")

    # allocate buffer
    reconstruction = memory_buffer_object(reconstruction_len)

    # get buffer's data pointer and len
    if object_as_buffer(reconstruction, &reconstruction_data, &reconstruction_len, c'w') < 0:
        raise RuntimeError("Getting data pointer for buffer failed.")

    # call idwt func
    # one of input_data_a/input_data_d can be NULL, then only reconstruction of non-null part will be performed
    if c_wt.d_idwt(input_data_a, input_len_a, input_data_d, input_len_d, w.w, reconstruction_data, reconstruction_len, mode_, correct_size) < 0:
        raise RuntimeError("C idwt failed.")
 
    return reconstruction

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
    cdef double *input_data
    cdef double* reconstruction_data
 
    cdef index_t input_len
    cdef index_t reconstruction_len

    cdef Wavelet w
    
    cdef object data, alternative_data, reconstruction
    cdef int i, rec_a
    cdef index_t left_bound, right_bound

    input_data = NULL
    input_len = 0

    if part not in ('a', 'd'):
        raise ValueError("Argument 1 must be 'a' or 'd', not '%s'." % part)
    rec_a = 0
    if part == 'a':
        rec_a = 1

    w = c_wavelet_from_object(wavelet)

    if level < 1:
        raise ValueError("Value of level must be greater than 0.")

    # input as array
    if object_as_buffer(coeffs, &input_data, &input_len, c'r') < 0:
        alternative_data = contiguous_array_from_any(coeffs)
        if object_as_buffer(alternative_data, &input_data, &input_len, c'r'):
            raise TypeError("Invalid data type, 1D array or iterable required.")
    if input_len < 1:
        raise ValueError("Invalid input length (len(data) < 1).")

    for i from 0 <= i < level:
        # output len
        reconstruction_len = c_wt.reconstruction_buffer_length(input_len, w.dec_len)
        if reconstruction_len < 1:
            raise RuntimeError("Invalid output length.")

        # reconstruct
        reconstruction = memory_buffer_object(reconstruction_len)
        if object_as_buffer(reconstruction, &reconstruction_data, &reconstruction_len, c'w') < 0:
            raise RuntimeError("Getting data pointer for buffer failed.")

        if rec_a:
            if c_wt.d_rec_a(input_data, input_len, w.w, reconstruction_data, reconstruction_len) < 0:
                raise RuntimeError("C rec_a failed.")
        else:
            if c_wt.d_rec_d(input_data, input_len, w.w, reconstruction_data, reconstruction_len) < 0:
                raise RuntimeError("C rec_d failed.")
        rec_a = 1

        data = reconstruction # keep reference
        input_len = reconstruction_len
        input_data = reconstruction_data

    if take > 0:
        if take < reconstruction_len:
            left_bound = right_bound = (reconstruction_len-take)/2
            if (reconstruction_len-take)%2:
                left_bound = left_bound + 1

            return reconstruction[left_bound:-right_bound]

    return reconstruction

###############################################################################
# swt

def swt_max_level(input_len):
    """
    swt_max_level(int input_len)

    Returns maximum level of Stationary Wavelet Transform for data of given length.
    """
    return c_wt.swt_max_level(input_len)

def swt(object data, object wavelet, int level):
    """
    swt(object data, object wavelet, int level)
    
    Performs multilevel Stationary Wavelet Transform.

    data    - input signal
    wavelet - wavelet to use (Wavelet object or name)
    level   - transform level

    Returns list of approximation and details coefficients pairs in form
        [(cA1, cD1), (cA2, cD2), ..., (cAn, cDn)], where n = level
    """
    cdef double* input_data
    cdef double* output_data
    
    cdef index_t input_len
    cdef index_t output_len
    cdef Wavelet w
    
    cdef alternative_data
    cdef object cA
    cdef object cD

    cdef int i
    
    # input
    if object_as_buffer(data, &input_data, &input_len, c'r') < 0:
        alternative_data = contiguous_array_from_any(data)
        if object_as_buffer(alternative_data, &input_data, &input_len, c'r'):
            raise TypeError("Invalid data type, 1D array or iterable object required.")
    if input_len < 1:
        raise ValueError("Invalid input data length.")
    elif input_len % 2:
        raise ValueError("Length of data must be even.")

    # wavelet
    w = c_wavelet_from_object(wavelet)
    
    # level
    if level < 1:
        raise ValueError("Level must be strictly positive number.")
    elif level > c_wt.swt_max_level(input_len):
        raise ValueError("Level value too high (max level for current input len is %d)." % c_wt.swt_max_level(input_len))

    # output length
    output_len = c_wt.swt_buffer_length(input_len)
    if output_len < 1:
        raise RuntimeError("Invalid output length.")
    
    ret = []
    for i from 1 <= i <= level:
        # alloc memory
        cD = memory_buffer_object(output_len)
        cA = memory_buffer_object(output_len)
        
        # decompose D
        if object_as_buffer(cD, &output_data, &output_len, c'w') < 0:
            raise RuntimeError("Getting data pointer for buffer failed.")
        if c_wt.d_swt_d(input_data, input_len, w.w, output_data, output_len, i) < 0:
            raise RuntimeError("C swt failed.")

        # decompose A
        if object_as_buffer(cA, &output_data, &output_len, c'w') < 0:
            raise RuntimeError("Getting data pointer for buffer failed.")
        if c_wt.d_swt_a(input_data, input_len, w.w, output_data, output_len, i) < 0:
            raise RuntimeError("C swt failed.")
        input_data = output_data # a -> input
        input_len = output_len

        ret.append((cA, cD))
    return ret

###############################################################################

__all__ = ['MODES', 'Wavelet', 'dwt', 'dwt_coeff_len', 'dwt_max_level',
           'idwt', 'swt', 'swt_max_level', 'upcoef', ]
