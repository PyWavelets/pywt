// Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
// See COPYING for license details.

// $Id: wt.h 53 2006-07-07 15:59:33Z Filip $

// Wavelet transforms using convolution functions defined in convolution.h

#ifndef _WT_H_
#define _WT_H_

#ifdef MSVC
	#pragma inline_depth(2)
#endif

#include <memory.h>
#include <math.h>

#include "common.h"
#include "convolution.h"
#include "wavelets.h"

// d_ prefix - double-precision input, double-precision output

// _a suffix - wavelet transform aproximations
// _d suffix - wavelet transform details

// Single level decomposition
int d_dec_a(double input[], index_t input_len,
			Wavelet* wavelet,
			double output[], index_t output_len,
			MODE mode);

int d_dec_d(double input[], index_t input_len,
			Wavelet* wavelet,
			double output[], index_t output_len,
			MODE mode);

// Single level reconstruction
int d_rec_a(double coeffs_a[], index_t coeffs_len,
			Wavelet* wavelet,
			double output[], index_t output_len);

int d_rec_d(double coeffs_d[], index_t coeffs_len,
			Wavelet* wavelet,
			double output[], index_t output_len);

// Single level IDWT reconstruction
int d_idwt(double coeffs_a[], index_t coeffs_a_len,
		   double coeffs_d[], index_t coeffs_d_len,
		   Wavelet* wavelet,
		   double output[], index_t output_len,
		   MODE mode, int fix_size_diff);

// SWT decomposition at given level
int d_swt_a(double input[], index_t input_len,
			Wavelet* wavelet,
			double output[], index_t output_len,
			int level);

int d_swt_d(double input[], index_t input_len,
			Wavelet* wavelet,
			double output[], index_t output_len,
			int level);

#endif
