#!/usr/bin/env python3
#
#  #564 sgirekills (MTE half) -- DETECTOR: dev_sgi_re.c's do_mte_transfer() refuses five unsupported transfer
#  parameters by DECLINING the transfer with a latched announcement, where it used to end the process:
#
#      S1  mode & MTE_MODE_STIPPLE              (before the destination switch: every destination)
#      S2  src > MTE_TLB_C                      (before the switch: every destination, fill or copy)
#      S3  mode & MTE_MODE_COPY                 (MTE_TLB_LIN_A / LIN_B only -- tiled COPY is implemented)
#      S4  depth != 8                           (linear only)
#      S5  bytemask != 0xffffffff               (linear only)
#
#  Every row is a REAL GUEST STORE or LOAD through real address decode and memory_rw on the unmodified
#  `-E sgi -e ip32' machine (session mechanics from regress/sgi_mte_fill_probe.py, #509): the MTE is programmed
#  with `sw', the RE TLBs with `sd', and a transfer fires on the write whose ADDRESS carries CRIME_DE_START.
#
#  ---------------------------------------------------------------------------------------------
#  CONTRACT (vacuity-floor clause (e)) -- WHAT THIS DETECTOR IS DESIGNED TO CATCH.
#
#  * the terminating call put back at any site (every session ends at its first refused transfer);
#  * the decline removed but the announcement kept -- the transfer proceeding with the refused parameter
#    ignored (member 1): every refused transfer is aimed at a destination it WOULD write, pre-painted, and the
#    row reads the paint back.  Tiled destinations use the #509 tile (re_tlb_[abc][0] = 0x8002 -> phys
#    0x20000); linear ones map phys page 0x30 in ONLY the array the arm reads (`sd 0x8000003000000000' to
#    CRIME_RE_LINEAR_A or _B), cleared again after use;
#  * a guard scoped to fewer destinations, sources, depths or masks than today's: S1 at tiled A/B/C, tiled A
#    COPY, LIN_A and LIN_B (at depth 8 with a full mask, so S4/S5 cannot hide the escape); S2 at every refused
#    source value {3,4,5,6,7} on a tiled fill, at 3 on a tiled COPY and on a linear fill; S3 and S4 at both
#    linear labels, S4 at every refused depth {16,32,64}; S5 at the reset default (BYTEMASK never written), at
#    0x0000ffff, 0xfffffffe, 0x7fffffff, at LIN_B, and across all 32 single-zero masks (one row);
#  * a guard grown to refuse legal transfers -- the ACCEPT side: a tiled fill and a tiled COPY at src C
#    (the S2 bound), linear fills at both labels and at the PROM's own mode 0x11 (DST_ECC), and tiled
#    fill/COPY with a non-full BYTEMASK (the linear restrictions must stay inside their branch);
#  * the latch: a missing announcement, a missing suppression, a `return' moved INSIDE the latch (the paint is
#    read after EVERY transfer, including the repeats), a bit shared between two new sites (one session drives
#    S1..S5 then S1 again and wants five distinct texts once each), and an assignment that clears an EXISTING
#    bit (SGIRE_W_TLBA_LEN, set first by one 4-byte store to CRIME_RE_TLB_A, must not announce again).
#
#  NOT CLAIMED: the rendering result of any ACCEPTED transfer beyond "it landed" (tiled fill: the word left the
#  paint; tiled COPY: the source's first byte; linear fill: 0x44444444) -- #509's own detector owns the tiled
#  colour channel; the `dst_y_step' and `default:' sibling arms (rows mtetlbflood, sgimtetlbdefault); START
#  honoured on a READ (filed); destination labels 3, 6, 7 (they reach the default arm, which writes nothing,
#  so a paint row there cannot see an S1/S2 escape -- disclosed, not rowed); masks with two or more zero bits
#  beyond the four rowed ones (sampled, not exhausted).
#
#  Clause (c), the null medium: an absent or non-emulator binary -- every session dies, every row that reads a
#  value or a survival reds (measured, not claimed: see the round's artifacts).
#
#  Usage:  sgi_mte_decline_probe.py <gxemul-binary> [label]
import os, sys, pty, select, time, re, tempfile

