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
ZERO, T0, T1, T2, T3 = 31, 1, 2, 3, 4

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)

def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)

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

setup = ["put d 0x%x, 0x%x" % (SCRATCH + 0,  k0(LPT_DATA)),
         "put d 0x%x, 0x%x" % (SCRATCH + 8,  KBC_SELFTEST),
         "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(KBC_CMD)),
         "put d 0x%x, 0x%x" % (SCRATCH + 24, k0(KBC_DATA))]

#  T0 holds the SCRATCH base and is clobbered LAST, after both port pointers are loaded.
lc       = load_const(T0, SCRATCH)
prologue = lc + [LDQ(T1, 0,  T0),    # t1 = k0(LPT_DATA)
                 LDQ(T3, 16, T0),    # t3 = k0(KBC_CMD)
                 LDQ(T2, 24, T0),    # t2 = k0(KBC_DATA)   (#516: the drain pointer)
                 LDQ(T0, 8,  T0),    # t0 = 0xAA   (base clobbered last)
                 STQ(T0, 0,  T1)]    # [A] CONTROL: same store into a port that cannot assert
armed    = [STQ(T0, 0, T3)]          # [B] the SAME value, one port away -> IRQ 1 -> exit(1)
drain    = [LDQ(T1, 0, T2)]          # [C] read the reply; T1 (LPT ptr) is DEAD here
cycle2   = [STQ(T0, 0, T3),          # [D] a SECOND assert/deassert cycle: the latch must
            LDQ(T1, 0, T2)]          #     hold, so NEITHER announce may repeat

prog = prologue + armed + drain + cycle2
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
cmds += ["pc=0x%x" % k0(CODE),
         "step %d" % len(prologue),   # up to and including the CONTROL store
         "print t0",                  # proves we are alive here, and prints the value stored
         "step %d" % len(armed),      # the one store that differs
         "step %d" % len(drain),      # [C] the load that completes the 8042 handshake
         "print t1",                  # what the DATA port answered
         "step %d" % len(cycle2)]     # [D] drive the whole cycle a second time
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
row("kbc attrib", "yes" if (alive or sig) else "died-outside-lca", "yes",
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
    "BOUND: two full IRQ cycles, and the assert announce may appear exactly ONCE")
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
