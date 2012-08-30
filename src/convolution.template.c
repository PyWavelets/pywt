// Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
// See COPYING for license details.

#include "convolution.h"

//## FOR $DTYPE$ IN (double, float):

int $DTYPE$_downsampling_convolution_periodization(const $DTYPE$* input, const_index_t N,
                             const $DTYPE$* filter, const_index_t F,
                             $DTYPE$* output, const_index_t step)

{

    index_t i, j, k, F_2, corr;
    index_t start;
    $DTYPE$ sum;
    $DTYPE$* ptr_w = output;

    i = step-1; // first element taken from input is input[step-1]
    //extending by (F-2)/2 elements
    start = F_2 = F/2;
    corr = 0;

    for(i=start; i < F; i+=step){
        sum = 0;
        for(j = 0; j < i+1-corr; ++j)    // overlapping
            sum += filter[j]*input[i-j-corr];

        if(N%2){
            if(F-j){ // if something to extend
                sum += filter[j] * input[N-1];
                if(F-j){
                    for(k = 2-corr; k <= F-j; ++k)
                        sum += filter[j-1+k] * input[N-k+1];
                }
            }
        } else { // extra element from input   -> i0 i1 i2 [i2]
            for(k = 1; k <= F-j; ++k)
                sum += filter[j-1+k] * input[N-k];
        }
        *(ptr_w++) = sum;
    }

    // F - N-1        - filter in input range
    // most time is spent in this loop
    for(; i < N; i+=step){                    // input elements,
        sum = 0;
        for(j = 0; j < F; ++j)
            sum += input[i-j]*filter[j];
        *(ptr_w++) = sum;
    }

    for(; i < N-step + (F/2)+1 + N%2; i += step){    // input elements
        sum = 0;
        k = i-N+1;
        for(j = k; j < F; ++j)                // overlapped elements
            sum += filter[j]*input[i-j];

        if(N%2 == 0){
            for(j = 0; j < k; ++j){            // out of boundary (filter elements [0, k-1])
                sum += filter[j]*input[k-1-j];
            }
        } else {                            // repeating extra element -> i0 i1 i2 [i2]
            for(j = 0; j < k-1; ++j)        // out of boundary (filter elements [0, k-1])
                sum += filter[j]*input[k-2-j];
            sum += filter[k-1] * input[N-1];
        }
        *(ptr_w++) = sum;
    }
    return 0;
}


