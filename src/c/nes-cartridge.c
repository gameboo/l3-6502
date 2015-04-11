#include "smlexport.h"
#include "utils.h"
#include <stdio.h>

extern Word8 * map_ppu_pattern_table(Word8*);

///////////////
// cartridge //
///////////////

static Word8 * chr_rom;
static Word8 read_chr_rom (Word16 a) { return chr_rom[a]; }
static void write_chr_rom (Word16 a, Word8 d) { chr_rom[a] = d; }
static Word8 * cart_ram;
static Word8 read_cart_ram (Word16 a) { return cart_ram[a]; }
static void write_cart_ram (Word16 a, Word8 d) { cart_ram[a] = d; }
static Word8 * lower_bank;
static Word8 read_lower_bank (Word16 a) { return lower_bank[a]; }
static void write_lower_bank (Word16 a, Word8 d) { /*lower_bank[a] = d;*/ }
static Word8 * upper_bank;
static Word8 read_upper_bank (Word16 a) { return upper_bank[a]; }
static void write_upper_bank (Word16 a, Word8 d) { /*upper_bank[a] = d;*/ }
//sram
//exprom
Word8 read_cart (Word16 addr)
{
    Display(2," -- cart read\n");
    Word8 res = 0x30;
    if ((addr >= 0x4020) && (addr < 0x6000)) // exprom
        res = 0x31;
    else if ((addr >= 0x6000) && (addr < 0x8000)) // sram
        res = read_cart_ram (addr&0x1FFF);
    else if ((addr >= 0x8000) && (addr < 0xC000)) // lower bank
        res = read_lower_bank(addr&0x3FFF);
    else if (addr >= 0xC000) // upper bank
        res = read_upper_bank(addr&0x3FFF);
    return res;
}
void write_cart (Word16 addr, Word8 data)
{
    Display(2," -- cart write\n");
    if ((addr >= 0x4020) && (addr < 0x6000)) {} // exprom
    else if ((addr >= 0x6000) && (addr < 0x8000)) // cart_ram
        write_cart_ram(addr&0x1FFF,data);
    else if ((addr >= 0x8000) && (addr < 0xC000)) // lower bank
        write_lower_bank(addr&0x3FFF, data);
    else if (addr >= 0xC000) // upper bank
        write_upper_bank(addr&0x3FFF, data);
}
void init_cart ()
{
    Display(2," -- cart init\n");
    cart_ram   = (Word8*) malloc (sizeof(Word8)*0x2000);
    chr_rom    = (Word8*) malloc (sizeof(Word8)*0x2000);
    lower_bank = (Word8*) malloc (sizeof(Word8)*0x4000);
    upper_bank = (Word8*) malloc (sizeof(Word8)*0x4000);
}
void free_cart ()
{
    Display(2," -- cart free\n");
    free(upper_bank);
    free(lower_bank);
    free(chr_rom);
    free(cart_ram);
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
        Display(2,"-- init cartridge lower bank\n");
        memcpy(lower_bank, &stream[16], 0x4000);
        Display(2,"-- init cartridge upper bank\n");
        memcpy(upper_bank, &stream[16+0x4000], 0x4000);
        Display(2,"-- init cartridge chr-rom\n");
        memcpy(chr_rom, &stream[16+0x8000], 0x2000);
        Display(2,"-- init ppu pattern table\n");
        map_ppu_pattern_table(chr_rom);
    }
}
