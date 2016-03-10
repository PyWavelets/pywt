/* Copyright (c) 2016 Holger Nahrstaedt */
/* See COPYING for license details. */

#include "templating.h"

#ifndef TYPE
#error TYPE must be defined here.
#else

#include "cwt.h"
#include "convolution.h"

#if defined _MSC_VER
#define restrict __restrict
#elif defined __GNUC__
#define restrict __restrict__
#endif
#define _USE_MATH_DEFINES
#include "math.h"

TYPE CAT(TYPE, _powof)(const TYPE x, const TYPE y)
{
    if (sizeof(TYPE) == sizeof(double))
        return pow(x,y);        
    else
        return powf(x,y);
}


int CAT(TYPE, _cwt_conv_real) (const TYPE * const restrict input, const size_t N, 
                    const TYPE * const restrict filter, const size_t F,
                    TYPE * const restrict output, const size_t O  )
{
        size_t len;
        size_t i = 0;
        size_t j = 0;
        TYPE *fTemp, *buf;

        len = N+F-1;
        buf = malloc(len*sizeof(TYPE));
        fTemp = malloc(F*sizeof(TYPE));

        for (i = 0; i < F; i++)
          fTemp[i] = filter[F - i - 1];        
        
        CAT(TYPE, _cwt_conv)(input,N,fTemp,F,buf,len);
        
        free(fTemp);

        for (i = 0; i < O; i++)
                output[i] = buf[(len -  O) / 2 + i];
        free(buf);
        return 0;
}

int CAT(TYPE, _gaus)(const TYPE * const restrict input,
                              TYPE * const restrict output, const size_t N,
                              const size_t number){
    //if (strcmp(wavelet->short_name, "gauss")){
           switch (number) {
               case 1:
                    CAT(TYPE, _gaus1)(input, output, N);
                    break;
                case 2:
                    CAT(TYPE, _gaus2)(input, output, N);
                    break;
                case 3:
                    CAT(TYPE, _gaus3)(input, output, N);
                    break;
                case 4:
                    CAT(TYPE, _gaus4)(input, output, N);
                    break;
                case 5:
                    CAT(TYPE, _gaus5)(input, output, N);
                    break;
                case 6:
                    CAT(TYPE, _gaus6)(input, output, N);
                    break;
                case 7:
                    CAT(TYPE, _gaus7)(input, output, N);
                    break;
                case 8:
                    CAT(TYPE, _gaus8)(input, output, N);
                    break;
          }
    //}
    return 0;
}

int CAT(TYPE, _gaus1)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = -2*input[i]*exp(-(input[i]*input[i]))/sqrt(sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _gaus2)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = 2*(2*(input[i]*input[i])-1)*exp(-(input[i]*input[i]))/sqrt(3*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _gaus3)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = -4*(2*(input[i]*input[i]*input[i])-3*input[i])*exp(-(input[i]*input[i]))/sqrt(15*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _gaus4)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = 4*(-12*(input[i]*input[i])+4*(input[i]*input[i]*input[i]*input[i])+3)*exp(-(input[i]*input[i]))/sqrt(105*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _gaus5)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = 8*(-4*(input[i]*input[i]*input[i]*input[i]*input[i])+20*(input[i]*input[i]*input[i])-15*input[i])*exp(-(input[i]*input[i]))/sqrt(105*9*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _gaus6)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = 8*(8*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])-60*(input[i]*input[i]*input[i]*input[i])+90*(input[i]*input[i])-15)*exp(-(input[i]*input[i]))/sqrt(105*9*11*sqrt(M_PI/2));
    }
    return 0;    
}


int CAT(TYPE, _gaus7)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = 16*(-8*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])+84*(input[i]*input[i]*input[i]*input[i]*input[i])-210*(input[i]*input[i]*input[i])+105*(input[i]))*exp(-(input[i]*input[i]))/sqrt(105*9*11*13*sqrt(M_PI/2));
    }
    return 0;    
}


int CAT(TYPE, _gaus8)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = 16*(16*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])-224*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])+840*(input[i]*input[i]*input[i]*input[i])-840*(input[i]*input[i])+105)*exp(-(input[i]*input[i]))/sqrt(105*9*11*13*15*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _mexh)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = (1-(input[i]*input[i]))*exp(-(input[i]*input[i])/2)*2/(sqrt(3)*sqrt(sqrt(M_PI)));
    }
    return 0;    
}

