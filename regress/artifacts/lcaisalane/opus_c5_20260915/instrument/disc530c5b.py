#!/usr/bin/env python3
# disc530c5b.py <gxemul-binary> <label>  -- #530 closing pass 5 (Opus): the 8253 access-count channel + stub zero stores.
# Lines below down to KCMD are copied VERBATIM from ../../opus_c4_20260914/instrument/disc530c4.frozen.py,
# whose helpers are in turn verbatim from regress/lca_isalane_probe.py.
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
print("disc530c5b binary=%s label=%s" % (BIN, LABEL))
def f3(v): return None if v is None else v & 3
def dib(v): return None if v is None else v & 1
KCMD, KDAT = 0x64, 0x60


# ---- P: THE 8253 COUNTER FLIP-FLOPS (dev_8253.c #440: rd_msb / wr_msb, ONE PER COUNTER, toggled on EVERY counter access
#      while the control word selects LSB+MSB).  Counter N at ISA 0x40+N is lane N; 0x40 is also a TAIL port (0 mod 0x20).
#      live : CW, flat LSB 0x34, flat MSB 0x12, flat read, flat read       -> 0x34 then 0x12 (the flip-flop alternates)
#      PS X : CW, ONE lca store of X, flat store 0x12, flat read r1, r2      -> base X / 0x12.  An EXTRA access of either
#             direction after the lca store (a phantom read, or a doubled store) makes it 0x12 / X.
#      PL L : CW, flat L, flat 0x12, ONE lca load, flat read r1             -> base delivered L, r1 0x12.  A duplicated
#             read makes r1 == L (whatever byte it delivers); delivering the second read makes it deliver 0x12.
PIT_CW = 0x43
def cw(): return [LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1)]                       # slots 0 FLAT(0x43), 1 CW
def fl_st(slot): return [LDQ(T1, 16, T0), LDQ(T2, 8 * slot, T0), STB(T2, 0, T1)]       # slot 2 = FLAT(counter)
def fl_st0():    return [LDQ(T1, 16, T0), STB(ZERO, 0, T1)]
def fl_rd(reg):  return [LDQ(T1, 16, T0)] + sent(reg) + [LDBU(reg, 0, T1)]
def b(v, sh): return None if v is None else (v >> sh) & 0xff

