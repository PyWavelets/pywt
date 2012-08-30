// Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
// See COPYING for license details.

// Allocating, setting properties and destroying wavelet structs
#include "wavelets.h"
#include "wavelets_coeffs.h"

Wavelet* wavelet(char name, int order)
{
    Wavelet *w, *wtmp;
    index_t i;

    // Haar wavelet
    if(name == 'h' || name == 'H'){

        // the same as db1
        w = wavelet('d', 1);
        w->family_name = "Haar";
        w->short_name = "haar";
        return w;

    // Reverse biorthogonal wavelets family
    } else if (name == 'r' || name == 'R') { 

        // rbio is like bior, only with switched filters
        wtmp = wavelet('b', order);
        w = copy_wavelet(wtmp);
        
        if(w == NULL)
            return NULL;
        
        w->dec_len = wtmp->rec_len;
        w->rec_len = wtmp->dec_len;

        /*
        w->dec_hi_offset = wtmp->rec_hi_offset;
        w->rec_hi_offset = wtmp->dec_hi_offset;
        w->dec_lo_offset = wtmp->rec_lo_offset;
        w->rec_lo_offset = wtmp->dec_lo_offset;
        */
        for(i = 0; i < w->rec_len; ++i){
            //## FOR $DTYPE$ IN (double, float):
                w->rec_lo_$DTYPE$[i] = wtmp->dec_lo_$DTYPE$[wtmp->dec_len-1-i];
                w->rec_hi_$DTYPE$[i] = wtmp->dec_hi_$DTYPE$[wtmp->dec_len-1-i];
            //## ENDFOR $DTYPE$
        }

        for(i = 0; i < w->dec_len; ++i){
            //## FOR $DTYPE$ IN (double, float):
                w->dec_hi_$DTYPE$[i] = wtmp->rec_hi_$DTYPE$[wtmp->rec_len-1-i];
                w->dec_lo_$DTYPE$[i] = wtmp->rec_lo_$DTYPE$[wtmp->rec_len-1-i];
            //## ENDFOR $DTYPE$
        }

        w->vanishing_moments_psi = order / 10; // 1st digit
        w->vanishing_moments_phi = -1;

        w->family_name = "Reverse biorthogonal";
        w->short_name = "rbio";

        free_wavelet(wtmp);
        
        return w;
    }

    w = wtmalloc(sizeof(Wavelet));
    if(w == NULL)
        return NULL;

    //w->dec_lo_offset = w->rec_lo_offset = 0;
    //w->dec_hi_offset = w->rec_hi_offset = 0;
    w->_builtin = 1;

    switch(name){

        // Daubechies wavelets family
        case 'd':
        case 'D':
            w->dec_len = w->rec_len = 2*order;

            w->vanishing_moments_psi = order;
            w->vanishing_moments_phi = 0;
            w->support_width = 2*order - 1;
            w->orthogonal = 1;
            w->biorthogonal = 1;
            w->symmetry = ASYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Daubechies";
            w->short_name = "db";

            switch (order) {
                //## FOR $ORDER$ IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20):
                case $ORDER$:
                    //## FOR $DTYPE$ IN (double, float):
                    w->dec_lo_$DTYPE$ = db$ORDER$_$DTYPE$[0];
                    w->dec_hi_$DTYPE$ = db$ORDER$_$DTYPE$[1];
                    w->rec_lo_$DTYPE$ = db$ORDER$_$DTYPE$[2];
                    w->rec_hi_$DTYPE$ = db$ORDER$_$DTYPE$[3];
                    //## ENDFOR $DTYPE$
                    break;
                //## ENDFOR $ORDER$
            
                default:
                    wtfree(w);
                    return NULL;
            }
            break;

        // Symlets wavelets family
        case 's':
        case 'S':
            w->dec_len = w->rec_len = order << 1;

            w->vanishing_moments_psi = order;
            w->vanishing_moments_phi = 0;
            w->support_width = 2*order - 1;
            w->orthogonal = 1;
            w->biorthogonal = 1;
            w->symmetry = NEAR_SYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Symlets";
            w->short_name = "sym";

            switch (order) {
                //## FOR $ORDER$ IN (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20):
                case $ORDER$:
                   //## FOR $DTYPE$ IN (double, float):
                    w->dec_lo_$DTYPE$ = sym$ORDER$_$DTYPE$[0];
                    w->dec_hi_$DTYPE$ = sym$ORDER$_$DTYPE$[1];
                    w->rec_lo_$DTYPE$ = sym$ORDER$_$DTYPE$[2];
                    w->rec_hi_$DTYPE$ = sym$ORDER$_$DTYPE$[3];
                    //## ENDFOR $DTYPE$
                    break;
                //## ENDFOR $ORDER$
            
                default:
                    wtfree(w);
                    return NULL;
            }
            break;

        // Coiflets wavelets family
        case 'c':
        case 'C':
            w->dec_len = w->rec_len = order * 6;

            w->vanishing_moments_psi = 2*order;
            w->vanishing_moments_phi = 2*order -1;
            w->support_width = 6*order - 1;
            w->orthogonal = 1;
            w->biorthogonal = 1;
            w->symmetry = NEAR_SYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Coiflets";
            w->short_name = "coif";

            switch (order) {
                //## FOR $ORDER$ IN (1, 2, 3, 4, 5):
                case $ORDER$:
                    //## FOR $DTYPE$ IN (double, float):
                    w->dec_lo_$DTYPE$ = coif$ORDER$_$DTYPE$[0];
                    w->dec_hi_$DTYPE$ = coif$ORDER$_$DTYPE$[1];
                    w->rec_lo_$DTYPE$ = coif$ORDER$_$DTYPE$[2];
                    w->rec_hi_$DTYPE$ = coif$ORDER$_$DTYPE$[3];
                    //## ENDFOR $DTYPE$
                    break;
                //## ENDFOR $ORDER$
            
                default:
                    wtfree(w);
                    return NULL;
            }
            break;

        // Biorthogonal wavelets family
        case 'b':
        case 'B':

            w->vanishing_moments_psi = order/10;
            w->vanishing_moments_phi = -1;
            w->support_width = -1;
            w->orthogonal = 0;
            w->biorthogonal = 1;
            w->symmetry = SYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Biorthogonal";
            w->short_name = "bior";

                switch (order) {
                    //## FOR $M$ IN (1, 3, 5):
                        case 1$M$:
                            //## FOR $DTYPE$ IN (double, float):
                                w->dec_lo_$DTYPE$ = bior1_$M$_$DTYPE$[0];
                                w->dec_hi_$DTYPE$ = bior1_$M$_$DTYPE$[1];
                                w->rec_lo_$DTYPE$ = bior1_$M$_$DTYPE$[2];
                                w->rec_hi_$DTYPE$ = bior1_$M$_$DTYPE$[3];
                            //## ENDFOR $DTYPE$
                            w->dec_len = w->rec_len = 2 * $M$;
                            break;
                    //## ENDFOR $M$

                    //## FOR $M$ IN (2, 4, 6, 8):
                        case 2$M$:
                            //## FOR $DTYPE$ IN (double, float):
                                w->dec_lo_$DTYPE$ = bior2_$M$_$DTYPE$[0];
                                w->dec_hi_$DTYPE$ = bior2_$M$_$DTYPE$[1];
                                w->rec_lo_$DTYPE$ = bior2_$M$_$DTYPE$[2];
                                w->rec_hi_$DTYPE$ = bior2_$M$_$DTYPE$[3];
                            //## ENDFOR $DTYPE$
                            w->dec_len = w->rec_len = 2 * $M$ + 2;
                            break;
                    //## ENDFOR $M$

                    //## FOR $M$ IN (1, 3, 5, 7, 9):
                        case 3$M$:
                            //## FOR $DTYPE$ IN (double, float):
                                w->dec_lo_$DTYPE$ = bior3_$M$_$DTYPE$[0];
                                w->dec_hi_$DTYPE$ = bior3_$M$_$DTYPE$[1];
                                w->rec_lo_$DTYPE$ = bior3_$M$_$DTYPE$[2];
                                w->rec_hi_$DTYPE$ = bior3_$M$_$DTYPE$[3];
                            //## ENDFOR $DTYPE$
                            w->dec_len = w->rec_len = 2 * $M$ + 2;
                            break;
                    //## ENDFOR $M$

                    //## FOR $M$ IN (4,):
                        case 4$M$:
                            //## FOR $DTYPE$ IN (double, float):
                                w->dec_lo_$DTYPE$ = bior4_$M$_$DTYPE$[0];
                                w->dec_hi_$DTYPE$ = bior4_$M$_$DTYPE$[1];
                                w->rec_lo_$DTYPE$ = bior4_$M$_$DTYPE$[2];
                                w->rec_hi_$DTYPE$ = bior4_$M$_$DTYPE$[3];
                            //## ENDFOR $DTYPE$
                            w->dec_len = w->rec_len = 2 * $M$ + 2;
                            break;
                    //## ENDFOR $M$

                    //## FOR $M$ IN (5,):
                        case 5$M$:
                            //## FOR $DTYPE$ IN (double, float):
                                w->dec_lo_$DTYPE$ = bior5_$M$_$DTYPE$[0];
                                w->dec_hi_$DTYPE$ = bior5_$M$_$DTYPE$[1];
                                w->rec_lo_$DTYPE$ = bior5_$M$_$DTYPE$[2];
                                w->rec_hi_$DTYPE$ = bior5_$M$_$DTYPE$[3];
                            //## ENDFOR $DTYPE$
                            w->dec_len = w->rec_len = 2 * $M$ + 2;
                            break;
                    //## ENDFOR $M$

                    //## FOR $M$ IN (8,):
                        case 6$M$:
                            //## FOR $DTYPE$ IN (double, float):
                                w->dec_lo_$DTYPE$ = bior6_$M$_$DTYPE$[0];
                                w->dec_hi_$DTYPE$ = bior6_$M$_$DTYPE$[1];
                                w->rec_lo_$DTYPE$ = bior6_$M$_$DTYPE$[2];
                                w->rec_hi_$DTYPE$ = bior6_$M$_$DTYPE$[3];
                            //## ENDFOR $DTYPE$
                            w->dec_len = w->rec_len = 2 * $M$ + 2;
                            break;
                    //## ENDFOR $M$

                    default:
                        wtfree(w);
                        return NULL;
                }
            //## ENDFOR $DTYPE$
            break;

        // Discrete FIR filter approximation of Meyer wavelet
        case 'm':
        case 'M':

            w->vanishing_moments_psi = -1;
            w->vanishing_moments_phi = -1;
            w->support_width = -1;
            w->orthogonal = 1;
            w->biorthogonal = 1;
            w->symmetry = SYMMETRIC;
            w->compact_support = 1;
            w->family_name = "Discrete Meyer (FIR Approximation)";
            w->short_name = "dmey";

            //## FOR $DTYPE$ IN (double, float):
                w->dec_lo_$DTYPE$ = dmey_$DTYPE$[0];
                w->dec_hi_$DTYPE$ = dmey_$DTYPE$[1];
                w->rec_lo_$DTYPE$ = dmey_$DTYPE$[2];
                w->rec_hi_$DTYPE$ = dmey_$DTYPE$[3];
            //## ENDFOR $DTYPE$
            w->dec_len = w->rec_len = 62;
            return w;
            break;

        default:
            wtfree(w);
            return NULL;
    }
    return w;
}