int CAT(TYPE, _morl)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = cos(5*input[i])*exp(-(input[i]*input[i])/2);
    }
    return 0;    
}


int CAT(TYPE, _cgau)(const TYPE * const restrict input,
                              TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
                              const size_t number){
    //if (strcmp(wavelet->short_name, "gauss")){
           switch (number) {
               case 1:
                    CAT(TYPE, _cgau1)(input, output_r, output_i, N);
                    break;
                case 2:
                    CAT(TYPE, _cgau2)(input, output_r, output_i, N);
                    break;
                case 3:
                    CAT(TYPE, _cgau3)(input, output_r, output_i, N);
                    break;
                case 4:
                    CAT(TYPE, _cgau4)(input, output_r, output_i, N);
                    break;
                case 5:
                    CAT(TYPE, _cgau5)(input, output_r, output_i, N);
                    break;
                case 6:
                    CAT(TYPE, _cgau6)(input, output_r, output_i, N);
                    break;
                case 7:
                    CAT(TYPE, _cgau7)(input, output_r, output_i, N);
                    break;
                case 8:
                    CAT(TYPE, _cgau8)(input, output_r, output_i, N);
                    break;
          }
    //}
    return 0;
}


int CAT(TYPE, _cgau1)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] = (-2*input[i]*cos(input[i])-sin(input[i]))*exp(-(input[i]*input[i]))/sqrt(2*sqrt(M_PI/2));
        output_i[i] = (2*input[i]*sin(input[i])-cos(input[i]))*exp(-(input[i]*input[i]))/sqrt(2*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _cgau2)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] = (4*(input[i]*input[i])*cos(input[i])+4*input[i]*sin(input[i])-3*cos(input[i]))*exp(-(input[i]*input[i]))/sqrt(10*sqrt(M_PI/2));
        output_i[i] = (-4*(input[i]*input[i])*sin(input[i])+4*input[i]*cos(input[i])+3*sin(input[i]))*exp(-(input[i]*input[i]))/sqrt(10*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _cgau3)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] = (-8*(input[i]*input[i]*input[i])*cos(input[i])-12*(input[i]*input[i])*sin(input[i])+18*input[i]*cos(input[i])+7*sin(input[i]))*exp(-(input[i]))/sqrt(76*sqrt(M_PI/2));
        output_i[i] = (8*(input[i]*input[i]*input[i])*sin(input[i])-12*(input[i]*input[i])*cos(input[i])-18*input[i]*sin(input[i])+7*cos(input[i]))*exp(-(input[i]))/sqrt(76*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _cgau4)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] =  (16*(input[i]*input[i]*input[i]*input[i])*cos(input[i])+32*(input[i]*input[i]*input[i])*sin(input[i])-72*(input[i]*input[i])*cos(input[i])-56*input[i]*sin(input[i])+25*cos(input[i]))*exp(-(input[i]*input[i]))/sqrt(764*sqrt(M_PI/2));;
        output_i[i] = (-16*(input[i]*input[i]*input[i]*input[i])*sin(input[i])+32*(input[i]*input[i]*input[i])*cos(input[i])+72*(input[i]*input[i])*sin(input[i])-56*input[i]*cos(input[i])-25*sin(input[i]))*exp(-(input[i]*input[i]))/sqrt(764*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _cgau5)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] = (-32*(input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])-80*(input[i]*input[i]*input[i]*input[i])*sin(input[i])+240*(input[i]*input[i]*input[i])*cos(input[i])+280*(input[i]*input[i])*sin(input[i])-250*input[i]*cos(input[i])-81*sin(input[i]))*exp(-(input[i]*input[i]))/sqrt(9496*sqrt(M_PI/2));
        output_i[i] = (32*(input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])-80*(input[i]*input[i]*input[i]*input[i])*cos(input[i])-240*(input[i]*input[i]*input[i])*sin(input[i])+280*(input[i]*input[i])*cos(input[i])+250*input[i]*sin(input[i])-81*cos(input[i]))*exp(-(input[i]*input[i]))/sqrt(9496*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _cgau6)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] = (64*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])+192*(input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])-720*(input[i]*input[i]*input[i]*input[i])*cos(input[i])-1120*(input[i]*input[i]*input[i])*sin(input[i])+1500*(input[i]*input[i])*cos(input[i])+972*input[i]*sin(input[i])-331*cos(input[i]))*exp(-(input[i]*input[i]))/sqrt(140152*sqrt(M_PI/2));
        output_i[i] = (-64*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])+192*(input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])+720*(input[i]*input[i]*input[i]*input[i])*sin(input[i])-1120*(input[i]*input[i]*input[i])*cos(input[i])-1500*(input[i]*input[i])*sin(input[i])+972*input[i]*cos(input[i])+331*sin(input[i]))*exp(-(input[i]*input[i]))/sqrt(140152*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _cgau7)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] = (-128*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])-448*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])+2016*(input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])+3920*(input[i]*input[i]*input[i]*input[i])*sin(input[i])-7000*(input[i]*input[i]*input[i])*cos(input[i])-6804*(input[i]*input[i])*sin(input[i])+4634*input[i]*cos(input[i])+1303*sin(input[i]))*exp(-(input[i]*input[i]))/sqrt(2390480*sqrt(M_PI/2));
        output_i[i] = (128*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])-448*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])-2016*(input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])+3920*(input[i]*input[i]*input[i]*input[i])*cos(input[i])+7000*(input[i]*input[i]*input[i])*sin(input[i])-6804*(input[i]*input[i])*cos(input[i])-4634*input[i]*sin(input[i])+1303*cos(input[i]))*exp(-(input[i]*input[i]))/sqrt(2390480*sqrt(M_PI/2));
    }
    return 0;    
}

