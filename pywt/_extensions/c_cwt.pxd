# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

from common cimport MODE, index_t, ArrayInfo, Coefficient
from wavelet cimport ContinuousWavelet


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