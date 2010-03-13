// Copyright (c) 2006-2010 Filip Wasilewski <http://filipwasilewski.pl/>
// See COPYING for license details.

// $Id$

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
                w->rec_lo_double[i] = wtmp->dec_lo_double[wtmp->dec_len-1-i];
                w->rec_hi_double[i] = wtmp->dec_hi_double[wtmp->dec_len-1-i];
                w->rec_lo_float[i] = wtmp->dec_lo_float[wtmp->dec_len-1-i];
                w->rec_hi_float[i] = wtmp->dec_hi_float[wtmp->dec_len-1-i];
        }

        for(i = 0; i < w->dec_len; ++i){
                w->dec_hi_double[i] = wtmp->rec_hi_double[wtmp->rec_len-1-i];
                w->dec_lo_double[i] = wtmp->rec_lo_double[wtmp->rec_len-1-i];
                w->dec_hi_float[i] = wtmp->rec_hi_float[wtmp->rec_len-1-i];
                w->dec_lo_float[i] = wtmp->rec_lo_float[wtmp->rec_len-1-i];
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
                case 1:
                    w->dec_lo_double = db1_double[0];
                    w->dec_hi_double = db1_double[1];
                    w->rec_lo_double = db1_double[2];
                    w->rec_hi_double = db1_double[3];
                    w->dec_lo_float = db1_float[0];
                    w->dec_hi_float = db1_float[1];
                    w->rec_lo_float = db1_float[2];
                    w->rec_hi_float = db1_float[3];
                    break;
                case 2:
                    w->dec_lo_double = db2_double[0];
                    w->dec_hi_double = db2_double[1];
                    w->rec_lo_double = db2_double[2];
                    w->rec_hi_double = db2_double[3];
                    w->dec_lo_float = db2_float[0];
                    w->dec_hi_float = db2_float[1];
                    w->rec_lo_float = db2_float[2];
                    w->rec_hi_float = db2_float[3];
                    break;
                case 3:
                    w->dec_lo_double = db3_double[0];
                    w->dec_hi_double = db3_double[1];
                    w->rec_lo_double = db3_double[2];
                    w->rec_hi_double = db3_double[3];
                    w->dec_lo_float = db3_float[0];
                    w->dec_hi_float = db3_float[1];
                    w->rec_lo_float = db3_float[2];
                    w->rec_hi_float = db3_float[3];
                    break;
                case 4:
                    w->dec_lo_double = db4_double[0];
                    w->dec_hi_double = db4_double[1];
                    w->rec_lo_double = db4_double[2];
                    w->rec_hi_double = db4_double[3];
                    w->dec_lo_float = db4_float[0];
                    w->dec_hi_float = db4_float[1];
                    w->rec_lo_float = db4_float[2];
                    w->rec_hi_float = db4_float[3];
                    break;
                case 5:
                    w->dec_lo_double = db5_double[0];
                    w->dec_hi_double = db5_double[1];
                    w->rec_lo_double = db5_double[2];
                    w->rec_hi_double = db5_double[3];
                    w->dec_lo_float = db5_float[0];
                    w->dec_hi_float = db5_float[1];
                    w->rec_lo_float = db5_float[2];
                    w->rec_hi_float = db5_float[3];
                    break;
                case 6:
                    w->dec_lo_double = db6_double[0];
                    w->dec_hi_double = db6_double[1];
                    w->rec_lo_double = db6_double[2];
                    w->rec_hi_double = db6_double[3];
                    w->dec_lo_float = db6_float[0];
                    w->dec_hi_float = db6_float[1];
                    w->rec_lo_float = db6_float[2];
                    w->rec_hi_float = db6_float[3];
                    break;
                case 7:
                    w->dec_lo_double = db7_double[0];
                    w->dec_hi_double = db7_double[1];
                    w->rec_lo_double = db7_double[2];
                    w->rec_hi_double = db7_double[3];
                    w->dec_lo_float = db7_float[0];
                    w->dec_hi_float = db7_float[1];
                    w->rec_lo_float = db7_float[2];
                    w->rec_hi_float = db7_float[3];
                    break;
                case 8:
                    w->dec_lo_double = db8_double[0];
                    w->dec_hi_double = db8_double[1];
                    w->rec_lo_double = db8_double[2];
                    w->rec_hi_double = db8_double[3];
                    w->dec_lo_float = db8_float[0];
                    w->dec_hi_float = db8_float[1];
                    w->rec_lo_float = db8_float[2];
                    w->rec_hi_float = db8_float[3];
                    break;
                case 9:
                    w->dec_lo_double = db9_double[0];
                    w->dec_hi_double = db9_double[1];
                    w->rec_lo_double = db9_double[2];
                    w->rec_hi_double = db9_double[3];
                    w->dec_lo_float = db9_float[0];
                    w->dec_hi_float = db9_float[1];
                    w->rec_lo_float = db9_float[2];
                    w->rec_hi_float = db9_float[3];
                    break;
                case 10:
                    w->dec_lo_double = db10_double[0];
                    w->dec_hi_double = db10_double[1];
                    w->rec_lo_double = db10_double[2];
                    w->rec_hi_double = db10_double[3];
                    w->dec_lo_float = db10_float[0];
                    w->dec_hi_float = db10_float[1];
                    w->rec_lo_float = db10_float[2];
                    w->rec_hi_float = db10_float[3];
                    break;
                case 11:
                    w->dec_lo_double = db11_double[0];
                    w->dec_hi_double = db11_double[1];
                    w->rec_lo_double = db11_double[2];
                    w->rec_hi_double = db11_double[3];
                    w->dec_lo_float = db11_float[0];
                    w->dec_hi_float = db11_float[1];
                    w->rec_lo_float = db11_float[2];
                    w->rec_hi_float = db11_float[3];
                    break;
                case 12:
                    w->dec_lo_double = db12_double[0];
                    w->dec_hi_double = db12_double[1];
                    w->rec_lo_double = db12_double[2];
                    w->rec_hi_double = db12_double[3];
                    w->dec_lo_float = db12_float[0];
                    w->dec_hi_float = db12_float[1];
                    w->rec_lo_float = db12_float[2];
                    w->rec_hi_float = db12_float[3];
                    break;
                case 13:
                    w->dec_lo_double = db13_double[0];
                    w->dec_hi_double = db13_double[1];
                    w->rec_lo_double = db13_double[2];
                    w->rec_hi_double = db13_double[3];
                    w->dec_lo_float = db13_float[0];
                    w->dec_hi_float = db13_float[1];
                    w->rec_lo_float = db13_float[2];
                    w->rec_hi_float = db13_float[3];
                    break;
                case 14:
                    w->dec_lo_double = db14_double[0];
                    w->dec_hi_double = db14_double[1];
                    w->rec_lo_double = db14_double[2];
                    w->rec_hi_double = db14_double[3];
                    w->dec_lo_float = db14_float[0];
                    w->dec_hi_float = db14_float[1];
                    w->rec_lo_float = db14_float[2];
                    w->rec_hi_float = db14_float[3];
                    break;
                case 15:
                    w->dec_lo_double = db15_double[0];
                    w->dec_hi_double = db15_double[1];
                    w->rec_lo_double = db15_double[2];
                    w->rec_hi_double = db15_double[3];
                    w->dec_lo_float = db15_float[0];
                    w->dec_hi_float = db15_float[1];
                    w->rec_lo_float = db15_float[2];
                    w->rec_hi_float = db15_float[3];
                    break;
                case 16:
                    w->dec_lo_double = db16_double[0];
                    w->dec_hi_double = db16_double[1];
                    w->rec_lo_double = db16_double[2];
                    w->rec_hi_double = db16_double[3];
                    w->dec_lo_float = db16_float[0];
                    w->dec_hi_float = db16_float[1];
                    w->rec_lo_float = db16_float[2];
                    w->rec_hi_float = db16_float[3];
                    break;
                case 17:
                    w->dec_lo_double = db17_double[0];
                    w->dec_hi_double = db17_double[1];
                    w->rec_lo_double = db17_double[2];
                    w->rec_hi_double = db17_double[3];
                    w->dec_lo_float = db17_float[0];
                    w->dec_hi_float = db17_float[1];
                    w->rec_lo_float = db17_float[2];
                    w->rec_hi_float = db17_float[3];
                    break;
                case 18:
                    w->dec_lo_double = db18_double[0];
                    w->dec_hi_double = db18_double[1];
                    w->rec_lo_double = db18_double[2];
                    w->rec_hi_double = db18_double[3];
                    w->dec_lo_float = db18_float[0];
                    w->dec_hi_float = db18_float[1];
                    w->rec_lo_float = db18_float[2];
                    w->rec_hi_float = db18_float[3];
                    break;
                case 19:
                    w->dec_lo_double = db19_double[0];
                    w->dec_hi_double = db19_double[1];
                    w->rec_lo_double = db19_double[2];
                    w->rec_hi_double = db19_double[3];
                    w->dec_lo_float = db19_float[0];
                    w->dec_hi_float = db19_float[1];
                    w->rec_lo_float = db19_float[2];
                    w->rec_hi_float = db19_float[3];
                    break;
                case 20:
                    w->dec_lo_double = db20_double[0];
                    w->dec_hi_double = db20_double[1];
                    w->rec_lo_double = db20_double[2];
                    w->rec_hi_double = db20_double[3];
                    w->dec_lo_float = db20_float[0];
                    w->dec_hi_float = db20_float[1];
                    w->rec_lo_float = db20_float[2];
                    w->rec_hi_float = db20_float[3];
                    break;
            
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
                case 2:
                    w->dec_lo_double = sym2_double[0];
                    w->dec_hi_double = sym2_double[1];
                    w->rec_lo_double = sym2_double[2];
                    w->rec_hi_double = sym2_double[3];
                    w->dec_lo_float = sym2_float[0];
                    w->dec_hi_float = sym2_float[1];
                    w->rec_lo_float = sym2_float[2];
                    w->rec_hi_float = sym2_float[3];
                    break;
                case 3:
                    w->dec_lo_double = sym3_double[0];
                    w->dec_hi_double = sym3_double[1];
                    w->rec_lo_double = sym3_double[2];
                    w->rec_hi_double = sym3_double[3];
                    w->dec_lo_float = sym3_float[0];
                    w->dec_hi_float = sym3_float[1];
                    w->rec_lo_float = sym3_float[2];
                    w->rec_hi_float = sym3_float[3];
                    break;
                case 4:
                    w->dec_lo_double = sym4_double[0];
                    w->dec_hi_double = sym4_double[1];
                    w->rec_lo_double = sym4_double[2];
                    w->rec_hi_double = sym4_double[3];
                    w->dec_lo_float = sym4_float[0];
                    w->dec_hi_float = sym4_float[1];
                    w->rec_lo_float = sym4_float[2];
                    w->rec_hi_float = sym4_float[3];
                    break;
                case 5:
                    w->dec_lo_double = sym5_double[0];
                    w->dec_hi_double = sym5_double[1];
                    w->rec_lo_double = sym5_double[2];
                    w->rec_hi_double = sym5_double[3];
                    w->dec_lo_float = sym5_float[0];
                    w->dec_hi_float = sym5_float[1];
                    w->rec_lo_float = sym5_float[2];
                    w->rec_hi_float = sym5_float[3];
                    break;
                case 6:
                    w->dec_lo_double = sym6_double[0];
                    w->dec_hi_double = sym6_double[1];
                    w->rec_lo_double = sym6_double[2];
                    w->rec_hi_double = sym6_double[3];
                    w->dec_lo_float = sym6_float[0];
                    w->dec_hi_float = sym6_float[1];
                    w->rec_lo_float = sym6_float[2];
                    w->rec_hi_float = sym6_float[3];
                    break;
                case 7:
                    w->dec_lo_double = sym7_double[0];
                    w->dec_hi_double = sym7_double[1];
                    w->rec_lo_double = sym7_double[2];
                    w->rec_hi_double = sym7_double[3];
                    w->dec_lo_float = sym7_float[0];
                    w->dec_hi_float = sym7_float[1];
                    w->rec_lo_float = sym7_float[2];
                    w->rec_hi_float = sym7_float[3];
                    break;
                case 8:
                    w->dec_lo_double = sym8_double[0];
                    w->dec_hi_double = sym8_double[1];
                    w->rec_lo_double = sym8_double[2];
                    w->rec_hi_double = sym8_double[3];
                    w->dec_lo_float = sym8_float[0];
                    w->dec_hi_float = sym8_float[1];
                    w->rec_lo_float = sym8_float[2];
                    w->rec_hi_float = sym8_float[3];
                    break;
                case 9:
                    w->dec_lo_double = sym9_double[0];
                    w->dec_hi_double = sym9_double[1];
                    w->rec_lo_double = sym9_double[2];
                    w->rec_hi_double = sym9_double[3];
                    w->dec_lo_float = sym9_float[0];
                    w->dec_hi_float = sym9_float[1];
                    w->rec_lo_float = sym9_float[2];
                    w->rec_hi_float = sym9_float[3];
                    break;
                case 10:
                    w->dec_lo_double = sym10_double[0];
                    w->dec_hi_double = sym10_double[1];
                    w->rec_lo_double = sym10_double[2];
                    w->rec_hi_double = sym10_double[3];
                    w->dec_lo_float = sym10_float[0];
                    w->dec_hi_float = sym10_float[1];
                    w->rec_lo_float = sym10_float[2];
                    w->rec_hi_float = sym10_float[3];
                    break;
                case 11:
                    w->dec_lo_double = sym11_double[0];
                    w->dec_hi_double = sym11_double[1];
                    w->rec_lo_double = sym11_double[2];
                    w->rec_hi_double = sym11_double[3];
                    w->dec_lo_float = sym11_float[0];
                    w->dec_hi_float = sym11_float[1];
                    w->rec_lo_float = sym11_float[2];
                    w->rec_hi_float = sym11_float[3];
                    break;
                case 12:
                    w->dec_lo_double = sym12_double[0];
                    w->dec_hi_double = sym12_double[1];
                    w->rec_lo_double = sym12_double[2];
                    w->rec_hi_double = sym12_double[3];
                    w->dec_lo_float = sym12_float[0];
                    w->dec_hi_float = sym12_float[1];
                    w->rec_lo_float = sym12_float[2];
                    w->rec_hi_float = sym12_float[3];
                    break;
                case 13:
                    w->dec_lo_double = sym13_double[0];
                    w->dec_hi_double = sym13_double[1];
                    w->rec_lo_double = sym13_double[2];
                    w->rec_hi_double = sym13_double[3];
                    w->dec_lo_float = sym13_float[0];
                    w->dec_hi_float = sym13_float[1];
                    w->rec_lo_float = sym13_float[2];
                    w->rec_hi_float = sym13_float[3];
                    break;
                case 14:
                    w->dec_lo_double = sym14_double[0];
                    w->dec_hi_double = sym14_double[1];
                    w->rec_lo_double = sym14_double[2];
                    w->rec_hi_double = sym14_double[3];
                    w->dec_lo_float = sym14_float[0];
                    w->dec_hi_float = sym14_float[1];
                    w->rec_lo_float = sym14_float[2];
                    w->rec_hi_float = sym14_float[3];
                    break;
                case 15:
                    w->dec_lo_double = sym15_double[0];
                    w->dec_hi_double = sym15_double[1];
                    w->rec_lo_double = sym15_double[2];
                    w->rec_hi_double = sym15_double[3];
                    w->dec_lo_float = sym15_float[0];
                    w->dec_hi_float = sym15_float[1];
                    w->rec_lo_float = sym15_float[2];
                    w->rec_hi_float = sym15_float[3];
                    break;
                case 16:
                    w->dec_lo_double = sym16_double[0];
                    w->dec_hi_double = sym16_double[1];
                    w->rec_lo_double = sym16_double[2];
                    w->rec_hi_double = sym16_double[3];
                    w->dec_lo_float = sym16_float[0];
                    w->dec_hi_float = sym16_float[1];
                    w->rec_lo_float = sym16_float[2];
                    w->rec_hi_float = sym16_float[3];
                    break;
                case 17:
                    w->dec_lo_double = sym17_double[0];
                    w->dec_hi_double = sym17_double[1];
                    w->rec_lo_double = sym17_double[2];
                    w->rec_hi_double = sym17_double[3];
                    w->dec_lo_float = sym17_float[0];
                    w->dec_hi_float = sym17_float[1];
                    w->rec_lo_float = sym17_float[2];
                    w->rec_hi_float = sym17_float[3];
                    break;
                case 18:
                    w->dec_lo_double = sym18_double[0];
                    w->dec_hi_double = sym18_double[1];
                    w->rec_lo_double = sym18_double[2];
                    w->rec_hi_double = sym18_double[3];
                    w->dec_lo_float = sym18_float[0];
                    w->dec_hi_float = sym18_float[1];
                    w->rec_lo_float = sym18_float[2];
                    w->rec_hi_float = sym18_float[3];
                    break;
                case 19:
                    w->dec_lo_double = sym19_double[0];
                    w->dec_hi_double = sym19_double[1];
                    w->rec_lo_double = sym19_double[2];
                    w->rec_hi_double = sym19_double[3];
                    w->dec_lo_float = sym19_float[0];
                    w->dec_hi_float = sym19_float[1];
                    w->rec_lo_float = sym19_float[2];
                    w->rec_hi_float = sym19_float[3];
                    break;
                case 20:
                    w->dec_lo_double = sym20_double[0];
                    w->dec_hi_double = sym20_double[1];
                    w->rec_lo_double = sym20_double[2];
                    w->rec_hi_double = sym20_double[3];
                    w->dec_lo_float = sym20_float[0];
                    w->dec_hi_float = sym20_float[1];
                    w->rec_lo_float = sym20_float[2];
                    w->rec_hi_float = sym20_float[3];
                    break;
            
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
                case 1:
                    w->dec_lo_double = coif1_double[0];
                    w->dec_hi_double = coif1_double[1];
                    w->rec_lo_double = coif1_double[2];
                    w->rec_hi_double = coif1_double[3];
                    w->dec_lo_float = coif1_float[0];
                    w->dec_hi_float = coif1_float[1];
                    w->rec_lo_float = coif1_float[2];
                    w->rec_hi_float = coif1_float[3];
                    break;
                case 2:
                    w->dec_lo_double = coif2_double[0];
                    w->dec_hi_double = coif2_double[1];
                    w->rec_lo_double = coif2_double[2];
                    w->rec_hi_double = coif2_double[3];
                    w->dec_lo_float = coif2_float[0];
                    w->dec_hi_float = coif2_float[1];
                    w->rec_lo_float = coif2_float[2];
                    w->rec_hi_float = coif2_float[3];
                    break;
                case 3:
                    w->dec_lo_double = coif3_double[0];
                    w->dec_hi_double = coif3_double[1];
                    w->rec_lo_double = coif3_double[2];
                    w->rec_hi_double = coif3_double[3];
                    w->dec_lo_float = coif3_float[0];
                    w->dec_hi_float = coif3_float[1];
                    w->rec_lo_float = coif3_float[2];
                    w->rec_hi_float = coif3_float[3];
                    break;
                case 4:
                    w->dec_lo_double = coif4_double[0];
                    w->dec_hi_double = coif4_double[1];
                    w->rec_lo_double = coif4_double[2];
                    w->rec_hi_double = coif4_double[3];
                    w->dec_lo_float = coif4_float[0];
                    w->dec_hi_float = coif4_float[1];
                    w->rec_lo_float = coif4_float[2];
                    w->rec_hi_float = coif4_float[3];
                    break;
                case 5:
                    w->dec_lo_double = coif5_double[0];
                    w->dec_hi_double = coif5_double[1];
                    w->rec_lo_double = coif5_double[2];
                    w->rec_hi_double = coif5_double[3];
                    w->dec_lo_float = coif5_float[0];
                    w->dec_hi_float = coif5_float[1];
                    w->rec_lo_float = coif5_float[2];
                    w->rec_hi_float = coif5_float[3];
                    break;
            
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
                        case 11:
                                w->dec_lo_double = bior1_1_double[0];
                                w->dec_hi_double = bior1_1_double[1];
                                w->rec_lo_double = bior1_1_double[2];
                                w->rec_hi_double = bior1_1_double[3];
                                w->dec_lo_float = bior1_1_float[0];
                                w->dec_hi_float = bior1_1_float[1];
                                w->rec_lo_float = bior1_1_float[2];
                                w->rec_hi_float = bior1_1_float[3];
                            w->dec_len = w->rec_len = 2 * 1;
                            break;
                        case 13:
                                w->dec_lo_double = bior1_3_double[0];
                                w->dec_hi_double = bior1_3_double[1];
                                w->rec_lo_double = bior1_3_double[2];
                                w->rec_hi_double = bior1_3_double[3];
                                w->dec_lo_float = bior1_3_float[0];
                                w->dec_hi_float = bior1_3_float[1];
                                w->rec_lo_float = bior1_3_float[2];
                                w->rec_hi_float = bior1_3_float[3];
                            w->dec_len = w->rec_len = 2 * 3;
                            break;
                        case 15:
                                w->dec_lo_double = bior1_5_double[0];
                                w->dec_hi_double = bior1_5_double[1];
                                w->rec_lo_double = bior1_5_double[2];
                                w->rec_hi_double = bior1_5_double[3];
                                w->dec_lo_float = bior1_5_float[0];
                                w->dec_hi_float = bior1_5_float[1];
                                w->rec_lo_float = bior1_5_float[2];
                                w->rec_hi_float = bior1_5_float[3];
                            w->dec_len = w->rec_len = 2 * 5;
                            break;
                        case 22:
                                w->dec_lo_double = bior2_2_double[0];
                                w->dec_hi_double = bior2_2_double[1];
                                w->rec_lo_double = bior2_2_double[2];
                                w->rec_hi_double = bior2_2_double[3];
                                w->dec_lo_float = bior2_2_float[0];
                                w->dec_hi_float = bior2_2_float[1];
                                w->rec_lo_float = bior2_2_float[2];
                                w->rec_hi_float = bior2_2_float[3];
                            w->dec_len = w->rec_len = 2 * 2 + 2;
                            break;
                        case 24:
                                w->dec_lo_double = bior2_4_double[0];
                                w->dec_hi_double = bior2_4_double[1];
                                w->rec_lo_double = bior2_4_double[2];
                                w->rec_hi_double = bior2_4_double[3];
                                w->dec_lo_float = bior2_4_float[0];
                                w->dec_hi_float = bior2_4_float[1];
                                w->rec_lo_float = bior2_4_float[2];
                                w->rec_hi_float = bior2_4_float[3];
                            w->dec_len = w->rec_len = 2 * 4 + 2;
                            break;
                        case 26:
                                w->dec_lo_double = bior2_6_double[0];
                                w->dec_hi_double = bior2_6_double[1];
                                w->rec_lo_double = bior2_6_double[2];
                                w->rec_hi_double = bior2_6_double[3];
                                w->dec_lo_float = bior2_6_float[0];
                                w->dec_hi_float = bior2_6_float[1];
                                w->rec_lo_float = bior2_6_float[2];
                                w->rec_hi_float = bior2_6_float[3];
                            w->dec_len = w->rec_len = 2 * 6 + 2;
                            break;
                        case 28:
                                w->dec_lo_double = bior2_8_double[0];
                                w->dec_hi_double = bior2_8_double[1];
                                w->rec_lo_double = bior2_8_double[2];
                                w->rec_hi_double = bior2_8_double[3];
                                w->dec_lo_float = bior2_8_float[0];
                                w->dec_hi_float = bior2_8_float[1];
                                w->rec_lo_float = bior2_8_float[2];
                                w->rec_hi_float = bior2_8_float[3];
                            w->dec_len = w->rec_len = 2 * 8 + 2;
                            break;
                        case 31:
                                w->dec_lo_double = bior3_1_double[0];
                                w->dec_hi_double = bior3_1_double[1];
                                w->rec_lo_double = bior3_1_double[2];
                                w->rec_hi_double = bior3_1_double[3];
                                w->dec_lo_float = bior3_1_float[0];
                                w->dec_hi_float = bior3_1_float[1];
                                w->rec_lo_float = bior3_1_float[2];
                                w->rec_hi_float = bior3_1_float[3];
                            w->dec_len = w->rec_len = 2 * 1 + 2;
                            break;
                        case 33:
                                w->dec_lo_double = bior3_3_double[0];
                                w->dec_hi_double = bior3_3_double[1];
                                w->rec_lo_double = bior3_3_double[2];
                                w->rec_hi_double = bior3_3_double[3];
                                w->dec_lo_float = bior3_3_float[0];
                                w->dec_hi_float = bior3_3_float[1];
                                w->rec_lo_float = bior3_3_float[2];
                                w->rec_hi_float = bior3_3_float[3];
                            w->dec_len = w->rec_len = 2 * 3 + 2;
                            break;
                        case 35:
                                w->dec_lo_double = bior3_5_double[0];
                                w->dec_hi_double = bior3_5_double[1];
                                w->rec_lo_double = bior3_5_double[2];
                                w->rec_hi_double = bior3_5_double[3];
                                w->dec_lo_float = bior3_5_float[0];
                                w->dec_hi_float = bior3_5_float[1];
                                w->rec_lo_float = bior3_5_float[2];
                                w->rec_hi_float = bior3_5_float[3];
                            w->dec_len = w->rec_len = 2 * 5 + 2;
                            break;
                        case 37:
                                w->dec_lo_double = bior3_7_double[0];
                                w->dec_hi_double = bior3_7_double[1];
                                w->rec_lo_double = bior3_7_double[2];
                                w->rec_hi_double = bior3_7_double[3];
                                w->dec_lo_float = bior3_7_float[0];
                                w->dec_hi_float = bior3_7_float[1];
                                w->rec_lo_float = bior3_7_float[2];
                                w->rec_hi_float = bior3_7_float[3];
                            w->dec_len = w->rec_len = 2 * 7 + 2;
                            break;
                        case 39:
                                w->dec_lo_double = bior3_9_double[0];
                                w->dec_hi_double = bior3_9_double[1];
                                w->rec_lo_double = bior3_9_double[2];
                                w->rec_hi_double = bior3_9_double[3];
                                w->dec_lo_float = bior3_9_float[0];
                                w->dec_hi_float = bior3_9_float[1];
                                w->rec_lo_float = bior3_9_float[2];
                                w->rec_hi_float = bior3_9_float[3];
                            w->dec_len = w->rec_len = 2 * 9 + 2;
                            break;
                        case 44:
                                w->dec_lo_double = bior4_4_double[0];
                                w->dec_hi_double = bior4_4_double[1];
                                w->rec_lo_double = bior4_4_double[2];
                                w->rec_hi_double = bior4_4_double[3];
                                w->dec_lo_float = bior4_4_float[0];
                                w->dec_hi_float = bior4_4_float[1];
                                w->rec_lo_float = bior4_4_float[2];
                                w->rec_hi_float = bior4_4_float[3];
                            w->dec_len = w->rec_len = 2 * 4 + 2;
                            break;
                        case 55:
                                w->dec_lo_double = bior5_5_double[0];
                                w->dec_hi_double = bior5_5_double[1];
                                w->rec_lo_double = bior5_5_double[2];
                                w->rec_hi_double = bior5_5_double[3];
                                w->dec_lo_float = bior5_5_float[0];
                                w->dec_hi_float = bior5_5_float[1];
                                w->rec_lo_float = bior5_5_float[2];
                                w->rec_hi_float = bior5_5_float[3];
                            w->dec_len = w->rec_len = 2 * 5 + 2;
                            break;
                        case 68:
                                w->dec_lo_double = bior6_8_double[0];
                                w->dec_hi_double = bior6_8_double[1];
                                w->rec_lo_double = bior6_8_double[2];
                                w->rec_hi_double = bior6_8_double[3];
                                w->dec_lo_float = bior6_8_float[0];
                                w->dec_hi_float = bior6_8_float[1];
                                w->rec_lo_float = bior6_8_float[2];
                                w->rec_hi_float = bior6_8_float[3];
                            w->dec_len = w->rec_len = 2 * 8 + 2;
                            break;

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
                w->dec_lo_double = dmey_double[0];
                w->dec_hi_double = dmey_double[1];
                w->rec_lo_double = dmey_double[2];
                w->rec_hi_double = dmey_double[3];
                w->dec_lo_float = dmey_float[0];
                w->dec_hi_float = dmey_float[1];
                w->rec_lo_float = dmey_float[2];
                w->rec_hi_float = dmey_float[3];
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
        w->dec_lo_double = wtcalloc(filters_length, sizeof(double));
        w->dec_hi_double = wtcalloc(filters_length, sizeof(double));
        w->rec_lo_double = wtcalloc(filters_length, sizeof(double));
        w->rec_hi_double = wtcalloc(filters_length, sizeof(double));

        if(w->dec_lo_double == NULL || w->dec_hi_double == NULL || w->rec_lo_double == NULL || w->rec_hi_double == NULL){
            free_wavelet(w);
            return NULL;
        }
        w->dec_lo_float = wtcalloc(filters_length, sizeof(float));
        w->dec_hi_float = wtcalloc(filters_length, sizeof(float));
        w->rec_lo_float = wtcalloc(filters_length, sizeof(float));
        w->rec_hi_float = wtcalloc(filters_length, sizeof(float));

        if(w->dec_lo_float == NULL || w->dec_hi_float == NULL || w->rec_lo_float == NULL || w->rec_hi_float == NULL){
            free_wavelet(w);
            return NULL;
        }

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
        w->dec_lo_double = wtcalloc(w->dec_len, sizeof(double));
        w->dec_hi_double = wtcalloc(w->dec_len, sizeof(double));
        w->rec_lo_double = wtcalloc(w->rec_len, sizeof(double));
        w->rec_hi_double = wtcalloc(w->rec_len, sizeof(double));

        if(w->dec_lo_double == NULL || w->dec_hi_double == NULL || w->rec_lo_double == NULL || w->rec_hi_double == NULL){
            free_wavelet(w);
            return NULL;
        }

        for(i=0; i< w->dec_len; ++i){
            w->dec_lo_double[i] = base->dec_lo_double[i];
            w->dec_hi_double[i] = base->dec_hi_double[i];
        }

        for(i=0; i< w->rec_len; ++i){
            w->rec_lo_double[i] = base->rec_lo_double[i];
            w->rec_hi_double[i] = base->rec_hi_double[i];
        }
        w->dec_lo_float = wtcalloc(w->dec_len, sizeof(float));
        w->dec_hi_float = wtcalloc(w->dec_len, sizeof(float));
        w->rec_lo_float = wtcalloc(w->rec_len, sizeof(float));
        w->rec_hi_float = wtcalloc(w->rec_len, sizeof(float));

        if(w->dec_lo_float == NULL || w->dec_hi_float == NULL || w->rec_lo_float == NULL || w->rec_hi_float == NULL){
            free_wavelet(w);
            return NULL;
        }

        for(i=0; i< w->dec_len; ++i){
            w->dec_lo_float[i] = base->dec_lo_float[i];
            w->dec_hi_float[i] = base->dec_hi_float[i];
        }

        for(i=0; i< w->rec_len; ++i){
            w->rec_lo_float[i] = base->rec_lo_float[i];
            w->rec_hi_float[i] = base->rec_hi_float[i];
        }

    return w;
}

void free_wavelet(Wavelet *w){
    if(wavelet == NULL)
        return;

    if(w->_builtin == 0){

        // dealocate filters
            if(w->dec_lo_double != NULL){
                wtfree(w->dec_lo_double);
                w->dec_lo_double = NULL;
            }

            if(w->dec_hi_double != NULL){
                wtfree(w->dec_hi_double);
                w->dec_hi_double = NULL;
            }

            if(w->rec_lo_double != NULL){
                wtfree(w->rec_lo_double);
                w->rec_lo_double = NULL;
            }

            if(w->rec_hi_double != NULL){
                wtfree(w->rec_hi_double);
                w->rec_hi_double = NULL;
            }
            if(w->dec_lo_float != NULL){
                wtfree(w->dec_lo_float);
                w->dec_lo_float = NULL;
            }

            if(w->dec_hi_float != NULL){
                wtfree(w->dec_hi_float);
                w->dec_hi_float = NULL;
            }

            if(w->rec_lo_float != NULL){
                wtfree(w->rec_lo_float);
                w->rec_lo_float = NULL;
            }

            if(w->rec_hi_float != NULL){
                wtfree(w->rec_hi_float);
                w->rec_hi_float = NULL;
            }
    }

    // finally free struct
    wtfree(w);
}
