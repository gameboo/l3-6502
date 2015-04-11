#include "smlexport.h"
#include "utils.h"
#include <stdio.h>
#include <SDL/SDL.h>

extern Word8 * regs;
#define PPUCTRL     regs[0]
#define PPUMASK     regs[1]
#define PPUSTATUS   regs[2]
#define OAMADDR     regs[3]
#define OAMDATA     regs[4]
#define PPUSCROLL   regs[5]
#define PPUADDR     regs[6]
#define PPUDATA     regs[7]

extern Word8 * palettes_vram;
extern Word8 * names_vram;
extern Word8 * patterns_vram;
extern Word8 * spr_vram;
extern Word16 vram_addr;

static SDL_Surface * screen = NULL;
static Uint32 * sys_palette;

void init_sys_palette(Uint32* pal)
{
    pal[0x00] = SDL_MapRGB(screen->format,0x75,0x75,0x75);
    pal[0x01] = SDL_MapRGB(screen->format,0x27,0x1b,0x8f);
    pal[0x02] = SDL_MapRGB(screen->format,0x00,0x00,0xab);
    pal[0x03] = SDL_MapRGB(screen->format,0x47,0x00,0x9f);
    pal[0x04] = SDL_MapRGB(screen->format,0x8f,0x00,0x77);
    pal[0x05] = SDL_MapRGB(screen->format,0xab,0x00,0x13);
    pal[0x06] = SDL_MapRGB(screen->format,0xa7,0x00,0x00);
    pal[0x07] = SDL_MapRGB(screen->format,0x7f,0x0b,0x00);
    pal[0x08] = SDL_MapRGB(screen->format,0x43,0x2f,0x00);
    pal[0x09] = SDL_MapRGB(screen->format,0x00,0x47,0x00);
    pal[0x0a] = SDL_MapRGB(screen->format,0x00,0x51,0x00);
    pal[0x0b] = SDL_MapRGB(screen->format,0x00,0x3f,0x17);
    pal[0x0c] = SDL_MapRGB(screen->format,0x1b,0x3f,0x5f);
    pal[0x0d] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x0e] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x0f] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x10] = SDL_MapRGB(screen->format,0xbc,0xbc,0xbc);
    pal[0x11] = SDL_MapRGB(screen->format,0x00,0x73,0xef);
    pal[0x12] = SDL_MapRGB(screen->format,0x23,0x3b,0xef);
    pal[0x13] = SDL_MapRGB(screen->format,0x83,0x00,0xf3);
    pal[0x14] = SDL_MapRGB(screen->format,0xbf,0x00,0xbf);
    pal[0x15] = SDL_MapRGB(screen->format,0xe7,0x00,0x5b);
    pal[0x16] = SDL_MapRGB(screen->format,0xdb,0x2b,0x00);
    pal[0x17] = SDL_MapRGB(screen->format,0xcb,0x4f,0x0f);
    pal[0x18] = SDL_MapRGB(screen->format,0x8b,0x73,0x00);
    pal[0x19] = SDL_MapRGB(screen->format,0x00,0x97,0x00);
    pal[0x1a] = SDL_MapRGB(screen->format,0x00,0xab,0x00);
    pal[0x1b] = SDL_MapRGB(screen->format,0x00,0x93,0x3b);
    pal[0x1c] = SDL_MapRGB(screen->format,0x00,0x83,0x8b);
    pal[0x1d] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x1e] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x1f] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x20] = SDL_MapRGB(screen->format,0xff,0xff,0xff);
    pal[0x21] = SDL_MapRGB(screen->format,0x3f,0xbf,0xff);
    pal[0x22] = SDL_MapRGB(screen->format,0x5f,0x97,0xff);
    pal[0x23] = SDL_MapRGB(screen->format,0xa7,0x8b,0xfd);
    pal[0x24] = SDL_MapRGB(screen->format,0xf7,0x7b,0xff);
    pal[0x25] = SDL_MapRGB(screen->format,0xff,0x77,0xb7);
    pal[0x26] = SDL_MapRGB(screen->format,0xff,0x77,0x63);
    pal[0x27] = SDL_MapRGB(screen->format,0xff,0x9b,0x3b);
    pal[0x28] = SDL_MapRGB(screen->format,0xf3,0xbf,0x3f);
    pal[0x29] = SDL_MapRGB(screen->format,0x83,0xd3,0x13);
    pal[0x2a] = SDL_MapRGB(screen->format,0x4f,0xdf,0x4b);
    pal[0x2b] = SDL_MapRGB(screen->format,0x58,0xf8,0x98);
    pal[0x2c] = SDL_MapRGB(screen->format,0x00,0xeb,0xdb);
    pal[0x2d] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x2e] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x2f] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x30] = SDL_MapRGB(screen->format,0xff,0xff,0xff);
    pal[0x31] = SDL_MapRGB(screen->format,0xab,0xe7,0xff);
    pal[0x32] = SDL_MapRGB(screen->format,0xc7,0xd7,0xff);
    pal[0x33] = SDL_MapRGB(screen->format,0xd7,0xcb,0xff);
    pal[0x34] = SDL_MapRGB(screen->format,0xff,0xc7,0xff);
    pal[0x35] = SDL_MapRGB(screen->format,0xff,0xc7,0xdb);
    pal[0x36] = SDL_MapRGB(screen->format,0xff,0xbf,0xb3);
    pal[0x37] = SDL_MapRGB(screen->format,0xff,0xdb,0xab);
    pal[0x38] = SDL_MapRGB(screen->format,0xff,0xe7,0xa3);
    pal[0x39] = SDL_MapRGB(screen->format,0xe3,0xff,0xa3);
    pal[0x3a] = SDL_MapRGB(screen->format,0xab,0xf3,0xbf);
    pal[0x3b] = SDL_MapRGB(screen->format,0xb3,0xff,0xcf);
    pal[0x3c] = SDL_MapRGB(screen->format,0x9f,0xff,0xf3);
    pal[0x3d] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x3e] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
    pal[0x3f] = SDL_MapRGB(screen->format,0x00,0x00,0x00);
}

