#!/usr/bin/env python3
#  lcaisalane F2 -- Opus measuring seat, 2026-09-13.  A CELL x VARIANT instrument, not a detector.
#
#  It measures, per binary, the guest-visible outcome of the cells the A/B/C dispute turns on:
#  the equality READ and WRITE cells, the three EXIT cells (read and write), and the (2,1)
#  high-byte-forward cell (F8).  Each measurement prints RESULT lines the F2 driver diffs across
#  the four binaries.  Nothing is asserted "ok/FAIL" here: the ANSWER differs per disposition, and
#  the report is the cross-variant table, so this prints raw observations keyed by cell.
#
#  Method mirrors the shipped witness (regress/lca_isalane_probe.py):
#    * one process per cell that can END (an exit cell today, or a decline under a variant that
#      might still exit if mis-built) -- but the write/read equality cells and (2,1) never exit
#      under any of the four, so they share sessions;
#    * every access is a GUEST INSTRUCTION (lca_isa is DM_DEFAULT, so `dump' would skip it);
#    * a read destination is pre-seeded with SENT so a FAULTED/declined load is distinguishable
#      from an ANSWERED zero -- the whole point on the read side;
#    * a WRITE is observed by reading the target port back through the FLAT mapping (a plain
#      forward, not lane-decoded), so the readback is independent of the handler under test.
#
#  Ports (all on alphabook1's bus_isa_init):
#    UART IER 0x3f9  (1 mod 4, ofs 1)  writable+readable (d->reg[com_ier]); dlab=0 at reset
#    UART LSR 0x3fd  (1 mod 4, ofs 1)  read-only, TXRDY|TSRE=0x60 forced every access
#    UART MSR 0x3fe  (2 mod 4, ofs 2)  read returns d->reg[com_msr] | 0xb0 (DCD|DSR|CTS forced)
#    UART SCR 0x3ff  (3 mod 4, ofs 3)  scratchpad: stores and returns the byte
#    8042 0x60/0x64  (0 mod 4, ofs 0)  liveness (0xAA->0x64 then 0x55 from 0x60)
import os, sys, pty, select, time, re

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"
RAW   = os.environ.get("LCAF2_RAW", "")

ZERO, T0, T1, T2, T3, T4, T5, T6 = 31, 1, 2, 3, 4, 5, 6, 7

def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, d, rb=ZERO): return mem(0x08, ra, rb, d)
def LDAH(ra, d, rb=ZERO): return mem(0x09, ra, rb, d)
def LDBU(ra, d, rb):      return mem(0x0a, ra, rb, d)   # byte load  -> len 1
def LDWU(ra, d, rb):      return mem(0x0c, ra, rb, d)   # word load  -> len 2
def LDL (ra, d, rb):      return mem(0x28, ra, rb, d)   # long load  -> len 4
def LDQ (ra, d, rb):      return mem(0x29, ra, rb, d)   # quad load  -> len 8
def STB (ra, d, rb):      return mem(0x0e, ra, rb, d)   # byte store -> len 1
def STW (ra, d, rb):      return mem(0x0d, ra, rb, d)   # word store -> len 2

def load_const(reg, val):
    lo = val & 0xffff; hi = (val >> 16) & 0xffff
    if lo >= 0x8000: hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo: ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

SENT = 0x11335577             # NO bit overlap with 0x60/0xb0/0x5a masks; low byte 0x77 distinct
def sent(reg): return load_const(reg, SENT)

K0SEG = 0xfffffc0000000000
def k0(p): return K0SEG | p
LCA_PCI_SIO  = 0x1c0000000
LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000
def SP(port):   return LCA_PCI_SIO  + (port << 5)
def FLAT(port): return LCA_ISA_BASE + port

KBC_CMD, KBC_DAT = 0x64, 0x60
IER, LSR, MSR, SCR = 0x3f9, 0x3fd, 0x3fe, 0x3ff
NODEV = 0x300

