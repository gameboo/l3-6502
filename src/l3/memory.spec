---------------------------------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge
---------------------------------------------------------------------------

-- these wrappers use a dummy unit to force L3 to generate sml functions as
-- opposed to maps

declare SMLReadMem  :: (bits(16) * unit) -> bits(8)
declare SMLFetch    :: (bits(16) * unit) -> ByteStream
declare SMLWriteMem :: bits(16) * bits(8) -> unit
declare SMLInitMem  :: unit -> unit

bits(8)    ReadMem  (addr :: bits(16)) = SMLReadMem (addr, ())
ByteStream Fetch    (addr :: bits(16)) = SMLFetch (addr, ())
unit       WriteMem (addr :: bits(16), data :: bits(8)) = SMLWriteMem (addr, data)
unit       InitMem  () = SMLInitMem ()
