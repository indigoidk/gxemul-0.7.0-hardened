#!/usr/bin/env python3
"""A MEASUREMENT for alphavmkill pass 1's disagreement, and a rung-3 WITNESS attempt for `alphaifetchkill'.
No build: both run on the committed-build binary.

SESSION A -- what member 4 (ACCEPT: drop exit(1), keep the identity mapping) would do, measured at NEIGHBOUR addresses
that the trap does not cover (the Opus seat's proposal).  ptbr == 0, supervisor mode:
  LOAD  from 0xfffffffd80000008 -> dest (member 4 predicts 0: identity -> past RAM -> zero-fill), then a marker
  STORE to   0xfffffffd80000008 -> a marker after it (predicts: dropped, execution continues)
  FETCH at   0xfffffffd80002000 via JMP -> predicts `[ Alpha PALcode 0x0 unimplemented! ]' (the zero-filled word is
        CALL_PAL 0), the CPU stops, the process stays alive under -V, and pc reads the jump target.

SESSION B -- `alphaifetchkill': the lca_isaphys vehicle (swpctx to a PCB whose ptbr names an all-zero L1 page), an
arming control (a raw-VA load now walks and misses, dest keeps the sentinel), then ONE JMP to a raw VA.  Predicts:
`wasn't found' for the jump target, then `FATAL: could not find physical address of the exception handler?', and the
host exits (wait status 256).

The session harness is the #538-pass-2 form: drain to EOF after `quit', reap, and require a clean exit for `alive'.
Usage: vm_neighbour_measure.py <gxemul-binary>
"""
import os, pty, re, select, sys, time

BIN = sys.argv[1]
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

ZERO, T0, T1, T2, T3, T4, T5, T6, T7 = 31, 1, 2, 3, 4, 5, 6, 7, 8
A0, V = 16, 22
def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
def STQ (ra, disp, rb):      return mem(0x2d, ra, rb, disp)
def JMP (rb):                return (0x1a << 26) | (ZERO << 21) | (rb << 16)      # func 0 = JMP, ra = zero
def CALL_PAL(n):             return n & 0x3ffffff
def load_const(reg, val):
    lo, hi = val & 0xffff, (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops
SENT = 0x0bad1d8a
def sent(reg): return load_const(reg, SENT)

K0SEG = 0xfffffc0000000000
def k0(p): return K0SEG | p
VMKILL = 0xfffffffd80000000
SCRATCH, CODE, P_ZERO, P_RAM, P_PCB = 0x01020000, 0x01040000, 0x01050000, 0x01056000, 0x01058000
ZERO_PFN = P_ZERO >> 13
assert ZERO_PFN == 0x828
VAL_A, MARK1, MARK2 = 0xaaaa0000aaaa, 0x1234, 0x5678
HWRPB_V, MAGIC = 0x10000008, int.from_bytes(b"HWRPB\0\0\0", "little")
RAW_TARGET = 0x01044000                        # a raw VA inside RAM; after the arm it walks L1[0], which is zero

def session(cmds, settle=3.0, spin=4.0):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", "alphabook1", "-M", "64", "0x20000000:" + DUMMY])
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
        if not rd(spin if i == len(cmds) - 1 else 0.6):
            alive = False; break
    try:
        os.write(fd, b"quit\n")
    except OSError:
        pass
    end = time.time() + 10.0
    while time.time() < end and rd(0.2):
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    try:
        _, st = os.waitpid(pid, 0)       # blocking: returns because gxemul installs no SIGHUP handler
    except OSError:
        st = None
    clean = st is not None and os.WIFEXITED(st) and os.WEXITSTATUS(st) == 0
    return buf.replace("\r", ""), alive and clean, st

def printed(t, reg):
    m = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return None if not m else int(m[-1], 16)
def hx(v): return "absent" if v is None else "0x%x" % v

# ---------------------------------------------------------------- SESSION A
setupA = ["put d 0x%x, 0x%x" % (k0(SCRATCH), VMKILL + 8),
          "put d 0x%x, 0x%x" % (k0(SCRATCH + 8), VMKILL + 0x2000),
          "put d 0x%x, 0x%x" % (k0(P_RAM), VAL_A)]
p1 = load_const(T1, P_RAM) + sent(T2) + [LDQ(T2, 0, T1)]
p1 += load_const(T1, HWRPB_V) + sent(T3) + [LDQ(T3, 0, T1)]
p2 = load_const(T0, SCRATCH) + [LDQ(T1, 0, T0)] + sent(T4) + [LDQ(T4, 0, T1)] + load_const(T5, MARK1)
p2 += load_const(V, 0x77) + [STQ(V, 0, T1)] + load_const(T6, MARK2)
p3 = [LDQ(T7, 8, T0), JMP(T7)]
progA = p1 + p2 + p3
cmdsA = setupA + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(progA)]
cmdsA += ["pc=0x%x" % k0(CODE), "step %d" % len(p1), "print t2", "print t3",
          "step %d" % len(p2), "print t4", "print t5", "print t6",
          "step %d" % len(p3), "step 3", "print pc"]
