#pragma once

#include "common.h"

#ifdef TYPE
#error TYPE should not be defined here.
#else

#define TYPE float
#include "convolution.template.h"
#undef TYPE

#define TYPE double
#include "convolution.template.h"
#undef TYPE

#endif /* TYPE */
