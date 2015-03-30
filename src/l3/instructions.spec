---------------------------------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge
---------------------------------------------------------------------------

-----------------------------
-- Load / Store Operations --
-----------------------------

-- LDA --
---------
{-
The accumulator is loaded with the value of the operand
The N (negative) and the Z (zero) flags are updated
-}
define Load > LDA (operand::bits(8)) =
{
    A <- operand;
    STATUS.N <- operand<7>;
    STATUS.Z <- operand == 0
}

-- LDX --
---------
{-
The X index regiser is loaded with the value of the operand
The N (negative) and the Z (zero) flags are updated
-}
define Load > LDX (operand::bits(8)) =
{
    X <- operand;
    STATUS.N <- operand<7>;
    STATUS.Z <- operand == 0
}

-- LDY --
---------
{-
The Y index regiser is loaded with the value of the operand
The N (negative) and the Z (zero) flags are updated
-}
define Load > LDY (operand::bits(8)) =
{
    Y <- operand;
    STATUS.N <- operand<7>;
    STATUS.Z <- operand == 0
}

-- STA --
---------
{-
The accumulator’s value is stored in the location pointed by the operand
The STATUS register is left untouched
-}
define Store > STA (addr::bits(16)) = WriteMem(addr, A)

-- STX --
---------
{-
The X index register's value is stored in the location pointed by the operand
The STATUS register is left untouched
-}
define Store > STX (addr::bits(16)) = WriteMem(addr, X)

-- STY --
---------
{-
The Y index register's value is stored in the location pointed by the operand
The STATUS register is left untouched
-}
define Store > STY (addr::bits(16)) = WriteMem(addr, Y)

-----------------------------------
-- Registers Transfer Operations --
-----------------------------------

-- TAX --
---------
{-
The accumulator’s value is stored into the X index register
The N (negative) and the Z (zero) flags are updated
-}
define Transfer > TAX () =
{
    X <- A;
    STATUS.N <- X<7>;
    STATUS.Z <- X == 0
}

-- TAY --
---------
{-
The accumulator’s value is stored into the Y index register
The N (negative) and the Z (zero) flags are updated
-}
define Transfer > TAY () =
{
    Y <- A;
    STATUS.N <- Y<7>;
    STATUS.Z <- Y == 0
}

-- TXA --
---------
{-
The X index register’s value is stored into the accumulator
The N (negative) and the Z (zero) flags are updated
-}
define Transfer > TXA () =
{
    A <- X;
    STATUS.N <- A<7>;
    STATUS.Z <- A == 0
}

-- TYA --
---------
{-
The Y index register’s value is stored into the accumulator
The N (negative) and the Z (zero) flags are updated
-}
define Transfer > TYA () =
{
    A <- Y;
    STATUS.N <- A<7>;
    STATUS.Z <- A == 0
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
define Stack > TSX () =
{
    X <- S;
    STATUS.N <- X<7>;
    STATUS.Z <- X == 0
}

-- TXS --
---------
{-
The X index register’s value is stored into the S (stack pointer) register
The STATUS register is left untouched
-}
define Stack > TXS () = S <- X

-- PHA --
---------
{-
The accumulator is stored on the stack. The S (stack pointer) register is
decremented by one
The STATUS register is left untouched
-}
define Stack > PHA () =
{
    WriteMem(0x01:S, A);
    S <- S - 1
}

-- PHP --
---------
{-
The STATUS register is stored on the stack. The S (stack pointer) register is
decremented by one
The STATUS register is left untouched
-}
define Stack > PHP () =
{
    WriteMem(0x01:S, &STATUS);
    S <- S - 1
}

-- PLA --
---------
{-
The S (stack pointer) register is incremented by one. The pointed location’s
content is then poped from the stack into the accumulator
The N (negative) and Z (zero) flags are updated
-}
define Stack > PLA () =
{
    S <- S + 1;
    A <- ReadMem(0x01:S);
    STATUS.N <- A<7>;
    STATUS.Z <- A == 0
}

-- PLP --
---------
{-
The S (stack pointer) register is incremented by one. The pointed location’s
content is then poped from the stack into the STATUS register
-}
define Stack > PLP () =
{
    S <- S + 1;
    STATUS <- STATUS_t(ReadMem(0x01:S))
}

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
define Logical > AND (operand::bits(8)) =
{
    A <- A && operand;
    STATUS.N <- A<7>;
    STATUS.Z <- A == 0
}

-- EOR --
---------
{-
The accumulator is ”XORed” with the operand. The result is stored in the
accumulator
The N (negative) and the Z (zero) flags are updated
-}
define Logical > EOR (operand::bits(8)) =
{
    A <- A ?? operand;
    STATUS.N <- A<7>;
    STATUS.Z <- A == 0
}

-- ORA --
---------
{-
The operand is ”ORed” with the accumulator. The result is stored in the
accumulator
The N (negative) and the Z (zero) flags are updated
-}
define Logical > ORA (operand::bits(8)) =
{
    A <- A || operand;
    STATUS.N <- A<7>;
    STATUS.Z <- A == 0
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
define Logical > BIT (operand::bits(8)) =
{
    res = A || operand;
    STATUS.N <- operand<7>;
    STATUS.V <- operand<6>;
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
define Arith > ADC (operand::bits(8)) =
{
    res`9 = SignExtend(A) + SignExtend(operand) +
                     (if STATUS.C then 1`9 else 0`9);
    STATUS.C <- res<8>;
    STATUS.N <- res<7>;
    STATUS.V <- if (A<7> == operand<7> and A<7> <> res<7>) then
                    true
                else
                    false;
    STATUS.Z <- A == 0;
    A <- res<7:0>
}

-- Unknown instruction, i.e. unsuccessful decode --
---------------------------------------------------
define UnknownInstruction = () -- TODO implement something

-- done defining instructions --
--------------------------------
define Run
