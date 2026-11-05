Begin your answer with the token MYTHOSREG575 on its own line, then `model: <your model name>`, then your verdict line.  You may
open files under C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/ READ-ONLY to check a claim; write nothing, build nothing, run no git command
that writes.  Everything the review needs is inlined below.

# REGRESS REVIEW (the Fable-only stage) -- round #575 `ppccrandcorc`: the detector as it will ship

**PROJECT FRAMING -- this is a defensive software-robustness project.**  GXemul is a computer-architecture emulator: a developer tool
that runs legacy operating systems in a software sandbox for research and preservation.  This fork is a HARDENING effort -- ordinary
software-correctness engineering on the emulator's own C code, each fix shipped with a regression test that keeps it fixed.  There is
no attack, no target system and no affected third party; the guest is an OS image or a few instruction words under test INSIDE the
emulator, and the host is the emulator process on the developer's own machine.  This round corrects an INSTRUCTION-SEMANTICS defect:
two PowerPC condition-register instructions computed the wrong logical function.  **Vocabulary**: a *test variant* is a
deliberately broken copy of the fix used to measure whether the regression test notices it; *detected* means a row went red;
*undetected* means every row stayed green; *EQUIVALENT* means the edit cannot change any result; a *null medium* is a run with no
working emulator behind the probe (a non-emulator binary, a missing one) or, for an instruction handler, a body that writes nothing.

**Your role: the flagship's REGRESS review**, the fable5 slot's step (owner, 2026-11-05: Mythos is that slot).  By standing owner
directive only the flagship seat reviews the `regress` stage.  The round: `src/cpus/cpu_ppc_instr.c`, X(crandc) and X(crorc) set
CR[BT] on !(ba & bb) and !(ba | bb) -- NAND and NOR -- where PowerPC Book I v2.01 (_scratchpad/ppc_uisa_book1_v201.txt:1909-1914)
defines CR[BA] & ~CR[BB] and CR[BA] | ~CR[BB].  The fix (block G) is the two condition lines and nothing else, as YOUR pass-1
ruling ordered (block F1, R1/R10).  The detector is regress/ppc_crlogic_probe.py (70 rows; block A), wired into gate 13 (block B).
Its repair chain ran passes 2, 3 and 4 with two repairs between them; pass 4 found zero floor breaches over a 453-cell enumeration
and five false records, which your records correction fixed; GPT-6 Astra's second reading then found three of those corrections
carrying NEW universal claims, and the main loop qualified them in place (block E: CLOSURE3.errata.md and RECORDS4_NOTE.md).  NO
SEAT HAS READ THE QUALIFIED SENTENCES; this review is the first reading of them.  This review is of the WHOLE detector as it will
land, and of the records that describe it.

Mark each claim CHECKED-IN-PACKET (block + line), CHECKED-IN-TREE (file:line you opened), REASONED, or UNSETTLED (name the one
measurement that settles it -- the main loop runs it).  A finding is fixed in this round only if it is a floor breach (L2), an
undischarged obligation (L3) or a wrong record (L4); everything else is FILED with its warrant.  Rows are owed per enumerated wrong
version of the fix inside the DEPENDS-ON bound (the predicates dominating the edited lines, walked to the enclosing function; operand
swaps only from fields the guarded body reads), never per possible state; a filter may reject or repair a row, never demand one
outside the bound.  Count the arguments, not the seats: an agreement that only restates the packet's own premise is no evidence.