#define DRAWPIX(sfc, x, y, colour)\
do {\
    *((Uint32*) sfc->pixels + y + x) = colour;\
} while (0)

/*
static void test_draw ()
{
    int x, y, ytimesw;
    static int h = 0;
    for (y = 0; y < screen->h; y++ )
    {
        ytimesw = y*screen->pitch/4;
        for (x = 0; x < screen->w; x++ )
        {
            DRAWPIX(screen, x, ytimesw, SDL_MapRGB(screen->format,(x*x)/256+3*y+h, (y*y)/256+x+h, h));
            h++;
        }
    }
}
*/

// accessing vram addr fields
#define CURRIDX(x)      (x & 0x0FFF)
#define TABLENBR(x)     ((x & 0x0C00)>>10)
#define XSCROLL(x)      (x & 0x001F)
#define YSCROLL(x)      ((x & 0x03E0)>>5)
#define FINEYSCROLL(x)  ((x & 0x7000)>>12)

static void draw_tile_line()
{
    Word8 tile_nbr = names_vram[CURRIDX(vram_addr)+0x400*TABLENBR(vram_addr)];
    Display(3,"Found tile number %d\n",tile_nbr);
    Word8 pattern_tbl_offset = ((PPUCTRL & 0x8) >> 3)*0x1000;
    Display(3,"Found pattern_tbl_offset 0x%4x\n",pattern_tbl_offset);
    Word8 * tile_ptr = &patterns_vram[(tile_nbr<<4)+pattern_tbl_offset];// 16 bytes per tyle so << 4
    Display(3,"Found tile_ptr\n");
    int i = 0;
    Word8 lobyte = tile_ptr[FINEYSCROLL(vram_addr)];
    Display(3,"Found lobyte 0x%2x\n",lobyte);
    Word8 hibyte = tile_ptr[FINEYSCROLL(vram_addr)+16];
    Display(3,"Found hibyte 0x%2x\n",hibyte);
    Word8 clr_idx_hi2 = 0; // TODO in the attribute table
    Word8 clr_idx_lo2 = 0;
    Word8 clr_idx = 0;
    Uint32 color = 0;
    for (i=0;i<8;i++)
    {
        Display(3,"Drawing pixel %d\n",i);
        clr_idx_lo2 = ((lobyte>>i)&0x1)|(((hibyte>>i)&0x1)<<1);
        clr_idx = (clr_idx_hi2<<2)|clr_idx_lo2;
        color = sys_palette[palettes_vram[clr_idx&0xf]&0x3F];
        DRAWPIX(screen,XSCROLL(vram_addr)*8+i,YSCROLL(vram_addr)*8+FINEYSCROLL(vram_addr), color);
    }
}

static void draw_screen ()
{
    int i = 0;
    int j = 0;
    for (i=0;i<240;i++)
    {
        Display(3,"Drawing line %d\n",i);
        for (j=0;j<32;j++)
        {
            Display(3,"Drawing tile %d\n",j);
            draw_tile_line();
            vram_addr ++;
        }
    }
}

void *ppu_draw (void * useless)
{
    while (1)
    {
        if(SDL_MUSTLOCK(screen)) 
            while (SDL_LockSurface(screen) < 0) {}

        Display(2,"draw\n");

        //test_draw();
        draw_screen();

        if(SDL_MUSTLOCK(screen)) SDL_UnlockSurface(screen);
        SDL_Flip(screen);
        //SDL_Delay(50);
    }
}

void ppu_draw_init ()
{
    SDL_Init(SDL_INIT_VIDEO);
    screen = SDL_SetVideoMode(256, 240, 32, SDL_HWSURFACE);
    if (screen == NULL)
    {
        fprintf (stderr, "Failed to create NES screen: %s\n", SDL_GetError());
        exit(EXIT_FAILURE);
    }
    sys_palette = (Uint32*) malloc (sizeof(Uint32)*0x40);
    init_sys_palette(sys_palette);
    SDL_WM_SetCaption("NES screen", NULL);
}

void ppu_draw_clean ()
{
    free(sys_palette);
    SDL_Quit();
}
