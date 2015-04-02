(* (c) Alexandre Joannou, University of Cambridge *)

fun read_mem addr16 = BitsN.fromInt (0, 8)
fun write_mem addr16 data8 = ()
val fetch_inst addr16 = [BitsN.fromInt(0, 8),BitsN.fromInt(0x88, 8),BitsN.fromInt(0x88, 8)]
val init_mem = ()

val init_cpu6505 =
(
  (* Memory operations *)
  (*cpu6502.ReadMem  := read_mem;*)
  cpu6502.WriteMem := write_mem;
  (*cpu6502.Fetch    := fetch_inst;*)
  cpu6502.InitMem  := init_mem;
  (* Debug / Display *)
  cpu6502.Display  := (fn str => print (str^"\n"))
)

val () =
(
  cpu6502.Next ();
  cpu6502.Next ();
  cpu6502.Next ();
  cpu6502.Next ();
  cpu6502.Next ()
)
