----------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge --
----------------------------------------------------

-- TODO add PC update in addressing mode functions ? / elsewhere ?

-- Each addressing mode function will generate the operand source and returns
-- it (except for the implied addressing more)  and update the PC TODO
construct Operand {Addr :: bits(16), Val :: bits(8), Acc}

-- Implied addressing mode --
-----------------------------
{-
This mode is used by 25 1-byte instructions. The operand is implied in the
opcode.
operand implied in the opcode
-}
unit implied = ()

-- Accumulator addressing mode --
---------------------------------
{-
This mode is used by 4 1-byte instructions. The operation is performed on the
accumulator.
operand = accumulator
-}
Operand accumulator = Acc

-- Immediate addressing mode --
-------------------------------
{-
This mode is used by 11 2-bytes instructions. The second byte of the in-
struction contains the operand of the performed operation.
operand = byte#2
-}
Operand immediate (a::bits(8)) = Val(a)

-- Absolute addressing mode --
------------------------------
{-
This mode is used by 23 3-bytes instructions. The second and third byte of the
instruction respectively contain the LSB and the MSB of the address of the
operand of the performed operation.
operand = Mem[byte#3; byte#2]
-}
Operand absolute (a::bits(8), b::bits(8)) = Addr(b:a)

-- X-indexed absolute addressing mode --
----------------------------------------
{-
This mode is used by 15 3-bytes instructions. The second and third byte of the
instruction respectively contain the LSB and the MSB of an address, then
completed by adding to it the content of the X-index register. This is the
final address of the operand of the performed operation.
operand = Mem[(byte#3; byte#2) + X]
-}
Operand absolute_x (a::bits(8), b::bits(8)) = Addr((b:a)+SignExtend(X))

-- Y-indexed absolute addressing mode --
----------------------------------------
{-
This mode is used by 9 3-bytes instructions. The second and third byte of the
instruction respectively contain the LSB and the MSB of an address, then
completed by adding to it the content of the Y-index register. This is the
final address of the operand of the performed operation.
operand = Mem[(byte#3; byte#2) + Y]
-}
Operand absolute_y (a::bits(8), b::bits(8)) = Addr((b:a)+SignExtend(Y))

-- Absolute indirect addressing mode --
---------------------------------------
{-
This mode is used by 1 3-bytes instructions. The second and third byte of the
instruction respectively contain the LSB and MSB of a memory location.  The
pointed location and the next location respectively contain the LSB and the MSB
of an address to be loaded in the PC (only used by the absolute indirect JMP
instruction).
PCLSB = Mem[Mem[(byte#3; byte#2) + 1]; Mem[byte#3; byte#2]]
PCMSB = Mem[(Mem[(byte#3; byte#2) + 1]; Mem[byte#3; byte#2]) + 1]
-}
Operand absolute_indirect (a::bits(8), b::bits(8)) =
{
    base`16 = (ReadMem((b:a)+1):ReadMem(b:a));
    Addr(ReadMem(base+1):ReadMem(base))
}

-- Relative addressing mode --
------------------------------
{-
This mode is used by 8 2-bytes instructions. It’s only used with branch
instructions. The second byte of the instruction contains an offset ([−128;
+127]) to be added to the PC when it’s set at the next instruction.
branch with offset in byte#2
-}
Operand relative (a::bits(8)) = Val(a)

-- Zero Page addressing mode --
-------------------------------
{-
This mode is used by 21 2-bytes instructions. The second byte of the
instruction contains the LSB of the address of the operand of the performed
12operation. The MSB is assumed to be 0.
operand = Mem[00; byte#2]
-}
Operand zero_page (a::bits(8)) = Addr(0`8:a)

-- X-indexed Zero Page addressing mode --
-----------------------------------------
{-
This mode is used by 16 2-bytes instructions. The second byte of the
instruction contains the LSB of an address, then completed by adding to it the
content of the X-index register (NO carry is generated by this addition).  The
MSB is assumed to be 0, and finally form the address of the operand of the
performed operation.
operand = Mem[00; (byte#2 + X)]
-}
Operand zero_page_x (a::bits(8)) = Addr(0`8:a+X)

-- Y-indexed Zero Page addressing mode --
-----------------------------------------
{-
This mode is used by 2 2-bytes instructions. The second byte of the instruction
contains the LSB of an address, then completed by adding to it the content of
the Y-index register (NO carry is generated by this addition).  The MSB is
assumed to be 0, and finally form the address of the operand of the performed
operation.
operand = Mem[00; (byte#2 + Y)]
-}
Operand zero_page_y (a::bits(8)) = Addr(0`8:a+Y)

-- Indexed indirect addressing mode (IND,X) --
----------------------------------------------
{-
This mode is used by 8 2-bytes instructions. The second byte is added to the X
index register (no carry). The result points to page zero (MSB are assumed to
be 0 for this indirection). The pointed location and the next location
respectively contain the LSB and the MSB of the address of the operand of the
performed operation.
operand = Mem[ Mem[00;(byte#2 + X + 1)] ; Mem[00;(byte#2 + X)] ]
-}
Operand indexed_indirect_x (a::bits(8)) =
{
    base`16 = 0`8 : X + a;
    Addr(ReadMem(base+1):ReadMem(base))
}

-- Indirect indexed addressing mode (IND),Y --
----------------------------------------------
{-
This mode is used by 8 2-bytes instructions. The second byte points to a
location in page zero. The pointed location and the next location respectively
contain the LSB and the MSB of a based address to which we add the content of
the Y index register to form the effective address of the operand of the
performed operation.
operand = Mem[ (Mem[00; (byte#2 + 1)]; Mem[00; (byte#2)]) + Y ]
-}
Operand indirect_indexed_y (a::bits(8)) =
{
    base`16 = ReadMem(0:a+1) : ReadMem(0:a);
    Addr(base+SignExtend(Y))
}