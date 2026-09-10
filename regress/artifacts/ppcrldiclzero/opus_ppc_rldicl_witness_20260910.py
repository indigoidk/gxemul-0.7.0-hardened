#!/usr/bin/env python3
"""ppcrldiclzero -- RUNG-3 WITNESS for X(rldicl) writing zero on every execution.

DEFECT.  src/cpus/cpu_ppc_instr.c, X(rldicl):

        uint64_t tmp = cpu->cd.ppc.gpr[rs], tmp2;
        while (sh-- != 0) { ... }              /*  rotate, into tmp        */
        tmp2 = 0;
        while (mb <= 63) {
                tmp |= ((uint64_t)1 << (63-mb));   /*  <-- tmp, not tmp2   */
                mb ++;
        }
        cpu->cd.ppc.gpr[ra] = tmp & tmp2;          /*  tmp2 is still 0     */

TWO TOKENS ARE WRONG, NOT ONE, and only the second is observable today:
  (1) the mask is ORed into `tmp' -- the ROTATED VALUE -- rather than into `tmp2',
      so the rotated data is destroyed by having the mask bits forced to 1;
  (2) `tmp2' is therefore never assigned after `= 0', so the AND yields 0.
Defect (2) hides defect (1).  The single-character repair `tmp |=' -> `tmp2 |='
fixes both at once; the "obvious" repair of deleting `& tmp2' fixes neither -- it
would ship  ROTL64(rS,SH) | MASK(MB,63)  , an OR where the architecture says AND.
Row `naive fix' below exists to make that statement measurable rather than argued.

ARCHITECTURE, read locally -- _scratchpad/ppc_pem_32and64_2005.txt:29736 (rldiclx):
        n <- sh[5] || sh[0-4]
        r <- ROTL[64](rS, n)
        b <- mb[5] || mb[0-4]
        m <- MASK(b, 63)
        rA <- r & m
and the prose at :29737 -- "A mask is generated having 1 bits from bit MB through
bit 63 and 0 bits elsewhere.  The rotated data is ANDed with the generated mask".
IBM bit numbering is big-endian, so MASK(b,63) is the LOW (64-b) bits: for b=32
that is 0x00000000ffffffff, which is why `rldicl rA,rS,0,32' is the canonical
32-bit zero-extend (`clrldi rA,rS,32', manual :29758).
EVERY `want' in this probe is computed from those five lines, never from the tree.

RUNG 3: real PowerPC instructions fetched from guest RAM, decoded by the real
decoder and executed by the real handler, on the UNMODIFIED in-tree `-E bareppc'.
No machine description edited, no device_add, no CPU model override -- bareppc's
own MACHINE_DEFAULT_CPU is PPC970, which is 64-bit in the in-tree CPU table, and
64-bit is what the decoder requires (`if (cpu->cd.ppc.bits == 32) goto bad').

THE ORACLE is a guest-visible wrong VALUE, not a process death, so it is read
directly out of the destination register.  Four controls:
  live          `li r9,0x1234' in the same session reads back 0x1234 -- the guest
                really executes and the readback path really works.
  seed holds    a destination register seeded with a sentinel and then stepped
                over a NON-WRITING instruction still holds the sentinel.  This is
                the control that makes a zero readback attributable: it proves 0
                means "rldicl wrote 0", not "nothing ever wrote this register".
  neg apparatus a bogus machine name must turn `live' RED.  Without this, `live'
                is a check that cannot fail.
  disasm xcheck every instruction word placed is disassembled by the tree's own
                disassembler (cpu_ppc.c, a DIFFERENT code path from the execute
                handler in cpu_ppc_instr.c) and compared against the operands the
                encoder intended.  Guards the hand-assembled-encoding trap.
  rldicr        the correctly-written sibling, same rotate-and-mask shape, same
                session -- attributes the failure to X(rldicl) rather than to the
                encoding, the machine, the rotate or this program.

TEST-FIRST SHAPE: every `want' is the ARCHITECTURAL value.  On the committed
pre-fix build the rldicl rows are RED; after `tmp |=' -> `tmp2 |=' the identical
script goes green.

Sentinel: PPC_RLDICL_WITNESS_DONE
"""

