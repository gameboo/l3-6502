#include "smlexport.h"

#define Display(lvl, ...) \
    do {\
        if (display_lvl >= lvl && display_lvl >= 0)\
        {\
            printf (__VA_ARGS__);\
            fflush(stdout);\
        }\
    } while (0)
