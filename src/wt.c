// Copyright (c) 2006-2010 Filip Wasilewski <http://filipwasilewski.pl/>
// See COPYING for license details.

// $Id$

#include "wt.h"

// Decomposition of input with lowpass filter
int double_dec_a(double input[], index_t input_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len,
                  MODE mode){

    // check output length
    if(output_len != dwt_buffer_length(input_len, wavelet->dec_len, mode)){
        return -1;
    }

    return double_downsampling_convolution(input, input_len, wavelet->dec_lo_double,
                                             wavelet->dec_len, output, 2, mode);
}


// Decomposition of input with highpass filter

int double_dec_d(double input[], index_t input_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len,
                  MODE mode){

    // check output length
    if(output_len != dwt_buffer_length(input_len, wavelet->dec_len, mode))
        return -1;

    return double_downsampling_convolution(input, input_len, wavelet->dec_hi_double,
                                             wavelet->dec_len, output, 2, mode);
}


// Direct reconstruction with lowpass reconstruction filter

int double_rec_a(double coeffs_a[], index_t coeffs_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len){

    // check output length
    if(output_len != reconstruction_buffer_length(coeffs_len, wavelet->rec_len))
        return -1;
    
    return double_upsampling_convolution_full(coeffs_a, coeffs_len, wavelet->rec_lo_double,
                                                wavelet->rec_len, output, output_len);
}


// Direct reconstruction with highpass reconstruction filter

int double_rec_d(double coeffs_d[], index_t coeffs_len,
                  Wavelet* wavelet,
                  double output[], index_t output_len){

    // check for output length
    if(output_len != reconstruction_buffer_length(coeffs_len, wavelet->rec_len))
        return -1;
    
    return double_upsampling_convolution_full(coeffs_d, coeffs_len, wavelet->rec_hi_double,
                                                wavelet->rec_len, output, output_len);
}


