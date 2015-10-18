#include "libcpu6502.h"
#include "utils.h"

/////////////////////////////
// function from nes-mem.c //
////////////////////////////////////////////////////////////////////////////////
extern Word8 ReadMem ( Word16 addr );
extern void WriteMem ( Word16 addr, Word8 data );
extern void StepMem ( Word64 inst_count );
extern void InitMem ();
extern void FreeMem ();

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

///////////////////////////////////////
// cpu6502 memory interface wrappers //
////////////////////////////////////////////////////////////////////////////////

void cpu6502_ifc_Display (int32_t lvl, const char * msg)
{
    Display(lvl, msg);
}

Word8 cpu6502_ifc_ReadMem ( Word16 addr )
{
    return ReadMem(addr);
}

void cpu6502_ifc_WriteMem ( Word16 addr, Word8 data )
{
    WriteMem(addr, data);
}

///////////////////////
// global ressources //
////////////////////////////////////////////////////////////////////////////////

unsigned int display_lvl = 0;
char ines_file[100] = "default.nes";

///////////////////
// main function //
////////////////////////////////////////////////////////////////////////////////
int main (int argc, const char ** argv)
{
    printf("--------------\n");
    printf("--- NES-L3 ---\n");
    printf("--------------\n");

    printf("\n");
    printf("Nintendo Entertainment System emulator Based on 6502 L3 model\n");
    printf("\n");

    // command line options
    ////////////////////////////////////////////////////////////////////////////

    int c;
    while (1)
    {
        static struct option long_options[] =
        {
            {"mute",    no_argument, &display_lvl, 0},
            {"verbose", optional_argument, 0, 'v'},
            {"ines",    required_argument, 0, 'i'},
            {0, 0, 0, 0}
        };
        int option_index = 0;

        c = getopt_long (argc, argv, "v::i:", long_options, &option_index);

        if (c == -1) break;
        switch (c)
        {
            case 0:
                if (long_options[option_index].flag != 0) break;
                printf ("option %s", long_options[option_index].name);
                if (optarg)
                    printf (" with arg %s", optarg);
                printf ("\n");
                break;

            case 'v':
                if (optarg)
                {
                    printf ("verbose. display_lvl set to `%d'\n", atoi(optarg));
                    display_lvl = atoi(optarg);
                }
                else
                    display_lvl = 2;
                break;

            case 'i':
                printf ("ines file specified: `%s'\n", optarg);
                strcpy(ines_file, optarg);
                break;

            case '?': break;

            default : abort ();
        }
    }

    if (optind < argc)
    {
        printf ("non-option ARGV-elements: ");
        while (optind < argc)
            printf ("%s ", argv[optind++]);
        putchar ('\n');
    }

    // NES emulator initialisation
    ////////////////////////////////////////////////////////////////////////////

    printf("... initializing 6502 L3 module\n");
    cpu6502_open(argc, argv);
    printf("... 6502 L3 module initialized\n");

    printf("... initializing C NES address space emulation module\n");
    InitMem(ines_file);
    printf("... C NES address space emulation module initialized\n");

    // NES emulator main execution loop
    ////////////////////////////////////////////////////////////////////////////
    Word64 inst_count = 0;
    cpu6502_SetRESET(1);
    while (1)
    //while (0)
    {
        cpu6502_Next();
        StepMem(inst_count);
        inst_count++;
    }

    // NES emulator cleaning
    ////////////////////////////////////////////////////////////////////////////

    printf("%lu instructions emulated. Closing emulator ...\n", inst_count);

    printf("... closing C NES address space emulation module\n");
    FreeMem();
    printf("... C NES address space emulation module closed\n");

    printf("... closing 6502 L3 module\n");
    cpu6502_close();
    printf("... 6502 L3 module closed\n");

    printf("\nSee ya !\n");

    return 0;
}
