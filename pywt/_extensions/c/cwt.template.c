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



void CAT(TYPE, _gaus)(const TYPE * const restrict input,
                              TYPE * const restrict output, const size_t N,
                              const size_t number){
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
           switch (number) {
               case 1:
                    CAT(TYPE, _gaus1)(input[i], &output[i]);
                    break;
                case 2:
                    CAT(TYPE, _gaus2)(input[i], &output[i]);
                    break;
                case 3:
                    CAT(TYPE, _gaus3)(input[i], &output[i]);
                    break;
                case 4:
                    CAT(TYPE, _gaus4)(input[i], &output[i]);
                    break;
                case 5:
                    CAT(TYPE, _gaus5)(input[i], &output[i]);
                    break;
                case 6:
                    CAT(TYPE, _gaus6)(input[i], &output[i]);
                    break;
                case 7:
                    CAT(TYPE, _gaus7)(input[i], &output[i]);
                    break;
                case 8:
                    CAT(TYPE, _gaus8)(input[i], &output[i]);
                    break;
          }
    }
}

void CAT(TYPE, _gaus1)(const TYPE  input, TYPE * const restrict output)
{
        *output = -2*input*exp(-(input*input))/sqrt(sqrt(M_PI/2)); 
}

void CAT(TYPE, _gaus2)(const TYPE input, TYPE * const restrict output)
{
        *output = 2*(2*(input*input)-1)*exp(-(input*input))/sqrt(3*sqrt(M_PI/2));
}

void CAT(TYPE, _gaus3)(const TYPE input, TYPE * const restrict output)
{
        *output = -4*(2*(input*input*input)-3*input)*exp(-(input*input))/sqrt(15*sqrt(M_PI/2)); 
}

void CAT(TYPE, _gaus4)(const TYPE  input, TYPE * const restrict output)
{
        *output = 4*(-12*(input*input)+4*(input*input*input*input)+3)*exp(-(input*input))/sqrt(105*sqrt(M_PI/2));  
}

void CAT(TYPE, _gaus5)(const TYPE input, TYPE * const restrict output)
{
        *output = 8*(-4*(input*input*input*input*input)+20*(input*input*input)-15*input)*exp(-(input*input))/sqrt(105*9*sqrt(M_PI/2));
}

void CAT(TYPE, _gaus6)(const TYPE input, TYPE * const restrict output)
{
        *output = 8*(8*(input*input*input*input*input*input)-60*(input*input*input*input)+90*(input*input)-15)*exp(-(input*input))/sqrt(105*9*11*sqrt(M_PI/2));
}


void CAT(TYPE, _gaus7)(const TYPE input, TYPE * const restrict output)
{
        *output = 16*(-8*(input*input*input*input*input*input*input)+84*(input*input*input*input*input)-210*(input*input*input)+105*(input))*exp(-(input*input))/sqrt(105*9*11*13*sqrt(M_PI/2));  
}


void CAT(TYPE, _gaus8)(const TYPE  input, TYPE * const restrict output)
{

        *output = 16*(16*(input*input*input*input*input*input*input*input)-224*(input*input*input*input*input*input)+840*(input*input*input*input)-840*(input*input)+105)*exp(-(input*input))/sqrt(105*9*11*13*15*sqrt(M_PI/2));  
}

void CAT(TYPE, _mexh)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = (1-(input[i]*input[i]))*exp(-(input[i]*input[i])/2)*2/(sqrt(3)*sqrt(sqrt(M_PI)));
    }  
}

void CAT(TYPE, _morl)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = cos(5*input[i])*exp(-(input[i]*input[i])/2);
    }   
}


void CAT(TYPE, _cgau)(const TYPE * const restrict input,
                              TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
                              const size_t number){
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        switch (number) {
            case 1:
                 CAT(TYPE, _cgau1)(input[i], &output_r[i], &output_i[i]);
                 break;
             case 2:
                 CAT(TYPE, _cgau2)(input[i], &output_r[i], &output_i[i]);
                 break;
             case 3:
                 CAT(TYPE, _cgau3)(input[i], &output_r[i], &output_i[i]);
                 break;
             case 4:
                 CAT(TYPE, _cgau4)(input[i], &output_r[i], &output_i[i]);
                 break;
             case 5:
                 CAT(TYPE, _cgau5)(input[i], &output_r[i], &output_i[i]);
                 break;
             case 6:
                 CAT(TYPE, _cgau6)(input[i], &output_r[i], &output_i[i]);
                 break;
             case 7:
                 CAT(TYPE, _cgau7)(input[i], &output_r[i], &output_i[i]);
                 break;
             case 8:
                 CAT(TYPE, _cgau8)(input[i], &output_r[i], &output_i[i]);
                 break;
       }
    }
}


void CAT(TYPE, _cgau1)(const TYPE input, TYPE * const restrict output_r, TYPE * const restrict output_i)
{

    *output_r = (-2*input*cos(input)-sin(input))*exp(-(input*input))/sqrt(2*sqrt(M_PI/2));
    *output_i = (2*input*sin(input)-cos(input))*exp(-(input*input))/sqrt(2*sqrt(M_PI/2));
}

void CAT(TYPE, _cgau2)(const TYPE  input, TYPE * const restrict output_r, TYPE * const restrict output_i)
{

        *output_r = (4*(input*input)*cos(input)+4*input*sin(input)-3*cos(input))*exp(-(input*input))/sqrt(10*sqrt(M_PI/2));
        *output_i = (-4*(input*input)*sin(input)+4*input*cos(input)+3*sin(input))*exp(-(input*input))/sqrt(10*sqrt(M_PI/2));
}

