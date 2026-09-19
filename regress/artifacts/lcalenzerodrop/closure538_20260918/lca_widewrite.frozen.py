#!/usr/bin/env python3
"""lca_widewrite_probe.py -- #530's width row, CLASS-CLOSED by #538: the four C=16 WRITE lanes.

WHAT IT PINS.  `#530`'s instruction-driven detector, lca_isalane_probe.py, cannot express an access wider than 8 bytes:
the widest Alpha store, STQ, is 8.  The only guest producer of a wider access to DEVICE_ACCESS(lca_isa) is the PROM
GETENV callback (CALL_PAL 0x3fffffe), which copies a host string into guest memory with store_buf() -- chunks of
1024/256/64/16/4/1 bytes, each only at an address aligned to its size, each reaching the handler whole.  This file drives
that producer at FOUR cells, one per byte lane, ONE ISOLATED EMULATOR SESSION PER CELL: a variant that drops a wide store
into the read arm writes zeros into store_buf's SOURCE (the emulator's own boot string), so cells sharing a session would
see a shorter string -- one session each removes the ordering question entirely.

HISTORY, because the first version's claim was wrong.  #530 (8bd97e4) shipped ONE cell, (C=16, k=0, lane 3), and said
"any guard that declines a len > 8 WRITE" was caught.  Its pass 2 measured seven one-edit variants that pass that cell
(regress/artifacts/lcalenzerodrop/opus_p2_20260918/, 102 legs), and the flagship ruled (#530 §F2, fable5 R1/R2) that ONE of
them is a floor breach: `&& (len <= 8 || (P & 3) == 3)` services wide writes at the rowed lane only.  LANE is a floor axis
because the body's `data[ofs]' distinguishes all four lanes; so the floor is {write arm} x {lane 0, 1, 2, 3}, and #538
rows the other three.  Row demand is per LANE, not per variant: the lane-1 exemption `&& (len <= 8 || (P & 3) != 1)`,
which the popular two-cell covering {mc2, kbc1024} misses, is red here at `low16'.

CONTRACT (clause e).  DESIGNED TO CATCH, at each of the four byte lanes (C=16, k=0): any variant that DECLINES, REFUSES
or MISROUTES a len > 8 WRITE -- the guard form (`len == 0 || len > 8'), the write-arm-conjunct form (`&& len <= 8'), a
LANE-conditioned form (`&& (len <= 8 || (P & 3) == L)', or `!= L', for any lane L), and a wrong lane byte (`data[0]'
for `data[ofs]', red at lanes 1-3).
DISCLOSED, NOT CAUGHT -- each with its warrant, and the named classes are ALREADY RULED in the parent's header:
  (i)    width thresholds above 16 (`len <= 16', `<= 64', `<= 256'): the body tests `len' only against 0 (joint cells);
         each is MEASURED killed at a wider cell in opus_p2_20260918 (va, vb, vw64, vw256), not rowed here.
  (ii)   port-conditioned refusals: the parent's p_port10 class -- the body never compares the port to a constant.  A
         refusal below port 0x200 happens to red `low16' (port 0x21); that is incidental, not a contract claim.
  (iii)  the discarded sparse bits a<4:0> (k): the parent's lcaisasize class -- a k-keyed or alignment-keyed refusal.
  (iv)   chunk position >= 2 of a multi-chunk write: the handler holds no state across calls.
  (v)    the READ direction: no wide-read producer exists (store_buf only writes; PROM PUTS reads single bytes).
  (vi)   delivery of a wide chunk's NON-LANE bytes: `lcawidefold' (reopened; the drop count is alignment-dependent).
  (vii)  data values: a wide chunk never forwards 0 -- argv strings and basenames carry no NUL, and the lane byte sits at
         offset <= 3 while the terminator is at >= 15.
  (viii) forward COUNT: every row here reads a LATCH, so a len > 8-gated duplicate or added forward is invisible.

WANT IS DERIVED, NEVER TYPED: sim_store_buf() replays src/core/memory.c's store_buf chunking on (a2, len) and applies the
SHIPPED handler rule (byte = s[chunk offset + (P & 3) % C], forwarded to port P) to every chunk; the last byte landing on
a register's port is that register's WANT.  THE WIDTH IS PINNED BY CONSTRUCTION, NOT BY VALUE: no forwarded byte can
distinguish a 16-byte chunk from a 4-byte one at the same address (both forward s[lane]), so each cell declares its chunk
list and the probe asserts it -- and asserts that the chunk landing on each observed register is wider than 8.

HARNESS RULES, each from a defect of the first version:
  * a session is RETRIED once, with tripled patience, only if its prints are missing AND the emulator was still ALIVE --
    as the parent's dsession() does; the first version retried a DEAD session and so could record a host death as a pass.
  * exit status is 0 only at full marks; the first version exited 0 on FAIL.
  * the last row is an IDENTITY row pinning the row count this file emits.

WITNESS vs DETECTOR.  This is a DETECTOR (green once the defect is gone).  #530's rung-3 WITNESS is lca_isalane_probe.py's
13/16 on the pre-fix build.
"""
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
MACH  = "alphabook1"
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")

