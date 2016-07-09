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

TYPE CAT(TYPE, _sqrt)(const TYPE x)
{
    if (sizeof(TYPE) == sizeof(double))
        return sqrt(x);        
    else
        return sqrtf(x);
}

TYPE CAT(TYPE, _exp)(const TYPE x)
{
    if (sizeof(TYPE) == sizeof(double))
        return exp(x);        
    else
        return expf(x);
}

TYPE CAT(TYPE, _cos)(const TYPE x)
{
    if (sizeof(TYPE) == sizeof(double))
        return cos(x);        
    else
        return cosf(x);
}

TYPE CAT(TYPE, _sin)(const TYPE x)
{
    if (sizeof(TYPE) == sizeof(double))
        return sin(x);
    else
        return sinf(x);
}

TYPE CAT(TYPE, _pi)()
{
    if (sizeof(TYPE) == sizeof(double))
        return M_PI;        
    else
        return (TYPE)M_PI;
}


void CAT(TYPE, _gaus)(const TYPE * const restrict input,
                              TYPE * const restrict output, const size_t N,
                              const size_t number){
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
           switch (number) {
               case 1:
                    output[i] = -2*input[i]*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2)); 
                    break;
                case 2:
                    output[i] = -2*(2*(input[i]*input[i])-1)*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(3*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                    break;
                case 3:
                    output[i] = -4*(-2*(input[i]*input[i]*input[i])+3*input[i])*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(15*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2)); 
                    break;
                case 4:
                    output[i] = 4*(-12*(input[i]*input[i])+4*(input[i]*input[i]*input[i]*input[i])+3)*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(105*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));  
                    break;
                case 5:
                    output[i] =  8*(-4*(input[i]*input[i]*input[i]*input[i]*input[i])+20*(input[i]*input[i]*input[i])-15*input[i])*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(105*9*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                    break;
                case 6:
                    output[i] = -8*(8*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])-60*(input[i]*input[i]*input[i]*input[i])+90*(input[i]*input[i])-15)*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(105*9*11*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                    break;
                case 7:
                    output[i] =  -16*(-8*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])+84*(input[i]*input[i]*input[i]*input[i]*input[i])-210*(input[i]*input[i]*input[i])+105*(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(105*9*11*13*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));  
                    break;
                case 8:
                    output[i] =  16*(16*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])-224*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])+840*(input[i]*input[i]*input[i]*input[i])-840*(input[i]*input[i])+105)*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(105*9*11*13*15*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));  
                    break;
          }
    }
}



void CAT(TYPE, _mexh)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = (1-(input[i]*input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i])/2)*2/(CAT(TYPE, _sqrt)(3)*CAT(TYPE, _sqrt)(CAT(TYPE, _sqrt)(CAT(TYPE, _pi)())));
    }  
}

