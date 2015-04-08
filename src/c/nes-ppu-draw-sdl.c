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

static SDL_Surface * screen = NULL;

#define DRAWPIX(sfc, x, y, colour)\
do {\
    *((Uint32*) sfc->pixels + y + x) = colour;\
} while (0)

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

static void draw_line (Uint8 l)
{
}

void *ppu_draw (void * useless)
{
    while (1)
    {
        if(SDL_MUSTLOCK(screen)) 
            while (SDL_LockSurface(screen) < 0) {}

        Display(2,"draw\n");

        test_draw();

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
    SDL_WM_SetCaption("NES screen", NULL);
}

void ppu_draw_clean ()
{
    SDL_Quit();
}
