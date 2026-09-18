#!/usr/bin/env python3
#
#  split_probe.py -- #530 pass-2 measuring seat (Opus 5), 2026-09-14.  NOT A SHIPPED ROW; a measurement.
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

#  slots: 0 FLAT(SCR) 1 0x5a 2 SP(SCR)+0x1d (h3) 3 +0x1b (h5) 4 +0x1a (h6) 5 +0x19 (h7) 6 SP(SCR) 7 FLAT(0x400)
C = [k0(FLAT(UART_SCR)), 0x5a, k0(SP(UART_SCR) + 0x1d), k0(SP(UART_SCR) + 0x1b), k0(SP(UART_SCR) + 0x1a),
     k0(SP(UART_SCR) + 0x19), k0(SP(UART_SCR)), k0(FLAT(0x400))]
P = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),   # scr (flat)
     ([LDQ(T1, 16, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"),                                  # q_h3
     ([LDQ(T1, 24, T0)] + sent(T5) + [LDQ(T5, 0, T1)], "t5"),                                  # q_h5
     ([LDQ(T1, 32, T0)] + sent(T6) + [LDQ(T6, 0, T1)], "t6"),                                  # q_h6
     ([LDQ(T1, 40, T0)] + sent(T2) + [LDQ(T2, 0, T1)], "t2"),                                  # q_h7
     ([LDQ(T1, 16, T0)] + sent(T3) + [LDL(T3, 0, T1)], "t3"),                                  # l_h3
     ([LDQ(T1, 48, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"),                                  # q_al (aligned control)
     ([LDQ(T1, 56, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),                                 # p400 (what the tail reads)
     (load_const(T3, 0x7e000000) + [LDQ(T1, 24, T0), STQ(T3, 0, T1), LDQ(T1, 0, T0)]
      + sent(T6) + [LDBU(T6, 0, T1)], "t6"),                                                   # w_h5 -> flat SCR
     (load_const(T3, 0x00c3007e) + [LDQ(T1, 16, T0), STQ(T3, 0, T1), LDQ(T1, 0, T0)]
      + sent(T2) + [LDBU(T2, 0, T1)], "t2")]                                                   # w_h3 -> flat SCR
NAMES = ["scr", "q_h3", "q_h5", "q_h6", "q_h7", "l_h3", "q_al", "p400", "w_h5", "w_h3"]

print("split_probe -- binary=%s label=%s" % (BIN, LABEL))
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
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "split_raw_%s.txt" % LABEL), "w",
          encoding="utf-8") as f:
    f.write("### cmds\n" + "\n".join(cmds) + "\n### transcript\n" + txt)
print("SPLIT_PROBE_DONE")
