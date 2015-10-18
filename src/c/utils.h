#ifndef _CPU6502_L3_C_UTILS
#define _CPU6502_L3_C_UTILS

#include "libcpu6502.h"
#include <stdio.h>

extern unsigned int display_lvl;

#define Display(lvl, ...) \
    do {\
        if (display_lvl >= lvl && display_lvl >= 0)\
        {\
            fflush(stdout);\
            printf (__VA_ARGS__);\
            fflush(stdout);\
        }\
    } while (0)

#endif