BIN   = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"

rows = []
def row(name, got, want, note=""):
    ok = (got == want)
    rows.append((name, ok))
    print("%-14s %-22s %-12s %-56s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok

OP_SW_T0_A3 = 0xace80000          # sw   $t0, 0($a3)
OP_SD_T0_A3 = 0xfce80000          # sd   $t0, 0($a3)
OP_LW_V0_AT = 0x8c220000          # lw   $v0, 0($at)
OP_B_SELF   = 0x1000ffff          # b    .
OP_NOP      = 0x00000000

CODE      = 0x80001000
SCRATCH   = 0xa0001800
LIVE_VAL  = 0x5a5a5a5a
SENTINEL  = 0xdeadbeef
DE_STATUS = 0xb5004000
DE_STAT   = "0x1e000000"          # CRIME_DE_STATUS: IDLE|SETUP_IDLE|PIXPIPE_IDLE|MTE_IDLE; RAM reads 0

DUMMY = os.path.join(tempfile.gettempdir(), "sgi_mte_decline_dummy.bin")
if not os.path.exists(DUMMY):
    with open(DUMMY, "wb") as f:
        f.write(b"\0" * 8)

#  CRIME base 0xb5000000 (KSEG1); offsets from src/include/thirdparty/crmfbreg.h.
RE_TLB_A, RE_TLB_B, RE_TLB_C = 0xb5001000, 0xb5001200, 0xb5001400
RE_LIN_A, RE_LIN_B           = 0xb5001700, 0xb5001780
MTE_MODE       = 0xb5003000
MTE_BYTEMASK   = 0xb5003008
MTE_BG         = 0xb5003018
MTE_SRC0       = 0xb5003020
MTE_DST0       = 0xb5003030
MTE_DST1_START = 0xb5003838       # CRIME_MTE_DST1 0x3038 | CRIME_DE_START 0x0800

#  MTE_MODE: DST_BUF 0x1c >> 2, SRC_BUF 0xe0 >> 5, DEPTH 0x300 >> 8 (depth = 8 << field), STIPPLE 0x400, COPY 0x800.
DST_A, DST_B, DST_C, DST_LA, DST_LB = 0 << 2, 1 << 2, 2 << 2, 4 << 2, 5 << 2
D8, D16, D32, D64 = 0x000, 0x100, 0x200, 0x300
STIPPLE, COPY, ECC = 0x400, 0x800, 0x001
def SRC(v): return v << 5

TILE      = 0x8002                # re_tlb_[abc][0]: bit 15 valid -> phys 0x20000 (the #509 tile)
TDEST     = 0xa0020000            # tiled pixel (0,0), KSEG1
LPAGE     = 0x80000030            # linear entry: valid | page 0x30
LDEST     = 0xa0030000            # linear destination, KSEG1 of phys 0x30000
LDST0, LDST1 = 0x00030000, 0x00030003
PAINT     = 0x99999999
BG_VAL    = 0x11223344
SRC_WORD  = 0x1a2b3c4d            # first byte < 0x80 (sgirebufshiftub), four distinct bytes
SRC_PIX   = 4 << 16               # SRC0: x = 4 bytes -> pixel 1 at depth 32

#  Each site's announcement.  The key phrase is HEAD's own text (the witness attributes on it); the suffix is the
#  decline's -- so a count of the SUFFIXED text counts declines, never a HEAD-style death message.
DECL = "transfer declined (once)"
KEY = {"S1": "unimplemented MTE_MODE_STIPPLE", "S2": "unimplemented SRC", "S3": "unimplemented MTE_MODE_COPY",
       "S4": "unimplemented MTE_DEPTH_x", "S5": "unimplemented MTE bytemask"}
TLBA_LEN_TEXT = "for CRIME_RE_TLB_A -- declined.  (once)"

def ntext(t, site):
    return len(re.findall(re.escape(KEY[site]) + r"[^\]\n]*" + re.escape(DECL), t))

def session(cmds, settle=1.5, spin=1.8):
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(BIN, [BIN, "-V", "-x", "-E", "sgi", "-e", "ip32", "-M", "64", "0x%x:" % CODE + DUMMY])
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
        if not rd(spin if i == len(cmds) - 1 else 0.22):
            alive = False; break
    try:
        os.write(fd, b"quit\n"); rd(0.4)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass
    return buf.replace("\r", ""), alive

class Sess(object):
    """One emulator session: a growing list of debugger commands, each check a labelled `lw' + `print v0'.
    Values come back IN ORDER; a check after the session ended reads 'died'."""
    def __init__(self):
        self.a = CODE; self.cmds = []; self.checks = []; self.reg = {}
    def _ops(self, ops):
        at = self.a; self.a += 4 * (len(ops) + 2) + 0x20
        put = ["put w 0x%x, 0x%08x" % (at + 4 * i, op) for i, op in enumerate(ops)]
        put += ["put w 0x%x, 0x%08x" % (at + 4 * len(ops), OP_B_SELF),
                "put w 0x%x, 0x%08x" % (at + 4 * len(ops) + 4, OP_NOP)]
        self.cmds += put + ["pc=0x%x" % at, "step %d" % len(ops)]
    def sw(self, addr, val):
        self.cmds += ["a3=0x%x" % addr, "t0=0x%x" % val]; self._ops([OP_SW_T0_A3])
    def sd(self, addr, val):
        self.cmds += ["a3=0x%x" % addr, "t0=0x%x" % val]; self._ops([OP_SD_T0_A3])
    def mte(self, addr, val, force=False):
        """An MTE register store, skipped when the register already holds the value (the transfer reads the
        registers, so a skipped store is the same machine state)."""
        if force or self.reg.get(addr) != val:
            self.sw(addr, val); self.reg[addr] = val
    def check(self, addr, label):
        self.cmds += ["at=0x%x" % addr, "v0=0x%x" % SENTINEL]; self._ops([OP_LW_V0_AT])
        self.cmds += ["print v0"]; self.checks.append(label)
    def go(self, mode, linear=False, bytemask=None, src0=None):
        if bytemask is not None:
            self.mte(MTE_BYTEMASK, bytemask)
        self.mte(MTE_MODE, mode)
        self.mte(MTE_BG, BG_VAL)
        if src0 is not None:
            self.mte(MTE_SRC0, src0)
        self.mte(MTE_DST0, LDST0 if linear else 0)
        self.sw(MTE_DST1_START, LDST1 if linear else 0)        # START: always stored, never skipped
    def run(self):
        t, alive = session(self.cmds)
        vals = re.findall(r"print\s+v0\s*\n\s*(0x[0-9a-f]+)", t)
        res = {}
        for i, lab in enumerate(self.checks):
            #  `lw' SIGN-EXTENDS: the paint 0x99999999 reads back as 0xffffffff99999999.  Compare the 32 bits the
            #  guest loaded.  (The first draft compared the whole register, so every `paint kept' row read
            #  "written" on the fixed build and every `landed' row was vacuous -- a paint that survived also
            #  differed from the 32-bit literal.  Measured 2026-10-17, probe_FIX_564.v1_signext.out.)
            res[lab] = ("0x%x" % (int(vals[i], 16) & 0xffffffff)) if i < len(vals) else "died"
        return t, alive, res

def tiles(s, a=True, b=False, c=False):
    if a: s.sd(RE_TLB_A, TILE << 48)
    if b: s.sd(RE_TLB_B, TILE << 48)
    if c: s.sd(RE_TLB_C, TILE << 48)

def lin_map(s, which):
    """Map phys page 0x30 in ONLY the named linear array; clear the other."""
    s.sd(RE_LIN_A, (LPAGE << 32) if which == "a" else 0)
    s.sd(RE_LIN_B, (LPAGE << 32) if which == "b" else 0)

P = "0x%x" % PAINT
def top(v):
    return v if not v.startswith("0x") else "0x%02x" % ((int(v, 16) >> 24) & 0xff)
def landed(v):
    return "died" if v == "died" else ("paint" if v == P else "landed")
def kept(v):
    return "died" if v == "died" else ("paint kept" if v == P else "written")

print("# sgi_mte_decline_probe -- binary=%s label=%s machine=sgi/ip32, %s" % (BIN, LABEL, time.strftime("%Y-%m-%d %H:%M:%S")))
print("%-14s %-22s %-12s %-56s %s" % ("row", "got", "want", "note", ""))

# ================================================================ controls
s = Sess(); s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "v")
t, alive, r = s.run()
row("live", r["v"], "0x%x" % LIVE_VAL, "RAM round-trip: the session and the CPU run")

