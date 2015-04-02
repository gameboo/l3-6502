#include "smlexport.h"

Word8 * mem;

Word8 CReadMem ( Word16 addr )
{
    return mem[addr];
}

void CWriteMem ( Word16 addr, Word8 data )
{
    mem[addr] = data;
}

void CWriteStream ( Word16 addr, Pointer stream , Word32 size )
{
    Word32 i;
    for (i=0; i < size; i++)
    {
        mem[addr+i] = stream[i];
    }
}

void CInitMem ()
{
    mem = (Word8 *) malloc (sizeof(Word8)*(2^16));
}
