#!/usr/bin/env python3
"""ppccrandcorc -- RUNG-3 DETECTOR for the PowerPC Condition Register logical instructions.

DEFECT (#575).  src/cpus/cpu_ppc_instr.c, X(crandc) and X(crorc), computed

    crandc:  CR[BT] = !(CR[BA] & CR[BB])      (that is crnand)
    crorc:   CR[BT] = !(CR[BA] | CR[BB])      (that is crnor)

ARCHITECTURE, PowerPC Book I v2.01 (_scratchpad/ppc_uisa_book1_v201.txt:1909-1914):

    crandc BT,BA,BB    CR[BT] <- CR[BA] & ~CR[BB]
    crorc  BT,BA,BB    CR[BT] <- CR[BA] | ~CR[BB]

CR bits are numbered 0..31 from the most significant end, as the handlers do with
(cr >> (31-n)) & 1.

WHAT THE ROWS MEASURE.  Each row runs one CR logical instruction on a real guest through
the real decoder (`-E bareppc`, unmodified in-tree machine; PPC970 at 64 bits and PPC603 at
32 bits), with CR seeded from the debugger, and reads CR back.  The truth-table rows give
every (CR[BA], CR[BB]) combination; the destination bit is pre-set to the INVERSE of the
architectural result, so a row passes only if the instruction wrote the right value (the two
round-2 rows `64 crandc bbmask' and `64 crorc bamask' pre-set it EQUAL to the result instead:
that is the only way a BB read of CR[BT] can be seen, see the pin rows below).  The `others'
rows check that no CR bit except the destinations changed, and the `mfcr' rows read CR
through a second channel (a guest mfcr into a GPR).  The four round-3 rows (`baread',
`bbread', `setbits') compare the WHOLE CR, from the register dump and from mfcr, with the
architectural CR, so an extra SET bit anywhere is seen.  The five correct siblings (crand,
cror, crnor, creqv, crxor) run the same table as controls of the oracle and the encoder.

CLAUSE (e) -- what this instrument catches (test-variant table 1, regress/artifacts/ppccrandcorc/table1_20261105/table1/
SCORES.txt, PRETABLE.out written before it with predictions computed by its v575.py simulator; 15 variants on the first 62
rows, all 15 red, each exactly as predicted): each handler's defect restored (b1, b2); both bodies made identity (c, the ruled
null medium of the handlers); the complement moved to BA, dropped, or the operator crossed between the two edited lines
(d1-d6); the BA/BB field mask weakened to & 7 or & 15 (m1-m4: the `hi' rows alone); the BT field mask weakened to & 7 (t1,
t2).  The pre-fix build scores 52 of 62 (the ten DISC rows); /bin/true 5 of 62 and /bin/false 1 of 62 score CONTROL=FAIL, and an
absent binary stops the probe before any row with no sentinel.
  ROUND 2 (2026-11-05, regress/artifacts/ppccrandcorc/r2_20261105/CLOSURE.md): the four pin rows after the `hi' rows were
  derived by simulating every single-edit cell of an enumeration of the two handlers (239 cells: every field mask 0..30 at BT,
  BA and BB; every source read taking another field's index; the read mask `& 1' widened to & 3 / & 7; the clear moved before
  the reads, deleted or toggled; the set deleted or toggled; table 1's condition edits, the pass-1 R5 bt-substitutions and
  the identity body; the dispatch bound to each other CR handler).  The first 62 rows missed 25 of them (pass 2: codex's nine
  and glm's read-mask cell among them); with the four rows every cell is red by simulation except four EQUIVALENT cells
  (crandc's BA read mask widened: `ba & !bb' only sees bit 0 of ba; `|=' -> `^=' after the clear) and the crandc toggle of (5).
  Table 2 measured that claim (r2_20261105/table2/SCORES.txt; PRETABLE_2.out written before it; 27 variants on these 66
  rows): all 27 exactly as predicted -- 26 red, and g2 (crandc's BA read mask & 3) green, as predicted EQUIVALENT.  The
  pre-fix build scores 56 of 66 (the ten DISC rows); /bin/true 5 of 66 and /bin/false 1 of 66 score CONTROL=FAIL.
  ROUND 3 (2026-11-05, regress/artifacts/ppccrandcorc/r3_20261105/CLOSURE3.md, v575c.py): pass 3 showed the round-2 VOCABULARY
  narrower than the classes it put in scope (read masks `& 3' / `& 7' only; the set only deleted or toggled).  The four whole-CR
  rows after the round-2 pins close the single-constant space at the four read-mask sites and the two set literals (453 cells
  simulated: the 239 plus `& (1|1<<k)' for k = 2..31 and & 0, 2, 4, 6 at every read site, the set literal 1+2^k for k = 1..31
  in both handlers, and 16 structural cells; 56 of them, codex's 54 among them, escaped the 66 rows and are red on the 70).
  COVERED: every read mask `& m' other than the fix's at crandc BB, crorc BA and crorc BB (all 2^32 m, by the proof in
  CLOSURE3.md), every crandc BA read mask with bit 0 clear; every set literal C != 1 in both handlers; the clear's and the
  set's `(31-bt)' re-addressed to (31-ba), (31-bb) or bt; the clear moved between the reads.  DELIBERATELY UNCOVERED, in
  two classes.  EQUIVALENT, proved: crandc BA read masks with bit 0 set (`ba & !bb' sees only bit 0 of ba); `|=' -> `^=' at
  either set (after the clear); the two read statements swapped.  DISCLOSED, NOT equivalent: the crandc toggle of (5)
  (crandc 31,0,1 over CR 0 must leave 0; the toggle leaves 1) -- no row sees it, for the reason (5) gives.  (Pass 4, F3:
  round 3 had listed the toggle under "EQUIVALENT, proved"; r3_20261105/RECORDS4_NOTE.md.)
  and does not cover:
  (1) crnand (opcode 19, extended opcode 225) is not decoded at HEAD and stops the CPU; it is filed separately as
      `ppccrnandundec' and is not run here.
  (2) The dyntrans fast path for these handlers is the handler itself (no separate
      translation), so one cold run per instruction exercises it.
  (3) The edge rows pin destination bits 0 and 31; the `hi' rows pin the BA/BB field masks at & 15, & 7, & 3, & 1 (BA, BB
      >= 16 with every submask alias holding the opposite value); the round-2 `bbmask'/`bamask' rows put the source at index
      31 over a uniform CR so that every mask 0..30 at that site reads a flipped input -- EXCEPT mask 16 on `64 crorc bamask',
      whose seed 0xffff7ffe has CR[16] = 0 (its destination, pre-set EQUAL): that alias is red on `64 crorc 11' (BA 1 -> 0),
      and the round-3 `64 crorc baread' row (BA = 31 over 0xfffffffe) flips every BA mask 0..30 on one row.  (Round 3 corrects
      the round-2 wording "EVERY mask 0..30 at that site reads a flipped input": pass 3, R1.)  Inputs at index 0 (the tables'
      BA=0/BB=0) and 31 (`64 crandc hi' BA, the round-2 and round-3 index-31 sources) are rowed; a destination at index 0 or
      31 is rowed by the edge rows, `64 crorc bbmask' and the two `setbits' rows.
  (4) The signed shift `1 << (31-bt)' at bt = 0 (all seven handlers) is `ppccrlogicshift', filed separately: on this
      toolchain it gives the architectural result, so no row here can see it (the pass-1 ruling, R2).
  (5) Not claimed (the pass-1 ruling: recommended, not owed): an extra CLEAR of a bit that is neither a source nor a
      destination -- the table seeds hold no ones there, the hi and round-2 pin sessions check only the destination, the two
      `setbits' rows carry zeros where the set-literal cells need them, and the two read rows (`baread' over 0xfffffffe and
      `bbread' over 0xfffffffc: ones at 31 and 30 of the 32 bits) see extra clears only incidentally (CLOSURE3.md's appendix
      lists what the whole-CR rows see: most crorc clear literals 1+2^k, k = 1..30, and no crandc one above k = 10; the
      regress review, R2, corrected "the round-3 whole-CR rows carry ones only where the set-literal cells need zeros");
      and a crandc body that
      TOGGLES the destination instead of clearing it -- every crandc row with result 0 pre-sets the inverse, and toggling
      the inverse gives the right value (`64 crandc setbits' pre-sets 0 with result 1: a toggle then the set gives 1 too).
      The crorc toggle IS seen: `64 crorc bamask' pre-sets a result of 0 EQUAL, which a toggle turns into 1.

Sentinel: PPC_CRLOGIC_PROBE_DONE (plus PPC_CRLOGIC_RESULT=n/N, PPC_CRLOGIC_CONTROL=OK|FAIL)
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: ppc_crlogic_probe.py <gxemul> [label]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
_TMPDIR = tempfile.mkdtemp(prefix="ppc_crlogic_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
open(DUMMY, "wb").write(b"\x00\x00\x00\x00")

CODE = 0x10000
SENT = 0x5A5A5A5A5A5A5A5A

rows = []
controls = []


def row(name, got, want, note="", control=False):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 18, name
    ok = (got == want)
    rows.append((name, ok))
    if control:
        controls.append((name, ok))
    print("%-19s %-12s %-12s %-50s %s" % (name, str(got), str(want), note,
                                          "ok" if ok else "FAIL"))
    return ok


# ----------------------------------------------------------------- architecture
#  Book I v2.01:1854-1914 -- one function per instruction, written from the manual.
ARCH = {
    "crand":  lambda a, b: a & b,
    "crandc": lambda a, b: a & (1 - b),
    "creqv":  lambda a, b: 1 - (a ^ b),
    "cror":   lambda a, b: a | b,
    "crorc":  lambda a, b: a | (1 - b),
    "crnor":  lambda a, b: 1 - (a | b),
    "crxor":  lambda a, b: a ^ b,
}
XO = {"crand": 257, "crandc": 129, "creqv": 289, "cror": 449, "crorc": 417,
      "crnor": 33, "crxor": 193}


def crbit(cr, n):
    return (cr >> (31 - n)) & 1


def setbit(cr, n, v):
    m = 1 << (31 - n)
    return (cr | m) if v else (cr & ~m & 0xFFFFFFFF)


# -------------------------------------------------------------------- encodings
def XL(op, bt, ba, bb):
    """Opcode 19 XL-form CR logical (Book I:1850 layout)."""
    assert op in XO and 0 <= bt <= 31 and 0 <= ba <= 31 and 0 <= bb <= 31
    return ((19 << 26) | (bt << 21) | (ba << 16) | (bb << 11) | (XO[op] << 1)) & 0xFFFFFFFF


def LI(rd, simm):
    return ((14 << 26) | (rd << 21) | (simm & 0xFFFF)) & 0xFFFFFFFF


def MFCR(rt):
    return ((31 << 26) | (rt << 21) | (19 << 1)) & 0xFFFFFFFF


NOP = (24 << 26)  # ori r0,r0,0


# ---------------------------------------------------------------------- sessions
def session(cr_seed, insns, timeout=90, machine="bareppc", cpu=None):
    """Seed CR (and r30), place `insns' at CODE, step them all, dump the registers."""
    cmds = ["cr=0x%x" % cr_seed, "r30=0x%x" % SENT]
    for i, w in enumerate(insns):
        cmds.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, w))
    cmds.append("unassemble 0x%x 0x%x" % (CODE, CODE + 4 * len(insns)))
    cmds.append("pc=0x%x" % CODE)
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
        end = t.find("GXemul> pc=", di)
        seg = t[di:end if end > 0 else len(t)]
        for m in re.finditer(r"^[0-9a-f]{8,16}: ([0-9a-f]{8})\s*(?:<- )?(\S+)(?:\t(\S+))?", seg, re.M):
            dis.append((int(m.group(1), 16), m.group(2), m.group(3) or ""))
    return regs, dis, t, how


def table(tag, ops, first_bt, cpu=None):
    """One session: every op in `ops' over the four (a, b) cases, BA/BB from CR bits 0..3.

    CR bits 0..3 hold the inputs 0,1,0,1 (bit 0 = 0, bit 1 = 1, bit 2 = 0, bit 3 = 1), so
    (a, b) = (0,0) uses BA=0,BB=2; (0,1) BA=0,BB=1; (1,0) BA=1,BB=0; (1,1) BA=1,BB=3.
    Each destination bit is pre-set to the INVERSE of the architectural result."""
    pick = {(0, 0): (0, 2), (0, 1): (0, 1), (1, 0): (1, 0), (1, 1): (1, 3)}
    seed = 0
    seed = setbit(seed, 1, 1)
    seed = setbit(seed, 3, 1)
    plan, bt = [], first_bt
    for op in ops:
        for ab in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            want = ARCH[op](*ab)
            seed = setbit(seed, bt, 1 - want)
            plan.append((op, ab, bt, want))
            bt += 1
    insns = [XL(op, b, pick[ab][0], pick[ab][1]) for op, ab, b, _ in plan] + [MFCR(10)]
    regs, dis, T, how = session(seed, insns, cpu=cpu)
    cr = regs.get("cr", -1)
    return seed, plan, regs, dis, how, cr


#  What the pre-#575 handlers computed, used ONLY to label rows DISC (the defect changes the
#  result) or PIN (the same either way); never used as a want.
DEFECT = {"crandc": lambda a, b: 1 - (a & b), "crorc": lambda a, b: 1 - (a | b)}


def score_table(prefix, seed, plan, regs, dis, how, cr, control):
    row(prefix + " session", how, "exit0", "the session ran to `quit'", control=True)
    mask = 0
    for op, ab, bt, want in plan:
        mask |= 1 << (31 - bt)
        kind = "PIN"
        if op in DEFECT and DEFECT[op](*ab) != want:
            kind = "DISC"
        row("%s %s %d%d" % (prefix, op, ab[0], ab[1]), crbit(cr, bt) if cr >= 0 else -1, want,
            "%s BT=%d: Book I %s(a=%d,b=%d)" % (kind, bt, op, ab[0], ab[1]), control=control)
    row(prefix + " others", hex(cr & ~mask & 0xFFFFFFFF) if cr >= 0 else "none",
        hex(seed & ~mask & 0xFFFFFFFF), "no CR bit but the destinations moved")
    row(prefix + " mfcr", hex(regs.get(10, -1)), hex(cr) if cr >= 0 else "none",
        "mfcr r10 reads the same CR (second channel)")
    names = [m for _, m, _ in dis[:len(plan)]]
    good = sum(1 for i, (op, _, _, _) in enumerate(plan) if i < len(names) and names[i] == op)
    row(prefix + " disasm", "%d/%d" % (good, len(plan)), "%d/%d" % (len(plan), len(plan)),
        "the tree's disassembler names each encoding", control=True)


print("ppccrandcorc RUNG-3 DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E bareppc (UNMODIFIED in-tree; PPC970 64-bit, and -C PPC603 32-bit)")
print("wants from PowerPC Book I v2.01:1854-1914")
print("%-19s %-12s %-12s %-50s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

# ============================================================ CONTROL SESSION ==
CTL_CR = 0x12345678
regs, dis, T, how = session(CTL_CR, [LI(9, 0x1234), NOP, MFCR(10)])
row("ctl session", how, "exit0", "the control session ran to `quit'", control=True)
row("ctl live", hex(regs.get(9, -1)), hex(0x1234), "li r9 -- the guest executes", control=True)
row("ctl seed holds", hex(regs.get(30, -1)), hex(SENT), "r30 seeded, never written", control=True)
row("ctl cr seed", hex(regs.get("cr", -1)), hex(CTL_CR), "the CR seed reads back", control=True)
row("ctl mfcr", hex(regs.get(10, -1)), hex(CTL_CR), "mfcr r10 = the seeded CR", control=True)

# ================================================ NEGATIVE APPARATUS CONTROL ==
nregs, _, _, nhow = session(CTL_CR, [LI(9, 0x1234)], machine="nosuchmachine", timeout=60)
row("neg apparatus", "%s/%s" % (nhow, hex(nregs.get(9, -1))), "exit1/-0x1",
    "a bogus machine runs no guest", control=True)

# ================================================ THE TWO HANDLERS, 64-BIT ===
score_table("64", *table("64", ["crandc", "crorc"], 8), control=False)

# ======================================= THE FIVE CORRECT SIBLINGS (controls) ==
score_table("s64", *table("s64", ["crand", "cror", "crnor", "creqv", "crxor"], 8), control=True)

# ============================================ DESTINATION EDGES (bits 0 and 31) ==
#  crandc BT=0 from (a,b)=(0,0) -> 0 (the old code gave 1); crorc BT=31 from (1,1) -> 1 (the
#  old code gave 0).  Inputs at CR bits 2,3 = 0,0 and 4,5 = 1,1; destinations pre-set inverse.
eseed = 0
eseed = setbit(eseed, 4, 1)
eseed = setbit(eseed, 5, 1)
eseed = setbit(eseed, 0, 1)
eseed = setbit(eseed, 31, 0)
eregs, edis, _, ehow = session(eseed, [XL("crandc", 0, 2, 3), XL("crorc", 31, 4, 5), MFCR(10)])
ecr = eregs.get("cr", -1)
row("edge session", ehow, "exit0", "the edge session ran to `quit'", control=True)
row("edge crandc bt0", crbit(ecr, 0) if ecr >= 0 else -1, 0, "DISC BT=0 (the CR's top bit)")
row("edge crorc bt31", crbit(ecr, 31) if ecr >= 0 else -1, 1, "DISC BT=31 (the CR's low bit)")
emask = (1 << 31) | 1
row("edge others", hex(ecr & ~emask & 0xFFFFFFFF) if ecr >= 0 else "none",
    hex(eseed & ~emask & 0xFFFFFFFF), "no CR bit but bits 0 and 31 moved")
#  The edge session runs mfcr and captures its disassembly like the table sessions; both are scored (pass-1 ruling R4).  `edge
#  disasm' compares MNEMONICS only: it checks that the disassembler names the two encodings whose BT fields are 0 and 31, not
#  that it prints BT, BA or BB (pass 2, F3).
row("edge mfcr", hex(eregs.get(10, -1)), hex(ecr) if ecr >= 0 else "none", "mfcr r10 reads the same CR (second channel)")
enames = [m for _, m, _ in edis[:2]]
row("edge disasm", "%d/2" % sum(1 for i, op in enumerate(("crandc", "crorc")) if i < len(enames) and enames[i] == op), "2/2",
    "the disassembler names both edge encodings", control=True)

# =========================================== FIELD-MASK PINS (BA, BB >= 16; pass-1 ruling R4) ==
#  Every table row uses BA in {0,1,2,4} and BB in {0,1,2,3,5}, so a decode mask weakened from `& 31` to `& 15`, `& 7` or `& 3`
#  scored 58/58 (`& 1` did not: the old edge row's BA 2 -> 0 read CR[0] = 1 and BB 3 -> 1 read CR[1] = 0, so crandc wrote 1 for a
#  want of 0; pass 2, F2).  Here BA and BB are >= 16 and every proper-submask alias of each (index & 15, & 7, & 3, & 1) holds the
#  OPPOSITE value, so a weakened mask reads a flipped input and the result flips.  crandc: BA=31 (1), BB=30 (0) -> 1, its aliases
#  15, 7, 3, 1 = 0 and 14, 6, 2, 0 = 1, BT=20 pre-set 0.  crorc: BA=29 (0), BB=28 (1) -> 0, its aliases 13, 5, 1 = 1 and 12, 4, 0
#  = 0, BT=21 pre-set 1.  Two sessions: the two alias sets disagree at bits 0 and 1.
def hi_row(name, op, bt, ba, bb, ones, zeros, want):
    seed = 0
    for n in ones:
        seed = setbit(seed, n, 1)
    for n in zeros:
        seed = setbit(seed, n, 0)
    seed = setbit(seed, bt, 1 - want)
    hregs, _, _, hhow = session(seed, [XL(op, bt, ba, bb), MFCR(10)])
    hcr = hregs.get("cr", -1)
    row(name, crbit(hcr, bt) if (hhow == "exit0" and hcr >= 0) else -1, want,
        "BA=%d BB=%d BT=%d, every submask alias opposite" % (ba, bb, bt))


hi_row("64 crandc hi", "crandc", 20, 31, 30, ones=[31, 14, 6, 2, 0], zeros=[30, 15, 7, 3, 1], want=1)
hi_row("64 crorc hi", "crorc", 21, 29, 28, ones=[28, 13, 5, 1], zeros=[29, 12, 4, 0], want=0)

# ================================ ROUND-2 PINS: whole-site field masks, the BB read of CR[BT], read-before-clear order ==
#  Derived by simulation (regress/artifacts/ppccrandcorc/r2_20261105/CLOSURE.md, v575b.py).  A source at index 31 over a UNIFORM
#  CR[0..30] opposite to CR[31] makes every mask m in 0..30 at that site (31 & m = m) read a flipped input, with the other
#  operand decisive -- when the seed IS uniform: `64 crorc bamask' pre-sets its destination CR[16] EQUAL (0), so its seed
#  0xffff7ffe is not uniform at 16 and mask 16 does not flip there (red on `64 crorc 11' instead; pass 3, R1, which corrected
#  the round-2 sentence "makes every mask m in 0..30 at that site ... read a flipped input" as it stood without this caveat).
#  Pre-setting CR[BT] to the INVERSE hides a BB read of CR[BT] on every row (it reads 1-want, and a & want = want, a | want =
#  want), so two of these rows pre-set CR[BT] EQUAL to the result instead.  BT == BB with b = 1 and want 0 is one aliasing
#  shape whose result changes when the clear precedes the reads.  ROUND 2 WROTE HERE "(BT == BA is a fixed point for both
#  handlers under the pre-set discipline)": that holds for an INVERSE pre-set only.  With an EQUAL pre-set, crandc 16,16,31
#  over 0xfffffffe (a = CR[16] = 1, b = 0, want 1) sees the early clear (a -> 0) AND every BB alias, BB <- BT and the BB read
#  masks: ONE crandc row would have closed what `64 crandc bbmask' and `64 crandc order' close together, so the four rows below
#  are NOT the minimum (pass 3, R2).  They are kept as they are: table 2 measured them (r2_20261105/table2/SCORES.txt).
#    64 crandc bbmask: crandc 16,5,31 over 0xfffffffe: a = 1, b = CR[31] = 0 -> 1; CR[16] pre-set 1 (EQUAL).  Every BB alias and
#                      CR[BT] read 1 (b = 1 -> 0); the read mask & 3 / & 7 sees CR[30] = 1 (& 3 gives bb = 2, & 7 gives bb = 6;
#                      round 2 wrote "bb = 2" for both: pass 3, R3; either way !bb = 0 -> 0).
#    64 crandc order:  crandc 9,5,9 over bits 5 and 9: a = b = 1 -> 0; CR[9] pre-set 1 (inverse).  Clearing CR[9] before the
#                      reads makes b = 0 and the result 1.
#    64 crorc bamask:  crorc 16,31,5 over 0xffff7ffe: a = CR[31] = 0, b = 1 -> 0; CR[16] pre-set 0 (EQUAL).  Every BA alias but
#                      16 (= BT; `64 crorc 11' covers m = 16) and a BB read of CR[BT] give 1; a toggle instead of the clear gives 1.
#    64 crorc bbmask:  crorc 31,5,31 over 0x00000001: a = 0, b = CR[31] = 1 -> 0; CR[31] pre-set 1 (inverse, = the source).
#                      Every BB alias reads 0 (-> 1); clearing CR[31] before the reads makes b = 0 and the result 1.
def pin_row(name, op, bt, ba, bb, seed, want, note):
    pregs, _, _, phow = session(seed, [XL(op, bt, ba, bb), MFCR(10)])
    pcr = pregs.get("cr", -1)
    row(name, crbit(pcr, bt) if (phow == "exit0" and pcr >= 0) else -1, want, note)


pin_row("64 crandc bbmask", "crandc", 16, 5, 31, setbit(0xFFFFFFFF, 31, 0), 1, "BB=31 over CR[0..30]=1; CR[16] pre-set EQUAL (1)")
pin_row("64 crandc order", "crandc", 9, 5, 9, setbit(setbit(0, 5, 1), 9, 1), 0, "BT=BB=9, a=b=1: the reads precede the clear")
pin_row("64 crorc bamask", "crorc", 16, 31, 5, setbit(setbit(0xFFFFFFFF, 31, 0), 16, 0), 0, "BA=31 over CR[0..30]=1; CR[16] pre-set EQUAL (0)")
pin_row("64 crorc bbmask", "crorc", 31, 5, 31, setbit(0, 31, 1), 0, "BT=BB=31 over CR[0..30]=0; the reads precede the clear")

# ================================= ROUND-3 WHOLE-CR ROWS: the read-mask constant, the set literal (pass 3, codex B1-B4) ==
#  Derived by simulation (regress/artifacts/ppccrandcorc/r3_20261105/CLOSURE3.md, v575c.py).  Each row compares the WHOLE CR
#  (the register dump, which must agree with mfcr r10) with the architectural CR, so a SET of any extra bit is seen -- a row
#  that checks only its destination cannot see one (codex B3-B4).  A read `(cr >> (31-x)) & m' with x = 31 shifts by 0, so
#  `& m' reads CR & m: one row with CR[0..30] = 1 (but the pre-set) sees EVERY mask m with a bit above bit 0 at that site.
#    64 crorc baread:   crorc 17,31,5 over 0xfffffffe: a = CR[31] = 0, b = CR[5] = 1 -> 0; CR[17] pre-set 1 (inverse).  Any BA
#                       read mask with a bit in 1..31 reads nonzero and gives 1 (B2's & 0x8001 reads CR[16] = 1 here, which
#                       `64 crorc bamask' holds at 0); every BA field mask 0..30, mask 16 included, reads CR[m] = 1 -> 1.
#    64 crorc bbread:   crorc 30,30,31 over 0xfffffffc: a = CR[30] = 0, b = CR[31] = 0 -> 1 at CR[30] (pre-set 0, inverse, and
#                       the a = 0 source at once).  Any BB read mask with a bit in 2..31 reads nonzero, !bb = 0 -> 0 (B1, k =
#                       2..31); bit 1 (& 3, & 7) is red on `64 crorc 00', whose BB = 2 read is 2.
#    64 crandc setbits: crandc 31,30,31 over 0x00000002: a = CR[30] = 1, b = CR[31] = 0 -> 1 at CR[31]; the set shifts by 0,
#                       so a literal 1+2^k also sets CR[31-k], a zero for k = 2..31 (B3); k = 1 lands on the source CR[30] = 1
#                       and is red on `64 crandc 01' (crandc 10,1,0 re-sets CR[9]).
#    64 crorc setbits:  crorc 31,0,31 over 0: a = b = 0 -> 1 at CR[31]; a literal 1+2^k sets CR[31-k], a zero for every k (B4).
def cr_row(name, op, bt, ba, bb, seed, want_cr, note):
    cregs, _, _, chow = session(seed, [XL(op, bt, ba, bb), MFCR(10)])
    ccr, cmf = cregs.get("cr", -1), cregs.get(10, -1)
    if chow != "exit0" or ccr < 0:
        got = "none"
    elif cmf != ccr:
        got = "cr=%s mfcr=%s" % (hex(ccr), hex(cmf))
    else:
        got = hex(ccr)
    row(name, got, hex(want_cr), note)


cr_row("64 crorc baread", "crorc", 17, 31, 5, 0xFFFFFFFE, 0xFFFFBFFE, "BA=31 over 0xfffffffe, whole CR: a=0 at the fix; a!=0 is red")
cr_row("64 crorc bbread", "crorc", 30, 30, 31, 0xFFFFFFFC, 0xFFFFFFFE, "BT=BA=30, BB=31 over 0xfffffffc, whole CR: bb=0")
cr_row("64 crandc setbits", "crandc", 31, 30, 31, 0x00000002, 0x00000003, "BT=31 over CR[30] only, whole CR: no extra set bit")
cr_row("64 crorc setbits", "crorc", 31, 0, 31, 0x00000000, 0x00000001, "BT=31 over 0, whole CR: no extra set bit")

# ================================================ THE TWO HANDLERS, 32-BIT ===
score_table("32", *table("32", ["crandc", "crorc"], 8, cpu="PPC603"), control=False)

# ===================================================================== RESULT ==
n_ok = sum(1 for _, ok in rows if ok)
ctl_ok = all(ok for _, ok in controls)
print("elapsed %.1fs" % (time.time() - t0))
print("PPC_CRLOGIC_RESULT=%d/%d" % (n_ok, len(rows)))
print("PPC_CRLOGIC_CONTROL=%s" % ("OK" if ctl_ok else "FAIL"))
print("PPC_CRLOGIC_PROBE_DONE")