s = Sess(); s.check(DE_STATUS, "v")
t, alive, r = s.run()
row("devsig", r["v"], DE_STAT, "CRIME_DE_STATUS: only the device answers this")

s = Sess(); s.mte(MTE_MODE, STIPPLE | D32); s.check(MTE_MODE, "v")
t, alive, r = s.run()
row("mode rt", r["v"], "0x%x" % (STIPPLE | D32), "an MTE register through the sgi_mte decode; no START")

# ================================================================ S1 STIPPLE: every destination
s = Sess(); tiles(s, a=True, b=True, c=True)
for lab, mode in (("a", DST_A | D32), ("b", DST_B | D32), ("c", DST_C | D32)):
    s.sw(TDEST, PAINT); s.go(STIPPLE | mode); s.check(TDEST, "t" + lab)
s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(STIPPLE | COPY | DST_A | SRC(0) | D32, src0=SRC_PIX); s.check(TDEST, "tcopy")
for lab in ("a", "b"):
    lin_map(s, lab); s.sw(LDEST, PAINT)
    s.go(STIPPLE | (DST_LA if lab == "a" else DST_LB) | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "l" + lab)
s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
t, alive, r = s.run()
row("stip a", kept(r["ta"]), "paint kept", "S1, tiled A fill at depth 32")
row("stip b", kept(r["tb"]), "paint kept", "S1, tiled B")
row("stip c", kept(r["tc"]), "paint kept", "S1, tiled C")
row("stip copy", kept(r["tcopy"]), "paint kept", "S1, tiled A COPY (the tiled COPY arm would run)")
row("stip lin a", kept(r["la"]), "paint kept", "S1, LIN_A depth 8 full mask (S3-S5 all pass)")
row("stip lin b", kept(r["lb"]), "paint kept", "S1, LIN_B depth 8 full mask")
row("stip surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "six refused transfers, then RAM")
row("stip once", ntext(t, "S1") if alive else "died", 1, "six refusals, one announcement")

# ================================================================ S2 src > MTE_TLB_C: the refused domain {3..7}
s = Sess(); tiles(s, a=True, c=True)
for v in (3, 4, 5, 6, 7):
    s.sw(TDEST, PAINT); s.go(SRC(v) | DST_A | D32); s.check(TDEST, "f%d" % v)
s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | SRC(3) | DST_A | D32, src0=SRC_PIX); s.check(TDEST, "copy3")
lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(SRC(3) | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lin3")
s.sw(TDEST, PAINT); s.go(SRC(2) | DST_A | D32); s.check(TDEST, "fillc")
s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | SRC(2) | DST_A | D32, src0=SRC_PIX); s.check(TDEST, "copyc")
s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
t, alive, r = s.run()
for v in (3, 4, 5, 6, 7):
    row("src %d" % v, kept(r["f%d" % v]), "paint kept", "S2, tiled A fill, src field %d" % v)
