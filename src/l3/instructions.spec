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

unit unexpectedBehaviour = nothing -- TODO

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
    case _ => unexpectedBehaviour
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
    case _ => unexpectedBehaviour
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
    case _ => unexpectedBehaviour
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
TODO
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
TODO
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
TODO
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
TODO
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
TODO
-}
define Inc > INC (op::Operand) = match op
{
    case Addr (a) =>
    {
        new_val = ReadMem(a) + 1;
        WriteMem(a, new_val);
        STATUS <- updateNZ (STATUS, new_val)
    }
    case _ => unexpectedBehaviour
}

-- INX --
---------
{-
TODO
-}
define Inc > INX =
{
    X <- X + 1;
    STATUS <- updateNZ (STATUS, X)
}

-- INY --
---------
{-
TODO
-}
define Inc > INY =
{
    Y <- Y + 1;
    STATUS <- updateNZ (STATUS, Y)
}

-- DEC --
{-
TODO
-}
define Dec > DEC (op::Operand) = match op
{
    case Addr (a) =>
    {
        new_val = ReadMem(a) - 1;
        WriteMem(a, new_val);
        STATUS <- updateNZ (STATUS, new_val)
    }
    case _ => unexpectedBehaviour
}

-- DEX --
---------
{-
TODO
-}
define Dec > DEX =
{
    X <- X - 1;
    STATUS <- updateNZ (STATUS, X)
}

-- DEY --
---------
{-
TODO
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
TODO
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
    case _ => unexpectedBehaviour
}

-- LSR --
---------
{-
TODO
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
    case _ => unexpectedBehaviour
}

-- ROL --
---------
{-
TODO
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
    case _ => unexpectedBehaviour
}

-- ROR --
---------
{-
TODO
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
    case _ => unexpectedBehaviour
}

----------
-- Jump --
----------

-- JMP --
---------
{-
TODO
-}
define Jump > JMP (op::Operand) = match op
{
    case Addr (a) => PC <- PC_t(a)
    case _ => unexpectedBehaviour
}

-- JSR --
---------
{-
TODO
-}
define Jump > JSR (op::Operand) = match op
{
    case Addr (a) =>
    {
        spush (PC.H);
        spush (PC.L);
        PC <- PC_t(a)
    }
    case _ => unexpectedBehaviour
}

-- RTS --
---------
{-
TODO
-}
define Jump > RTS = { PC.L <- spop; PC.H <- spop }

--------------
-- Branches --
--------------

-- BCC --
---------
{-
TODO
-}
define Branch > BCC (op::Operand) = when not STATUS.C do doBranch (op)

-- BCS --
---------
{-
TODO
-}
define Branch > BCS (op::Operand) = when STATUS.C do doBranch (op)

-- BEQ --
---------
{-
TODO
-}
define Branch > BEQ (op::Operand) = when STATUS.Z do doBranch (op)

-- BMI --
---------
{-
TODO
-}
define Branch > BMI (op::Operand) = when STATUS.N do doBranch (op)

-- BNE --
---------
{-
TODO
-}
define Branch > BNE (op::Operand) = when not STATUS.Z do doBranch (op)

-- BPL --
---------
{-
TODO
-}
define Branch > BPL (op::Operand) = when not STATUS.N do doBranch (op)

-- BVC --
---------
{-
TODO
-}
define Branch > BVC (op::Operand) = when not STATUS.V do doBranch (op)

-- BVS --
---------
{-
TODO
-}
define Branch > BVS (op::Operand) = when STATUS.V do doBranch (op)

----------------------
-- Flags Fperations --
----------------------

-- CLC --
{-
TODO
-}
define Flags > CLC = STATUS.C <- false

-- CLD --
{-
TODO
-}
define Flags > CLD = STATUS.D <- false

-- CLI --
{-
TODO
-}
define Flags > CLI = STATUS.I <- false

-- CLV --
{-
TODO
-}
define Flags > CLV = STATUS.V <- false

-- SEC --
{-
TODO
-}
define Flags > SEC = STATUS.C <- true

-- SED --
{-
TODO
-}
define Flags > SED = STATUS.D <- true

-- SEI --
{-
TODO
-}
define Flags > SEI = STATUS.I <- true

-----------------------
-- System Operations --
-----------------------

-- BRK --
---------
{-
TODO
-}
define Sys > BRK = nothing -- TODO

-- NOP --
---------
{-
TODO
-}
define Sys > NOP = nothing

-- RTI --
---------
{-
TODO
-}
define Sys > RTI = nothing -- TODO

-- Unknown instruction, i.e. unsuccessful decode --
---------------------------------------------------
define UnknownInstruction = unexpectedBehaviour

-- done defining instructions --
--------------------------------
define Run
