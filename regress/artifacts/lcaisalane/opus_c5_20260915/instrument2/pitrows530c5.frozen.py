#!/usr/bin/env python3
# pitrows530c5.py <gxemul-binary> <label>
# #530 closing pass 5, Opus seat (2nd instance).  A PROTOTYPE SESSION -- NOT the shipped probe.  It asks one question:
# can the 8253's per-counter read/write flip-flops (dev_8253.c:280-285, #440) carry the forward-count class's cells at
# LANES 0/1/2 and at the split TAILS, as rows with wants, in place of the 8042 PC-style TODO stub?
#
# Encoders / session / print-parsing are copied VERBATIM from regress/lca_isalane_probe.py via
# ../instrument/disc530c5b.frozen.py.  build()/run() are NEW here: they allow SEVERAL prints per phase, which halves
# the phase count (and so the "put w" command count, which dominates wall time).
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
def prints_in_order(txt):
    return [int(v, 16) for _, v in re.findall(r"print\s+(t\d)\s*\n\s*(0x[0-9a-f]+)", txt)]
def run(consts, phases, names, settle=3.0, spin=4.0):
    #  phases: list of (ops, [print-register, ...]).  names: one per PRINT, in order.
    prog = load_const(T0, SCRATCH); lens = [len(prog)]
    for ops, _ in phases:
        prog += ops; lens.append(len(ops))
    cmds  = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    cmds += ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for (ops, prs), n in zip(phases, lens[1:]):
        cmds.append("step %d" % n)
        for p in prs: cmds.append("print %s" % p)
    txt, alive = session(cmds, settle, spin)
    vals = prints_in_order(txt)
    got = {n: (vals[i] if i < len(vals) else None) for i, n in enumerate(names)}
    #  EVIDENCE: dev_8253.c:198/:200 emit an UNLATCHED fatal() on an MSB write to counters 1 and 2.  Counted, not
    #  rowed -- it is a cost of this channel, and a cost has to be measured rather than predicted.
    ev = sorted(set(re.findall(r"TODO: [^\n]*", txt)))
    return alive, got, [(m, len(re.findall(re.escape(m), txt))) for m in ev]
def hx(v): return "absent" if v is None else "0x%x" % v
def b(v, sh=0): return None if v is None else (v >> sh) & 0xff

PASS = FAIL = 0
def row(name, got, want, note):
    global PASS, FAIL
    ok = (got == want)
    if ok: PASS += 1
    else:  FAIL += 1
    print("%-18s %-12s %-12s %-64s %s" % (name, got, want, note, "ok" if ok else "FAIL"))

print("pitrows530c5 -- binary=%s label=%s machine=%s" % (BIN, LABEL, MACH))
print("  PROTOTYPE session for #530 repair 6: the 8253 per-counter rd_msb/wr_msb flip-flops as the forward-count")
print("  class's channel at lanes 0/1/2 and the split tails.  dev_8253.c:280-285 toggles on EVERY counter access,")
print("  read and write, while (mode_byte & 0x30) == I8253_TIMER_16BIT; a control word rewinds both (:320-321).")
print("row                got          want         note")

PITCW = 0x43
WIDTHS = (("b", 1, LDBU, STB), ("w", 2, LDWU, STW), ("l", 4, LDL, STL), ("q", 8, LDQ, STQ))

def cw(cwslot=1):  return [LDQ(T1, 0, T0), LDQ(T2, 8 * cwslot, T0), STB(T2, 0, T1)]
def fl_st(s, aslot=2):  return [LDQ(T1, 8 * aslot, T0), LDQ(T2, 8 * s, T0), STB(T2, 0, T1)]
def fl_st0(aslot=2):    return [LDQ(T1, 8 * aslot, T0), STB(ZERO, 0, T1)]
def fl_rd(r, aslot=2):  return [LDQ(T1, 8 * aslot, T0)] + sent(r) + [LDBU(r, 0, T1)]

