#include "smlexport.h"
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

static SDL_Surface * screen = NULL;

void *ppu_draw (void * useless)
{
    static int r = 0;
    static int g = 0;
    static int b = 0;
    static int i =0;
    while (1)
    {
        printf("draw (%3d,%3d,%3d)\n",r,g,b);
        SDL_FillRect(screen, NULL, SDL_MapRGB(screen->format, r, g, b));
        SDL_Flip(screen);
        //SDL_Delay(1);
        r+=25;
        r%=256;
        if (i % 4) {g+=25;g%=256;}
        if (i % 8) {b+=25;b%=256;}
        i++;
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
    SDL_WM_SetCaption("NES screen", NULL);
}

void ppu_draw_clean ()
{
    SDL_Quit();
}
