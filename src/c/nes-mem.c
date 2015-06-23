#include "smlexport.h"
#include "utils.h"
#include <stdio.h>

/////////
// ram //
/////////

#define RAM_OFFSET(x) (x & 0x7FF)

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
extern void step_ppu ();

////////////
// others //
////////////

#define OTHERS_OFFSET(x) (x & 0x1F)

static Word8 read_others (Word16 addr)
{
    Display(2," -- others read\n");
    return 0x20;
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

///////////////
// cartridge //
///////////////

extern Word8 read_cart (Word16 addr);
extern void write_cart (Word16 addr, Word8 data);
extern void init_cart ();
extern void free_cart ();

///////////////////////////////
// functions exported to sml //
///////////////////////////////

Word8 CReadMem ( Word16 addr )
{
    Word8 res = 0x42;
    if ((addr >= 0x0000) && (addr < 0x2000)) // 4 mirrors
        res = read_ram(addr);
    else if ((addr >= 0x2000) && (addr < 0x1FF8)) // 1024 mirrors
        res = read_ppu(addr);
    //else if (addr >= 0x1FF8 and addr < 0x4000) // nothing ?
    else if ((addr >= 0x4000) && (addr < 0x4020)) // registers
        res = read_others (addr);
    else if (addr >= 0x4020) // Cartridge
        res = read_cart (addr);
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
    else if (addr >= 0x4020) // cartridge
        write_cart (addr, data);
}

void CStepMem ( Word64 inst_count )
{
    if (inst_count % 1024 == 0 && inst_count != 0)
        step_ppu();
}

void CInitMem ()
{
    Display(2,"CInitMem\n");
    init_ram();
    init_ppu();
    init_others();
    init_cart();
}

void CFreeMem ()
{
    Display(2,"CFreeMem\n");
    free_ram();
    free_ppu();
    free_others();
    free_cart();
}
