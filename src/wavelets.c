// Copyright (c) 2006 Filip Wasilewski <filipwasilewski@gmail.com>
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
		w->family_name = "Haar\0";
		w->short_name = "haar\0";
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

		w->dec_hi_offset = wtmp->rec_hi_offset;
		w->rec_hi_offset = wtmp->dec_hi_offset;
		w->dec_lo_offset = wtmp->rec_lo_offset;
		w->rec_lo_offset = wtmp->dec_lo_offset;

		for(i = 0; i < w->rec_len; ++i){
			w->rec_lo[i] = wtmp->dec_lo[wtmp->dec_len-1-i];
			w->rec_hi[i] = wtmp->dec_hi[wtmp->dec_len-1-i];
		}

		for(i = 0; i < w->dec_len; ++i){
			w->dec_hi[i] = wtmp->rec_hi[wtmp->rec_len-1-i];
			w->dec_lo[i] = wtmp->rec_lo[wtmp->rec_len-1-i];
		}

		w->vanishing_moments_phi = wtmp->vanishing_moments_psi;
		w->vanishing_moments_psi = wtmp->vanishing_moments_phi;

		w->family_name = "Reverse biorthogonal\0";
		w->short_name = "rbio\0";
		
		return w;
	}

	w = wtmalloc(sizeof(Wavelet));
	if(w == NULL)
		return NULL;

	w->dec_lo_offset = w->rec_lo_offset = 0;
	w->dec_hi_offset = w->rec_hi_offset = 0;
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
			w->family_name = "Daubechies\0";
			w->short_name = "db\0";

			switch (order) {
				case 1:
					w->dec_lo = db1[0];
					w->dec_hi = db1[1];
					w->rec_lo = db1[2];
					w->rec_hi = db1[3];
					break;
				case 2:
					w->dec_lo = db2[0];
					w->dec_hi = db2[1];
					w->rec_lo = db2[2];
					w->rec_hi = db2[3];
					break;
				case 3:
					w->dec_lo = db3[0];
					w->dec_hi = db3[1];
					w->rec_lo = db3[2];
					w->rec_hi = db3[3];
					break;
				case 4:
					w->dec_lo = db4[0];
					w->dec_hi = db4[1];
					w->rec_lo = db4[2];
					w->rec_hi = db4[3];
					break;
				case 5:
					w->dec_lo = db5[0];
					w->dec_hi = db5[1];
					w->rec_lo = db5[2];
					w->rec_hi = db5[3];
					break;
				case 6:
					w->dec_lo = db6[0];
					w->dec_hi = db6[1];
					w->rec_lo = db6[2];
					w->rec_hi = db6[3];
					break;
				case 7:
					w->dec_lo = db7[0];
					w->dec_hi = db7[1];
					w->rec_lo = db7[2];
					w->rec_hi = db7[3];
					break;
				case 8:
					w->dec_lo = db8[0];
					w->dec_hi = db8[1];
					w->rec_lo = db8[2];
					w->rec_hi = db8[3];
					break;
				case 9:
					w->dec_lo = db9[0];
					w->dec_hi = db9[1];
					w->rec_lo = db9[2];
					w->rec_hi = db9[3];
					break;
				case 10:
					w->dec_lo = db10[0];
					w->dec_hi = db10[1];
					w->rec_lo = db10[2];
					w->rec_hi = db10[3];
					break;
				case 11:
					w->dec_lo = db11[0];
					w->dec_hi = db11[1];
					w->rec_lo = db11[2];
					w->rec_hi = db11[3];
					break;
				case 12:
					w->dec_lo = db12[0];
					w->dec_hi = db12[1];
					w->rec_lo = db12[2];
					w->rec_hi = db12[3];
					break;
				case 13:
					w->dec_lo = db13[0];
					w->dec_hi = db13[1];
					w->rec_lo = db13[2];
					w->rec_hi = db13[3];
					break;
				case 14:
					w->dec_lo = db14[0];
					w->dec_hi = db14[1];
					w->rec_lo = db14[2];
					w->rec_hi = db14[3];
					break;
				case 15:
					w->dec_lo = db15[0];
					w->dec_hi = db15[1];
					w->rec_lo = db15[2];
					w->rec_hi = db15[3];
					break;
				case 16:
					w->dec_lo = db16[0];
					w->dec_hi = db16[1];
					w->rec_lo = db16[2];
					w->rec_hi = db16[3];
					break;
				case 17:
					w->dec_lo = db17[0];
					w->dec_hi = db17[1];
					w->rec_lo = db17[2];
					w->rec_hi = db17[3];
					break;
				case 18:
					w->dec_lo = db18[0];
					w->dec_hi = db18[1];
					w->rec_lo = db18[2];
					w->rec_hi = db18[3];
					break;
				case 19:
					w->dec_lo = db19[0];
					w->dec_hi = db19[1];
					w->rec_lo = db19[2];
					w->rec_hi = db19[3];
					break;
				case 20:
					w->dec_lo = db20[0];
					w->dec_hi = db20[1];
					w->rec_lo = db20[2];
					w->rec_hi = db20[3];
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
			w->family_name = "Symlets\0";
			w->short_name = "sym\0";

			switch (order) {
				case 2:
					w->dec_lo = sym2[0];
					w->dec_hi = sym2[1];
					w->rec_lo = sym2[2];
					w->rec_hi = sym2[3];
					break;
				case 3:
					w->dec_lo = sym3[0];
					w->dec_hi = sym3[1];
					w->rec_lo = sym3[2];
					w->rec_hi = sym3[3];
					break;
				case 4:
					w->dec_lo = sym4[0];
					w->dec_hi = sym4[1];
					w->rec_lo = sym4[2];
					w->rec_hi = sym4[3];
					break;
				case 5:
					w->dec_lo = sym5[0];
					w->dec_hi = sym5[1];
					w->rec_lo = sym5[2];
					w->rec_hi = sym5[3];
					break;
				case 6:
					w->dec_lo = sym6[0];
					w->dec_hi = sym6[1];
					w->rec_lo = sym6[2];
					w->rec_hi = sym6[3];
					break;
				case 7:
					w->dec_lo = sym7[0];
					w->dec_hi = sym7[1];
					w->rec_lo = sym7[2];
					w->rec_hi = sym7[3];
					break;
				case 8:
					w->dec_lo = sym8[0];
					w->dec_hi = sym8[1];
					w->rec_lo = sym8[2];
					w->rec_hi = sym8[3];
					break;
				case 9:
					w->dec_lo = sym9[0];
					w->dec_hi = sym9[1];
					w->rec_lo = sym9[2];
					w->rec_hi = sym9[3];
					break;
				case 10:
					w->dec_lo = sym10[0];
					w->dec_hi = sym10[1];
					w->rec_lo = sym10[2];
					w->rec_hi = sym10[3];
					break;
				case 11:
					w->dec_lo = sym11[0];
					w->dec_hi = sym11[1];
					w->rec_lo = sym11[2];
					w->rec_hi = sym11[3];
					break;
				case 12:
					w->dec_lo = sym12[0];
					w->dec_hi = sym12[1];
					w->rec_lo = sym12[2];
					w->rec_hi = sym12[3];
					break;
				case 13:
					w->dec_lo = sym13[0];
					w->dec_hi = sym13[1];
					w->rec_lo = sym13[2];
					w->rec_hi = sym13[3];
					break;
				case 14:
					w->dec_lo = sym14[0];
					w->dec_hi = sym14[1];
					w->rec_lo = sym14[2];
					w->rec_hi = sym14[3];
					break;
				case 15:
					w->dec_lo = sym15[0];
					w->dec_hi = sym15[1];
					w->rec_lo = sym15[2];
					w->rec_hi = sym15[3];
					break;
				case 16:
					w->dec_lo = sym16[0];
					w->dec_hi = sym16[1];
					w->rec_lo = sym16[2];
					w->rec_hi = sym16[3];
					break;
				case 17:
					w->dec_lo = sym17[0];
					w->dec_hi = sym17[1];
					w->rec_lo = sym17[2];
					w->rec_hi = sym17[3];
					break;
				case 18:
					w->dec_lo = sym18[0];
					w->dec_hi = sym18[1];
					w->rec_lo = sym18[2];
					w->rec_hi = sym18[3];
					break;
				case 19:
					w->dec_lo = sym19[0];
					w->dec_hi = sym19[1];
					w->rec_lo = sym19[2];
					w->rec_hi = sym19[3];
					break;
				case 20:
					w->dec_lo = sym20[0];
					w->dec_hi = sym20[1];
					w->rec_lo = sym20[2];
					w->rec_hi = sym20[3];
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
			w->family_name = "Coiflets\0";
			w->short_name = "coif\0";

			switch (order) {
				case 1:
					w->dec_lo = coif1[0];
					w->dec_hi = coif1[1];
					w->rec_lo = coif1[2];
					w->rec_hi = coif1[3];
					break;
				case 2:
					w->dec_lo = coif2[0];
					w->dec_hi = coif2[1];
					w->rec_lo = coif2[2];
					w->rec_hi = coif2[3];
					break;
				case 3:
					w->dec_lo = coif3[0];
					w->dec_hi = coif3[1];
					w->rec_lo = coif3[2];
					w->rec_hi = coif3[3];
					break;
				case 4:
					w->dec_lo = coif4[0];
					w->dec_hi = coif4[1];
					w->rec_lo = coif4[2];
					w->rec_hi = coif4[3];
					break;
				case 5:
					w->dec_lo = coif5[0];
					w->dec_hi = coif5[1];
					w->rec_lo = coif5[2];
					w->rec_hi = coif5[3];
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
			w->family_name = "Biorthogonal\0";
			w->short_name = "bior\0";

			switch (order) {
				case 11:
					w->dec_lo = bior1_1[0];
					w->dec_hi = bior1_1[1];
					w->rec_lo = bior1_1[2];
					w->rec_hi = bior1_1[3];
					w->dec_len = w->rec_len = 2;
					break;
				case 13:
					w->dec_lo = bior1_3[0];
					w->dec_hi = bior1_3[1];
					w->rec_lo = bior1_3[2];
					w->rec_hi = bior1_3[3];
					w->dec_len = w->rec_len = 6;
					w->dec_hi_offset = w->rec_lo_offset = 2;
					break;
				case 15:
					w->dec_lo = bior1_5[0];
					w->dec_hi = bior1_5[1];
					w->rec_lo = bior1_5[2];
					w->rec_hi = bior1_5[3];
					w->dec_len = w->rec_len = 10;
					w->dec_hi_offset = w->rec_lo_offset = 4;
					break;
				case 22:
					w->dec_lo = bior2_2[0];
					w->dec_hi = bior2_2[1];
					w->rec_lo = bior2_2[2];
					w->rec_hi = bior2_2[3];
					w->dec_len = w->rec_len = 6;
					w->dec_hi_offset = w->rec_lo_offset = 1;
					break;
				case 24:
					w->dec_lo = bior2_4[0];
					w->dec_hi = bior2_4[1];
					w->rec_lo = bior2_4[2];
					w->rec_hi = bior2_4[3];
					w->dec_len = w->rec_len = 10;
					w->dec_hi_offset = w->rec_lo_offset = 3;
					break;
				case 26:
					w->dec_lo = bior2_6[0];
					w->dec_hi = bior2_6[1];
					w->rec_lo = bior2_6[2];
					w->rec_hi = bior2_6[3];
					w->dec_len = w->rec_len = 14;
					w->dec_hi_offset = w->rec_lo_offset = 5;
					break;
				case 28:
					w->dec_lo = bior2_8[0];
					w->dec_hi = bior2_8[1];
					w->rec_lo = bior2_8[2];
					w->rec_hi = bior2_8[3];
					w->dec_len = w->rec_len = 18;
					w->dec_hi_offset = w->rec_lo_offset = 7;
					break;
				case 31:
					w->dec_lo = bior3_1[0];
					w->dec_hi = bior3_1[1];
					w->rec_lo = bior3_1[2];
					w->rec_hi = bior3_1[3];
					w->dec_len = w->rec_len = 4;
					break;
				case 33:
					w->dec_lo = bior3_3[0];
					w->dec_hi = bior3_3[1];
					w->rec_lo = bior3_3[2];
					w->rec_hi = bior3_3[3];
					w->dec_len = w->rec_len = 8;
					w->dec_hi_offset = w->rec_lo_offset = 2;
					break;
				case 35:
					w->dec_lo = bior3_5[0];
					w->dec_hi = bior3_5[1];
					w->rec_lo = bior3_5[2];
					w->rec_hi = bior3_5[3];
					w->dec_len = w->rec_len = 12;
					w->dec_hi_offset = w->rec_lo_offset = 4;
					break;
				case 37:
					w->dec_lo = bior3_7[0];
					w->dec_hi = bior3_7[1];
					w->rec_lo = bior3_7[2];
					w->rec_hi = bior3_7[3];
					w->dec_len = w->rec_len = 16;
					w->dec_hi_offset = w->rec_lo_offset = 6;
					break;
				case 39:
					w->dec_lo = bior3_9[0];
					w->dec_hi = bior3_9[1];
					w->rec_lo = bior3_9[2];
					w->rec_hi = bior3_9[3];
					w->dec_len = w->rec_len = 20;
					w->dec_hi_offset = w->rec_lo_offset = 8;
					break;
				case 44:
					w->dec_lo = bior4_4[0];
					w->dec_hi = bior4_4[1];
					w->rec_lo = bior4_4[2];
					w->rec_hi = bior4_4[3];
					w->dec_len = w->rec_len = 10;
					w->dec_hi_offset = w->rec_lo_offset = 1;
					break;
				case 55:
					w->dec_lo = bior5_5[0];
					w->dec_hi = bior5_5[1];
					w->rec_lo = bior5_5[2];
					w->rec_hi = bior5_5[3];
					w->dec_len = w->rec_len = 12;
					w->dec_hi_offset = w->rec_lo_offset = 0;
					w->dec_lo_offset = w->rec_hi_offset = 12;
					break;
				case 68:
					w->dec_lo = bior6_8[0];
					w->dec_hi = bior6_8[1];
					w->rec_lo = bior6_8[2];
					w->rec_hi = bior6_8[3];
					w->dec_len = w->rec_len = 18;
					w->dec_hi_offset = w->rec_lo_offset = 3;
					break;

				default:
					wtfree(w);
					return NULL;
			}
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
			w->family_name = "Discrete Meyer (FIR Approximation)\0";
			w->short_name = "dmey\0";

			
			w->dec_lo = dmey[0];
			w->dec_hi = dmey[1];
			w->rec_lo = dmey[2];
			w->rec_hi = dmey[3];
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

	w->dec_lo_offset = w->rec_lo_offset = 0;
	w->dec_hi_offset = w->rec_hi_offset = 0;

	// Important!
	// Otherwise filters arrays allocated here won't be deallocated by free_wavelet
	w->_builtin = 0;

	w->dec_len = w->rec_len = filters_length;

	w->dec_lo = wtcalloc(filters_length, sizeof(double));
	w->dec_hi = wtcalloc(filters_length, sizeof(double));
	w->rec_lo = wtcalloc(filters_length, sizeof(double));
	w->rec_hi = wtcalloc(filters_length, sizeof(double));

	if(w->dec_lo == NULL || w->dec_hi == NULL || w->rec_lo == NULL || w->rec_hi == NULL){
		free_wavelet(w);
		return NULL;
	}

	// set properties to "blank" values
	w->vanishing_moments_psi = 0;
	w->vanishing_moments_phi = 0;
	w->support_width = -1;
	w->orthogonal = 0;
	w->orthonormal = 0;
	w->biorthogonal = 0;
	w->symmetry = UNKNOWN;
	w->compact_support = 0;
	w->family_name = "\0";
	w->short_name = "\0";

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

	w->dec_lo = wtcalloc(w->dec_len, sizeof(double));
	w->dec_hi = wtcalloc(w->dec_len, sizeof(double));
	w->rec_lo = wtcalloc(w->rec_len, sizeof(double));
	w->rec_hi = wtcalloc(w->rec_len, sizeof(double));

	if(w->dec_lo == NULL || w->dec_hi == NULL || w->rec_lo == NULL || w->rec_hi == NULL){
		free_wavelet(w);
		return NULL;
	}

	for(i=0; i< w->dec_len; ++i){
		w->dec_lo[i] = base->dec_lo[i];
		w->dec_hi[i] = base->dec_hi[i];
	}

	for(i=0; i< w->rec_len; ++i){
		w->rec_lo[i] = base->rec_lo[i];
		w->rec_hi[i] = base->rec_hi[i];
	}

	return w;
}

void free_wavelet(Wavelet *w){
	if(wavelet == NULL)
		return;

	if(w->_builtin == 0){

		// dealocate filters
		
		if(w->dec_lo != NULL){
			wtfree((double*)w->dec_lo);
			w->dec_lo = NULL;
		}

		if(w->dec_hi != NULL){
			wtfree((double*)w->dec_hi);
			w->dec_hi = NULL;
		}

		if(w->rec_lo != NULL){
			wtfree((double*)w->rec_lo);
			w->rec_lo = NULL;
		}

		if(w->rec_hi != NULL){
			wtfree((double*)w->rec_hi);
			w->rec_hi = NULL;
		}
	}

	// finally free struct
	wtfree(w);
}
