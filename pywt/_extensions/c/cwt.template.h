/* Copyright (c) 2016 Holger Nahrstaedt */
/* See COPYING for license details. */


#include "templating.h"

#ifndef TYPE
#error TYPE must be defined here.
#else

#include "cwt.h"

#if defined _MSC_VER
#define restrict __restrict
#elif defined __GNUC__
#define restrict __restrict__
#endif


TYPE CAT(TYPE, _powof)(const TYPE x, const TYPE y);


int CAT(TYPE, _gaus)(const TYPE * const restrict input,
                              TYPE * const restrict output, const size_t N,
                              const size_t number);

int CAT(TYPE, _gaus1)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);
int CAT(TYPE, _gaus2)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);
int CAT(TYPE, _gaus3)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);
int CAT(TYPE, _gaus4)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);
int CAT(TYPE, _gaus5)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);
int CAT(TYPE, _gaus6)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);
int CAT(TYPE, _gaus7)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);
int CAT(TYPE, _gaus8)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);




int CAT(TYPE, _mexh)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);

int CAT(TYPE, _morl)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N);

int CAT(TYPE, _cgau)(const TYPE * const restrict input,
                              TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
                              const size_t number);

int CAT(TYPE, _cgau1)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N);
int CAT(TYPE, _cgau2)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N);
int CAT(TYPE, _cgau3)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N);
int CAT(TYPE, _cgau4)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N);
int CAT(TYPE, _cgau5)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N);
int CAT(TYPE, _cgau6)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N);
int CAT(TYPE, _cgau7)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N);
int CAT(TYPE, _cgau8)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N);


int CAT(TYPE, _shan)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
                              const TYPE  FB, const TYPE  FC);

int CAT(TYPE, _fbsp)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
                              const int M, const TYPE  FB, const TYPE  FC);

int CAT(TYPE, _cmor)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
                              const TYPE  FB, const TYPE  FC);
#endif /* TYPE */
#undef restrict
