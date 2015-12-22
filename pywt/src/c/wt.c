#include "wt.h"

#ifdef TYPE
#error TYPE should not be defined here.
#else

#define TYPE float
#include "wt.template.c"
#undef TYPE

#define TYPE double
#include "wt.template.c"
#undef TYPE

#endif /* TYPE */
