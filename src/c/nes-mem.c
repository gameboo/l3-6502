#include "smlexport.h"
#include <stdio.h>

/////////
// ram //
/////////

#define RAM_OFFSET(x) (x % 0x800)

static Word8 * ram;
static Word8 read_ram (Word16 addr)
{
    printf(" -- ram read\n");
    return ram[RAM_OFFSET(addr)];
}
static void write_ram (Word16 addr, Word8 data)
{
    printf(" -- ram write\n");
    ram[RAM_OFFSET(addr)] = data;
}
static void init_ram ()
{
    printf(" -- ram init\n");
    ram = (Word8*) malloc (sizeof(Word8)*0x800);
}
static void free_ram ()
{
    printf(" -- ram free\n");
    free(ram);
}

/////////
// PPU //
/////////

#define PPU_OFFSET(x) (x % 0x8)

Word8 * ppu_regs;
Word8 * ppu_pattern;
Word8 * ppu_name;
Word8 * ppu_palette;

static Word8 read_ppu (Word16 addr)
{
    Word8 res = 0;
    printf(" -- ppu read\n");
    switch PPU_OFFSET(addr)
    {
        case 2:
            res = ppu_regs[2];
            ppu_regs[2] = ppu_regs[2] & 0x7F;
            break;
        case 4:
            res = ppu_regs[4];
            break;
        case 7:
            res = ppu_regs[7];
            break;
        default:
            printf(" -- ppu reg %d write only\n",PPU_OFFSET(addr));
            res = 0;
            break;
    }
}
static void write_ppu (Word16 addr, Word8 data)
{
    printf(" -- ppu write\n");
}
static void init_ppu ()
{
    printf(" -- ppu init\n");
    ppu_palette = (Word8*) malloc (sizeof(Word8)*0x0020);
    ppu_name = (Word8*) malloc (sizeof(Word8)*0x1000);
    ppu_pattern = (Word8*) malloc (sizeof(Word8)*0x2000);
    ppu_regs = (Word8*) malloc (sizeof(Word8)*8);
}
static void free_ppu ()
{
    printf(" -- ppu free\n");
    free(ppu_regs);
    free(ppu_pattern);
    free(ppu_name);
    free(ppu_palette);
}

////////////
// others //
////////////

#define OTHERS_OFFSET(x) (x % 0x20)

static Word8 read_others (Word16 addr)
{
    printf(" -- others read\n");
}
static void write_others (Word16 addr, Word8 data)
{
    printf(" -- others write\n");
}
static void init_others ()
{
    printf(" -- others init\n");
}
static void free_others ()
{
    printf(" -- others free\n");
}

/////////////
// EXP ROM //
/////////////

#define EXP_ROM_OFFSET(x) (x % 0x1FDF)

static Word8 read_exp_rom (Word16 addr)
{
    printf(" -- exp rom read\n");
}
static void write_exp_rom (Word16 addr, Word8 data)
{
    printf(" -- exp rom write\n");
}
static void init_exp_rom ()
{
    printf(" -- exp rom init\n");
}
static void free_exp_rom ()
{
    printf(" -- exp rom free\n");
}

///////////////////
// Work/Save RAM //
///////////////////

#define WSRAM_OFFSET(x) (x % 0x2000)

static Word8 read_wsram (Word16 addr)
{
    printf(" -- w/s ram read\n");
}
static void write_wsram (Word16 addr, Word8 data)
{
    printf(" -- w/s ram write\n");
}
static void init_wsram ()
{
    printf(" -- w/s ram init\n");
}
static void free_wsram ()
{
    printf(" -- w/s ram free\n");
}

//////////////
// PRGM ROM //
//////////////

#define PRGM_OFFSET(x) (x % 0x8000)

static Word8 read_prgm (Word16 addr)
{
    printf(" -- prgm read\n");
}
static void write_prgm (Word16 addr, Word8 data)
{
    printf(" -- prgm write\n");
}
static void init_prgm ()
{
    printf(" -- prgm init\n");
}
static void free_prgm ()
{
    printf(" -- prgm free\n");
}

///////////////////////////////
// functions exported to sml //
///////////////////////////////

Word8 CReadMem ( Word16 addr )
{
    Word8 res = 42;
    if ((addr >= 0x0000) && (addr < 0x2000)) // 4 mirrors
        res = read_ram(addr);
    else if ((addr >= 0x2000) && (addr < 0x1FF8)) // 1024 mirrors
        res = read_ppu(addr);
    //else if (addr >= 0x1FF8 and addr < 0x4000) // nothing ?
    else if ((addr >= 0x4000) && (addr < 0x4020)) // registers
        res = read_others (addr);
    else if ((addr >= 0x4020) && (addr < 0x6000)) // expansion rom
        res = read_exp_rom (addr);
    else if ((addr >= 0x6000) && (addr < 0x8000)) // SRAM
        res = read_wsram (addr);
    else if ((addr >= 0x8000) && (addr < 0xC000)) // PRGM-ROM
        res = read_prgm (addr);
    else if (addr >= 0xC000) // PRGM-ROM
        res = read_prgm (addr);
    printf("CReadMem @0x%04x = 0x%02x\n", addr, res);
    return res;
}

void CWriteMem ( Word16 addr, Word8 data )
{
    printf("CWriteMem @0x%04x <- 0x%02x\n", addr, data);
    if ((addr >= 0x0000) && (addr < 0x2000)) // 4 mirrors
        write_ram(addr, data);
    else if ((addr >= 0x2000) && (addr < 0x1FF8)) // 1024 mirrors
        write_ppu(addr, data);
    //else if (addr >= 0x1FF8 && addr < 0x4000) // nothing ?
    else if ((addr >= 0x4000) && (addr < 0x4020)) // registers
        write_others (addr, data);
    else if ((addr >= 0x4020) && (addr < 0x6000)) // expansion rom
        write_exp_rom (addr, data);
    else if ((addr >= 0x6000) && (addr < 0x8000)) // SRAM
        write_wsram (addr, data);
    else if ((addr >= 0x8000) && (addr < 0xC000)) // PRGM-ROM
        write_prgm (addr, data);
    else if (addr >= 0xC000) // PRGM-ROM
        write_prgm (addr, data);
}

void CWriteStream ( Word16 addr, Pointer stream , Word32 size )
{
    printf("CWriteStream not supported in NES mode\n");
}

void CInitMem ()
{
    printf("CInitMem\n");
    init_ram();
    init_ppu();
    init_others();
    init_exp_rom();
    init_wsram();
    init_prgm();
}

void CFreeMem ()
{
    printf("CFreeMem\n");
    free_ram();
    free_ppu();
    free_exp_rom();
    free_prgm();
}