txtA, aliveA, stA = session(cmdsA)
print("SESSION A (neighbours, ptbr == 0)")
print("  live=%s sig=%s  load(VMKILL+8)=%s  after-load mark=%s  after-store mark=%s  pc=%s"
      % (hx(printed(txtA, "t2")), hx(printed(txtA, "t3")), hx(printed(txtA, "t4")), hx(printed(txtA, "t5")),
         hx(printed(txtA, "t6")), hx(printed(txtA, "pc"))))
print("  alive(clean exit)=%s wait=%r" % (aliveA, stA))
for pat in ("PALcode 0x0 unimplemented", "All machines stopped", "non-existant", "nonexist", "could not find physical",
            "Alpha kernel virtual memory", "wasn't found"):
    print("  %-34s %d" % (pat, txtA.count(pat)))

# ---------------------------------------------------------------- SESSION B
setupB = ["put d 0x%x, 0x%x" % (k0(SCRATCH), k0(SCRATCH)),
          "put d 0x%x, 0x%x" % (k0(SCRATCH + 16), k0(P_PCB)),
          "put d 0x%x, 0x%x" % (k0(SCRATCH + 24), RAW_TARGET),
          "put d 0x%x, 0x0" % k0(P_ZERO),
          "put d 0x%x, 0x%x" % (k0(P_RAM), VAL_A),
          "put d 0x%x, 0x%x" % (k0(P_PCB + 16), ZERO_PFN),
          "put d 0x%x, 0x%x" % (k0(P_PCB + 40), ZERO_PFN)]
q1 = load_const(T0, SCRATCH) + [LDQ(T0, 0, T0)]                  # T0 = k0(SCRATCH), before the arm
q1 += [LDQ(A0, 16, T0), CALL_PAL(0x30)]                         # ARM
q1 += load_const(T1, P_RAM) + sent(T2) + [LDQ(T2, 0, T1)]        # the arming control: walks and misses
q2 = [LDQ(T1, 24, T0), JMP(T1)]                                 # the fetch at a raw VA
progB = q1 + q2
cmdsB = setupB + ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(progB)]
cmdsB += ["pc=0x%x" % k0(CODE), "step %d" % len(q1), "print t2", "step %d" % len(q2), "step 2", "print pc"]
txtB, aliveB, stB = session(cmdsB)
print("SESSION B (alphaifetchkill: armed, then a JMP to raw 0x%x)" % RAW_TARGET)
print("  arming control t2=%s (want SENT 0x%x)  alive(clean exit)=%s wait=%r" % (hx(printed(txtB, "t2")), SENT, aliveB, stB))
for pat in ("wasn't found", "could not find physical", "FATAL"):
    print("  %-34s %d" % (pat, txtB.count(pat)))
m = re.findall(r"\[ alpha_translate_v2p: (0x[0-9a-f]+) wasn't found \]", txtB)
print("  miss addresses: %s" % sorted(set(m)))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vm_neighbour_A.txt"), "w").write(txtA)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vm_neighbour_B.txt"), "w").write(txtB)
print("VM_NEIGHBOUR_DONE")
