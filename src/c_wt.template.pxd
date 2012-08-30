# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

cdef extern from "common.h":

    ctypedef int index_t
    ctypedef int const_index_t

    cdef void* wtmalloc(long size)
    cdef void* wtcalloc(long len, long size)
    cdef void wtfree(void* ptr)
    
    ctypedef enum MODE:
        MODE_INVALID = -1
        MODE_ZEROPAD = 0
        MODE_SYMMETRIC
        MODE_ASYMMETRIC
        MODE_CONSTANT_EDGE
        MODE_SMOOTH
        MODE_PERIODIC
        MODE_PERIODIZATION
        MODE_MAX


    # buffers lengths
    cdef index_t dwt_buffer_length(index_t input_len, index_t filter_len, MODE mode)
    cdef index_t upsampling_buffer_length(index_t coeffs_len, index_t filter_len, MODE mode)
    cdef index_t idwt_buffer_length(index_t coeffs_len, index_t filter_len, MODE mode)
    cdef index_t swt_buffer_length(index_t coeffs_len)
    cdef index_t reconstruction_buffer_length(index_t coeffs_len, index_t filter_len)

    # max dec levels
    cdef int dwt_max_level(index_t input_len, index_t filter_len)
    cdef int swt_max_level(index_t input_len)


cdef extern from "wavelets.h":

    ctypedef enum SYMMETRY:
        ASYMMETRIC
        NEAR_SYMMETRIC
        SYMMETRIC

    ctypedef struct Wavelet:
        //## FOR $DTYPE$ IN (double, float):
        $DTYPE$* dec_hi_$DTYPE$      # highpass decomposition
        $DTYPE$* dec_lo_$DTYPE$      # lowpass   decomposition
        $DTYPE$* rec_hi_$DTYPE$      # highpass reconstruction
        $DTYPE$* rec_lo_$DTYPE$      # lowpass   reconstruction
        //## ENDFOR $DTYPE$
        
        index_t dec_len         # length of decomposition filter
        index_t rec_len         # length of reconstruction filter

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
    cdef Wavelet* blank_wavelet(index_t filter_length)
    cdef void free_wavelet(Wavelet* wavelet)


cdef extern from "wt.h":

//## FOR $DTYPE$ IN (double, float):

    cdef int $DTYPE$_dec_a($DTYPE$ input[], index_t input_len, Wavelet* wavelet, $DTYPE$ output[], index_t output_len, MODE mode)
    cdef int $DTYPE$_dec_d($DTYPE$ input[], index_t input_len, Wavelet* wavelet, $DTYPE$ output[], index_t output_len, MODE mode)

    cdef int $DTYPE$_rec_a($DTYPE$ coeffs_a[], index_t coeffs_len, Wavelet* wavelet, $DTYPE$ output[], index_t output_len)
    cdef int $DTYPE$_rec_d($DTYPE$ coeffs_d[], index_t coeffs_len, Wavelet* wavelet, $DTYPE$ output[], index_t output_len)

    cdef int $DTYPE$_idwt($DTYPE$ coeffs_a[], index_t coeffs_a_len, $DTYPE$ coeffs_d[], index_t coeffs_d_len,
                        Wavelet* wavelet, $DTYPE$ output[], index_t output_len, MODE mode, int correct_size)

    cdef int $DTYPE$_swt_a($DTYPE$ input[], index_t input_len, Wavelet* wavelet, $DTYPE$ output[], index_t output_len, int level)
    cdef int $DTYPE$_swt_d($DTYPE$ input[], index_t input_len, Wavelet* wavelet, $DTYPE$ output[], index_t output_len, int level)

//## ENDFOR $DTYPE$

