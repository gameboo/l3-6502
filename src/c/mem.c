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

void CInitMem ()
{
    mem = (Word8 *) malloc (sizeof(Word8)*(2^16));
}
