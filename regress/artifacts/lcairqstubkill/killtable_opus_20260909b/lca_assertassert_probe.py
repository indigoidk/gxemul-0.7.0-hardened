#!/usr/bin/env python3
#  #516 pass-2-repair MEASURING SEAT: does a SECOND ASSERT EDGE with NO intervening
#  deassert exist on unmodified `alphabook1', reachable by ordinary stepped guest stores?
#
#  Sequence:  [A] control store to LPT (cannot assert)
#             [B] STQ 0xAA -> 8042 CMD (ISA 0x64)      -> IRQ 1  -> aggregate 0x00 -> 0x02  ASSERT#1
#             [E] STB IER_ETXRDY -> UART 0x3f9,
#                 STB MCR_IENABLE -> UART 0x3fc        -> IRQ 4  -> aggregate 0x02 -> 0x12  ASSERT#2
#  No drain between, so no deassert edge can intervene.
#  Both legs are ALREADY witnessed in this tree (lca_irqstub_probe.py / lca_irqstub_uart_probe.py).
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-24s %-24s %-52s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

ZERO, T0, T1, T2, T3, T4, T5, T6, T7 = 31, 1, 2, 3, 4, 5, 6, 7, 8

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)   # BWX, as lca_irqstub_uart_probe.py uses

def load_const(reg, val):
    lo = val & 0xffff; hi = (val >> 16) & 0xffff
    if lo >= 0x8000: hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo: ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

K0SEG = 0xfffffc0000000000
def k0(p): return K0SEG | p
SCRATCH, CODE = 0x01020000, 0x01040000
ISA_BASE  = 0x1d0000000
KBC_CMD   = ISA_BASE + 0x64
LPT_DATA  = ISA_BASE + 0x378
UART      = ISA_BASE + 0x3f8      # tty0, IRQ 4  (bus_isa.c installs it unconditionally)
UART_IER  = UART + 1
UART_MCR  = UART + 4
IER_ETXRDY, MCR_IENABLE = 0x02, 0x08
KBC_SELFTEST = 0xAA

DUMMY = "/tmp/gxo516q_dummy.bin"
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 8)

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
            if not r: continue
            try:
                d = os.read(fd, 65536)
                if not d: return False
                buf += d.decode("latin-1", "replace")
            except OSError:
                return False
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

print("lca_assertassert_probe -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("%-14s %-24s %-24s %-52s %s" % ("row", "got", "want", "note", ""))

setup = ["put d 0x%x, 0x%x" % (SCRATCH +  0, k0(LPT_DATA)),
         "put d 0x%x, 0x%x" % (SCRATCH +  8, KBC_SELFTEST),
         "put d 0x%x, 0x%x" % (SCRATCH + 16, k0(KBC_CMD)),
         "put d 0x%x, 0x%x" % (SCRATCH + 32, k0(UART_IER)),
         "put d 0x%x, 0x%x" % (SCRATCH + 40, k0(UART_MCR))]

prologue = load_const(T7, SCRATCH) + [
    LDQ(T1,  0, T7),          # LPT
    LDQ(T3, 16, T7),          # KBC_CMD
    LDQ(T4, 32, T7),          # UART IER
    LDQ(T5, 40, T7),          # UART MCR
    LDQ(T0,  8, T7),          # 0xAA
    STQ(T0,  0, T1)]          # [A] CONTROL
armed = [STQ(T0, 0, T3)]      # [B] ASSERT #1  (8042 -> IRQ 1)
uart  = [LDA(T6, IER_ETXRDY), STB(T6, 0, T4),
         LDA(T6, MCR_IENABLE), STB(T6, 0, T5)]   # [E] ASSERT #2  (ns16550 -> IRQ 4)

prog = prologue + armed + uart
cmds = setup + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
cmds += ["pc=0x%x" % k0(CODE),
         "step %d" % len(prologue),
         "print t0",
         "step %d" % len(armed),
         "step %d" % len(uart)]
txt, alive = session(cmds)

ANN_A = "ISA interrupt assert not implemented"
ANN_D = "ISA interrupt deassert not implemented"

row("lpt ctl", "yes" if printed(txt, "t0") != "absent" else "died-early", "yes",
    "CONTROL: identical store into a port that cannot assert")
row("kbc live", "yes" if "pckbc: write to CTL" in txt else "no", "yes",
    "DEVICE SIGNATURE: the 8042 announced the command (IRQ 1 leg)")
row("uart live", "yes" if "ns16550" in txt else "no", "yes",
    "DEVICE SIGNATURE: the ns16550 announced its register writes (IRQ 4 leg)")
row("alive", "alive" if alive else "dead", "alive",
    "no host death on either leg")
row("assert once", txt.count(ANN_A), 1,
    "THE ROW UNDER TEST: two ASSERT EDGES, no deassert between -- the latch must hold")
row("deassert once", txt.count(ANN_D), 0,
    "control: this session drives NO deassert edge at all")

for _l in txt.split(chr(10)):
    if ("lca_interrupt" in _l or "lca: ISA interrupt" in _l or "LCAEDGE" in _l
            or "pckbc: write to CTL" in _l or "ns16550" in _l):
        print("  EVIDENCE: %s" % _l.strip())

ok = sum(1 for _, o in rows if o)
print("AA_RESULT=%d/%d" % (ok, len(rows)))
print("AA_DONE")