void CAT(TYPE, _morl)(const TYPE * const restrict input, TYPE * const restrict output, const size_t N)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output[i] = CAT(TYPE, _cos)(5*input[i])*CAT(TYPE, _exp)(-(input[i]*input[i])/2);
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
                 output_r[i] = (-2*input[i]*CAT(TYPE, _cos)(input[i])-CAT(TYPE, _sin)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(2*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                 output_i[i] = (2*input[i]*CAT(TYPE, _sin)(input[i])-CAT(TYPE, _cos)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(2*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                 break;
             case 2:
                 output_r[i] = (4*(input[i]*input[i])*CAT(TYPE, _cos)(input[i])+4*input[i]*CAT(TYPE, _sin)(input[i])-3*CAT(TYPE, _cos)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(10*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                output_i[i] = (-4*(input[i]*input[i])*CAT(TYPE, _sin)(input[i])+4*input[i]*CAT(TYPE, _cos)(input[i])+3*CAT(TYPE, _sin)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(10*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                 break;
             case 3:
                 output_r[i] = (-8*(input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-12*(input[i]*input[i])*CAT(TYPE, _sin)(input[i])+18*input[i]*CAT(TYPE, _cos)(input[i])+7*CAT(TYPE, _sin)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(76*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                 output_i[i] = (8*(input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-12*(input[i]*input[i])*CAT(TYPE, _cos)(input[i])-18*input[i]*CAT(TYPE, _sin)(input[i])+7*CAT(TYPE, _cos)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(76*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));

                 break;
             case 4:
                 output_r[i] =  (16*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+32*(input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-72*(input[i]*input[i])*CAT(TYPE, _cos)(input[i])-56*input[i]*CAT(TYPE, _sin)(input[i])+25*CAT(TYPE, _cos)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(764*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));;
                 output_i[i] = (-16*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+32*(input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+72*(input[i]*input[i])*CAT(TYPE, _sin)(input[i])-56*input[i]*CAT(TYPE, _cos)(input[i])-25*CAT(TYPE, _sin)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(764*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));

                 break;
             case 5:
                 output_r[i] = (-32*(input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-80*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+240*(input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+280*(input[i]*input[i])*CAT(TYPE, _sin)(input[i])-250*input[i]*CAT(TYPE, _cos)(input[i])-81*CAT(TYPE, _sin)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(9496*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                 output_i[i] = (32*(input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-80*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-240*(input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+280*(input[i]*input[i])*CAT(TYPE, _cos)(input[i])+250*input[i]*CAT(TYPE, _sin)(input[i])-81*CAT(TYPE, _cos)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(9496*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));

                 break;
             case 6:
                output_r[i] = (64*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+192*(input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-720*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-1120*(input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+1500*(input[i]*input[i])*CAT(TYPE, _cos)(input[i])+972*input[i]*CAT(TYPE, _sin)(input[i])-331*CAT(TYPE, _cos)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(140152*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                output_i[i] = (-64*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+192*(input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+720*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-1120*(input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-1500*(input[i]*input[i])*CAT(TYPE, _sin)(input[i])+972*input[i]*CAT(TYPE, _cos)(input[i])+331*CAT(TYPE, _sin)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(140152*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));

                 break;
             case 7:
                 output_r[i] = (-128*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-448*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+2016*(input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+3920*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-7000*(input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-6804*(input[i]*input[i])*CAT(TYPE, _sin)(input[i])+4634*input[i]*CAT(TYPE, _cos)(input[i])+1303*CAT(TYPE, _sin)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(2390480*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                 output_i[i] = (128*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-448*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-2016*(input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+3920*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+7000*(input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-6804*(input[i]*input[i])*CAT(TYPE, _cos)(input[i])-4634*input[i]*CAT(TYPE, _sin)(input[i])+1303*CAT(TYPE, _cos)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(2390480*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));

                 break;
             case 8:
                 output_r[i] = (256*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+1024*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-5376*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-12544*(input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+28000*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+36288*(input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-37072*(input[i]*input[i])*CAT(TYPE, _cos)(input[i])-20848*input[i]*CAT(TYPE, _sin)(input[i])+5937*CAT(TYPE, _cos)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(46206736*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));
                 output_i[i] = (-256*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+1024*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+5376*(input[i]*input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])-12544*(input[i]*input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])-28000*(input[i]*input[i]*input[i]*input[i])*CAT(TYPE, _sin)(input[i])+36288*(input[i]*input[i]*input[i])*CAT(TYPE, _cos)(input[i])+37072*(input[i]*input[i])*CAT(TYPE, _sin)(input[i])-20848*input[i]*CAT(TYPE, _cos)(input[i])-5937*CAT(TYPE, _sin)(input[i]))*CAT(TYPE, _exp)(-(input[i]*input[i]))/CAT(TYPE, _sqrt)(46206736*CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()/2));

                 break;
       }
    }
}


void CAT(TYPE, _shan)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
const TYPE  FB, const TYPE  FC)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] =CAT(TYPE, _cos)(2*CAT(TYPE, _pi)()*FC*input[i])*CAT(TYPE, _sqrt)(FB);
        output_i[i] = CAT(TYPE, _sin)(2*CAT(TYPE, _pi)()*FC*input[i])*CAT(TYPE, _sqrt)(FB);
        if (input[i] != 0)
        {
            output_r[i] *= CAT(TYPE, _sin)(input[i]*FB*CAT(TYPE, _pi)())/(input[i]*FB*CAT(TYPE, _pi)());
            output_i[i] *= CAT(TYPE, _sin)(input[i]*FB*CAT(TYPE, _pi)())/(input[i]*FB*CAT(TYPE, _pi)());
        }
    }  
}

void CAT(TYPE, _fbsp)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
const unsigned int M, const TYPE  FB, const TYPE  FC)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        if (input[i] != 0)
        {
            output_r[i] = CAT(TYPE, _cos)(2*CAT(TYPE, _pi)()*FC*input[i])*CAT(TYPE, _sqrt)(FB)*CAT(TYPE, _powof)(CAT(TYPE, _sin)(CAT(TYPE, _pi)()*input[i]*FB/(TYPE)M)/(CAT(TYPE, _pi)()*input[i]*FB/(TYPE)M),(TYPE)M);
            output_i[i] = CAT(TYPE, _sin)(2*CAT(TYPE, _pi)()*FC*input[i])*CAT(TYPE, _sqrt)(FB)*CAT(TYPE, _powof)(CAT(TYPE, _sin)(CAT(TYPE, _pi)()*input[i]*FB/(TYPE)M)/(CAT(TYPE, _pi)()*input[i]*FB/(TYPE)M),(TYPE)M);
        }
        else
        {
            output_r[i] = CAT(TYPE, _cos)(2*CAT(TYPE, _pi)()*FC*input[i])*CAT(TYPE, _sqrt)(FB);
            output_i[i] = CAT(TYPE, _sin)(2*CAT(TYPE, _pi)()*FC*input[i])*CAT(TYPE, _sqrt)(FB);
        }
    }
}



void CAT(TYPE, _cmor)(const TYPE * const restrict input, TYPE * const restrict output_r, TYPE * const restrict output_i, const size_t N,
const TYPE  FB, const TYPE  FC)
{
    size_t i = 0;
    for (i = 0; i < N; i++)
    {
        output_r[i] =CAT(TYPE, _cos)(2*CAT(TYPE, _pi)()*FC*input[i])*CAT(TYPE, _exp)(-(input[i]*input[i])/FB)/CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()*FB);
        output_i[i] = CAT(TYPE, _sin)(2*CAT(TYPE, _pi)()*FC*input[i])*CAT(TYPE, _exp)(-(input[i]*input[i])/FB)/CAT(TYPE, _sqrt)(CAT(TYPE, _pi)()*FB);

    }   
}


#endif /* TYPE */
#undef restrict
