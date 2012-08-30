// Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
// See COPYING for license details.

#include "wt.h"

// Decomposition of input with lowpass filter

//## FOR $DTYPE$ IN (double, float):

int $DTYPE$_dec_a($DTYPE$ input[], index_t input_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len,
                  MODE mode){

    // check output length
    if(output_len != dwt_buffer_length(input_len, wavelet->dec_len, mode)){
        return -1;
    }

    return $DTYPE$_downsampling_convolution(input, input_len, wavelet->dec_lo_$DTYPE$,
                                             wavelet->dec_len, output, 2, mode);
}


// Decomposition of input with highpass filter

int $DTYPE$_dec_d($DTYPE$ input[], index_t input_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len,
                  MODE mode){

    // check output length
    if(output_len != dwt_buffer_length(input_len, wavelet->dec_len, mode))
        return -1;

    return $DTYPE$_downsampling_convolution(input, input_len, wavelet->dec_hi_$DTYPE$,
                                             wavelet->dec_len, output, 2, mode);
}


// Direct reconstruction with lowpass reconstruction filter

int $DTYPE$_rec_a($DTYPE$ coeffs_a[], index_t coeffs_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len){

    // check output length
    if(output_len != reconstruction_buffer_length(coeffs_len, wavelet->rec_len))
        return -1;
    
    return $DTYPE$_upsampling_convolution_full(coeffs_a, coeffs_len, wavelet->rec_lo_$DTYPE$,
                                                wavelet->rec_len, output, output_len);
}


// Direct reconstruction with highpass reconstruction filter

int $DTYPE$_rec_d($DTYPE$ coeffs_d[], index_t coeffs_len,
                  Wavelet* wavelet,
                  $DTYPE$ output[], index_t output_len){

    // check for output length
    if(output_len != reconstruction_buffer_length(coeffs_len, wavelet->rec_len))
        return -1;
    
    return $DTYPE$_upsampling_convolution_full(coeffs_d, coeffs_len, wavelet->rec_hi_$DTYPE$,
                                                wavelet->rec_len, output, output_len);
}


// IDWT reconstruction from approximation and detail coeffs
//
// If fix_size_diff is 1 then coeffs arrays can differ by one in length (this
// is useful in multilevel decompositions and reconstructions of odd-length signals)
// Requires zero-filled output buffer
int $DTYPE$_idwt($DTYPE$ coeffs_a[], index_t coeffs_a_len,
                 $DTYPE$ coeffs_d[], index_t coeffs_d_len,
                 Wavelet* wavelet,
                 $DTYPE$ output[], index_t output_len,
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

    // // set output to zero (this can be omitted if output array is already cleared)
    // memset(output, 0, output_len * sizeof($DTYPE$));

    // reconstruct approximation coeffs with lowpass reconstruction filter
    if(coeffs_a){
        if($DTYPE$_upsampling_convolution_valid_sf(coeffs_a, input_len, wavelet->rec_lo_$DTYPE$,
                                wavelet->rec_len, output, output_len, mode) < 0){
            goto error;
        }
    }
    // and add reconstruction of details coeffs performed with highpass reconstruction filter
    if(coeffs_d){
        if($DTYPE$_upsampling_convolution_valid_sf(coeffs_d, input_len, wavelet->rec_hi_$DTYPE$,
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
int $DTYPE$_swt_($DTYPE$ input[], index_t input_len,
                          const $DTYPE$ filter[], index_t filter_len,
                          $DTYPE$ output[], index_t output_len,
                          int level){

    $DTYPE$* e_filter;
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
        e_filter = wtcalloc(e_filter_len, sizeof($DTYPE$));
        if(e_filter == NULL)
            return -1;

        // compute upsampled filter values
        for(i = 0; i < filter_len; ++i){
            e_filter[i << (level-1)] = filter[i];
        }
        ret = $DTYPE$_downsampling_convolution(input, input_len, e_filter, e_filter_len, output, 1, MODE_PERIODIZATION);
        wtfree(e_filter);
        return ret;

    } else {
        return $DTYPE$_downsampling_convolution(input, input_len, filter, filter_len, output, 1, MODE_PERIODIZATION);
    }
}

// Approximation at specified level
// input    - approximation coeffs from upper level or signal if level == 1
int $DTYPE$_swt_a($DTYPE$ input[], index_t input_len, Wavelet* wavelet, $DTYPE$ output[], index_t output_len, int level){
    return $DTYPE$_swt_(input, input_len, wavelet->dec_lo_$DTYPE$, wavelet->dec_len, output, output_len, level);
}

// Details at specified level
// input    - approximation coeffs from upper level or signal if level == 1
int $DTYPE$_swt_d($DTYPE$ input[], index_t input_len, Wavelet* wavelet, $DTYPE$ output[], index_t output_len, int level){
    return $DTYPE$_swt_(input, input_len, wavelet->dec_hi_$DTYPE$, wavelet->dec_len, output, output_len, level);
}

//## ENDFOR $DTYPE$
