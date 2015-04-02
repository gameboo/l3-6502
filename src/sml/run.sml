(* (c) Alexandre Joannou, University of Cambridge *)

fun read_mem (addr16, useless) = BitsN.fromInt (0, 8)
fun write_mem (addr16, data8) = ()
fun fetch_inst addr16 = [BitsN.fromInt(0, 8),BitsN.fromInt(0x88, 8),BitsN.fromInt(0x88, 8)]
fun init_mem () = ()

fun init_cpu6505 () =
(
  (* Memory operations *)
  cpu6502.SMLReadMem  := read_mem;
  cpu6502.SMLWriteMem := write_mem;
  cpu6502.SMLFetch    := fetch_inst;
  cpu6502.SMLInitMem  := init_mem;
  (* Debug / Display *)
  cpu6502.Display  := (fn str => print (str^"\n"))
)

val () =
(
  init_cpu6505 ();
  cpu6502.Next ();
  cpu6502.Next ();
  cpu6502.Next ();
  cpu6502.Next ();
  cpu6502.Next ()
)
