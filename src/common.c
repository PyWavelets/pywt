// Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
// See COPYING for license details.

#include "common.h"

#ifdef PY_EXTENSION
void *wtcalloc(size_t len, size_t size){
        void *p = wtmalloc(len*size);
        if(p)
            memset(p, 0, len*size);
        return p;
}
#endif

// buffers and max levels params

index_t dwt_buffer_length(index_t input_len, index_t filter_len, MODE mode){
    if(input_len < 1 || filter_len < 1)
        return 0;

    switch(mode){
            case MODE_PERIODIZATION:
                return (index_t) ceil(input_len / 2.0);
            default:
                return (index_t) floor((input_len + filter_len - 1) / 2.0);
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
    int i;
    if(input_len < 1 || filter_len < 2)
        return 0;
    
    i = (int) floor(log((double)input_len/(double)(filter_len-1)) /log(2.0));
    return (i > 0) ? i : 0;
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
    return (i > 0) ? i : 0;
}
