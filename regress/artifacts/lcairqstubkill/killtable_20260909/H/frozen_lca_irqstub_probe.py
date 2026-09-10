#!/usr/bin/env python3
#
#  lcairqstubkill -- RUNG-3 WITNESS: ONE guest store to the 8042 command port ends the host.
#
#  THE DEFECT.  `dev_lca.c' registers the machine's interrupt handlers and they are bare kills:
#
#      void lca_interrupt_assert(struct interrupt *interrupt)
#      {
#              fatal("lca_interrupt_assert: TODO\n");
#              exit(1);
#      }                                        /*  and _deassert, identically  */
#
#  `DEVINIT(lca)' registers them for "<machine>.lca" and hands that SAME path to `bus_isa_init',
#  so every ISA interrupt is routed into a function whose whole body is fatal() + exit(1).
#
#  THE CHAIN, every link read in the source and then MEASURED by this probe:
#
#    1.  a guest store to the 8042 COMMAND port queues a reply; `dev_pckbc_access' ends by
#        calling `pckbc_reassert_interrupts'                            -- SYNCHRONOUS, in the
#                                                                          guest store itself
#    2.  that asserts ISA line 1; `isa_interrupt_assert' sets the PIC IRR bit
#    3.  `isa_interrupt_common': new = pic1->irr & ~pic1->ier.  `dev_8259.c' memsets the struct
#        and `ier' is written ONLY by a guest store, so AT RESET NOTHING IS MASKED and the first
#        IRR bit propagates upward on d->irq
#    4.  d->irq came from INTERRUPT_CONNECT(interrupt_base_path,...) = "<machine>.lca"
#    5.  lca_interrupt_assert(): fatal(); exit(1)
#
#  **Four guest instructions total.  No disk image, no OS, no host timer, no driver setup, and no
#  unusual value -- 0xAA is the standard 8042 self-test command.**
#
#  ROUTE CHOSEN FROM A codex ISA CENSUS (regress/artifacts/lcairqstubkill/codex_reach_20260907.txt,
#  denominator: 12 instantiation call sites in bus_isa_init).  Two of its findings decided the
#  shape, and both corrected a premise of mine:
#    *  **the WDC controllers exist only if an IDE image is attached**, so the IDE route this row
#       was originally written around is NOT available to a probe that attaches a memory file;
#    *  **PIT and RTC asserts are HOST-TIMER driven** and therefore invisible to a stepped probe,
#       while PCKBC and the UARTs are synchronous with the guest access.
#
#  THE MATCHED CONTROL IS THE LPT PORT, and the census is why it is the right one: `dev_lpt_tick'
#  is EMPTY and `dev_lpt_access' never asserts an IRQ.  So a store of the same width, through the
#  same K0SEG path, into the same ISA window, at a port that cannot assert, MUST SURVIVE.  That is
#  what attributes the death to the DEVICE REACHED rather than to storing into ISA space at all.
#
#  ONE PROCESS, control first: only the PORT differs between the two stores.
#
#  *** CONTRACT -- WHAT THIS WITNESSES AND WHAT IT DOES NOT. ***
#  It establishes that on unmodified `alphabook1' a single ordinary guest store to a documented
#  8042 register ends the host process, with the terminating stub's own diagnostic as evidence.
#  It does NOT establish that any shipped guest issues that command.
#
#  *** THE SECOND HALF OF THIS CONTRACT WAS DISCHARGED BY #516 ON 2026-09-09, AND THE SENTENCE IS
#  CORRECTED RATHER THAN DELETED so a reader can see what the round owed. ***  It read: "it is NOT
#  a detector of a repair: 'host survives' would green for a silent return, for a latched announce,
#  and for an actual interrupt implementation alike.  A fix round owes a row that discriminates
#  those."  That row is now `irq announce' + `irq honest', and their siblings cover the second stub.
#
#  WHAT IT NOW COVERS, stated so a later escape is either inside this claim or outside it:
#    * BOTH stubs -- assert and deassert.  The deassert edge is driven by [C], the load that drains
#      the 8042's reply; before that no witness in this tree reached the second stub AT ALL, and a
#      verbatim reinstatement of its exit(1) scored 6/6 on the shipped detector (MEASURED, M2d).
#    * the LATCH, by [D] -- a second full assert/deassert cycle, so an announce that repeats reds.
#    * the HONESTY of each announce, anchored to its OWN site's full text.
#  WHAT IT STILL DOES NOT COVER, disclosed under clause (e):
#    * interrupt DELIVERY.  Nothing here can observe delivery, because Alpha has none to observe --
#      that is the defect the announce reports, not an instrument limitation.
#    * the three OTHER routes to the deassert edge (a PIC1 specific EOI to ISA 0x20; an IMR write
#      to ISA 0x21 masking IRQ 1 or everything).  *** REPORTED reachable in one guest access each
#      by the pass-1 measuring seat; THE WORD HERE WAS "MEASURED" UNTIL 2026-09-09 AND NO ARTIFACT
#      ENUMERATING THOSE RUNS WAS PRESERVED -- only the 8042 route has raws.  A score claim names
#      the log that produced it, and these have none, so the claim is downgraded to its true
#      strength rather than left wearing a measurement's clothes. ***  The no-row conclusion does
#      NOT rest on it: it rests on the mutation-indistinguishability argument below, which is
#      source-derived and needs no reachability figure at all.  No
#      row is owed for them: all four routes land in the same function with the same
#      interrupt->extra, so no dev_lca.c mutant can distinguish them and a second row would be
#      vacuous by construction.  A PLAIN EOI (0x20 -> 0x20) does NOT reach it -- `d->isr' is never
#      set in dev_8259.c, so `irr &= ~isr' is a no-op -- which is worth recording because it is the
#      route a reader would reach for first.
#
#  Usage:  lca_irqstub_probe.py <gxemul-binary> [label]
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"          #  device_add(machine, "lca") is ST_ALPHABOOK1 ONLY

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-24s %-24s %-52s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

