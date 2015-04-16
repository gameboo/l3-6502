(* (c) Alexandre Joannou, University of Cambridge *)

(* Plug into C functions *)

val CReadMem     = _import "CReadMem"     public: Word16.word -> Word8.word;
val CWriteMem    = _import "CWriteMem"    public: Word16.word * Word8.word -> unit;
val CLoadiNES    = _import "CLoadiNES"    public: Word8Vector.vector * Word32.word -> unit;
val CInitMem     = _import "CInitMem"     public: unit -> unit;
val CFreeMem     = _import "CFreeMem"     public: unit -> unit;
val CStepMem     = _import "CStepMem"     public: Word64.word -> unit;

val setupCSetRESET = _export "CSetRESET": (bool -> unit) -> unit;
val setupCSetNMI   = _export "CSetNMI"  : (bool -> unit) -> unit;
val setupCSetIRQ   = _export "CSetIRQ"  : (bool -> unit) -> unit;
val doSetRESET = ref false
val doSetNMI   = ref false
val doSetIRQ   = ref false
val _ = setupCSetRESET (fn (b) => doSetRESET := b)
val _ = setupCSetNMI   (fn (b) => doSetNMI   := b)
val _ = setupCSetIRQ   (fn (b) => doSetIRQ   := b)

val (_, CSet_display_lvl) = _symbol "display_lvl" alloc: (unit -> Int32.int) * (Int32.int -> unit);

fun read_mem (addr16, useless) =
  BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)))), 8)
fun write_mem (addr16, data8) =
  CWriteMem(Word16.fromInt(BitsN.toInt(addr16)),Word8.fromInt(BitsN.toInt(data8)))
fun fetch_inst (addr16, useless) =
[BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)))), 8),
 BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)+1))), 8),
 BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)+2))), 8)]

fun init_mem (inesfile) =
(
  CInitMem ();
  CLoadiNES (inesfile, Word32.fromInt(Vector.length(inesfile)))
)

fun free_mem () = CFreeMem()

(* helpers *)
fun failExit s = ( print (s ^ "\n"); OS.Process.exit OS.Process.failure )

(* Initialising L3 components *)

fun init_cpu6505 () =
(
  (* Memory operations *)
  cpu6502.SMLReadMem  := read_mem;
  cpu6502.SMLWriteMem := write_mem;
  cpu6502.SMLFetch    := fetch_inst;
  (* 6502 init function *)
  let
    val lo = BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(0xFFFC))),8)
    val hi = BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(0xFFFD))),8)
  in
    cpu6502.Init (BitsN.concat([hi,lo]))
  end
)

fun init_system (inesfile) =
(
  init_mem (inesfile);
  init_cpu6505 ()
)

fun clean_system () =
(
  free_mem ()
)

(* Actual simulation *)



fun exec_loop (inst_nb) =
(
  cpu6502.SetRESET(!doSetRESET);
  cpu6502.SetNMI(!doSetNMI);
  cpu6502.SetIRQ(!doSetIRQ);
  cpu6502.Next();
  doSetRESET := false;
  doSetNMI   := false;
  doSetIRQ   := false;
  CStepMem(inst_nb);
  exec_loop (inst_nb+Word64.fromInt(1))
)

fun run (inesfile) =
(
  init_system (inesfile);

  exec_loop (Word64.fromInt(0));

  clean_system ()
)

(* Option parsing code, taken from https://github.com/acjf3/l3mips *)

fun printUsage () =
print ("\n\
\6502 emulator (based on an L3 specification)\n\
\http://www.cl.cam.ac.uk/~acjf3/l3\n\n\
\usage: " ^ OS.Path.file (CommandLine.name ()) ^ " [arguments] <iNES file>\n\n\
\arguments:\n\
\  -d or --display <lvl>    Set verbosity level (default -1, i.e. no display)\n\
\  -h or --help             TODO Print this message\n\n")

fun getNumber s =
  case IntExtra.fromString s of
    SOME n => n
  | NONE   => failExit ("Bad number: " ^ s)

fun getArguments () =
  List.map (
    fn "-h" => "--help"
    |  "-d" => "--display"
    |  s    => s)
    (CommandLine.arguments ())

fun processOption (s: string) =
  let
    fun loop acc =
      fn a :: b :: r =>
        if a = s then (SOME b, List.rev acc @ r)
        else loop (a :: acc) (b :: r)
      |  r => (NONE, List.rev acc @ r)
  in
    loop []
  end

val () =
  case getArguments () of
    ["--help"] => printUsage ()
  | l =>
      let
        val (disp, l) = processOption "--display" l
        val () = case Option.map getNumber disp of
                    NONE       =>
                    (cpu6502.Display := (fn (dlvl, str) => ());CSet_display_lvl(Int32.fromInt(0-1)))
                  | SOME lvl   => (
                      if lvl >= 0 then
                        cpu6502.Display := ( fn (dlvl, str) => if dlvl <= lvl then (
                          TextIO.flushOut TextIO.stdOut;
                          print(str^"\n");
                          TextIO.flushOut TextIO.stdOut) else ()
                        )
                      else
                        cpu6502.Display := (fn (dlvl, str) => ());
                      CSet_display_lvl (Int32.fromInt(lvl))
                    )
        val istream   = (BinIO.openIn o hd) l
        val vec       = BinIO.inputAll istream
        val ()        = BinIO.closeIn istream
      in
        run(vec)
      end
