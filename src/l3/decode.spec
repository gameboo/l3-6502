----------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge --
----------------------------------------------------

string * nat * instruction Decode (inst::ByteStream) = match inst
{
    case 0x00 @ _         => ("BRK", 1, Sys      (BRK))
    case 0x01 @ a @ _     => ("ORA - indexed_indirect_x", 2, Logical  (ORA (indexed_indirect_x (a))))
    case 0x05 @ a @ _     => ("ORA - zero_page", 2, Logical  (ORA (zero_page (a))))
    case 0x06 @ a @ _     => ("ASL - zero_page", 2, Shift    (ASL (zero_page (a))))
    case 0x08 @ _         => ("PHP", 1, Stack    (PHP))
    case 0x09 @ a @ _     => ("ORA - immediate", 2, Logical  (ORA (immediate (a))))
    case 0x0A @ _         => ("ASL - accumulator", 1, Shift    (ASL (accumulator)))
    case 0x0D @ a @ b @ _ => ("ORA - absolute", 3, Logical  (ORA (absolute (a, b))))
    case 0x0E @ a @ b @ _ => ("ASL - absolute", 3, Shift    (ASL (absolute (a, b))))
    case 0x10 @ a @ _     => ("BPL - relative", 2, Branch   (BPL (relative (a))))
    case 0x11 @ a @ _     => ("ORA - indirect_indexed_y", 2, Logical  (ORA (indirect_indexed_y (a))))
    case 0x15 @ a @ _     => ("ORA - zero_page_x", 2, Logical  (ORA (zero_page_x (a))))
    case 0x16 @ a @ _     => ("ASL - zero_page_x", 2, Shift    (ASL (zero_page_x (a))))
    case 0x18 @ _         => ("CLC", 1, Flags    (CLC))
    case 0x19 @ a @ b @ _ => ("ORA - absolute_y", 3, Logical  (ORA (absolute_y (a, b))))
    case 0x1D @ a @ b @ _ => ("ORA - absolute_x", 3, Logical  (ORA (absolute_x (a, b))))
    case 0x1E @ a @ b @ _ => ("ASL - absolute_x", 3, Shift    (ASL (absolute_x (a, b))))
    case 0x20 @ a @ b @ _ => ("JSR - absolute", 3, Jump     (JSR (absolute (a, b))))
    case 0x21 @ a @ _     => ("AND - indexed_indirect_x", 2, Logical  (AND (indexed_indirect_x (a))))
    case 0x24 @ a @ _     => ("BIT - zero_page", 2, Logical  (BIT (zero_page (a))))
    case 0x25 @ a @ _     => ("AND - zero_page", 2, Logical  (AND (zero_page (a))))
    case 0x26 @ a @ _     => ("ROL - zero_page", 2, Shift    (ROL (zero_page (a))))
    case 0x28 @ _         => ("PLP", 1, Stack    (PLP))
    case 0x29 @ a @ _     => ("AND - immediate", 2, Logical  (AND (immediate (a))))
    case 0x2A @ _         => ("ROL - accumulator", 1, Shift    (ROL (accumulator)))
    case 0x2C @ a @ b @ _ => ("BIT - absolute", 3, Logical  (BIT (absolute (a, b))))
    case 0x2D @ a @ b @ _ => ("AND - absolute", 3, Logical  (AND (absolute (a, b))))
    case 0x2E @ a @ b @ _ => ("ROL - absolute", 3, Shift    (ROL (absolute (a, b))))
    case 0x30 @ a @ _     => ("BMI - relative", 2, Branch   (BMI (relative (a))))
    case 0x31 @ a @ _     => ("AND - indirect_indexed_y", 2, Logical  (AND (indirect_indexed_y (a))))
    case 0x35 @ a @ _     => ("AND - zero_page_x", 2, Logical  (AND (zero_page_x (a))))
    case 0x36 @ a @ _     => ("ROL - zero_page_x", 2, Shift    (ROL (zero_page_x (a))))
    case 0x38 @ _         => ("SEC", 1, Flags    (SEC))
    case 0x39 @ a @ b @ _ => ("AND - absolute_y", 3, Logical  (AND (absolute_y (a, b))))
    case 0x3D @ a @ b @ _ => ("AND - absolute_x", 3, Logical  (AND (absolute_x (a, b))))
    case 0x3E @ a @ b @ _ => ("ROL - absolute_x", 3, Shift    (ROL (absolute_x (a, b))))
    case 0x40 @ _         => ("RTI", 1, Sys      (RTI))
    case 0x41 @ a @ _     => ("EOR - indexed_indirect_x", 2, Logical  (EOR (indexed_indirect_x (a))))
    case 0x45 @ a @ _     => ("EOR - zero_page", 2, Logical  (EOR (zero_page (a))))
    case 0x46 @ a @ _     => ("LSR - zero_page", 2, Shift    (LSR (zero_page (a))))
    case 0x48 @ _         => ("PHA", 1, Stack    (PHA))
    case 0x49 @ a @ _     => ("EOR - immediate", 2, Logical  (EOR (immediate (a))))
    case 0x4A @ _         => ("LSR - accumulator", 1, Shift    (LSR (accumulator)))
    case 0x4C @ a @ b @ _ => ("JMP - absolute", 3, Jump     (JMP (absolute (a, b))))
    case 0x4D @ a @ b @ _ => ("EOR - absolute", 3, Logical  (EOR (absolute (a, b))))
    case 0x4E @ a @ b @ _ => ("LSR - absolute", 3, Shift    (LSR (absolute (a, b))))
    case 0x50 @ a @ _     => ("BVC - relative", 2, Branch   (BVC (relative (a))))
    case 0x51 @ a @ _     => ("EOR - indirect_indexed_y", 2, Logical  (EOR (indirect_indexed_y (a))))
    case 0x55 @ a @ _     => ("EOR - zero_page_x", 2, Logical  (EOR (zero_page_x (a))))
    case 0x56 @ a @ _     => ("LSR - zero_page_x", 2, Shift    (LSR (zero_page_x (a))))
    case 0x58 @ _         => ("CLI", 1, Flags    (CLI))
    case 0x59 @ a @ b @ _ => ("EOR - absolute_y", 3, Logical  (EOR (absolute_y (a, b))))
    case 0x5D @ a @ b @ _ => ("EOR - absolute_x", 3, Logical  (EOR (absolute_x (a, b))))
    case 0x5E @ a @ b @ _ => ("LSR - absolute_x", 3, Shift    (LSR (absolute_x (a, b))))
    case 0x60 @ _         => ("RTS", 1, Jump     (RTS))
    case 0x61 @ a @ _     => ("ADC - indexed_indirect_x", 2, Arith    (ADC (indexed_indirect_x (a))))
    case 0x65 @ a @ _     => ("EOR - zero_page", 2, Logical  (EOR (zero_page (a))))
    case 0x66 @ a @ _     => ("LSR - zero_page", 2, Shift    (LSR (zero_page (a))))
    case 0x68 @ _         => ("PLA", 1, Stack    (PLA))
    case 0x69 @ a @ _     => ("ADC - immediate", 2, Arith    (ADC (immediate (a))))
    case 0x6A @ _         => ("ROR", 1, Shift    (ROR(accumulator)))
    case 0x6C @ a @ b @ _ => ("JMP - absolute_indirect", 3, Jump     (JMP (absolute_indirect (a, b))))
    case 0x6D @ a @ b @ _ => ("ADC - absolute", 3, Arith    (ADC (absolute (a, b))))
    case 0x6E @ a @ b @ _ => ("ROR - absolute", 3, Shift    (ROR (absolute (a, b))))
    case 0x70 @ a @ _     => ("BVS - relative", 2, Branch   (BVS (relative (a))))
    case 0x71 @ a @ _     => ("ADC - indirect_indexed_y", 2, Arith    (ADC (indirect_indexed_y (a))))
    case 0x75 @ a @ _     => ("ADC - zero_page_x", 2, Arith    (ADC (zero_page_x (a))))
    case 0x76 @ a @ _     => ("ROR - zero_page_x", 2, Shift    (ROR (zero_page_x (a))))
    case 0x78 @ _         => ("SEI", 1, Flags    (SEI))
    case 0x79 @ a @ b @ _ => ("ADC - absolute_y", 3, Arith    (ADC (absolute_y (a, b))))
    case 0x7D @ a @ b @ _ => ("ADC - absolute_x", 3, Arith    (ADC (absolute_x (a, b))))
    case 0x7E @ a @ b @ _ => ("ROR - absolute_x", 3, Shift    (ROR (absolute_x (a, b))))
    case 0x81 @ a @ _     => ("STA - indexed_indirect_x", 2, Store    (STA (indexed_indirect_x (a))))
    case 0x84 @ a @ _     => ("STY - zero_page", 2, Store    (STY (zero_page (a))))
    case 0x85 @ a @ _     => ("STA - zero_page", 2, Store    (STA (zero_page (a))))
    case 0x86 @ a @ _     => ("STX - zero_page", 2, Store    (STX (zero_page (a))))
    case 0x88 @ _         => ("DEY", 1, Dec      (DEY))
    case 0x8A @ _         => ("TXA", 1, Transfer (TXA))
    case 0x8C @ a @ b @ _ => ("STY - absolute", 3, Store    (STY (absolute (a, b))))
    case 0x8D @ a @ b @ _ => ("STA - absolute", 3, Store    (STA (absolute (a, b))))
    case 0x8E @ a @ b @ _ => ("STX - absolute", 3, Store    (STX (absolute (a, b))))
    case 0x90 @ a @ _     => ("BCC - relative", 2, Branch   (BCC (relative (a))))
    case 0x91 @ a @ _     => ("STA - indirect_indexed_y", 2, Store    (STA (indirect_indexed_y (a))))
    case 0x94 @ a @ _     => ("STY - zero_page_x", 2, Store    (STY (zero_page_x (a))))
    case 0x95 @ a @ _     => ("STA - zero_page_x", 2, Store    (STA (zero_page_x (a))))
    case 0x96 @ a @ _     => ("STX - zero_page_y", 2, Store    (STX (zero_page_y (a))))
    case 0x98 @ _         => ("TYA", 1, Transfer (TYA))
    case 0x99 @ a @ b @ _ => ("STA - absolute_y", 3, Store    (STA (absolute_y (a, b))))
    case 0x9A @ _         => ("TXS", 1, Stack    (TXS))
    case 0x9D @ a @ b @ _ => ("STA - absolute_x", 3, Store    (STA (absolute_x (a, b))))
    case 0xA0 @ a @ _     => ("LDY - immediate", 2, Load     (LDY (immediate (a))))
    case 0xA1 @ a @ _     => ("LDA - indexed_indirect_x", 2, Load     (LDA (indexed_indirect_x (a))))
    case 0xA2 @ a @ _     => ("LDX - immediate", 2, Load     (LDX (immediate (a))))
    case 0xA4 @ a @ _     => ("LDY - zero_page", 2, Load     (LDY (zero_page (a))))
    case 0xA5 @ a @ _     => ("LDA - zero_page", 2, Load     (LDA (zero_page (a))))
    case 0xA6 @ a @ _     => ("LDX - zero_page", 2, Load     (LDX (zero_page (a))))
    case 0xA8 @ _         => ("TAY", 1, Transfer (TAY))
    case 0xA9 @ a @ _     => ("LDA - immediate", 2, Load     (LDA (immediate (a))))
    case 0xAA @ _         => ("TAX", 1, Transfer (TAX))
    case 0xAC @ a @ b @ _ => ("LDY - absolute", 3, Load     (LDY (absolute (a, b))))
    case 0xAD @ a @ b @ _ => ("LDA - absolute", 3, Load     (LDA (absolute (a, b))))
    case 0xAE @ a @ b @ _ => ("LDX - absolute", 3, Load     (LDX (absolute (a, b))))
    case 0xB0 @ a @ _     => ("BCS - relative", 2, Branch   (BCS (relative (a))))
    case 0xB1 @ a @ _     => ("LDA - indirect_indexed_y", 2, Load     (LDA (indirect_indexed_y (a))))
    case 0xB4 @ a @ _     => ("LDY - zero_page_x", 2, Load     (LDY (zero_page_x (a))))
    case 0xB5 @ a @ _     => ("LDA - zero_page_x", 2, Load     (LDA (zero_page_x (a))))
    case 0xB6 @ a @ _     => ("LDX - zero_page_y", 2, Load     (LDX (zero_page_y (a))))
    case 0xB8 @ _         => ("CLV", 1, Flags    (CLV))
    case 0xB9 @ a @ b @ _ => ("LDA - absolute_y", 3, Load     (LDA (absolute_y (a, b))))
    case 0xBA @ _         => ("TSX", 1, Stack    (TSX))
    case 0xBC @ a @ b @ _ => ("LDY - absolute_x", 3, Load     (LDY (absolute_x (a, b))))
    case 0xBD @ a @ b @ _ => ("LDA - absolute_x", 3, Load     (LDA (absolute_x (a, b))))
    case 0xBE @ a @ b @ _ => ("LDX - absolute_y", 3, Load     (LDX (absolute_y (a, b))))
    case 0xC0 @ a @ _     => ("CPY - immediate", 2, Arith    (CPY (immediate (a))))
    case 0xC1 @ a @ _     => ("CMP - indexed_indirect_x", 2, Arith    (CMP (indexed_indirect_x (a))))
    case 0xC4 @ a @ _     => ("CPY - zero_page", 2, Arith    (CPY (zero_page (a))))
    case 0xC5 @ a @ _     => ("CMP - zero_page", 2, Arith    (CMP (zero_page (a))))
    case 0xC6 @ a @ _     => ("DEC - zero_page", 2, Dec      (DEC (zero_page (a))))
    case 0xC8 @ _         => ("INY", 1, Inc      (INY))
    case 0xC9 @ a @ _     => ("CMP - immediate", 2, Arith    (CMP (immediate (a))))
    case 0xCA @ _         => ("DEX", 1, Dec      (DEX))
    case 0xCC @ a @ b @ _ => ("CPY - absolute", 3, Arith    (CPY (absolute (a, b))))
    case 0xCD @ a @ b @ _ => ("CMP - absolute", 3, Arith    (CMP (absolute (a, b))))
    case 0xCE @ a @ b @ _ => ("DEC - absolute", 3, Dec      (DEC (absolute (a, b))))
    case 0xD0 @ a @ _     => ("BNE - relative", 2, Branch   (BNE (relative (a))))
    case 0xD1 @ a @ _     => ("CMP - indirect_indexed_y", 2, Arith    (CMP (indirect_indexed_y (a))))
    case 0xD5 @ a @ _     => ("CMP - zero_page_x", 2, Arith    (CMP (zero_page_x (a))))
    case 0xD6 @ a @ _     => ("DEC - zero_page_x", 2, Dec      (DEC (zero_page_x (a))))
    case 0xD8 @ _         => ("CLD", 1, Flags    (CLD))
    case 0xD9 @ a @ b @ _ => ("CMP - absolute_y", 3, Arith    (CMP (absolute_y (a, b))))
    case 0xDD @ a @ b @ _ => ("CMP - absolute_x", 3, Arith    (CMP (absolute_x (a, b))))
    case 0xDE @ a @ b @ _ => ("DEC - absolute_x", 3, Dec      (DEC (absolute_x (a, b))))
    case 0xE0 @ a @ _     => ("CPX - immediate", 2, Arith    (CPX (immediate (a))))
    case 0xE1 @ a @ _     => ("SBC - indexed_indirect_x", 2, Arith    (SBC (indexed_indirect_x (a))))
    case 0xE4 @ a @ _     => ("CPX - zero_page", 2, Arith    (CPX (zero_page (a))))
    case 0xE5 @ a @ _     => ("SBC - zero_page", 2, Arith    (SBC (zero_page (a))))
    case 0xE6 @ a @ _     => ("INC - zero_page", 2, Inc      (INC (zero_page (a))))
    case 0xE8 @ _         => ("INX", 1, Inc      (INX))
    case 0xE9 @ a @ _     => ("SBC - immediate", 2, Arith    (SBC (immediate (a))))
    case 0xEA @ _         => ("NOP", 1, Sys      (NOP))
    case 0xEC @ a @ b @ _ => ("CPX - absolute", 3, Arith    (CPX (absolute (a, b))))
    case 0xED @ a @ b @ _ => ("SBC - absolute", 3, Arith    (SBC (absolute (a, b))))
    case 0xEE @ a @ b @ _ => ("INC - absolute", 3, Inc      (INC (absolute (a, b))))
    case 0xF0 @ a @ _     => ("BEQ - relative", 2, Branch   (BEQ (relative (a))))
    case 0xF1 @ a @ _     => ("SBC - indirect_indexed_y", 2, Arith    (SBC (indirect_indexed_y (a))))
    case 0xF5 @ a @ _     => ("SBC - zero_page_x", 2, Arith    (SBC (zero_page_x (a))))
    case 0xF6 @ a @ _     => ("INC - zero_page_x", 2, Inc      (INC (zero_page_x (a))))
    case 0xF8 @ _         => ("SED", 1, Flags    (SED))
    case 0xF9 @ a @ b @ _ => ("SBC - absolute_y", 3, Arith    (SBC (absolute_y (a, b))))
    case 0xFD @ a @ b @ _ => ("SBC - absolute_x", 3, Arith    (SBC (absolute_x (a, b))))
    case 0xFE @ a @ b @ _ => ("INC - absolute_x", 3, Inc      (INC (absolute_x (a, b))))
    -- reserved instructions
    case _ => ("Unknown instruction", 1, UnknownInstruction)
}
