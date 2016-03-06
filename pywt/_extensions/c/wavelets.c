/* Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/> */
/* See COPYING for license details. */

/* Allocating, setting properties and destroying wavelet structs */
#include "wavelets.h"
#include "wavelets_coeffs.h"

#define SWAP(x, y) ({typeof(x) tmp = x; x = y; y = tmp;})

Wavelet* wavelet(char name, unsigned int order)
{
    Wavelet *w;

    /* Haar wavelet */
    if(name == 'h' || name == 'H'){

        /* the same as db1 */
        w = wavelet('d', 1);
        w->family_name = "Haar";
        w->short_name = "haar";
        return w;

    /* Reverse biorthogonal wavelets family */
    } else if (name == 'r' || name == 'R') {
        /* rbio is like bior, only with switched filters */
        w = wavelet('b', order);
        if (w == NULL) return NULL;

        SWAP(w->dec_len, w->rec_len);
        SWAP(w->rec_lo_float, w->dec_lo_float);
        SWAP(w->rec_hi_float, w->dec_hi_float);
        SWAP(w->rec_lo_double, w->dec_lo_double);
        SWAP(w->rec_hi_double, w->dec_hi_double);

        {
            size_t i, j;
            for(i = 0, j = w->rec_len - 1; i < j; i++, j--){
                SWAP(w->rec_lo_float[i], w->rec_lo_float[j]);
                SWAP(w->rec_hi_float[i], w->rec_hi_float[j]);
                SWAP(w->dec_lo_float[i], w->dec_lo_float[j]);
                SWAP(w->dec_hi_float[i], w->dec_hi_float[j]);

                SWAP(w->rec_lo_double[i], w->rec_lo_double[j]);
                SWAP(w->rec_hi_double[i], w->rec_hi_double[j]);
                SWAP(w->dec_lo_double[i], w->dec_lo_double[j]);
                SWAP(w->dec_hi_double[i], w->dec_hi_double[j]);
            }
        }

        w->family_name = "Reverse biorthogonal";
        w->short_name = "rbio";

        return w;
    }

    switch(name){

        /* Daubechies wavelets family */
        case 'd':
        case 'D':
            if (order < 1 || order > 38) return NULL;
            w = blank_wavelet(2 * order);
            if(w == NULL) return NULL;

            w->vanishing_moments_psi = order;
            w->vanishing_moments_phi = 0;
            w->support_width = 2*order - 1;
            w->orthogonal = 1;
            w->biorthogonal = 1;
            w->symmetry = ASYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Daubechies";
            w->short_name = "db";

            {
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_float[i] = db_float[order - 1][i];
                    w->dec_lo_float[i] = db_float[order - 1][w->dec_len-1-i];
                    w->rec_hi_float[i] = ((i % 2) ? -1 : 1)
                      * db_float[order - 1][w->dec_len-1-i];
                    w->dec_hi_float[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * db_float[order - 1][i];
                }
            }

            {
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_double[i] = db_double[order - 1][i];
                    w->dec_lo_double[i] = db_double[order - 1][w->dec_len-1-i];
                    w->rec_hi_double[i] = ((i % 2) ? -1 : 1)
                      * db_double[order - 1][w->dec_len-1-i];
                    w->dec_hi_double[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * db_double[order - 1][i];
                }
            }

            break;

        /* Symlets wavelets family */
        case 's':
        case 'S':
            if (order < 2 || order > 20) return NULL;
            w = blank_wavelet(2 * order);
            if(w == NULL) return NULL;

            w->vanishing_moments_psi = order;
            w->vanishing_moments_phi = 0;
            w->support_width = 2*order - 1;
            w->orthogonal = 1;
            w->biorthogonal = 1;
            w->symmetry = NEAR_SYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Symlets";
            w->short_name = "sym";

            {
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_float[i] = sym_float[order - 2][i];
                    w->dec_lo_float[i] = sym_float[order - 2][w->dec_len-1-i];
                    w->rec_hi_float[i] = ((i % 2) ? -1 : 1)
                      * sym_float[order - 2][w->dec_len-1-i];
                    w->dec_hi_float[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * sym_float[order - 2][i];
                }
            }

            {
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_double[i] = sym_double[order - 2][i];
                    w->dec_lo_double[i] = sym_double[order - 2][w->dec_len-1-i];
                    w->rec_hi_double[i] = ((i % 2) ? -1 : 1)
                      * sym_double[order - 2][w->dec_len-1-i];
                    w->dec_hi_double[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * sym_double[order - 2][i];
                }
            }
            break;

        /* Coiflets wavelets family */
        case 'c':
        case 'C':
            if (order < 1 || order > 17) return NULL;
            w = blank_wavelet(6 * order);
            if(w == NULL) return NULL;

            w->vanishing_moments_psi = 2*order;
            w->vanishing_moments_phi = 2*order -1;
            w->support_width = 6*order - 1;
            w->orthogonal = 1;
            w->biorthogonal = 1;
            w->symmetry = NEAR_SYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Coiflets";
            w->short_name = "coif";

            {
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_float[i] = coif_float[order - 1][i] * sqrt2_float;
                    w->dec_lo_float[i] = coif_float[order - 1][w->dec_len-1-i]
                      * sqrt2_float;
                    w->rec_hi_float[i] = ((i % 2) ? -1 : 1)
                      * coif_float[order - 1][w->dec_len-1-i] * sqrt2_float;
                    w->dec_hi_float[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * coif_float[order - 1][i] * sqrt2_float;
                }
            }

            {
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_double[i] = coif_double[order - 1][i] * sqrt2_double;
                    w->dec_lo_double[i] = coif_double[order - 1][w->dec_len-1-i]
                      * sqrt2_double;
                    w->rec_hi_double[i] = ((i % 2) ? -1 : 1)
                      * coif_double[order - 1][w->dec_len-1-i] * sqrt2_double;
                    w->dec_hi_double[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * coif_double[order - 1][i] * sqrt2_double;
                }
            }
            break;

        /* Biorthogonal wavelets family */
        case 'b':
        case 'B': {
            unsigned int N = order / 10, M = order % 10;
            size_t M_idx;
            size_t M_max;
            switch (N) {
            case 1:
                if (M % 2 != 1 || M > 5) return NULL;
                M_idx = M / 2;
                M_max = 5;
                break;
            case 2:
                if (M % 2 != 0 || M < 2 || M > 8) return NULL;
                M_idx = M / 2 - 1;
                M_max = 8;
                break;
            case 3:
                if (M % 2 != 1) return NULL;
                M_idx = M / 2;
                M_max = 9;
                break;
            case 4:
            case 5:
                if (M != N) return NULL;
                M_idx = 0;
                M_max = M;
                break;
            case 6:
                if (M != 8) return NULL;
                M_idx = 0;
                M_max = 8;
                break;
            default:
                return NULL;
            }

            w = blank_wavelet((N == 1) ? 2 * M : 2 * M + 2);
            if(w == NULL) return NULL;

            w->vanishing_moments_psi = order/10;
            w->vanishing_moments_phi = -1;
            w->support_width = -1;
            w->orthogonal = 0;
            w->biorthogonal = 1;
            w->symmetry = SYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Biorthogonal";
            w->short_name = "bior";

            {
                size_t n = M_max - M;
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_float[i] = bior_float[N - 1][0][i+n];
                    w->dec_lo_float[i] = bior_float[N - 1][M_idx+1][w->dec_len-1-i];
                    w->rec_hi_float[i] = ((i % 2) ? -1 : 1)
                      * bior_float[N - 1][M_idx+1][w->dec_len-1-i];
                    w->dec_hi_float[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * bior_float[N - 1][0][i+n];
                }
            }

            {
                size_t n = M_max - M;
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_double[i] = bior_double[N - 1][0][i+n];
                    w->dec_lo_double[i] = bior_double[N - 1][M_idx+1][w->dec_len-1-i];
                    w->rec_hi_double[i] = ((i % 2) ? -1 : 1)
                      * bior_double[N - 1][M_idx+1][w->dec_len-1-i];
                    w->dec_hi_double[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * bior_double[N - 1][0][i+n];
                }
            }

            break;
        }

        /* Discrete FIR filter approximation of Meyer wavelet */
        case 'm':
        case 'M':
            w = blank_wavelet(62);
            if(w == NULL) return NULL;

            w->vanishing_moments_psi = -1;
            w->vanishing_moments_phi = -1;
            w->support_width = -1;
            w->orthogonal = 1;
            w->biorthogonal = 1;
            w->symmetry = SYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Discrete Meyer (FIR Approximation)";
            w->short_name = "dmey";

            {
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_float[i] = dmey_float[i];
                    w->dec_lo_float[i] = dmey_float[w->dec_len-1-i];
                    w->rec_hi_float[i] = ((i % 2) ? -1 : 1)
                      * dmey_float[w->dec_len-1-i];
                    w->dec_hi_float[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * dmey_float[i];
                }
            }

            {
                size_t i;
                for(i = 0; i < w->rec_len; ++i){
                    w->rec_lo_double[i] = dmey_double[i];
                    w->dec_lo_double[i] = dmey_double[w->dec_len-1-i];
                    w->rec_hi_double[i] = ((i % 2) ? -1 : 1)
                      * dmey_double[w->dec_len-1-i];
                    w->dec_hi_double[i] = (((w->dec_len-1-i) % 2) ? -1 : 1)
                      * dmey_double[i];
                }
            }
            break;

        default:
            return NULL;
    }
    return w;
}


