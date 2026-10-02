#!/usr/bin/env python3
"""lca_irqstub_uart_probe.py -- a SECOND, independent guest path to the same stub.

    usage:  lca_irqstub_uart_probe.py <gxemul-binary> [label]

*** READ THIS FIRST: THIS ROW WAS ALREADY WITNESSED, AND I DID NOT CHECK BEFORE BUILDING THIS.
`regress/lca_irqstub_probe.py' shipped in `7c2f8e4' on 2026-09-07 and reaches the same two
stubs with ONE guest store to the 8042 command port, scoring 3/4, with an LPT control chosen
from a codex ISA census.  The ledger's witness field said so in detail.  I built this without
reading it and overwrote that file; it has been restored and this one renamed. ***

SO WHAT IS THIS FOR?  It is a SECOND path through a DIFFERENT device -- ns16550 rather than
8042, IRQ 4 rather than IRQ 1, three byte stores rather than one word store.  Two independent
guest routes to one stub is worth having: a repair that silences one and not the other is
visible immediately.  But it is a SUPPLEMENT, and the 8042 probe is the row's witness of
record.

WHAT THIS PINS.  `dev_lca.c' registers `lca_interrupt_assert'/`_deassert' as the machine's
interrupt template, and both are a bare diagnostic plus `exit(1)' with NO GUARD.  `devinit_lca()'
hands the same interrupt path to `bus_isa_init()', which connects the upstream interrupt and
UNCONDITIONALLY installs the first ns16550 on ISA IRQ 4.  So the source-derived path is
[#556, 2026-10-02 -- a records correction; the text above is kept as it was written] dev_lca.c:119,140 implement
per-instance warning latches and return without exit(1); the committed build survives the interrupt and passes.
(hbundle_regress27:F9: regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)

    dev_ns16550_tick() -> isa_interrupt_assert() -> isa_interrupt_common()
                       -> lca_interrupt_assert() -> exit(1)

and it needs no machine-description modification, which is what makes it a witness candidate
rather than laundering.

*** WHY THIS PROBE USES GUEST STORES AND NOT `put'.  MEASURED, and it is the reason an earlier
attempt of mine did not fire. ***  The debugger's `put' calls memory_rw with NO_EXCEPTIONS
(debugger_cmds.c:1461,:1507), and memory_rw only invokes a device handler when
`!no_exceptions || (flags & DM_READS_HAVE_NO_SIDE_EFFECTS)'.  ns16550 registers DM_DEFAULT
(dev_ns16550.c:353), so **a debugger `put' to the UART never reaches DEVICE_ACCESS(ns16550)** --
the write is absorbed and the debugger still echoes it back, which is what makes it look like it
worked.  Device access in a probe must be made by GUEST INSTRUCTIONS; `put' is for RAM only.

The UART registers are byte-wide, so this needs `stb'.  That is a BWX instruction and a 21066
would not have BWX on real hardware -- but `cpu_alpha_instr.c:895' decodes `case 0x0e' with no
feature gate, and `ALPHA_FEATURE_BWX' (cpu_alpha.h:57) is DEFINED AND NEVER CONSULTED anywhere in
the tree.  So stb executes here on any Alpha.  Recorded because it is a fact about the emulator,
not about the hardware, and a future round that gates BWX would break this probe.

ORACLE POLARITY: this asserts the CORRECT behaviour -- the session SURVIVES an ordinary UART
interrupt.  It is therefore RED on the committed build (which exits) and GREEN once the stubs stop
ending the process.

ATTRIBUTION: `ram ctl' runs the IDENTICAL instruction sequence against RAM instead of the UART.
If that also died, the death would be the code sequence and not the device.  One control, two
hypotheses separated.
"""
import os, sys, pty, select, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-12s %-12s %-60s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder
ZERO = 31
T0, T1, T2, T3, T4 = 1, 2, 3, 4, 5

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)   # BWX; ungated in this tree
SELFBR = 0xc3ffffff                                            # br r31, -1

