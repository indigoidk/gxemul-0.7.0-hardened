#!/usr/bin/env python3
"""ppcrldimimask -- RUNG-3 DETECTOR for X(rldimi) mask bounds and wrapping defects.

DEFECT.  src/cpus/cpu_ppc_instr.c, X(rldimi):

    uint32_t iw = ic->arg[0];
    int rs = (iw >> 21) & 31, ra = (iw >> 16) & 31;
    int sh = ((iw >> 11) & 31) | ((iw & 2) << 4);
    int mb = ((iw >> 6) & 31) | (iw & 0x20);
    int rc = ic->arg[0] & 1;
    int m;
    uint64_t tmp, s = cpu->cd.ppc.gpr[rs];
    while (sh-- != 0) { ... }
    m = mb; tmp = 0;
    do {
        tmp |= ((uint64_t)1 << (63-m));
        m ++;
    } while (m != 63 - sh);
    cpu->cd.ppc.gpr[ra] &= ~tmp;
    cpu->cd.ppc.gpr[ra] |= (tmp & s);

THE DEFECT HAS TWO DIRECTIONS:
  (1) The rotate loop `while (sh-- != 0)` post-decrements, leaving `sh == -1` on exit
      for every SH (including SH=0).
  (2) The termination test `m != 63 - sh` is therefore evaluated with `sh == -1`,
      becoming `m != 64` always. The mask generated is always MB..63 instead of MB..63-SH.

  Consequences on two classes of encodings:
  - Non-wrapping (MB <= 63-SH): the mask fails to stop at 63-SH and runs all the way
    to 63, OVERWRITING the low SH bits of destination RA that must be preserved.
  - Wrapping (MB > 63-SH): the mask stops at bit 63 and OMITS the required insertion
    into positions 0..63-SH, leaving those destination bits unchanged.

THE FOUR-EDIT REPAIR:
  1. Save SH in a separate variable: `int m, n = sh;`
  2. Consume the copy in the rotate loop: `while (n-- != 0)`
  3. Circular increment in the mask loop: `m = (m + 1) & 63;`
  4. Compare against successor modulo 64: `while (m != ((64 - sh) & 63));`

A partial repair saving SH but using non-wrapping `m++` and `m != 64 - sh` hits
`(uint64_t)1 << -1` at MB=40, SH=40 (undefined behaviour in C).

ARCHITECTURE, PowerPC Book I v2.01:4315-4327 (rldimi RTL and prose):
  n  <- sh[5] || sh[0:4]
  r  <- ROTL64((RS), n)
  b  <- mb[5] || mb[0:4]
  m  <- MASK(b, ~n)               where ~n on 6-bit field is 63-SH
  RA <- (r & m) | ((RA) & ~m)

  MASK(x, y) is defined at Book I:578 as "1s in positions x through y (wrapping if x > y)".
  PEM:6882 and Book I:4031 confirm "It is not possible to specify an all-zero mask."

CLAUSE (e) DISCLOSURE (what this instrument cannot see):
  (1) Model width vs mode width: the probe runs on `-E bareppc -M 64` (PPC970, 64-bit
      model, MSR[SF]=1). It cannot observe a 64-bit CPU operating in 32-bit mode (MSR[SF]=0),
      where `update_cr0` branching on `cpu->cd.ppc.bits == 64` would compare 64 bits instead
      of 32 bits (filed separately as ppccr0modewidth).
  (2) Unimplemented instructions: `rldic` (XO=2), `rldcl` (XO=8), `rldcr` (XO=9) are not
      implemented in the tree's decoder (`goto bad`) and cannot be driven here.
  (3) Full OS boot rigs: no 64-bit PowerPC guest OS boot image exists in the tree; rung 3
      unmodified machine guest execution is the highest achievable rung.

SHIPPED CONTRACT: 29 rows; 495 distinct census cells.  The census uses an all-ones source and
does not test the rotate amount independently of the mask bounds -- the pattern rows do, at
exactly three rotate amounts (SH 8, 24, 40: `pres nowrap', `full rot', `pres wrap'), so an edit
keyed on one other SH value is NOT pinned.  `full rot' is the one full-width mask from a patterned
source; `alias rs=ra' is the one rA == rS row.  The CR row checks readback PRESENCE only; CR0 value
semantics are not covered.  No rlwimi rows here.

Sentinel: PPC_RLDIMI_PROBE_DONE (plus PPC_RLDIMI_RESULT=n/N, PPC_RLDIMI_CONTROL=OK|FAIL)
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: ppc_rldimi_probe.py <gxemul> [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
#  The loader needs a 4-byte stub; it is private to this run (the witnesses shared one /tmp path).
_TMPDIR = tempfile.mkdtemp(prefix="ppc_rldimi_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x10000
M64 = (1 << 64) - 1
SENT = 0x5A5A5A5A5A5A5A5A        # sentinel pre-seeded into destination registers
RS_ONES = M64                    # all-ones source: makes every mask window observable
RS_VAL = 0xDEADBEEFCAFEF00D      # pattern source
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


def want_rldimi(rs_val, ra_val, sh, mb):
    """Architectural rldimi result per Book I:4315."""
    m = mask_range(mb, (63 - sh) & 63)
    return (rotl64(rs_val, sh) & m) | (ra_val & (~m & M64))


def want_rldicl(rs_val, sh, mb):
    return rotl64(rs_val, sh) & mask_b_63(mb)


def want_rldicr(rs_val, sh, me):
    return rotl64(rs_val, sh) & mask_0_e(me)


# -------------------------------------------------------------------- encodings
def enc_md(xo, rs, ra, sh, mbe, rc=0):
    """opcode 30 (rldicl/rldicr/rldimi). Book I format MD."""
    assert 0 <= sh <= 63 and 0 <= mbe <= 63 and 0 <= xo <= 7
    return ((30 << 26) | (rs << 21) | (ra << 16) | ((sh & 31) << 11)
            | ((mbe & 31) << 6) | (((mbe >> 5) & 1) << 5) | (xo << 2)
            | (((sh >> 5) & 1) << 1) | rc) & 0xFFFFFFFF


def RLDICL(ra, rs, sh, mb, rc=0):
    return enc_md(0, rs, ra, sh, mb, rc)


def RLDICR(ra, rs, sh, me, rc=0):
    return enc_md(1, rs, ra, sh, me, rc)


def RLDIMI(ra, rs, sh, mb, rc=0):
    return enc_md(3, rs, ra, sh, mb, rc)


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


print("ppcrldimimask RUNG-3 DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E bareppc -M 64 (UNMODIFIED in-tree; MACHINE_DEFAULT_CPU=PPC970, 64-bit)")
print("wants derived from PowerPC Book I v2.01:4315 (rldimi)")
print("%-19s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()
disasm_checked = 0
disasm_ok = 0

# ============================================================ CONTROL SESSION ==
ctl_insns = [
    LI(9, 0x1234),                       # liveness
    NOP,                                 # seed-holds probe steps over this
    RLDICL(4, SRC, 0, 32),               # clrldi r4,r3,32 -- sibling control
    RLDICR(5, SRC, 0, 31),               # sibling control
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

want_dis = ["li", "nop", "rldicl", "rldicr"]
want_ops = ["r9,4660", "", "r4,r3,0,32", "r5,r3,0,31"]
got_pairs = [(m, o) for _, m, o in dis]
disasm_checked += len(want_dis)
disasm_ok += sum(1 for i, (m, o) in enumerate(got_pairs[:len(want_dis)])
                 if m == want_dis[i] and o == want_ops[i])
row("disasm xcheck", "%d/%d" % (disasm_ok, disasm_checked), "4/4",
    "tree's disassembler agrees with encoder")
row("ctl rldicl", hex(regs.get(4, -1)), hex(want_rldicl(RS_VAL, 0, 32)),
    "sibling control: rldicl zero-extend")
row("ctl rldicr", hex(regs.get(5, -1)), hex(want_rldicr(RS_VAL, 0, 31)),
    "sibling control: rldicr extract")

# ================================================ NEGATIVE APPARATUS CONTROL ==
nregs, _, nT, nhow = session(seed([(9, SENT)]), [LI(9, 0x1234)],
                             machine="nosuchmachine", timeout=60)
row("neg apparatus", "%s/%s" % (nhow, hex(nregs.get(9, -1))), "exit1/-0x1",
    "bogus machine -> no guest -> live fails")

# ============================================ REACHABILITY CONTROL (32-bit) ===
b32regs, _, b32T, b32how = session(
    seed([(SRC, RS_VAL), (4, SENT), (9, SENT)]),
    [LI(9, 0x1234), RLDIMI(4, SRC, 8, 0)], timeout=60, machine="bareppc",
    cpu="PPC603")
row("bits32 live", hex(b32regs.get(9, -1)), hex(0x1234),
    "PPC603 (32-bit): guest still runs li")
row("bits32 rld bad", "TODO" if "TODO: rld" in b32T else "no-msg", "TODO",
    "decoder sends rld* to bad on 32-bit CPU")

# ==================================================== CORE DIRECTION PROBES ===
# Session 1: Non-wrapping encodings (MB <= 63-SH), rA initialized to 0, rS = ~0
# Defect symptom: overwrites low SH bits (runs to bit 63 instead of 63-SH)
s1_setup = seed([(SRC, RS_ONES)] + [(r, 0) for r in DESTS])
s1_insns = [
    RLDIMI(4, SRC, 8, 0),        # SH=8, MB=0 -> mask 0..55; defect gives 0..63
    RLDIMI(5, SRC, 32, 0),       # SH=32, MB=0 -> mask 0..31; defect gives 0..63
    RLDIMI(6, SRC, 0, 0),        # SH=0, MB=0 -> mask 0..63 (coincidental agree)
    RLDIMI(7, SRC, 16, 16),      # SH=16, MB=16 -> mask 16..47; defect gives 16..63
    RLDIMI(8, SRC, 0, 63),       # SH=0, MB=63 -> mask 63..63 (singleton bit 63)
]
s1_regs, s1_dis, s1_T, s1_how = session(s1_setup, s1_insns)
want_s1_dis = ["rldimi", "rldimi", "rldimi", "rldimi", "rldimi"]
want_s1_ops = ["r4,r3,8,0", "r5,r3,32,0", "r6,r3,0,0", "r7,r3,16,16", "r8,r3,0,63"]
disasm_checked += len(want_s1_dis)
disasm_ok += sum(1 for i, (_, m, o) in enumerate(s1_dis[:len(want_s1_dis)])
                 if m == want_s1_dis[i] and o == want_s1_ops[i])

row("nowrap sh8 mb0", hex(s1_regs.get(4, -1)), hex(want_rldimi(RS_ONES, 0, 8, 0)),
    "MB<=63-SH: mask must stop at bit 55")
row("nowrap sh32 mb0", hex(s1_regs.get(5, -1)), hex(want_rldimi(RS_ONES, 0, 32, 0)),
    "MB<=63-SH: mask must stop at bit 31")
row("nowrap sh0 mb0", hex(s1_regs.get(6, -1)), hex(want_rldimi(RS_ONES, 0, 0, 0)),
    "SH=0: coincidental agree on committed build")
row("nowrap sh16 mb16", hex(s1_regs.get(7, -1)), hex(want_rldimi(RS_ONES, 0, 16, 16)),
    "MB<=63-SH: mask 16..47; defect gives 16..63")
row("nowrap single", hex(s1_regs.get(8, -1)), hex(want_rldimi(RS_ONES, 0, 0, 63)),
    "singleton mask at bit 63")

# Session 2: Wrapping encodings (MB > 63-SH), rA initialized to 0, rS = ~0
# Defect symptom: stops at bit 63 and OMITS insertion into positions 0..63-SH
s2_setup = seed([(SRC, RS_ONES)] + [(r, 0) for r in DESTS])
s2_insns = [
    RLDIMI(4, SRC, 40, 40),      # SH=40, MB=40 -> 63-SH=23; mask 40..63 + 0..23 (48 bits)
    RLDIMI(5, SRC, 63, 63),      # SH=63, MB=63 -> 63-SH=0; mask 63 + 0 (2 bits)
    RLDIMI(6, SRC, 63, 1),       # SH=63, MB=1 -> 63-SH=0; mask 1..63 + 0 (64 bits, full)
    RLDIMI(7, SRC, 48, 32),      # SH=48, MB=32 -> 63-SH=15; mask 32..63 + 0..15 (48 bits)
]
s2_regs, s2_dis, s2_T, s2_how = session(s2_setup, s2_insns)
want_s2_dis = ["rldimi", "rldimi", "rldimi", "rldimi"]
want_s2_ops = ["r4,r3,40,40", "r5,r3,63,63", "r6,r3,63,1", "r7,r3,48,32"]
disasm_checked += len(want_s2_dis)
disasm_ok += sum(1 for i, (_, m, o) in enumerate(s2_dis[:len(want_s2_dis)])
                 if m == want_s2_dis[i] and o == want_s2_ops[i])

row("wrap sh40 mb40", hex(s2_regs.get(4, -1)), hex(want_rldimi(RS_ONES, 0, 40, 40)),
    "worked case: mask 40..63 + 0..23")
row("wrap sh63 mb63", hex(s2_regs.get(5, -1)), hex(want_rldimi(RS_ONES, 0, 63, 63)),
    "wrapping boundary: 2-bit mask (bits 63 and 0)")
row("wrap full", hex(s2_regs.get(6, -1)), hex(want_rldimi(RS_ONES, 0, 63, 1)),
    "wrapping full 64-bit mask (bits 1..63 and 0)")
row("wrap sh48 mb32", hex(s2_regs.get(7, -1)), hex(want_rldimi(RS_ONES, 0, 48, 32)),
    "wrapping mask 32..63 + 0..15")

# Session 3: Destination preservation with structured data and seeded rA
#  Two rows added on pass 2 (2026-09-12), both from a PATTERNED source:
#   * `full rot': every full-width mask elsewhere (`wrap full', and the census's six full-mask cells)
#     uses the all-ones source, so an edit skipping the ROTATE only when the mask is full --
#     `while (n-- != 0 && mb != ((64 - sh) & 63))', codex -- scored green.  SH=24, MB=40 is full
#     (MB == 64-SH) and also puts a third rotate amount (24) beside `pres nowrap' (8) and `pres wrap' (40).
#   * `alias rs=ra': rlwimi carries three aliasing rows and rldimi carried none, so a merge that
#     re-reads gpr[rs] AFTER clearing gpr[ra] -- instead of the snapshot `s' -- was green (glm).
#     r8 is both source and destination, seeded with RS_VAL; SH=8, MB=16 is a partial mask.
s3_setup = seed([(SRC, RS_VAL)] + [(r, SENT) for r in DESTS] + [(8, RS_VAL)])
s3_insns = [
    RLDIMI(4, SRC, 8, 0),        # nowrap: preserve low 8 bits of rA (bits 56..63)
    RLDIMI(5, SRC, 40, 40),      # wrap: preserve unmasked bits 24..39 of rA
    RLDIMI(6, SRC, 0, 32),       # nowrap: preserve high 32 bits (bits 0..31)
    RLDIMI(7, SRC, 24, 40),      # full mask from a patterned source: the rotate must show
    RLDIMI(8, 8, 8, 16),         # rA == rS: the merge must use the value read before the write
]
s3_regs, s3_dis, s3_T, s3_how = session(s3_setup, s3_insns)
want_s3_dis = ["rldimi", "rldimi", "rldimi", "rldimi", "rldimi"]
want_s3_ops = ["r4,r3,8,0", "r5,r3,40,40", "r6,r3,0,32", "r7,r3,24,40", "r8,r8,8,16"]
disasm_checked += len(want_s3_dis)
disasm_ok += sum(1 for i, (_, m, o) in enumerate(s3_dis[:len(want_s3_dis)])
                 if m == want_s3_dis[i] and o == want_s3_ops[i])

row("pres nowrap", hex(s3_regs.get(4, -1)), hex(want_rldimi(RS_VAL, SENT, 8, 0)),
    "preserve unmasked destination bits 56..63")
row("pres wrap", hex(s3_regs.get(5, -1)), hex(want_rldimi(RS_VAL, SENT, 40, 40)),
    "preserve unmasked destination bits 24..39")
row("pres sh0", hex(s3_regs.get(6, -1)), hex(want_rldimi(RS_VAL, SENT, 0, 32)),
    "preserve unmasked high 32 bits 0..31")
row("full rot", hex(s3_regs.get(7, -1)), hex(want_rldimi(RS_VAL, SENT, 24, 40)),
    "full mask, patterned source: result is ROTL64(rS,24)")
row("alias rs=ra", hex(s3_regs.get(8, -1)), hex(want_rldimi(RS_VAL, RS_VAL, 8, 16)),
    "rA == rS: merge uses rS as read, not the cleared rA")

# ========================================================= CR0 RECORD FORM =====
# rldimi. with Rc=1
cr_setup = seed([(SRC, RS_VAL), (4, SENT)])
cr_insns = [
    RLDIMI(4, SRC, 8, 0, rc=1),
]
cr_regs, cr_dis, cr_T, cr_how = session(cr_setup, cr_insns)
row("cr0 record form", "exit0" if "cr" in cr_regs else "no-cr", "exit0",
    "rldimi. executes with Rc=1 and dumps CR")

# ==================================================== COMPREHENSIVE CENSUS =====
# Sweep structured combinations across the full (SH, MB) space:
# - MB sweeps at fixed SH in {0, 8, 40, 63} (4 x 64 = 256)
# - SH sweeps at fixed MB in {0, 40} (2 x 64 = 128)
# - Diagonal (k, k) for k in 0..63 (64)
# - Anti-diagonal (k, 63-k) for k in 0..63 (64)
census_combos = []
for sh_val in [0, 8, 40, 63]:
    for mb_val in range(64):
        census_combos.append((sh_val, mb_val))
for mb_val in [0, 40]:
    for sh_val in range(64):
        census_combos.append((sh_val, mb_val))
for k in range(64):
    census_combos.append((k, k))
    census_combos.append((k, (63 - k) & 63))

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
    insns = [RLDIMI(DESTS[i], SRC, sh, mb) for i, (sh, mb) in enumerate(chunk)]
    st = seed([(SRC, RS_ONES)] + [(r, 0) for r in DESTS])
    cregs, cdis, cT, chow = session(st, insns)
    if chow != "exit0":
        print("CENSUS SESSION ABORTED how=%s at base=%d" % (chow, base))
        break
    for i, (sh, mb) in enumerate(chunk):
        disasm_checked += 1
        if i < len(cdis) and cdis[i][1] == "rldimi" and \
           cdis[i][2] == "r%d,r%d,%d,%d" % (DESTS[i], SRC, sh, mb):
            disasm_ok += 1
    for i, (sh, mb) in enumerate(chunk):
        census_run += 1
        got = cregs.get(DESTS[i], None)
        exp = want_rldimi(RS_ONES, 0, sh, mb)
        if got != exp:
            census_fail += 1
        if got == 0:
            census_zero += 1

#  Both wants are LITERALS (measured: killtable_20260911/probe_BASE.raw, 511/511 and 495).  They were
#  `len(uniq_census)' and `disasm_checked' -- derived from the very lists they count, so a census
#  shrunk by an edit passed both rows (codex, promotion design 2026-09-12).  511 = 16 control/core + 495;
#  the two pass-2 rows (`full rot', `alias rs=ra') add two placed words, so 513 -- re-measured in
#  ppcrlwimiwidth/killtable3_20260912/ (BASE leg), not carried.
row("disasm total", "%d/%d" % (disasm_ok, disasm_checked), "513/513",
    "every placed word re-read by disassembler")
row("census run", census_run, 495,
    "(SH,MB) cells driven across sweeps and diagonals")
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
#  CONTROL = rows green on EVERY build, fixed or not.  Checked against every recorded leg
#  (killtable_20260911/, killtable_nullmedium_20260911/): green on HEAD and on every mutant but
#  M_NOCIRC, whose census sessions run near the 90 s session timeout: table 1 TIMED OUT at 182 of 495
#  cells, table 2 (killtable2_20260912/) completed all 495 in 394 s.  Load decides which; the gate fails
#  there either way, on `census wrong'.  A correct build runs the whole probe in well under a second.
#  `nowrap sh0 mb0', `nowrap single' and `pres sh0' are the TARGET-INSTRUCTION controls: green on
#  the committed build, so they prove rldimi itself wrote registers -- `live' proves only `li'.
#  Without them a no-op rldimi read CONTROL=OK at a predicted 13/27 (codex promotion review).
CONTROL_ROWS = ("session", "live", "seed holds", "src intact", "disasm xcheck", "ctl rldicl",
                "ctl rldicr", "neg apparatus", "bits32 live", "bits32 rld bad", "cr0 record form",
                "disasm total", "census run", "nowrap sh0 mb0", "nowrap single", "pres sh0")
_status = dict(rows)
control_ok = all(_status.get(n, False) for n in CONTROL_ROWS)
try:
    os.remove(DUMMY)
    os.rmdir(_TMPDIR)
except OSError:
    pass
print("PPC_RLDIMI_RESULT=%d/%d" % (npass, len(rows)))
print("PPC_RLDIMI_CONTROL=%s" % ("OK" if control_ok else "FAIL"))
print("PPC_RLDIMI_PROBE_DONE")
sys.exit(0 if control_ok and npass == len(rows) else 1)
