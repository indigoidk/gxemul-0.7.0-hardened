#!/usr/bin/env python3
# disc530c4.py <gxemul-binary> <label>  -- guest-visible discriminators for the c4 escapes and the panel cells.
# Helpers copied verbatim from regress/lca_isalane_probe.py (encoders, session, build).
import os, sys, pty, select, time, re
BIN = sys.argv[1]; LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH = "alphabook1"
ZERO, T0, T1, T2, T3, T4, T5, T6 = 31, 1, 2, 3, 4, 5, 6, 7
def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, d, rb=ZERO): return mem(0x08, ra, rb, d)
def LDAH(ra, d, rb=ZERO): return mem(0x09, ra, rb, d)
def LDBU(ra, d, rb):      return mem(0x0a, ra, rb, d)
def LDL (ra, d, rb):      return mem(0x28, ra, rb, d)
def LDQ (ra, d, rb):      return mem(0x29, ra, rb, d)
def STB (ra, d, rb):      return mem(0x0e, ra, rb, d)
def LDWU(ra, d, rb):      return mem(0x0c, ra, rb, d)
def STW (ra, d, rb):      return mem(0x0d, ra, rb, d)
def STL (ra, d, rb):      return mem(0x2c, ra, rb, d)
def STQ (ra, d, rb):      return mem(0x2d, ra, rb, d)
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
LCA_PCI_SIO = 0x1c0000000
LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000
def SP(port): return LCA_PCI_SIO + (port << 5)
def FLAT(port): return LCA_ISA_BASE + port
SCRATCH = 0x01020000; CODE = 0x01040000
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 8)
def session(cmds, settle, spin):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64", "0x20000000:" + DUMMY]); os._exit(127)
    buf = ""
    def rd(t):
        nonlocal buf; end = time.time() + t
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
        if not rd(spin if i == len(cmds) - 1 else 0.45): alive = False; break
    try: os.write(fd, b"quit\n"); rd(0.5)
    except OSError: pass
    try: os.close(fd)
    except OSError: pass
    return buf.replace("\r", ""), alive
def build(consts, phases):
    prog = load_const(T0, SCRATCH); lens = [len(prog)]
    for ops, _ in phases:
        prog += ops; lens.append(len(ops))
    cmds  = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    cmds += ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for (ops, pr), n in zip(phases, lens[1:]):
        cmds.append("step %d" % n)
        if pr is not None: cmds.append("print %s" % pr)
    return cmds
def prints_in_order(txt):
    return [int(v, 16) for _, v in re.findall(r"print\s+(t\d)\s*\n\s*(0x[0-9a-f]+)", txt)]
def run(consts, phases, names, settle=3.0, spin=4.0):
    cmds = build(consts, phases)
    txt, alive = session(cmds, settle, spin)
    vals = prints_in_order(txt)
    got = {n: (vals[i] if i < len(vals) else None) for i, n in enumerate(names)}
    return alive, got
def hx(v): return "absent" if v is None else "0x%x" % v

UART_IER, UART_IIR = 0x3f9, 0x3fa
# arm TXRDY: IER=0 then IER=ETXRDY(0x02) sets IIR_TXRDY
def iir_arm(): return load_const(T3, 0x02) + [LDQ(T1, 0, T0), STB(ZERO, 0, T1), STB(T3, 0, T1)]
print("disc530c4 binary=%s label=%s" % (BIN, LABEL))
def f3(v): return None if v is None else v & 3
def dib(v): return None if v is None else v & 1
KCMD, KDAT = 0x64, 0x60

# A. dataA: a NONZERO store to FCR (0x3fa, lane 2) with TXRDY armed; flat IIR & 3 after.
C = [k0(FLAT(UART_IER)), k0(FLAT(UART_IIR)), k0(SP(UART_IIR))]
P = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),
     (iir_arm() + load_const(T3, 0x06) + [LDQ(T1, 16, T0), STB(T3, 0, T1), LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),
     (iir_arm() + load_const(T3, 0x00060000) + [LDQ(T1, 16, T0), STL(T3, 0, T1), LDQ(T1, 8, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]
a, g = run(C, P, ["ctl", "stb6", "stl6"])
print("  A dataA  alive=%s ctl=%s  STB 0x06->FCR: IIR&3=%s  STL 0x60000->FCR: IIR&3=%s   (base 0x2/0x2/0x2; dataA 0x1 after a nonzero store)"
      % (a, hx(f3(g["ctl"])), hx(f3(g["stb6"])), hx(f3(g["stl6"]))))

# B. R2w: an lca READ of IIR at len 2 / 4 / 8 after arming; the delivered lane & 3.
for nm, ld, sh in (("LDWU", LDWU, 0), ("LDL", LDL, 16), ("LDQ", LDQ, 16)):
    C = [k0(FLAT(UART_IER)), k0(SP(UART_IIR))]
    P = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T4) + [ld(T4, 0, T1)], "t4")]
    a, g = run(C, P, ["rd"])
    v = g["rd"]
    print("  B R2w    alive=%s %s SP(0x3fa) raw=%s lane&3=%s   (base 0x2; RD2-at-this-width 0x1)"
          % (a, nm, hx(v), hx(None if v is None else (v >> sh) & 3)))

