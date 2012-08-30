// Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
// See COPYING for license details.

// Wavelet transforms using convolution functions defined in convolution.h

#ifndef _WT_H_
#define _WT_H_

#include <memory.h>
#include <math.h>

#include "common.h"
#include "convolution.h"
#include "wavelets.h"


// _a suffix - wavelet transform approximations
// _d suffix - wavelet transform details

//## FOR $DTYPE$ IN (double, float):

// Single level decomposition
int $DTYPE$_dec_a($DTYPE$ input[], index_t input_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len,
                  MODE mode);

int $DTYPE$_dec_d($DTYPE$ input[], index_t input_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len,
                  MODE mode);

// Single level reconstruction
int $DTYPE$_rec_a($DTYPE$ coeffs_a[], index_t coeffs_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len);

int $DTYPE$_rec_d($DTYPE$ coeffs_d[], index_t coeffs_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len);

// Single level IDWT reconstruction
int $DTYPE$_idwt($DTYPE$ coeffs_a[], index_t coeffs_a_len,
                 $DTYPE$ coeffs_d[], index_t coeffs_d_len,
                 Wavelet* wavelet,
                 $DTYPE$ output[], index_t output_len,
                 MODE mode, int fix_size_diff);

// SWT decomposition at given level
int $DTYPE$_swt_a($DTYPE$ input[], index_t input_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len,
                  int level);

int $DTYPE$_swt_d($DTYPE$ input[], index_t input_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len,
                  int level);

//## ENDFOR $DTYPE$

#endif