Wavelet* blank_wavelet(index_t filters_length)
{
    Wavelet* w;

    if(filters_length < 1)
        return NULL;

    // pad to even length
    if(filters_length % 2)
        ++filters_length;

    w = wtmalloc(sizeof(Wavelet));
    if(w == NULL) return NULL;

    //w->dec_lo_offset = w->rec_lo_offset = 0;
    //w->dec_hi_offset = w->rec_hi_offset = 0;

    // Important!
    // Otherwise filters arrays allocated here won't be deallocated by free_wavelet
    w->_builtin = 0;

    w->dec_len = w->rec_len = filters_length;

    //## FOR $DTYPE$ IN (double, float):
        w->dec_lo_$DTYPE$ = wtcalloc(filters_length, sizeof($DTYPE$));
        w->dec_hi_$DTYPE$ = wtcalloc(filters_length, sizeof($DTYPE$));
        w->rec_lo_$DTYPE$ = wtcalloc(filters_length, sizeof($DTYPE$));
        w->rec_hi_$DTYPE$ = wtcalloc(filters_length, sizeof($DTYPE$));

        if(w->dec_lo_$DTYPE$ == NULL || w->dec_hi_$DTYPE$ == NULL || w->rec_lo_$DTYPE$ == NULL || w->rec_hi_$DTYPE$ == NULL){
            free_wavelet(w);
            return NULL;
        }
    //## ENDFOR $DTYPE$

    // set properties to "blank" values
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
    index_t i;

    if(base == NULL) return NULL;

    if(base->dec_len < 1 || base->rec_len < 1)
        return NULL;

    w = wtmalloc(sizeof(Wavelet));
    if(w == NULL) return NULL;

    memcpy(w, base, sizeof(Wavelet));

    w->_builtin = 0;

    //## FOR $DTYPE$ IN (double, float):

        w->dec_lo_$DTYPE$ = wtcalloc(w->dec_len, sizeof($DTYPE$));
        w->dec_hi_$DTYPE$ = wtcalloc(w->dec_len, sizeof($DTYPE$));
        w->rec_lo_$DTYPE$ = wtcalloc(w->rec_len, sizeof($DTYPE$));
        w->rec_hi_$DTYPE$ = wtcalloc(w->rec_len, sizeof($DTYPE$));

        if(w->dec_lo_$DTYPE$ == NULL || w->dec_hi_$DTYPE$ == NULL || w->rec_lo_$DTYPE$ == NULL || w->rec_hi_$DTYPE$ == NULL){
            free_wavelet(w);
            return NULL;
        }

        for(i=0; i< w->dec_len; ++i){
            w->dec_lo_$DTYPE$[i] = base->dec_lo_$DTYPE$[i];
            w->dec_hi_$DTYPE$[i] = base->dec_hi_$DTYPE$[i];
        }

        for(i=0; i< w->rec_len; ++i){
            w->rec_lo_$DTYPE$[i] = base->rec_lo_$DTYPE$[i];
            w->rec_hi_$DTYPE$[i] = base->rec_hi_$DTYPE$[i];
        }

    //## ENDFOR $DTYPE$

    return w;
}

void free_wavelet(Wavelet *w){
    if(wavelet == NULL)
        return;

    if(w->_builtin == 0){

        // deallocate filters
        //## FOR $DTYPE$ IN (double, float):        
            if(w->dec_lo_$DTYPE$ != NULL){
                wtfree(w->dec_lo_$DTYPE$);
                w->dec_lo_$DTYPE$ = NULL;
            }

            if(w->dec_hi_$DTYPE$ != NULL){
                wtfree(w->dec_hi_$DTYPE$);
                w->dec_hi_$DTYPE$ = NULL;
            }

            if(w->rec_lo_$DTYPE$ != NULL){
                wtfree(w->rec_lo_$DTYPE$);
                w->rec_lo_$DTYPE$ = NULL;
            }

            if(w->rec_hi_$DTYPE$ != NULL){
                wtfree(w->rec_hi_$DTYPE$);
                w->rec_hi_$DTYPE$ = NULL;
            }
        //## ENDFOR $DTYPE$
    }

    // finally free struct
    wtfree(w);
}
