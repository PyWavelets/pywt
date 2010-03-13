// Copyright (c) 2006-2010 Filip Wasilewski <http://filipwasilewski.pl/>
// See COPYING for license details.

// $Id$

// Wavelet transforms using convolution functions defined in convolution.h

#ifndef _WT_H_
#define _WT_H_

#include <memory.h>
#include <math.h>

#include "common.h"
#include "convolution.h"
#include "wavelets.h"


// _a suffix - wavelet transform aproximations
// _d suffix - wavelet transform details
// Single level decomposition
int double_dec_a(double input[], index_t input_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len,
                  MODE mode);

int double_dec_d(double input[], index_t input_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len,
                  MODE mode);

// Single level reconstruction
int double_rec_a(double coeffs_a[], index_t coeffs_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len);

int double_rec_d(double coeffs_d[], index_t coeffs_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len);

// Single level IDWT reconstruction
int double_idwt(double coeffs_a[], index_t coeffs_a_len,
                 double coeffs_d[], index_t coeffs_d_len,
                 Wavelet* wavelet,
                 double output[], index_t output_len,
                 MODE mode, int fix_size_diff);

// SWT decomposition at given level
int double_swt_a(double input[], index_t input_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len,
                  int level);

int double_swt_d(double input[], index_t input_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len,
                  int level);
// Single level decomposition
int float_dec_a(float input[], index_t input_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len,
                  MODE mode);

int float_dec_d(float input[], index_t input_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len,
                  MODE mode);

// Single level reconstruction
int float_rec_a(float coeffs_a[], index_t coeffs_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len);

int float_rec_d(float coeffs_d[], index_t coeffs_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len);

// Single level IDWT reconstruction
int float_idwt(float coeffs_a[], index_t coeffs_a_len,
                 float coeffs_d[], index_t coeffs_d_len,
                 Wavelet* wavelet,
                 float output[], index_t output_len,
                 MODE mode, int fix_size_diff);

// SWT decomposition at given level
int float_swt_a(float input[], index_t input_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len,
                  int level);

int float_swt_d(float input[], index_t input_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len,
                  int level);

#endif
