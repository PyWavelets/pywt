/*
 * Note: this currently doesn't get installed.  There's also no way to query
 * the location of wt.h.  Conclusion: there is no C API.
 */

#include <stdio.h>

#include "wt.h"

int main(){

    // Using C API to decompose 1D signal.
    // Results equivalent to pywt.dwt([1,2,3,4,5,6,7,8], 'db2', 'zpd').
    // Compile: gcc -I../src dwt_decompose.c ../src/wt.c ../src/wavelets.c ../src/common.c ../src/convolution.c

    Wavelet *w = wavelet('d', 2);
    MODE mode = MODE_ZEROPAD;

    int i;
    float input[] = {1,2,3,4,5,6,7,8,9};
    float *cA, *cD;
    pywt_index_t input_len, output_len;

    input_len = sizeof input / sizeof input[0];
    output_len = dwt_buffer_length(input_len, w->dec_len, mode);

    cA = wtcalloc(output_len, sizeof(float));
    cD = wtcalloc(output_len, sizeof(float));

    printf("Wavelet: %s %d\n\n", w->family_name, w->vanishing_moments_psi);

    float_dec_a(input, input_len, w, cA, output_len, mode);
    float_dec_d(input, input_len, w, cD, output_len, mode);

    for(i=0; i<output_len; i++){
        printf("%f ", cA[i]);
    }
    printf("\n\n");

    for(i=0; i<output_len; i++){
        printf("%f ", cD[i]);
    }
    printf("\n");

    free_wavelet(w);
    wtfree(cA);
    wtfree(cD);
    return 0;
}
