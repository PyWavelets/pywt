// Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
// See COPYING for license details.

// $Id$

// Common constants, typedefs and functions

#ifndef _COMMON_H_
#define _COMMON_H_

#include <stdlib.h>
#include <math.h>
#include <memory.h>

// Memory management functions, can be changet to Python C-API equivalents
#define wtmalloc(size_t) malloc(size_t)
#define wtcalloc(len, size_t) calloc(len, size_t)
#define wtfree(ptr) free(ptr)


// Signal extension modes
typedef enum {
       MODE_INVALID = -1,
       MODE_ZEROPAD = 0,   // default, signal extended with zeros
       MODE_SYMMETRIC,     // signal extended symmetrically (mirror)
       MODE_ASYMMETRIC,
       MODE_CONSTANT_EDGE, // signal extended with the border value
       MODE_SMOOTH,        // linear extrapolation (first derivative)
       MODE_PERIODIC,      // signal is treated as being periodic
       MODE_PERIODIZATION, // signal is treated as being periodic, minimal output lenght
       MODE_MAX
} MODE;


///////////////////////////////////////////////////////////////////////////////
// Typedefs

// Integer type for indexing arrays.
// - it is signed because negative indexes are used in several places
// - TODO: should be changed to Py_ssize_t in future releases for Python 2.5

typedef int index_t; 
typedef const index_t const_index_t;

// Data type for input arrays (ie. can be changed to float)
typedef double DTYPE;
typedef const DTYPE CONST_DTYPE;


///////////////////////////////////////////////////////////////////////////////
// Calculating buffer lengths for various operations

// Length of DWT coeffs for specified input data length, filter length and
// signal extension mode 

index_t dwt_buffer_length(index_t input_len, index_t filter_len, MODE mode);

// Length of reconstructed signal for specified input coeffs length and filter
// length. It is used for direct reconstruction from coefficients (normal
// convolution of upsampled coeffs with filter).

index_t reconstruction_buffer_length(index_t coeffs_len, index_t filter_len);

// Length of IDWT reconstructed signal for specified input coeffs length, filter
// length and extension mode.

index_t idwt_buffer_length(index_t coeffs_len, index_t filter_len, MODE mode);

// Length of SWT coefficients for specified input signal length.
// Equals to input_len

index_t swt_buffer_length(index_t input_len);


///////////////////////////////////////////////////////////////////////////////
// Maximum useful level of DWT decomposition.

int dwt_max_level(index_t input_len, index_t filter_len);


///////////////////////////////////////////////////////////////////////////////
// Maximum useful level of SWT decomposition.

int swt_max_level(index_t input_len);


#endif //_COMMON_H_