for N in (0, 1, 2):
    port = 0x40 + N
    CWV = 0x34 | (N << 6)
    #       0            1    2            3          4     5     6
    C = [k0(FLAT(PIT_CW)), CWV, k0(FLAT(port)), k0(SP(port)), 0x34, 0x12, 0x5a]
    P = [(cw() + fl_st(4) + fl_st(5) + fl_rd(T3), "t3"), (fl_rd(T4), "t4")]
    names = ["live1", "live2"]
    for X in (0x5a, 0x00):
        st = ([LDQ(T1, 24, T0), LDQ(T3, 48, T0), STB(T3, 0, T1)] if X else [LDQ(T1, 24, T0), STB(ZERO, 0, T1)])
        P += [(cw() + st + fl_st(5) + fl_rd(T3), "t3"), (fl_rd(T4), "t4")]
        names += ["ps%02x_r1" % X, "ps%02x_r2" % X]
    for Lv in (0x5a, 0x00):
        P += [(cw() + (fl_st(6) if Lv else fl_st0()) + fl_st(5) + [LDQ(T1, 24, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),
              (fl_rd(T4), "t4")]
        names += ["pl%02x_dlv" % Lv, "pl%02x_r1" % Lv]
    a, g = run(C, P, names)
    print("  P pit%x lane %d alive=%s live=%s/%s (want 0x34/0x12) | STB 0x5a: %s/%s  STB 0x00: %s/%s (base X/0x12; extra access 0x12/X)"
          " | LDBU L=0x5a: dlv=%s r1=%s  L=0x00: dlv=%s r1=%s (base L/0x12; dup read r1=L; dup delivered dlv=0x12)"
          % (port, N, a, hx(g["live1"]), hx(g["live2"]), hx(g["ps5a_r1"]), hx(g["ps5a_r2"]), hx(g["ps00_r1"]), hx(g["ps00_r2"]),
             hx(g["pl5a_dlv"]), hx(g["pl5a_r1"]), hx(g["pl00_dlv"]), hx(g["pl00_r1"])))

# ---- PT: the same channel at the TAIL port 0x40 (counter 0): unaligned STQ / LDQ at SP(0x3f) + 0x1e (head 2 at the unmapped
#      0x3f, TAIL 6 at 0x40) and + 0x1b (head 5, TAIL 3).  The tail's position 0 is register byte h.
#       0            1     2             3                    4                    5     6            7            8
C = [k0(FLAT(PIT_CW)), 0x34, k0(FLAT(0x40)), k0(SP(0x3f) + 0x1e), k0(SP(0x3f) + 0x1b), 0x12, 0x5a << 16, 0x5a << 40, 0x5a]
P = []; names = []
for tag, aslot, vslot in (("t6x5a", 3, 6), ("t6x00", 3, None), ("t3x5a", 4, 7)):
    st = [LDQ(T1, 8 * aslot, T0)] + ([LDQ(T3, 8 * vslot, T0), STQ(T3, 0, T1)] if vslot else [STQ(ZERO, 0, T1)])
    P += [(cw() + st + fl_st(5) + fl_rd(T3), "t3"), (fl_rd(T4), "t4")]
    names += [tag + "_r1", tag + "_r2"]
for tag, aslot, Lv in (("l6x5a", 3, 0x5a), ("l6x00", 3, 0), ("l3x5a", 4, 0x5a)):
    P += [(cw() + (fl_st(8) if Lv else fl_st0()) + fl_st(5) + [LDQ(T1, 8 * aslot, T0)] + sent(T3) + [LDQ(T3, 0, T1)], "t3"),
          (fl_rd(T4), "t4")]
    names += [tag + "_dlv", tag + "_r1"]
a, g = run(C, P, names)
print("  PT pit40 tails alive=%s | STQ tail6 X=0x5a: %s/%s  X=0: %s/%s  STQ tail3 X=0x5a: %s/%s (base X/0x12; extra access 0x12/X)"
      % (a, hx(g["t6x5a_r1"]), hx(g["t6x5a_r2"]), hx(g["t6x00_r1"]), hx(g["t6x00_r2"]), hx(g["t3x5a_r1"]), hx(g["t3x5a_r2"])))
print("  PT pit40 tails | LDQ tail6 L=0x5a: dlv=%s r1=%s  L=0: dlv=%s r1=%s  LDQ tail3 L=0x5a: dlv=%s r1=%s (base L/0x12)"
      % (hx(b(g["l6x5a_dlv"], 16)), hx(g["l6x5a_r1"]), hx(b(g["l6x00_dlv"], 16)), hx(g["l6x00_r1"]),
         hx(b(g["l3x5a_dlv"], 40)), hx(g["l3x5a_r1"])))

# ---- EZ: the 8042 PC-style stub with a ZERO store and a NONZERO store (codex's lane x data joint), at 0x63 and 0x61.
for port in (0x63, 0x61):
    C = [k0(FLAT(port)), k0(SP(port)), 0x5a]
    fr = lambda reg: [LDQ(T1, 0, T0)] + sent(reg) + [LDBU(reg, 0, T1)]
    P = [(fr(T2), "t2"),
         ([LDQ(T1, 8, T0), STB(ZERO, 0, T1)] + fr(T3), "t3"),
         ([LDQ(T1, 8, T0), LDQ(T4, 16, T0), STB(T4, 0, T1)] + fr(T5), "t5"),
         (fr(T6), "t6")]
    a, g = run(C, P, ["a", "z", "n", "c"])
    x = lambda p, q: None if (p is None or q is None) else (p ^ q) & 0x10
    print("  EZ stub%02x alive=%s flips: zero-store=%s nonzero-store=%s ctl=%s   (base 0x0/0x0/0x10; cdxZL3 at 0x63: 0x10/0x0/0x10)"
          % (port, a, hx(x(g["a"], g["z"])), hx(x(g["z"], g["n"])), hx(x(g["n"], g["c"]))))
print("DISC530C5B_DONE")
