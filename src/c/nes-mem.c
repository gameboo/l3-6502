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

Word8 * lower_bank;
Word8 read_lower_bank (Word16 a) { lower_bank[a]; }
//void write_lower_bank (Word16 a, Word8 d) { lower_bank[a] = d; }
Word8 * upper_bank;
Word8 read_upper_bank (Word16 a) { upper_bank[a]; }
//void write_upper_bank (Word16 a, Word8 d) { upper_bank[a] = d; }
//sram
//exprom
static Word8 read_cart (Word16 addr)
{
    Display(2," -- cart read\n");
    Word8 res = 0x30;
    if ((addr >= 0x4020) && (addr < 0x6000)) // exprom
        res = 0x31;
    else if ((addr >= 0x6000) && (addr < 0x8000)) // sram
        res = 0x32;
    else if ((addr >= 0x8000) && (addr < 0xC000)) // lower bank
        res = read_lower_bank(addr&0x3FFF);
    else if (addr >= 0xC000) // upper bank
        res = read_upper_bank(addr&0x3FFF);
    return res;
}
static void write_cart (Word16 addr, Word8 data)
{
    Display(2," -- cart write -- not supported\n");
    /*
    if ((addr >= 0x4020) && (addr < 0x6000)) {}// exprom
    else if ((addr >= 0x6000) && (addr < 0x8000)) {}// sram
    else if ((addr >= 0x8000) && (addr < 0xC000)) // lower bank
        res = write_lower_bank(addr&0x3FFF, data);
    else if (addr >= 0xC000) // upper bank
        res = write_upper_bank(addr&0x3FFF, data);
    */
}
static void init_cart ()
{
    Display(2," -- cart init\n");
    lower_bank = (Word8*) malloc (sizeof(Word8)*0x4000);
    upper_bank = (Word8*) malloc (sizeof(Word8)*0x4000);
}
static void free_cart ()
{
    Display(2," -- cart free\n");
    free(upper_bank);
    free(lower_bank);
}

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

void CLoadiNES ( Pointer stream , Word32 size )
{
    Display(2,"CLoadiNES\n");
    if (upper_bank == NULL || lower_bank == NULL)
    {
        Display(2,"cartridge space uninitialized\n");
        exit(-1);
    }
    else
    {
        Display(2,"-- init cartridge upper bank\n");
        memcpy(upper_bank, &stream[15], 0x4000);
        Display(2,"-- init cartridge lower bank\n");
        memcpy(lower_bank, &stream[15+0x4000], 0x4000);
        /*
        int i = 0;
        for (i = 0; i < 0x4000; i++)
        {
            lower_bank[i] = 0xFF;
            upper_bank[i] = 0xFF;
        }
        */
    }
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