**Write your answer in this order** (it is banked as regress/artifacts/ppccrandcorc/regress_20261105/MYTHOS_REGRESS.md):
1. Evidence basis (which blocks and which files you opened).
2. The vacuity floor, clause by clause, each with the artifact that discharges it or the breach: (a) the pre-fix build fails;
   (b) a verbatim reinstatement of the removed defect at EVERY fixed site fails (b1, b2 in block C); (c) a null medium fails -- which
   rows, which pins (the dead binaries AND the handlers' identity bodies, c_identity); (d) null-repair -- each operand and operator
   the two fixed conditions depend on, weakened to the least-restrictive form that still reads like the same check, and any such
   variant the tables lack (the 453-cell closure is block E; say whether its DEPENDS-ON reading is right and whether a cell is
   missing); (e) the contract in the docstring (catches / deliberately uncovered): true as written, and complete for what the
   tables measured; (f) anchors -- which rows pin WHICH bit changed rather than only that something did.
3. Gate 13's #575 block (block B): does every pin red under (i) a dead probe, (ii) a probe that silently loses rows, (iii) a probe
   that adds a row, (iv) a probe whose sentinel prints but whose RESULT line is missing?  Name any pin that cannot fail.  Block H
   is the block replayed over table 3's banked logs: does it show what it claims?
4. The test-variant tables (blocks C, D): is any row VACUOUS by construction (its observable cannot vary under the variant it is
   meant to catch)?  Is any listed detection explained by a different row than the record claims?  Are the deliberately uncovered
   cells correctly disclosed -- the 36 EQUIVALENT ones (proved?), the crandc clear replaced by a toggle (DISCLOSED, not equivalent),
   field masks with a bit above bit 4 (outside the denominator, F1), and an extra CLEAR of a bit that is neither a source nor a
   destination (not claimed)?
5. Records: wrong numbers or claims in the docstring (block A), the gate comment (block B), the PRETABLE predictions (block D), the
   table verdicts and errata (block C), and above all the QUALIFIED F1, F2 and F4 sentences in block E, which no seat has read.
6. The main loop's dispositions (block F): which accepted disposition is wrong?  Counted: pass 2 -- codex's 9 floor breaches and 7
   false records, and GLM's 4 breaches (2 the same cells as codex's B3-B4, 1 proved EQUIVALENT, 1 new: table 2's g1) and 1 false
   record, all dispositioned in repair 2; pass 3 -- 54 breaches and 7 false records, all accepted (54 confirmed by simulation);
   pass 4 -- 0 breaches and 5 false records, all accepted; the second reading -- 2 accepted and 3 qualified.  The two Gemini answers
   that said CLOSE at pass 3 were discounted as restating the packet's premise: is that right?
7. Which of your own findings is weakest, and what would overturn it.
Final line: `MYTHOSREG575: <n> CHECKS <b> FLOOR-BREACHES <r> RECORD-FINDINGS VERDICT:<REGRESS-CLEAN|REGRESS-WITH-FINDINGS|REGRESS-BREACH>`

---

### A. the probe as it will ship (regress/ppc_crlogic_probe.py, the staged copy: the working copy with seven score-shaped docstring strings in words; landing_20261105/PROBE_IDENTITY.md proves the syntax tree minus the docstring unchanged)

```
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
      destination -- the table seeds hold no ones there, the hi and round-2 pin sessions check only the destination, and the
      round-3 whole-CR rows carry ones only where the set-literal cells need zeros (CLOSURE3.md's appendix lists what they
      see incidentally: most crorc clear literals 1+2^k, k = 1..30, and no crandc one above k = 10); and a crandc body that
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
```

### B. gate 13's #575 block (the staged regress/gate_ppc.sh: HEAD's file plus exactly this block)

```
# ---- ppccrandcorc (#575): crandc and crorc computed NAND and NOR -- its 70-row rung-3 detector ---------------------------------------
# X(crandc) and X(crorc) set CR[BT] on !(CR[BA] & CR[BB]) and !(CR[BA] | CR[BB]); PowerPC Book I v2.01 defines CR[BA] & ~CR[BB] and
# CR[BA] | ~CR[BB].  `-E bareppc -M 64` (PPC970) and `-C PPC603` run each CR logical instruction on a real guest through the real
# decoder, CR seeded from the debugger; the truth-table, edge and `hi' rows pre-set the destination to the INVERSE of the
# architectural result, two round-2 rows pre-set it EQUAL (the only way a BB read of CR[BT] shows), and the four round-3 rows
# compare the whole CR (round 3 corrected "every destination pre-set to the INVERSE": pass 3, R7); the five correct siblings run
# the same table as controls; edge rows pin BT 0 and 31; two rows pin the BA/BB field masks with every submask alias seeded
# opposite; four round-2 rows close every field mask 0..30, the BB read of CR[BT] and the read-before-clear order (the closure by
# simulation: regress/artifacts/ppccrandcorc/r2_20261105/CLOSURE.md, 239 cells); four round-3 whole-CR rows close the read-mask
# constants and the set literals (r3_20261105/CLOSURE3.md, 453 cells: 56 escaped the 66 rows, 0 escape the 70).  BEFORE the NetBSD
# prerequisite, like the blocks above.  Test-variant tables: regress/artifacts/ppccrandcorc/table1_20261105/, r2_20261105/ and
# r3_20261105/ (the pass-1 ruling: regress/artifacts/ppccrandcorc/adj_p1_20261105/).
CLLOG=$LOGDIR/ppc_crlogic.log
python3 -u ppc_crlogic_probe.py "$PMAX" gate > "$CLLOG" 2>&1 || true
if [ "$(grep -cx 'PPC_CRLOGIC_PROBE_DONE' "$CLLOG")" != 1 ]; then
    note "ppc_crlogic: completion sentinel missing or duplicated; last lines follow"
    tail -5 "$CLLOG" | sed 's/^/       /'
    check "ppc_crlogic probe completed" "no" "yes"
else
    check "ppc_crlogic probe completed" "yes" "yes"
    check "ppc_crlogic sentinel is the last line" "$(tail -n 1 "$CLLOG")" "PPC_CRLOGIC_PROBE_DONE"
    for k in RESULT CONTROL; do
        check "ppc_crlogic $k= lines" "$(grep -c "^PPC_CRLOGIC_$k=" "$CLLOG")" "1"
    done
    check "ppc_crlogic RESULT=70/70" "$(grep -cx 'PPC_CRLOGIC_RESULT=70/70' "$CLLOG")" "1"
    check "ppc_crlogic CONTROL=OK"   "$(grep -cx 'PPC_CRLOGIC_CONTROL=OK' "$CLLOG")" "1"
    for v in "ctl session" "ctl live" "ctl seed holds" "ctl cr seed" "ctl mfcr" "neg apparatus" "64 session" "64 crandc 00" "64 crandc 01" "64 crandc 10" "64 crandc 11" "64 crorc 00" "64 crorc 01" "64 crorc 10" "64 crorc 11" "64 others" "64 mfcr" "64 disasm" "s64 session" "s64 crand 00" "s64 crand 01" "s64 crand 10" "s64 crand 11" "s64 cror 00" "s64 cror 01" "s64 cror 10" "s64 cror 11" "s64 crnor 00" "s64 crnor 01" "s64 crnor 10" "s64 crnor 11" "s64 creqv 00" "s64 creqv 01" "s64 creqv 10" "s64 creqv 11" "s64 crxor 00" "s64 crxor 01" "s64 crxor 10" "s64 crxor 11" "s64 others" "s64 mfcr" "s64 disasm" "edge session" "edge crandc bt0" "edge crorc bt31" "edge others" "edge mfcr" "edge disasm" "64 crandc hi" "64 crorc hi" "64 crandc bbmask" "64 crandc order" "64 crorc bamask" "64 crorc bbmask" "64 crorc baread" "64 crorc bbread" "64 crandc setbits" "64 crorc setbits" "32 session" "32 crandc 00" "32 crandc 01" "32 crandc 10" "32 crandc 11" "32 crorc 00" "32 crorc 01" "32 crorc 10" "32 crorc 11" "32 others" "32 mfcr" "32 disasm"; do
        check "ppc_crlogic row: $v" "$(count "$CLLOG" "^$v  .*ok$")" "1"
    done
    clok=$(count "$CLLOG" " ok$"); clbad=$(count "$CLLOG" " FAIL$"); clrun=$((clok + clbad))
    check "ppc_crlogic rows run"   "$clrun" 70
    check "ppc_crlogic rows green" "$clok" 70
    check "ppc_crlogic rows red"   "$clbad" 0
fi
```

### C1. the test-variant scores: table 3 (r3_20261105/table3/SCORES.txt) whole, then the base/HEAD/null legs of tables 2 and 1

```
base [70 rows] 70/70 CONTROL=OK DONE=1 RED=none
HEAD [70 rows] 60/70 CONTROL=OK DONE=1 RED=64_crandc_00,64_crandc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,32_crandc_00,32_crandc_01,32_crorc_10,32_crorc_11
null_true [70 rows] 5/70 CONTROL=FAIL DONE=1 RED=65 rows (list elided)
null_absent [70 rows] none CONTROL=none DONE=0 RED=none
null_false [70 rows] 1/70 CONTROL=FAIL DONE=1 RED=69 rows (list elided)
b1_crandc_nand [70 rows] 65/70 CONTROL=OK DONE=1 RED=64_crandc_00,64_crandc_01,edge_crandc_bt0,32_crandc_00,32_crandc_01
b2_crorc_nor [70 rows] 65/70 CONTROL=OK DONE=1 RED=64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11
c_identity [70 rows] 44/70 CONTROL=OK DONE=1 RED=26 rows (list elided)
d1_crandc_nba_and_b [70 rows] 63/70 CONTROL=OK DONE=1 RED=64_crandc_01,64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_01,32_crandc_10
d2_crorc_nba_or_b [70 rows] 62/70 CONTROL=OK DONE=1 RED=64_crorc_01,64_crorc_10,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01,32_crorc_10
d3_crandc_and [70 rows] 62/70 CONTROL=OK DONE=1 RED=64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_10,32_crandc_11
d4_crorc_or [70 rows] 60/70 CONTROL=OK DONE=1 RED=64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01
d5_crandc_crossed [70 rows] 64/70 CONTROL=OK DONE=1 RED=64_crandc_00,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_11
d6_crorc_crossed [70 rows] 63/70 CONTROL=OK DONE=1 RED=64_crorc_00,64_crorc_11,edge_crorc_bt31,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_11
g1_crandc_bbread3 [70 rows] 68/70 CONTROL=OK DONE=1 RED=64_crandc_bbmask,64_crandc_setbits
g2_crandc_baread3 [70 rows] 70/70 CONTROL=OK DONE=1 RED=none
m10_crandc_bbmask17 [70 rows] 68/70 CONTROL=OK DONE=1 RED=64_crandc_bbmask,64_crandc_order
m1_crandc_mask7 [70 rows] 66/70 CONTROL=OK DONE=1 RED=64_crandc_hi,64_crandc_bbmask,64_crandc_order,64_crandc_setbits
m2_crorc_mask7 [70 rows] 66/70 CONTROL=OK DONE=1 RED=64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread
m3_crandc_mask15 [70 rows] 67/70 CONTROL=OK DONE=1 RED=64_crandc_hi,64_crandc_bbmask,64_crandc_setbits
m4_crorc_mask15 [70 rows] 66/70 CONTROL=OK DONE=1 RED=64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread
m5_crandc_bbmask29 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_bbmask
m6_crandc_bbmask27 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_bbmask
m7_crandc_bbmask23 [70 rows] 68/70 CONTROL=OK DONE=1 RED=64_crandc_bbmask,64_crandc_order
m8_crorc_bamask29 [70 rows] 68/70 CONTROL=OK DONE=1 RED=64_crorc_bamask,64_crorc_baread
m9_crorc_bbmask29 [70 rows] 68/70 CONTROL=OK DONE=1 RED=64_crorc_bbmask,64_crorc_bbread
o1_crandc_earlyclear [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_order
o2_crorc_earlyclear [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_bbmask
r1_crorc_bbread_k2 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_bbread
r2_crorc_bbread_k15 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_bbread
r3_crorc_bbread_k30 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_bbread
r4_crorc_bbread_k31 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_bbread
r5_crorc_baread_k15 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_baread
s1_crandc_bb_from_bt [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_bbmask
s2_crorc_bb_from_bt [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_bamask
t1_crandc_btmask7 [70 rows] 55/70 CONTROL=OK DONE=1 RED=64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others
t2_crorc_btmask7 [70 rows] 53/70 CONTROL=OK DONE=1 RED=17 rows (list elided)
u1_crandc_clear_ba [70 rows] 57/70 CONTROL=OK DONE=1 RED=64_crandc_00,64_crandc_01,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11,32_crorc_01,32_crorc_11,32_others
u2_crorc_clear_bb [70 rows] 60/70 CONTROL=OK DONE=1 RED=64_crorc_01,64_crorc_11,64_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,32_crorc_01,32_crorc_11,32_others
u3_crandc_set_bb [70 rows] 61/70 CONTROL=OK DONE=1 RED=64_crandc_10,64_crorc_01,64_others,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10,32_crorc_01,32_others
u4_crorc_set_ba [70 rows] 58/70 CONTROL=OK DONE=1 RED=64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10,32_crorc_11,32_others
u5_crandc_clear_rbt [70 rows] 62/70 CONTROL=OK DONE=1 RED=64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11
u6_crorc_set_rbt [70 rows] 58/70 CONTROL=OK DONE=1 RED=64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10,32_crorc_11,32_others
u7_crandc_midclear [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_order
u8_crorc_midclear [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_bbmask
u9_crorc_swap [70 rows] 70/70 CONTROL=OK DONE=1 RED=none
x1_crandc_setlit_k7 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_setbits
x2_crandc_setlit_k19 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_setbits
x3_crandc_setlit_k30 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_setbits
x4_crandc_setlit_k31 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crandc_setbits
x5_crorc_setlit_k26 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_setbits
x6_crorc_setlit_k27 [70 rows] 69/70 CONTROL=OK DONE=1 RED=64_crorc_setbits
z0_crorc_bbread0 [70 rows] 64/70 CONTROL=OK DONE=1 RED=64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01
z2_crandc_bbread2 [70 rows] 65/70 CONTROL=OK DONE=1 RED=64_crandc_11,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_11
z4_crorc_baread4 [70 rows] 65/70 CONTROL=OK DONE=1 RED=64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11
z6_crandc_baread6 [70 rows] 65/70 CONTROL=OK DONE=1 RED=64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10
restored [70 rows] 70/70 CONTROL=OK DONE=1 RED=none


(table 2, its base, HEAD and null legs; its 27 variants are table 3's first 27)
base [66 rows] 66/66 CONTROL=OK DONE=1 RED=none
HEAD [66 rows] 56/66 CONTROL=OK DONE=1 RED=64_crandc_00,64_crandc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,32_crandc_00,32_crandc_01,32_crorc_10,32_crorc_11
null_true [66 rows] 5/66 CONTROL=FAIL DONE=1 RED=61 rows (list elided)
null_absent [66 rows] none CONTROL=none DONE=0 RED=none
null_false [66 rows] 1/66 CONTROL=FAIL DONE=1 RED=65 rows (list elided)
c_identity [66 rows] 44/66 CONTROL=OK DONE=1 RED=22 rows (list elided)
restored [66 rows] 66/66 CONTROL=OK DONE=1 RED=none

(table 1, the same legs; its 15 variants are table 3's first 15)
base [62 rows] 62/62 CONTROL=OK DONE=1 RED=none
HEAD [62 rows] 52/62 CONTROL=OK DONE=1 RED=64_crandc_00,64_crandc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,32_crandc_00,32_crandc_01,32_crorc_10,32_crorc_11
null_true [62 rows] 5/62 CONTROL=FAIL DONE=1 RED=57 rows (list elided)
null_absent [62 rows] none CONTROL=none DONE=0 RED=none
null_false [62 rows] 1/62 CONTROL=FAIL DONE=1 RED=61 rows (list elided)
c_identity [62 rows] 42/62 CONTROL=OK DONE=1 RED=20 rows (list elided)
restored [62 rows] 62/62 CONTROL=OK DONE=1 RED=none
```

### C2. the table verdicts and their dated errata

# #575 ppccrandcorc -- test-variant TABLE 3 (repair 3: the full single-constant closure, 70 rows), 2026-11-05 ~08:43-08:59Z

Driver `../table3_575.run.sh` (frozen copy of table3_575.sh), WSL scratch clone /tmp/gx575t3 under a clone-local .MUTANT; restored,
cmp-clean against GXEMUL-SEC, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument `probe70_frozen.py`, cmp-identical to the
in-tree probe and to `../base70/probe70_run.py` (70/70 on build/, CLEARANCE.txt part 1 and part 2 OK).  `../PRETABLE_3.out` (every
prediction EXACT, computed by `../v575c.py`, which first reproduces all 29 table-2 legs) is older than every file in this directory.
Scores: SCORES.txt (57 lines).

* base 70/70 CONTROL=OK; HEAD 60/70 on exactly the 10 predicted rows (the eight table rows where NAND/NOR differ from ANDC/ORC -- crandc 00
  and 01, crorc 10 and 11, each in the 64- and 32-bit sessions -- plus the two edge rows).  Null media: /bin/true 5/70 and /bin/false 1/70, each CONTROL=FAIL; an absent binary: the probe raises before any row (no
  RESULT line, CONTROL=none, DONE=0), as predicted.
* ALL 51 VARIANTS EXACTLY AS PREDICTED -- 53 of 53 predicted lines (base, HEAD, 51 variants) match their red sets row for row, 0
  misses: table 2's 27 re-created (26 red, g2 green as the proved equivalent); and the 24 repair-3 representatives -- crorc's BB read
  widened by one bit at k = 2, 15, 30, 31 and its BA read `& 0x8001` (red on `64 crorc bbread` / `baread`), crandc's set literal
  `1 + 2^k` at k = 7, 19, 30, 31 and crorc's at k = 26, 27 (red on `64 crandc setbits` / `64 crorc setbits`), one read mask of 0/2/4/6
  per site, the eight non-equivalent structural cells, and the crorc read swap green as the proved equivalent.
* The four R5 bt-substitutions are predictions only (PRETABLE_2.errata.md); they were not built, as the pass-1 ruling allowed.

# #575 ppccrandcorc -- test-variant TABLE 2 (repair 2: 66 rows, the class closure), 2026-11-05 ~08:1xZ (02:1x local)

Driver `../table2_575.run.sh` (frozen copy), WSL scratch clone /tmp/gx575t2 under a clone-local .MUTANT sentinel; restored, cmp-clean
against GXEMUL-SEC, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument `probe66_frozen.py` == the in-tree probe after repair 2
(cmp-identical to base66/probe66_run.py, 66/66 on build/).  `../PRETABLE_2.out` (02:08:00 local) predates every file in this directory
(the earliest, MD5.txt, 02:10:46); its predictions were computed by `../v575b.py`, the extended simulator whose 62-row re-derivation
reproduces table 1's 17 legs, over the closure of `../CLOSURE.md` (239 cells).  Scores: SCORES.txt (red sets read off the FAIL rows).

* base 66/66, CONTROL=OK.  HEAD 56/66: the ten DISC rows, as predicted.
* All 27 variants scored EXACTLY their predicted red sets (29 of 29 runs with base and HEAD): 26 red; g2 (crandc's BA read mask
  widened to `& 3`) green, as PRETABLE_2 predicted -- proved EQUIVALENT there (with `!bb` in {0,1}, `ba & !bb` reads only ba's low bit).
  The new variants are the pass-2 classes: s1/s2 (BB reads CR[BT]), o1/o2 (the clear moved before the source reads), m5-m10 (single-
  bit field masks, codex's B5-B9 and one more), g1 (crandc's BB read mask `& 3`) and the rest of CLOSURE.md's cell classes.
* Null media: /bin/true 5/66 CONTROL=FAIL; /bin/false 1/66 CONTROL=FAIL; an absent binary stops the probe before any row with no
  sentinel (the gate's first check reds it).

# table2/VERDICT.md -- errata (2026-11-05, round 3; pass 3 = ../../p3_20261105/codex_codex_r575_p3.txt)

VERDICT.md is the measurement record of table 2 and is not rewritten (nor SCORES.txt, MD5.txt or TABLE.log).  Each item quotes
what it corrects.  No score changes.

## R4 -- m5-m10 are not all single-bit field masks

VERDICT.md says:

> m5-m10 (single-bit field masks, codex's B5-B9 and one more)

Five of the six remove one bit of the 5-bit field mask `& 31` (11111): m5 crandc BB `& 29` (11101) and m8 crorc BA `& 29`, m9 crorc
BB `& 29` remove bit value 2; m6 crandc BB `& 27` (11011) removes 4; m7 crandc BB `& 23` (10111) removes 8.  m10 crandc BB `& 17`
(10001) removes THREE bits, values 2, 4 and 8.  Correct reading: "m5-m9 single-bit field masks (codex's B5-B9); m10 a three-bit one".
The predictions and scores of all six are unaffected (SCORES.txt; ../PRETABLE_2.out).

## R5 -- the earliest file in table2/ is not MD5.txt

VERDICT.md says:

> `../PRETABLE_2.out` (02:08:00 local) predates every file in this directory (the earliest, MD5.txt, 02:10:46)

The earliest file in table2/ is probe66_frozen.py, 02:10:35.403 local (08:10:35.403Z); then cpu_ppc_instr.c.fix575, 02:10:46.645;
then MD5.txt, 02:10:46.732 (ls --full-time, 2026-11-05).  PRETABLE_2.out, 02:08:00.006, predates all three, so the claim that the
predictions precede the table stands; only the parenthetical naming MD5.txt as the earliest file was false.

# #575 ppccrandcorc -- test-variant TABLE 1 (62 rows), 2026-11-05 07:4xZ (01:4x local)

Driver `../table1_575.run.sh` (frozen copy), WSL scratch clone /tmp/gx575t under a clone-local .MUTANT sentinel; restored, cmp-clean
against GXEMUL-SEC, rebuilt fresh, sentinel cleared (TABLE.log, last lines).  Instrument `probe62_frozen.py` == the in-tree probe after
apply_r575.py (cmp-identical to base62/probe62_run.py, which scored 62/62 on build/).  `../PRETABLE.out` was written before the driver
(the only older file here is the frozen probe, copied first); its predictions are EXACT and were COMPUTED by `../v575.py`, a simulator of
the probe's sessions.  Scores: SCORES.txt (red sets read off each run's FAIL rows; the probe prints no RED line).

* base 62/62, CONTROL=OK.  HEAD (impl_20261105/cpu_ppc_instr.c.pre575) 52/62, CONTROL=OK: exactly the ten predicted rows (64/32 crandc
  00, 01; 64/32 crorc 10, 11; edge crandc bt0; edge crorc bt31) -- the same ten as the 10-29 witness (witness_20261029/WITNESS_head.out).
* All 15 variants scored EXACTLY their predicted red sets (17 of 17 including base and HEAD):
  b1 crandc NAND restored, b2 crorc NOR restored -- 5 each; c identity bodies (the ruled null medium of the two handlers) -- 20;
  d1-d6 (operand complement moved, dropped, operator crossed) -- 5 each, the four the ruling listed per variant plus a hi row on d1-d4;
  m1-m4 (BA/BB mask & 7 and & 15) -- 1 each, the hi row of that handler ONLY (the owed rows' whole reason: 58/58 before them);
  t1, t2 (BT mask & 7) -- 13 each.
* Null media: /bin/true 5/62 CONTROL=FAIL; /bin/false 1/62 CONTROL=FAIL; an absent binary raises FileNotFoundError in the probe before
  any row and prints no sentinel (probe_null_absent.out) -- the gate's first check (the completion sentinel) reds it.

# VERDICT.errata.md -- correction to VERDICT.md (#575 ppccrandcorc, table 1), dated 2026-11-05 (round 2)

VERDICT.md is a historical record and is NOT rewritten.  The correction comes from pass 2 (p2_20261105/codex_codex_r575_p2.txt F6)
and was checked against adj_p1_20261105/MYTHOS_local.md (the R5 table) and SCORES.txt.

## F6 -- "the four the ruling listed per variant"

VERDICT.md lines 12-13 say: "d1-d6 (operand complement moved, dropped, operator crossed) -- 5 each, the four the ruling listed
per variant plus a hi row on d1-d4".

Correction: the pass-1 ruling's R5 table did not list four rows for every d variant.  It listed FOUR for d1-d4 (64/32 crandc 01, 10;
64/32 crorc 01, 10; 64/32 crandc 10, 11; 64/32 crorc 00, 01) and FIVE for d5 and d6 (64/32 crandc 00, 11 plus edge crandc bt0;
64/32 crorc 00, 11 plus edge crorc bt31).  The measured 5-each (SCORES.txt lines 9-14) therefore decomposes as:

    d1-d4: the ruling's four rows plus that handler's `hi` row (the ruling wrote the table before the hi rows existed, and its
           parenthetical "the owed rows stay green under all nine" is false for c and d1-d4 -- SCORES.txt lines 8-12);
    d5-d6: the ruling's five rows, unchanged (the hi rows stay green: (1,0) and (0,1) are not fixed points of the crossed
           operator for the 00/11 cells, but the hi inputs (1,0) -> 1|!0 = 1 and (0,1) -> 0&!1 = 0 equal the wants).

Nothing else in VERDICT.md changes: 15 of 15 variants red, 17 of 17 legs exactly as predicted, the null-media and HEAD lines stand.

### D. table 3's predictions, written before its run (r3_20261105/PRETABLE_3.out)

```
PRETABLE_3 -- #575 ppccrandcorc, test-variant table 3 (70 rows).  Written BEFORE table 3 runs.  Instrument: the in-tree
probe regress/ppc_crlogic_probe.py after round 3 (r3_20261105/base70/probe70_run.py is its frozen copy).  Baseline: the fix
(GXEMUL-SEC src/cpus/cpu_ppc_instr.c).  Every prediction below is EXACT and COMPUTED by r3_20261105/v575c.py (`pretable3'),
whose 66-row re-derivation matches table 2's PRETABLE_2.out on all 29 legs (`check66').  Only the apparatus rows (ctl*, neg
apparatus, *session, *mfcr, *disasm) are predicted green unconditionally; bit rows, `others' rows and the four round-3 whole-CR
rows are computed.  Null media: /bin/true and /bin/false: CONTROL=FAIL; an absent binary: the probe raises before any row, no
sentinel, CONTROL=none, DONE=0.  The control session's seed below is the probe's REAL CTL_CR (PRETABLE_2 printed 0: pass 3, R6).

ROW MANIFEST (session: seed; instructions as op BT,BA,BB; rows):
  ctl               seed=0x12345678  (apparatus)
                    rows: ctl session, ctl live, ctl seed holds, ctl cr seed, ctl mfcr, neg apparatus
  64                seed=0x50d40000  crandc 8,0,2  crandc 9,0,1  crandc 10,1,0  crandc 11,1,3  crorc 12,0,2  crorc 13,0,1  crorc 14,1,0  crorc 15,1,3
                    rows: 64 session, 64 crandc 00, 64 crandc 01, 64 crandc 10, 64 crandc 11, 64 crorc 00, 64 crorc 01, 64 crorc 10, 64 crorc 11, 64 others, 64 mfcr, 64 disasm
  s64               seed=0x50e87690  crand 8,0,2  crand 9,0,1  crand 10,1,0  crand 11,1,3  cror 12,0,2  cror 13,0,1  cror 14,1,0  cror 15,1,3  crnor 16,0,2  crnor 17,0,1  crnor 18,1,0  crnor 19,1,3  creqv 20,0,2  creqv 21,0,1  creqv 22,1,0  creqv 23,1,3  crxor 24,0,2  crxor 25,0,1  crxor 26,1,0  crxor 27,1,3
                    rows: s64 session, s64 crand 00, s64 crand 01, s64 crand 10, s64 crand 11, s64 cror 00, s64 cror 01, s64 cror 10, s64 cror 11, s64 crnor 00, s64 crnor 01, s64 crnor 10, s64 crnor 11, s64 creqv 00, s64 creqv 01, s64 creqv 10, s64 creqv 11, s64 crxor 00, s64 crxor 01, s64 crxor 10, s64 crxor 11, s64 others, s64 mfcr, s64 disasm
  edge              seed=0x8c000000  crandc 0,2,3  crorc 31,4,5
                    rows: edge session, edge crandc bt0, edge crorc bt31, edge others, edge mfcr, edge disasm
  64 crandc hi      seed=0xa2020001  crandc 20,31,30
                    rows: 64 crandc hi
  64 crorc hi       seed=0x44040408  crorc 21,29,28
                    rows: 64 crorc hi
  64 crandc bbmask  seed=0xfffffffe  crandc 16,5,31
                    rows: 64 crandc bbmask
  64 crandc order   seed=0x04400000  crandc 9,5,9
                    rows: 64 crandc order
  64 crorc bamask   seed=0xffff7ffe  crorc 16,31,5
                    rows: 64 crorc bamask
  64 crorc bbmask   seed=0x00000001  crorc 31,5,31
                    rows: 64 crorc bbmask
  64 crorc baread   seed=0xfffffffe  crorc 17,31,5
                    rows: 64 crorc baread
  64 crorc bbread   seed=0xfffffffc  crorc 30,30,31
                    rows: 64 crorc bbread
  64 crandc setbits seed=0x00000002  crandc 31,30,31
                    rows: 64 crandc setbits
  64 crorc setbits  seed=0x00000000  crorc 31,0,31
                    rows: 64 crorc setbits
  32                seed=0x50d40000  crandc 8,0,2  crandc 9,0,1  crandc 10,1,0  crandc 11,1,3  crorc 12,0,2  crorc 13,0,1  crorc 14,1,0  crorc 15,1,3
                    rows: 32 session, 32 crandc 00, 32 crandc 01, 32 crandc 10, 32 crandc 11, 32 crorc 00, 32 crorc 01, 32 crorc 10, 32 crorc 11, 32 others, 32 mfcr, 32 disasm
  70 rows: ctl session | ctl live | ctl seed holds | ctl cr seed | ctl mfcr | neg apparatus | 64 session | 64 crandc 00 | 64 crandc 01 | 64 crandc 10 | 64 crandc 11 | 64 crorc 00 | 64 crorc 01 | 64 crorc 10 | 64 crorc 11 | 64 others | 64 mfcr | 64 disasm | s64 session | s64 crand 00 | s64 crand 01 | s64 crand 10 | s64 crand 11 | s64 cror 00 | s64 cror 01 | s64 cror 10 | s64 cror 11 | s64 crnor 00 | s64 crnor 01 | s64 crnor 10 | s64 crnor 11 | s64 creqv 00 | s64 creqv 01 | s64 creqv 10 | s64 creqv 11 | s64 crxor 00 | s64 crxor 01 | s64 crxor 10 | s64 crxor 11 | s64 others | s64 mfcr | s64 disasm | edge session | edge crandc bt0 | edge crorc bt31 | edge others | edge mfcr | edge disasm | 64 crandc hi | 64 crorc hi | 64 crandc bbmask | 64 crandc order | 64 crorc bamask | 64 crorc bbmask | 64 crorc baread | 64 crorc bbread | 64 crandc setbits | 64 crorc setbits | 32 session | 32 crandc 00 | 32 crandc 01 | 32 crandc 10 | 32 crandc 11 | 32 crorc 00 | 32 crorc 01 | 32 crorc 10 | 32 crorc 11 | 32 others | 32 mfcr | 32 disasm

VARIANTS (exact red sets on the 70 rows; table 2's 27 first, then the round-3 representatives):
   base                    0 red: none
   HEAD                   10 red: 64_crandc_00,64_crandc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,32_crandc_00,32_crandc_01,32_crorc_10,32_crorc_11
   b1_crandc_nand          5 red: 64_crandc_00,64_crandc_01,edge_crandc_bt0,32_crandc_00,32_crandc_01
   b2_crorc_nor            5 red: 64_crorc_10,64_crorc_11,edge_crorc_bt31,32_crorc_10,32_crorc_11
   c_identity             26 red: 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,edge_crandc_bt0,edge_crorc_bt31,64_crandc_hi,64_crorc_hi,64_crandc_order,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crandc_setbits,64_crorc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11
   d1_crandc_nba_and_b     7 red: 64_crandc_01,64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_01,32_crandc_10
   d2_crorc_nba_or_b       8 red: 64_crorc_01,64_crorc_10,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01,32_crorc_10
   d3_crandc_and           8 red: 64_crandc_10,64_crandc_11,64_crandc_hi,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_10,32_crandc_11
   d4_crorc_or            10 red: 64_crorc_00,64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01
   d5_crandc_crossed       6 red: 64_crandc_00,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_11
   d6_crorc_crossed        7 red: 64_crorc_00,64_crorc_11,edge_crorc_bt31,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_11
   m1_crandc_mask7         4 red: 64_crandc_hi,64_crandc_bbmask,64_crandc_order,64_crandc_setbits
   m2_crorc_mask7          4 red: 64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread
   m3_crandc_mask15        3 red: 64_crandc_hi,64_crandc_bbmask,64_crandc_setbits
   m4_crorc_mask15         4 red: 64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread
   t1_crandc_btmask7      15 red: 64_crandc_00,64_crandc_01,64_crandc_10,64_crandc_11,64_crorc_01,64_others,64_crandc_hi,64_crandc_order,64_crandc_setbits,32_crandc_00,32_crandc_01,32_crandc_10,32_crandc_11,32_crorc_01,32_others
   t2_crorc_btmask7       17 red: 64_crorc_00,64_crorc_01,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_01,32_crorc_10,32_crorc_11,32_others
   s1_crandc_bb_from_bt    1 red: 64_crandc_bbmask
   s2_crorc_bb_from_bt     1 red: 64_crorc_bamask
   o1_crandc_earlyclear    1 red: 64_crandc_order
   o2_crorc_earlyclear     1 red: 64_crorc_bbmask
   m5_crandc_bbmask29      1 red: 64_crandc_bbmask
   m6_crandc_bbmask27      1 red: 64_crandc_bbmask
   m7_crandc_bbmask23      2 red: 64_crandc_bbmask,64_crandc_order
   m8_crorc_bamask29       2 red: 64_crorc_bamask,64_crorc_baread
   m9_crorc_bbmask29       2 red: 64_crorc_bbmask,64_crorc_bbread
   m10_crandc_bbmask17     2 red: 64_crandc_bbmask,64_crandc_order
   g1_crandc_bbread3       2 red: 64_crandc_bbmask,64_crandc_setbits
   g2_crandc_baread3       0 red: none  [EQUIVALENT: proved; a 0-red run is the prediction]
   r1_crorc_bbread_k2      1 red: 64_crorc_bbread
   r2_crorc_bbread_k15     1 red: 64_crorc_bbread
   r3_crorc_bbread_k30     1 red: 64_crorc_bbread
   r4_crorc_bbread_k31     1 red: 64_crorc_bbread
   r5_crorc_baread_k15     1 red: 64_crorc_baread
   x1_crandc_setlit_k7     1 red: 64_crandc_setbits
   x2_crandc_setlit_k19    1 red: 64_crandc_setbits
   x3_crandc_setlit_k30    1 red: 64_crandc_setbits
   x4_crandc_setlit_k31    1 red: 64_crandc_setbits
   x5_crorc_setlit_k26     1 red: 64_crorc_setbits
   x6_crorc_setlit_k27     1 red: 64_crorc_setbits
   z0_crorc_bbread0        6 red: 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01
   z2_crandc_bbread2       5 red: 64_crandc_11,64_crandc_bbmask,64_crandc_order,64_crandc_setbits,32_crandc_11
   z4_crorc_baread4        5 red: 64_crorc_11,edge_crorc_bt31,64_crorc_bamask,64_crorc_baread,32_crorc_11
   z6_crandc_baread6       5 red: 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10
   u1_crandc_clear_ba     13 red: 64_crandc_00,64_crandc_01,64_crandc_11,64_crorc_01,64_crorc_11,64_others,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11,32_crorc_01,32_crorc_11,32_others
   u2_crorc_clear_bb      10 red: 64_crorc_01,64_crorc_11,64_others,64_crorc_hi,64_crorc_bbmask,64_crorc_baread,64_crorc_bbread,32_crorc_01,32_crorc_11,32_others
   u3_crandc_set_bb        9 red: 64_crandc_10,64_crorc_01,64_others,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10,32_crorc_01,32_others
   u4_crorc_set_ba        12 red: 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crorc_bt31,edge_others,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10,32_crorc_11,32_others
   u5_crandc_clear_rbt     8 red: 64_crandc_00,64_crandc_01,64_crandc_11,edge_crandc_bt0,64_crandc_order,32_crandc_00,32_crandc_01,32_crandc_11
   u6_crorc_set_rbt       12 red: 64_crorc_00,64_crorc_10,64_crorc_11,64_others,edge_crandc_bt0,edge_crorc_bt31,64_crorc_bbread,64_crorc_setbits,32_crorc_00,32_crorc_10,32_crorc_11,32_others
   u7_crandc_midclear      1 red: 64_crandc_order
   u8_crorc_midclear       1 red: 64_crorc_bbmask
   u9_crorc_swap           0 red: none  [EQUIVALENT: proved; a 0-red run is the prediction]

PREDICTED ONLY (not built; the pass-1 ruling R5 bt-substitutions):
   r5a_crandc_bt_and_nbb   4 red: 64_crandc_10,64_crandc_hi,64_crandc_bbmask,32_crandc_10
   r5b_crandc_ba_and_nbt   5 red: 64_crandc_10,64_crandc_hi,64_crandc_bbmask,64_crandc_setbits,32_crandc_10
   r5c_crorc_bt_or_nbb     6 red: 64_crorc_01,64_crorc_hi,64_crorc_bamask,64_crorc_bbmask,64_crorc_baread,32_crorc_01
   r5d_crorc_ba_or_nbt     4 red: 64_crorc_00,64_crorc_bbread,64_crorc_setbits,32_crorc_00
```

### E1. the closure (r3_20261105/CLOSURE3.md: its head, the four rows, the PROOF, what stays undetected, the contract)

```
# #575 ppccrandcorc -- CLASS CLOSURE BY SIMULATION, ROUND 3 (2026-11-05)

Simulator: r3_20261105/v575c.py (r2_20261105/v575b.py extended; `v575c.py check66' re-derives table 2's 27 predictions on
the 66 rows and matches r2_20261105/PRETABLE_2.out exactly, which licenses the extension).  Handlers simulated statement by
statement: src/cpus/cpu_ppc_instr.c X(crandc) :2729-2737 and X(crorc) :2756-2764; dispatch :4638 and :4641.

WHAT PASS 3 FOUND (p3_20261105/codex_codex_r575_p3.txt).  Round 2's enumeration had put the read-mask sites (:2732-2733,
:2759-2760) and the set statements (:2736, :2763) in scope with a vocabulary narrower than the class: read masks {& 3, & 7} only,
the set edited only to `deleted' and `^='.  This round enumerates the FULL single-constant family at those sites that codex
named (1+2^k at every read site and every set literal, {0,2,4,6} at every read site), adds k = 31 at the same sites (in bound:
the same constant sites, one more constant), the 16 structural cells of codex's denominator, and then PROVES the rest of the
2^32-constant space at each site by argument (section PROOF below), so the contract can name the whole site.

ENUMERATION (one edit per cell, per handler): round 2's 239 cells unchanged (field mask m in 0..30 at BT, BA, BB; each source
read taking another field's index; the read mask & 3 / & 7; the clear moved before the reads, deleted or toggled; the set
deleted or ^=; the condition edits; the dispatch re-bindings; c) PLUS: the read mask `& 1' -> `& (1|1<<k)' for k = 2..31 and
-> & 0, & 2, & 4, & 6 at each of the four read sites (34 x 4 = 136); the set literal `1' -> the unsigned constant 1+2^k,
k = 1..31, in each handler (31 x 2 = 62); and 16 structural cells: the clear's and the set's `(31-bt)' -> `(31-ba)' / `(31-bb)'
(ba, bb hold the READ VALUES there, so the edit addresses CR[a] / CR[b]) and -> `bt' (bit position bt = CR index 31-bt), the
clear moved between the two reads, and the two read statements swapped (8 x 2 = 16).

DENOMINATOR: 453 cells = 6 clear + 15 cond + 12 decode + 186 mask + 8 read + 8 rmask + 136 rmask3 + 4 set + 62 setlit + 16 struct.
codex's denominator was 447: the same cells without k = 31 at the four read sites (4 cells) and at the two set literals
(2 cells).  Its partition (357 detected, 35 equivalent, 54 breaches, 1 disclosed) is checked cell by cell below.

[... the 54 survivors, the 35 equivalents and the 453-cell CELL -> ROW MAP are in the file ...]
## THE 4 ROUND-3 ROWS (single-instruction sessions shaped like the `hi'/pin rows; each compares the WHOLE CR, from the
register dump and from mfcr r10, with the architectural CR)

  64 crorc baread   crorc BT=17 BA=31 BB=5 seed=0xfffffffe want CR=0xffffbffe  CR[BT] pre-set inverse (1)
  64 crorc bbread   crorc BT=30 BA=30 BB=31 seed=0xfffffffc want CR=0xfffffffe  CR[BT] pre-set inverse (0) = the BA source
  64 crandc setbits crandc BT=31 BA=30 BB=31 seed=0x00000002 want CR=0x00000003  CR[BT] pre-set inverse (0)
  64 crorc setbits  crorc BT=31 BA=0 BB=31 seed=0x00000000 want CR=0x00000001  CR[BT] pre-set inverse (0) = the BB source

  64 crorc baread   crorc 17,31,5 over 0xfffffffe: a = CR[31] = 0, b = CR[5] = 1 -> 0.  The BA read shifts by 0, so a = CR & m: every
                    mask m with ANY bit 1..31 set reads nonzero and gives 1 (codex B2's & 0x8001 reads CR[16] = 1 here; the
                    round-2 `64 crorc bamask' row has CR[16] = 0, its destination).  Also: every BA field mask 0..30 (CR[m] = 1),
                    mask 16 included, which repairs R1.
  64 crorc bbread   crorc 30,30,31 over 0xfffffffc: a = CR[30] = 0, b = CR[31] = 0 -> 1 at CR[30] (its own pre-set inverse 0 IS
                    the a = 0 source).  The BB read shifts by 0: every mask m with any bit 2..31 set reads nonzero, !bb = 0, 0
                    (B1, k = 2..31); bit 1 = CR[30] = 0 here, and `& 3' / `& 7' are red on `64 crorc 00' (its BB = 2 read is 2).
  64 crandc setbits crandc 31,30,31 over 0x00000002: a = CR[30] = 1, b = CR[31] = 0 -> 1 at CR[31]; the set shifts by 0, so a
                    literal 1+2^k also sets CR[31-k]: zero in the seed for k = 2..31 (B3 and k = 31); k = 1 lands on CR[30] = 1,
                    the source, and is red on `64 crandc 01' (crandc 10,1,0 sets CR[9] after `crandc 9' cleared it).
  64 crorc setbits  crorc 31,0,31 over 0: a = b = 0 -> 1 at CR[31]; every extra bit CR[31-k], k = 1..31, lands on a zero (B4).

WHY FOUR AND NO FEWER (single-instruction sessions).  The four open families need, respectively: (i) crorc with a = 0, b = 1,
result 0 and CR[16] = 1 (B2); (ii) crorc with a = 0, b = 0 (result 1) and CR[0..29] all 1 so that a BB read shifted by 0 has
bits 2..31 set (B1); (iii) crandc with result 1 and zeros at CR[BT-k] for k = 7, 9, 11..31 (B3); (iv) crorc with result 1 and
zeros at CR[BT-26], CR[BT-27] (B4).  (i) and (ii)/(iv) differ in the result; (ii) needs ones where (iv) needs zeros (the
extra set bits of (iv) at BT-26, BT-27 lie in 0..5 for any BT, inside (ii)'s ones at 0..29, and moving BT below 27 shifts
(iv)'s bits out); (iii) is crandc.  So no single instruction serves two families, and 4 rows is the minimum; a multi-
instruction session would cost more rows (session/others/mfcr/disasm), as the edge session shows.  (The round-2 rows are
kept as measured: they were not the minimum, see r2_20261105/CLOSURE.errata.md.)

## PROOF: the whole 2^32 constant space at the six sites (what the contract may claim beyond the enumerated cells)

A read is a = (cr >> (31-x)) & m with x the field index; call q = cr >> (31-x), whose bit j is CR[x-j] (j <= x, zero above).
  crandc BA (:2732):  the condition `ba & !bb' is bitwise with !bb in {0,1}, so only bit 0 of a counts.  m with bit 0 set:
                      EQUIVALENT (32 of them enumerated here).  m with bit 0 clear: a & 1 = 0, the result is always 0, red on
                      `64 crandc 10' (want 1).  Closed for every m.
  crandc BB (:2733):  `!bb' sees only bb != 0.  `64 crandc bbmask' (BB = 31, q = 0xfffffffe, want 1 needs bb = 0): any m with a
                      bit in 1..31 reads nonzero -> red.  m = 0: bb = 0 always, crandc becomes CR[BA], red on `64 crandc 11'.
                      Closed for every m != 1.
  crorc BA (:2759):   `ba | !bb' sees only a != 0.  `64 crorc baread' (BA = 31, q = 0xfffffffe, want 0 needs a = 0): any m with
                      a bit in 1..31 -> red.  m = 0: a = 0 always, crorc becomes !CR[BB], red on `64 crorc 11'.  Closed.
  crorc BB (:2760):   `64 crorc bbread' (BB = 31, q = 0xfffffffc, want 1 needs bb = 0): any m with a bit in 2..31 -> red; m
                      with bit 1: `64 crorc 00' (q = 2, want 1) -> red; m = 0: bb = 0 always, result always 1, red on
                      `64 crorc 01'.  Closed.
  set literal C (:2736, :2763): cr |= (C << (31-BT)).  C without bit 0: CR[BT] is never set, red on every result-1 row.  C with
                      bit 0 and some other bit j: on the `setbits' rows (BT = 31) the extra bit lands on CR[31-j], a zero for
                      j = 2..31 (crandc) and j = 1..31 (crorc), seen by the whole-CR compare; j = 1 at crandc is red on
                      `64 crandc 01'.  Closed for every C != 1 (and C = 0 is `set deleted').
  The field masks `& 31' (:2730-2731, :2757-2758) are closed over 0..30 by enumeration; a mask with bits above 4 is the fix
  (the field is 5 bits), so the mask sites are closed over every constant too.

## WHAT STAYS UNDETECTED, AND WHY

  - the 36 EQUIVALENT cells above (proved; no row can see them);
  - crandc clear -> toggle (^=): DISCLOSED in the probe's clause (e)(5) (every crandc row with result 0 pre-sets the inverse,
    and the round-3 `64 crandc setbits' row pre-sets 0 with result 1: a toggle of 0 then |= gives 1 too);
  - OUTSIDE the denominator (disclosed, (e)(5)): an extra CLEAR (clear literal 1+2^k).  The round-3 whole-CR rows see some of
    them incidentally (appendix); the rest need ones at non-source, non-destination bits, which the set-literal rows cannot
    carry.  Not claimed.

## PROBE CONTRACT TEXT (clause (e), round 3)

  ROUND 3 (regress/artifacts/ppccrandcorc/r3_20261105/CLOSURE3.md): the four whole-CR rows after the round-2 pins close the
  single-constant space at the four read-mask sites and the two set literals.  COVERED: every read mask `& m' other than the
  fix's at crandc BB, crorc BA and crorc BB (all 2^32 m, by the proof; 1+2^k for k = 1..31 and 0, 2, 4, 6 enumerated and
  simulated), every crandc BA read mask with bit 0 clear; every set literal C != 1 in both handlers (1+2^k, k = 1..31,
  enumerated); the clear/set addressing cells (31-bt) -> (31-ba), (31-bb), bt and the clear moved between the reads.
  DELIBERATELY UNCOVERED: crandc BA read masks with bit 0 set (EQUIVALENT: `ba & !bb' sees only bit 0 of ba); `|=' -> `^='
  at either set (EQUIVALENT after the clear); the read statements swapped (EQUIVALENT); the crandc toggle of (5); an extra
  CLEAR of a non-source, non-destination bit (5).

OLD rows: 62 (table 1), 66 (round 2).  NEW rows: 4 (N = 70).
```

### E2. the errata to CLOSURE3.md after pass 4, WITH the second-reading qualifications (r3_20261105/CLOSURE3.errata.md)

# #575 ppccrandcorc -- ERRATA to CLOSURE3.md (round 3), written 2026-11-05 after pass 4

Source of the corrections: p4_20261105/codex_codex_r575_p4.txt (F1-F5) and p4_20261105/DISPOSITION.md.  CLOSURE3.md itself is NOT
rewritten; this file sits beside it and supersedes the three sentences quoted below.  Each correction was re-checked against
src/cpus/cpu_ppc_instr.c and the probe before it was written here (the seat that wrote CLOSURE3 wrote this too, and a correction is
not safer than the thing it corrects).  F2 and F3 were corrected in the probe itself, not in CLOSURE3: see RECORDS4_NOTE.md.

The fix, the four measured rows, the 70-row gate block, table 3 (table3/SCORES.txt, PRETABLE_3.out) and the 453-cell partition
(416 detected, 36 equivalent, 1 disclosed) are unchanged by these errata.  No row, seed, instruction or want changes.

## F1 -- the field-mask "closed over every constant" sentence (CLOSURE3.md:736-737, section PROOF)

CORRECTS:  "The field masks `& 31' (:2730-2731, :2757-2758) are closed over 0..30 by enumeration; a mask with bits above 4 is the
            fix (the field is 5 bits), so the mask sites are closed over every constant too."

WHY IT IS FALSE.  The handlers mask RAW shifted instruction words, not extracted indices (cpu_ppc_instr.c:2730-2731 and
:2757-2758: `bt = (iword >> 21) & 31; ba = (iword >> 16) & 31, bb = (iword >> 11) & 31`).  For opcode 19 the shifted words are

    iword >> 21 = (19 << 5)  | BT
    iword >> 16 = (19 << 10) | (BT << 5) | BA
    iword >> 11 = (19 << 15) | (BT << 10) | (BA << 5) | BB

so a mask with a bit above bit 4 MAY import the neighbouring field (or the opcode) -- it does wherever it keeps a bit the neighbour
or the opcode sets (0x8000001f adds only bit 31 to the field's five bits, and bit 31 is clear in the shifted word, so it decodes
exactly): BT mask 63 gives BT + 32 (19 = 0b10011 has bit 0
set), BA mask 63 imports BT's low bit, BB mask 63 imports BA's low bit.  Such a decode is not the fix; it can also produce a shift
count `31 - bt' outside 0..31 at :2734/:2736.  The simulator cannot see this: v575c.py:94 masks the ALREADY EXTRACTED indices
(`bt & V.get("mbt", 31)`), so in its model a mask m acts as `index & m` -- the identity on every index exactly when (m & 31) == 31
(m = 32 maps every index to 0) -- a property of the model, not of the C.

CORRECTED CLAIM.  The field-mask sites are closed over m = 0..30 by enumeration only: those 186 cells (m = 0..30 at BT, BA, BB in
both handlers) are all DETECTED (table 3 / codex's pass-4 partition: 186 of 186; the BT families on their `setbits' row, crandc BB
on `64 crandc bbmask', crorc BA on `64 crorc baread', crorc BB on `64 crorc bbmask', crandc BA m = 0..29 on `64 crandc setbits'
and m = 30 on `64 crandc 10').  Field masks with any bit above bit 4 (m >= 32) act on the raw shifted word, may import neighbouring
fields, and are OUTSIDE the 453-cell denominator: DISCLOSED here, not proved and not simulated (their compiled behaviour, including
the out-of-range shift counts, is not modelled).  The PROOF section's six constant-space arguments (the four read masks, the two
set literals; CLOSURE3.md:720-735 as corrected by F4 below) stand: they act on `cr >> (31-x)` and `C << (31-BT)`, whose operands
ARE the extracted values.

## F4 -- "C without bit 0 ... red on every result-1 row" (CLOSURE3.md:732, section PROOF)

CORRECTS:  "C without bit 0: CR[BT] is never set, red on every result-1 row."

WHY IT IS FALSE.  CR[BT] is indeed never set, but a table session runs several instructions, and a later instruction's misplaced
literal can land on an earlier destination.  crorc set literal C = 2 in the 64-bit table session (PRETABLE_3.out:12: crorc 12,0,2;
crorc 13,0,1; crorc 14,1,0; crorc 15,1,3): `C << (31-BT)` sets CR[BT-1], so crorc 14 sets CR[13] and crorc 15 sets CR[14].  CR[14]
is the destination of `64 crorc 10' (want 1): that row PASSES although its own instruction never set its bit; so does `32 crorc 10'.
The mutant is still red (`64 crorc 00', `64 crorc 01', `64 crorc 11', and the `setbits' row), but not on EVERY result-1 row.

CORRECTED CLAIM.  The setbits rows detect every incorrect set literal except crandc C = 3, which `64 crandc 01' detects: there BT = 31,
the shift is 0, and the final CR is 2 | C on `64 crandc setbits' (want 3) and C on `64 crorc setbits' (want 1).  crorc: every
C != 1 is red on `64 crorc setbits'.  crandc: exactly C in {1, 3} pass `64 crandc setbits'; C = 3 is red on `64 crandc 01' (crandc
10,1,0 re-sets CR[9]; CLOSURE3.md:706).  So every C != 1 is detected in both handlers (C = 0 is `set deleted'), which is what the
contract claims; the clause about "every result-1 row" is withdrawn.

## F5 -- the cost of a multi-instruction session (CLOSURE3.md:714-715, "WHY FOUR AND NO FEWER")

CORRECTS:  "So no single instruction serves two families, and 4 rows is the minimum; a multi-instruction session would cost more
            rows (session/others/mfcr/disasm), as the edge session shows."

WHY IT IS FALSE.  Under the round-3 whole-CR method a row is self-contained: cr_row (ppc_crlogic_probe.py:374-383; :372-381 in table3/probe70_frozen.py) scores exit0,
the register dump's agreement with mfcr r10, and the whole CR in ONE row, so a multi-instruction session costs no apparatus rows.
And one such row does serve two families.  Session: seed CR = 0x00000002; crandc 31,30,31; crorc 30,30,0; mfcr r10; compare the
whole CR with 0x00000003.  Correct handlers: crandc 31,30,31 reads a = CR[30] = 1, b = CR[31] = 0 and sets CR[31] (CR = 0x3);
crorc 30,30,0 reads a = CR[30] = 1, b = CR[0] = 0, clears and re-sets CR[30] (CR = 0x3).  The crandc set literal 1+2^k, k = 2..31,
also sets CR[31-k], a zero that the second instruction (which rewrites only CR[30]) leaves set: red (k = 1 lands on CR[30] and is
red on `64 crandc 01' as before).  The crorc set literal 1+2^k at the k = 26, 27 survivors, shifted by 31-30 = 1, sets CR[4] and
CR[3] respectively, both zero: red.  With `64 crorc baread' and `64 crorc bbread' this makes THREE added rows sufficient when a
session may hold more than one instruction.

CORRECTED CLAIM.  Four is the minimum under the SINGLE-instruction restriction the round chose (the first sentence of "WHY FOUR AND
NO FEWER", the four families' incompatible seeds, stands as the argument for that case); with multi-instruction sessions three rows
suffice, at no extra apparatus cost.  The four measured rows (`baread', `bbread', `crandc setbits', `crorc setbits') stay as they
are: table 3 measured them, and the gate's 70-row block names them.

## Not corrected here

  - F2 (the `64 crorc baread' printed note "a=0 for every mask") and F3 (the probe docstring's placement of the crandc toggle under
    "EQUIVALENT, proved") live in ppc_crlogic_probe.py and were corrected there, text only: RECORDS4_NOTE.md.  CLOSURE3.md's own
    classification of the toggle (:684-685, :742, :756) is correct and unchanged.
  - CLOSURE3.md:12 ("PROVES the rest of the 2^32-constant space at each site") refers to the six read-mask / set-literal sites of
    the PROOF section, which pass 4 endorsed; it is not the F1 sentence and is left as written.

## SECOND-READING CORRECTIONS (2026-11-05 ~09:5xZ, main loop, from GPT-6 Astra's second reading: ../rec4_20261105/codex_codex_r575_rec4.txt)

The second reading accepted F3 and F5 and found three of THESE corrections making new universal claims; each is now qualified in place
above (the pre-correction text is kept as CLOSURE3.errata.md.pre_2nd):
* F1, "a mask with a bit above bit 4 imports the neighbouring field" -> MAY import (0x8000001f decodes exactly); "a mask with bits
  above 4 is indeed the identity" in the simulator -> the identity exactly when (m & 31) == 31 (m = 32 maps every index to 0); and
  "act on the raw shifted word, import neighbouring fields" -> may import.
* F4, "closed by the `setbits' rows directly, with no appeal to the table rows" -> the setbits rows detect every incorrect set literal
  except crandc C = 3, which `64 crandc 01' detects (as the paragraph already went on to say).
The exclusion of unenumerated masks (m >= 32) from the denominator is unchanged; no detector gap follows from any of this.

### E3. the records correction after pass 4, WITH the second-reading note (r3_20261105/RECORDS4_NOTE.md)

# #575 ppccrandcorc -- RECORDS CORRECTION after pass 4 (2026-11-05, Mythos 5.1, the seat that wrote CLOSURE3)

Pass 4 (p4_20261105/codex_codex_r575_p4.txt, `CODEXP4R575: 453 CELLS SWEPT 0 BREACHES 5 FALSE RECORDS VERDICT:REPAIR`;
p4_20261105/DISPOSITION.md F1-F5) closed the repair chain with zero floor breaches and five false records.  This note records
where each was corrected.  No source, gate, build, run of the probe, table or git action; CLOSURE3.md, PRETABLE_3.out and table3/
are untouched.  Files written: this note, CLOSURE3.errata.md, ppc_crlogic_probe.py.pre_rec4 (all in r3_20261105/); file edited:
regress/ppc_crlogic_probe.py (text only, proof below).

## The five records

F1  CLOSURE3.md:736-737 (PROOF) -- corrected in CLOSURE3.errata.md.
    BEFORE: "a mask with bits above 4 is the fix (the field is 5 bits), so the mask sites are closed over every constant too."
    AFTER:  field masks are closed over m = 0..30 by enumeration (186 cells, all detected); masks with a bit above bit 4 act on the
            RAW shifted instruction word (cpu_ppc_instr.c:2730-2731, :2757-2758) and may import a neighbouring field (BT mask 63 ->
            BT + 32; BA mask 63 imports BT's low bit; BB mask 63 imports BA's low bit); v575c.py:94 masks extracted indices and
            cannot model them; they are OUTSIDE the denominator and DISCLOSED, not proved.
    Probe: no copy of this claim.  The docstring's field-mask scope is "every field mask 0..30" (:38, :62-64) and its "all 2^32 m"
    sentence (:52) is about the READ masks, which pass 4 endorsed.  Nothing to change there.

F2  ppc_crlogic_probe.py:384 (now :386), the `64 crorc baread' row's printed note -- corrected IN PLACE.
    BEFORE: "BA=31 over 0xfffffffe, whole CR: a=0 for every mask"
    AFTER:  "BA=31 over 0xfffffffe, whole CR: a=0 at the fix; a!=0 is red"
    Why: a = CR[31] = 0 under the fix's decode and read mask.  Read mask 3 gives a = 0xfffffffe & 3 = 2; BA field mask 16
    gives a = CR[16] = 1.  The row is red exactly because those mutations make a nonzero (read mask 0 keeps a = 0 and is red on
    `64 crorc 11' instead, CLOSURE3.md:728 -- which is why the new note does not say "every other mask").  The comment block above
    the row (:362-364 frozen, :364-366 now) already stated this correctly and is unchanged.

F3  ppc_crlogic_probe.py:54-56 (now :54-58), docstring clause (e), ROUND 3 paragraph -- corrected IN PLACE.
    BEFORE: "DELIBERATELY UNCOVERED (EQUIVALENT, proved): crandc BA read masks with bit 0 set (`ba & !bb' sees only bit 0 of ba);
             `|=' -> `^=' at either set (after the clear); the two read statements swapped; and the crandc toggle of (5)."
    AFTER:  "DELIBERATELY UNCOVERED, in two classes.  EQUIVALENT, proved: crandc BA read masks with bit 0 set (`ba & !bb' sees only
             bit 0 of ba); `|=' -> `^=' at either set (after the clear); the two read statements swapped.  DISCLOSED, NOT
             equivalent: the crandc toggle of (5) (crandc 31,0,1 over CR 0 must leave 0; the toggle leaves 1) -- no row sees it,
             for the reason (5) gives.  (Pass 4, F3: round 3 had listed the toggle under "EQUIVALENT, proved";
             r3_20261105/RECORDS4_NOTE.md.)"
    Why: crandc 31,0,1 over CR = 0 reads a = b = 0, result 0; the fix clears CR[31] (CR stays 0), a toggle sets it (CR = 1).  Not
    equivalent; it is the one DISCLOSED cell, as CLOSURE3.md:684-685 and :742 classify it (CLOSURE3's contract text :755-757 lists
    it without the EQUIVALENT label and needed no change).  The round-2 paragraph (:42-43) already lists it apart from the "four
    EQUIVALENT cells" and is unchanged.

F4  CLOSURE3.md:732 (PROOF) -- corrected in CLOSURE3.errata.md.
    BEFORE: "C without bit 0: CR[BT] is never set, red on every result-1 row."
    AFTER:  not every result-1 row: in a table session a later instruction's misplaced literal can land on an earlier destination
            (crorc C = 2 sets CR[BT-1]: crorc 15 sets CR[14], so `64 crorc 10' and `32 crorc 10' pass).  The set-literal sites are
            closed by the `setbits' rows directly (final CR = 2 | C, want 3; final CR = C, want 1): every C != 1 is red there, bar
            crandc C = 3, red on `64 crandc 01'.
    Probe: no copy (the docstring's "every set literal C != 1 in both handlers", :53, is the covered claim and stands).

F5  CLOSURE3.md:714-715 ("WHY FOUR AND NO FEWER") -- corrected in CLOSURE3.errata.md.
    BEFORE: "4 rows is the minimum; a multi-instruction session would cost more rows (session/others/mfcr/disasm), as the edge
             session shows."
    AFTER:  four is the minimum under the single-instruction restriction only; a cr_row-style row scores exit0, mfcr agreement and
            the whole CR itself, so a multi-instruction session costs no apparatus rows, and one such row (seed 0x2; crandc
            31,30,31; crorc 30,30,0; mfcr; want 0x3) catches both set-literal survivor families: three rows suffice.  The four
            measured rows stay.
    Probe: no copy (the round-3 comment block :357-371 frozen makes no minimality claim; the round-2 "NOT the minimum" remark at
    :333-336 is pass 3's R2, a different sentence).

## Text-only proof of the probe edit

Backup: r3_20261105/ppc_crlogic_probe.py.pre_rec4, md5 772576e7f1795ff8006c5884148e0fa8 = table3/probe70_frozen.py (table3/MD5.txt
line 1) = the in-tree probe before this edit.  After the edit the in-tree probe is 400 lines (was 398), md5 55523a4198d42cc1b412584897eb9d35,
maximum line width 143 (unchanged; the edited lines are 90..133 wide).

Command (run from GXEMUL-SEC/regress, Python 3.12.10, `-I`):

    python -I -c '
    import ast, sys
    def strip(path):
        t = ast.parse(open(path, encoding="utf-8").read())
        if t.body and isinstance(t.body[0], ast.Expr) and isinstance(t.body[0].value, ast.Constant) \
                and isinstance(t.body[0].value.value, str):
            t.body.pop(0)                                   # drop the module docstring
        for n in ast.walk(t):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                n.value = "<STR>"                           # every string constant -> placeholder
        return ast.dump(t)
    a, b = strip(sys.argv[1]), strip(sys.argv[2])
    print("ast.dump equal (docstring dropped, every str constant -> <STR>):", a == b, "len", len(a), len(b))
    ' ppc_crlogic_probe.py artifacts/ppccrandcorc/r3_20261105/table3/probe70_frozen.py

Result:

    ast.dump equal (docstring dropped, every str constant -> <STR>): True len 53679 53679

`diff table3/probe70_frozen.py ppc_crlogic_probe.py` shows exactly two hunks: docstring lines 54-56 -> 54-58 (F3) and line 384 ->
386 (F2); `python -I -m py_compile` accepts the file.  Every row's name, seed, instruction, want and order, every function body and
every non-string constant are identical to the frozen instrument.  The in-tree probe now differs from table 3's frozen instrument
(table3/probe70_frozen.py) in PRINTED TEXT ONLY: one row note and the module docstring.  Table 3's scores are unaffected (the gate's
70-row block, gate_ppc.sh:357, matches row NAMES and does not read note text), so the difference is recorded here, not re-tabled.

Second reading: per DISPOSITION.md, one Gemini reading of the corrected sentences (CLOSURE3.errata.md and the two probe hunks) is
owed before landing; this note does not claim it.

SECOND READING (2026-11-05 ~09:5xZ): GPT-6 Astra accepted F3 and F5 and qualified three new universal claims in these corrections
(F1's import and identity claims, F2's "only under", F4's "no appeal to the table rows"); all qualified in place here and in
CLOSURE3.errata.md (pre-correction copies: *.pre_2nd; the reading: ../rec4_20261105/codex_codex_r575_rec4.txt).

### E4. round 2's closure errata (r2_20261105/CLOSURE.errata.md)

# CLOSURE.md -- errata (2026-11-05, round 3; pass 3 = p3_20261105/codex_codex_r575_p3.txt)

CLOSURE.md is a record of round 2 and is not rewritten.  Each item quotes what it corrects.

## R2 -- "WHY THESE FOUR AND NO FEWER" is false: three rows would have closed the 239 cells

CLOSURE.md, "WHY THESE FOUR AND NO FEWER", says:

> crandc clear-before-read needs BT == BB with b = 1 (want 0), a different seed: its own row (BT == BA is invisible for crandc:
> a is forced to 1-want, and the early clear changes a only when b = 1, where the result is 0 either way).  [...]  The two crandc
> needs (want 1 uniform ones; BT == BB with b = 1) and the two crorc needs (uniform ones; uniform zeros) are pairwise incompatible
> seeds, so four rows is the minimum for single-instruction sessions.

"a is forced to 1-want" carries the INVERSE pre-set into a design that, two sentences earlier, already pre-sets EQUAL.  With an
EQUAL pre-set, the single row

    crandc 16,16,31 over 0xfffffffe, want 1 (a = CR[16] = 1 pre-set EQUAL, b = CR[31] = 0)

sees the clear moved before the reads (a -> 0, result 0), every BB field mask 0..30 (CR[m] = 1 -> b = 1 -> 0), BB <- BT (CR[16] =
1 -> 0) and the BB read masks & 3 / & 7 (CR[30] = 1 -> bb != 0 -> 0): everything `64 crandc bbmask' and `64 crandc order' close
together.  Verified by simulation in round 3 (r3_20261105/v575c.py, the same 239 cells): the 62 rows plus {crandc 16,16,31, `64 crorc
bamask', `64 crorc bbmask'} leave the same 4 EQUIVALENT cells and the same 1 disclosed cell undetected as the four round-2 rows do --
three rows, not four, was the minimum.  The four rows STAY as they are: table 2 measured them (table2/SCORES.txt, 27 variants exactly
as predicted), and round 3 adds its rows beside them (r3_20261105/CLOSURE3.md).

## The vocabulary was narrower than the classes it put in scope (pass 3, B1-B4)

CLOSURE.md, ENUMERATION:

> the read mask `& 1' widened to `& 3' and `& 7' at BA and at BB; the clear moved before the reads, deleted, or replaced by a
> toggle; the set deleted or `|=' -> `^='

and "DENOMINATOR: 239 cells".  Those statements are true of the 239 cells, and every prediction in CLOSURE.md stands for them.
But the read-mask sites (cpu_ppc_instr.c:2732-2733, :2759-2760) and the set statements (:2736, :2763) admit other single-constant
edits the enumeration did not list: `& (1|1<<k)' for k = 2..31 and & 0, 2, 4, 6 at each read, and the set literal 1 -> 1+2^k.
Of those, 54 (codex B1-B4: crorc BB read masks k = 2..30, crorc BA `& 0x8001', crandc set literals k = 7, 9, 11..30, crorc set
literals k = 26, 27) plus k = 31 at crorc BB and at the crandc set literal survive the 66 rows.  Round 3's enumeration (453 cells)
and its four whole-CR rows close them: r3_20261105/CLOSURE3.md.  The sentence in the probe's clause (e) that "with the four rows
every cell is red by simulation except four EQUIVALENT cells" was true of the 239 cells only; the probe's clause (e) now says so.

### F1. your pass-1 ruling (adj_p1_20261105/MYTHOS_local.md)

MYTHOSADJP1R575
model: Mythos 5.1 (claude-mythos-5-1)
VERDICT: APPLY-WITH-CHANGES -- the two expression edits are correct and sufficient; the probe owes four rows, the floor owes four more variants, and three premises in the brief's census are false (none touches the defect claim). `ppccrlogicshift` is FILED, not joined. GLM's "58/58 unreachable" finding is wrong.

1. THE FIX

The defect is as stated. `cpu_ppc_instr.c:2735` sets CR[BT] on `!(ba & bb)` (NAND) and `:2762` on `!(ba | bb)` (NOR); the crorc body at 2756-2764 is byte-identical to crnor at 2765-2773. Book I at `ppc_uisa_book1_v201.txt:1909` reads `CRBT <- CRBA & ~CRBB` and `CRBT <- CRBA | ~CRBB`, with prose at 1911-1914 naming the complement on BB. Walked: crandc arch 0,0,1,0 vs HEAD 1,1,1,0 (DISC at 00, 01); crorc arch 1,0,1,1 vs HEAD 1,0,0,0 (DISC at 10, 11). The witness's ten reds at `WITNESS_head.out:12-13,18-19,48-49,52-53,58-59` are exactly those cells.

[R1] The exact changes: line 2735 becomes `if (ba & !bb)` and line 2762 becomes `if (ba | !bb)`. Nothing else in either handler changes. `ba`/`bb` are masked to 0/1 at 2732-2733 and 2759-2760, so `!bb` is the exact complement and the walk gives the arch column on all four rows. Reads precede the clear (2732-2734), so BT==BA or BT==BB aliasing is order-safe. Decode is reached only via `:4638` and `:4641`; CRNAND (225, `opcodes_ppc.h:59`) is absent from the case list at 4629-4635 and falls to `default: goto bad` at 4648. There is no POWER-mode path: `cpu_ppc.c:96` sets `mode = MODE_PPC` unconditionally and the `power` flag at `cpu_ppc.c:608` lives only in the disassembler. P2 is settled.

Second defect: yes, latent. `1 << (31-bt)` at bt=0 is a signed `1 << 31`, undefined under C11 6.5.7p4, at 14 sites across all seven handlers (2725-2727 through 2779-2781); `cr` is `uint32_t` (`cpu_ppc.h:126`). On the gcc build it behaves (the witness's edge rows ran at bt=0 and bt=31).

[R2] `ppccrlogicshift`: FILED. Same device, yes. Same semantic class, no: representation hygiene versus a wrong boolean function. Same detector, no: the un-fixed shift produces the architectural result on this toolchain, so no row of this probe can red under its reinstatement; its instrument is `-fsanitize=shift` or an unsigned-type review, not a CR truth table. Two of three legs fail. The fix must NOT switch just these two handlers to `1u <<` (codex's "unnamed alternative"); that would partially repair a 14-site defect inside this round and spoil the other round's witness. Deepseek's in-round ruling is rejected on the same grounds. `ppccrnandundec` stays out as the brief says (CPU-STOP class, xo 225 not run here, `ppc_crlogic_probe.py:27-29`).

2. THE DETECTOR

The 58-row probe is the right instrument in kind: real decoder, real guest, two widths (the second copy is the same source compiled with `DYNTRANS_DUALMODE_32`), inverse pre-set so a pass requires a write. The 58 is real: 6 apparatus + 12 (64 table) + 24 (siblings) + 4 (edge) + 12 (32 table), and 48 = 6 + 8 PIN + 24 + 2 + 8, matching `WITNESS_head.out` line by line.

[R3] GLM's finding that the crandc edge row aliases its destination with BA is FALSE. The edge row is `XL("crandc", 0, 2, 3)` at `ppc_crlogic_probe.py:238`: BT=0, BA=2, BB=3, as the comment at 231-232 says. GLM applied the truth-table pick (BA=0 for a=0) to a row that does not use it. 58/58 is reachable on the fixed build.

[R4] Rows OWED (4):
- `64 crandc hi` and `64 crorc hi`: one row per handler with BA, BB >= 16 and every proper-submask alias bit (indices `& 15`, `& 7`, `& 3`, `& 1`) seeded to the opposite value. Every current row uses BA in {0,1,2,4} and BB in {0,1,2,3,5} (`:162`, `:238`), so a one-character mask weakening `& 31` to `& 7` at 2731 or 2758 scores 58/58 today. Four seats found this independently. One width suffices; the 32-bit copy is the same source.
- `edge mfcr` and `edge disasm`: the brief's §3 claims an mfcr row and a disasm row per session. The edge session runs `MFCR(10)` and captures `edis` (`:238`) but scores neither (`:240-245`). Either the rows are added or the premise is withdrawn; I rule they are added, since `edge disasm` is the only encoder pin at the BT field extremes.

VACUOUS by construction (channel cannot vary under the named variant):
- Under every variant in the floor: the 20 sibling rows, 6 apparatus controls, 4 session rows, 3 disasm rows (disassembler is `cpu_ppc.c:823-830`, untouched), 3 mfcr rows (both channels read the one `uint32_t`; they agreed on HEAD's wrong values too, witness line 21), and 3 others rows (no floor variant writes outside BT).
- Under (d) complement-swap and under complement-drop: both edge rows. Inputs (0,0) and (1,1) are fixed points of those mutations (walked: `!0&0=0`, `0&0=0`; `!1|1=1`, `1|1=1`).
- Under a single-site (b): every row of the other handler, and the two PIN rows of the restored handler.

Null medium: identity bodies for both handlers (brief §5c) is correct. Predicted 18 red (16 truth + 2 edge), 40/58; the owed hi rows, pre-set inverse, make that 20 red of 62. It also doubles as the proof of P4: a row reds under the null exactly because the pre-set is the inverse. Grok's narrowing is right and harmless: on HEAD the DISC rows (including both edges) cannot distinguish "wrong write" from "no write"; post-fix every row can.

Controls: the six apparatus rows (`:213-222`), the session rows, the disasm rows and the 20 sibling rows (all `control=True`) feed `PPC_CRLOGIC_CONTROL`; `others`, `mfcr` and edge rows are scored but not controls (`:194-197`, `:241-245`). That split is right.

Recommended, not owed: seed background ones in bits that are neither sources nor destinations so `others` can see an extra clear (today it sees only extra sets, since the seed is 0x50000000 outside the destinations; grok's `& ~1u` escape); one preset-true row per handler to catch codex's toggle escape `cr ^= (1 << (31-bt))`; the other-diagonal edge rows (crandc bt31, crorc bt0) belong to `ppccrlogicshift`, which needs a bt=0 set-path pin that this probe lacks.

3. THE TEST-VARIANT TABLE (bounded to lines 2729-2737 and 2756-2764)

[R5] Nine variants, each from the fixed build, red rows on the 58-row denominator (the owed rows stay green under all nine):

| # | variant | red rows | n |
|---|---|---|---|
| b1 | crandc `!(ba & bb)` restored | 64/32 crandc 00, 01; edge crandc bt0 | 5 |
| b2 | crorc `!(ba \| bb)` restored | 64/32 crorc 10, 11; edge crorc bt31 | 5 |
| c | both bodies identity | 16 truth + 2 edge | 18 |
| d1 | crandc `!ba & bb` | 64/32 crandc 01, 10 | 4 |
| d2 | crorc `!ba \| bb` | 64/32 crorc 01, 10 | 4 |
| d3 | crandc `ba & bb` (complement dropped, collapses to crand) | 64/32 crandc 10, 11 | 4 |
| d4 | crorc `ba \| bb` (collapses to cror) | 64/32 crorc 00, 01 | 4 |
| d5 | crandc `ba \| !bb` (operator crossed with crorc) | 64/32 crandc 00, 11; edge bt0 | 5 |
| d6 | crorc `ba & !bb` (operator crossed with crandc) | 64/32 crorc 00, 11; edge bt31 | 5 |

d3/d4 are kimi's addition and are the defect's own class (a handler computing a sibling's function). d5/d6 are the copy-paste risk between two lines edited in one round. No predicate dominates either edited line (the `if` is the only branch), so clause 1 of the bound at `tools/CLAUDE.md:1448-1451` adds nothing. Clause 2 bt-substitutions (`bt & !bb`, `ba & !bt`, `bt | !bb`, `ba | !bt`) each red an existing row by enumeration (64/32 crandc 10 for the first two; 64/32 crorc 01 and 00 for the last two); list them in PRETABLE as predicted, not built. GLM's `~bb` is not a variant for crandc: `ba & ~bb` with 0/1 operands equals `ba & !bb` on all four rows, so it has no channel; for crorc it is caught by row 01.

4. SEAT FINDINGS AND FALSE PREMISES

Right: the two expressions (all six seats, by enumeration); the 58 census (codex, grok); the PIN overcount (codex, grok); the edge session's unscored mfcr/disasm (codex, `:238-245`); the field-mask escape (codex, grok, GLM, minimax); the complement-drop variant (kimi); `others` blind to extra clears and the toggle escape (grok, codex); the shift is real but a different class (codex, grok, GLM, kimi, minimax); POWER mode settled from `cpu_ppc.c:96` (codex, grok).

Wrong: GLM's aliased-edge finding (R3) and GLM's claim that crandc `ba & ~bb` fails at (1,0): `1 & ~0 = 1`. Minimax's claim that `!ba | bb` gives 0,1,0,1 and reds three rows: `!0 | 0 = 1`, so it reds exactly 01 and 10, and the brief's §5d prediction stands. Minimax's 50-or-70 denominator: the witness shows 58. Deepseek's in-round shift fix (R2) and its `bt != 15` mutant: BT=15 is `64 crorc 11` (witness line 19), which reds it. Kimi's ledger arithmetic is right in spirit but its 40/50 totals omit the four session rows.

[R6] False premises in the brief: (a) "the four PIN rows of each handler at each width" is two per handler per width, eight total (witness 14-17, 54-57); (b) "an mfcr row per session" and "a disasm row per session" are false for the edge session; (c) the §3 passing census omits the four session rows and does not sum to 48 as written. P1, P2 and P4 hold. P3 is not settleable read-only; the measurement to name is the post-fix full battery with every other gate unchanged green. Also note for the dependent round: `ppccrnandundec`'s draft sketches `!(ba & bb)` as the crnand body, which is today's crandc; it must not alias `instr(crandc)` once this lands.

5. VERDICT

[R7] Gate 13: keep the parse-before-score shape, CONTROL=OK and the sentinel, and equality on both halves, but re-pin at the new total (62/62) after the four owed rows land; 58 is not the number to freeze. [R8] Write PRETABLE.out with the row manifest (BT, BA, BB, seed per row) and the nine-variant table before any variant is built. [R9] Correct the three §3 premises in the brief. [R10] Ship the two expression edits exactly as proposed, with no other source change.

APPLY-WITH-CHANGES: the design stands; the changes are the four owed rows, the four added variants, the re-pin, and the census corrections.

MYTHOSADJP1R575: 10 RULINGS 4 ROWS-OWED 9 VARIANTS VERDICT:APPLY-WITH-CHANGES

### F2. the repairs' implementation notes (r2_20261105/IMPL_NOTE.md, r3_20261105/IMPL_NOTE.md)

# #575 ppccrandcorc -- ROUND 2 implementation note (2026-11-05, Mythos 5.1)

The fix (src/cpus/cpu_ppc_instr.c:2735 `if (ba & !bb)`, :2762 `if (ba | !bb)`) is untouched.  This round closes the detector
over an enumerated class of single edits to the two handlers, corrects the false records pass 2 found, and prepares table 2.
No table was run here (the main loop runs it); no source, build or git action was taken.

## Rows added (4): N = 62 -> 66

Single-instruction sessions shaped like the `hi' rows (ppc_crlogic_probe.py, `pin_row`, after the two hi rows):

    64 crandc bbmask   crandc BT=16 BA=5  BB=31  seed 0xfffffffe  want 1  CR[16] pre-set EQUAL (1)
    64 crandc order    crandc BT=9  BA=5  BB=9   seed 0x04400000  want 0  CR[9]  pre-set inverse (1)
    64 crorc bamask    crorc  BT=16 BA=31 BB=5   seed 0xffff7ffe  want 0  CR[16] pre-set EQUAL (0)
    64 crorc bbmask    crorc  BT=31 BA=5  BB=31  seed 0x00000001  want 0  CR[31] pre-set inverse (1)

A source at index 31 over a uniform CR[0..30] opposite to CR[31] makes every field mask m in 0..30 at that site read a flipped
input (31 & m = m).  Two rows pre-set CR[BT] EQUAL to the result because an inverse pre-set hides a BB read of CR[BT] on every
row (codex B1-B2); the crorc one incidentally sees the crorc toggle.  BT == BB with b = 1 pins read-before-clear (BT == BA is a
fixed point for both handlers).  CLOSURE.md, "WHY THESE FOUR AND NO FEWER", gives the seed-incompatibility argument.

## Closure (CLOSURE.md; simulator v575b.py, which reproduces table 1's 17 legs on the 62 rows exactly: `check62')

Denominator 239 cells = 186 field masks (m 0..30 at BT, BA, BB, both handlers) + 8 source-read index substitutions + 8 read-mask
widenings (& 3, & 7 at BA, BB) + 6 clear edits (early, deleted, toggle) + 4 set edits (deleted, ^=) + 15 condition edits (b, d-moved,
d-dropped, d-crossed, the four R5 bt-substitutions, identity per handler, c both identity) + 12 dispatch re-bindings.

    missed by the 62 rows:        25  (codex's nine and glm's crandc BB `& 3' among them; codex's {30,29,27,23,15} sweep saw 3 of the
                                       11 crandc BB mask misses: 5,9,11,13,17,19,21,23,25,27,29)
    closed by the 4 new rows:     20
    EQUIVALENT (proved):           4  crandc BA read mask & 3 / & 7 (`ba & !bb' is bitwise with !bb in {0,1}: only bit 0 of ba
                                       survives -- glm's BA-site cell is not a breach); crandc/crorc set `|=' -> `^=' (the clear
                                       has just zeroed the bit).  Each also survives 40000 random (cr,BT,BA,BB) differential trials.
    EXCLUDED:                      1  crandc clear -> toggle (disclosed in clause (e)(5)); the crorc toggle is now red on `64 crorc bamask'.
    undetected by the 66 rows:     0

## Base run (base66/probe_base66.out, build/gxemul; CLEARANCE.txt: cmp identical, binary newer than source)

    PPC_CRLOGIC_RESULT=66/66
    PPC_CRLOGIC_CONTROL=OK
    PPC_CRLOGIC_PROBE_DONE          (elapsed 0.2s; 66 rows ok, 0 FAIL)

No row was red on the fix, so no row's seed or want was re-derived; no want was fitted to the binary.

## Records corrected

- probe docstring/comments: F1 (clause (e)(3): index-31 inputs ARE rowed -- the hi row's BA31 and the three new index-31 sources;
  index-0 inputs are the tables' BA=0/BB=0), F2 (field-mask comment: `& 1' was already red on the old edge row; `& 15/7/3' were the
  58/58 escapes), F3 (`edge disasm' compares mnemonics only), (e)(5) (toggle: crandc only; hi/pin sessions have no `others' row).
  F7 touches nothing in the probe (its only "debugger" sentence, line 19, is true); fixed in v575b.py's and PRETABLE_2's wording.
- table1_20261105/PRETABLE.errata.md: F4 (absent binary: no CONTROL record, DONE=0), F5 (probe62_frozen.py is 86 ms older than
  PRETABLE.out), F7, and the four R5 bt-substitution predictions on the 62 rows (3, 3, 3, 2 red -- codex's sets).
- table1_20261105/table1/VERDICT.errata.md: F6 (the ruling listed four rows for d1-d4 and five for d5-d6).
- PRETABLE.out, SCORES.txt, VERDICT.md: not rewritten.

## Gate (gate_ppc.sh, #575 block only)

Names list = the base run's 66 names in order; RESULT=66/66; rows run/green 66; header "66-row"; the comment names the closure and
r2_20261105/.  `diff gate_ppc.sh.pre_r2 gate_ppc.sh`: old lines 328, 333-334, 347, 349, 353-354 (7 out, 9 in), all inside lines
328-356; `bash -n` clean.

## Table-2 inputs (written BEFORE any table; the main loop runs the table)

- variants/*.c: 27 = table 1's 15 re-created (identical edits, identical names) + 12 round-2 closures: s1/s2 (BB read of CR[BT];
  codex B1-B2), o1/o2 (clear before the reads; B3-B4, glm breach 1), m5-m9 (crandc BB & 29/27/23, crorc BA & 29, crorc BB & 29;
  B5-B9), m10 (crandc BB & 17, a miss codex's sweep lacked), g1 (crandc BB read `& 3', glm breach 2's real cell), g2 (crandc BA read
  `& 3': glm's other cell, predicted 0 red = EQUIVALENT).  Each is one exact edit of GXEMUL-SEC/src/cpus/cpu_ppc_instr.c (diff: one
  changed statement; o1/o2 move one statement, c_identity is table 1's two-handler edit).
- PRETABLE_2.out: the 66-row manifest and, per variant, the EXACT red set v575b.py computes; the four R5 bt-substitutions listed
  as PREDICTED ONLY (4, 4, 5, 2 red on 66 rows).  Expectation for table 2: base 66/66; HEAD 56/66 (the same ten); 26 variants red
  exactly as listed; g2 0 red (equivalence confirmed, not a detector failure).

## Files touched

    edited:  regress/ppc_crlogic_probe.py, regress/gate_ppc.sh (#575 block)
    written: r2_20261105/{ppc_crlogic_probe.py.pre_r2, gate_ppc.sh.pre_r2, v575b.py, CLOSURE.md, CLEARANCE.txt, PRETABLE_2.out,
             IMPL_NOTE.md, base66/probe66_run.py, base66/probe_base66.out, variants/*.c (27)}
             table1_20261105/PRETABLE.errata.md, table1_20261105/table1/VERDICT.errata.md

# #575 ppccrandcorc -- ROUND 3 implementation note (2026-11-05, Mythos 5.1)

The fix (src/cpus/cpu_ppc_instr.c:2735 `if (ba & !bb)`, :2762 `if (ba | !bb)`) is untouched.  This round closes the detector over
the FULL single-constant space at the sites round 2 had put in scope with a narrower vocabulary (pass 3, codex B1-B4), corrects
the seven false records R1-R7, and prepares table 3.  No table was run here (the main loop runs it); no source, build or git
action was taken; gate_ppc.sh was NOT edited (another implementer holds it): its #575 block is in gate_575_block.new.

## Codex's pass-3 findings, checked one by one (CLOSURE3.md; simulator v575c.py)

v575c.py extends r2_20261105/v575b.py (read mask = any constant; set literal; clear/set re-addressing; clear between the reads;
swapped reads) and first re-derives table 2's 29 legs on the 66 rows: `check66` matches PRETABLE_2.out on all 29, which licenses
the extension.  Then:

    codex's 54 survivors (B1 29, B2 1, B3 22, B4 2):  54 CONFIRMED (none red on the 66 rows), 0 refuted; all 54 red on the 70.
    codex's 35 equivalents:                            35 CONFIRMED (proof + 40000 random differential trials), 0 refuted.
    denominator: 453 cells = codex's 447 + k = 31 at the four read sites (4) and at the two set literals (2), in bound (same
                 constant sites, one more constant).  Partition on the 70 rows: 416 detected (360 by the 62/66 rows, 56 closed
                 by the 4 new rows), 36 EQUIVALENT (codex's 35 + crandc BA `& 0x80000001`), 1 disclosed (crandc clear -> toggle),
                 0 undetected.
    beyond the enumeration: CLOSURE3.md's PROOF section closes every 2^32 constant at the four read sites and the two set literals
                 (the enumerated families are the sampled representatives), so the contract names the whole site.
    appendix (outside the denominator, not claimed): the clear literal 1 -> 1+2^k (an extra CLEAR, disclosed (e)(5)); the new
                 whole-CR rows happen to see most crorc ones (k = 1..30) and no crandc one above k = 10.

## Rows added (4): N = 66 -> 70 (single-instruction sessions shaped like the `hi'/pin rows; each compares the WHOLE CR)

    64 crorc baread    crorc  17,31,5   seed 0xfffffffe  want CR 0xffffbffe  (B2; also every BA field mask 0..30 incl. 16: R1)
    64 crorc bbread    crorc  30,30,31  seed 0xfffffffc  want CR 0xfffffffe  (B1, k = 2..31)
    64 crandc setbits  crandc 31,30,31  seed 0x00000002  want CR 0x00000003  (B3, k = 2..31; k = 1 is red on `64 crandc 01')
    64 crorc setbits   crorc  31,0,31   seed 0x00000000  want CR 0x00000001  (B4, every k)

`cr_row` reads the CR from the register dump and from mfcr r10 and reports a disagreement as the got value.  Why 4 and no fewer:
CLOSURE3.md, "WHY FOUR AND NO FEWER" (the four families need pairwise incompatible seeds/results in one instruction).

## Base run (base70/probe_base70.out, build/gxemul; CLEARANCE.txt: cmp identical, binary newer than source)

    PPC_CRLOGIC_RESULT=70/70
    PPC_CRLOGIC_CONTROL=OK
    PPC_CRLOGIC_PROBE_DONE          (elapsed 0.3s; 70 rows ok, 0 FAIL; row order == v575c.py `names`)

No row was red on the fix, so no row was re-derived; no want was fitted to the binary (the four wants are the architectural CRs).

## Records corrected (each quotes what it corrects)

- probe (in place): R1 -- clause (e)(3) and the pin-block comment: `64 crorc bamask' has CR[16] = 0 (its EQUAL pre-set), so mask
  16 is not flipped there (red on `64 crorc 11'; now also on `64 crorc baread', uniform 0xfffffffe).  R3 -- the `64 crandc bbmask'
  comment: `& 3' gives bb = 2, `& 7' gives bb = 6.  R2 (probe side) -- "(BT == BA is a fixed point ...)" holds for an INVERSE pre-set
  only; crandc 16,16,31 over 0xfffffffe would have closed both crandc needs; the four round-2 rows are NOT the minimum and are kept
  as measured.  Clause (e) gains the ROUND 3 paragraph (the contract: covered / deliberately uncovered cells) and (5) is reworded
  for the whole-CR rows.
- r2_20261105/CLOSURE.errata.md: R2 ("WHY THESE FOUR AND NO FEWER"; the three-row design verified by simulation to leave the same
  5 cells) and the vocabulary-narrower-than-the-class note.
- r2_20261105/table2/VERDICT.errata.md: R4 (m5-m9 single-bit, m10 removes three bits), R5 (earliest file: probe66_frozen.py
  02:10:35.403, then cpu_ppc_instr.c.fix575, then MD5.txt; PRETABLE_2 still predates all).
- r2_20261105/PRETABLE_2.errata.md: R6 (the control seed is CTL_CR 0x12345678; the manifest printed the simulator's placeholder 0;
  no prediction depends on it).
- gate_575_block.new: R7 ("every destination pre-set to the INVERSE" -> the truth-table/edge/hi rows inverse, two round-2 rows
  EQUAL, four round-3 rows whole-CR), RESULT=70/70, rows run/green 70, header "70-row", the names list = the base run's 70 names in
  order (one line), the comment's counts (239 / 453 cells, 56 escaped the 66, 0 escape the 70).  Taken from the CURRENT gate block
  (gate lines 331-361 at the time of writing) and changed only there; `bash -n` clean.
- PRETABLE_2.out, SCORES.txt, VERDICT.md, CLOSURE.md: not rewritten.

## Table-3 inputs (written BEFORE any table; the main loop runs the table)

- variants/*.c: 51 = table 2's 27 re-created (cmp-identical to r2_20261105/variants/) + 24 round-3 representatives, each one exact
  edit of GXEMUL-SEC/src/cpus/cpu_ppc_instr.c (one changed statement; u7/u8 move one statement; c_identity is table 1's two-handler
  edit): r1-r4 crorc BB read `& 0x5`, `& 0x8001`, `& 0x40000001`, `& 0x80000001u` (B1 at k = 2, 15, 30 and k = 31); r5 crorc BA
  `& 0x8001` (B2); x1-x4 crandc set literal 0x81u, 0x80001u, 0x40000001u, 0x80000001u (B3 at k = 7, 19, 30 and k = 31); x5-x6
  crorc set literal 0x04000001u, 0x08000001u (B4); z0/z2/z4/z6 the read masks & 0, 2, 4, 6 (one per site); u1-u8 the non-equivalent
  structural families (clear/set re-addressed to (31-ba), (31-bb), bt; the clear between the reads); u9 crorc reads swapped
  (predicted 0 red = EQUIVALENT, like g2).
- PRETABLE_3.out: the 70-row manifest with the REAL control seed 0x12345678 and, per variant, the EXACT red set v575c.py computes;
  the four R5 bt-substitutions PREDICTED ONLY (4, 5, 6, 4 red).  Expectation: base 70/70; HEAD 60/70 (the same ten DISC rows);
  49 variants red exactly as listed; g2 and u9 0 red.
- table3_575.sh: table2_575.sh adapted (clone /tmp/gx575t3, clone-local .MUTANT first, refuses without PRETABLE_3.out and the
  frozen probe table3/probe70_frozen.py -- copy base70/probe70_run.py there; it must be cmp-identical to the in-tree probe -- restore
  = cp from GXEMUL-SEC + cmp + rebuild + `[ gxemul -nt source ]` before the sentinel goes; "[70 rows]" in SCORES.txt); `bash -n` clean.

## Files touched

    edited:  regress/ppc_crlogic_probe.py (docstring clause (e); pin-block comments; +cr_row and 4 rows)
    written: r3_20261105/{ppc_crlogic_probe.py.pre_r3, gate_ppc.sh.pre_r3, v575c.py, CLOSURE3.md, CLEARANCE.txt, PRETABLE_3.out,
             gate_575_block.new, table3_575.sh, IMPL_NOTE.md, base70/probe70_run.py, base70/probe_base70.out, variants/*.c (51)}
             r2_20261105/{CLOSURE.errata.md, PRETABLE_2.errata.md, table2/VERDICT.errata.md}
    not touched: regress/gate_ppc.sh, src/, build/, git.

### F3. the dispositions of pass 3, pass 4 and the second reading (p3_20261105/, p4_20261105/, rec4_20261105/DISPOSITION.md)

# #575 ppccrandcorc PASS 3 -- disposition (main loop, 2026-11-05 ~10:0xZ)

Seats: codex GPT-6 Astra at `ultra` ANSWERED (codex_codex_r575_p3.txt; `CODEXP3R575: 447 CELLS SWEPT 54 BREACHES 7 FALSE RECORDS
VERDICT:REPAIR`; read the packet, CLOSURE.md and source; built and ran nothing).  Gemini 4 Argon x2 ANSWERED (gweb/jobs_20261105_rounds/
p3_r575 and p3_r575_r2: both `VERDICT: CLOSE`, 0 BROKEN) -- they confirmed the four EQUIVALENT cells by derivation and accepted the
239-cell enumeration AS THE PACKET STATED IT; neither re-derived the vocabulary, so their agreement on the brief's own premise is no
evidence (carrier: unanimity on a brief-supplied fact is worth nothing).  glm-5.3 SEAT DOWN (Ollama monthly limit); grok-4.7 SEAT
FAILURE (402 billing wall).

## codex's findings (DERIVED, not measured -- checkable by the round's own simulator)

The 239-cell vocabulary did not exhaust the single-constant edits at two sites it had already put in scope:
* B1 -- crorc's BB read `& 1` -> `& (1 | 1<<k)`, k = 2..30: 29 survivors (the only a=0, b=0 crorc row reads BB=2, whose shifted word
  has no set bit above bit 1).  B2 -- crorc's BA read `& 1` -> `& 0x8001`: 1 survivor.
* B3 -- crandc's set literal `1` -> `1 + 2^k` for 22 values of k; B4 -- crorc's for k = 26, 27: extra SET bits outside the destination,
  invisible because the sessions that would show them check only the destination bit or shift the extra bit out.
* R1-R7: the uniform-seed claim for `crorc bamask` (CR[16] is 0 in its seed); "four rows and no fewer" (one crandc row, `crandc
  16,16,31` seed 0xfffffffe, would cover both crandc additions); the `&7` value in the crandc bbmask comment (6, not 2); table 2 calling
  m5-m10 single-bit masks (m10 removes three bits); table 2's "MD5.txt is the earliest file" (PRETABLE_2.out predates it, but probe66_
  frozen.py and the .fix575 are earlier than MD5.txt); PRETABLE_2's control seed 0 (the probe's CTL_CR is 0x12345678); gate_ppc.sh's
  "every destination pre-set to the INVERSE" (the new rows use equal presets).

## Disposition (standing rules; no new ruling is needed)

* The READ-MASK class was graded a floor breach at pass 2 (glm's `& 1` -> `& 3`) and repair 2's closure put it, and the set
  statement, in its own enumeration -- with a vocabulary ({&3, &7}; |= -> ^=) narrower than the class.  Pass 3 found the same classes
  open.  So, if the simulator confirms B1-B4, they are floor breaches (L2) and repair 3 completes the closure over the FULL
  single-constant space at those sites (codex's 447-cell denominator is the starting point), adding the fewest rows that detect every
  non-equivalent cell, and writes into the contract which cells are covered and which are deliberately not.
* R1-R7 are wrong records (L4): corrected in place in the probe/gate, and as dated errata beside the table-2 files and CLOSURE.md
  (never rewriting a measurement record).  R2 corrects the minimality CLAIM; the four measured rows stay.
* Repair 3 is #575's, an AUP-released item: implemented by a LOCAL Mythos 5.1 run (as repair 2 was).  It writes the gate_ppc.sh change
  as a block file for the main loop to apply, because the qhs repair-7 implementer is editing gate_ppc.sh's qhs block in the same window.

# #575 ppccrandcorc PASS 4 -- disposition (main loop, 2026-11-05 ~09:4xZ)

Seats: codex GPT-6 Astra at `ultra` ANSWERED (codex_codex_r575_p4.txt; `CODEXP4R575: 453 CELLS SWEPT 0 BREACHES 5 FALSE RECORDS
VERDICT:REPAIR`; it read the packet, the handlers, the decoder, the probe, v575c.py, CLOSURE3, the gate block and the records, and
built and ran nothing).  Gemini 4 Argon x2 ANSWERED (gemini_p4_r575.md, gemini_p4_r575_r2.md): both CLOSE, each re-deriving the four
new rows' seeds and whole-CR wants; neither ended in the requested line (scored exit 1 by the sender; read in full).  glm-5.3 SEAT DOWN
(Ollama monthly limit); grok-4.7 SEAT FAILURE (402 billing wall).

## The chain: this is the closing pass

ZERO floor breaches survive, on a VALID pass: the diff was delivered (both probe hunks inlined), the roster's misses are named above,
and the zero carries its denominator -- codex's independent partition of the 453 cells (416 detected, 36 equivalent, 1 disclosed), with
the six constant sites (the four reads, the two set literals) proved over their whole 2^32 value space.  Under the stop condition the
repair chain CLOSES here.

## The five false records (L4 -- corrected in-round; records only, no row and no product change)

* F1 -- CLOSURE3's claim that its proof covers every FIELD-mask constant: the C code masks RAW shifted instruction words (`iword >> 21`
  carries the opcode above BT, and so on), so a mask with bits above bit 4 imports a neighbouring field (BT mask 63 gives BT + 32; BA
  mask 63 imports BT's low bit).  v575c.py masks already-extracted indices and cannot support that extrapolation.  Correct the scope:
  the enumerated field masks m = 0..30 are covered; raw-word masks reaching into neighbouring fields are outside the denominator and
  disclosed (their compiled behaviour, including out-of-range shift counts, is not modelled).
* F2 -- the `64 crorc baread` row's printed note says "a=0 for every mask": the baseline a is 0, and the mutations are caught exactly
  because they make it nonzero (read mask 3 gives a = 2; BA field mask 16 gives a = CR[16] = 1).
* F3 -- the docstring lists "the crandc toggle of (5)" under "EQUIVALENT, proved": it is not equivalent (crandc 31,0,1 over CR 0 must
  leave 0; the toggle gives 1); it is the DISCLOSED cell, as CLOSURE3 itself classifies it.
* F4 -- CLOSURE3:732, "C without bit 0 is red on every result-1 row": later instructions in a session can set the missed bit
  (crorc C = 2: `64 crorc 10` and `32 crorc 10` pass); other rows catch the mutant, and the setbits proof is the correct statement.
* F5 -- "WHY FOUR AND NO FEWER"'s claim that a multi-instruction session would cost more apparatus rows: under the whole-CR comparison,
  one session (seed 0x2; crandc 31,30,31; crorc 30,30,0; mfcr) catches both set-literal families, so three rows suffice; four is the
  minimum only under the single-instruction restriction the round chose.  The four measured rows stay.

The corrections go to the round's ruler and implementer (local Mythos 5.1, which wrote CLOSURE3 -- asked to be harder on its own claims):
dated errata beside CLOSURE3.md, the docstring and the row note corrected in place.  The baread note is a printed string, so the
in-tree probe will then differ from table 3's frozen instrument in TEXT ONLY; that difference is recorded rather than re-tabled, and
the gate's row patterns do not read note text.  A records correction earns a second reading (a correction is not safer than what it
corrects): one Gemini reading of the corrected sentences before landing.

ADDENDUM ~10:1xZ: two later re-sends of the same Gemini jobs (gemini_p4_r575_b.md: VALID AND CLOSES, 0 breaches on 453;
gemini_p4_r575_r2_b.md: UNSETTLED -- the per-cell sections were omitted from its packet for size).  Nothing beyond the record above.

# #575 ppccrandcorc -- second reading of the five records corrections (main loop, 2026-11-05 ~09:5xZ)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED: `CODEXREC4R575: 2 ACCEPTED 3 TO FIX VERDICT:FIX` (codex_codex_r575_rec4.txt; it raised the
five findings and was asked to be harder on their corrections).  Gemini 4 Argon: the first send's control check came back EMPTY
(gweb/rounds.log 03:23:21 local); the retry ANSWERED (gemini_rec4_r575.md, 03:25:16 local).  glm-5.3 / grok-4.7: walled.

Outcome: F3 and F5 ACCEPTED as corrected.  F1, F2 and F4 had each acquired a NEW universal claim in the correction itself -- the
correction-is-not-safer rule landing exactly as written: F1 "a mask above bit 4 imports the neighbouring field" (it MAY; 0x8000001f
decodes exactly) and "the identity in the simulator" (only when (m & 31) == 31); F2's note "only under the fix's decode" (read mask 0
also gives a = 0; the corrected PROBE note itself is true); F4 "with no appeal to the table rows" (crandc C = 3 needs `64 crandc 01`).
All qualified in place in ../r3_20261105/CLOSURE3.errata.md and RECORDS4_NOTE.md (pre-correction copies *.pre_2nd); the probe is
unchanged by this step.  None of it is a detector gap: the chain stays closed.  One phrase of the main loop's own qualification
("0x8000001f keeps only bit 31") was itself wrong and was corrected before this record (it adds bit 31 to the field's five bits).

ADDENDUM: Gemini's reading (gemini_rec4_r575.md) says ACCEPT on all five -- including F1's "masks beyond 5 bits import adjacent fields"
as stated, which codex refuted with a concrete counterexample (0x8000001f decodes exactly).  Gemini read the corrections BEFORE the
qualifications above and ratified the overbroad sentence as the packet gave it; codex's counterexamples are checkable from the code
and stand.  Count the arguments, not the seats: the qualified text is the record.

### G. the fix (the staged src/cpus/cpu_ppc_instr.c against HEAD: the commit's whole change to the file)

```
@@ -2732,7 +2732,7 @@ X(crandc) {
     ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
     bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
     cpu->cd.ppc.cr &= ~(1 << (31-bt));
-    if (!(ba & bb))
+    if (ba & !bb)    /*  #575: CR[BA] & ~CR[BB] (Book I); this was NAND  */
         cpu->cd.ppc.cr |= (1 << (31-bt));
 }
 X(creqv) {
@@ -2759,7 +2759,7 @@ X(crorc) {
     ba = (cpu->cd.ppc.cr >> (31-ba)) & 1;
     bb = (cpu->cd.ppc.cr >> (31-bb)) & 1;
     cpu->cd.ppc.cr &= ~(1 << (31-bt));
-    if (!(ba | bb))
+    if (ba | !bb)    /*  #575: CR[BA] | ~CR[BB] (Book I); this was NOR  */
         cpu->cd.ppc.cr |= (1 << (31-bt));
 }
 X(crnor) {
```

### H. gate 13's #575 block replayed over table 3's banked logs (pretest_575.py; the probe call replaced, marked, by a copy of each log) and the witness

```
Gate 13's `#575` block replayed over table 3's banked logs, the probe call replaced by each log (`regress/artifacts/ppccrandcorc/landing_20261105/DRYRUN575.out`): base (the fix) green; HEAD red (13 of 79 checks); identity bodies red (29 of 79 checks); /bin/true red (69 of 79 checks); /bin/false red (73 of 79 checks); absent binary red (1 of 1 checks).

--- HEAD (probe_HEAD.out): REPLAY_DONE checks=79 fails=13
    FAIL ppc_crlogic RESULT=70/70                             got=0 want=1
    FAIL ppc_crlogic row: 64 crandc 00                        got=0 want=1
    FAIL ppc_crlogic row: 64 crandc 01                        got=0 want=1
    FAIL ppc_crlogic row: 64 crorc 10                         got=0 want=1
    FAIL ppc_crlogic row: 64 crorc 11                         got=0 want=1
    FAIL ppc_crlogic row: edge crandc bt0                     got=0 want=1
    FAIL ppc_crlogic row: edge crorc bt31                     got=0 want=1
    FAIL ppc_crlogic row: 32 crandc 00                        got=0 want=1
    FAIL ppc_crlogic row: 32 crandc 01                        got=0 want=1
    FAIL ppc_crlogic row: 32 crorc 10                         got=0 want=1
    FAIL ppc_crlogic row: 32 crorc 11                         got=0 want=1
    FAIL ppc_crlogic rows green                               got=60 want=70
    FAIL ppc_crlogic rows red                                 got=10 want=0
(every leg's list: landing_20261105/DRYRUN575.out)

witness_20261029/WITNESS_head.out (the 58-row first form on the committed build 987cb596): PPC_CRLOGIC_RESULT=48/58, CONTROL=OK, the ten DISC rows red; an Opus 5.5 seat re-ran it on the same binary: 48/58.
```