row("src 3 copy", kept(r["copy3"]), "paint kept", "S2's active side: a COPY from src 3")
row("src 3 lin", kept(r["lin3"]), "paint kept", "S2 at a linear destination")
row("src c fill", landed(r["fillc"]), "landed", "ACCEPT: src 2 = MTE_TLB_C, the bound")
row("src c copy", top(r["copyc"]), "0x1a", "ACCEPT: a COPY from TLB_C lands the source's first byte")
row("src surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "seven refused transfers, then RAM")
row("src once", ntext(t, "S2") if alive else "died", 1, "seven refusals, one announcement")

# ================================================================ S3 linear COPY, both labels
s = Sess()
for lab in ("a", "b"):
    lin_map(s, lab); s.sw(LDEST, PAINT)
    s.go(COPY | (DST_LA if lab == "a" else DST_LB) | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, lab)
s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
t, alive, r = s.run()
row("copy lin a", kept(r["a"]), "paint kept", "S3, LIN_A")
row("copy lin b", kept(r["b"]), "paint kept", "S3, LIN_B")
row("copy surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
row("copy once", ntext(t, "S3") if alive else "died", 1, "")

# ================================================================ S4 linear depth != 8: {16,32,64} x both labels
s = Sess()
for lab in ("a", "b"):
    lin_map(s, lab)
    for dn, dv in (("16", D16), ("32", D32), ("64", D64)):
        s.sw(LDEST, PAINT); s.go((DST_LA if lab == "a" else DST_LB) | dv, linear=True, bytemask=0xffffffff)
        s.check(LDEST, lab + dn)
s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
t, alive, r = s.run()
for lab in ("a", "b"):
    for dn in ("16", "32", "64"):
        row("depth %s %s" % (lab, dn), kept(r[lab + dn]), "paint kept", "S4, LIN_%s depth %s" % (lab.upper(), dn))
row("depth surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
row("depth once", ntext(t, "S4") if alive else "died", 1, "six refusals, one announcement")

# ================================================================ S5 bytemask: the reset default, in a session that never stores it
s = Sess(); lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True); s.check(LDEST, "v")
s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
t, alive, r = s.run()
row("mask unwritten", kept(r["v"]), "paint kept", "S5 at BYTEMASK's reset value 0, never stored")
row("mask unw surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")

# ================================================================ S5 bytemask: edges, LIN_B, and the 32 single-zero masks
s = Sess(); lin_map(s, "a")
for m in (0x0000ffff, 0xfffffffe, 0x7fffffff):
    s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=m); s.check(LDEST, "m%08x" % m)
s.sw(LDEST, PAINT)
for b in range(32):
    s.mte(MTE_BYTEMASK, 0xffffffff ^ (1 << b)); s.sw(MTE_DST1_START, LDST1)
s.check(LDEST, "sweep")
lin_map(s, "b"); s.sw(LDEST, PAINT); s.go(DST_LB | D8, linear=True, bytemask=0x0000ffff); s.check(LDEST, "linb")
s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
t, alive, r = s.run()
for m in (0x0000ffff, 0xfffffffe, 0x7fffffff):
    row("mask %08x" % m, kept(r["m%08x" % m]), "paint kept", "S5, LIN_A")
row("mask sweep", kept(r["sweep"]), "paint kept", "S5, all 32 single-zero masks, paint read once at the end")
row("mask lin b", kept(r["linb"]), "paint kept", "S5, LIN_B")
row("mask surv", "survived" if r["live"] == "0x%x" % LIVE_VAL else "died", "survived", "")
row("mask once", ntext(t, "S5") if alive else "died", 1, "thirty-six refusals, one announcement")

# ================================================================ ACCEPT: what must still land
s = Sess(); tiles(s, a=True)
lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "la")
lin_map(s, "b"); s.sw(LDEST, PAINT); s.go(DST_LB | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "lb")
lin_map(s, "a"); s.sw(LDEST, PAINT); s.go(ECC | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "ecc")
s.sw(TDEST, PAINT); s.go(DST_A | D32, bytemask=0x0000ffff); s.check(TDEST, "tmask")
s.sw(TDEST + 4, SRC_WORD); s.sw(TDEST, PAINT); s.go(COPY | DST_A | D32, bytemask=0x0000ffff, src0=SRC_PIX); s.check(TDEST, "tcopy")
t, alive, r = s.run()
row("lin fill a", r["la"], "0x44444444", "ACCEPT: LIN_A, depth 8, full mask -- BG's low byte")
row("lin fill b", r["lb"], "0x44444444", "ACCEPT: LIN_B")
row("lin fill ecc", r["ecc"], "0x44444444", "ACCEPT: the PROM's own linear mode 0x11 (DST_ECC)")
row("tile mask", landed(r["tmask"]), "landed", "ACCEPT: tiled fill with BYTEMASK 0x0000ffff")
row("tile copy mask", top(r["tcopy"]), "0x1a", "ACCEPT: tiled COPY with BYTEMASK 0x0000ffff")

