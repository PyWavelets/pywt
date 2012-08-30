// Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
// See COPYING for license details.

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

//##FOR $DTYPE$ in (double, float):
int $DTYPE$_downsampling_convolution(const $DTYPE$* input, const_index_t N, const $DTYPE$* filter, const_index_t F, $DTYPE$* output, const_index_t step, MODE mode);
//##ENDFOR $DTYPE$

// Straightforward implementation with memory reallocation - for very short signals (shorter than filter).
// This id called from downsampling_convolution

//##FOR $DTYPE$ in (double, float):
int $DTYPE$_allocating_downsampling_convolution(const $DTYPE$* input, const_index_t N, const $DTYPE$* filter, const_index_t F, $DTYPE$* output, const_index_t step, MODE mode);
//##ENDFOR $DTYPE$

// standard convolution
// decimation step = 1

//##FOR $DTYPE$ in (double, float):
// #define $DTYPE$_convolution(data, data_len, filter, filter_len, output) $DTYPE$_downsampling_convolution(data, data_len, filter, filter_len, output, 1, MODE_ZEROPAD);
//##ENDFOR $DTYPE$

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

//##FOR $DTYPE$ in (double, float):
int $DTYPE$_upsampling_convolution_full(const $DTYPE$* input, const_index_t N, const $DTYPE$* filter, const_index_t F, $DTYPE$* output, const_index_t O);
//##ENDFOR $DTYPE$

// Performs valid convolution (signals must overlap)
// Extends (virtually) input for MODE_PERIODIZATION.

//##FOR $DTYPE$ in (double, float):
int $DTYPE$_upsampling_convolution_valid_sf(const $DTYPE$* input, const_index_t N, const $DTYPE$* filter, const_index_t F, $DTYPE$* output, const_index_t O, MODE mode);
//##ENDFOR $DTYPE$

// TODO
// for SWT
// int upsampled_filter_convolution(const $DTYPE$* input, const int N, const $DTYPE$* filter, const int F, $DTYPE$* output, int step, int mode);

#endif
