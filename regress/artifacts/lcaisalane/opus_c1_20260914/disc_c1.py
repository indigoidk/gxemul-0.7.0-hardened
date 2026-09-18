#!/usr/bin/env python3
#  disc_c1.py <gxemul-binary> [label] -- discriminator for the #530 closing-pass-1 mutants.
#  Prints three guest-visible values, each a cell the 51-row detector does NOT observe:
#     d_msr : (4,2) STL 0x11223344 -> SP(MSR), read back through FLAT(MSR).  fix -> data[2]=0x22 (|0xb0=0xb2);
#             c1_w2 -> data[0]=0x44 (|0xb0=0xf4).
#     d_ier : (4,1) STL 0x11223344 -> SP(IER), read back through FLAT(IER).  fix -> data[1]=0x33;
#             c1_w1w -> data[0]=0x44.
#     d_scr : (4,3) LDL SP(SCR) FULL register after a flat store of 0x5a.  fix -> 0x5a000000;
#             c1_r4 (len==4 && ofs>=2 also fills lane 0) -> 0x5a00005a.
import os, sys, pty, select, time, re
BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"
ZERO, T0, T1, T2, T3, T4, T5, T6 = 31, 1, 2, 3, 4, 5, 6, 7
def mem(op, ra, rb, disp): return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDBU(ra, disp, rb):      return mem(0x0a, ra, rb, disp)
def LDL (ra, disp, rb):      return mem(0x28, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)
def STL (ra, disp, rb):      return mem(0x2c, ra, rb, disp)
def load_const(reg, val):
    lo = val & 0xffff; hi = (val >> 16) & 0xffff
    if lo >= 0x8000: hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo: ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops
K0SEG = 0xfffffc0000000000
def k0(p): return K0SEG | p
LCA_PCI_SIO  = 0x1c0000000
LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000
def SP(port):   return LCA_PCI_SIO  + (port << 5)
def FLAT(port): return LCA_ISA_BASE + port
UART_IER, UART_MSR, UART_SCR = 0x3f9, 0x3fe, 0x3ff
SCRATCH, CODE = 0x01020000, 0x01040000
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 8)
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
def hx(v): return "absent" if v is None else "0x%x" % v

VAL = 0x11223344
#  slots: 0 SP(MSR) 1 FLAT(MSR) 2 SP(IER) 3 FLAT(IER) 4 FLAT(SCR) 5 0x5a 6 SP(SCR)
C = [k0(SP(UART_MSR)), k0(FLAT(UART_MSR)), k0(SP(UART_IER)), k0(FLAT(UART_IER)),
     k0(FLAT(UART_SCR)), 0x5a, k0(SP(UART_SCR))]
P = [(load_const(T3, VAL) + [LDQ(T1, 0, T0), STL(T3, 0, T1), LDQ(T1, 8, T0), LDBU(T2, 0, T1)], "t2"),   # d_msr
     (load_const(T3, VAL) + [LDQ(T1, 16, T0), STL(T3, 0, T1), LDQ(T1, 24, T0), LDBU(T4, 0, T1)], "t4"), # d_ier
     ([LDQ(T1, 32, T0), LDQ(T2, 40, T0), STB(T2, 0, T1), LDQ(T1, 48, T0), LDL(T5, 0, T1)], "t5")]        # d_scr
cmds = build(C, P)
txt, alive = session(cmds, 3.0, 4.0)
vals = prints_in_order(txt)
names = ["d_msr", "d_ier", "d_scr"]
got = {n: (vals[i] if i < len(vals) else None) for i, n in enumerate(names)}
print("DISC %s alive=%s  d_msr=%s d_ier=%s d_scr=%s"
      % (LABEL, alive, hx(got["d_msr"]), hx(got["d_ier"]), hx(got["d_scr"])))
print("DISC_DONE")
