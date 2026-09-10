# lcairqedgepin -- ROW DESIGN: a green-run pin for the second ISA line's assert edge in regress/lca_irqstub_probe.py

Please do not simply ratify. Check the premises, not just the derivations. ANALYSIS only -- prose plus the
exact row you would add, quoted in the probe's own idiom; write no file. VERDICT LINE FIRST. Ordinary
interrupt-controller modelling engineering.

## THE TREE
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`. Read `regress/lca_irqstub_probe.py` (the shipped 12-row
detector of `#516`; its program phases [B]..[G], the `uart live` row that raises and drops the ns16550 on
IRQ 4 between the 8042's assert and its drain, its CONTRACT header which discloses this row under clause
(e)), `src/devices/dev_8259.c` (OCW2/OCW3 handling: how a guest selects IRR vs ISR for readback, and what a
read of the command port returns), `src/devices/bus_isa.c` (`isa_interrupt_common`: the aggregate
`pic1->irr & ~pic1->ier` edge test), `src/devices/dev_lca.c` (the two `#516` interrupt stubs), and
`src/devices/dev_ns16550.c` (the inline tick that asserts IRQ 4 when `com_mcr & MCR_IENABLE`).

## SETTLED (say which you cannot verify)
S1. `#516` de-fatalised `lca_interrupt_assert/_deassert` into once-latched announces. The detector's twelfth
    row `uart live` proves the MCR store landed (reads MCR back, wants 0x8), and its `assert once` row
    counts the assert announce (want 1). On the fix the latched announce prints once whether or not the
    UART phase [E] re-entered the stub, so if the UART silently stopped asserting, mutant M12 (the
    assert-guard latch-bit swap, which swept 11/11 before the row was added) would escape again and no
    green-run row would say why. The measurement-time evidence was M12's own `assert once` = 3.
S2. The row filed as `lcairqedgepin`: read PIC1's IRR back after [E] and want 0x12 (IRQ 1 from the 8042 and
    IRQ 4 from the UART both pending). One row; it changes the instrument, so it owes a table.
S3. Every probe here single-steps a guest program built from `put w` words at CODE with `put d` operands
    at SCRATCH, then `print tN`; interrupt DELIVERY is invisible while stepping, but device dispatch
    (including the 8259's register file) is reached synchronously by guest loads and stores.

## THE QUESTIONS
Q1. How does a guest read PIC1's IRR on this model? Quote dev_8259.c's OCW3 handling: the exact byte to
    write to port 0x20 (read-register command selecting IRR), and what a subsequent load from 0x20 returns
    -- irr, isr, or the poll result. Is the read masked by IER? Does the model implement OCW3 at all, and
    if not, what DOES a read of 0x20/0x21 return (IMR at 0x21?) and which of those exposes the pending set?
Q2. The exact row: the [E'] phase (a store of the OCW3 byte, a load of 0x20 into a free register, `print`
    it), where it sits relative to [E] and [F] in the existing program, which registers are free (the
    probe's register discipline is documented in its header), and the wanted value with its derivation
    (which bits of IRR are set after [B] and [E], given `pic1->irr` semantics in dev_8259.c and whether the
    8042's IRQ is still pending before the drain [C]).
Q3. CHANNEL: name the mutant this row kills that no existing row kills (M12 under a silently-dead UART
    edge is the filed case -- state precisely the double mutant: M12 plus what UART change), and the
    observable that differs. If the honest answer is that the row pins the UART edge INDEPENDENTLY of the
    stub (a control row rather than a kill row), say so -- that is a valid disposition for a filed row.
Q4. Table cost: which of the 16 measured cells of `#516` could change score when this row is added, and
    would you re-run all 16 or the base plus M12 plus the two `uart`-adjacent cells? Say why.
State what you read versus what you took from this packet. If you found something ELSE, say so.
