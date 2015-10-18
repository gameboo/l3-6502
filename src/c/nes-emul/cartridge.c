#include "libcpu6502.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>

extern Word8 * map_ppu_pattern_table(Word8*);

///////////////
// cartridge //
///////////////

Word8 * cart_chr_mem;
Word8 * cart_ram;
Word8 * cart_lower_pgr_bank;
Word8 * cart_upper_pgr_bank;

static Word8 *  raw_header;
static Word8 *  raw_trainer;
static Word8 ** raw_pgr_rom;
static Word8 ** raw_chr_rom;
static Word8 *  raw_sram;

//sram
//exprom
Word8 read_cart (Word16 addr)
{
    Display(2," -- cart read\n");
    Word8 res = 0x30;
    if ((addr >= 0x4020) && (addr < 0x6000)) // exprom
        res = 0x31;
    else if ((addr >= 0x6000) && (addr < 0x8000)) // sram
        res = cart_ram[addr&0x1FFF];
    else if ((addr >= 0x8000) && (addr < 0xC000)) // lower bank
        res = cart_lower_pgr_bank[addr&0x3FFF];
    else if (addr >= 0xC000) // upper bank
        res = cart_upper_pgr_bank[addr&0x3FFF];
    return res;
}
void write_cart (Word16 addr, Word8 data)
{
    Display(2," -- cart write\n");
    if ((addr >= 0x4020) && (addr < 0x6000)) // exprom
    {
        Display(1, "Write to exprom !!!");
    }
    else if ((addr >= 0x6000) && (addr < 0x8000)) // cart_ram
        cart_ram[addr&0x1FFF] = data;
    else if ((addr >= 0x8000) && (addr < 0xC000)) // lower bank
    {
        Display(1, "Write to prg-rom lower bank !!!");
        //cart_lower_pgr_bank[addr&0x3FFF] = data;
    }
    else if (addr >= 0xC000) // upper bank
    {
        Display(1, "Write to prg-rom upper bank !!!");
        //cart_upper_pgr_bank[addr&0x3FFF] = data;
    }
}

/*
typedef struct
{
    char mapper_low_nibble: 4;
    char VRAM_opt_hi: 1;
    char trainer: 1;
    char PRG_RAM: 1;
    char VRAM_opt_low: 1;
} flag6_t;

typedef struct
{
    char mapper_hi_nibble: 4;
    char NES2dot0: 2;
    char PlayChoice_10: 1;
    char VS_Unisystem: 1;
} flag7_t;

typedef struct
{
    char reserved: 7;
    char PAL_NTSC: 1;
} flag9_t;

typedef struct
{
    char unknown0: 2;
    char BusConflicts: 1;
    char PRG_RAM: 1;
    char unknown1: 2;
    char TV_system: 2;
} flag10_t;
*/

typedef char flag6_t;
typedef char flag7_t;
typedef char flag9_t;
typedef char flag10_t;

typedef struct
{
    char magic[4];
    char PRGROM_SZ_16KB;
    char CHRROM_SZ_8KB;
    flag6_t flag6;
    flag7_t flag7;
    char PRGRAM_SZ_8KB;
    flag9_t flag9;
    flag10_t flag10;
    char zeros[5];
} iNESHeader_t;

static iNESHeader_t * header;

#define iNES_trainer_present(header)\
    ((header->flag6)&0x04)

#define iNES_mapper(header)\
    (((header->flag7)&0xF0) | ((header->flag6)>>4))

#define HEADER_SZ   16
#define TRAINER_SZ  512
#define SZ_16KB     16384
#define SZ_8KB      8192
#define SRAM_SZ     8192

