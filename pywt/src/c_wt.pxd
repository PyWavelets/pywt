# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

from common cimport MODE, index_t
from wavelet cimport Wavelet


cdef extern from "wt.h":
    # Cython does not know the 'restrict' keyword
    cdef int double_dec_a(const double * const input, const size_t input_len,
                          const Wavelet * const wavelet,
                          double * const output, const size_t output_len,
                          const MODE mode)
    cdef int double_dec_d(const double * const input, const size_t input_len,
                          const Wavelet * const wavelet,
                          double * const output, const size_t output_len,
                          const MODE mode)

    cdef int double_rec_a(const double * const coeffs_a, const size_t coeffs_len,
                          const Wavelet * const wavelet,
                          double * const output, const size_t output_len)
    cdef int double_rec_d(const double * const coeffs_d, const size_t coeffs_len,
                          const Wavelet * const wavelet,
                          double * const output, const size_t output_len)

    cdef int double_idwt(double * const coeffs_a, const size_t coeffs_a_len,
                         double * const coeffs_d, const size_t coeffs_d_len,
                         const Wavelet * const wavelet,
                         double * const output, const size_t output_len,
                         const MODE mode, const int correct_size)

    cdef int double_swt_a(double input[], index_t input_len, Wavelet* wavelet,
                          double output[], index_t output_len, int level)
    cdef int double_swt_d(double input[], index_t input_len, Wavelet* wavelet,
                          double output[], index_t output_len, int level)


    cdef int float_dec_a(const float * const input, const size_t input_len,
                         const Wavelet * const wavelet,
                         float * const output, const size_t output_len,
                         const MODE mode)
    cdef int float_dec_d(const float * const input, const size_t input_len,
                         const Wavelet * const wavelet,
                         float * const output, const size_t output_len,
                         const MODE mode)

    cdef int float_rec_a(const float * const coeffs_a, const size_t coeffs_len,
                         const Wavelet * const wavelet,
                         float * const output, const size_t output_len)
    cdef int float_rec_d(const float * const coeffs_d, const size_t coeffs_len,
                         const Wavelet * const wavelet,
                         float * const output, const size_t output_len)

    cdef int float_idwt(const float * const coeffs_a, const size_t coeffs_a_len,
                        const float * const coeffs_d, const size_t coeffs_d_len,
                        const Wavelet * const wavelet,
                        float * const output, const size_t output_len,
                        const MODE mode, const int correct_size)

    cdef int float_swt_a(float input[], index_t input_len, Wavelet* wavelet,
                         float output[], index_t output_len, int level)
    cdef int float_swt_d(float input[], index_t input_len, Wavelet* wavelet,
                         float output[], index_t output_len, int level)
