---------------------------------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge
---------------------------------------------------------------------------

-- these wrappers use a dummy unit to force L3 to generate sml functions as
-- opposed to maps

declare SMLReadMem  :: (bits(16) * unit) -> bits(8)
declare SMLWriteMem :: bits(16) * bits(8) -> unit

bits(8)    ReadMem  (addr :: bits(16)) = SMLReadMem (addr, ())
ByteStream Fetch    (addr :: bits(16)) = list {SMLReadMem (addr, ()), SMLReadMem (addr+1, ()), SMLReadMem (addr+2, ())}
unit       WriteMem (addr :: bits(16), data :: bits(8)) = SMLWriteMem (addr, data)