def load_const(reg, val):
    lo, hi = val & 0xffff, (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

# ---------------------------------------------------------------- addresses
K0SEG   = 0xfffffc0000000000
def k0(p): return K0SEG | p

LCA_ISA_BASE = 0x1c0000000 + 0x10000000      # LCA_PCI_SIO + 0x10000000, dev_lca.c:47
UART         = LCA_ISA_BASE + 0x3f8          # bus_isa.c:250, isa_portbase + 0x3f8
SCRATCH = 0x01020000
CODE    = 0x01040000
RAMDST  = 0x01060000                          # the control's harmless target

IER_ETXRDY, MCR_IENABLE, ANY_BYTE = 0x02, 0x08, 0x41

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

def session(cmds, settle=1.6, spin=4.0):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY])
        os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r:
                continue
            try:
                d = os.read(fd, 65536)
                if not d:
                    return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.35):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def build(base):
    """The identical sequence, parameterised only by the DESTINATION base."""
    p  = load_const(T0, SCRATCH)
    p += [LDQ(T1, 0, T0), LDQ(T2, 8, T0), LDQ(T3, 16, T0)]
    p += [LDA(T4, IER_ETXRDY),  STB(T4, 0, T1)]     # IER  = enable tx-empty interrupt
    p += [LDA(T4, MCR_IENABLE), STB(T4, 0, T2)]     # MCR  = OUT2, gates the assert
    p += [LDA(T4, ANY_BYTE),    STB(T4, 0, T3)]     # THR  -> sets IIR_TXRDY
    p += [SELFBR]                                    # free-run so DEVICE_TICK is reached
    setup = ["put d 0x%x, 0x%x" % (SCRATCH + 0,  k0(base + 1)),   # IER
             "put d 0x%x, 0x%x" % (SCRATCH + 8,  k0(base + 4)),   # MCR
             "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(base + 0))]   # THR
    cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op)
                    for i, op in enumerate(p)]
    return cmds + ["pc=0x%x" % k0(CODE), "continue"]

print("lca_irqstub_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-14s %-12s %-12s %-60s %s" % ("row", "got", "want", "note", ""))

#  ---- CONTROL 1: LIVENESS ---------------------------------------------------------------
t, alive = session(["put w 0x%x, 0x%08x" % (k0(CODE), SELFBR),
                    "pc=0x%x" % k0(CODE), "continue"])
row("live", "alive" if alive else "died", "alive",
    "CONTROL: a free-running self-branch alone must survive")

#  ---- CONTROL 2: ATTRIBUTION -- the same instructions, aimed at RAM ----------------------
t2, alive2 = session(build(RAMDST))
row("ram ctl", "alive" if alive2 else "died", "alive",
    "ATTRIBUTION: the IDENTICAL sequence against RAM must survive")

#  ---- THE WITNESS -----------------------------------------------------------------------
t3, alive3 = session(build(UART))
row("uart irq", "alive" if alive3 else "died", "alive",
    "an ordinary UART interrupt must not end the emulator")
row("stub named", "no" if "lca_interrupt_assert" not in t3 else "yes", "no",
    "the stub's own TODO diagnostic must not appear")

#  ================================================================================================
#  #516: THE LATCH ROW, and this probe is the only place it can be measured.
#
#  This session FREE-RUNS on a self-branch so `DEVICE_TICK' is reached repeatedly, and the UART is
#  left with IER on -- so the tick keeps re-asserting the ISA interrupt for the whole spin window.
#  **That makes an UNLATCHED announce print MANY times and a latched one print EXACTLY ONCE**,
#  which is the only observable difference between the two, and it exists here and not in the
#  sibling probe.
#  [#556, 2026-10-02 -- a records correction; the text above is kept as it was written] Historical note: lines
#  181-189 originally claimed the session repeatedly entered the assert callback; as explained at :195-231,
#  edge-triggering enters it once regardless of latching.  (hbundle_regress27:F10:
#  regress/artifacts/astraretro_harness_20260926/HARNESS_DISPOSITIONS.md)
#
#  Counting is the oracle, not presence: a presence row would be satisfied by a latch that never
#  engages, which is precisely the mutant this row exists to catch.
ANN_A = "ISA interrupt assert not implemented"
_n_ann = t3.count(ANN_A)