# ------------------------------------------------------------------ counters 0/1/2  =  lanes 0/1/2
for N in (0, 1, 2):
    port = 0x40 + N
    CWV = 0x34 | (N << 6)          # counter N, RW = 11 (LSB then MSB), mode 2, binary
    #      0              1     2                3              4     5     6                     7
    C = [k0(FLAT(PITCW)), CWV, k0(FLAT(port)), k0(SP(port)), 0x34, 0x12, 0x5a5a5a5a5a5a5a5a, 0x77]
    def lca_st(st, X): return ([LDQ(T1, 24, T0), LDQ(T2, 48, T0), st(T2, 0, T1)] if X
                               else [LDQ(T1, 24, T0), st(ZERO, 0, T1)])
    def lca_ld(ld, r): return [LDQ(T1, 24, T0)] + sent(r) + [ld(r, 0, T1)]

    P = [(cw() + fl_st(4) + fl_st(5) + fl_rd(T3) + fl_rd(T4), ["t3", "t4"])]
    names = ["live1", "live2"]
    for X in (0x5a, 0x00):
        for w, n, ld, st in WIDTHS:
            P.append((cw() + lca_st(st, X) + fl_st(5) + fl_rd(T3) + fl_rd(T4), ["t3", "t4"]))
            names += ["ps%02x_%d_r1" % (X, n), "ps%02x_%d_r2" % (X, n)]
    for L in (0x5a, 0x00):
        for w, n, ld, st in WIDTHS:
            P.append((cw() + (fl_st(6) if L else fl_st0()) + fl_st(5) + lca_ld(ld, T3) + fl_rd(T4), ["t3", "t4"]))
            names += ["pl%02x_%d_dlv" % (L, n), "pl%02x_%d_r1" % (L, n)]
    P.append((cw() + fl_st(6) + fl_st(5) + lca_ld(LDQ, T3) + fl_st(7) + fl_rd(T4) + fl_rd(T5), ["t3", "t4", "t5"]))
    names += ["pw_dlv", "pw_r1", "pw_r2"]

    a, g, ev = run(C, P, names)
    print("  RAW[pit%02x]: alive=%s live=%s/%s  pw=%s/%s/%s" % (port, a, hx(g["live1"]), hx(g["live2"]),
          hx(g["pw_dlv"]), hx(g["pw_r1"]), hx(g["pw_r2"])))
    for m, c in ev: print("  EVIDENCE[pit%02x]: %d x %s" % (port, c, m))
    row("pit%d alive" % N, "alive" if a else "dead", "alive", "CONTROL: nothing in this session may end the host")
    row("pit%d live1" % N, hx(g["live1"]), hx(0x34),
        "LIVENESS+DEVSIG: after a CW, flat LSB 0x34 / MSB 0x12 read back LSB first")
    row("pit%d live2" % N, hx(g["live2"]), hx(0x12),
        "LIVENESS+DEVSIG: ...then MSB -- two DIFFERENT bytes in order: only the 16-bit flip-flop does that")
    for X in (0x5a, 0x00):
        for w, n, ld, st in WIDTHS:
            row("pit%d ps%02x w%d" % (N, X, n), hx(b(g["ps%02x_%d_r1" % (X, n)])), hx(X),
                "(%d,%d) STORE 0x%02x: one lca write leaves it in the LSB (EXTRA access -> 0x12)" % (n, N, X))
            row("pit%d ps%02x w%dB" % (N, X, n), hx(b(g["ps%02x_%d_r2" % (X, n)])), hx(0x12),
                "(%d,%d) ...and the MSB holds the flat 0x12 (EXTRA access -> 0x%02x)" % (n, N, X))
    for L in (0x5a, 0x00):
        for w, n, ld, st in WIDTHS:
            row("pit%d pl%02x r%d" % (N, L, n), hx(b(g["pl%02x_%d_dlv" % (L, n)], 8 * (N % n))), hx(L),
                "(%d,%d) LOAD delivers the counter LSB 0x%02x at position %d" % (n, N, L, N % n))
            row("pit%d pl%02x r%dB" % (N, L, n), hx(b(g["pl%02x_%d_r1" % (L, n)])), hx(0x12),
                "(%d,%d) ...and the NEXT flat read gets the MSB (a duplicated read -> 0x%02x)" % (n, N, L))
    row("pit%d pw r1" % N, hx(b(g["pw_r1"])), hx(0x12),
        "(8,%d) LOAD then a flat store 0x77: read parity unmoved -> MSB 0x12" % N)
    row("pit%d pw r2" % N, hx(b(g["pw_r2"])), hx(0x77),
        "(8,%d) ...and 0x77 went to the LSB (an added WRITE on the read arm sends it to the MSB)" % N)
    print("")

# ------------------------------------------------------------------ split TAILS at port 0x40 (counter 0, lane 0)
#  SP(0x3f) + K: an 8-byte access straddling the 1 KB split at SP(0x40).  K = 0x1f/0x1e/0x1d/0x1b gives
#  head 1/2/3/5 at the UNMAPPED port 0x3f and TAIL 7/6/5/3 at port 0x40.  The tail's buffer position 0 is
#  register byte (8 - tail) = head, so the delivered byte is at that shift.
#      0              1     2              3                  4                  5                  6
C = [k0(FLAT(PITCW)), 0x34, k0(FLAT(0x40)), k0(SP(0x3f) + 0x1f), k0(SP(0x3f) + 0x1e), k0(SP(0x3f) + 0x1d),
     k0(SP(0x3f) + 0x1b), 0x34, 0x12, 0x77, 0x5a5a5a5a5a5a5a5a]
