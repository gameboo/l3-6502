#include "smlexport.h"
#include "utils.h"
#include <stdio.h>

/////////
// ram //
/////////

#define RAM_OFFSET(x) (x % 0x800)

static Word8 * ram;
static Word8 read_ram (Word16 addr)
{
    Display(2," -- ram read\n");
    return ram[RAM_OFFSET(addr)];
}
static void write_ram (Word16 addr, Word8 data)
{
    Display(2," -- ram write\n");
    ram[RAM_OFFSET(addr)] = data;
}
static void init_ram ()
{
    Display(2," -- ram init\n");
    ram = (Word8*) malloc (sizeof(Word8)*0x800);
}
static void free_ram ()
{
    Display(2," -- ram free\n");
    free(ram);
}

/////////
// PPU //
/////////

extern Word8 read_ppu (Word16 addr);
extern void write_ppu (Word16 addr, Word8 data);
extern void init_ppu ();
extern void free_ppu ();

////////////
// others //
////////////

#define OTHERS_OFFSET(x) (x % 0x20)

static Word8 read_others (Word16 addr)
{
    Display(2," -- others read\n");
    return 42;
}
static void write_others (Word16 addr, Word8 data)
{
    Display(2," -- others write\n");
}
static void init_others ()
{
    Display(2," -- others init\n");
}
static void free_others ()
{
    Display(2," -- others free\n");
}

/////////////
// EXP ROM //
/////////////

#define EXP_ROM_OFFSET(x) (x % 0x1FDF)

static Word8 read_exp_rom (Word16 addr)
{
    Display(2," -- exp rom read\n");
    return 42;
}
static void write_exp_rom (Word16 addr, Word8 data)
{
    Display(2," -- exp rom write\n");
}
static void init_exp_rom ()
{
    Display(2," -- exp rom init\n");
}
static void free_exp_rom ()
{
    Display(2," -- exp rom free\n");
}

///////////////////
// Work/Save RAM //
///////////////////

#define WSRAM_OFFSET(x) (x % 0x2000)

static Word8 read_wsram (Word16 addr)
{
    Display(2," -- w/s ram read\n");
    return 42;
}
static void write_wsram (Word16 addr, Word8 data)
{
    Display(2," -- w/s ram write\n");
}
static void init_wsram ()
{
    Display(2," -- w/s ram init\n");
}
static void free_wsram ()
{
    Display(2," -- w/s ram free\n");
}

//////////////
// PRGM ROM //
//////////////

#define PRGM_OFFSET(x) (x % 0x8000)

static Word8 read_prgm (Word16 addr)
{
    Display(2," -- prgm read\n");
    return 42;
}
static void write_prgm (Word16 addr, Word8 data)
{
    Display(2," -- prgm write\n");
}
static void init_prgm ()
{
    Display(2," -- prgm init\n");
}
static void free_prgm ()
{
    Display(2," -- prgm free\n");
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
    Display(2,"CReadMem @0x%04x = 0x%02x\n", addr, res);
    return res;
}

void CWriteMem ( Word16 addr, Word8 data )
{
    Display(2,"CWriteMem @0x%04x <- 0x%02x\n", addr, data);
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
    Display(2,"CWriteStream not supported in NES mode\n");
}

void CInitMem ()
{
    Display(2,"CInitMem\n");
    init_ram();
    init_ppu();
    init_others();
    init_exp_rom();
    init_wsram();
    init_prgm();
}

void CFreeMem ()
{
    Display(2,"CFreeMem\n");
    free_ram();
    free_ppu();
    free_exp_rom();
    free_prgm();
}
