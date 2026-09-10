#!/usr/bin/env python3
#  #516 pass-2-repair MEASURING SEAT -- PROPOSED repair of the M12 floor breach.
#  Structurally the shipped 11-row probe with ONE insertion: a second ASSERT EDGE driven
#  between [B] and [C], from a DIFFERENT ISA line, with no deassert between.  Same session,
#  no new load sensitivity.  The existing deassert coverage is preserved by turning the
#  second line back OFF before [C], so the 8042 drain still takes the aggregate to zero.
#
#     [A] LPT control store                      (no edge)
#     [B] STQ 0xAA -> 8042 CMD  (ISA 0x64)       agg 0x00 -> 0x02   ASSERT #1
#     [E] STB 0x02 -> UART IER, STB 0x08 -> MCR  agg 0x02 -> 0x12   ASSERT #2   <-- the new edge
#     [F] STB 0x00 -> UART IER                   agg 0x12 -> 0x02   ASSERT #3 (still nonzero)
#     [C] LDQ  <- 8042 DATA     (ISA 0x60)       agg 0x02 -> 0x00   DEASSERT #1
#     [D] the whole 8042 cycle again             ASSERT #4, DEASSERT #2
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-15s %-24s %-24s %-52s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

ZERO, T0, T1, T2, T3, T4, T5, T6, T7 = 31, 1, 2, 3, 4, 5, 6, 7, 8
def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)
def load_const(reg, val):
    lo = val & 0xffff; hi = (val >> 16) & 0xffff
    if lo >= 0x8000: hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo: ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

K0SEG = 0xfffffc0000000000
def k0(p): return K0SEG | p
SCRATCH, CODE = 0x01020000, 0x01040000
ISA_BASE = 0x1d0000000
KBC_CMD, KBC_DATA, LPT_DATA = ISA_BASE + 0x64, ISA_BASE + 0x60, ISA_BASE + 0x378
UART = ISA_BASE + 0x3f8
UART_IER, UART_MCR = UART + 1, UART + 4
KBC_SELFTEST, KBC_REPLY = 0xAA, 0x55
IER_ETXRDY, MCR_IENABLE = 0x02, 0x08

DUMMY = "/tmp/gxo516q_dummy.bin"
if not os.path.exists(DUMMY): open(DUMMY, "wb").write(b"\0" * 8)

def session(cmds, settle=1.6, spin=2.2):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "0x20000000:" + DUMMY]); os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.1)
            if not r: continue
            try:
                d = os.read(fd, 65536)
                if not d: return False
                buf += d.decode("latin-1", "replace")
            except OSError: return False
        return True
    alive = rd(settle)
    for i, c in enumerate(cmds):
        try: os.write(fd, (c + "\n").encode("latin-1"))
        except OSError: alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.35): alive = False; break
    try: os.write(fd, b"quit\n"); rd(0.4)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return "absent" if not m else "0x%x" % int(m.group(1), 16)

print("lca_irqstub_probe_REPAIR -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-15s %-24s %-24s %-52s %s" % ("row", "got", "want", "note", ""))

setup = ["put d 0x%x, 0x%x" % (SCRATCH +  0, k0(LPT_DATA)),
         "put d 0x%x, 0x%x" % (SCRATCH +  8, KBC_SELFTEST),
         "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(KBC_CMD)),
         "put d 0x%x, 0x%x" % (SCRATCH + 24, k0(KBC_DATA)),
         "put d 0x%x, 0x%x" % (SCRATCH + 32, k0(UART_IER)),
         "put d 0x%x, 0x%x" % (SCRATCH + 40, k0(UART_MCR))]

prologue = load_const(T7, SCRATCH) + [
    LDQ(T1,  0, T7), LDQ(T3, 16, T7), LDQ(T2, 24, T7),
    LDQ(T4, 32, T7), LDQ(T5, 40, T7), LDQ(T0, 8, T7),
    STQ(T0,  0, T1)]                                   # [A] CONTROL
armed  = [STQ(T0, 0, T3)]                              # [B] ASSERT #1
second = [LDA(T6, IER_ETXRDY), STB(T6, 0, T4),
          LDA(T6, MCR_IENABLE), STB(T6, 0, T5)]        # [E] ASSERT #2 -- the new edge
clear2 = [LDA(T6, 0), STB(T6, 0, T4)]                  # [F] drop IRQ 4 again
drain  = [LDQ(T1, 0, T2)]                              # [C] DEASSERT #1
cycle2 = [STQ(T0, 0, T3), LDQ(T1, 0, T2)]              # [D] ASSERT #4, DEASSERT #2

prog = prologue + armed + second + clear2 + drain + cycle2
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
cmds += ["pc=0x%x" % k0(CODE),
         "step %d" % len(prologue), "print t0",
         "step %d" % len(armed),
         "step %d" % len(second),
         "step %d" % len(clear2),
         "step %d" % len(drain), "print t1",
         "step %d" % len(cycle2)]
txt, alive = session(cmds)

ANN_A = "ISA interrupt assert not implemented"
ANN_D = "ISA interrupt deassert not implemented"
HON_A = "ISA interrupt assert not implemented (Alpha has no"
HON_D = "ISA interrupt deassert not implemented (Alpha has no"

row("lpt ctl", "yes" if printed(txt, "t0") != "absent" else "died-early", "yes", "CONTROL")
row("kbc live", "yes" if "pckbc: write to CTL" in txt else "no", "yes", "DEVICE SIGNATURE 8042")
row("uart live", "yes" if "ns16550" in txt else "no", "yes",
    "#516b DEVICE SIGNATURE: the SECOND ISA line (ns16550, IRQ 4) really ran")
row("kbc kill", "alive" if alive else "dead", "alive", "no host death")
row("kbc attrib", "yes" if (alive or ("lca_interrupt" in txt)) else "died-outside-lca", "yes",
    "ATTRIBUTION")
row("irq announce", "yes" if ANN_A in txt else "no", "yes", "DISCRIMINATOR assert")
row("irq honest", "yes" if HON_A in txt else "no", "yes", "assert announce names the reason")
row("drain sig", printed(txt, "t1"), "0x%x" % KBC_REPLY, "DEVICE SIGNATURE 8042 reply")
row("deassert ann", "yes" if ANN_D in txt else "no", "yes", "DISCRIMINATOR deassert")
row("deassert honest", "yes" if HON_D in txt else "no", "yes", "SIBLING PARITY")
row("assert once", txt.count(ANN_A), 1,
    "BOUND: FOUR assert edges incl. TWO with no deassert between -- kills M12")
row("deassert once", txt.count(ANN_D), 1, "BOUND: sibling")

for _l in txt.split(chr(10)):
    if "LCAEDGE" in _l or "lca_interrupt" in _l or "lca: ISA interrupt" in _l:
        print("  EVIDENCE: %s" % _l.strip())

ok = sum(1 for _, o in rows if o)
print("REPAIR_RESULT=%d/%d" % (ok, len(rows)))
print("REPAIR_DONE")