void LoadiNES ( const char * filename )
{
    Display(2,"LoadiNES\n");
    FILE * fp = fopen(filename, "rb");
    if (fp)
    {
        raw_header = (Word8*) malloc (HEADER_SZ*sizeof(Word8));
        size_t header_read = fread (raw_header, HEADER_SZ, 1, fp);
        if (header_read == 1)
        {
            header = (iNESHeader_t*) raw_header ;

            Display(3, " >>>> iNES header for %s :\n", filename);
            Display(3, "\traw [");
            for (int i = 0 ; i < HEADER_SZ-1; i++) Display(3, "%02x:",raw_header[i]);
            Display(3, "%02x]\n",raw_header[HEADER_SZ-1]);
            Display(3, "\tmagic = %s\n", header->magic);
            Display(3, "\tPRGROM_SZ_16KB = 0x%02x\n", header->PRGROM_SZ_16KB);
            Display(3, "\tCHRROM_SZ_8KB = 0x%02x\n", header->CHRROM_SZ_8KB);
            Display(3, "\tflag6 = 0x%02x\n", header->flag6);
            Display(3, "\tflag7 = 0x%02x\n", header->flag7);
            Display(3, "\tPRGRAM_SZ_8KB = 0x%02x\n", header->PRGRAM_SZ_8KB);
            Display(3, "\tflag9 = 0x%02x\n", header->flag9);
            Display(3, "\tflag10 = 0x%02x\n", header->flag10);
            Display(3, "\tzeros = %s\n", header->zeros);

            if (iNES_trainer_present(header))
            {
                raw_trainer = (Word8*) malloc (TRAINER_SZ*sizeof(Word8));
                size_t trainer_read = fread (raw_trainer, TRAINER_SZ, 1, fp);
                if (trainer_read == 1)
                {
                    //TODO
                }
                else
                {
                    fprintf(stderr,
                        "fread failed to read the trainer.\
                        Read %zu times TRAINER_SZ bytes\n", trainer_read);
                    abort();
                }
            }
            else Display(3,"No trainer after header. Continue...\n");
            if(header->PRGROM_SZ_16KB >= 1)
            {
                raw_pgr_rom = (Word8**) malloc (header->PRGROM_SZ_16KB*sizeof(Word8*));
                for (int i = 0; i < header->PRGROM_SZ_16KB; i++)
                {
                    raw_pgr_rom[i] = (Word8*) malloc (SZ_16KB * sizeof(Word8));
                    size_t pgr_rom_read = fread (raw_pgr_rom[i], SZ_16KB, 1, fp);
                    if (pgr_rom_read != 1)
                    {
                        fprintf(stderr,
                            "fread failed to read prg_rom %d.\
                            Read %zu times SZ_16KB bytes\n", i, pgr_rom_read);
                        abort();
                    }
                    else Display(3, "Read PGR_ROM %d\n", i);
                }
            }
            else
            {
                fprintf(stderr,
                    "No PGR_ROM in iNES file!\n");
                abort();
            }
            if(header->CHRROM_SZ_8KB >= 1)
            {
                raw_chr_rom = (Word8**) malloc (header->CHRROM_SZ_8KB*sizeof(Word8*));
                for (int i = 0; i < header->CHRROM_SZ_8KB; i++)
                {
                    raw_chr_rom[i] = (Word8*) malloc (SZ_8KB * sizeof(Word8));
                    size_t chr_rom_read = fread (raw_chr_rom[i], SZ_8KB, 1, fp);
                    if (chr_rom_read != 1)
                    {
                        fprintf(stderr,
                            "fread failed to read chr_rom %d.\
                            Read %zu times SZ_8KB bytes\n", i, chr_rom_read);
                        abort();
                    }
                    else Display(3, "Read CHR_ROM %d\n", i);
                }
            }
            else
            {
                fprintf(stderr,
                    "No PGR_ROM in iNES file!\n");
                abort();
            }
            raw_sram = (Word8*) malloc (SRAM_SZ*sizeof(Word8));
            switch(iNES_mapper(header))
            {
                case 0:
                    cart_upper_pgr_bank = raw_pgr_rom[1];
                    cart_lower_pgr_bank = raw_pgr_rom[0];
                    cart_ram            = raw_sram;
                    cart_chr_mem        = raw_chr_rom[0];
                    map_ppu_pattern_table(cart_chr_mem);
                    break;
                default:
                fprintf(stderr,
                    "Unsupported iNES mapper %d\n", iNES_mapper(header));
                abort();
            }
        }
        else
        {
            fprintf(stderr,
                "fread failed to read the ines header.\
                Read %zu times HEADER_SZ bytes\n", header_read);
            abort();
        }
    }
    else
    {
        fprintf(stderr, "fopen failed to open file %s in \"rb\" mode\n", filename);
        abort();
    }
}

void init_cart (char * filename)
{
    Display(2," -- cart init\n");
    LoadiNES(filename);
}

void free_cart ()
{
    Display(2," -- cart free\n");
    if(header->CHRROM_SZ_8KB >= 1)
    {
        for (int i = 0; i < header->CHRROM_SZ_8KB; i++)
            free(raw_chr_rom[i]);
        free(raw_chr_rom);
    }
    if(header->PRGROM_SZ_16KB >= 1)
    {
        for (int i = 0; i < header->PRGROM_SZ_16KB; i++)
            free(raw_pgr_rom[i]);
        free(raw_pgr_rom);
    }
    if (iNES_trainer_present(header))
        free(raw_trainer);
    free(raw_sram);
    free(raw_header);
}
