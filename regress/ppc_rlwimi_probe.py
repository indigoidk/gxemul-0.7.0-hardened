#!/usr/bin/env python3
"""ppcrlwimiwidth -- RUNG-3 DETECTOR for X(rlwimi) width contamination and high-half insertion defects.

DEFECT.  src/cpus/cpu_ppc_instr.c, X(rlwimi):

    MODE_uint_t tmp = reg(ic->arg[0]), ra = reg(ic->arg[1]);
    uint32_t iword = ic->arg[2];
    int sh = (iword >> 11) & 31;
    int mb = (iword >> 6) & 31;
    int me = (iword >> 1) & 31;
    int rc = iword & 1;

    tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;

    for (;;) {
        uint64_t mask;
        mask = (uint64_t)1 << (31-mb);
        ra &= ~mask;
        ra |= (tmp & mask);
        if (mb == me)
            break;
        mb ++;
        if (mb == 32)
            mb = 0;
    }
    reg(ic->arg[1]) = ra;
    if (rc)
        update_cr0(cpu, ra);

THE DEFECT HAS TWO PARTS:
  (1) WIDTH CONTAMINATION:
      In 64-bit compilation, MODE_uint_t is uint64_t. When 1 <= SH <= 31,
      `tmp >> (32-sh)` performs a 64-bit right shift, pulling high-half source
      bits down into positions 0..31 of tmp, contaminating the rotated word.
      Siblings rlwinm and rlwnm cast to uint32_t first; rlwimi failed to do so.
  (2) MISSING HIGH-HALF INSERTION:
      ROTL32 rotates the low word duplicated into both halves (positions 0:31
      and 32:63). The architectural mask is MASK(MB+32, ME+32). When MB > ME,
      the mask wraps from bit 63 to bit 0, covering every bit position in 0..31
      (the entire high half). Therefore, when MB > ME, RA's high 32 bits MUST
      be replaced with the rotated low-word data. The unpatched code left the
      high half of RA untouched.

THE TWO-PART REPAIR:
  1. Narrow tmp on read:
     uint32_t tmp = (uint32_t)reg(ic->arg[0]);
  2. High-half replacement before the walk loop:
     if (mb > me)
         ra = (ra & 0xffffffffULL) | ((uint64_t)tmp << 32);

  *** THE CONDITIONAL MUST PRECEDE THE LOOP. *** The loop walks mb around to me,
  so after it mb == me and the guard would never fire.

ARCHITECTURE, PowerPC Book I v2.01:4310-4327 (rlwimi RTL and prose):
  n  <- SH
  r  <- ROTL32((RS)[32:63], n)
  m  <- MASK(MB+32, ME+32)
  RA <- (r & m) | ((RA) & ~m)

  MASK(x, y) is defined at Book I:578 as "1s in positions x through y (wrapping if x > y)".
  ROTL32 is defined at Book I:4008 / 4126 as rotating bits 32:63 duplicated into both halves.

CLAUSE (e) DISCLOSURE (what this instrument cannot see):
  (1) Model width vs mode width: the probe runs on `-E bareppc -M 64` (PPC970, 64-bit
      model, MSR[SF]=1). It cannot observe a 64-bit CPU operating in 32-bit mode (MSR[SF]=0),
      where `update_cr0` branching on `cpu->cd.ppc.bits == 64` compares 64 bits instead of
      32 bits (filed separately as ppccr0modewidth).
  (2) 32-bit CPU high-half truncation: on 32-bit CPUs (PPC603), registers are 32 bits, so
      high-half insertion is discarded by 32-bit register truncation.
  (3) Full OS boot rigs: no 64-bit PowerPC guest OS boot image exists in the tree; rung 3
      unmodified machine guest execution is the highest achievable rung.
  (4) The record form: `cr0 record form' checks that CR READ BACK, not CR0's value and not the
      destination's value in that session -- an edit that skips the insertion only when Rc=1 is
      not pinned (codex, 2026-09-12 adjudication; rldimi carries the same limit).
  (5) The `mb > me' bound: every named wrap row has MB > ME, so `>' versus `>=' is pinned ONLY by
      the census's MB == ME cells, (0,0) and (31,31) -- measured: the `>=' mutant scores 27/28 with
      `census wrong' its sole killer (artifacts/ppcrlwimiwidth/opus_pass2_20260912/rlwimi_RM_GE.log).

Sentinel: PPC_RLWIMI_PROBE_DONE (plus PPC_RLWIMI_RESULT=n/N, PPC_RLWIMI_CONTROL=OK|FAIL)
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: ppc_rlwimi_probe.py <gxemul> [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
#  The loader needs a 4-byte stub; it is private to this run (the witness shared
#  /tmp/ppc_rldimi_dummy.bin with the rldimi witness, so two concurrent runs raced on it).
_TMPDIR = tempfile.mkdtemp(prefix="ppc_rlwimi_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x10000
M64 = (1 << 64) - 1
SENT = 0x5A5A5A5A5A5A5A5A        # sentinel pre-seeded into destination registers
RS_ONES = M64                    # all-ones source
RS_VAL = 0xDEADBEEFCAFEF00D      # pattern source with differing halves
SRC = 3                          # rS is always r3; r3 is never a destination
DESTS = list(range(4, 30))       # r4..r29 -- 26 destinations per session

rows = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 18, name
    ok = (got == want)
    rows.append((name, ok))
    print("%-19s %-20s %-20s %-46s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


# ----------------------------------------------------------------- architecture
def rotl64(x, n):
    n &= 63
    return ((x << n) | (x >> (64 - n))) & M64 if n else x & M64


def mask_b_63(b):
    """MASK(b,63), big-endian bit numbering = the low (64-b) bits."""
    assert 0 <= b <= 63
    return (1 << (64 - b)) - 1


def mask_0_e(e):
    """MASK(0,e), big-endian = the high (e+1) bits."""
    assert 0 <= e <= 63
    return (((1 << (e + 1)) - 1) << (63 - e)) & M64


def mask_range(b, e):
    """MASK(b,e), the architecture's own wrapping mask generator (Book I:578, PEM:6879)."""
    assert 0 <= b <= 63 and 0 <= e <= 63
    m = (mask_b_63(b) & mask_0_e(e)) if b <= e else (mask_b_63(b) | mask_0_e(e))
    assert m != 0, "MASK(%d,%d) came out all-zero, which architecture forbids" % (b, e)
    return m


