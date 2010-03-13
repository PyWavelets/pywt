// Copyright (c) 2006-2010 Filip Wasilewski <http://filipwasilewski.pl/>
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
// input    - input data
// N        - input data length
// filter   - filter data
// F        - filter data length
// output   - output data
// step     - decimation step
// mode     - signal extension mode

// memory efficient version
int double_downsampling_convolution(const double* input, const_index_t N, const double* filter, const_index_t F, double* output, const_index_t step, MODE mode);
int float_downsampling_convolution(const float* input, const_index_t N, const float* filter, const_index_t F, float* output, const_index_t step, MODE mode);

// Straightfoward implementation with memory reallocation - for very short signals (shorter than filter).
// This id called from downsampling_convolution
int double_allocating_downsampling_convolution(const double* input, const_index_t N, const double* filter, const_index_t F, double* output, const_index_t step, MODE mode);
int float_allocating_downsampling_convolution(const float* input, const_index_t N, const float* filter, const_index_t F, float* output, const_index_t step, MODE mode);

// standard convolution
// decimation step = 1
// #define double_convolution(data, data_len, filter, filter_len, output) double_downsampling_convolution(data, data_len, filter, filter_len, output, 1, MODE_ZEROPAD);
// #define float_convolution(data, data_len, filter, filter_len, output) float_downsampling_convolution(data, data_len, filter, filter_len, output, 1, MODE_ZEROPAD);

///////////////////////////////////////////////////////////////////////////////
// Performs normal (full) convolution of "upsampled" input coeffs array with filter
// Requires zero-filled output buffer (adds values instead of overwriting - can
// be called many times with the same output).
//
// input    - input data
// N        - input data length
// filter   - filter data
// F        - filter data length
// output   - output data
// O        - output lenght (currently not used)
// mode     - signal extension mode
int double_upsampling_convolution_full(const double* input, const_index_t N, const double* filter, const_index_t F, double* output, const_index_t O);
int float_upsampling_convolution_full(const float* input, const_index_t N, const float* filter, const_index_t F, float* output, const_index_t O);

// Performs valid convolution (signals must overlap)
// Extends (virtually) input for MODE_PERIODIZATION.
int double_upsampling_convolution_valid_sf(const double* input, const_index_t N, const double* filter, const_index_t F, double* output, const_index_t O, MODE mode);
int float_upsampling_convolution_valid_sf(const float* input, const_index_t N, const float* filter, const_index_t F, float* output, const_index_t O, MODE mode);

// TODO
// for SWT
// int upsampled_filter_convolution(const $DTYPE$* input, const int N, const $DTYPE$* filter, const int F, $DTYPE$* output, int step, int mode);

#endif