#  *** MEASURED VACUOUS AS A LATCH TEST, AND RELABELLED RATHER THAN LEFT TO IMPLY COVERAGE IT DOES
#  NOT HAVE.  The grok seat predicted this on pass 2 and a mutant confirmed it. ***
#
#  I wrote this row believing the free-running tick RE-ENTERS `lca_interrupt_assert', so that an
#  unlatched announce would print many times and a latched one once.  grok read the path instead:
#  **`isa_interrupt_common' is EDGE-TRIGGERED on the PIC aggregate.**  It calls ASSERT when IRR goes
#  0->nonzero and returns when the aggregate merely stays asserted -- and this session leaves IER on
#  and never drops IRR, so the stub is entered EXACTLY ONCE however long the guest free-runs.
#
#  MEASURED, not conceded: mutant `M1_unlatch' removes the latch entirely so the announce fires on
#  every entry, and it scores **6/6 and 5/5 with this count still reading 1** -- a CLEAN SWEEP.
#  (regress/artifacts/lcairqstubkill/killtable_20260908/)
#
#  So the row cannot discriminate the latch, and it no longer claims to.  What it DOES pin is real
#  and worth keeping: the announce is not emitted more than once per session, which would catch a
#  future edit that moved it outside the guard AND a future change that made the stub re-entrant.
#
#  *** THE LATCH IS UNEXERCISED BY **THIS** WITNESS, AND THAT IS THE WHOLE OF THE CLAIM. ***
#  Exercising it needs TWO assert edges in one session -- an IRR that falls and rises again -- and
#  this probe cannot produce them BY CONSTRUCTION: it free-runs with IER on, so the UART keeps
#  re-asserting and the aggregate never falls.
#
#  *** THIS SENTENCE READ "UNEXERCISED BY ANY WITNESS IN THIS TREE" UNTIL 2026-09-09, AND THE
#  ROUND'S OWN REPAIR HAD ALREADY REFUTED IT FIFTEEN LINES BELOW. ***  `lca_irqstub_probe.py'
#  drives a second assert AND a second deassert edge at [D], and its `assert once' / `deassert
#  once' rows DO exercise the latch -- MEASURED: `M9_deassert_nolatch' and `M10_assert_nolatch'
#  each score 10/11, killed by exactly those count rows
#  (regress/artifacts/lcairqstubkill/killtable_20260909/TABLE_D.out).
#
#  The defect was SCOPE: a claim true of this probe was written as a claim about the tree, and it
#  then survived the very edit that falsified it, because the correction was appended BELOW it
#  instead of applied TO it.  **An absence record that its own round refutes gets corrected, not
#  left standing next to its refutation** -- and a reader hitting this line first would have taken
#  the stale half, because it is the one that reads like a settled fact.
#  Found by the pass-2 review seat, which is the half of a correction nobody re-reads.
row("irq once", str(_n_ann) if alive3 else "died", "1",
    "the announce is not repeated (does NOT test the latch -- see above)")

#  *** THIS DISCLOSURE WAS OVERTURNED ON 2026-09-09 AND IS CORRECTED IN PLACE, NOT DELETED. ***
#  It is kept verbatim below because it is the reasoning that had to be refuted, and because the
#  round nearly shipped on it.  WHAT IS NOW TRUE: the deassert edge IS reachable, and by FOUR
#  independent one-instruction routes, so disclosing it under clause (e) was the WRONG DISPOSITION
#  -- clause (e) is for cells that are unreachable or need a capability the tree lacks, and this
#  needed neither.  It is a clause-(b) FLOOR BREACH (L2), and it was MEASURED: a verbatim
#  reinstatement of exit(1) at the deassert site alone scored 6/6 on the six-row detector.
#  `lca_irqstub_probe.py' now drives that edge at [C] and the latch at [D]; see its contract.
#  THIS probe remains assert-only BY CONSTRUCTION -- it free-runs with IER on, so the UART keeps
#  re-asserting and the aggregate never falls -- which is why the finding lands in its sibling.
#  The superseded text follows.
#
#  *** DISCLOSED, NOT BUILT: THE DEASSERT LATCH IS UNWITNESSED. ***  The grok seat traced this on
#  pass 1: `isa_interrupt_common' takes ONE EDGE per call -- ASSERT when IRR goes 0->nonzero,
#  DEASSERT when it goes nonzero->0 -- and NEITHER witness reaches the deassert edge.  The 8042
#  probe never reads the 0x55 reply; this one leaves IER on and free-runs, so the aggregate never
#  falls back to zero.  **So `lca_interrupt_deassert' and its separate latch bit have no row here,
#  and no mutant of them could be killed.**  Coverage debt under clause (e), named rather than left
#  to be discovered.  Closing it needs a guest sequence that LOWERS the interrupt again, which is a
#  different session and is not built in this round.

#  *** #516 MOVED THIS COMPUTATION DOWN, for the same reason as the sibling probe. ***  It sat
#  ABOVE the last row, so `bad` was computed over the OLD row set while `len(rows)` was evaluated
#  at print time.  Post-fix that happened to render correctly (nothing failed, so `bad` was empty
#  either way) and PRE-FIX it did not: the run reported 3/5 when the honest score was 2/5, because
#  the added row failed and was not counted.  **A split scorer is silently right whenever nothing
#  fails, which is exactly when nobody checks it.**  Keeping the computation adjacent to the print
#  makes the split impossible to reintroduce.
bad = [n for n, ok in rows if not ok]
print("\nIRQSTUB_RESULT=%d/%d" % (len(rows) - len(bad), len(rows)))
if bad:
    print("FAILING: " + " ".join(bad))
open("/tmp/irqstub_last.txt", "w").write(t3)
print("IRQSTUB_DONE")
