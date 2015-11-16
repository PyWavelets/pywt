#pragma once

#ifdef TYPE
#error TYPE should not be defined here.
#else

#define TYPE float
#include "wavelets_coeffs.template.h"
#undef TYPE

#define TYPE double
#include "wavelets_coeffs.template.h"
#undef TYPE

#endif /* TYPE */
