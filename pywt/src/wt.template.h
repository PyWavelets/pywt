/* Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/> */
/* See COPYING for license details. */

/* Wavelet transforms using convolution functions defined in convolution.h */

#include "templating.h"

#ifndef TYPE
#error TYPE must be defined here.
#else

#include "wt.h"

#if defined _MSC_VER
#define restrict __restrict
#elif defined __GNUC__
#define restrict __restrict__
#endif

/* _a suffix - wavelet transform approximations */
/* _d suffix - wavelet transform details */

/* Single level decomposition */
int CAT(TYPE, _dec_a)(const TYPE * const restrict input, const size_t input_len,
                      const Wavelet * const restrict wavelet,
                      TYPE * const restrict output, const size_t output_len,
                      const MODE mode);

int CAT(TYPE, _dec_d)(const TYPE * const restrict input, const size_t input_len,
                      const Wavelet * const restrict wavelet,
                      TYPE * const restrict output, const size_t output_len,
                      const MODE mode);

/* Single level reconstruction */
int CAT(TYPE, _rec_a)(const TYPE * const restrict coeffs_a, const size_t coeffs_len,
                      const Wavelet * const restrict wavelet,
                      TYPE * const restrict output, const size_t output_len);

int CAT(TYPE, _rec_d)(const TYPE * const restrict coeffs_d, const size_t coeffs_len,
                      const Wavelet * const restrict wavelet,
                      TYPE * const restrict output, const size_t output_len);

/* Single level IDWT reconstruction */
int CAT(TYPE, _idwt)(const TYPE * const restrict coeffs_a, const size_t coeffs_a_len,
                     const TYPE * const restrict coeffs_d, const size_t coeffs_d_len,
                     const Wavelet * const wavelet,
                     TYPE * const restrict output, const size_t output_len,
                     const MODE mode, const int fix_size_diff);

/* SWT decomposition at given level */
int CAT(TYPE, _swt_a)(TYPE input[], index_t input_len,
                      Wavelet* wavelet,
                      TYPE output[], index_t output_len,
                      int level);

int CAT(TYPE, _swt_d)(TYPE input[], index_t input_len,
                      Wavelet* wavelet,
                      TYPE output[], index_t output_len,
                      int level);

#endif /* TYPE */
#undef restrict