int $DTYPE$_downsampling_convolution(const $DTYPE$* input, const_index_t N,
                             const $DTYPE$* filter, const_index_t F,
                             $DTYPE$* output,
                             const_index_t step, MODE mode)
{

    // This convolution performs efficient downsampling by computing every step'th
    // element of normal convolution (currently tested only for step=1 and step=2).
    //
    // It also implements several different strategies of dealing with border
    // distortion problem (the problem of computing convolution for not existing
    // elements of signal). To handle this the signal has to be "extended" on both
    // sides by computing the missing values.
    //
    // General schema is as follows:
    // 1. Handle extended on the left, convolve filter with samples computed for time < 0
    // 2. Do the normal decimated convolution of filter with signal samples
    // 3. Handle extended on the right, convolve filter with samples computed for time > n-1


    index_t i, j, k;
    index_t start;
    $DTYPE$ sum, tmp;
    #ifdef OPT_UNROLL2
        $DTYPE$ sum2;
    #endif
    #ifdef OPT_UNROLL4
        #ifndef OPT_UNROLL2
            $DTYPE$ sum2;
        #endif
        $DTYPE$ sum3, sum4;
    #endif

    $DTYPE$* ptr_w = output;

    i = start = step-1; // first element taken from input is input[step-1]

    if(F <= N){

        if(mode == MODE_PERIODIZATION){
            return $DTYPE$_downsampling_convolution_periodization(input, N, filter, F, output, step);

        // Other signal extension modes
        } else {

            ///////////////////////////////////////////////////////////////////////
            // 0 - F-1    - sliding in filter
            switch(mode)
            {
                case MODE_SYMMETRIC:
                    for(i=start; i < F; i+=step){
                        sum = 0;
                        for(j = 0; j <= i; ++j)
                            sum += filter[j]*input[i-j];
                        k = i+1;
                        for(j = i+1; j < F; ++j)
                            sum += filter[j] * input[j-k];
                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_ASYMMETRIC:
                    for(i=start; i < F; i+=step){
                        sum = 0;
                        for(j = 0; j <= i; ++j)
                            sum += filter[j]*input[i-j];
                        k = i+1;
                        for(j = i+1; j < F; ++j)
                            sum += filter[j] * (input[0] - input[j-k]); // -=
                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_CONSTANT_EDGE:
                    for(i=start; i < F; i+=step){
                        sum = 0;
                        for(j = 0; j <= i; ++j)
                            sum += filter[j]*input[i-j];

                        k = i+1;
                        for(j = i+1; j < F; ++j)
                            sum += filter[j] * input[0];

                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_SMOOTH:
                    for(i=start; i < F; i+=step){
                        sum = 0;
                        for(j = 0; j <= i; ++j)
                            sum += filter[j]*input[i-j];
                        tmp = input[0]-input[1];
                        for(j = i+1; j < F; ++j){
                            sum += filter[j] * (input[0] + tmp * (j-i));
                        }
                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_PERIODIC:
                    for(i=start; i < F; i+=step){
                        sum = 0;
                        for(j = 0; j <= i; ++j)
                            sum += filter[j]*input[i-j];

                        k = N+i;
                        for(j = i+1; j < F; ++j)
                            sum += filter[j] * input[k-j];

                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_ZEROPAD:
                default:
                    for(i=start; i < F; i+=step){
                        sum = 0;
                        for(j = 0; j <= i; ++j)
                            sum += filter[j]*input[i-j];
                        *(ptr_w++) = sum;
                    }
                    break;
            }

            ///////////////////////////////////////////////////////////////////////
            // F - N-1        - filter in input range - simple convolution
            // most time is spent in this loop
            //printf("entering loop\n");
            #ifdef OPT_UNROLL4
            // manually unroll the loop a bit
            //printf("F: %d, N: %d, i: %d\n", F, N, i);
            if((N - F)/step > 4) {
                for(; i < (N - (3*step)); i += 4*step){                    // input elements,
                    //printf("EO4 iter: %d\n", i);
                    sum  = input[i]          * filter[0];
                    sum2 = input[i+step]     * filter[0];
                    sum3 = input[i+(2*step)] * filter[0];
                    sum4 = input[i+(3*step)] * filter[0];
                    for(j = 1; j < F; ++j){
                        sum += input[i-j]           * filter[j];
                        sum2 += input[(step+i)-j]   * filter[j];
                        sum3 += input[(2*step+i)-j] * filter[j];
                        sum4 += input[(3*step+i)-j] * filter[j];
                    }
                    *(ptr_w++) = sum;
                    *(ptr_w++) = sum2;
                    *(ptr_w++) = sum3;
                    *(ptr_w++) = sum4;
                }
            }
            #endif

            #ifdef OPT_UNROLL2
            if((N - F)/step > 2) {
                for(; i < (N - step); i += 2*step){                    // input elements,
                    //printf("EO2 iter: %d\n", i);
                    sum  = input[i]   * filter[0];
                    sum2 = input[i+step] * filter[0];
                    for(j = 1; j < F; ++j){
                        sum += input[i-j]         * filter[j];
                        sum2 += input[(step+i)-j] * filter[j];
                    }
                    *(ptr_w++) = sum;
                    *(ptr_w++) = sum2;
                }
            }
            #endif

            for(; i < N; i+=step){                    // input elements,
                sum = input[i] * filter[0];
                for(j = 1; j < F; ++j){
                    //printf("EO1 iter: %d\n", i);
                    sum += input[i-j]*filter[j];
                }
                *(ptr_w++) = sum;
            }
            ///////////////////////////////////////////////////////////////////////
            // N - N+F-1    - sliding out filter
            switch(mode)
            {
                case MODE_SYMMETRIC:
                    for(; i < N+F-1; i += step){    // input elements
                        sum = 0;
                        k = i-N+1;                    // 1, 2, 3 // overlapped elements
                        for(j = k; j < F; ++j)                    //TODO: j < F-_offset
                            sum += filter[j]*input[i-j];

                        for(j = 0; j < k; ++j)        // out of boundary        //TODO: j = _offset
                            sum += filter[j]*input[N-k+j]; // j-i-1            0*(N-1), 0*(N-2) 1*(N-1)

                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_ASYMMETRIC:
                    for(; i < N+F-1; i += step){    // input elements
                        sum = 0;
                        k = i-N+1;
                        for(j = k; j < F; ++j)        // overlapped elements
                            sum += filter[j]*input[i-j];

                        for(j = 0; j < k; ++j)        // out of boundary
                            sum += filter[j]*(input[N-1]-input[N-k-1+j]); // -=    j-i-1
                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_CONSTANT_EDGE:
                    for(; i < N+F-1; i += step){    // input elements
                        sum = 0;
                        k = i-N+1;
                        for(j = k; j < F; ++j)        // overlapped elements
                            sum += filter[j]*input[i-j];

                        for(j = 0; j < k; ++j)        // out of boundary (filter elements [0, k-1])
                            sum += filter[j]*input[N-1]; // input[N-1] = const

                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_SMOOTH:
                    for(; i < N+F-1; i += step){    // input elements
                        sum = 0;
                        k = i-N+1; // 1, 2, 3, ...
                        for(j = k; j < F; ++j)        // overlapped elements
                            sum += filter[j]*input[i-j];

                        tmp = input[N-1]-input[N-2];
                        for(j = 0; j < k; ++j)        // out of boundary (filter elements [0, k-1])
                            sum += filter[j] * (input[N-1] + tmp * (k-j));
                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_PERIODIC:
                    for(; i < N+F-1; i += step){    // input elements
                        sum = 0;
                        k = i-N+1;
                        for(j = k; j < F; ++j)        // overlapped elements
                            sum += filter[j]*input[i-j];
                        for(j = 0; j < k; ++j)        // out of boundary (filter elements [0, k-1])
                            sum += filter[j]*input[k-1-j];
                        *(ptr_w++) = sum;
                    }
                    break;

                case MODE_ZEROPAD:
                default:
                    for(; i < N+F-1; i += step){
                        sum = 0;
                        for(j = i-(N-1); j < F; ++j)
                            sum += input[i-j]*filter[j];
                        *(ptr_w++) = sum;
                    }
                    break;
            }
        }
        return 0;

    } else {
        // reallocating memory for short signals (shorter than filter) is cheap
        return $DTYPE$_allocating_downsampling_convolution(input, N, filter, F, output, step, mode);
    }
}

///////////////////////////////////////////////////////////////////////////////
//
// like downsampling_convolution, but with memory allocation
//

int $DTYPE$_allocating_downsampling_convolution(const $DTYPE$* input, const_index_t N,
                                        const $DTYPE$* filter, const_index_t F,
                                        $DTYPE$* output,
                                        const_index_t step, MODE mode)
{
    index_t i, j, F_minus_1, N_extended_len, N_extended_right_start;
    index_t start, stop;
    $DTYPE$ sum, tmp;
    $DTYPE$ *buffer;
    $DTYPE$* ptr_w = output;

    F_minus_1 = F - 1;
    start = F_minus_1+step-1;

    // allocate memory and copy input
    if(mode != MODE_PERIODIZATION){

        N_extended_len = N + 2*F_minus_1;
        N_extended_right_start = N + F_minus_1;

        buffer = wtcalloc(N_extended_len, sizeof($DTYPE$));
        if(buffer == NULL)
            return -1;

        memcpy(buffer+F_minus_1, input, sizeof($DTYPE$) * N);
        stop = N_extended_len;

    } else {

        N_extended_len = N + F-1;
        N_extended_right_start = N-1 + F/2;

        buffer = wtcalloc(N_extended_len, sizeof($DTYPE$));
        if(buffer == NULL)
            return -1;

        memcpy(buffer+F/2-1, input, sizeof($DTYPE$) * N);

        start -= 1;

        if(step == 1)
            stop = N_extended_len-1;
        else // step == 2
            stop = N_extended_len;
    }

    // copy extended signal elements
    switch(mode){

        case MODE_PERIODIZATION:
            if(N%2){ // odd - repeat last element
                buffer[N_extended_right_start] = input[N-1];
                for(j = 1; j < F/2; ++j)
                    buffer[N_extended_right_start+j] = buffer[F/2-2 + j]; // copy from beginning of `input` to right
                for(j = 0; j < F/2-1; ++j)                                  // copy from 'buffer' to left
                    buffer[F/2-2-j] =  buffer[N_extended_right_start-j];
            } else {
                for(j = 0; j < F/2; ++j)
                    buffer[N_extended_right_start+j] = input[j%N]; // copy from beginning of `input` to right
                for(j = 0; j < F/2-1; ++j)                           // copy from 'buffer' to left
                    buffer[F/2-2-j] =  buffer[N_extended_right_start-1-j];
            }
            break;

        case MODE_SYMMETRIC:
            for(j = 0; j < N; ++j){
                buffer[F_minus_1-1-j] = input[j%N];
                buffer[N_extended_right_start+j] = input[N-1-(j%N)];
            }
            i=j;
            // use `buffer` as source
            for(; j < F_minus_1; ++j){
                buffer[F_minus_1-1-j] =  buffer[N_extended_right_start-1+i-j];
                buffer[N_extended_right_start+j] = buffer[F_minus_1+j-i];
            }
            break;

        case MODE_ASYMMETRIC:
            for(j = 0; j < N; ++j){
                buffer[F_minus_1-1-j] = input[0] - input[j%N];
                buffer[N_extended_right_start+j] = (input[N-1] - input[N-1-(j%N)]);
            }
            i=j;
            // use `buffer` as source
            for(; j < F_minus_1; ++j){
                buffer[F_minus_1-1-j] =  buffer[N_extended_right_start-1+i-j];
                buffer[N_extended_right_start+j] = buffer[F_minus_1+j-i];
            }
            break;

        case MODE_SMOOTH:
            if(N>1){
                tmp = input[0]-input[1];
                for(j = 0; j < F_minus_1; ++j)
                    buffer[j] = input[0] +    (tmp * (F_minus_1-j));
                tmp = input[N-1]-input[N-2];
                for(j = 0; j < F_minus_1; ++j)
                    buffer[N_extended_right_start+j] = input[N-1] + (tmp*j);
                break;
            }

        case MODE_CONSTANT_EDGE:
            for(j = 0; j < F_minus_1; ++j){
                buffer[j] = input[0];
                buffer[N_extended_right_start+j] = input[N-1];
            }
            break;

        case MODE_PERIODIC:
            for(j = 0; j < F_minus_1; ++j)
                buffer[N_extended_right_start+j] = input[j%N]; // copy from beginning of `input` to right

            for(j = 0; j < F_minus_1; ++j)                       // copy from 'buffer' to left
                buffer[F_minus_1-1-j] =  buffer[N_extended_right_start-1-j];
            break;

        case MODE_ZEROPAD:
        default:
            //memset(buffer, 0, sizeof($DTYPE$)*F_minus_1);
            //memset(buffer+N_extended_right_start, 0, sizeof($DTYPE$)*F_minus_1);
            //memcpy(buffer+N_extended_right_start, buffer, sizeof($DTYPE$)*F_minus_1);
            break;
    }


    ///////////////////////////////////////////////////////////////////////
    // F - N-1        - filter in input range
    // perform convolution with decimation
    for(i=start; i < stop; i+=step){                    // input elements
        sum = 0;
        for(j = 0; j < F; ++j){
            sum += buffer[i-j]*filter[j];
        }
        *(ptr_w++) = sum;
    }

    // free memory
    wtfree(buffer);
    return 0;
}

///////////////////////////////////////////////////////////////////////////////
// requires zero-filled output buffer
// output is larger than input
// performs "normal" convolution of "upsampled" input coeffs array with filter

int $DTYPE$_upsampling_convolution_full(const $DTYPE$* input, const_index_t N,
                                const $DTYPE$* filter, const_index_t F,
                                $DTYPE$* output, const_index_t O){
    register index_t i;
    register index_t j;
    $DTYPE$ *ptr_out;

    if(F<2)
        return -1;

    ptr_out = output + ((N-1) << 1);

    for(i = N-1; i >= 0; --i){
        // sliding in filter from the right (end of input)
        // i0 0  i1 0  i2 0
        //                f1 -> o1
        //             f1 f2 -> o2
        //          f1 f2 f3 -> o3

        for(j = 0; j < F; ++j)
            ptr_out[j] += input[i] * filter[j]; // input[i] - const in loop
        ptr_out -= 2;
    }
    return 0;
}

///////////////////////////////////////////////////////////////////////////////
// performs IDWT for PERIODIZATION mode only
// (refactored from the upsampling_convolution_valid_sf function)
//
// The upsampling is performed by splitting filters to even and odd elements
// and performing 2 convolutions
//
// The input data has to be periodically extended for this mode.

int $DTYPE$_upsampling_convolution_valid_sf_periodization(const $DTYPE$* input, const_index_t N,
                                    const $DTYPE$* filter, const_index_t F,
                                    $DTYPE$* output, const_index_t O)
{

    $DTYPE$ *ptr_out = output;
    $DTYPE$ *filter_even, *filter_odd;
    $DTYPE$ *periodization_buf = NULL;
    $DTYPE$ *periodization_buf_rear = NULL;
    $DTYPE$ *ptr_base;
    $DTYPE$ sum_even, sum_odd;
    index_t i, j, k, N_p = 0;
    index_t F_2 = F/2;

    if(F%2) return -3; // Filter must have even-length.

    ///////////////////////////////////////////////////////////////////////////
    // Handle special situation when input coeff data is shorter than half of
    // the filter's length. The coeff array has to be extended periodically.
    // This can be only valid for PERIODIZATION_MODE

    if(N < F_2)
    // =======
    {
        // Input data for periodization mode has to be periodically extended

        // New length for temporary input
        N_p = F_2-1 +N;

        // periodization_buf will hold periodically copied input coeffs values
        periodization_buf = wtcalloc(N_p, sizeof($DTYPE$));

        if(periodization_buf == NULL)
            return -1;

        // Copy input data to its place in the periodization_buf
        // -> [0 0 0 i1 i2 i3 0 0 0]
        k = (F_2-1)/2;
        for(i=k; i < k+N; ++i)
            periodization_buf[i] = input[(i-k)%N];

        //if(N%2)
        //    periodization_buf[i++] = input[N-1];

        // [0 0 0 i1 i2 i3 0 0 0]
        //  points here ^^
        periodization_buf_rear = periodization_buf+i-1;

        // copy cyclically () to right
        // [0 0 0 i1 i2 i3 i1 i2 ...]
        j = i-k;
        for(; i < N_p; ++i)
            periodization_buf[i] = periodization_buf[i-j];

        // copy cyclically () to left
        // [... i2 i3 i1 i2 i3 i1 i2 i3]
        j = 0;
        for(i=k-1; i >= 0; --i){
            periodization_buf[i] = periodization_buf_rear[j];
            --j;
        }

        // Now perform the valid convolution
        if(F_2%2){
            $DTYPE$_upsampling_convolution_valid_sf(periodization_buf, N_p, filter, F, output, O, MODE_ZEROPAD);

        // The F_2%2==0 case needs special result fix (oh my, another one..)
        } else {

            // Cheap result fix for short inputs
            // Memory allocation for temporary output is done.
            // Computed temporary result is copied to output*

            ptr_out = wtcalloc(idwt_buffer_length(N, F, MODE_PERIODIZATION), sizeof($DTYPE$));
            if(ptr_out == NULL){
                wtfree(periodization_buf);
                return -1;
            }

            // Convolve here as for (F_2%2) branch above
            $DTYPE$_upsampling_convolution_valid_sf(periodization_buf, N_p, filter, F, ptr_out, O, MODE_ZEROPAD);

            // rewrite result to output
            for(i=2*N-1; i > 0; --i){
                output[i] += ptr_out[i-1];
            }
            // and the first element
            output[0] += ptr_out[2*N-1];
            wtfree(ptr_out);
            // and voil`a!, ugh
        }

    } else {
    // Otherwise (N >= F_2)

        // Allocate memory for even and odd elements of the filter
        filter_even = wtmalloc(F_2 * sizeof($DTYPE$));
        filter_odd = wtmalloc(F_2 * sizeof($DTYPE$));

        if(filter_odd == NULL || filter_odd == NULL){
            if(filter_odd == NULL) wtfree(filter_odd);
            if(filter_even == NULL) wtfree(filter_even);
            return -1;
        }

        // split filter to even and odd values
        for(i = 0; i < F_2; ++i){
            filter_even[i] = filter[i << 1];
            filter_odd[i] = filter[(i << 1) + 1];
        }

        ///////////////////////////////////////////////////////////////////////////
        // This part is quite complicated and has some wild checking to get results
        // similar to those from Matlab(TM) Wavelet Toolbox

        k = F_2-1;

        // Check if extending is really needed
        N_p = F_2-1 + (index_t) ceil(k/2.); /*split filter len correct. +  extra samples*/

        // ok, if is then do:
        // 1. Allocate buffers for front and rear parts of extended input
        // 2. Copy periodically appropriate elements from input to the buffers
        // 3. Convolve front buffer, input and rear buffer with even and odd
        //    elements of the filter (this results in upsampling)
        // 4. Free memory

        if(N_p > 0){
        // =======

            // Allocate memory only for the front and rear extension parts, not the
            // whole input
            periodization_buf = wtcalloc(N_p, sizeof($DTYPE$));
            periodization_buf_rear = wtcalloc(N_p, sizeof($DTYPE$));

            // Memory checking
            if(periodization_buf == NULL || periodization_buf_rear == NULL){
                if(periodization_buf == NULL) wtfree(periodization_buf);
                if(periodization_buf_rear == NULL) wtfree(periodization_buf_rear);
                wtfree(filter_odd);
                wtfree(filter_even);
                return -1;
            }

            // Fill buffers with appropriate elements
            memcpy(periodization_buf + N_p - k, input, k * sizeof($DTYPE$));        // copy from beginning of input to end of buffer
            for(i = 1; i <= (N_p - k); ++i)                                        // kopiowanie 'cykliczne' od końca input
                periodization_buf[(N_p - k) - i] = input[N - (i%N)];

            memcpy(periodization_buf_rear, input + N - k, k * sizeof($DTYPE$));    // copy from end of input to beginning of buffer
            for(i = 0; i < (N_p - k); ++i)                                        // kopiowanie 'cykliczne' od początku input
                periodization_buf_rear[k + i] = input[i%N];

            ///////////////////////////////////////////////////////////////////
            // Convolve filters with the (front) periodization_buf and compute
            // the first part of output

            ptr_base = periodization_buf + F_2 - 1;

            if(k%2 == 1){
                sum_odd = 0;

                for(j = 0; j < F_2; ++j)
                    sum_odd += filter_odd[j] * ptr_base[-j];
                *(ptr_out++) += sum_odd;

                --k;
                if(k)
                    $DTYPE$_upsampling_convolution_valid_sf(periodization_buf + 1, N_p-1, filter, F, ptr_out, O-1, MODE_ZEROPAD);

                ptr_out += k; // k0 - 1 // really move backward by 1

            } else if(k){
                $DTYPE$_upsampling_convolution_valid_sf(periodization_buf, N_p, filter, F, ptr_out, O, MODE_ZEROPAD);
                ptr_out += k;
            }
        }

        ///////////////////////////////////////////////////////////////////////////
        // Perform _valid_ convolution (only when all filter_even and filter_odd elements
        // are in range of input data).
        //
        // This part is simple, no extra hacks, just two convolutions in one loop

        ptr_base = ($DTYPE$*)input + F_2 - 1;
        for(i = 0; i < N-(F_2-1); ++i){    // sliding over signal from left to right

            sum_even = 0;
            sum_odd = 0;

            for(j = 0; j < F_2; ++j){
                sum_even += filter_even[j] * ptr_base[i-j];
                sum_odd += filter_odd[j] * ptr_base[i-j];
            }

            *(ptr_out++) += sum_even;
            *(ptr_out++) += sum_odd;
        }
        //
        ///////////////////////////////////////////////////////////////////////////

        if(N_p > 0){
        // =======

            k = F_2-1;
            if(k%2 == 1){
                if(F/2 <= N_p - 1){ // k > 1 ?
                    $DTYPE$_upsampling_convolution_valid_sf(periodization_buf_rear , N_p-1, filter, F, ptr_out, O-1, MODE_ZEROPAD);
                }

                ptr_out += k; // move forward anyway -> see lower

                if(F_2%2 == 0){ // remaining one element
                    ptr_base = periodization_buf_rear + N_p - 1;

                    sum_even = 0;
                    for(j = 0; j < F_2; ++j){
                        sum_even += filter_even[j] * ptr_base[-j];
                    }
                    *(--ptr_out) += sum_even; // move backward first
                }
            } else {
                if(k){
                    $DTYPE$_upsampling_convolution_valid_sf(periodization_buf_rear, N_p, filter, F, ptr_out, O, MODE_ZEROPAD);
                }
            }
        }
        if(periodization_buf != NULL) wtfree(periodization_buf);
        if(periodization_buf_rear != NULL) wtfree(periodization_buf_rear);

        wtfree(filter_even);
        wtfree(filter_odd);

    }
    return 0;
}


///////////////////////////////////////////////////////////////////////////////
// performs IDWT for all modes
//
// The upsampling is performed by splitting filters to even and odd elements
// and performing 2 convolutions.
// After refactoring the PERIODIZATION mode case to separate function this
// looks much clearer now.

int $DTYPE$_upsampling_convolution_valid_sf(const $DTYPE$* input, const_index_t N,
                                    const $DTYPE$* filter, const_index_t F,
                                    $DTYPE$* output, const_index_t O,
                                    MODE mode){

    $DTYPE$ *ptr_out = output;
    $DTYPE$ *filter_even, *filter_odd;
    $DTYPE$ *ptr_base;
    $DTYPE$ sum_even, sum_odd;
    #ifdef OPT_UNROLL2
        $DTYPE$ sum_even2, sum_odd2;
    #endif
    #ifdef OPT_UNROLL4
        #ifndef OPT_UNROLL2
            $DTYPE$ sum_even2, sum_odd2;
        #endif
        $DTYPE$ sum_even3, sum_odd3;
        $DTYPE$ sum_even4, sum_odd4;
    #endif

    index_t i, j;
    index_t F_2 = F/2;

    if(mode == MODE_PERIODIZATION) // Special case
        return $DTYPE$_upsampling_convolution_valid_sf_periodization(input, N, filter, F, output, O);

    if((F%2) || (N < F_2)) // Filter must have even length.
        return -1;

    // Allocate memory for even and odd elements of the filter
    filter_even = wtmalloc(F_2 * sizeof($DTYPE$));
    filter_odd = wtmalloc(F_2 * sizeof($DTYPE$));

    if(filter_odd == NULL || filter_odd == NULL){
        if(filter_odd == NULL) wtfree(filter_odd);
        if(filter_even == NULL) wtfree(filter_even);
        return -1;
    }

    // split filter to even and odd values
    for(i = 0; i < F_2; ++i){
        filter_even[i] = filter[i << 1];
        filter_odd[i] = filter[(i << 1) + 1];
    }

    ///////////////////////////////////////////////////////////////////////////
    // Perform _valid_ convolution (only when all filter_even and filter_odd elements
    // are in range of input data).
    //
    // This part is simple, no extra hacks, just two convolutions in one loop

    ptr_base = ($DTYPE$*)input + F_2 - 1;
    i = 0;

    #ifdef OPT_UNROLL4
    // manually unroll the loop a bit
    for(; i < N-(F_2-1+8); i+=4){    // sliding over signal from left to right
        sum_even  = filter_even[0] * ptr_base[i];
        sum_even2 = filter_even[0] * ptr_base[i+1];
        sum_even3 = filter_even[0] * ptr_base[i+2];
        sum_even4 = filter_even[0] * ptr_base[i+3];

        sum_odd   = filter_odd[0] * ptr_base[i];
        sum_odd2  = filter_odd[0] * ptr_base[i+1];
        sum_odd3  = filter_odd[0] * ptr_base[i+2];
        sum_odd4  = filter_odd[0] * ptr_base[i+3];

        for(j = 1; j < F_2; ++j){
            sum_even  += filter_even[j] * ptr_base[i-j];
            sum_even2 += filter_even[j] * ptr_base[(i+1)-j];
            sum_even3 += filter_even[j] * ptr_base[(i+2)-j];
            sum_even4 += filter_even[j] * ptr_base[(i+3)-j];

            sum_odd  += filter_odd[j] * ptr_base[i-j];
            sum_odd2 += filter_odd[j] * ptr_base[(i+1)-j];
            sum_odd3 += filter_odd[j] * ptr_base[(i+2)-j];
            sum_odd4 += filter_odd[j] * ptr_base[(i+3)-j];
        }

        *(ptr_out++) += sum_even;
        *(ptr_out++) += sum_odd;
        *(ptr_out++) += sum_even2;
        *(ptr_out++) += sum_odd2;
        *(ptr_out++) += sum_even3;
        *(ptr_out++) += sum_odd3;
        *(ptr_out++) += sum_even4;
        *(ptr_out++) += sum_odd4;
    }
    #endif

    #ifdef OPT_UNROLL2
    // manually unroll the loop a bit
    for(; i < N-(F_2+1); i+=2){    // sliding over signal from left to right
        sum_even = filter_even[0] * ptr_base[i];
        sum_even2 = filter_even[0] * ptr_base[i+1];

        sum_odd  = filter_odd[0] * ptr_base[i];
        sum_odd2  = filter_odd[0] * ptr_base[i+1];

        for(j = 1; j < F_2; ++j){
            sum_even += filter_even[j] * ptr_base[i-j];
            sum_even2 += filter_even[j] * ptr_base[(i+1)-j];

            sum_odd += filter_odd[j] * ptr_base[i-j];
            sum_odd2 += filter_odd[j] * ptr_base[(i+1)-j];
        }

        *(ptr_out++) += sum_even;
        *(ptr_out++) += sum_odd;
        *(ptr_out++) += sum_even2;
        *(ptr_out++) += sum_odd2;
    }
    #endif

    for(; i < N-(F_2-1); ++i){    // sliding over signal from left to right
        sum_even = filter_even[0] * ptr_base[i];
        sum_odd  = filter_odd[0] * ptr_base[i];

        for(j = 1; j < F_2; ++j){
            sum_even += filter_even[j] * ptr_base[i-j];
            sum_odd += filter_odd[j] * ptr_base[i-j];
        }

        *(ptr_out++) += sum_even;
        *(ptr_out++) += sum_odd;
    }

    //
    ///////////////////////////////////////////////////////////////////////////

    wtfree(filter_even);
    wtfree(filter_odd);
    return 0;
}

// -> swt - todo
int $DTYPE$_upsampled_filter_convolution(const $DTYPE$* input, const_index_t N, const $DTYPE$* filter, const_index_t F, $DTYPE$* output, const_index_t step, MODE mode)
{
    return -1;
}

//## ENDFOR $DTYPE$
