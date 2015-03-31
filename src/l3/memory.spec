---------------------------------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge
---------------------------------------------------------------------------

declare MEM :: bits(16) -> bits(8)

ByteStream Fetch = list { MEM(&PC), MEM(&PC+1), MEM(&PC+2) }
bits(8) ReadMem (addr::bits(16)) = MEM(addr)
unit WriteMem (addr::bits(16), data::bits(8)) = MEM(addr) <- data

unit initMemory = MEM <- InitMap (UNKNOWN)
