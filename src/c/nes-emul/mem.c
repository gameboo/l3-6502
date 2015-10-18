#include "libcpu6502.h"
#include "utils.h"
#include <stdlib.h>

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

extern Word8 read_ppu  (Word16 addr);
extern void  write_ppu (Word16 addr, Word8 data);
extern void  init_ppu  ();
extern void  free_ppu  ();
extern void  step_ppu  (Word64 inst_count);

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

Word8 ReadMem ( Word16 addr )
{
    Word8 res = 0x42;
    if ((addr >= 0x0000) && (addr < 0x2000)) // 4 mirrors
        res = read_ram(addr);
    else if ((addr >= 0x2000) && (addr < 0x4000)) // 1024 mirrors
        res = read_ppu(addr);
    else if ((addr >= 0x4000) && (addr < 0x4020)) // registers
        res = read_others (addr);
    else if (addr >= 0x4020) // Cartridge
        res = read_cart (addr);
    Display(2,"ReadMem @0x%04x = 0x%02x\n", addr, res);
    return res;
}

void WriteMem ( Word16 addr, Word8 data )
{
    Display(2,"WriteMem @0x%04x <- 0x%02x\n", addr, data);
    if ((addr >= 0x0000) && (addr < 0x2000)) // 4 mirrors
        write_ram(addr, data);
    else if ((addr >= 0x2000) && (addr < 0x4000)) // 1024 mirrors
        write_ppu(addr, data);
    else if ((addr >= 0x4000) && (addr < 0x4020)) // registers
        write_others (addr, data);
    else if (addr >= 0x4020) // cartridge
        write_cart (addr, data);
}

void StepMem ( Word64 inst_count )
{
    cpu6502_SetRESET(0);
    cpu6502_SetNMI(0);
    step_ppu(inst_count);
}

void InitMem (char * ines_filename)
{
    Display(2,"InitMem\n");
    init_cart(ines_filename);
    init_ppu();
    init_others();
    init_ram();
}

void FreeMem ()
{
    Display(2,"FreeMem\n");
    free_ram();
    free_others();
    free_ppu();
    free_cart();
}
