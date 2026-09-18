#!/usr/bin/env python3
"""lca_widecell_probe.py -- the FROZEN width row (8bd97e4:regress/lca_widewrite_probe.py) generalised to
the other wide cells the store_buf producer reaches.  Opus measuring seat, #530 closing pass 7, 2026-09-18.

WHAT IS COPIED VERBATIM FROM THE FROZEN ROW: the encoder, load_const, sent(), SP/k0, session() (the pty
harness, `-V -x -E alpha -e alphabook1 -M 64 -o <string> 0x20000000:alpha_dummy.bin'), build(), printed(),
row(), the retry-once-with-tripled-patience rule, and the GETENV phase shape (a0 = 0x22 PROM_R_GETENV,
a1 = 0x8 PROM_E_BOOTED_OSFLAGS, a3 = LEN, ra = the instruction after the CALL_PAL, computed from the layout).

WHAT CHANGES, PER CELL (the CELLS table): the -o string, a3, the GETENV destination a2 (port and the
discarded sparse offset k), and which device register(s) are preset / read back.  The frozen row stores
its preset through the SPARSE window and reads it back through the SPARSE window (1-byte accesses, identical
in every variant by construction); the ns16550/8259 cells do the same.  The 8042 cells sequence the command
byte through the FLAT mapping (LCA_ISA_BASE + port, which bypasses lca_isa entirely), exactly as the parent
probe's kbc_ldcmd/kbc_rdcmd do, so the ONLY lca_isa access in those cells is the GETENV chunk itself.

WANT IS DERIVED, NEVER TYPED: sim_store_buf() replays src/core/memory.c's store_buf chunking on (a2, len)
and applies the SHIPPED handler rule (byte = s[chunk offset + (P & 3) % C], forwarded to port P) to every
chunk; the last byte landing on a register's port is that register's WANT (preset if none lands).
"""
import os, pty, re, select, sys, time

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
CELL  = sys.argv[3] if len(sys.argv) > 3 else "?"
MACH  = "alphabook1"
DUMMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alpha_dummy.bin")

# ---- encoder, copied from lca_widewrite_probe.py (itself copied from lca_isalane_probe.py)
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

def load_const(reg, val):                     # 32-bit only, exactly as the parent
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

def session(bootstr, cmds, settle, spin):     # the frozen row's session(), -o made a parameter
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

def build(consts, phases):                    # copied verbatim in behaviour
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
    ok = (got == want)
    rows.append((name, ok))
    g = got if not isinstance(got, int) else "0x%x" % got
    w = want if not isinstance(want, int) else "0x%x" % want
    print("%-18s %-12s %-12s %-60s %s" % (name, g, w, note, "ok" if ok else "FAIL"))
    return ok

# ---- the producer, replayed: src/core/memory.c store_buf() + the SHIPPED lca_isa write rule
def sim_store_buf(a, n):
    """Chunks (sparse_addr, size, string_offset) exactly as store_buf issues them."""
    out, off, psize = [], 0, 1024
    while n != 0:
        if (a & (psize - 1)) == 0:
            while n >= psize:
                out.append((a, psize, off)); a += psize; off += psize; n -= psize
        psize >>= 2
    return out                                # store_buf's trailing byte loop is dead: psize 1 drains it

