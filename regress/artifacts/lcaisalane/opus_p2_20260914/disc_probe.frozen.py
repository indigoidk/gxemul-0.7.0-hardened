#!/usr/bin/env python3
#
#  disc_probe.py -- #530 pass-2 measuring seat (Opus 5), 2026-09-14.  NOT A SHIPPED ROW; a NON-EQUIVALENCE check.
#
#  QUESTION: the #530 contract DISCLOSES the len 3 / 5-7 heads "that memory_rw's 1 KB split produces for a
#  TRANSLATED unaligned LDL/LDQ (this probe runs on K0SEG, untranslated)".  But MEMORY_RW's split loop is
#  keyed on `!(misc_flags & PHYSICAL) && cpu->translate_v2p != NULL' -- NOT on whether the address is a
#  mapped one -- and Alpha always has alpha_translate_v2p, and LS_GENERIC_N passes CACHE_DATA only (no
#  PHYSICAL) and never checks alignment.  So an unaligned LDQ/LDL/STQ on K0SEG that crosses a 1 KB
#  boundary should reach lca_isa as a len-3/5/6/7 head.  1 KB = 32 sparse ports, so the head's port is
#  31 mod 32 -- and 0x3ff (the UART scratch register) is 31 mod 32.  This probe asks whether that is so.
#
#  Machine, invocation, encoder and session plumbing are copied from regress/lca_isalane_probe.py.
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"

ZERO, T0, T1, T2, T3, T4, T5, T6 = 31, 1, 2, 3, 4, 5, 6, 7
def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDBU(ra, disp, rb):      return mem(0x0a, ra, rb, disp)
def LDL (ra, disp, rb):      return mem(0x28, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)
def STL (ra, disp, rb):      return mem(0x2c, ra, rb, disp)
def load_const(reg, val):
    lo = val & 0xffff; hi = (val >> 16) & 0xffff
    if lo >= 0x8000: hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo: ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops
SENT = 0x0bad1d8a
def sent(reg): return load_const(reg, SENT)

K0SEG = 0xfffffc0000000000
def k0(p): return K0SEG | p
LCA_PCI_SIO  = 0x1c0000000
LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000
def SP(port):   return LCA_PCI_SIO  + (port << 5)
def FLAT(port): return LCA_ISA_BASE + port
UART_SCR = 0x3ff
SCRATCH = 0x01020000
CODE    = 0x01040000

DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f: f.write(b"\0" * 8)

def session(cmds, settle, spin):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64", "0x20000000:" + DUMMY])
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
        if not rd(spin if i == len(cmds) - 1 else 0.45): alive = False; break
    try: os.write(fd, b"quit\n"); rd(0.5)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    return buf.replace("\r", ""), alive

def build(consts, phases):
    prog = load_const(T0, SCRATCH); lens = [len(prog)]
    for ops, _ in phases: prog += ops; lens.append(len(ops))
    cmds  = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    cmds += ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for (ops, pr), n in zip(phases, lens[1:]):
        cmds.append("step %d" % n)
        if pr is not None: cmds.append("print %s" % pr)
    return cmds

def prints_in_order(txt):
    return [int(v, 16) for _, v in re.findall(r"print\s+(t\d)\s*\n\s*(0x[0-9a-f]+)", txt)]
def hx(v): return "absent" if v is None else "0x%x" % v

#  PURPOSE: each pass-2 mutant scored 37/37 on the shipped probe is only a detector gap if it CHANGES A GUEST-
#  OBSERVABLE OUTCOME.  One session, cells kill table 1 never rowed: len-4 and len-8 STORES (the canonical
#  real-OS `stl' outb), a wide access to a 0-mod-4 port (MCR 0x3fc), a full-register len-4 read, a len-8 read at
#  lane 3, and a port above 0x3ff.  No cell here ends the host on the fix or on any pass-2 mutant.
UART_MCR, UART_LSR = 0x3fc, 0x3fd
#  slots: 0 FLAT(SCR) 1 SP(SCR) 2 FLAT(MCR) 3 SP(MCR) 4 SP(LSR) 5 FLAT(LSR) 6 SP(0x7ff)
C = [k0(FLAT(UART_SCR)), k0(SP(UART_SCR)), k0(FLAT(UART_MCR)), k0(SP(UART_MCR)), k0(SP(UART_LSR)),
     k0(FLAT(UART_LSR)), k0(SP(0x7ff))]
P = [(load_const(T3, 0x11) + [LDQ(T1, 0, T0), STB(T3, 0, T1)] + load_const(T3, 0x7e000000)
      + [LDQ(T1, 8, T0), STL(T3, 0, T1), LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),   # scr_l  (4,3) W
     (load_const(T3, 0x6d000000) + [LDQ(T1, 8, T0), STQ(T3, 0, T1), LDQ(T1, 0, T0)]
      + sent(T4) + [LDBU(T4, 0, T1)], "t4"),                                                    # scr_q  (8,3) W
     (load_const(T3, 0x01) + [LDQ(T1, 16, T0), STB(T3, 0, T1)] + load_const(T3, 0x03)
      + [LDQ(T1, 24, T0), STL(T3, 0, T1), LDQ(T1, 16, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"), # mcr_l  (4,0) W
     ([LDQ(T1, 24, T0)] + sent(T6) + [LDL(T6, 0, T1)], "t6"),                                    # mcr_rd (4,0) R
     ([LDQ(T1, 32, T0)] + sent(T2) + [LDL(T2, 0, T1)], "t2"),                                    # lsr_l  (4,1) R full
     ([LDQ(T1, 8, T0)] + sent(T3) + [LDQ(T3, 0, T1)], "t3"),                                     # scr_rq (8,3) R
     ([LDQ(T1, 48, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),                                   # p7ff   port > 0x3ff
     ([LDQ(T1, 40, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]                                   # lsr (flat, reference)
NAMES = ["scr_l", "scr_q", "mcr_l", "mcr_rd", "lsr_l", "scr_rq", "p7ff", "lsr"]

print("disc_probe -- binary=%s label=%s" % (BIN, LABEL))
cmds = build(C, P)
txt, alive = session(cmds, 3.0, 4.0)
if len(prints_in_order(txt)) < len(NAMES) and alive:
    txt, alive = session(cmds, 9.0, 12.0)
vals = prints_in_order(txt)
got = {n: (vals[i] if i < len(vals) else None) for i, n in enumerate(NAMES)}
print("alive=%s" % alive)
for n in NAMES:
    print("  %-6s %s" % (n, hx(got[n])))
for l in txt.split("\n"):
    if "lca_isa" in l or "non-existant" in l or "aborting" in l:
        print("  EVIDENCE: " + l.strip())
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "disc_raw_%s.txt" % LABEL), "w",
          encoding="utf-8") as f:
    f.write("### cmds\n" + "\n".join(cmds) + "\n### transcript\n" + txt)
print("DISC_PROBE_DONE")
