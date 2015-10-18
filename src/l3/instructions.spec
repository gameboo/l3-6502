---------------------------------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge
---------------------------------------------------------------------------

-------------
-- helpers --
-------------

STATUS_t updateN (st::STATUS_t, val::bits(8)) = {var new = st; new.N <- val<7>; new}
STATUS_t updateZ (st::STATUS_t, val::bits(8)) = {var new = st; new.Z <- val == 0; new}
STATUS_t updateNZ (st::STATUS_t, val::bits(8)) =
{
    var new = st;
    new <- updateN (new, val);
    new <- updateZ (new, val);
    new
}

unit spush (val::bits(8)) = { WriteMem(0x01:S, val); S <- S - 1 }
bits(8) spop = { S <- S + 1; ReadMem(0x01:S) }

bits(8) valFromOp (op::Operand) = match op
{
    case Addr(a) => ReadMem(a)
    case Val(v) => v
    case Acc => A
}

unit doBranch (op::Operand) = PC <- PC_t (&PC + SignExtend(valFromOp (op)))

unit unexpectedBehaviour = Display(1,"Unexpected Behaviour\\n") -- TODO
unit unexpectedOperand = Display(1,"Unexpected Operand\\n") -- TODO

-----------------------------
-- Load / Store Operations --
-----------------------------

-- LDA --
---------
{-
The accumulator is loaded with the value of the operand
The N (negative) and the Z (zero) flags are updated
-}
define Load > LDA (op::Operand) =
{
    val = valFromOp(op);
    A <- val;
    STATUS <- updateNZ (STATUS, val)
}
-- LDX --
---------
{-
The X index regiser is loaded with the value of the operand
The N (negative) and the Z (zero) flags are updated
-}
define Load > LDX (op::Operand) =
{
    val = valFromOp(op);
    X <- val;
    STATUS <- updateNZ (STATUS, val)
}

-- LDY --
---------
{-
The Y index regiser is loaded with the value of the operand
The N (negative) and the Z (zero) flags are updated
-}
define Load > LDY (op::Operand) =
{
    val = valFromOp(op);
    Y <- val;
    STATUS <- updateNZ (STATUS, val)
}

-- STA --
---------
{-
The accumulator’s value is stored in the location pointed by the operand
The STATUS register is left untouched
-}
define Store > STA (op::Operand) = match op
{
    case Addr(a) => WriteMem(a, A)
    case _ => unexpectedOperand
}

-- STX --
---------
{-
The X index register's value is stored in the location pointed by the operand
The STATUS register is left untouched
-}
define Store > STX (op::Operand) = match op
{
    case Addr(a) => WriteMem(a, X)
    case _ => unexpectedOperand
}

-- STY --
---------
{-
The Y index register's value is stored in the location pointed by the operand
The STATUS register is left untouched
-}
define Store > STY (op::Operand) = match op
{
    case Addr(a) => WriteMem(a, Y)
    case _ => unexpectedOperand
}

-----------------------------------
-- Registers Transfer Operations --
-----------------------------------

-- TAX --
---------
{-
The accumulator’s value is stored into the X index register
The N (negative) and the Z (zero) flags are updated
-}
define Transfer > TAX =
{
    X <- A;
    STATUS <- updateNZ (STATUS, X)
}

-- TAY --
---------
{-
The accumulator’s value is stored into the Y index register
The N (negative) and the Z (zero) flags are updated
-}
define Transfer > TAY =
{
    Y <- A;
    STATUS <- updateNZ (STATUS, Y)
}

-- TXA --
---------
{-
The X index register’s value is stored into the accumulator
The N (negative) and the Z (zero) flags are updated
-}
define Transfer > TXA =
{
    A <- X;
    STATUS <- updateNZ (STATUS, A)
}

-- TYA --
---------
{-
The Y index register’s value is stored into the accumulator
The N (negative) and the Z (zero) flags are updated
-}
define Transfer > TYA =
{
    A <- Y;
    STATUS <- updateNZ (STATUS, A)
}

----------------------
-- Stack Operations --
----------------------

-- TSX --
---------
{-
The S (stack pointer) register’s value is stored into the X index register
The N (negative) and the Z (zero) flags are updated
-}
define Stack > TSX =
{
    X <- S;
    STATUS <- updateNZ (STATUS, X)
}