def shipped_lands(a_sparse, n, sbytes):
    """[(port, byte)] in issue order: P = A >> 5, byte = s[off + (P & 3) % C]  (dev_lca.c:297-302)."""
    return [((a >> 5), sbytes[off + ((a >> 5) & 3) % c]) for a, c, off in sim_store_buf(a_sparse, n)]

ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
def pat(n): return (ALPH * (n // len(ALPH) + 1))[:n]

# ---- the cells.  kind: 'sp' = preset/readback through the SPARSE window (as the frozen row);
#      'kbc' = the 8042 command byte, sequenced through the FLAT mapping (as the parent's kbc_* helpers).
#      xform: what the register reads back as, given what was stored (MSR ORs in DCD|DSR|CTS = 0xb0).
IDENT = lambda v: v
MSRX  = lambda v: v | 0xb0
CELLS = {
    # name      a3    target port  k    -o string    [(reg port, kind, preset, xform)]           setup
    "frozen16": (16,  0x2ff,       0,   pat(16),     [(0x2ff, "sp", 0x5a, IDENT)],               None),
    "k16":      (16,  0x2ff,       16,  pat(16),     [(0x2ff, "sp", 0x5a, IDENT)],               None),
    "l0w16":    (16,  0x2fc,       0,   pat(16),     [(0x2fc, "sp", 0x03, IDENT)],               None),
    "l0w64":    (64,  0x2fc,       0,   pat(64),     [(0x2fc, "sp", 0x03, IDENT)],               None),
    "l2w64":    (64,  0x2fe,       0,   pat(64),     [(0x2fe, "sp", 0x00, MSRX)],                None),
    "low16":    (16,  0x021,       0,   pat(16),     [(0x021, "sp", 0xff, IDENT)],               None),
    "mc2":      (32,  0x2fe,       16,  pat(32),     [(0x2ff, "sp", 0x5a, IDENT),
                                                      (0x2fe, "sp", 0x00, MSRX)],                None),
    "kbc16":    (16,  0x060,       0,   pat(16),     [(0x060, "kbc", 0x04, IDENT)],              None),
    "kbc256":   (256, 0x060,       0,   pat(256),    [(0x060, "kbc", 0x04, IDENT)],              None),
    "kbc1024":  (1024,0x060,       0,   pat(1024),   [(0x060, "kbc", 0x04, IDENT)],              None),
}
if CELL not in CELLS:
    sys.exit("usage: lca_widecell_probe.py <bin> <label> <cell>   cells: " + " ".join(CELLS))
A3V, TGT, K, BOOTSTR, REGS, _ = CELLS[CELL]
SBYTES = BOOTSTR.encode("latin-1") + b"\0"
LENV = A3V if len(BOOTSTR) >= A3V else len(BOOTSTR) + 1          # alpha_prom_call: min(a3, strlen + 1)
A_SPARSE = (TGT << 5) + K
LANDS = shipped_lands(A_SPARSE, LENV, SBYTES)

# consts: slot 0 = RET, slot 1 = GETENV a2, then per register: its address (and the 8042 flat ports)
KBC_CMD, KBC_DAT = 0x64, 0x60
consts = [0, k0(SP(TGT) + K)]
def slot(v):
    consts.append(v); return 8 * (len(consts) - 1)
RES = [T3, T4, T5, T6, T7]                   # result registers; print names t3..t7
RNAME = {T3: "t3", T4: "t4", T5: "t5", T6: "t6", T7: "t7"}
plan = []
for j, (port, kind, preset, xf) in enumerate(REGS):
    if kind == "sp":
        s_reg = slot(k0(SP(port)))
        preset_ops = [LDQ(T2, s_reg, T0)] + load_const(T1, preset) + [STB(T1, 0, T2)]
        read_ops = lambda r, s_reg=s_reg: [LDQ(T2, s_reg, T0)] + sent(r) + [LDBU(r, 0, T2)]
        arm_ops = []
    else:                                     # kbc: FLAT cmd port 0x64, FLAT data port 0x60
        s_cmd, s_dat = slot(k0(FLAT(KBC_CMD))), slot(k0(FLAT(KBC_DAT)))
        preset_ops = ([LDQ(T2, s_cmd, T0)] + load_const(T1, 0x60) + [STB(T1, 0, T2)]      # K_LDCMDBYTE
                      + [LDQ(T2, s_dat, T0)] + load_const(T1, preset) + [STB(T1, 0, T2)])
        read_ops = lambda r, s_cmd=s_cmd, s_dat=s_dat: ([LDQ(T2, s_cmd, T0)] + load_const(T1, 0x20)
                      + [STB(T1, 0, T2), LDQ(T2, s_dat, T0)] + sent(r) + [LDBU(r, 0, T2)])  # K_RDCMDBYTE
        arm_ops = [LDQ(T2, s_cmd, T0)] + load_const(T1, 0x60) + [STB(T1, 0, T2)]           # K_LDCMDBYTE
    want = preset
    for p, b in LANDS:
        if p == port:
            want = b
    plan.append((port, kind, preset, xf, preset_ops, read_ops, arm_ops, want))

phases = []
for port, kind, preset, xf, pre, rd_, arm, want in plan:
    phases.append((pre, None))
for j, (port, kind, preset, xf, pre, rd_, arm, want) in enumerate(plan):
    phases.append((rd_(RES[j]), RNAME[RES[j]]))
arm_all = []
for port, kind, preset, xf, pre, rd_, arm, want in plan:
    arm_all += arm
p_get = (arm_all + load_const(A0, 0x22) + load_const(A1, 0x8) + [LDQ(A2, 8, T0)]
         + load_const(A3, A3V) + [LDQ(RA, 0, T0), CALL_PAL_PROM])
phases.append((p_get, None))
nreg = len(plan)
for j, (port, kind, preset, xf, pre, rd_, arm, want) in enumerate(plan):
    phases.append((rd_(RES[nreg + j]), RNAME[RES[nreg + j]]))
consts[0] = k0(CODE) + 4 * (len(load_const(T0, SCRATCH)) + sum(len(o) for o, _ in phases[:2 * nreg + 1]))

print("lca_widecell -- binary=%s label=%s cell=%s machine=%s a3=%d len=%d a2=SP(0x%x)+%d A=0x%x"
      % (BIN, LABEL, CELL, MACH, A3V, LENV, TGT, K, A_SPARSE))
print("  -o string: %d chars, begins %r" % (len(BOOTSTR), BOOTSTR[:20]))
print("  store_buf chunks (sparse addr, size, string offset): %s"
      % ", ".join("(0x%x,%d,%d)" % c for c in sim_store_buf(A_SPARSE, LENV)))
print("  SHIPPED rule lands: %s" % ", ".join("port 0x%x <- 0x%02x %r" % (p, b, chr(b)) for p, b in LANDS))

cmds = build(consts, phases)
names = [RNAME[r] for r in RES[:2 * nreg]]
txt, alive = session(BOOTSTR, cmds, 3.0, 4.0)
retried = False
if any(printed(txt, n) is None for n in names):
    retried = True
    txt, alive = session(BOOTSTR, cmds, 3.0 * 3, 4.0 * 3)
print("WIDECELL_RETRIED=%s" % ("yes" if retried else "none"))
if os.environ.get("WIDECELL_RAW"):
    open(os.environ["WIDECELL_RAW"], "w", encoding="utf-8").write(txt)

row("%s alive" % CELL, "alive" if alive else "died", "alive", "the guest survives the inline CALL_PAL 0x3fffffe")
for j, (port, kind, preset, xf, pre, rd_, arm, want) in enumerate(plan):
    got = printed(txt, RNAME[RES[j]])
    row("%s live %x" % (CELL, port), got, xf(preset),
        "CONTROL: preset 0x%02x round-trips through port 0x%x (%s)" % (preset, port, kind))
for j, (port, kind, preset, xf, pre, rd_, arm, want) in enumerate(plan):
    got = printed(txt, RNAME[RES[nreg + j]])
    row("%s getenv %x" % (CELL, port), got, xf(want),
        "after GETENV len %d: shipped rule puts 0x%02x on port 0x%x" % (LENV, want, port))
ok = sum(1 for _, o in rows if o)
print("WIDECELL_RESULT=%s %s %d/%d" % (CELL, LABEL, ok, len(rows)))
print("WIDECELL_DONE")