import re
import subprocess
import sys
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: ppc_rldicl_witness.py <gxemul> [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
DUMMY = "/tmp/ppc_rldicl_dummy.bin"
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x10000
M64 = (1 << 64) - 1
SENT = 0x5A5A5A5A5A5A5A5A        # sentinel pre-seeded into every destination
RS_ONES = M64                    # census source: makes EVERY cell non-vacuous
RS_VAL = 0xDEADBEEFCAFEF00D      # value source: exercises the rotate too
SRC = 3                          # rS is always r3; r3 is never a destination
DESTS = list(range(4, 30))       # r4..r29 -- 26 destinations per session

rows = []


def row(name, got, want, note=""):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 17, name
    ok = (got == want)
    rows.append((name, ok))
    print("%-18s %-20s %-20s %-48s %s" % (name, str(got), str(want), note,
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


def want_rldicl(rs_val, sh, mb):
    return rotl64(rs_val, sh) & mask_b_63(mb)


def want_rldicr(rs_val, sh, me):
    return rotl64(rs_val, sh) & mask_0_e(me)


def want_rldimi(rs_val, ra_val, sh, mb):
    """manual :29908 -- m <- MASK(b, ~n); prose :29909 "1 bits from bit MB
       through bit 63 - SH"."""
    m = mask_b_63(mb) & mask_0_e((63 - sh) & 63)
    return (rotl64(rs_val, sh) & m) | (ra_val & (~m & M64))


def rotl32(x, n):
    """ROTL[32] per manual :6878 -- two copies of rS[32-63], then rotate."""
    lo = x & 0xFFFFFFFF
    n &= 31
    r32 = ((lo << n) | (lo >> (32 - n))) & 0xFFFFFFFF if n else lo
    return (r32 << 32) | r32


def mask32(mb, me):
    """MASK(mb+32, me+32) confined to the low 32 bits, PowerPC wrap-around form."""
    m = 0
    b = mb
    while True:
        m |= 1 << (31 - b)
        if b == me:
            break
        b = (b + 1) & 31
    return m


def want_rlwinm(rs_val, sh, mb, me):
    return rotl32(rs_val, sh) & mask32(mb, me)


def want_rlwimi(rs_val, ra_val, sh, mb, me):
    m = mask32(mb, me)
    return (rotl32(rs_val, sh) & m) | (ra_val & (~m & M64))


# -------------------------------------------------------------------- encodings
def enc_md(xo, rs, ra, sh, mbe, rc=0):
    """opcode 30 (rldicl/rldicr/rldimi).  Field placement derived from the manual's
       own instruction-format diagram at :29706-29734:
         0-5 opcode | 6-10 S | 11-15 A | 16-20 sh[0-4] | 21-26 mb[5]||mb[0-4]
         | 27-29 XO | 30 sh[5] | 31 Rc      (all big-endian bit numbers)"""
    assert 0 <= sh <= 63 and 0 <= mbe <= 63 and 0 <= xo <= 7
    return ((30 << 26) | (rs << 21) | (ra << 16) | ((sh & 31) << 11)
            | ((mbe & 31) << 6) | (((mbe >> 5) & 1) << 5) | (xo << 2)
            | (((sh >> 5) & 1) << 1) | rc) & 0xFFFFFFFF


def RLDICL(ra, rs, sh, mb):
    return enc_md(0, rs, ra, sh, mb)


def RLDICR(ra, rs, sh, me):
    return enc_md(1, rs, ra, sh, me)


def RLDIMI(ra, rs, sh, mb):
    return enc_md(3, rs, ra, sh, mb)


def enc_m(op, rs, ra, sh, mb, me, rc=0):
    """opcode 20/21 (rlwimi/rlwinm): 0-5 op | 6-10 S | 11-15 A | 16-20 SH
       | 21-25 MB | 26-30 ME | 31 Rc."""
    return ((op << 26) | (rs << 21) | (ra << 16) | (sh << 11) | (mb << 6)
            | (me << 1) | rc) & 0xFFFFFFFF


def RLWINM(ra, rs, sh, mb, me):
    return enc_m(21, rs, ra, sh, mb, me)


def RLWIMI(ra, rs, sh, mb, me):
    return enc_m(20, rs, ra, sh, mb, me)


def LI(rd, simm):
    return ((14 << 26) | (rd << 21) | (0 << 16) | (simm & 0xFFFF)) & 0xFFFFFFFF


def ORI(ra, rs, imm):
    return ((24 << 26) | (rs << 21) | (ra << 16) | (imm & 0xFFFF)) & 0xFFFFFFFF


NOP = ORI(0, 0, 0)               # ori r0,r0,0 -- writes r0 only


# ---------------------------------------------------------------------- sessions
def session(setup, insns, timeout=90, machine="bareppc", cpu=None):
    """Place `insns' at CODE, seed registers, step exactly len(insns), dump regs.
       Returns (regs dict, disasm list, transcript, how)."""
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
    # the LAST `reg' dump in the transcript
    idx = t.rfind("GXemul> reg")
    regs = {}
    if idx >= 0:
        for m in re.finditer(r"\br(\d\d) = (0x[0-9a-fA-F]+)", t[idx:]):
            regs[int(m.group(1))] = int(m.group(2), 16)
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


print("ppcrldiclzero RUNG-3 WITNESS -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E bareppc -M 64 (UNMODIFIED in-tree; MACHINE_DEFAULT_CPU=PPC970,"
      " 64-bit)")
print("wants derived from _scratchpad/ppc_pem_32and64_2005.txt:29736 (rldiclx),"
      " :6878 (ROTL32)")
print("%-18s %-20s %-20s %-48s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()
disasm_checked = 0
disasm_ok = 0

# ============================================================ CONTROL SESSION ==
ctl_insns = [
    LI(9, 0x1234),                       # liveness
    NOP,                                 # seed-holds probe steps over this
    RLDICL(4, SRC, 0, 32),               # clrldi r4,r3,32 -- the canonical case
    RLDICR(5, SRC, 0, 31),               # DISCRIMINATING control: correct sibling
    RLDICL(6, SRC, 8, 0),                # pure rotate, mask = all ones
    RLDICR(7, SRC, 8, 63),               # same rotate through the good sibling
]
ctl_setup = seed([(SRC, RS_VAL), (30, SENT)] + [(r, SENT) for r in DESTS])
regs, dis, T, how = session(ctl_setup, ctl_insns)

open("/tmp/ppc_rldicl_ctl.txt", "w").write(T)

row("session", how, "exit0", "the control session ran to `quit'")
row("live", hex(regs.get(9, -1)), hex(0x1234),
    "li r9,0x1234 -- the guest executes and readback works")
row("seed holds", hex(regs.get(30, -1)), hex(SENT),
    "r30 seeded, never a destination: a 0 readback means SOMETHING wrote it")
row("src intact", hex(regs.get(SRC, -1)), hex(RS_VAL),
    "rS is unchanged by any of these instructions")

# --- disassembler cross-check (different code path from the execute handler)
want_dis = ["li", "nop", "rldicl", "rldicr", "rldicl", "rldicr"]
want_ops = ["r9,4660", "", "r4,r3,0,32", "r5,r3,0,31", "r6,r3,8,0",
            "r7,r3,8,63"]
got_pairs = [(m, o) for _, m, o in dis]
disasm_checked += len(want_dis)
disasm_ok += sum(1 for i, (m, o) in enumerate(got_pairs[:len(want_dis)])
                 if m == want_dis[i] and o == want_ops[i])
row("disasm xcheck", "%d/%d" % (disasm_ok, disasm_checked), "6/6",
    "tree's OWN disassembler agrees with the encoder, operand for operand")

# --- the defect, and its discriminating sibling, in ONE session
row("zx32 rldicl", hex(regs.get(4, -1)), hex(want_rldicl(RS_VAL, 0, 32)),
    "clrldi r4,r3,32 -- the 32-bit zero-extend compilers emit constantly")
row("zx32 rldicr", hex(regs.get(5, -1)), hex(want_rldicr(RS_VAL, 0, 31)),
    "DISCRIMINATING: the sibling, same session, same rotate, same encoder")
row("rot8 rldicl", hex(regs.get(6, -1)), hex(want_rldicl(RS_VAL, 8, 0)),
    "rotldi r6,r3,8 -- mask is all-ones, so this is a PURE rotate")
row("rot8 rldicr", hex(regs.get(7, -1)), hex(want_rldicr(RS_VAL, 8, 63)),
    "DISCRIMINATING: the same pure rotate through the good sibling")

# --- what the NAIVE repair would produce, stated as a measurable prediction
# DERIVED, not measured here: what the "obvious" repair would produce.
_naive = rotl64(RS_VAL, 0) | mask_b_63(32)
row("naive fix wrong", "differs" if _naive != want_rldicl(RS_VAL, 0, 32) else "same",
    "differs",
    "DERIVED: deleting `& tmp2' ships OR-not-AND (0x%x), still wrong" % _naive)

# ================================================ NEGATIVE APPARATUS CONTROL ==
# Prove `live' CAN go red.  A bogus machine name means no machine is built, so a
# green `live' would be a check that cannot fail.
nregs, _, nT, nhow = session(seed([(9, SENT)]), [LI(9, 0x1234)],
                             machine="nosuchmachine", timeout=60)
row("neg apparatus", "%s/%s" % (nhow, hex(nregs.get(9, -1))), "exit1/-0x1",
    "bogus machine -> no guest -> `live' MUST fail; the oracle is failable")

# ============================================ REACHABILITY CONTROL (32-bit) ===
# The decoder sends rld* to `bad' when bits == 32.  Same session, same encoding,
# a 32-bit CPU: the instruction must NOT execute as rldicl.
b32regs, _, b32T, b32how = session(
    seed([(SRC, RS_VAL), (4, SENT), (9, SENT)]),
    [LI(9, 0x1234), RLDICL(4, SRC, 0, 32)], timeout=60, machine="bareppc",
    cpu="PPC603")
open("/tmp/ppc_rldicl_32.txt", "w").write(b32T)
row("bits32 live", hex(b32regs.get(9, -1)), hex(0x1234),
    "PPC603 (32-bit): the guest still runs -- li executes")
row("bits32 rld bad", "TODO" if "TODO: rld" in b32T else "no-msg", "TODO",
    "decoder prints `TODO: rld* in 32-bit mode?' and goes to bad -- unreachable")

# ===================================================== VACUITY (question 3) ===
# A cell where the ARCHITECTURAL answer is itself zero: a detector row placed
# here could never fail, whatever the handler does.
RS_VAC = 0xFFFFFFFF00000000
vregs, _, vT, vhow = session(seed([(SRC, RS_VAC)] + [(r, SENT) for r in DESTS]),
                             [RLDICL(4, SRC, 0, 32), RLDICL(5, SRC, 0, 0)])
row("vacuous cell", hex(vregs.get(4, -1)), hex(want_rldicl(RS_VAC, 0, 32)),
    "rS=0xffffffff00000000, SH=0, MB=32: correct answer IS 0 -- GREEN on a")
row("vac neighbour", hex(vregs.get(5, -1)), hex(want_rldicl(RS_VAC, 0, 0)),
    "  broken build.  Its MB=0 neighbour on the same rS is not vacuous.")

# ============================================================ THE (SH,MB) CENSUS
# rS = all-ones, so ROTL64(rS,SH) = all-ones for every SH and the architectural
# answer is exactly MASK(MB,63), which is NONZERO for every MB in 0..63.  Every
# cell of this census is therefore provably non-vacuous by construction.
combos = []
for mb in range(64):
    combos.append((0, mb))                      # MB sweep at SH=0
for sh in range(1, 64):
    combos.append((sh, 0))                      # SH sweep at MB=0
for k in range(1, 64):
    combos.append((k, k))                       # the diagonal
seen = set()
uniq = []
for c in combos:
    if c not in seen:
        seen.add(c)
        uniq.append(c)

census_fail = 0
census_zero = 0
census_run = 0
for base in range(0, len(uniq), len(DESTS)):
    chunk = uniq[base:base + len(DESTS)]
    insns = [RLDICL(DESTS[i], SRC, sh, mb) for i, (sh, mb) in enumerate(chunk)]
    st = seed([(SRC, RS_ONES)] + [(r, SENT) for r in DESTS])
    cregs, cdis, cT, chow = session(st, insns)
    if chow != "exit0":
        print("CENSUS SESSION ABORTED how=%s at base=%d" % (chow, base))
        break
    # disassembler cross-check on every census word too
    for i, (sh, mb) in enumerate(chunk):
        disasm_checked += 1
        if i < len(cdis) and cdis[i][1] == "rldicl" and \
           cdis[i][2] == "r%d,r%d,%d,%d" % (DESTS[i], SRC, sh, mb):
            disasm_ok += 1
    for i, (sh, mb) in enumerate(chunk):
        census_run += 1
        got = cregs.get(DESTS[i], None)
        exp = want_rldicl(RS_ONES, sh, mb)
        if got != exp:
            census_fail += 1
        if got == 0:
            census_zero += 1

row("census run", census_run, len(uniq),
    "(SH,MB) cells driven: MB sweep + SH sweep + diagonal, rS=all-ones")
row("census wrong", census_fail, 0,
    "cells whose result differs from MASK(MB,63) -- want 0 after a fix")
row("census zero", census_zero, 0,
    "cells that returned EXACTLY ZERO -- want 0 after a fix")
row("disasm total", "%d/%d" % (disasm_ok, disasm_checked),
    "%d/%d" % (disasm_checked, disasm_checked),
    "every placed word re-read by the tree's own disassembler")

# ====================================================== SIBLINGS (question 4) ==
# rldimi: X(rldimi) computes its mask end as `63 - sh' AFTER the rotate loop has
# post-decremented sh to -1, so the end is always 64 and the mask always runs to
# bit 63 instead of stopping at 63-SH.
sib_setup = seed([(SRC, M64), (4, 0), (5, 0), (6, 0)])
sib_insns = [
    RLDIMI(4, SRC, 8, 0),        # mask should be MASK(0,55); code gives MASK(0,63)
    RLDIMI(5, SRC, 0, 0),        # SH=0 -> 63-0 == 63, so this one should agree
    RLDIMI(6, SRC, 32, 0),       # mask should be MASK(0,31)
]
sregs, sdis, sT, show = session(sib_setup, sib_insns)
open("/tmp/ppc_rldicl_sib.txt", "w").write(sT)

# *** SEPARATE SESSION, AND A DIFFERENT SOURCE, BECAUSE THE FIRST ATTEMPT AT THESE
# THREE ROWS WAS VACUOUS BY CONSTRUCTION.  With rS = all-ones a 64-bit-wide rotate
# and a true ROTL32 agree bit for bit, so the rows went GREEN while proving nothing.
# RS_HALVES has DIFFERENT halves, which is exactly what makes a cross-half bleed
# observable.  Recorded rather than silently corrected: a row that cannot fail is
# the failure mode this project names most often. ***
RS_HALVES = 0xAAAAAAAA0000000F
w_setup = seed([(SRC, RS_HALVES), (7, SENT), (8, SENT), (9, SENT), (10, SENT)])
w_insns = [
    RLWINM(7, SRC, 4, 0, 31),    # 32-bit sibling that DOES truncate rS first
    RLWIMI(8, SRC, 4, 0, 31),    # 32-bit sibling that does NOT truncate rS
    RLWIMI(9, SRC, 0, 0, 31),    # SH=0 short-circuits the rotate: no bleed possible
    RLDICR(10, SRC, 4, 63),      # rldicr on the same source, as a live control
]
wregs, wdis, wT, whow = session(w_setup, w_insns)
open("/tmp/ppc_rldicl_wide.txt", "w").write(wT)

row("rldimi sh8", hex(sregs.get(4, -1)), hex(want_rldimi(M64, 0, 8, 0)),
    "mask must END at bit 63-SH=55; `63 - sh' is evaluated with sh already -1")
row("rldimi sh0", hex(sregs.get(5, -1)), hex(want_rldimi(M64, 0, 0, 0)),
    "SH=0 is the one case where the clobbered sh gives the right end")
row("rldimi sh32", hex(sregs.get(6, -1)), hex(want_rldimi(M64, 0, 32, 0)),
    "mask must end at bit 31")
row("wide session", whow, "exit0", "rS=0xaaaaaaaa0000000f -- the halves DIFFER")
row("rlwinm", hex(wregs.get(7, -1)), hex(want_rlwinm(RS_HALVES, 4, 0, 31)),
    "control: rlwinm casts rS to uint32_t FIRST, so it should be correct")
row("rlwimi wide", hex(wregs.get(8, -1)),
    hex(want_rlwimi(RS_HALVES, SENT, 4, 0, 31)),
    "ROTL32 is over rS[32-63] ONLY; MODE_uint_t rotates 64 bits wide")
row("rlwimi sh0", hex(wregs.get(9, -1)),
    hex(want_rlwimi(RS_HALVES, SENT, 0, 0, 31)),
    "SH=0 short-circuits the rotate, so no bleed is possible -- must stay green")
row("wide live", hex(wregs.get(10, -1)), hex(want_rldicr(RS_HALVES, 4, 63)),
    "rldicr on the same source: the session really executed")

# ================================================================ SCORE + DONE
npass = sum(1 for _, ok in rows if ok)
print("")
print("SCORE %d/%d  elapsed=%.1fs  binary=%s  label=%s"
      % (npass, len(rows), time.time() - t0, BIN, LABEL))
print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
print("PPC_RLDICL_WITNESS_DONE")