int CAT(TYPE, _cgau8)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] = (256*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])+1024*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])-5376*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])-12544*(input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])+28000*(input[i]*input[i]*input[i]*input[i])*cos(input[i])+36288*(input[i]*input[i]*input[i])*sin(input[i])-37072*(input[i]*input[i])*cos(input[i])-20848*input[i]*sin(input[i])+5937*cos(input[i]))*exp(-(input[i]*input[i]))/sqrt(46206736*sqrt(M_PI/2));
        output_i[i] = (-256*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])+1024*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])+5376*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*sin(input[i])-12544*(input[i]*input[i]*input[i]*input[i]*input[i])*cos(input[i])-28000*(input[i]*input[i]*input[i]*input[i])*sin(input[i])+36288*(input[i]*input[i]*input[i])*cos(input[i])+37072*(input[i]*input[i])*sin(input[i])-20848*input[i]*cos(input[i])-5937*sin(input[i]))*exp(-(input[i]*input[i]))/sqrt(46206736*sqrt(M_PI/2));
    }
    return 0;    
}


int CAT(TYPE, _shan)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
const TYPE  FB, const TYPE  FC)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] =cos(2*M_PI*FC*input[i])*sqrt(FB);
        output_i[i] = sin(2*M_PI*FC*input[i])*sqrt(FB);
        if (input[i] != 0)
        {
            output_r[i] *= sin(input[i]*FB*M_PI)/(input[i]*FB*M_PI);
            output_i[i] *= sin(input[i]*FB*M_PI)/(input[i]*FB*M_PI);
        }
    }
    return 0;    
}

int CAT(TYPE, _fbsp)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
const int M, const TYPE  FB, const TYPE  FC)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] =cos(2*M_PI*FC*input[i])*sqrt(FB);
        output_i[i] = sin(2*M_PI*FC*input[i])*sqrt(FB);
        if (input[i] != 0)
        {
            output_r[i] *= CAT(TYPE, _powof)(sin(input[i]*FB*M_PI/(double)M)/(input[i]*FB*M_PI/(double)M),M);
            output_i[i] *= CAT(TYPE, _powof)(sin(input[i]*FB*M_PI/(double)M)/(input[i]*FB*M_PI/(double)M),M);
        }
    }
    return 0;    
}



int CAT(TYPE, _cmor)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
const TYPE  FB, const TYPE  FC)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] =cos(2*M_PI*FC*input[i])*exp(-(input[i]*input[i])/FB)/sqrt(M_PI*FB);
        output_i[i] = sin(2*M_PI*FC*input[i])*exp(-(input[i]*input[i])/FB)/sqrt(M_PI*FB);

    }
    return 0;    
}


#endif /* TYPE */
#undef restrict