# C. WT: 8042 reply queued, 0xd1, then an unaligned STQ whose TAIL lands on 0x60; flat status DIB.
for off, h in ((0x1e, 2), (0x1d, 3), (0x1b, 5), (0x1f, 1)):
    C = [k0(FLAT(KCMD)), 0xAA, 0xd1, k0(SP(0x5f) + off)]
    P = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1), LDQ(T2, 16, T0), STB(T2, 0, T1)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),
         ([LDQ(T1, 24, T0), STQ(ZERO, 0, T1), LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]
    a, g = run(C, P, ["pre", "post"])
    print("  C WT     alive=%s head %d / TAIL %d at 0x60: DIB pre=%s post=%s   (base 1/1; fallthrough at tail len %d: post 0)"
          % (a, h, 8 - h, hx(dib(g["pre"])), hx(dib(g["post"])), 8 - h))

# D. RD2 at LANE 0: TWO self-test replies queued, one lca READ of 0x60, then flat status DIB.
for nm, addr, ld in (("LDBU (1,0)", SP(KDAT), LDBU), ("LDQ (8,0)", SP(KDAT), LDQ), ("LDQ tail6", SP(0x5f) + 0x1e, LDQ)):
    C = [k0(FLAT(KCMD)), 0xAA, k0(addr)]
    P = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1), STB(T2, 0, T1), LDQ(T1, 16, T0)] + sent(T3) + [ld(T3, 0, T1)], "t3"),
         ([LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]
    a, g = run(C, P, ["rd", "st"])
    print("  D RD2L0  alive=%s %s: value=%s DIB after=%s   (base: one reply left, DIB 1; a duplicated read pops both, DIB 0)"
          % (a, nm, hx(g["rd"]), hx(dib(g["st"]))))

# E. the 8042 PC-style stub at 0x61-0x6f: `static int x; x++' toggles bit 0x10 on EVERY access.
#    flat read a, ONE lca access, flat read b: base a == b in bit 4 (three accesses); an extra access flips it.
for port in (0x61, 0x63, 0x62, 0x68):
    C = [k0(FLAT(port)), k0(SP(port))]
    P = [([LDQ(T1, 0, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),
         ([LDQ(T1, 8, T0), STB(ZERO, 0, T1), LDQ(T1, 0, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),
         ([LDQ(T1, 8, T0)] + sent(T4) + [LDL(T4, 0, T1), LDQ(T1, 0, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),
         ([LDQ(T1, 0, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6")]
    a, g = run(C, P, ["a", "b_st", "b_ld", "ctl"])
    x = lambda p, q: None if (p is None or q is None) else (p ^ q) & 0x10
    print("  E tog%02x  alive=%s a=%s after-STB=%s after-LDL=%s next=%s | flips: store=%s load=%s ctl=%s   (base 0x0/0x0/0x10; one extra access per lca op: 0x10)"
          % (port, a, hx(g["a"]), hx(g["b_st"]), hx(g["b_ld"]), hx(g["ctl"]),
             hx(x(g["a"], g["b_st"])), hx(x(g["b_st"], g["b_ld"])), hx(x(g["b_ld"], g["ctl"]))))

# F. 8253 counter 1 (0x41, lane 1): control word 0x74 (ctr 1, LSB+MSB, mode 2), lca STB 0x34 -> SP(0x41),
#    then two flat reads: base LSB then MSB (0x34, 0x00); a phantom read after the store swaps them.
C = [k0(FLAT(0x43)), 0x74, k0(SP(0x41)), k0(FLAT(0x41))]
P = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)] + load_const(T3, 0x34) + [LDQ(T1, 16, T0), STB(T3, 0, T1),
      LDQ(T1, 24, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),
     ([LDQ(T1, 24, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]
a, g = run(C, P, ["r1", "r2"])
print("  F pit41  alive=%s read1=%s read2=%s   (base 0x34/0x0; phantom read after the lane-1 store: 0x0/0x34)"
      % (a, hx(g["r1"]), hx(g["r2"])))

# G. CMOS (0x71, lane 1): select REG C via flat 0x70, lca STB 0x40 -> SP(0x71) writes REG C, flat read 0x71.
C = [k0(FLAT(0x70)), 0x0c, k0(SP(0x71)), k0(FLAT(0x71))]
P = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)] + load_const(T3, 0x40) + [LDQ(T1, 16, T0), STB(T3, 0, T1),
      LDQ(T1, 0, T0), STB(T2, 0, T1), LDQ(T1, 24, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]
a, g = run(C, P, ["regc"])
print("  G cmos71 alive=%s REG C after lca store of 0x40=%s   (base 0x40; a phantom read after the store clears it: 0x0)"
      % (a, hx(g["regc"])))
print("DISC530C4_DONE")
