---------------------------------------------------------------------------
-- (c) Alexandre Joannou, University of Cambridge
---------------------------------------------------------------------------

unit save_ctx =
{
        spush (PC.H);
        spush (PC.L);
        spush (&STATUS)
}

unit Next =
{
    -- Highest priority, RESET
    if INT.RESET then
    {
        save_ctx;
        PC.L <- ReadMem(0xFFFC);
        PC.H <- ReadMem(0xFFFD)
    }
    -- Non maskable interrupt
    else if INT.NMI then
    {
        save_ctx;
        PC.L <- ReadMem(0xFFFA);
        PC.H <- ReadMem(0xFFFB)
    }
    -- Lowest priority, Interrupt request
    else if INT.IRQ and not STATUS.I then
    {
        save_ctx;
        STATUS.I <- true;
        PC.L <- ReadMem(0xFFFE);
        PC.H <- ReadMem(0xFFFF)
    } else nothing;
    (pc_inc, inst) = Decode (Fetch (&PC));
    PC <- PC_t(&PC + [pc_inc]);
    Display("running one inst !");
    Run(inst)
}
