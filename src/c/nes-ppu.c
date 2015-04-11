#include "smlexport.h"
#include "utils.h"
#include <stdio.h>
#include <pthread.h>

Word8 * regs;
#define PPUCTRL     regs[0]
#define PPUMASK     regs[1]
#define PPUSTATUS   regs[2]
#define OAMADDR     regs[3]
#define OAMDATA     regs[4]
#define PPUSCROLL   regs[5]
#define PPUADDR     regs[6]
#define PPUDATA     regs[7]

#define PPU_OFFSET(x) ((x) & 0x0007)

static Word8 write_latch;
static int ppuscroll_write_count;
static Word8 hoffset_latch;
static Word8 voffset_latch;
static int ppuaddr_write_count;
Word16 vram_addr;

//////////
// VRAM //
//////////
Word8 * palettes_vram;
Word8 * names_vram;
Word8 * patterns_vram;
static inline Word8 getVRAM (Word16 addr)
{
    Word16 masked_addr = addr & 0x3FFF;
    if (masked_addr < 0x2000)
        return patterns_vram[masked_addr];
    else if ((masked_addr >= 0x2000) && (masked_addr < 0x3F00))
        return names_vram[masked_addr&0x00FF];
    else // between 0x3F00 and 0x4000
        return palettes_vram[masked_addr&0x001F];
}
static inline void setVRAM (Word16 addr, Word8 data)
{
    Word16 masked_addr = addr & 0x3FFF;
    if (masked_addr < 0x2000)
        patterns_vram[masked_addr] = data;
    else if ((masked_addr >= 0x2000) && (masked_addr < 0x3F00))
        names_vram[masked_addr&0x00FF] = data;
    else // between 0x3F00 and 0x4000
        palettes_vram[masked_addr&0x001F] = data;
}

////////////////
// Sprite RAM //
////////////////
Word8 * spr_vram;
#define OAM(x) (spr_vram[(x) & 0xFF])

/////////////////////
// ppu draw thread //
/////////////////////
static pthread_t ppu_draw_thread;
extern void *ppu_draw (void * useless);

///////////////////////
// nes-mem interface //
///////////////////////
Word8 read_ppu (Word16 addr)
{
    Word8 res = 0;
    Display(2," -- ppu read\n");
    switch PPU_OFFSET(addr)
    {
        case 2: // PPUSTATUS
            res = PPUSTATUS & 0xE0;
            res = res | (write_latch & 0x1F);
            // clear VBlank bit
            PPUSTATUS &= 0x7F;
            // clear PPUSCROLL
            PPUSCROLL = 0;
            // clear PPUADDR
            PPUADDR   = 0;
            break;
        case 4: // OAMDATA
            res = OAMDATA;
            break;
        case 7: // PPUDATA
            // XXX the first read is supposed to be invalid and buffer the
            // data... What does that mean on the increment of vram_addr ?
            // Also, "does not apply to color palettes"
            res = getVRAM(vram_addr);
            // increment vram_addr
            vram_addr = (PPUCTRL%0x04) ? (vram_addr+32)%0xFFFF:(vram_addr+1)%0xFFFF;
            break;
        default:
            Display(2," -- attempted read ppu reg %d, write only\n",PPU_OFFSET(addr));
            res = regs[PPU_OFFSET(addr)];
            break;
    }
    return res;
}

void write_ppu (Word16 addr, Word8 data)
{
    Display(2," -- ppu write\n");
    switch PPU_OFFSET(addr)
    {
        case 0: // PPUCTRL
            PPUCTRL = data;
            // when bit 7 is set, send NMI
            if (data & 0x80) CSetNMI (1);
            else CSetNMI (0);
            break;
        case 1: // PPUMASK
            PPUMASK = data;
            break;
        case 3: // OAMADDR
            OAMADDR = data;
            break;
        case 4: // OAMDATA
            OAMDATA = data;
            // writes data to OAM
            OAM(OAMADDR) = data;
            // increment OAMADDR
            OAMADDR = (OAMADDR + 1);
            break;
        case 5: // PPUSCROLL
            PPUSCROLL = data;
            // set the appropriate offset register
            if (ppuscroll_write_count % 2)
                voffset_latch = data;
            else
                hoffset_latch = data;
            // update count for next write
            ppuscroll_write_count++;
            break;
        case 6: // PPUADDR
            PPUADDR = data;
            // set the address register
            Word16 mask = (ppuaddr_write_count % 2) ? 0xFF00 : 0x00FF;
            Word16 addrbyte = (ppuaddr_write_count % 2) ? data : data << 8;
            vram_addr = (vram_addr & mask) | addrbyte;
            // update count for next write
            ppuaddr_write_count++;
            break;
        case 7: // PPUDATA
            PPUDATA = data;
            // writes data to VRAM
            setVRAM(vram_addr, data);
            // increment vram_addr
            vram_addr = (PPUCTRL%0x04) ? (vram_addr+32)%0xFFFF:(vram_addr+1)%0xFFFF;
            break;
        default:
            Display(2," -- ppu reg %d write only\n",PPU_OFFSET(addr));
            break;
    }
    write_latch = data; 
}

Word8 * map_ppu_pattern_table(Word8* new_chr_mem)
{
    Display(3,"backup old\n");
    Word8 * old = patterns_vram;
    Display(3,"replace with new\n");
    patterns_vram = new_chr_mem;
    Display(3,"return old\n");
    return old;
}

void init_ppu ()
{
    Display(2," -- ppu init\n");
    spr_vram = (Word8*) malloc (sizeof(Word8)*0x0100); // 256 bytes
    patterns_vram = (Word8*) malloc (sizeof(Word8)*0x2000); // 8K
    names_vram = (Word8*) malloc (sizeof(Word8)*0x1000); // 4K //XXX supposed to be 2K and potentioally another 2K in the cartridge
    palettes_vram = (Word8*) malloc (sizeof(Word8)*0x0020); // 32 bytes
    regs = (Word8*) malloc (sizeof(Word8)*8);
    ppu_draw_init();
    if (pthread_create(&ppu_draw_thread, NULL, ppu_draw, NULL))
    {
        fprintf(stderr, "Error creating ppu draw thread\n");
        return 1;
    }
}

void free_ppu ()
{
    Display(2," -- ppu free\n");
    ppu_draw_clean();
    free(regs);
    free(palettes_vram);
    free(names_vram);
    free(patterns_vram);
    free(spr_vram);

    write_latch = 0;
    ppuscroll_write_count = 0;
    hoffset_latch = 0;
    voffset_latch = 0;
    ppuaddr_write_count = 0;
    vram_addr = 0;
}