-- TXS --
---------
{-
The X index register’s value is stored into the S (stack pointer) register
The STATUS register is left untouched
-}
define Stack > TXS = S <- X

-- PHA --
---------
{-
The accumulator is stored on the stack. The S (stack pointer) register is
decremented by one
The STATUS register is left untouched
-}
define Stack > PHA = spush (A)

-- PHP --
---------
{-
The STATUS register is stored on the stack. The S (stack pointer) register is
decremented by one
The STATUS register is left untouched
-}
define Stack > PHP = spush (&STATUS)

-- PLA --
---------
{-
The S (stack pointer) register is incremented by one. The pointed location’s
content is then poped from the stack into the accumulator
The N (negative) and Z (zero) flags are updated
-}
define Stack > PLA =
{
    A <- spop;
    STATUS <- updateNZ (STATUS, A)
}

-- PLP --
---------
{-
The S (stack pointer) register is incremented by one. The pointed location’s
content is then poped from the stack into the STATUS register
-}
define Stack > PLP = STATUS <- STATUS_t(spop)

------------------------
-- Logical Operations --
------------------------

-- AND --
---------
{-
The accumulator is ”ANDed” with the operand, and the result is stored in the
accumulator
The N (negative) and Z (zero) flags are updated
-}
define Logical > AND (op::Operand) =
{
    A <- A && valFromOp(op);
    STATUS <- updateNZ (STATUS, A)
}

-- EOR --
---------
{-
The accumulator is ”XORed” with the operand. The result is stored in the
accumulator
The N (negative) and the Z (zero) flags are updated
-}
define Logical > EOR (op::Operand) =
{
    A <- A ?? valFromOp(op);
    STATUS <- updateNZ (STATUS, A)
}

-- ORA --
---------
{-
The operand is ”ORed” with the accumulator. The result is stored in the
accumulator
The N (negative) and the Z (zero) flags are updated
-}
define Logical > ORA (op::Operand) =
{
    A <- A || valFromOp(op);
    STATUS <- updateNZ (STATUS, A)
}

-- BIT --
---------
{-
The accumulator is ”ANDed” with the operand. The result is not stored, but the
STATUS register is updated
The Z (zero) flag is updated
The N (negative) and the V (overflow) flags are respectively updated with the
7th and the 6th bit of the operand
-}
define Logical > BIT (op::Operand) =
{
    val = valFromOp(op);
    res = A || val;
    STATUS.N <- val<7>;
    STATUS.V <- val<6>;
    STATUS.Z <- res == 0
}

---------------------------
-- Arithmetic Operations --
---------------------------