def rotl32(x, n):
    """ROTL[32] per Book I:4008 -- two copies of (RS)[32:63], then rotate."""
    lo = x & 0xFFFFFFFF
    n &= 31
    r32 = ((lo << n) | (lo >> (32 - n))) & 0xFFFFFFFF if n else lo
    return (r32 << 32) | r32


def mask32(mb, me):
    """MASK(MB+32, ME+32) at 64 bits (Book I:4125, 4310)."""
    assert 0 <= mb <= 31 and 0 <= me <= 31
    return mask_range(mb + 32, me + 32)


def want_rlwimi(rs_val, ra_val, sh, mb, me):
    """Architectural rlwimi result per Book I:4310."""
    m = mask32(mb, me)
    return (rotl32(rs_val, sh) & m) | (ra_val & (~m & M64))


def want_rlwinm(rs_val, sh, mb, me):
    """Architectural rlwinm result per Book I:4125."""
    m = mask32(mb, me)
    return rotl32(rs_val, sh) & m


# -------------------------------------------------------------------- encodings
def enc_m(op, rs, ra, sh, mb, me, rc=0):
    """Opcode 20 (rlwimi) / 21 (rlwinm) / 23 (rlwnm). Book I format M."""
    assert 0 <= op <= 63 and 0 <= rs <= 31 and 0 <= ra <= 31
    assert 0 <= sh <= 31 and 0 <= mb <= 31 and 0 <= me <= 31 and 0 <= rc <= 1
    return ((op << 26) | (rs << 21) | (ra << 16) | (sh << 11)
            | (mb << 6) | (me << 1) | rc) & 0xFFFFFFFF


def RLWIMI(ra, rs, sh, mb, me, rc=0):
    return enc_m(20, rs, ra, sh, mb, me, rc)


