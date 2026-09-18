#!/usr/bin/env python3
# disc530c5.py <gxemul-binary> <label>  -- #530 closing pass 5 (Opus): guest-visible discriminators.
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
print("disc530c5 binary=%s label=%s" % (BIN, LABEL))
def f3(v): return None if v is None else v & 3
def dib(v): return None if v is None else v & 1
KCMD, KDAT = 0x64, 0x60


def flat_status(reg): return [LDQ(T1, 0, T0)] + sent(reg) + [LDBU(reg, 0, T1)]       # slot 0 = FLAT(0x64)
def flat_pop(reg):    return [LDQ(T1, 8, T0)] + sent(reg) + [LDBU(reg, 0, T1)]       # slot 8 = FLAT(0x60)

# Z. RD2 GATED ON A ZERO FETCHED BYTE.  0xab (the 8042 keyboard-INTERFACE self-test, reply 0x00) then 0xaa (reply
#    0x55) queue [0x00, 0x55].  One lca load of SP(0x60): base delivers 0x00 and leaves 0x55 (DIB 1); RD2z delivers the
#    SECOND read, 0x55, and leaves nothing (DIB 0).
for nm, ld in (("LDBU (1,0)", LDBU), ("LDL (4,0)", LDL), ("LDQ (8,0)", LDQ)):
    C = [k0(FLAT(KCMD)), k0(FLAT(KDAT)), 0xab, 0xaa, k0(SP(KDAT))]
    P = [([LDQ(T1, 0, T0), LDQ(T2, 16, T0), STB(T2, 0, T1), LDQ(T2, 24, T0), STB(T2, 0, T1),
           LDQ(T1, 32, T0)] + sent(T3) + [ld(T3, 0, T1)], "t3"),
         (flat_status(T4), "t4"), (flat_pop(T5), "t5"), (flat_status(T6), "t6")]
    a, g = run(C, P, ["rd", "s1", "d1", "s2"])
    print("  Z RD2z   alive=%s %s: delivered=%s DIB=%s next pop=%s DIB=%s   (base 0x0/1/0x55/0; RD2z 0x55/0/..../0)"
          % (a, nm, hx(g["rd"]), hx(dib(g["s1"])), hx(g["d1"]), hx(dib(g["s2"]))))

# W. A KEYBOARD COMMAND sent through a store: 0xf4 (KBC_ENABLE, one ACK 0xfa) written to the 8042 DATA port 0x60 in the
#    NORMAL state -- as a direct STB (the (1,0) cell) and as the TAIL of an unaligned STQ at SP(0x5f) + off (tail 7/6/5/3).
#    Then flat status, flat pop, flat status.  base: DIB 1, 0xfa, DIB 0 (one ACK).  A DOUBLED store: DIB 1, 0xfa, DIB 1
#    (two ACKs).  A phantom READ after the store: DIB 0 (the ACK popped by the model, never seen by the guest).
for nm, addr, st, val in (("STB direct (1,0)", SP(KDAT), STB, 0xf4),
                          ("STQ tail7 (h1)", SP(0x5f) + 0x1f, STQ, 0xf4 << 8),
                          ("STQ tail6 (h2)", SP(0x5f) + 0x1e, STQ, 0xf4 << 16),
                          ("STQ tail5 (h3)", SP(0x5f) + 0x1d, STQ, 0xf4 << 24),
                          ("STQ tail3 (h5)", SP(0x5f) + 0x1b, STQ, 0xf4 << 40)):
    C = [k0(FLAT(KCMD)), k0(FLAT(KDAT)), k0(addr), val]
    P = [([LDQ(T1, 16, T0), LDQ(T3, 24, T0), st(T3, 0, T1)] + flat_status(T4), "t4"),
         (flat_pop(T5), "t5"), (flat_status(T6), "t6")]
    a, g = run(C, P, ["s1", "d1", "s2"])
    print("  W kbcmd  alive=%s %s: DIB=%s pop=%s DIB=%s   (base 1/0xfa/0; doubled store 1/0xfa/1; phantom read 0/..../0)"
          % (a, nm, hx(dib(g["s1"])), hx(g["d1"]), hx(dib(g["s2"]))))
print("DISC530C5_DONE")
