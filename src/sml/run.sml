(* (c) Alexandre Joannou, University of Cambridge *)

(* Plug into C functions *)

val CReadMem  = _import "CReadMem"  public: Word16.word -> Word8.word;
val CWriteMem = _import "CWriteMem" public: Word16.word * Word8.word -> unit;
val CInitMem  = _import "CInitMem"  public: unit -> unit;

fun read_mem (addr16, useless) =
  BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)))), 8)
fun write_mem (addr16, data8) =
  CWriteMem(Word16.fromInt(BitsN.toInt(addr16)),Word8.fromInt(BitsN.toInt(data8)))
fun fetch_inst (addr16, useless) =
[BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)))), 8),
 BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)+1))), 8),
 BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)+2))), 8)]
fun init_mem () = CInitMem()

(* Initialising L3 components*)

fun init_cpu6505 () =
(
  (* Memory operations *)
  cpu6502.SMLReadMem  := read_mem;
  cpu6502.SMLWriteMem := write_mem;
  cpu6502.SMLFetch    := fetch_inst;
  cpu6502.SMLInitMem  := init_mem;
  (* Debug / Display *)
  cpu6502.Display     := (fn str => print (str^"\n"));
  (* 6502 init function *)
  cpu6502.Init ()
)

(* Actual simulation *)

fun exec_loop () = (cpu6502.Next(); exec_loop ())

val () =
(
  init_cpu6505 ();
  cpu6502.SetRESET(true);
  cpu6502.Next ();
  cpu6502.SetRESET(false);
  exec_loop ()
)