def RLWINM(ra, rs, sh, mb, me, rc=0):
    return enc_m(21, rs, ra, sh, mb, me, rc)


def LI(rd, simm):
    return ((14 << 26) | (rd << 21) | (0 << 16) | (simm & 0xFFFF)) & 0xFFFFFFFF


def ORI(ra, rs, imm):
    return ((24 << 26) | (rs << 21) | (ra << 16) | (imm & 0xFFFF)) & 0xFFFFFFFF


NOP = ORI(0, 0, 0)


# ---------------------------------------------------------------------- sessions
def session(setup, insns, timeout=90, machine="bareppc", cpu=None):
    """Place `insns' at CODE, seed registers, step exactly len(insns), dump regs."""
    cmds = list(setup)
    for i, w in enumerate(insns):
        cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    if insns:
        cmds.append("unassemble 0x%x 0x%x" % (CODE, CODE + 4 * len(insns)))
    cmds.append("pc=0x%x" % CODE)
    if insns:
        cmds.append("step %d" % len(insns))
    cmds.append("reg")
    argv = [BIN, "-V", "-x", "-E", machine, "-M", "64"]
    if cpu:
        argv += ["-C", cpu]
    argv += ["0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds + ["quit"]) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        out = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        return {}, [], out, "TIMEOUT"
    t = p.stdout.decode("latin-1", "replace").replace("\r", "")
    rc = p.returncode
    how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    idx = t.rfind("GXemul> reg")
    regs = {}
    if idx >= 0:
        for m in re.finditer(r"\br(\d\d) = (0x[0-9a-fA-F]+)", t[idx:]):
            regs[int(m.group(1))] = int(m.group(2), 16)
        m_cr = re.search(r"\bcr\s*=\s*(0x[0-9a-fA-F]+)", t[idx:])
        if m_cr:
            regs["cr"] = int(m_cr.group(1), 16)
    dis = []
    di = t.find("GXemul> unassemble")
    if di >= 0:
        seg = t[di:t.find("GXemul> pc=", di) if t.find("GXemul> pc=", di) > 0
                else len(t)]
        for m in re.finditer(r"^[0-9a-f]{16}: ([0-9a-f]{8})\s*(?:<- )?(\S+)"
                             r"(?:\t(\S+))?", seg, re.M):
            dis.append((int(m.group(1), 16), m.group(2), m.group(3) or ""))
    return regs, dis, t, how


def seed(pairs):
    return ["r%d=0x%x" % (r, v) for r, v in pairs]


print("ppcrlwimiwidth RUNG-3 DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E bareppc -M 64 (UNMODIFIED in-tree; MACHINE_DEFAULT_CPU=PPC970, 64-bit)")
print("wants derived from PowerPC Book I v2.01:4310 (rlwimi)")
print("%-19s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()
disasm_checked = 0
disasm_ok = 0

# ============================================================ CONTROL SESSION ==
ctl_insns = [
    LI(9, 0x1234),                       # liveness
    NOP,                                 # seed-holds probe steps over this
    RLWINM(4, SRC, 0, 0, 31),            # rlwinm r4,r3,0,0,31 -- sibling control
]
ctl_setup = seed([(SRC, RS_VAL), (30, SENT)] + [(r, SENT) for r in DESTS])
regs, dis, T, how = session(ctl_setup, ctl_insns)

row("session", how, "exit0", "the control session ran to `quit'")
row("live", hex(regs.get(9, -1)), hex(0x1234),
    "li r9,0x1234 -- guest executes and readback works")
row("seed holds", hex(regs.get(30, -1)), hex(SENT),
    "r30 seeded, never destination: proves write is real")
row("src intact", hex(regs.get(SRC, -1)), hex(RS_VAL),
    "rS is unchanged by instructions")

want_dis = ["li", "nop", "rlwinm"]
want_ops = ["r9,4660", "", "r4,r3,0,0,31"]
got_pairs = [(m, o) for _, m, o in dis]
disasm_checked += len(want_dis)
disasm_ok += sum(1 for i, (m, o) in enumerate(got_pairs[:len(want_dis)])
                 if m == want_dis[i] and o == want_ops[i])
row("disasm xcheck", "%d/%d" % (disasm_ok, disasm_checked), "3/3",
    "tree's disassembler agrees with encoder")
row("ctl rlwinm", hex(regs.get(4, -1)), hex(want_rlwinm(RS_VAL, 0, 0, 31)),
    "sibling control: rlwinm low word extract")

# ================================================ NEGATIVE APPARATUS CONTROL ==
nregs, _, nT, nhow = session(seed([(9, SENT)]), [LI(9, 0x1234)],
                             machine="nosuchmachine", timeout=60)
row("neg apparatus", "%s/%s" % (nhow, hex(nregs.get(9, -1))), "exit1/-0x1",
    "bogus machine -> no guest -> live fails")

# ============================================ REACHABILITY CONTROL (32-bit) ===
b32regs, _, b32T, b32how = session(
    seed([(SRC, RS_VAL), (4, SENT), (9, SENT)]),
    [LI(9, 0x1234), RLWIMI(4, SRC, 8, 0, 31)], timeout=60, machine="bareppc",
    cpu="PPC603")
row("bits32 live", hex(b32regs.get(9, -1)), hex(0x1234),
    "PPC603 (32-bit): guest still runs li")
# On 32-bit CPU, rlwimi is a valid instruction (does not trap to bad)
row("bits32 rlwimi", hex(b32regs.get(4, -1) & 0xFFFFFFFF),
    hex(want_rlwimi(RS_VAL, SENT, 8, 0, 31) & 0xFFFFFFFF),
    "PPC603 (32-bit): rlwimi executes cleanly")

# ==================================================== CORE DIRECTION PROBES ===
# Session 1: Non-wrapping encodings (MB <= ME), rS has differing halves
# Defect 1 symptom: width contamination when SH > 0 (drags RS high-half bits down)
s1_setup = seed([(SRC, RS_VAL)] + [(r, 0) for r in DESTS])
s1_insns = [
    RLWIMI(4, SRC, 0, 0, 31),    # SH=0, MB=0, ME=31 (full word; passes pre-fix because SH=0)
    RLWIMI(5, SRC, 8, 0, 15),    # SH=8, MB=0, ME=15 (width contamination into top 16 bits of word)
    RLWIMI(6, SRC, 16, 8, 23),   # SH=16, MB=8, ME=23 (width contamination into middle bits)
    RLWIMI(7, SRC, 4, 16, 31),   # SH=4, MB=16, ME=31 (width contamination into lower bits)
]
s1_regs, s1_dis, s1_T, s1_how = session(s1_setup, s1_insns)
want_s1_dis = ["rlwimi", "rlwimi", "rlwimi", "rlwimi"]
want_s1_ops = ["r4,r3,0,0,31", "r5,r3,8,0,15", "r6,r3,16,8,23", "r7,r3,4,16,31"]
disasm_checked += len(want_s1_dis)
disasm_ok += sum(1 for i, (_, m, o) in enumerate(s1_dis[:len(want_s1_dis)])
                 if m == want_s1_dis[i] and o == want_s1_ops[i])

row("nowrap sh0", hex(s1_regs.get(4, -1)), hex(want_rlwimi(RS_VAL, 0, 0, 0, 31)),
    "SH=0, MB<=ME: full 32-bit word, unaffected by shift")
row("nowrap sh8 mb0", hex(s1_regs.get(5, -1)), hex(want_rlwimi(RS_VAL, 0, 8, 0, 15)),
    "SH=8, MB<=ME: width contamination corrupts low word")
row("nowrap sh16 mb8", hex(s1_regs.get(6, -1)), hex(want_rlwimi(RS_VAL, 0, 16, 8, 23)),
    "SH=16, MB<=ME: width contamination into middle bits")
row("nowrap sh4 mb16", hex(s1_regs.get(7, -1)), hex(want_rlwimi(RS_VAL, 0, 4, 16, 31)),
    "SH=4, MB<=ME: width contamination into low bits")

# Session 2: Wrapping encodings (MB > ME)
# Defect 2 symptom: high-half replacement omitted (leaves RA high half untouched)
# Subcase A: The mutant from brief: r3=0xaaaaaaaa0000000f, r4=0x5a5a5a5a5a5a5a5a, sh=0, mb=31, me=0
# rlwimi r4,r3,0,31,0 -> want 0x0000000f5a5a5a5b, mutant 0x5a5a5a5a5a5a5a5b
MUT_RS = 0xAAAAAAAA0000000F
s2_setup = seed([(SRC, MUT_RS), (4, SENT), (5, SENT), (6, SENT), (7, SENT)])
s2_insns = [
    RLWIMI(4, SRC, 0, 31, 0),    # Brief mutant: SH=0, MB=31, ME=0 (word 0x506407c0)
    RLWIMI(5, SRC, 0, 24, 8),    # SH=0, MB=24, ME=8 (wrapping, SH=0)
    RLWIMI(6, SRC, 8, 20, 10),   # SH=8, MB=20, ME=10 (wrapping, SH>0: both defects active!)
    RLWIMI(7, SRC, 16, 28, 4),   # SH=16, MB=28, ME=4 (wrapping, SH>0: both defects active!)
]
s2_regs, s2_dis, s2_T, s2_how = session(s2_setup, s2_insns)
want_s2_dis = ["rlwimi", "rlwimi", "rlwimi", "rlwimi"]
want_s2_ops = ["r4,r3,0,31,0", "r5,r3,0,24,8", "r6,r3,8,20,10", "r7,r3,16,28,4"]
disasm_checked += len(want_s2_dis)
disasm_ok += sum(1 for i, (_, m, o) in enumerate(s2_dis[:len(want_s2_dis)])
                 if m == want_s2_dis[i] and o == want_s2_ops[i])

row("wrap mutant", hex(s2_regs.get(4, -1)), hex(want_rlwimi(MUT_RS, SENT, 0, 31, 0)),
    "brief mutant: rlwimi r4,r3,0,31,0 -> high word 0x0000000f")
row("wrap sh0 mb24", hex(s2_regs.get(5, -1)), hex(want_rlwimi(MUT_RS, SENT, 0, 24, 8)),
    "SH=0, MB>ME: high half must be replaced with rotated low word")
row("wrap sh8 mb20", hex(s2_regs.get(6, -1)), hex(want_rlwimi(MUT_RS, SENT, 8, 20, 10)),
    "SH=8, MB>ME: both defects active (width contam + high half)")
row("wrap sh16 mb28", hex(s2_regs.get(7, -1)), hex(want_rlwimi(MUT_RS, SENT, 16, 28, 4)),
    "SH=16, MB>ME: both defects active (width contam + high half)")

# Session 3: Destination preservation with structured data and seeded rA
s3_setup = seed([(SRC, RS_VAL)] + [(r, SENT) for r in DESTS])
s3_insns = [
    RLWIMI(4, SRC, 8, 0, 15),    # nowrap: preserve low 16 bits of low word + all high half
    RLWIMI(5, SRC, 0, 24, 8),    # wrap: preserve unmasked bits 9..23 of low word, replace high half
    RLWIMI(6, SRC, 0, 1, 0),     # wrap: full word boundary wrap (bits 1..31 and 0)
]
s3_regs, s3_dis, s3_T, s3_how = session(s3_setup, s3_insns)
want_s3_dis = ["rlwimi", "rlwimi", "rlwimi"]
want_s3_ops = ["r4,r3,8,0,15", "r5,r3,0,24,8", "r6,r3,0,1,0"]
disasm_checked += len(want_s3_dis)
disasm_ok += sum(1 for i, (_, m, o) in enumerate(s3_dis[:len(want_s3_dis)])
                 if m == want_s3_dis[i] and o == want_s3_ops[i])

row("pres nowrap", hex(s3_regs.get(4, -1)), hex(want_rlwimi(RS_VAL, SENT, 8, 0, 15)),
    "preserve unmasked destination bits in low and high words")
row("pres wrap", hex(s3_regs.get(5, -1)), hex(want_rlwimi(RS_VAL, SENT, 0, 24, 8)),
    "preserve unmasked bits in low word, replace high half")
row("wrap fullword", hex(s3_regs.get(6, -1)), hex(want_rlwimi(RS_VAL, SENT, 0, 1, 0)),
    "wrap fullword boundary: replace entire high half + all 32 low bits")

# Session 4: Register Aliasing (RA == RS)
# Test Question 2: Does RA == RS behave differently?
# r4 initialized to RS_VAL (differing halves: 0xDEADBEEFCAFEF00D).
# When RA == RS, r4 is both source and destination.
s4_setup = seed([(4, RS_VAL), (5, RS_VAL), (6, RS_VAL)])
s4_insns = [
    RLWIMI(4, 4, 8, 0, 15),     # alias nowrap: SH=8, MB<=ME -> width contamination on self
    RLWIMI(5, 5, 0, 31, 0),     # alias wrap: SH=0, MB>ME -> high half replacement on self
    RLWIMI(6, 6, 4, 20, 10),    # alias both: SH=4, MB>ME -> both defects on self
]
s4_regs, s4_dis, s4_T, s4_how = session(s4_setup, s4_insns)
want_s4_dis = ["rlwimi", "rlwimi", "rlwimi"]
want_s4_ops = ["r4,r4,8,0,15", "r5,r5,0,31,0", "r6,r6,4,20,10"]
disasm_checked += len(want_s4_dis)
disasm_ok += sum(1 for i, (_, m, o) in enumerate(s4_dis[:len(want_s4_dis)])
                 if m == want_s4_dis[i] and o == want_s4_ops[i])

row("alias nowrap", hex(s4_regs.get(4, -1)), hex(want_rlwimi(RS_VAL, RS_VAL, 8, 0, 15)),
    "RA==RS nowrap: self-insertion with SH=8")
row("alias wrap", hex(s4_regs.get(5, -1)), hex(want_rlwimi(RS_VAL, RS_VAL, 0, 31, 0)),
    "RA==RS wrap: self-insertion replacing high half")
row("alias both", hex(s4_regs.get(6, -1)), hex(want_rlwimi(RS_VAL, RS_VAL, 4, 20, 10)),
    "RA==RS both: self-insertion with SH=4, MB>ME")

# ========================================================= CR0 RECORD FORM =====
# rlwimi. with Rc=1
cr_setup = seed([(SRC, RS_VAL), (4, SENT)])
cr_insns = [
    RLWIMI(4, SRC, 8, 0, 15, rc=1),
]
cr_regs, cr_dis, cr_T, cr_how = session(cr_setup, cr_insns)
row("cr0 record form", "exit0" if "cr" in cr_regs else "no-cr", "exit0",
    "rlwimi. executes with Rc=1 and dumps CR")

# ==================================================== COMPREHENSIVE CENSUS =====
# Sweep structured combinations across (SH, MB, ME) space:
# - Quadrant 1: SH=0, MB<=ME (non-wrapping, zero shift)
# - Quadrant 2: SH in {1, 8, 16, 31}, MB<=ME (non-wrapping, shift > 0: width contamination)
# - Quadrant 3: SH=0, MB>ME (wrapping, zero shift: missing high-half)
# - Quadrant 4: SH in {1, 8, 16, 31}, MB>ME (wrapping, shift > 0: both defects)
census_combos = []
# Fixed representative (MB, ME) pairs:
mb_me_nowrap = [(0, 31), (0, 15), (8, 23), (16, 31), (10, 20), (0, 0), (31, 31)]
mb_me_wrap = [(31, 0), (24, 8), (20, 10), (28, 4), (1, 0), (31, 30), (16, 8)]

for sh_val in [0, 1, 8, 16, 31]:
    for mb, me in mb_me_nowrap:
        census_combos.append((sh_val, mb, me))
    for mb, me in mb_me_wrap:
        census_combos.append((sh_val, mb, me))

# Add diagonal and boundary sweeps:
for k in range(32):
    census_combos.append((k, k, (31 - k)))
    census_combos.append((k, (31 - k), k))

seen = set()
uniq_census = []
for c in census_combos:
    if c not in seen:
        seen.add(c)
        uniq_census.append(c)

census_fail = 0
census_zero = 0
census_run = 0

for base in range(0, len(uniq_census), len(DESTS)):
    chunk = uniq_census[base:base + len(DESTS)]
    insns = [RLWIMI(DESTS[i], SRC, sh, mb, me) for i, (sh, mb, me) in enumerate(chunk)]
    st = seed([(SRC, RS_VAL)] + [(r, SENT) for r in DESTS])
    cregs, cdis, cT, chow = session(st, insns)
    if chow != "exit0":
        print("CENSUS SESSION ABORTED how=%s at base=%d" % (chow, base))
        break
    for i, (sh, mb, me) in enumerate(chunk):
        disasm_checked += 1
        if i < len(cdis) and cdis[i][1] == "rlwimi" and \
           cdis[i][2] == "r%d,r%d,%d,%d,%d" % (DESTS[i], SRC, sh, mb, me):
            disasm_ok += 1
    for i, (sh, mb, me) in enumerate(chunk):
        census_run += 1
        got = cregs.get(DESTS[i], None)
        exp = want_rlwimi(RS_VAL, SENT, sh, mb, me)
        if got != exp:
            census_fail += 1
        if got == 0:
            census_zero += 1

#  Both wants are LITERALS (measured: killtable_20260911/probe_BASE.raw, 146/146 and 129).  They were
#  `len(uniq_census)' and `disasm_checked' -- derived from the very lists they count, so a census
#  shrunk by an edit passed both rows (codex, promotion design 2026-09-12).  146 = 3+4+4+3+3+129.
row("disasm total", "%d/%d" % (disasm_ok, disasm_checked), "146/146",
    "every placed word re-read by disassembler")
row("census run", census_run, 129,
    "(SH,MB,ME) cells driven across sweeps and diagonals")
row("census wrong", census_fail, 0,
    "cells differing from architectural result (0 after fix)")
row("census zero", census_zero, 0,
    "cells returning zero (0 after fix)")

# ================================================================ SCORE + DONE
npass = sum(1 for _, ok in rows if ok)
print("")
print("SCORE %d/%d  elapsed=%.1fs  binary=%s  label=%s"
      % (npass, len(rows), time.time() - t0, BIN, LABEL))
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
#  CONTROL = the rows that prove the probe measured: green on the fix AND on the committed build.
#  They are NOT green on every mutant, and this comment said they were until the 2026-09-12
#  adjudication pass (codex) -- joint tables 2 and 3 (killtable2_20260912/, killtable3_20260912/) show
#  CONTROL=FAIL on R_REV_COND (`nowrap sh0') and R_NULL (`bits32 rlwimi', `nowrap sh0'): a mutant that
#  breaks the target instruction itself reds its target-instruction control, which is the purpose.
#  So CONTROL=OK certifies the apparatus, never that a leg is harmless.
#  A missing name reads False -- a renamed control fails loudly rather than dropping out.
#  `nowrap sh0' is the TARGET-INSTRUCTION control: rlwimi at SH=0, MB<=ME is correct on the
#  committed build, so it proves rlwimi itself wrote a register -- `live' proves only `li'
#  (codex promotion review 2026-09-12: without it a no-op rlwimi still read CONTROL=OK).
CONTROL_ROWS = ("session", "live", "seed holds", "src intact", "disasm xcheck", "ctl rlwinm",
                "neg apparatus", "bits32 live", "bits32 rlwimi", "cr0 record form",
                "disasm total", "census run", "nowrap sh0")
_status = dict(rows)
control_ok = all(_status.get(n, False) for n in CONTROL_ROWS)
try:
    os.remove(DUMMY)
    os.rmdir(_TMPDIR)
except OSError:
    pass
print("PPC_RLWIMI_RESULT=%d/%d" % (npass, len(rows)))
print("PPC_RLWIMI_CONTROL=%s" % ("OK" if control_ok else "FAIL"))
print("PPC_RLWIMI_PROBE_DONE")
sys.exit(0 if control_ok and npass == len(rows) else 1)