SCRATCH = 0x01020000
CODE    = 0x01040000
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")
if not os.path.exists(DUMMY):
    open(DUMMY, "wb").write(b"\0" * 8)

def session(cmds, settle=3.0, spin=4.0):
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
        try:
            os.write(fd, (c + "\n").encode("latin-1"))
        except OSError:
            alive = False; break
        if not rd(spin if i == len(cmds) - 1 else 0.45):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.5)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return None if not m else int(m.group(1), 16)

def build(consts, phases):
    prog = load_const(T0, SCRATCH)
    lens = [len(prog)]
    for ops, _ in phases:
        prog += ops; lens.append(len(ops))
    cmds  = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    cmds += ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for (ops, pr), n in zip(phases, lens[1:]):
        cmds.append("step %d" % n)
        if pr is not None:
            cmds.append("print %s" % pr)
    return cmds

def run(tag, consts, phases, settle=3.0, spin=4.0):
    cmds = build(consts, phases)
    txt, alive = session(cmds, settle, spin)
    if RAW:
        with open(os.path.join(RAW, "raw_%s.txt" % tag), "w", encoding="utf-8") as f:
            f.write("### cmds\n" + "\n".join(cmds) + "\n### transcript\n" + txt)
    return txt, alive

def hx(v): return "absent" if v is None else "0x%x" % v
def dead_or_hint(txt): return "attrib" if "in lca_isa access function" in txt else "other"

print("lca_f2_probe -- binary=%s label=%s" % (BIN, LABEL))
print("SENT=0x%x" % SENT)

# ============================================================ SESSION 1: reads + writes that
# never exit under ANY of the four (equality cells + (2,1)); one live session.
#  slots: 0 SP(IER) 1 FLAT(IER) 2 SP(LSR) 3 FLAT(LSR) 4 SP(MSR) 5 FLAT(MSR) 6 SP(SCR) 7 FLAT(SCR)
#         8 K0/CMD 9 selftest 10 K0/DAT
C1 = [k0(SP(IER)), k0(FLAT(IER)), k0(SP(LSR)), k0(FLAT(LSR)),
      k0(SP(MSR)), k0(FLAT(MSR)), k0(SP(SCR)), k0(FLAT(SCR)),
      k0(SP(KBC_CMD)), 0xAA, k0(SP(KBC_DAT))]