#      7     8     9     10
TAILS = ((7, 3, 8), (6, 4, 16), (5, 5, 24), (3, 6, 40))     # (tail len, address slot, delivered-byte shift)

P = [(cw() + fl_st(7) + fl_st(8) + fl_rd(T3) + fl_rd(T4), ["t3", "t4"])]
names = ["live1", "live2"]
for t, aslot, sh in TAILS:
    for X in (0x5a, 0x00):
        st = ([LDQ(T1, 8 * aslot, T0), LDQ(T2, 80, T0), STQ(T2, 0, T1)] if X
              else [LDQ(T1, 8 * aslot, T0), STQ(ZERO, 0, T1)])
        P.append((cw() + st + fl_st(8) + fl_rd(T3) + fl_rd(T4), ["t3", "t4"]))
        names += ["t%d_ps%02x_r1" % (t, X), "t%d_ps%02x_r2" % (t, X)]
for t, aslot, sh in TAILS:
    for L in (0x5a, 0x00):
        P.append((cw() + (fl_st(10) if L else fl_st0()) + fl_st(8)
                  + [LDQ(T1, 8 * aslot, T0)] + sent(T3) + [LDQ(T3, 0, T1)] + fl_rd(T4), ["t3", "t4"]))
        names += ["t%d_pl%02x_dlv" % (t, L), "t%d_pl%02x_r1" % (t, L)]
for t, aslot, sh in ((6, 4, 16), (3, 6, 40)):
    P.append((cw() + fl_st(10) + fl_st(8) + [LDQ(T1, 8 * aslot, T0)] + sent(T3) + [LDQ(T3, 0, T1)]
              + fl_st(9) + fl_rd(T4) + fl_rd(T5), ["t3", "t4", "t5"]))
    names += ["t%d_pw_dlv" % t, "t%d_pw_r1" % t, "t%d_pw_r2" % t]

a, g, ev = run(C, P, names)
print("  RAW[tails]: alive=%s live=%s/%s" % (a, hx(g["live1"]), hx(g["live2"])))
for m, c in ev: print("  EVIDENCE[tails]: %d x %s" % (c, m))
row("pitT alive", "alive" if a else "dead", "alive", "CONTROL: nothing in this session may end the host")
row("pitT live1", hx(g["live1"]), hx(0x34), "LIVENESS+DEVSIG: flat LSB then MSB at port 0x40")
row("pitT live2", hx(g["live2"]), hx(0x12), "LIVENESS+DEVSIG: ...the second read gets the OTHER half")
for t, aslot, sh in TAILS:
    for X in (0x5a, 0x00):
        row("pitT ps%02x t%d" % (X, t), hx(b(g["t%d_ps%02x_r1" % (t, X)])), hx(X),
            "(%d,0) STQ TAIL at 0x40 stores 0x%02x: one write -> LSB (EXTRA access -> 0x12)" % (t, X))
        row("pitT ps%02x t%dB" % (X, t), hx(b(g["t%d_ps%02x_r2" % (t, X)])), hx(0x12),
            "(%d,0) ...MSB holds the flat 0x12 (EXTRA access -> 0x%02x)" % (t, X))
for t, aslot, sh in TAILS:
    for L in (0x5a, 0x00):
        row("pitT pl%02x t%d" % (L, t), hx(b(g["t%d_pl%02x_dlv" % (t, L)], sh)), hx(L),
            "(%d,0) LDQ TAIL delivers the LSB 0x%02x at register byte %d" % (t, L, sh // 8))
        row("pitT pl%02x t%dB" % (L, t), hx(b(g["t%d_pl%02x_r1" % (t, L)])), hx(0x12),
            "(%d,0) ...and the next flat read gets the MSB (a duplicated read -> 0x%02x)" % (t, L))
for t in (6, 3):
    row("pitT pw t%d" % t, hx(b(g["t%d_pw_r1" % t])), hx(0x12),
        "(%d,0) LDQ TAIL then a flat store 0x77: read parity unmoved -> MSB 0x12" % t)
    row("pitT pw t%dB" % t, hx(b(g["t%d_pw_r2" % t])), hx(0x77),
        "(%d,0) ...and 0x77 went to the LSB (an added WRITE on the read arm sends it to the MSB)" % t)
print("")
print("PITROWS_RESULT=%d/%d" % (PASS, PASS + FAIL))
print("PITROWS_DONE")