-- ADC --
---------
{-
The accumulator is added to the (signed) operand and the carry bit, and the
result is stored in the accumulator
The N (negative), V (overflow), Z (zero) and C (carry) flags are updated
If D (decimal mode) flag is enabled, the Z (zero) flag is invalid ;
the accumulator has to be checked for zero result
-}
define Arith > ADC (op::Operand) =
{
    val = valFromOp(op);
    res`9 = SignExtend(A) + SignExtend(val) +
                     (if STATUS.C then 1`9 else 0`9);
    STATUS.C <- res<8>;
    -- TODO check overflow computation
    STATUS.V <- if (A<7> == val<7> and A<7> <> res<7>) then
                    true
                else
                    false;
    A <- res<7:0>;
    STATUS <- updateNZ (STATUS, A)
}

-- SBC --
---------
{-
The operand is subtracted from the accumulator, using the complement of the C
(carry) flag as an additional borrow. The result is stored in the accumulator.
The N (negative), V (overflow) and Z (zero) flags are updated
The C (carry) flag is updated with the borrow from the operation
-}
define Arith > SBC (op::Operand) =
{
    val = valFromOp(op);
    res`9 = SignExtend(A) - SignExtend(val) -
                     (if STATUS.C then 0`9 else 1`9);
    STATUS.C <- res < 0x100`9;
    -- TODO check overflow computation
    STATUS.V <- if (A<7> == val<7> and A<7> <> res<7>) then
                    true
                else
                    false;
    A <- res<7:0>;
    STATUS <- updateNZ (STATUS, A)
}

-- CMP --
---------
{-
The operand is subtracted from the accumulator. The result is ignored, but the
STATUS register is updated.
The N (negative), the Z (zero) and the C (carry) flags are updated
-}
define Arith > CMP (op::Operand) =
{
    val = valFromOp(op);
    res`9 = SignExtend(A) - SignExtend(val);
    STATUS.C <- res < 0x100`9;
    STATUS <- updateNZ (STATUS, res<7:0>)
}

-- CPX --
---------
{-
The operand is subtracted from the X index register. The result is ignored, but
the STATUS register is updated.
The N (negative), the Z (zero) and the C (carry) flags are updated
-}
define Arith > CPX (op::Operand) =
{
    val = valFromOp(op);
    res`9 = SignExtend(X) - SignExtend(val);
    STATUS.C <- res < 0x100`9;
    STATUS <- updateNZ (STATUS, res<7:0>)
}

-- CPY --
---------
{-
The operand is subtracted from the Y index register. The result is ignored, but
the STATUS register is updated.
The N (negative), the Z (zero) and the C (carry) flags are updated
-}
define Arith > CPY (op::Operand) =
{
    val = valFromOp(op);
    res`9 = SignExtend(Y) - SignExtend(val);
    STATUS.C <- res < 0x100`9;
    STATUS <- updateNZ (STATUS, res<7:0>)
}

-----------------------------
-- Increments / Decrements --
-----------------------------

-- INC --
{-
The operand is incremented by one. The result is stored back in the memory.
The N (negative) and the Z (zero) flags are updated
-}
define Inc > INC (op::Operand) = match op
{
    case Addr (a) =>
    {
        new_val = ReadMem(a) + 1;
        WriteMem(a, new_val);
        STATUS <- updateNZ (STATUS, new_val)
    }
    case _ => unexpectedOperand
}

-- INX --
---------
{-
The X index register is incremented by one. The result is stored in the X index
register.
The N (negative) and the Z (zero) flags are updated
-}
define Inc > INX =
{
    X <- X + 1;
    STATUS <- updateNZ (STATUS, X)
}

-- INY --
---------
{-
The Y index register is incremented by one. The result is stored in the Y index
register.
The N (negative) and the Z (zero) flags are updated
-}
define Inc > INY =
{
    Y <- Y + 1;
    STATUS <- updateNZ (STATUS, Y)
}

-- DEC --
{-
The operand is decremented by one. The result is stored back in the memory.
The N (negative) and the Z (zero) flags are updated
-}
define Dec > DEC (op::Operand) = match op
{
    case Addr (a) =>
    {
        new_val = ReadMem(a) - 1;
        WriteMem(a, new_val);
        STATUS <- updateNZ (STATUS, new_val)
    }
    case _ => unexpectedOperand
}

-- DEX --
---------
{-
The X index register is decremented by one. The result is stored in the X index
register.
The N (negative) and the Z (zero) flags are updated
-}
define Dec > DEX =
{
    X <- X - 1;
    STATUS <- updateNZ (STATUS, X)
}

-- DEY --
---------
{-
The Y index register is decremented by one. The result is stored in the Y index
register.
The N (negative) and the Z (zero) flags are updated
-}
define Dec > DEY =
{
    Y <- Y - 1;
    STATUS <- updateNZ (STATUS, Y)
}

------------
-- Shifts --
------------

-- ASL --
---------
{-
The operand (accumulator/memory) is shifted one bit left, inserting one ”0”
from the right. The result is stored in the operand.
The N (negative) and the Z (zero) flags are updated
The C (carry) flag is updated with the ejected bit’s value
-}
define Shift > ASL (op::Operand) = match op
{
    case Addr (a) =>
    {
        new_val`9 = ZeroExtend(ReadMem(a)) << 1;
        WriteMem(a, new_val<7:0>);
        STATUS.C <- new_val<8>;
        STATUS <- updateNZ (STATUS, new_val<7:0>)
    }
    case Acc =>
    {
        new_val`9 = ZeroExtend(A) << 1;
        A <- new_val<7:0>;
        STATUS.C <- new_val<8>;
        STATUS <- updateNZ (STATUS, new_val<7:0>)
    }
    case _ => unexpectedOperand
}

-- LSR --
---------
{-
The operand (accumulator/memory) is shifted one bit right, inserting one ”0”
from the left. The result is stored in the operand.
The C (carry) flag is updated with the ejected bit’s value
The Z (zero) flag is updated
The N (negative) flag is reset to ”0”
-}
define Shift > LSR (op::Operand) = match op
{
    case Addr (a) =>
    {
        val = ReadMem(a);
        STATUS.C <- val<0>;
        new_val = val >> 1;
        WriteMem(a, new_val);
        STATUS <- updateNZ (STATUS, new_val)
    }
    case Acc =>
    {
        STATUS.C <- A<0>;
        A <- A >> 1;
        STATUS <- updateNZ (STATUS, A)
    }
    case _ => unexpectedOperand
}

-- ROL --
---------
{-
The operand (accumulator/memory) is rotated one bit left, inserting the value
of the C (carry) flag from the right, and then updating C with the ejected
bit’s value. The result is stored in the operand.
The N (negative) and Z (zero) flags are updated
The C (carry) flag is updated with the ejected bit’s value
-}
define Shift > ROL (op::Operand) = match op
{
    case Addr (a) =>
    {
        var new_val`9 = ZeroExtend(ReadMem(a)) << 1;
        new_val<0> <- STATUS.C;
        STATUS.C <- new_val<8>;
        WriteMem(a, new_val<7:0>);
        STATUS <- updateNZ (STATUS, new_val<7:0>)
    }
    case Acc =>
    {
        var new_val`9 = ZeroExtend(A) << 1;
        new_val<0> <- STATUS.C;
        STATUS.C <- new_val<8>;
        A <- new_val<7:0>;
        STATUS <- updateNZ (STATUS, new_val<7:0>)
    }
    case _ => unexpectedOperand
}

-- ROR --
---------
{-
The operand (accumulator/memory) is rotated one bit right, inserting the value
of the C (carry) flag from the right, and then updating C with the ejected
bit’s value. The result is stored in the operand.
The N (negative) and Z (zero) flags are updated
The C (carry) flag is updated with the ejected bit’s value
-}
define Shift > ROR (op::Operand) = match op
{
    case Addr (a) =>
    {
        val = ReadMem(a);
        var new_val = val >> 1;
        new_val<7> <- STATUS.C;
        WriteMem(a, new_val);
        STATUS.C <- val<0>;
        STATUS <- updateNZ (STATUS, new_val)
    }
    case Acc =>
    {
        val = A;
        var new_val = val >> 1;
        new_val<7> <- STATUS.C;
        A <- new_val;
        STATUS.C <- val<0>;
        STATUS <- updateNZ (STATUS, new_val)
    }
    case _ => unexpectedOperand
}

----------
-- Jump --
----------

-- JMP --
---------
{-
The PC (program counter) is loaded with the operand’s value.
The STATUS register is left untouched
-}
define Jump > JMP (op::Operand) = match op
{
    case Addr (a) => PC <- PC_t(a)
    case _ => unexpectedOperand
}

-- JSR --
---------
{-
The PC (program counter) is first stored on the stack (high byte first, then
low byte), then loaded with the operand’s value. The S (stack pointer) register
is decremented by 2.
The STATUS register is left untouched
-}
define Jump > JSR (op::Operand) = match op
{
    case Addr (a) =>
    {
        spush (PC.H);
        spush (PC.L);
        PC <- PC_t(a)
    }
    case _ => unexpectedOperand
}

-- RTS --
---------
{-
The S (stack pointer) register is incremented by one. The pointed location’s
value is poped from the stack into the PC (program counter) register’s low
byte. Then, the S (stack pointer) register is incremented by one. The pointed
location’s value is poped from the stack into the PC (program counter)
register’s high byte.
The STATUS register is left untouched
-}
define Jump > RTS = { PC.L <- spop; PC.H <- spop }

--------------
-- Branches --
--------------

-- BCC --
---------
{-
If the C (carry) flag is ”0”, the (signed) offset contained in the operand is
added to the PC (program counter) register to point to a new instruction.
The STATUS register is left untouched
-}
define Branch > BCC (op::Operand) = when not STATUS.C do doBranch (op)

-- BCS --
---------
{-
If the C (carry) flag is ”1”, the (signed) offset contained in the operand is
added to the PC (program counter) register to point to a new instruction.
The STATUS register is left untouched
-}
define Branch > BCS (op::Operand) = when STATUS.C do doBranch (op)

-- BEQ --
---------
{-
If the Z (zero) flag is ”1”, the (signed) offset contained in the operand is
added to the PC (program counter) register to point to a new instruction.
The STATUS register is left untouched
-}
define Branch > BEQ (op::Operand) = when STATUS.Z do doBranch (op)

-- BMI --
---------
{-
If the N (negative) flag is ”1”, the (signed) offset contained in the operand
is added to the PC (program counter) register to point to a new instruction.
The STATUS register is left untouched
-}
define Branch > BMI (op::Operand) = when STATUS.N do doBranch (op)

-- BNE --
---------
{-
If the Z (zero) flag is ”0”, the (signed) offset contained in the operand is
added to the PC (program counter) register to point to a new instruction.
The STATUS register is left untouched
-}
define Branch > BNE (op::Operand) = when not STATUS.Z do doBranch (op)

-- BPL --
---------
{-
If the N (negative) flag is ”0”, the (signed) offset contained in the operand
is added to the PC (program counter) register to point to a new instruction.
The STATUS register is left untouched
-}
define Branch > BPL (op::Operand) = when not STATUS.N do doBranch (op)

-- BVC --
---------
{-
If the V (overflow) flag is ”0”, the (signed) offset contained in the operand
is added to the PC (program counter) register to point to a new instruction.
The STATUS register is left untouched
-}
define Branch > BVC (op::Operand) = when not STATUS.V do doBranch (op)

-- BVS --
---------
{-
If the V (overflow) flag is ”1”, the (signed) offset contained in the operand
is added to the PC (program counter) register to point to a new instruction.
The STATUS register is left untouched
-}
define Branch > BVS (op::Operand) = when STATUS.V do doBranch (op)

----------------------
-- Flags Fperations --
----------------------

-- CLC --
{-
The STATUS register is updated.
The C (carry) flag is reset to 0
-}
define Flags > CLC = STATUS.C <- false

-- CLD --
{-
The STATUS register is updated.
The D (decimal mode) flag is reset to 0
-}
define Flags > CLD = STATUS.D <- false

-- CLI --
{-
The STATUS register is updated.
The I (irq disable) flag is reset to 0
-}
define Flags > CLI = STATUS.I <- false

-- CLV --
{-
The STATUS register is updated.
The V (overflow) flag is reset to 0
-}
define Flags > CLV = STATUS.V <- false

-- SEC --
{-
The STATUS register is updated.
The C (carry) flag is set to ”1”
-}
define Flags > SEC = STATUS.C <- true

-- SED --
{-
The STATUS register is updated.
The D (decimal mode) flag is set to ”1”
-}
define Flags > SED = STATUS.D <- true

-- SEI --
{-
The STATUS register is updated.
The I (irq disable) flag is set to 1
-}
define Flags > SEI = STATUS.I <- true

-----------------------
-- System Operations --
-----------------------

-- BRK --
---------
{-
This instruction triggers an interrupt request to the CPU, allowing ”software
interrupts”
The B (break command) flag is set to 1
The I (irq disable) flag will be set to 1 when the irq will be handled
-}
define Sys > BRK = { INT.IRQ <- true; STATUS.B <- true }

-- NOP --
---------
{-
No operation
-}
define Sys > NOP = nothing

-- RTI --
---------
{-
return from BRK/IRQ/NMI
The S (stack pointer) register is incremented by one. The pointed location’s
value is poped from the stack into the STATUS register. Then, the S (stack
pointer) register is incremented by one. The pointed location’s value is poped
from the stack into the PC (program counter) register’s low byte. Then, the S
(stack pointer) register is incremented by one. The pointed location’s value is
poped from the stack into the PC (program counter) register’s high byte.
-}
define Sys > RTI = { STATUS <- STATUS_t(spop); PC.L <- spop; PC.H <- spop }

-- Unknown instruction, i.e. unsuccessful decode --
---------------------------------------------------
define UnknownInstruction = unexpectedBehaviour

-- done defining instructions --
--------------------------------
define Run