Wavelet* blank_wavelet(size_t filters_length)
{
    Wavelet* w;

    if(filters_length < 1)
        return NULL;

    /* pad to even length */
    if(filters_length % 2)
        ++filters_length;

    w = wtmalloc(sizeof(Wavelet));
    if(w == NULL) return NULL;

    w->dec_len = w->rec_len = filters_length;

    w->dec_lo_float = wtcalloc(filters_length, sizeof(float));
    w->dec_hi_float = wtcalloc(filters_length, sizeof(float));
    w->rec_lo_float = wtcalloc(filters_length, sizeof(float));
    w->rec_hi_float = wtcalloc(filters_length, sizeof(float));

    w->dec_lo_double = wtcalloc(filters_length, sizeof(double));
    w->dec_hi_double = wtcalloc(filters_length, sizeof(double));
    w->rec_lo_double = wtcalloc(filters_length, sizeof(double));
    w->rec_hi_double = wtcalloc(filters_length, sizeof(double));

    if(w->dec_lo_float == NULL || w->dec_hi_float == NULL ||
       w->rec_lo_float == NULL || w->rec_hi_float == NULL ||
       w->dec_lo_double == NULL || w->dec_hi_double == NULL ||
       w->rec_lo_double == NULL || w->rec_hi_double == NULL){
        free_wavelet(w);
        return NULL;
    }

    /* set properties to "blank" values */
    w->vanishing_moments_psi = 0;
    w->vanishing_moments_phi = 0;
    w->support_width = -1;
    w->orthogonal = 0;
    w->biorthogonal = 0;
    w->symmetry = UNKNOWN;
    w->compact_support = 0;
    w->family_name = "";
    w->short_name = "";

    return w;
}


