// Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
// See COPYING for license details.

// $Id$

#include "wt.h"

// Decomposition of input with lowpass filter

int d_dec_a(double input[], index_t input_len,
			Wavelet* wavelet,
			double output[], index_t output_len,
			MODE mode){

	// check output length
	if(output_len != dwt_buffer_length(input_len, wavelet->dec_len, mode)){
		return -1;
	}

	return downsampling_convolution(input, input_len, wavelet->dec_lo,
										wavelet->dec_len, output, 2, mode);
}


// Decomposition of input with highpass filter

int d_dec_d(double input[], index_t input_len,
			Wavelet* wavelet,
			double output[], index_t output_len,
			MODE mode){

	// check output length
	if(output_len != dwt_buffer_length(input_len, wavelet->dec_len, mode))
		return -1;

	return downsampling_convolution(input, input_len, wavelet->dec_hi,
										wavelet->dec_len, output, 2, mode);
}


// Direct reconstruction with lowpass reconstruction filter

int d_rec_a(double coeffs_a[], index_t coeffs_len,
			Wavelet* wavelet,
			double output[], index_t output_len){

	// check output length
	if(output_len != reconstruction_buffer_length(coeffs_len, wavelet->rec_len))
		return -1;
	
	return upsampling_convolution_full(coeffs_a, coeffs_len, wavelet->rec_lo,
										wavelet->rec_len, output, output_len);
}


// Direct reconstruction with highpass reconstruction filter

int d_rec_d(double coeffs_d[], index_t coeffs_len,
			Wavelet* wavelet,
			double output[], index_t output_len){

	// check for output length
	if(output_len != reconstruction_buffer_length(coeffs_len, wavelet->rec_len))
		return -1;
	
	return upsampling_convolution_full(coeffs_d, coeffs_len, wavelet->rec_hi,
										wavelet->rec_len, output, output_len);
}


// IDWT reconstruction from aproximation and detail coeffs
//
// If fix_size_diff is 1 then coeffs arrays can differ by one in length (this
// is useful in multilevel decompositions and reconstructions of odd-length signals)
// Requires zoer-filled output buffer
int d_idwt(double coeffs_a[], index_t coeffs_a_len,
		   double coeffs_d[], index_t coeffs_d_len,
		   Wavelet* wavelet,
		   double output[], index_t output_len,
		   MODE mode, int fix_size_diff){

	int input_len;
	
	// If one of coeffs array is NULL then the reconstruction will be performed
	// using the other one

	if(coeffs_a != NULL && coeffs_d != NULL){

		if(fix_size_diff){
			if( (coeffs_a_len > coeffs_d_len ? coeffs_a_len - coeffs_d_len
											 : coeffs_d_len-coeffs_a_len) > 1){ // abs(a-b)
				goto error;
			}

			input_len = coeffs_a_len>coeffs_d_len ? coeffs_d_len
												  : coeffs_a_len; // min
		} else {
			if(coeffs_a_len != coeffs_d_len)
				goto error;

			input_len = coeffs_a_len;
		}

	} else if(coeffs_a != NULL){
		input_len  = coeffs_a_len;

	} else if (coeffs_d != NULL){
		input_len = coeffs_d_len;

	} else {
		goto error;
	}
	
	// check output size
	if(output_len != idwt_buffer_length(input_len, wavelet->rec_len, mode))
		goto error;

	// // set output to zero (this can be ommited if output array is already cleared)
	// memset(output, 0, output_len * sizeof(double));

	// reconstruct approximation coeffs with lowpass reconstruction filter
	if(coeffs_a){
		if( upsampling_convolution_valid_sf(coeffs_a, input_len, wavelet->rec_lo,
								wavelet->rec_len, output, output_len, mode) < 0){
			goto error;
		}
	}
	// and add reconstruction of details coeffs performed with highpass reconstruction filter
	if(coeffs_d){
		if(	upsampling_convolution_valid_sf(coeffs_d, input_len, wavelet->rec_hi,
								wavelet->rec_len, output, output_len, mode) < 0){
			goto error;
		}
	}

	return 0;

	error:
		return -1;
}

// basic SWT step
// TODO: optimize
__inline int d_swt_(double input[], index_t input_len,
					const double filter[], index_t filter_len,
					double output[], index_t output_len,
					int level){

	double* e_filter;
	index_t i, e_filter_len;

	if(level < 1)
		return -1;
	
	if(level > swt_max_level(input_len))
		return -2;

	if(output_len != swt_buffer_length(input_len))
		return -1;

	// TODO: quick hack, optimize
	if(level > 1){
		// allocate filter first
		e_filter_len = filter_len << (level-1);
		e_filter = wtcalloc(e_filter_len, sizeof(double));
		if(e_filter == NULL)
			return -1;

		// compute upsampled filter values
		for(i = 0; i < filter_len; ++i){
			e_filter[i << (level-1)] = filter[i];
		}
		i = downsampling_convolution(input, input_len, e_filter, e_filter_len, output, 1, MODE_PERIODIZATION);
		wtfree(e_filter);
		return i;

	} else {
		return downsampling_convolution(input, input_len, filter, filter_len, output, 1, MODE_PERIODIZATION);
	}
}

// Approximation at specified level
// input	- approximation coeffs from upper level or signal if level == 1
int d_swt_a(double input[], index_t input_len, Wavelet* wavelet, double output[], index_t output_len, int level){
	return d_swt_(input, input_len, wavelet->dec_lo, wavelet->dec_len, output, output_len, level);
}

// Details at specified level
// input	- approximation coeffs from upper level or signal if level == 1
int d_swt_d(double input[], index_t input_len, Wavelet* wavelet, double output[], index_t output_len, int level){
	return d_swt_(input, input_len, wavelet->dec_hi, wavelet->dec_len, output, output_len, level);
}

