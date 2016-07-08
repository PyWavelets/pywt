# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

from common cimport MODE, pywt_index_t, ArrayInfo, Coefficient
from wavelet cimport DiscreteWavelet, ContinuousWavelet


cdef extern from "c/wt.h":
    # Cython does not know the 'restrict' keyword
    cdef int double_downcoef_axis(const double * const input, const ArrayInfo input_info,
                                  double * const output, const ArrayInfo output_info,
                                  const DiscreteWavelet * const wavelet, const size_t axis,
                                  const Coefficient detail, const MODE mode)
    cdef int double_idwt_axis(const double * const coefs_a, const ArrayInfo * const a_info,
                              const double * const coefs_d, const ArrayInfo * const d_info,
                              double * const output, const ArrayInfo output_info,
                              const DiscreteWavelet * const wavelet, const size_t axis,
                              const MODE mode)
    cdef int double_dec_a(const double * const input, const size_t input_len,
                          const DiscreteWavelet * const wavelet,
                          double * const output, const size_t output_len,
                          const MODE mode)
    cdef int double_dec_d(const double * const input, const size_t input_len,
                          const DiscreteWavelet * const wavelet,
                          double * const output, const size_t output_len,
                          const MODE mode)

    cdef int double_rec_a(const double * const coeffs_a, const size_t coeffs_len,
                          const DiscreteWavelet * const wavelet,
                          double * const output, const size_t output_len)
    cdef int double_rec_d(const double * const coeffs_d, const size_t coeffs_len,
                          const DiscreteWavelet * const wavelet,
                          double * const output, const size_t output_len)

    cdef int double_idwt(double * const coeffs_a, const size_t coeffs_a_len,
                         double * const coeffs_d, const size_t coeffs_d_len,
                         double * const output, const size_t output_len,
                         const DiscreteWavelet * const wavelet, const MODE mode)

    cdef int double_swt_a(double input[], pywt_index_t input_len, DiscreteWavelet* wavelet,
                          double output[], pywt_index_t output_len, int level)
    cdef int double_swt_d(double input[], pywt_index_t input_len, DiscreteWavelet* wavelet,
                          double output[], pywt_index_t output_len, int level)


    cdef int float_downcoef_axis(const float * const input, const ArrayInfo input_info,
                                 float * const output, const ArrayInfo output_info,
                                 const DiscreteWavelet * const wavelet, const size_t axis,
                                 const Coefficient detail, const MODE mode)
    cdef int float_idwt_axis(const float * const coefs_a, const ArrayInfo * const a_info,
                             const float * const coefs_d, const ArrayInfo * const d_info,
                             float * const output, const ArrayInfo output_info,
                             const DiscreteWavelet * const wavelet, const size_t axis,
                             const MODE mode)
    cdef int float_dec_a(const float * const input, const size_t input_len,
                         const DiscreteWavelet * const wavelet,
                         float * const output, const size_t output_len,
                         const MODE mode)
    cdef int float_dec_d(const float * const input, const size_t input_len,
                         const DiscreteWavelet * const wavelet,
                         float * const output, const size_t output_len,
                         const MODE mode)

    cdef int float_rec_a(const float * const coeffs_a, const size_t coeffs_len,
                         const DiscreteWavelet * const wavelet,
                         float * const output, const size_t output_len)
    cdef int float_rec_d(const float * const coeffs_d, const size_t coeffs_len,
                         const DiscreteWavelet * const wavelet,
                         float * const output, const size_t output_len)

    cdef int float_idwt(const float * const coeffs_a, const size_t coeffs_a_len,
                        const float * const coeffs_d, const size_t coeffs_d_len,
                        float * const output, const size_t output_len,
                        const DiscreteWavelet * const wavelet, const MODE mode)

    cdef int float_swt_a(float input[], pywt_index_t input_len, DiscreteWavelet* wavelet,
                         float output[], pywt_index_t output_len, int level)
    cdef int float_swt_d(float input[], pywt_index_t input_len, DiscreteWavelet* wavelet,
                         float output[], pywt_index_t output_len, int level)

cdef extern from "c/cwt.h":
    # Cython does not know the 'restrict' keyword
    
    cdef void double_gaus(const double * const input, double * const output, const size_t N,
                                  const size_t number)

    cdef void double_mexh(const double * const input, double * const output, const size_t N)
    
    cdef void double_morl(const double * const input, double * const output, const size_t N)
    

    cdef void double_cgau(const double * const input, double * const output_r, double * const output_i, const size_t N,
                                  const size_t number)
    
    cdef void double_shan(const double * const input, double * const output_r, double * const output_i, const size_t N,
                                  double FB, double FC)
    cdef void double_fbsp(const double * const input, double * const output_r, double * const output_i, const size_t N,
                                  int M, double FB, double FC)
    cdef void double_cmor(const double * const input, double * const output_r, double * const output_i, const size_t N,
                                  double FB, double FC)   


    cdef void float_gaus(const float * const input, float * const output, const size_t N,
                                  const size_t number)

    cdef void float_mexh(const float * const input, float * const output, const size_t N)
    
    cdef void float_morl(const float * const input, float * const output, const size_t N)
    
    cdef void float_cgau(const float * const input, float * const output_r, float * const output_i, const size_t N,
                                  const size_t number)

    cdef void float_shan(const float * const input, float * const output_r, float * const output_i, const size_t N,
                        float FB, float FC)

    cdef void float_fbsp(const float * const input, float * const output_r, float * const output_i, const size_t N,
                        int M, float FB, float FC)   

    cdef void float_cmor(const float * const input, float * const output_r, float * const output_i, const size_t N,
                        float FB, float FC)