Wavelet* copy_wavelet(Wavelet* base)
{
    Wavelet* w;

    if(base == NULL) return NULL;

    if(base->dec_len < 1 || base->rec_len < 1)
        return NULL;

    w = wtmalloc(sizeof(Wavelet));
    if(w == NULL) return NULL;

    memcpy(w, base, sizeof(Wavelet));

    w->dec_lo_float = wtmalloc(w->dec_len * sizeof(float));
    w->dec_hi_float = wtmalloc(w->dec_len * sizeof(float));
    w->rec_lo_float = wtmalloc(w->rec_len * sizeof(float));
    w->rec_hi_float = wtmalloc(w->rec_len * sizeof(float));
    w->dec_lo_double = wtmalloc(w->dec_len * sizeof(double));
    w->dec_hi_double = wtmalloc(w->dec_len * sizeof(double));
    w->rec_lo_double = wtmalloc(w->rec_len * sizeof(double));
    w->rec_hi_double = wtmalloc(w->rec_len * sizeof(double));

    if(w->dec_lo_float == NULL || w->dec_hi_float == NULL ||
       w->rec_lo_float == NULL || w->rec_hi_float == NULL ||
       w->dec_lo_double == NULL || w->dec_hi_double == NULL ||
       w->rec_lo_double == NULL || w->rec_hi_double == NULL){
      free_wavelet(w);
      return NULL;
    }

    // FIXME: Test coverage, the only use in `wavelet` overwrites the filter
    memcpy(w->dec_lo_float, base->dec_lo_float, w->dec_len * sizeof(float));
    memcpy(w->dec_hi_float, base->dec_hi_float, w->dec_len * sizeof(float));
    memcpy(w->rec_lo_float, base->rec_lo_float, w->rec_len * sizeof(float));
    memcpy(w->rec_hi_float, base->rec_hi_float, w->rec_len * sizeof(float));
    memcpy(w->dec_lo_double, base->dec_lo_double, w->dec_len * sizeof(double));
    memcpy(w->dec_hi_double, base->dec_hi_double, w->dec_len * sizeof(double));
    memcpy(w->rec_lo_double, base->rec_lo_double, w->rec_len * sizeof(double));
    memcpy(w->rec_hi_double, base->rec_hi_double, w->rec_len * sizeof(double));

    return w;
}

void free_wavelet(Wavelet *w){

    /* deallocate filters */
    wtfree(w->dec_lo_float);
    wtfree(w->dec_hi_float);
    wtfree(w->rec_lo_float);
    wtfree(w->rec_hi_float);

    wtfree(w->dec_lo_double);
    wtfree(w->dec_hi_double);
    wtfree(w->rec_lo_double);
    wtfree(w->rec_hi_double);

    /* finally free struct */
    wtfree(w);
}

#undef SWAP
