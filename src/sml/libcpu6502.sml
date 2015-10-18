(* (c) Alexandre Joannou, University of Cambridge *)

(* exporting functions *)
(*
- sml :
  val foo_export_wrapper = _export "ISA_foo" public : (real * char -> int) -> unit;
  val _ = foo_export_wrapper (ISA.foo)
- c :
  Int32 ISA_foo (Real64 x0, Char x1);
*)

val Next_export_wrapper = _export "cpu6502_Next" public : (unit -> unit) -> unit;
val _ = Next_export_wrapper (cpu6502.Next);

val SetRESET_export_wrapper = _export "cpu6502_SetRESET" public : (bool -> unit) -> unit;
val _ = SetRESET_export_wrapper (cpu6502.SetRESET);

val SetNMI_export_wrapper = _export "cpu6502_SetNMI" public : (bool -> unit) -> unit;
val _ = SetNMI_export_wrapper (cpu6502.SetNMI);

val SetIRQ_export_wrapper = _export "cpu6502_SetIRQ" public : (bool -> unit) -> unit;
val _ = SetIRQ_export_wrapper (cpu6502.SetIRQ);

(* importing functions *)
(*
- c :
  int ISA_ifc_bar (double d, char c);
- sml :
  val bar_ifc_import = _import "ISA_ifc_bar" external : real * char -> int;
  fun bar_ifc_import_wrapper (a, b) = bar_ifc_import (a, b) (* possible casting of arguments / return value*)
  val _ = ISA.bar := bar_ifc_import_wrapper
*)

val ReadMem_ifc_import = _import "cpu6502_ifc_ReadMem" external : Word16.word -> Word8.word;
fun ReadMem_ifc_import_wrapper (addr16, useless) =
  BitsN.fromInt(Word8.toInt(ReadMem_ifc_import (Word16.fromInt(BitsN.toInt(addr16)))), 8)
val _ = cpu6502.SMLReadMem := ReadMem_ifc_import_wrapper;

val WriteMem_ifc_import = _import "cpu6502_ifc_WriteMem" external : Word16.word * Word8.word -> unit;
fun WriteMem_ifc_import_wrapper (addr16, data8) =
  WriteMem_ifc_import (Word16.fromInt(BitsN.toInt(addr16)),Word8.fromInt(BitsN.toInt(data8)))
val _ = cpu6502.SMLWriteMem := WriteMem_ifc_import_wrapper;

val Display_ifc_import = _import "cpu6502_ifc_Display" external : (Int32.int * string) -> unit;
fun Display_ifc_import_wrapper (lvl, msg) = Display_ifc_import (Int32.fromInt(lvl), msg)
val _ = cpu6502.Display := Display_ifc_import_wrapper;
