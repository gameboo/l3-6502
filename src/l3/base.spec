---------------------------------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge
---------------------------------------------------------------------------

declare A :: bits(8) -- Accumulator register
declare X :: bits(8) -- X index register
declare Y :: bits(8) -- Y index register
declare S :: bits(8) -- stack pointer register

-- Program Counter --
register PC_t :: bits(16)
{
    15-8 : H -- high order byte of the Program Counter
     7-0 : L -- low order byte of the Program Counter
}
declare PC :: PC_t -- Program Counter register

-- STATUS --
register STATUS_t :: bits(8)
{
    7 : N -- Negative flag
    6 : V -- oVerflow flag
    5 : r -- reserved (set to 1)
    4 : B -- Break flag
    3 : D -- Decimal mode flag
    2 : I -- Interrupt ReQuest disable flag
    1 : Z -- Zero flag
    0 : C -- Carry flag
}
declare STATUS :: STATUS_t -- STATUS register

-- interrupts --
register INT_t :: bits(3)
{
    2 : IRQ     -- interrupt request
    1 : NMI     -- non maskable interrupt
    0 : RESET   -- reset
}
declare INT :: INT_t -- Interrupt sources

-- types --
type ByteStream = bits(8) list -- Byte stream (variable length instructions)
declare instrNbr :: nat

-- Initialisation --
unit Init (pc :: bits(16)) =
{
    A           <- 0`8;
    X           <- 0`8;
    Y           <- 0`8;
    S           <- 0`8;
    PC          <- PC_t(pc);
    STATUS      <- STATUS_t(0);
    STATUS.r    <- true;
    INT         <- INT_t(0);
    instrNbr    <- 0
}

-- debug --
string cpuStateStr =
{
    var str = "";
    str <- str : "A = 0x" : PadLeft (#"0", 2, [A]);
    str <- str : ", S = 0x" : PadLeft (#"0", 2, [S]);
    str <- str : "\\nX = 0x" : PadLeft (#"0", 2, [X]);
    str <- str : ", Y = 0x" : PadLeft (#"0", 2, [Y]);
    str <- str : "\\nPC = [":PadLeft (#"0", 2, [PC.H]):":":PadLeft (#"0", 2, [PC.L]):"]";
    str <- str : "\\nSTATUS = <";
    for b in 7..0 do str <- str : if &STATUS<b> then "1" else "0";
    str <- str : ">";
    str <- str : "\\nINT{IRQ:":if INT.IRQ then "1" else "0";
    str <- str : ",NMI:":if INT.NMI then "1" else "0";
    str <- str : ",RESET:":if INT.RESET then "1" else "0":"}";
    str
}
