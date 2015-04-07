#include "smlexport.h"
#include "utils.h"
#include <stdio.h>

Word8 * mem;

Word8 CReadMem ( Word16 addr )
{
    Display(2,"CReadMem @0x%04x = 0x%02x\n", addr, mem[addr]);
    return mem[addr];
}

void CWriteMem ( Word16 addr, Word8 data )
{
    Display(2,"CWriteMem @0x%04x <- 0x%02x\n", addr, data);
    mem[addr] = data;
}

void CWriteStream ( Word16 addr, Pointer stream , Word32 size )
{
    Display(2,"CWriteStream @ 0x%04x\n", addr);
    Word32 i;
    for (i=0; i < size; i++)
    {
        mem[(addr+i)%0xFFFF] = stream[i];
    }
}

void CInitMem ()
{
    Display(2,"CInitMem\n");
    mem = (Word8 *) malloc (sizeof(Word8)*(2^16));
}

void CFreeMem ()
{
    Display(2,"CFreeMem\n");
    free(mem);
}
