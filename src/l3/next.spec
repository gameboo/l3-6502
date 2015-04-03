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
    Display("===============================");
    -- Highest priority, RESET
    if INT.RESET then
    {
        Display(" --> RESET <-- ");
        save_ctx ();
        PC.L <- ReadMem(0xFFFC);
        PC.H <- ReadMem(0xFFFD)
    }
    -- Non maskable interrupt
    else if INT.NMI then
    {
        Display(" --> NMI <-- ");
        save_ctx ();
        PC.L <- ReadMem(0xFFFA);
        PC.H <- ReadMem(0xFFFB)
    }
    -- Lowest priority, Interrupt request
    else if INT.IRQ and not STATUS.I then
    {
        Display(" --> IRQ <-- ");
        save_ctx ();
        STATUS.I <- true;
        PC.L <- ReadMem(0xFFFE);
        PC.H <- ReadMem(0xFFFF)
    } else nothing;
    Display(cpuStateStr);
    Display("-------------------------------");
    Display("#":[instrNbr]:" Fetch @ 0x":[&PC]);
    instBytes = Fetch (&PC);
    (pc_inc, inst) = Decode (instBytes);
    PC <- PC_t(&PC + [pc_inc]);
    Run(inst);
    instrNbr <- instrNbr + 1
}

unit SetRESET ( v :: bool) = INT.RESET <- v
unit SetNMI   ( v :: bool) = INT.NMI   <- v
unit SetIRQ   ( v :: bool) = INT.IRQ   <- v