void CAT(TYPE, _cgau3)(const TYPE  input, TYPE * const restrict output_r, TYPE * const restrict output_i)
{

        *output_r = (-8*(input*input*input)*cos(input)-12*(input*input)*sin(input)+18*input*cos(input)+7*sin(input))*exp(-(input))/sqrt(76*sqrt(M_PI/2));
        *output_i = (8*(input*input*input)*sin(input)-12*(input*input)*cos(input)-18*input*sin(input)+7*cos(input))*exp(-(input))/sqrt(76*sqrt(M_PI/2));
}

void CAT(TYPE, _cgau4)(const TYPE  input, TYPE * const restrict output_r, TYPE * const restrict output_i)
{
        *output_r =  (16*(input*input*input*input)*cos(input)+32*(input*input*input)*sin(input)-72*(input*input)*cos(input)-56*input*sin(input)+25*cos(input))*exp(-(input*input))/sqrt(764*sqrt(M_PI/2));;
        *output_i = (-16*(input*input*input*input)*sin(input)+32*(input*input*input)*cos(input)+72*(input*input)*sin(input)-56*input*cos(input)-25*sin(input))*exp(-(input*input))/sqrt(764*sqrt(M_PI/2));
}

void CAT(TYPE, _cgau5)(const TYPE  input, TYPE * const restrict output_r, TYPE * const restrict output_i)
{
        *output_r = (-32*(input*input*input*input*input)*cos(input)-80*(input*input*input*input)*sin(input)+240*(input*input*input)*cos(input)+280*(input*input)*sin(input)-250*input*cos(input)-81*sin(input))*exp(-(input*input))/sqrt(9496*sqrt(M_PI/2));
        *output_i = (32*(input*input*input*input*input)*sin(input)-80*(input*input*input*input)*cos(input)-240*(input*input*input)*sin(input)+280*(input*input)*cos(input)+250*input*sin(input)-81*cos(input))*exp(-(input*input))/sqrt(9496*sqrt(M_PI/2));
}

void CAT(TYPE, _cgau6)(const TYPE  input, TYPE * const restrict output_r, TYPE * const restrict output_i)
{
        *output_r = (64*(input*input*input*input*input*input)*cos(input)+192*(input*input*input*input*input)*sin(input)-720*(input*input*input*input)*cos(input)-1120*(input*input*input)*sin(input)+1500*(input*input)*cos(input)+972*input*sin(input)-331*cos(input))*exp(-(input*input))/sqrt(140152*sqrt(M_PI/2));
        *output_i = (-64*(input*input*input*input*input*input)*sin(input)+192*(input*input*input*input*input)*cos(input)+720*(input*input*input*input)*sin(input)-1120*(input*input*input)*cos(input)-1500*(input*input)*sin(input)+972*input*cos(input)+331*sin(input))*exp(-(input*input))/sqrt(140152*sqrt(M_PI/2));
}

void CAT(TYPE, _cgau7)(const TYPE input, TYPE * const restrict output_r, TYPE * const restrict output_i)
{
        *output_r = (-128*(input*input*input*input*input*input*input)*cos(input)-448*(input*input*input*input*input*input)*sin(input)+2016*(input*input*input*input*input)*cos(input)+3920*(input*input*input*input)*sin(input)-7000*(input*input*input)*cos(input)-6804*(input*input)*sin(input)+4634*input*cos(input)+1303*sin(input))*exp(-(input*input))/sqrt(2390480*sqrt(M_PI/2));
        *output_i = (128*(input*input*input*input*input*input*input)*sin(input)-448*(input*input*input*input*input*input)*cos(input)-2016*(input*input*input*input*input)*sin(input)+3920*(input*input*input*input)*cos(input)+7000*(input*input*input)*sin(input)-6804*(input*input)*cos(input)-4634*input*sin(input)+1303*cos(input))*exp(-(input*input))/sqrt(2390480*sqrt(M_PI/2));
}

void CAT(TYPE, _cgau8)(const TYPE input, TYPE * const restrict output_r, TYPE * const restrict output_i)
{
        *output_r = (256*(input*input*input*input*input*input*input*input)*cos(input)+1024*(input*input*input*input*input*input*input)*sin(input)-5376*(input*input*input*input*input*input)*cos(input)-12544*(input*input*input*input*input)*sin(input)+28000*(input*input*input*input)*cos(input)+36288*(input*input*input)*sin(input)-37072*(input*input)*cos(input)-20848*input*sin(input)+5937*cos(input))*exp(-(input*input))/sqrt(46206736*sqrt(M_PI/2));
        *output_i = (-256*(input*input*input*input*input*input*input*input)*sin(input)+1024*(input*input*input*input*input*input*input)*cos(input)+5376*(input*input*input*input*input*input)*sin(input)-12544*(input*input*input*input*input)*cos(input)-28000*(input*input*input*input)*sin(input)+36288*(input*input*input)*cos(input)+37072*(input*input)*sin(input)-20848*input*cos(input)-5937*sin(input))*exp(-(input*input))/sqrt(46206736*sqrt(M_PI/2));
}


void CAT(TYPE, _shan)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
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
}

void CAT(TYPE, _fbsp)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
const unsigned int M, const TYPE  FB, const TYPE  FC)
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
}



void CAT(TYPE, _cmor)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
const TYPE  FB, const TYPE  FC)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] =cos(2*M_PI*FC*input[i])*exp(-(input[i]*input[i])/FB)/sqrt(M_PI*FB);
        output_i[i] = sin(2*M_PI*FC*input[i])*exp(-(input[i]*input[i])/FB)/sqrt(M_PI*FB);

    }   
}


#endif /* TYPE */
#undef restrict