// IDWT reconstruction from aproximation and detail coeffs
//
// If fix_size_diff is 1 then coeffs arrays can differ by one in length (this
// is useful in multilevel decompositions and reconstructions of odd-length signals)
// Requires zoer-filled output buffer
int double_idwt(double coeffs_a[], index_t coeffs_a_len,
                 double coeffs_d[], index_t coeffs_d_len,
                 Wavelet* wavelet,
                 double output[], index_t output_len,
                 MODE mode, int fix_size_diff){

    index_t input_len;
    
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
        if(double_upsampling_convolution_valid_sf(coeffs_a, input_len, wavelet->rec_lo_double,
                                wavelet->rec_len, output, output_len, mode) < 0){
            goto error;
        }
    }
    // and add reconstruction of details coeffs performed with highpass reconstruction filter
    if(coeffs_d){
        if(double_upsampling_convolution_valid_sf(coeffs_d, input_len, wavelet->rec_hi_double,
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
int double_swt_(double input[], index_t input_len,
                          const double filter[], index_t filter_len,
                          double output[], index_t output_len,
                          int level){

    double* e_filter;
    index_t i, e_filter_len;
    int ret;

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
        ret = double_downsampling_convolution(input, input_len, e_filter, e_filter_len, output, 1, MODE_PERIODIZATION);
        wtfree(e_filter);
        return ret;

    } else {
        return double_downsampling_convolution(input, input_len, filter, filter_len, output, 1, MODE_PERIODIZATION);
    }
}

// Approximation at specified level
// input    - approximation coeffs from upper level or signal if level == 1
int double_swt_a(double input[], index_t input_len, Wavelet* wavelet, double output[], index_t output_len, int level){
    return double_swt_(input, input_len, wavelet->dec_lo_double, wavelet->dec_len, output, output_len, level);
}

// Details at specified level
// input    - approximation coeffs from upper level or signal if level == 1
int double_swt_d(double input[], index_t input_len, Wavelet* wavelet, double output[], index_t output_len, int level){
    return double_swt_(input, input_len, wavelet->dec_hi_double, wavelet->dec_len, output, output_len, level);
}
int float_dec_a(float input[], index_t input_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len,
                  MODE mode){

    // check output length
    if(output_len != dwt_buffer_length(input_len, wavelet->dec_len, mode)){
        return -1;
    }

    return float_downsampling_convolution(input, input_len, wavelet->dec_lo_float,
                                             wavelet->dec_len, output, 2, mode);
}


// Decomposition of input with highpass filter

int float_dec_d(float input[], index_t input_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len,
                  MODE mode){

    // check output length
    if(output_len != dwt_buffer_length(input_len, wavelet->dec_len, mode))
        return -1;

    return float_downsampling_convolution(input, input_len, wavelet->dec_hi_float,
                                             wavelet->dec_len, output, 2, mode);
}


// Direct reconstruction with lowpass reconstruction filter

int float_rec_a(float coeffs_a[], index_t coeffs_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len){

    // check output length
    if(output_len != reconstruction_buffer_length(coeffs_len, wavelet->rec_len))
        return -1;
    
    return float_upsampling_convolution_full(coeffs_a, coeffs_len, wavelet->rec_lo_float,
                                                wavelet->rec_len, output, output_len);
}


// Direct reconstruction with highpass reconstruction filter

int float_rec_d(float coeffs_d[], index_t coeffs_len,
                  Wavelet* wavelet,
                  float output[], index_t output_len){

    // check for output length
    if(output_len != reconstruction_buffer_length(coeffs_len, wavelet->rec_len))
        return -1;
    
    return float_upsampling_convolution_full(coeffs_d, coeffs_len, wavelet->rec_hi_float,
                                                wavelet->rec_len, output, output_len);
}


// IDWT reconstruction from aproximation and detail coeffs
//
// If fix_size_diff is 1 then coeffs arrays can differ by one in length (this
// is useful in multilevel decompositions and reconstructions of odd-length signals)
// Requires zoer-filled output buffer
int float_idwt(float coeffs_a[], index_t coeffs_a_len,
                 float coeffs_d[], index_t coeffs_d_len,
                 Wavelet* wavelet,
                 float output[], index_t output_len,
                 MODE mode, int fix_size_diff){

    index_t input_len;
    
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
    // memset(output, 0, output_len * sizeof(float));

    // reconstruct approximation coeffs with lowpass reconstruction filter
    if(coeffs_a){
        if(float_upsampling_convolution_valid_sf(coeffs_a, input_len, wavelet->rec_lo_float,
                                wavelet->rec_len, output, output_len, mode) < 0){
            goto error;
        }
    }
    // and add reconstruction of details coeffs performed with highpass reconstruction filter
    if(coeffs_d){
        if(float_upsampling_convolution_valid_sf(coeffs_d, input_len, wavelet->rec_hi_float,
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
int float_swt_(float input[], index_t input_len,
                          const float filter[], index_t filter_len,
                          float output[], index_t output_len,
                          int level){

    float* e_filter;
    index_t i, e_filter_len;
    int ret;

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
        e_filter = wtcalloc(e_filter_len, sizeof(float));
        if(e_filter == NULL)
            return -1;

        // compute upsampled filter values
        for(i = 0; i < filter_len; ++i){
            e_filter[i << (level-1)] = filter[i];
        }
        ret = float_downsampling_convolution(input, input_len, e_filter, e_filter_len, output, 1, MODE_PERIODIZATION);
        wtfree(e_filter);
        return ret;

    } else {
        return float_downsampling_convolution(input, input_len, filter, filter_len, output, 1, MODE_PERIODIZATION);
    }
}

// Approximation at specified level
// input    - approximation coeffs from upper level or signal if level == 1
int float_swt_a(float input[], index_t input_len, Wavelet* wavelet, float output[], index_t output_len, int level){
    return float_swt_(input, input_len, wavelet->dec_lo_float, wavelet->dec_len, output, output_len, level);
}

// Details at specified level
// input    - approximation coeffs from upper level or signal if level == 1
int float_swt_d(float input[], index_t input_len, Wavelet* wavelet, float output[], index_t output_len, int level){
    return float_swt_(input, input_len, wavelet->dec_hi_float, wavelet->dec_len, output, output_len, level);
}