# ================================================================ LATCH: an existing bit first, then S1..S5 and S1 again, in one session
s = Sess(); tiles(s, a=True)
s.sw(RE_TLB_A, 0)                                       # a 4-byte store: SGIRE_W_TLBA_LEN, announced once
s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "s1")
s.sw(TDEST, PAINT); s.go(SRC(3) | DST_A | D32); s.check(TDEST, "s2")
lin_map(s, "a")
s.sw(LDEST, PAINT); s.go(COPY | DST_LA | D8, linear=True, bytemask=0xffffffff); s.check(LDEST, "s3")
s.sw(LDEST, PAINT); s.go(DST_LA | D16, linear=True, bytemask=0xffffffff); s.check(LDEST, "s4")
s.sw(LDEST, PAINT); s.go(DST_LA | D8, linear=True, bytemask=0x0000ffff); s.check(LDEST, "s5")
tiles(s, a=True)
s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "s1again")
s.sw(RE_TLB_A, 0)                                       # the existing bit again: must NOT announce a second time
s.sw(SCRATCH, LIVE_VAL); s.check(SCRATCH, "live")
t, alive, r = s.run()
paints = [r[k] for k in ("s1", "s2", "s3", "s4", "s5", "s1again")]
row("latch paint", "all kept" if all(v == P for v in paints) else ("died" if "died" in paints else "written"),
    "all kept", "six refusals incl. a repeat of S1 after the latch is set")
row("latch texts", "/".join(str(ntext(t, k)) for k in ("S1", "S2", "S3", "S4", "S5")) if alive else "died",
    "1/1/1/1/1", "five distinct sites in one session: five bits, not one")
row("latch old bit", len(re.findall(re.escape(TLBA_LEN_TEXT), t)) if alive else "died", 1,
    "SGIRE_W_TLBA_LEN set before the new sites stays set after them")

# ================================================================ AFTER a decline: the engine still works and the status reads idle
s = Sess(); tiles(s, a=True)
s.sw(TDEST, PAINT); s.go(STIPPLE | DST_A | D32); s.check(TDEST, "decl")
s.sw(TDEST, PAINT); s.go(DST_A | D32); s.check(TDEST, "fill")
s.check(DE_STATUS, "stat")
t, alive, r = s.run()
row("after fill", landed(r["fill"]), "landed", "a legal fill after a declined one lands")
row("after status", r["stat"], DE_STAT, "CRIME_DE_STATUS after a decline")

ok = sum(1 for _, k in rows if k)
print("MTEDECL_RESULT=%d/%d" % (ok, len(rows)))
print("MTEDECL_DONE")
