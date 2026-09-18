#!/usr/bin/env python3
# disc530c3.py <gxemul-binary> <label>  -- guest-visible discriminators for the c3 escapes.
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
print("disc530c3 binary=%s label=%s" % (BIN, LABEL))

# --- W1 discriminator: STQ 0 -> SP(0x3fa) (len 8 store), then flat IIR & 3
C = [k0(FLAT(UART_IER)), k0(FLAT(UART_IIR)), k0(SP(UART_IIR))]
P = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),                                  # ctl: no lca store
     (iir_arm() + [LDQ(T1, 16, T0), STQ(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),  # STQ(8,2)
     (iir_arm() + [LDQ(T1, 16, T0), STW(ZERO, 0, T1), LDQ(T1, 8, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5")]  # STW(2,2)
a, g = run(C, P, ["ctl", "stq8", "stw2"])
f3 = lambda v: None if v is None else v & 3
print("  W1/W2 iir: alive=%s ctl(IIR&3)=%s  STQ8=%s  STW2=%s" % (a, hx(f3(g["ctl"])), hx(f3(g["stq8"])), hx(f3(g["stw2"]))))
print("  EXPECT base: ctl=0x2 STQ8=0x2 STW2=0x2 ;  W1-mutant: STQ8=0x1 ;  W2-mutant: STW2=0x1")

# --- D1 discriminator: STL 0x00000001 -> SP(IER 0x3f9) (lane1 len4 ofs1: data[1]=0, data[0]=1), flat IER readback
C2 = [k0(SP(UART_IER)), k0(FLAT(UART_IER))]
P2 = [(load_const(T3, 0x01) + [LDQ(T1, 0, T0), STL(T3, 0, T1), LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]
a2, g2 = run(C2, P2, ["ier"])
print("  D1 ier: alive=%s  IER(flat)=%s" % (a2, hx(g2["ier"])))
print("  EXPECT base: IER=0x0 (forwards data[1]=0) ;  D1-mutant: IER=0x1 (forwards data[0]=0x01)")

# --- W3/W4 lane-0 discriminator (8042): self-test queues 0x55 (flat), 0xd1 = load-output state (flat), then a
#     lca STB 0 to SP(0x60) (lane 0, len 1) lands in output_byte; a phantom READ of 0x60 would pop the 0x55.
#     Channel: flat status 0x64 & KBS_DIB (0x01), before (ctl) and after the lca store.
KCMD, KDAT = 0x64, 0x60
C3 = [k0(FLAT(KCMD)), 0xAA, 0xd1, k0(SP(KDAT))]
P3 = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1), LDQ(T2, 16, T0), STB(T2, 0, T1)]
       + sent(T3) + [LDBU(T3, 0, T1)], "t3"),                                                   # status before
      ([LDQ(T1, 24, T0), STB(ZERO, 0, T1), LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]  # status after
a3, g3 = run(C3, P3, ["pre", "post"])
f1 = lambda v: None if v is None else v & 1
print("  W3/W4 kbc: alive=%s DIB before=%s after lca STB->SP(0x60)=%s" % (a3, hx(f1(g3["pre"])), hx(f1(g3["post"]))))
print("  EXPECT base: 0x1 / 0x1 ;  W3/W4-mutant (len-1 lane-0 fallthrough; W3 only): after=0x0")
# the same with an STW (len 2, lane 0) -- W4's width
P3b = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1), LDQ(T2, 16, T0), STB(T2, 0, T1)]
        + [LDQ(T1, 24, T0), STW(ZERO, 0, T1), LDQ(T1, 0, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]
a3b, g3b = run(C3, P3b, ["post"])
print("  W3/W4 kbc STW: alive=%s DIB after lca STW->SP(0x60)=%s   (base 0x1; W3 and W4 0x0)" % (a3b, hx(f1(g3b["post"]))))

# --- RD2 discriminator: arm TXRDY, then READ IIR THROUGH lca (LDBU SP(0x3fa), lane 2 len 1)
C4 = [k0(FLAT(UART_IER)), k0(SP(UART_IIR))]
P4 = [(iir_arm() + [LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4")]
a4, g4 = run(C4, P4, ["iir"])
print("  RD2 iir-read: alive=%s LDBU SP(0x3fa) & 3 = %s   (base 0x2 TXRDY; RD2 0x1: the first forward acked it)"
      % (a4, hx(f3(g4["iir"]))))

# --- H1b discriminator: LDQ at SP(0x3ff)+0x1c = a 4-byte split HEAD at port 0x3ff (lane 3, sparse low bits 0x1c)
UART_SCR = 0x3ff
C5 = [k0(FLAT(UART_SCR)), 0x5a, k0(SP(UART_SCR) + 0x1c), k0(SP(UART_SCR))]
P5 = [([LDQ(T1, 0, T0), LDQ(T2, 8, T0), STB(T2, 0, T1), LDQ(T1, 16, T0)] + sent(T4) + [LDQ(T4, 0, T1)], "t4"),
      ([LDQ(T1, 24, T0)] + sent(T5) + [LDL(T5, 0, T1)], "t5"),                                   # direct (4,3) ctl
      (load_const(T3, 0x7e000000) + [LDQ(T1, 16, T0), STQ(T3, 0, T1), LDQ(T1, 0, T0)]
       + sent(T6) + [LDBU(T6, 0, T1)], "t6")]                                                     # STQ h4 head
a5, g5 = run(C5, P5, ["h4r", "d43", "h4w"])
print("  H1b: alive=%s LDQ h4 head=%s  direct LDL (4,3)=%s  STQ h4 head -> SCR=%s"
      % (a5, hx(g5["h4r"]), hx(g5["d43"]), hx(g5["h4w"])))
print("  EXPECT base: 0x5a000000 / 0x5a000000 / 0x7e ;  H1b: 0x5a / 0x5a000000 / 0x0 (position 0 of 0x7e000000)")
print("DISC530C3_DONE")
