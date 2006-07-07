// Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
// See COPYING for license details.

// $Id$

#ifndef _CONVOLUTION_H_
#define _CONVOLUTION_H_

#include <math.h>
#include "common.h"


///////////////////////////////////////////////////////////////////////////////
// Performs convolution of input with filter and downsamples by taking every
// step-th element from the result.
//
// input	- input data
// N		- input data length
// filter	- filter data
// F		- filter data length
// output	- output data
// step		- decimation step
// mode		- signal extension mode

// memory efficient version

int downsampling_convolution(CONST_DTYPE* input, const_index_t N, const double* filter, const_index_t F, DTYPE* output, const int step, const int mode);

// Straightfoward implementation with memory reallocation - for very short signals (shorter than filter).
// This id called from downsampling_convolution

int allocating_downsampling_convolution(CONST_DTYPE* input, const_index_t N, const double* filter, const_index_t F, DTYPE* output, const int step, const int mode);

// standard convolution
// decimation step = 1

#define convolution(data, data_len, filter, filter_len, output) downsampling_convolution(data, data_len, filter, filter_len, output, 1, MODE_ZEROPAD);


///////////////////////////////////////////////////////////////////////////////
// Upsamples input signal by inserting zeros and convolves with filter.
// input: i0 i1 i2 i3 -> (upsampling) -> i0 0 i1 0 i2 0 i3 (0)
//
// input	- input data
// N		- input data length
// filter	- filter data
// F		- filter data length
// output	- output data
// mode		- signal extension mode

///////////////////////////////////////////////////////////////////////////////
// Performs normal (full) convolution of "upsampled" input coeffs array with filter
// Requires zero-filled output buffer (adds values instead of overwriting - can
// be called many times with the same output).
//
// input	- input data
// N		- input data length
// filter	- filter data
// F		- filter data length
// output	- output data
// O		- output lenght (currently not used)
// mode		- signal extension mode

int upsampling_convolution_full(CONST_DTYPE* input, const_index_t N, const double* filter, const_index_t F, DTYPE* output, const_index_t O);

// Performs valid convolution (signals must overlap)
// Extends (virtually) input for MODE_PERIODIZATION.

int upsampling_convolution_valid_sf(CONST_DTYPE* input, const_index_t N, const double* filter, const_index_t F, DTYPE* output, const_index_t O, const int mode);

// TODO
// for SWT
// int upsampled_filter_convolution(const DTYPE* input, const int N, const double* filter, const int F, DTYPE* output, int step, int mode);

#endif