P1 = [
  # liveness through ofs 0
  ([LDQ(T1, 64, T0), LDQ(T2, 72, T0), STB(T2, 0, T1),
    LDQ(T1, 80, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),           # live: 0x55
  # R(1,1): LDBU sparse(LSR) len1 ofs1 ; want-per-variant
  ([LDQ(T1, 16, T0)] + sent(T2) + [LDBU(T2, 0, T1)], "t2"),          # r11 (sparse LSR b)
  ([LDQ(T1, 24, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),          # r11 flat devsig
  # R(2,1): LDWU sparse(IER... use LSR) len2 ofs1 -> byte in lane1 (data[1]); read LSR
  ([LDQ(T1, 16, T0)] + sent(T4) + [LDWU(T4, 0, T1)], "t4"),          # r21 (sparse LSR w)
  # R(2,2): LDWU sparse(MSR) len2 ofs2
  ([LDQ(T1, 32, T0)] + sent(T5) + [LDWU(T5, 0, T1)], "t5"),          # r22 (sparse MSR w)
  ([LDQ(T1, 40, T0)] + sent(T6) + [LDBU(T6, 0, T1)], "t6"),          # r22 flat MSR devsig
  # ---- WRITES ----
  # W(1,1): STB 0x3a -> sparse(IER) len1 ofs1 ; readback FLAT(IER) len1
  (load_const(T2, 0x3a) + [LDQ(T1, 0, T0), STB(T2, 0, T1),
     LDQ(T1, 8, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3"),          # w11 readback IER
  # W(2,1): STW 0x5a00 -> sparse(IER) len2 ofs1 -> forwards data[1]=0x5a (F8); readback IER
  (load_const(T2, 0x5a00) + [LDQ(T1, 0, T0), STW(T2, 0, T1),
     LDQ(T1, 8, T0)] + sent(T4) + [LDBU(T4, 0, T1)], "t4"),          # w21 readback IER
  # W(2,2): STW 0x0040 -> sparse(MSR) len2 ofs2 -> forwards data[0]=0x40; readback MSR
  (load_const(T2, 0x0040) + [LDQ(T1, 32, T0), STW(T2, 0, T1),
     LDQ(T1, 40, T0)] + sent(T5) + [LDBU(T5, 0, T1)], "t5"),         # w22 readback MSR
]
t1, a1 = run("s1", C1, P1)
def g(r): return printed(t1, r)
# re-extract by ORDER: print sequence is t3,t2,t3,t4,t5,t6,t3,t4,t5 -> but printed() matches
# LAST occurrence of each reg name, so read via distinct raw dump.
print("S1_ALIVE=%s" % a1)
# Parse each print in order from the transcript to avoid reg-name collisions.
seq = re.findall(r"print\s+(t\d)\s*\n\s*(0x[0-9a-f]+)", t1)
vals = [int(v, 16) for _, v in seq]
names = ["live","r11_sparse","r11_flat","r21_sparse","r22_sparse","r22_flat",
         "w11_ier","w21_ier","w22_msr"]
for i, nm in enumerate(names):
    print("S1 %-12s %s" % (nm, hx(vals[i]) if i < len(vals) else "absent"))
print("S1_SEQ_LEN=%d expected=%d" % (len(vals), len(names)))

# ============================================================ EXIT-CELL SESSIONS (one each)
# Each may end the host on HEAD/C; may serve on B; declines (alive) on A/C for reads.
def exit_session(tag, port, store, val, lenop):
    """lenop builds the access op given (destreg, srcreg, ptrreg). Returns (alive, readback, txt)."""
    # slots: 0 SP(port) 1 FLAT(port) 2 val
    C = [k0(SP(port)), k0(FLAT(port)), val]
    if store:
        # write val to sparse(port) via the width op; readback FLAT(port) len1 AFTER
        P = [ (load_const(T2, val) + [LDQ(T1, 0, T0)] + lenop(None, T2, T1), None),
              ([LDQ(T1, 8, T0)] + sent(T3) + [LDBU(T3, 0, T1)], "t3") ]
    else:
        # read sparse(port) into a seeded reg
        P = [ ([LDQ(T1, 0, T0)] + sent(T2) + lenop(T2, None, T1), "t2") ]
    txt, alive = session(build(C, P))
    if RAW:
        open(os.path.join(RAW, "raw_%s.txt" % tag), "w", encoding="utf-8").write(txt)
    rb = printed(txt, "t3") if store else printed(txt, "t2")
    return alive, rb, txt

# READ exit cells: (1,2) LDBU MSR ; (1,3) LDBU SCR ; (2,3) LDWU SCR
for tag, port, op in [("r12", MSR, lambda d,s,p: [LDBU(d,0,p)]),
                      ("r13", SCR, lambda d,s,p: [LDBU(d,0,p)]),
                      ("r23", SCR, lambda d,s,p: [LDWU(d,0,p)])]:
    al, rb, tx = exit_session(tag, port, False, 0, op)
    print("EXIT %-4s alive=%s read=%s hint=%s" % (tag, al, hx(rb), dead_or_hint(tx)))

# WRITE exit cells: (1,2) STB MSR ; (1,3) STB SCR ; (2,3) STW SCR
for tag, port, val, op in [("w12", MSR, 0x40, lambda d,s,p: [STB(s,0,p)]),
                           ("w13", SCR, 0x3c, lambda d,s,p: [STB(s,0,p)]),
                           ("w23", SCR, 0x7e00, lambda d,s,p: [STW(s,0,p)])]:
    al, rb, tx = exit_session(tag, port, True, val, op)
    print("EXIT %-4s alive=%s readback=%s hint=%s" % (tag, al, hx(rb), dead_or_hint(tx)))

print("LCAF2_DONE")
