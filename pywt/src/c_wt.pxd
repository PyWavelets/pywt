# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

cdef extern from "common.h":

    ctypedef int index_t

    cdef void* wtmalloc(long size)
    cdef void* wtcalloc(long len, long size)
    cdef void wtfree(void* ptr)

    ctypedef enum MODE:
        MODE_INVALID = -1
        MODE_ZEROPAD = 0
        MODE_SYMMETRIC
        MODE_CONSTANT_EDGE
        MODE_SMOOTH
        MODE_PERIODIC
        MODE_PERIODIZATION
        MODE_MAX


    # buffers lengths
    cdef size_t dwt_buffer_length(size_t input_len, size_t filter_len, MODE mode)
    cdef size_t upsampling_buffer_length(size_t coeffs_len, size_t filter_len,
                                         MODE mode)
    cdef size_t reconstruction_buffer_length(size_t coeffs_len, size_t filter_len)
    cdef size_t idwt_buffer_length(size_t coeffs_len, size_t filter_len, MODE mode)
    cdef size_t swt_buffer_length(size_t coeffs_len)

    # max dec levels
    cdef unsigned char dwt_max_level(size_t input_len, size_t filter_len)
    cdef unsigned char swt_max_level(size_t input_len)


cdef extern from "wavelets.h":

    ctypedef enum SYMMETRY:
        ASYMMETRIC
        NEAR_SYMMETRIC
        SYMMETRIC

    ctypedef struct Wavelet:

        double* dec_hi_double      # highpass decomposition
        double* dec_lo_double      # lowpass   decomposition
        double* rec_hi_double      # highpass reconstruction
        double* rec_lo_double      # lowpass   reconstruction

        float* dec_hi_float
        float* dec_lo_float
        float* rec_hi_float
        float* rec_lo_float


        size_t dec_len         # length of decomposition filter
        size_t rec_len         # length of reconstruction filter

        # FIXME: Are these used?
        index_t dec_hi_offset
        index_t dec_lo_offset
        index_t rec_hi_offset
        index_t rec_lo_offset

        int vanishing_moments_psi
        int vanishing_moments_phi
        index_t support_width

        int orthogonal
        int biorthogonal

        int symmetry

        int compact_support

        int _builtin

        char* family_name
        char* short_name


    cdef Wavelet* wavelet(char name, int type)
    cdef Wavelet* blank_wavelet(size_t filter_length)
    cdef void free_wavelet(Wavelet* wavelet)


cdef extern from "wt.h":

    # Cython does not know the 'restrict' keyword
    cdef int double_dec_a(const double  * const input, const size_t input_len,
                          const Wavelet * const wavelet,
                          double  * const output, const size_t output_len,
                          const MODE mode)
    cdef int double_dec_d(const double  * const input, const size_t input_len,
                          const Wavelet * const wavelet,
                          double  * const output, const size_t output_len,
                          const MODE mode)

    cdef int double_rec_a(const double * const coeffs_a, const size_t coeffs_len,
                          const Wavelet * const wavelet,
                          double  * const output, const size_t output_len)
    cdef int double_rec_d(const double * const coeffs_d, const size_t coeffs_len,
                          const Wavelet * const wavelet,
                          double  * const output, const size_t output_len)

    cdef int double_idwt(double * const coeffs_a, const size_t coeffs_a_len,
                         double * const coeffs_d, const size_t coeffs_d_len,
                         const Wavelet * const wavelet,
                         double  * const output, const size_t output_len,
                         const MODE mode, const int correct_size)

    cdef int double_swt_a(double input[], index_t input_len, Wavelet* wavelet,
                          double output[], index_t output_len, int level)
    cdef int double_swt_d(double input[], index_t input_len, Wavelet* wavelet,
                          double output[], index_t output_len, int level)


    cdef int float_dec_a(const float  * const input, const size_t input_len,
                         const Wavelet * const wavelet,
                         float  * const output, const size_t output_len,
                         const MODE mode)
    cdef int float_dec_d(const float  * const input, const size_t input_len,
                         const Wavelet * const wavelet,
                         float  * const output, const size_t output_len,
                         const MODE mode)

    cdef int float_rec_a(const float * const coeffs_a, const size_t coeffs_len,
                         const Wavelet * const wavelet,
                         float  * const output, const size_t output_len)
    cdef int float_rec_d(const float * const coeffs_d, const size_t coeffs_len,
                         const Wavelet * const wavelet,
                         float  * const output, const size_t output_len)

    cdef int float_idwt(const float * const coeffs_a, const size_t coeffs_a_len,
                        const float * const coeffs_d, const size_t coeffs_d_len,
                        const Wavelet * const wavelet,
                        float  * const output, const size_t output_len,
                        const MODE mode, const int correct_size)

    cdef int float_swt_a(float input[], index_t input_len, Wavelet* wavelet,
                         float output[], index_t output_len, int level)
    cdef int float_swt_d(float input[], index_t input_len, Wavelet* wavelet,
                         float output[], index_t output_len, int level)