# ---- encoder, copied from the parent via the first version, unchanged
ZERO, T0, T1, T2, T3, T4, T5, T6, T7 = 31, 1, 2, 3, 4, 5, 6, 7, 8
A0, A1, A2, A3 = 16, 17, 18, 19
RA = 26
def mem(op, ra, rb, disp):
    assert -32768 <= disp <= 32767, "displacement %d out of range" % disp
    return (op << 26) | (ra << 21) | (rb << 16) | (disp & 0xffff)
def LDA (ra, disp, rb=ZERO): return mem(0x08, ra, rb, disp)
def LDAH(ra, disp, rb=ZERO): return mem(0x09, ra, rb, disp)
def LDBU(ra, disp, rb):      return mem(0x0a, ra, rb, disp)
def STB (ra, disp, rb):      return mem(0x0e, ra, rb, disp)
def LDQ (ra, disp, rb):      return mem(0x29, ra, rb, disp)
CALL_PAL_PROM = (0x00 << 26) | 0x3fffffe

def load_const(reg, val):
    lo = val & 0xffff
    hi = (val >> 16) & 0xffff
    if lo >= 0x8000:
        hi = (hi + 1) & 0xffff
    ops = [LDAH(reg, hi if hi < 0x8000 else hi - 0x10000)]
    if lo:
        ops.append(LDA(reg, lo if lo < 0x8000 else lo - 0x10000, reg))
    return ops

SENT = 0x0bad1d8a
def sent(reg): return load_const(reg, SENT)

K0SEG        = 0xfffffc0000000000
def k0(p):   return K0SEG | p
LCA_PCI_SIO  = 0x1c0000000
LCA_ISA_BASE = LCA_PCI_SIO + 0x10000000
def SP(port):   return LCA_PCI_SIO + (port << 5)
def FLAT(port): return LCA_ISA_BASE + port
SCRATCH, CODE = 0x01020000, 0x01040000
KBC_CMD, KBC_DAT = 0x64, 0x60

def session(bootstr, cmds, settle, spin):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "alpha", "-e", MACH, "-M", "64",
                       "-o", bootstr, "0x20000000:" + DUMMY])
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
    try:
        os.waitpid(pid, 0)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

def build(consts, phases):
    prog = load_const(T0, SCRATCH)
    lens = [len(prog)]
    for ops, _ in phases:
        prog += ops
        lens.append(len(ops))
    cmds  = ["put d 0x%x, 0x%x" % (SCRATCH + 8 * i, v) for i, v in enumerate(consts)]
    cmds += ["put w 0x%x, 0x%08x" % (k0(CODE) + 4 * i, op) for i, op in enumerate(prog)]
    cmds += ["pc=0x%x" % k0(CODE), "step %d" % lens[0]]
    for (ops, pr), n in zip(phases, lens[1:]):
        cmds.append("step %d" % n)
        if pr is not None:
            cmds.append("print %s" % pr)
    return cmds

