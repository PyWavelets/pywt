// Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
// See COPYING for license details.

// $Id$

#include "common.h"

index_t dwt_buffer_length(index_t input_len, index_t filter_len, MODE mode){
	if(input_len < 1 || filter_len < 1)
		return 0;

	switch(mode){
			case MODE_PERIODIZATION:
				return (index_t) ceil(input_len / 2.);
				break;
			default:
				return (index_t) floor((input_len + filter_len - 1) / 2.);
				break;
	}
}

index_t reconstruction_buffer_length(index_t coeffs_len, index_t filter_len){
	if(coeffs_len < 1 || filter_len < 1)
		return 0;
	
	return 2*coeffs_len+filter_len-2;
}

index_t idwt_buffer_length(index_t coeffs_len, index_t filter_len, MODE mode){
	if(coeffs_len < 0 || filter_len < 0)
		return 0;
	
	switch(mode){
			case MODE_PERIODIZATION:
				return 2*coeffs_len;
				break;
			default:
				return 2*coeffs_len-filter_len+2;
	}
}

index_t swt_buffer_length(index_t input_len){
	if(input_len < 0)
		return 0;

	return input_len;
}

int dwt_max_level(index_t input_len, index_t filter_len){
	if(input_len < 1 || filter_len < 2)
		return 0;
	
	return (int) floor(log((double)input_len/(double)(filter_len-1)) /log(2.0));
}

int swt_max_level(index_t input_len){
	int i, j;
	i = (int) floor(log((double) input_len)/log(2.0));

	// check how many times (maximum i times) input_len is divisible by 2
	for(j=0; j <= i; ++j){
		if((input_len & 0x1)==1)
			return j;
		input_len >>= 1;
	}
	return i;
}

