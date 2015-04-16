---------------------------------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge
---------------------------------------------------------------------------

unit save_ctx () =
{
        spush (PC.H);
        spush (PC.L);
        spush (&STATUS)
}

unit Next () =
{
    Display(1,"=========================================");
    -- Highest priority, RESET
    if INT.RESET then
    {
        Display(1," --> RESET <-- ");
        save_ctx ();
        PC.L <- ReadMem(0xFFFC);
        PC.H <- ReadMem(0xFFFD)
    }
    -- Non maskable interrupt
    else if INT.NMI then
    {
        Display(1," --> NMI <-- ");
        save_ctx ();
        PC.L <- ReadMem(0xFFFA);
        PC.H <- ReadMem(0xFFFB)
    }
    -- Lowest priority, Interrupt request
    else if INT.IRQ and not STATUS.I then
    {
        Display(1," --> IRQ <-- ");
        save_ctx ();
        STATUS.I <- true;
        PC.L <- ReadMem(0xFFFE);
        PC.H <- ReadMem(0xFFFF)
    } else nothing;
    Display(2,cpuStateStr);
    Display(2,"-----------------------------------------");
    instBytes = Fetch (&PC);
    (inst_str, pc_inc, inst) = Decode (instBytes);
    Display(1, "[#":[instrNbr]:" - 0x":[&PC]:" - ":[pc_inc]:" byte":(if pc_inc > 1 then "s" else ""):"] ":inst_str);
    PC <- PC_t(&PC + [pc_inc]);
    Run(inst);
    instrNbr <- instrNbr + 1
}

unit SetRESET ( v :: bool) = { Display(3,"SetRESET(":[v]:")"); INT.RESET <- v }
unit SetNMI   ( v :: bool) = { Display(3,"SetNMI(":[v]:")");   INT.NMI   <- v }
unit SetIRQ   ( v :: bool) = { Display(3,"SetIRQ(":[v]:")");   INT.IRQ   <- v }