# ---------------------------------------------------------------- encoder (memory format only)
ZERO, T0, T1, T2, T3, T4, T5, T6, T7 = 31, 1, 2, 3, 4, 5, 6, 7, 8
#  #516/M12: T4..T7 added for the SECOND ISA line.  The shipped set stopped at T3, and a probe
#  reaching for an undefined T4 dies with a NameError rather than emitting a bad encoding --
#  which is the safe direction, and is how the measuring seat found it.

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)   # BWX; ungated in this tree
#  The UART registers are BYTE-wide, so the second line needs STB.  NOT a new capability:
#  regress/lca_irqstub_uart_probe.py already drives this exact device with STB on this exact
#  machine, and cpu_alpha_instr.c decodes opcode 0x0e with no BWX gate.

def load_const(reg, val):
    #  32-bit only, and deliberately so: this builds the SCRATCH pointer, never a 64-bit operand.
    lo = val & 0xffff
    hi = (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

# ---------------------------------------------------------------- addresses (ALL RAM < 64 MB)
K0SEG        = 0xfffffc0000000000
def k0(p):   return K0SEG | p

LCA_IOC_BASE = 0x180000000
LCA_IOC_CONF = LCA_IOC_BASE + 0x020      # alpha_lcareg.h
LCA_PCI_CONF = 0x1e0000000               # alpha_lcareg.h; DEVINIT maps 0x20000000 bytes here
SCRATCH      = 0x01020000
CODE         = 0x01040000
LEGAL        = 0x1                       # `idata & ~1' == 0 -> ACCEPTED by the CONF guard

assert max(SCRATCH, CODE) < 64 * 1024 * 1024, "scratch/code must be inside RAM"

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

# ---------------------------------------------------------------- session
def session(cmds, settle=1.6, spin=2.2):
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

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % int(m.group(1), 16)

print("lca_irqstub_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-14s %-24s %-24s %-52s %s" % ("row", "got", "want", "note", ""))

#  ---- ISA port addresses, derived: B = LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000 ----------------
ISA_BASE = 0x1d0000000
KBC_CMD  = ISA_BASE + 0x64        # 8042 command port; IRQ 1
LPT_DATA = ISA_BASE + 0x378       # LPT; dev_lpt_tick is EMPTY -- it never asserts
KBC_SELFTEST = 0xAA               # standard 8042 self-test: queues a reply
KBC_DATA = ISA_BASE + 0x60        # 8042 DATA port; a load DRAINS the queued reply
KBC_REPLY = 0x55                  # what `case 0xaa:' queues (dev_pckbc.c)
UART      = ISA_BASE + 0x3f8      # ns16550 tty0 on IRQ 4 -- THE SECOND ISA LINE
UART_IER  = UART + 1
UART_MCR  = UART + 4
IER_ETXRDY, MCR_IENABLE = 0x02, 0x08
#  *** THE UART ASSERTS SYNCHRONOUSLY, AND THAT IS THE WHOLE REASON THESE ROWS CAN EXIST. ***
#  DEVICE_ACCESS(ns16550) calls dev_ns16550_tick(cpu, d) INLINE at four sites, and the assert
#  lives in that tick behind `d->reg[com_mcr] & MCR_IENABLE'.  So it is NOT a host-timer route
#  and a STEPPED probe can drive it -- unlike the PIT and the RTC, whose asserts are
#  timer-driven and therefore invisible here.  bus_isa_init installs it UNCONDITIONALLY: no
#  IDE image, no device_add, no machine modification, which is what keeps this a witness
#  rather than a laundered one.

setup = ["put d 0x%x, 0x%x" % (SCRATCH + 0,  k0(LPT_DATA)),
         "put d 0x%x, 0x%x" % (SCRATCH + 8,  KBC_SELFTEST),
         "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(KBC_CMD)),
         "put d 0x%x, 0x%x" % (SCRATCH + 24, k0(KBC_DATA)),
         "put d 0x%x, 0x%x" % (SCRATCH + 32, k0(UART_IER)),
         "put d 0x%x, 0x%x" % (SCRATCH + 40, k0(UART_MCR))]

#  T7 holds the SCRATCH base now, so every port pointer is loaded before anything clobbers it.
lc       = load_const(T7, SCRATCH)
prologue = lc + [LDQ(T1, 0,  T7),    # t1 = k0(LPT_DATA)
                 LDQ(T3, 16, T7),    # t3 = k0(KBC_CMD)
                 LDQ(T2, 24, T7),    # t2 = k0(KBC_DATA)
                 LDQ(T4, 32, T7),    # t4 = k0(UART_IER)
                 LDQ(T5, 40, T7),    # t5 = k0(UART_MCR)
                 LDQ(T0, 8,  T7),    # t0 = 0xAA
                 STQ(T0, 0,  T1)]    # [A] CONTROL: a port that cannot assert -- must survive
armed    = [STQ(T0, 0, T3)]          # [B] ASSERT #1   aggregate 0x00 -> 0x02
#  *** [E] IS WHY THIS PROBE HAS A SECOND DEVICE AT ALL: TWO ASSERT EDGES WITH NO DEASSERT
#  BETWEEN. ***  `isa_interrupt_common' asserts on ANY change of `pic1->irr & ~pic1->ier' to a
#  different NONZERO value -- not only on 0 -> nonzero -- so raising a SECOND line re-enters the
#  assert stub while the first is still pending.  That is the ONLY sequence in which a defect in
#  the ASSERT guard is observable, and no single-line sequence can produce it: an IMR mask/unmask
#  gives assert -> deassert -> assert, and the deassert in the middle sets the sibling latch bit.
second   = [LDA(T6, IER_ETXRDY),  STB(T6, 0, T4),
            LDA(T6, MCR_IENABLE), STB(T6, 0, T5)]    # [E] ASSERT #2   0x02 -> 0x12
#  [F] drops IRQ 4 again -- and note this is a THIRD ASSERT, not a deassert: 0x12 -> 0x02 is a
#  change to a different NONZERO aggregate.  Dropping it here is what lets [C] still take the
#  aggregate to ZERO, so the deassert edge the round owes is preserved rather than traded away.
clear2   = [LDA(T6, 0), STB(T6, 0, T4)]              # [F] ASSERT #3   0x12 -> 0x02
drain    = [LDQ(T1, 0, T2)]          # [C] DEASSERT #1  0x02 -> 0x00; T1 (LPT ptr) is DEAD here
cycle2   = [STQ(T0, 0, T3),          # [D] ASSERT #4 and DEASSERT #2 -- the latch ACROSS a cycle
            LDQ(T1, 0, T2)]
#  [G] read com_mcr BACK.  dev_ns16550.c answers a read of com_mcr with `d->reg[com_mcr]', so a
#  returned 0x08 could only have come from the device's own register file -- RAM and unmapped
#  space answer differently.  *** THIS REPLACES A GREP FOR THE STRING "ns16550", which the
#  measuring seat flagged in its OWN proposal: that string comes from debug(), so the row would go
#  quiet under -q without saying so -- a control that cannot fail in the state that matters. ***
mcrback  = [LDQ(T6, 0, T5)]

prog = prologue + armed + second + clear2 + drain + cycle2 + mcrback
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
cmds += ["pc=0x%x" % k0(CODE),
         "step %d" % len(prologue),   # up to and including the CONTROL store
         "print t0",                  # proves we are alive here, and prints the value stored
         "step %d" % len(armed),      # [B] ASSERT #1
         "step %d" % len(second),     # [E] ASSERT #2 -- second line up, no deassert between
         "step %d" % len(clear2),     # [F] ASSERT #3 -- second line down again
         "step %d" % len(drain),      # [C] DEASSERT #1 -- completes the 8042 handshake
         "print t1",                  # what the DATA port answered
         "step %d" % len(cycle2),     # [D] drive the whole cycle a second time
         "step %d" % len(mcrback),    # [G] and ONLY NOW execute the readback
         "print t6"]                  # DEVICE SIGNATURE for the second ISA line
txt, alive = session(cmds)

ctl_alive = ("print t0" in txt) and (printed(txt, "t0") != "absent")

#  ---- CONTROL: an identical store into a non-asserting ISA port SURVIVES -----------------------
row("lpt ctl", "yes" if ctl_alive else "died-early", "yes",
    "CONTROL: same width, same window, a port that cannot assert -- must survive")

#  ---- LIVENESS + DEVICE SIGNATURE: the 8042 actually saw the command --------------------------
#  Its own handler prints this; RAM and unmapped space cannot.
saw_kbc = ("pckbc: write to CTL" in txt)
row("kbc live", "yes" if saw_kbc else "no", "yes",
    "DEVICE SIGNATURE: dev_pckbc_access announced the command it received")

#  ---- THE DEFECT ROW ---------------------------------------------------------------------------
#  ORACLE POLARITY is the ladder's: assert the CORRECT behaviour, so this is RED pre-fix and
#  GREEN post-fix with the SAME script.
row("kbc kill", "alive" if alive else "dead", "alive",
    "one ordinary store to a documented 8042 register must NOT end the host")

#  ---- ATTRIBUTION: if it died, it died in ONE OF THE TWO LCA INTERRUPT STUBS --------------------
#  Green in both directions by construction; RED only if the host dies WITHOUT this diagnostic.
#
#  *** THE OPERAND IS `lca_interrupt' AND NOT `lca_interrupt_assert', AND THE WIDENING IS A
#  CORRECTNESS FIX RATHER THAN A LOOSENING.  Found 2026-09-09 by the measuring seat. ***  This
#  session now drives BOTH stubs, so a reinstated exit(1) in the DEASSERT stub kills the host with
#  `lca_interrupt_deassert: TODO' -- which does not contain the string `lca_interrupt_assert'
#  ("de" sits in the middle).  The row still went RED, correctly, and reported `died-elsewhere' --
#  **a true failure under a false label**, sending a reader hunting a death outside this file when
#  it happened in the sibling function four lines away.  A red must not lie about WHERE.
sig = ("lca_interrupt" in txt)
#  *** THE LABEL READ `died-outside-lca' FOR ONE DAY AND WAS MEASURABLY FALSE.  Corrected
#  2026-09-09 from the measuring seat's mutant M14. ***  Under a SILENT death inside
#  lca_interrupt_deassert the row printed `died-outside-lca' while the death was INSIDE lca --
#  one false label traded for another, and the SPECIFIC one is worse than the vague one it
#  replaced, because a reader can act on it and go hunting in the wrong file.  **This row's
#  evidence is the ABSENCE OF A DIAGNOSTIC, never a location, so that is all it may claim.**
row("kbc attrib", "yes" if (alive or sig) else "no-lca-diagnostic", "yes",
    "ATTRIBUTION: a death here must carry EITHER interrupt stub's own diagnostic")

for _l in txt.split(chr(10)):
    if "lca_interrupt" in _l or "pckbc: write to CTL" in _l:
        print("  EVIDENCE: %s" % _l.strip())

print("")
#  ================================================================================================
#  #516: THE ROWS THIS PROBE'S OWN CONTRACT SAYS THE FIX ROUND OWES.
#
#  The contract above states the blind spot in its own words: *"it is NOT a detector of a repair:
#  'host survives' would green for a silent return, for a latched announce, and for an actual
#  interrupt implementation alike.  A fix round owes a row that discriminates those."*
#
#  The shipped disposition is DECLINE + a bounded per-instance announce, so the discriminator is the
#  announce itself: a silent return prints nothing, and an actual implementation would print nothing
#  either (it would deliver instead).  Only the chosen repair prints THIS text.
ANN_A = "ISA interrupt assert not implemented"
#  #516: the honesty rows are anchored to their OWN site's full text.  A bare
#  "Alpha has no" matched EITHER announce, so once the deassert row was added a
#  dishonest ASSERT announce swept the table clean (MEASURED: M5, 8/8).
HON_A = "ISA interrupt assert not implemented (Alpha has no"
HON_D = "ISA interrupt deassert not implemented (Alpha has no"

#  ---- the SECOND ISA line's own device-signature control -------------------------------
row("uart live", printed(txt, "t6"), "0x%x" % MCR_IENABLE,
    "DEVICE SIGNATURE for [E]: com_mcr reads back from the UART's own register file")

row("irq announce", "yes" if ANN_A in txt else "no", "yes",
    "DISCRIMINATOR: a silent return and a real implementation both print nothing here")

#  *** THE ANNOUNCE MUST NAME ALPHA'S MISSING DELIVERY, NOT MERELY SAY "TODO". ***  The round's whole
#  claim is that it stops the host dying WITHOUT making interrupts work, and the diagnostic is the
#  only place a guest-side reader ever learns that.  A message that omits it would let the record be
#  read as "interrupts now work", which is exactly what the round must not assert.
row("irq honest", "yes" if HON_A in txt else "no", "yes",
    "the announce must say WHY -- the round fixes the kill, not the delivery")

#  ---- #516: THE DEASSERT SITE.  Without these the deassert stub has NO witness at all. --------
row("drain sig", printed(txt, "t1"), "0x%x" % KBC_REPLY,
    "DEVICE SIGNATURE: only the 8042 answers 0x55 to a load from ISA 0x60")

ANN_D = "ISA interrupt deassert not implemented"
row("deassert ann", "yes" if ANN_D in txt else "no", "yes",
    "DISCRIMINATOR: the SECOND stub -- reached only once the queue empties")

row("deassert honest", "yes" if HON_D in txt else "no", "yes",
    "SIBLING PARITY: the deassert announce owes the same reason its sibling does")

#  ---- THE LATCH IS THE OTHER HALF OF THE CLAIM.  "(once)" is an ASSERTION about a bound. ----
row("assert once", txt.count(ANN_A), 1,
    "BOUND: FOUR assert edges, TWO with no deassert between -- this is what kills M12")
row("deassert once", txt.count(ANN_D), 1,
    "BOUND: same for the sibling -- a latch that resets is a log flood, not a latch")

#  *** #516 MOVED THIS COMPUTATION DOWN, AND THE PROBE'S OWN OUTPUT IS WHAT EXPOSED THE NEED. ***
#  It used to sit ABOVE the last rows, so adding rows below it produced a score whose numerator was
#  counted over the OLD row set and whose denominator was evaluated at print time: every row
#  printed `ok` and the summary said 4/6.  A score line that contradicts its own rows is the
#  cheapest possible signal, and it is only available because the rows are printed individually.
#  Keeping the computation adjacent to the print makes the split impossible to reintroduce.
ok = sum(1 for _, o in rows if o)
print("LCAIRQ_RESULT=%d/%d" % (ok, len(rows)))
print("LCAIRQ_WITNESS=%s" % ("PASS" if ok == len(rows) else "FAIL"))
print("LCAIRQ_DONE")