def printed(t, reg):
    m = re.search(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
    return None if not m else int(m.group(1), 16)

rows = []
def row(name, got, want, note=""):
    assert len(name) <= 13, "row name %r exceeds 13 characters (the %%-14s column + gate pattern)" % name
    ok = (got == want)
    rows.append((name, ok))
    g = got if not isinstance(got, int) else "0x%x" % got
    w = want if not isinstance(want, int) else "0x%x" % want
    print("%-14s %-24s %-24s %-56s %s" % (name, g, w, note, "ok" if ok else "FAIL"))
    return ok

# ---- the producer, replayed (src/core/memory.c store_buf) + the SHIPPED lca_isa write rule
def sim_store_buf(a, n):
    out, off, psize = [], 0, 1024
    while n != 0:
        if (a & (psize - 1)) == 0:
            while n >= psize:
                out.append((a, psize, off)); a += psize; off += psize; n -= psize
        psize >>= 2
    return out                                # the trailing store_byte loop is dead: psize 1 drains it

def shipped_lands(a_sparse, n, sbytes):
    return [((a >> 5), sbytes[off + ((a >> 5) & 3) % c]) for a, c, off in sim_store_buf(a_sparse, n)]

ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
def pat(n): return (ALPH * (n // len(ALPH) + 1))[:n]
IDENT = lambda v: v
MSRX  = lambda v: v | 0xb0                    # the ns16550 MSR reads back OR DCD|DSR|CTS

#  ---- THE CELLS
#  name: (a3, target port, k, -o string, chunks expected, [(reg port, kind, preset, xform, row tag)])
#  THE FLOOR, as ruled (fable5, #530 §F2, R1/R2): the four C=16 WRITE lanes at k = 0.  `wide' is the shipped
#  cell and keeps its row names; the other three close the LANE partition that `data[ofs]' distinguishes.
#  Each a3 = 16 against a 16-character string, so len = min(16, 17) = 16: ONE 16-byte chunk (asserted below).
#  name     a3  port   k  -o string            chunks  [(reg port, kind, preset, xform, row tag)]
CELLS = {
    "wide":  (16, 0x2ff, 0, "ABCDEFGHIJKLMNOP", [16], [(0x2ff, "sp", 0x5a, IDENT, "")]),  # lane 3: ns16550 SCR
    "l0w16": (16, 0x2fc, 0, "ABCDEFGHIJKLMNOP", [16], [(0x2fc, "sp", 0x03, IDENT, "")]),  # lane 0: ns16550 MCR
    "low16": (16, 0x021, 0, "ABCDEFGHIJKLMNOP", [16], [(0x021, "sp", 0xff, IDENT, "")]),  # lane 1: 8259 IMR
    "l2w16": (16, 0x2fe, 0, "ABCDEFGHIJKLMNOP", [16], [(0x2fe, "sp", 0x00, MSRX,  "")]),  # lane 2: ns16550 MSR
}
assert sorted(spec[1] & 3 for spec in CELLS.values()) == [0, 1, 2, 3], "the floor is ALL FOUR lanes"

def run_cell(name, spec):
    a3v, tgt, k, bootstr, chunks, regs = spec
    sbytes = bootstr.encode("latin-1") + b"\0"
    lenv = a3v if len(bootstr) >= a3v else len(bootstr) + 1   # alpha_prom_call: min(a3, strlen + 1)
    a_sparse = (tgt << 5) + k
    got_chunks = [c for _, c, _ in sim_store_buf(a_sparse, lenv)]
    assert got_chunks == chunks, "cell %s: replayed chunks %r != declared %r -- the WIDTH is not what this cell claims" \
        % (name, got_chunks, chunks)
    lands = shipped_lands(a_sparse, lenv, sbytes)
    #  THE WIDTH PIN (fable5 R2; the #530 pass-2 F10 gap).  No forwarded-byte VALUE can pin the width: a 4-byte chunk
    #  at the same address forwards the same s[lane].  So the construction itself is asserted: the chunk that lands on
    #  each observed register must be WIDER THAN 8, or this cell is not testing what its rows claim.
    for a, c, off in sim_store_buf(a_sparse, lenv):
        if any((a >> 5) == port for port, _, _, _, _ in regs):
            assert c > 8, "cell %s: the chunk landing on port 0x%x is %d bytes -- not a wide write" % (name, a >> 5, c)
    consts = [0, k0(SP(tgt) + k)]
    def slot(v):
        consts.append(v); return 8 * (len(consts) - 1)
    res = [T3, T4, T5, T6, T7]
    rname = {T3: "t3", T4: "t4", T5: "t5", T6: "t6", T7: "t7"}
    plan = []
    for port, kind, preset, xf, tag in regs:
        if kind == "sp":
            s_reg = slot(k0(SP(port)))
            pre = [LDQ(T2, s_reg, T0)] + load_const(T1, preset) + [STB(T1, 0, T2)]
            rd_ = lambda r, s_reg=s_reg: [LDQ(T2, s_reg, T0)] + sent(r) + [LDBU(r, 0, T2)]
            arm = []
        else:                                 # the 8042 command byte, sequenced through FLAT
            s_cmd, s_dat = slot(k0(FLAT(KBC_CMD))), slot(k0(FLAT(KBC_DAT)))
            pre = ([LDQ(T2, s_cmd, T0)] + load_const(T1, 0x60) + [STB(T1, 0, T2)]
                   + [LDQ(T2, s_dat, T0)] + load_const(T1, preset) + [STB(T1, 0, T2)])
            rd_ = lambda r, s_cmd=s_cmd, s_dat=s_dat: ([LDQ(T2, s_cmd, T0)] + load_const(T1, 0x20)
                   + [STB(T1, 0, T2), LDQ(T2, s_dat, T0)] + sent(r) + [LDBU(r, 0, T2)])
            arm = [LDQ(T2, s_cmd, T0)] + load_const(T1, 0x60) + [STB(T1, 0, T2)]
        want = preset
        for p, b in lands:
            if p == port:
                want = b
        plan.append((port, xf, preset, tag, pre, rd_, arm, want))
    phases = [(pre, None) for _, _, _, _, pre, _, _, _ in plan]
    phases += [(rd_(res[j]), rname[res[j]]) for j, (_, _, _, _, _, rd_, _, _) in enumerate(plan)]
    arm_all = sum((arm for _, _, _, _, _, _, arm, _ in plan), [])
    phases.append((arm_all + load_const(A0, 0x22) + load_const(A1, 0x8) + [LDQ(A2, 8, T0)]
                   + load_const(A3, a3v) + [LDQ(RA, 0, T0), CALL_PAL_PROM], None))
    n = len(plan)
    phases += [(rd_(res[n + j]), rname[res[n + j]]) for j, (_, _, _, _, _, rd_, _, _) in enumerate(plan)]
    consts[0] = k0(CODE) + 4 * (len(load_const(T0, SCRATCH)) + sum(len(o) for o, _ in phases[:2 * n + 1]))
    cmds = build(consts, phases)
    names = [rname[r] for r in res[:2 * n]]
    txt, alive = session(bootstr, cmds, 3.0, 4.0)
    retried = False
    if alive and any(printed(txt, x) is None for x in names):   # F6: never retry a session that DIED
        retried = True
        txt, alive = session(bootstr, cmds, 9.0, 12.0)
    print("  cell %-8s a3=%d len=%d a2=SP(0x%x)+%d chunks=%s retried=%s"
          % (name, a3v, lenv, tgt, k, got_chunks, "yes" if retried else "none"))
    if os.environ.get("WIDEWRITE_RAW"):
        open(os.environ["WIDEWRITE_RAW"] + "." + name, "w", encoding="utf-8").write(txt)
    row("%s alive" % name, "alive" if alive else "died", "alive",
        "the guest survives the inline CALL_PAL 0x3fffffe")
    for j, (port, xf, preset, tag, _, _, _, want) in enumerate(plan):
        row(("%s live%s" % (name, tag)).strip(), printed(txt, rname[res[j]]), xf(preset),
            "ROUND-TRIP CONTROL: preset 0x%02x round-trips through port 0x%x" % (preset, port))
    for j, (port, xf, preset, tag, _, _, _, want) in enumerate(plan):
        row(("%s getenv%s" % (name, tag)).strip(), printed(txt, rname[res[n + j]]), xf(want),
            "len %d: the shipped rule puts 0x%02x on port 0x%x" % (lenv, want, port))

print("lca_widewrite -- binary=%s label=%s machine=%s cells=%s" % (BIN, LABEL, MACH, " ".join(CELLS)))
for name, spec in CELLS.items():
    run_cell(name, spec)
EXPECT_ROWS = 3 * len(CELLS) + 1               # alive, live, getenv per cell, plus this row
row("row count", len(rows) + 1, EXPECT_ROWS, "IDENTITY: the row count this file emits")
ok = sum(1 for _, o in rows if o)
print("WIDEWRITE_RESULT=%d/%d" % (ok, len(rows)))
print("WIDEWRITE_DONE")
sys.exit(0 if ok == len(rows) else 1)
