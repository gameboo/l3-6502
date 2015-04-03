(* (c) Alexandre Joannou, University of Cambridge *)

(* Plug into C functions *)

val CReadMem     = _import "CReadMem"  public: Word16.word -> Word8.word;
val CWriteMem    = _import "CWriteMem" public: Word16.word * Word8.word -> unit;
val CWriteStream = _import "CWriteStream" public: Word16.word * Word8Vector.vector * Word32.word -> unit;
val CInitMem     = _import "CInitMem"  public: unit -> unit;
val CFreeMem     = _import "CFreeMem"  public: unit -> unit;

fun read_mem (addr16, useless) =
  BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)))), 8)
fun write_mem (addr16, data8) =
  CWriteMem(Word16.fromInt(BitsN.toInt(addr16)),Word8.fromInt(BitsN.toInt(data8)))
fun fetch_inst (addr16, useless) =
[BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)))), 8),
 BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)+1))), 8),
 BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(BitsN.toInt(addr16)+2))), 8)]

val reset_pc = ref (BitsN.fromInt(0,16))
val fileToLoad = ref (NONE: (int * Word8Vector.vector) option)
fun init_mem (stream) =
(
  CInitMem();
  case stream of
       SOME(addr, data) =>
         CWriteStream (Word16.fromInt(addr), data, Word32.fromInt(Vector.length(data)))
    |  _ => ();
  let
    val lo = BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(0xFFFC))),8)
    val hi = BitsN.fromInt(Word8.toInt(CReadMem(Word16.fromInt(0xFFFD))),8)
  in
    reset_pc := BitsN.concat([hi,lo])
  end
)
fun free_mem () = CInitMem()

(* helpers *)
fun failExit s = ( print (s ^ "\n"); OS.Process.exit OS.Process.failure )

(* Initialising L3 components *)

val start_pc = ref (NONE)

fun init_cpu6505 () =
(
  (* Memory operations *)
  cpu6502.SMLReadMem  := read_mem;
  cpu6502.SMLWriteMem := write_mem;
  cpu6502.SMLFetch    := fetch_inst;
  (* 6502 init function *)
  cpu6502.Init (Option.getOpt (!start_pc, !reset_pc))
)

fun init_system () =
(
  init_mem (!fileToLoad);
  init_cpu6505 ()
)

fun clean_system () =
(
  free_mem ()
)

(* Actual simulation *)

fun exec_loop () = (cpu6502.Next(); exec_loop ())

fun run () =
(
  init_system ();

  exec_loop ();

  clean_system ()
)

(* Option parsing code, taken from https://github.com/acjf3/l3mips *)

fun printUsage () =
print ("\n\
\6502 emulator (based on an L3 specification)\n\
\http://www.cl.cam.ac.uk/~acjf3/l3\n\n\
\usage: " ^ OS.Path.file (CommandLine.name ()) ^ " [arguments]\n\n\
\arguments:\n\
\  -d or --display <on|off> Turn on/off display statements in L3 sources (default off)\n\
\  --pc <address>           TODO Initial program counter value \n\
\  --at <address> <file>    TODO Load binary file <file> at location <address>l\n\
\  -h or --help             TODO Print this message\n\n")

fun getNumber s =
  case IntExtra.fromString s of
    SOME n => n
  | NONE   => failExit ("Bad number: " ^ s)

fun getHexNumber s =
  case StringCvt.scanString (Int.scan StringCvt.HEX) s of
    SOME n => n
  | NONE   => failExit ("Bad hex number: " ^ s)

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

fun processOption2 (s: string) =
  let
    fun loop acc =
      fn a :: b :: c :: r =>
        if a = s then (SOME (b,c), List.rev acc @ r)
        else loop (a :: acc) (b :: c :: r)
      |  r => (NONE, List.rev acc @ r)
  in
    loop []
  end

fun getCode p =
  let
    fun loop acc =
      fn    "--at" :: a :: c :: r => loop ((getNumber a, c) :: acc) r
      |     [r] => SOME (List.rev ((p, r) :: acc))
      |     _   => NONE
   in
      loop []
   end

val () =
  case getArguments () of
    ["--help"] => printUsage ()
  | l =>
      let
        val (disp, l) = processOption "--display" l
        val () = case disp of
                    NONE       => cpu6502.Display := (fn str => ())
                  | SOME "on"  => cpu6502.Display := (fn str => print (str^"\n"))
                  | SOME "off" => cpu6502.Display := (fn str => ())
                  | _          => failExit "--display must be on or off\n"
        val (p, l) = processOption "--pc" l
        fun flip f x y = f y x
        fun curry f x y = f (x,y)
        val () = start_pc := Option.map (((flip (curry BitsN.fromInt) 16)) o getHexNumber) p
        val (addr_file, l) = processOption2 "--at" l
        val () = case addr_file of
                    SOME (addr, file) =>
                    let
                      val istream   = BinIO.openIn file
                      val vec       = BinIO.inputAll istream
                      val ()        = BinIO.closeIn istream
                    in
                      fileToLoad := SOME(getHexNumber addr, vec)
                    end
                  | _ => fileToLoad := NONE
      in
        run ()
      end
