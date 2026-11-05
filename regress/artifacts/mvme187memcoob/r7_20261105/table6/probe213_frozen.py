#!/usr/bin/env python3
"""mvme187memcoob -- DETECTOR (built on its rung-3 witness) for the MVME187 memory controller, dev_mvme187.c.

DEFECT (filed 2026-10-02).  DEVICE_ACCESS(mvme187_memc) ended the emulator (fatal() + exit(1)) on a store to memconf (+0x08) and on any
offset its switch did not name, and indexed the 124-byte register struct with the folded offset (0..0xff) before the switch -- an
out-of-bounds read in the C source for 0x7c..0xff whose value the exiting arms never used.

THE FIX (#NNN).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
folds onto the same image; a memconf store is not kept and is announced once per device; any other offset reads 0, a store there is
not kept, and the first such access is announced once per device with its direction, offset, controller and (for a store) value.  No
indexed read remains: the three served arms read their own fields and the default arm reads none.

WHAT THE ROWS MEASURE.  Cold `-E mvme88k -e mvme187 -M 64` debugger runs (UNMODIFIED in-tree) with r3 = 0xfff43000 (MVME187_MEM_CTLR).
The witness rows place one m88k ld.bu / st.b with `put w` and step it once.  The controls read chipid, chiprev, memconf and controller
1's chipid: their session and pc rows, with `neg apparatus`, are the nine APPARATUS PINS (the CONTROL rows), and their r2 rows pin the
per-field reads.  The four sessions the old code ended (loads of the unserved offsets +0x0c, +0x7c and +0xff, and a memconf store) must
survive to the prompt.  The latch rows need several accesses in ONE emulator lifetime, so msession() places each word at the next word
from 0x10000, steps each once, sends each load to its own register (r2, r4-r15, each seeded with 0x55555555 so a load that does not
retire cannot read as a green 0) and reads them all at the end.  R3: a memconf store of 0xff, the memconf load (3: no bit kept), a
load at +0x7c (0), a controller-1 memconf store; exactly two announce lines, one per category, none naming the second store.  R4: the
chipid and chiprev loads, then four unserved-offset loads, the last through controller 1; the served loads read their fields, the
rest read 0, pc advances, one announce naming offset 0xc.  R5: a default-arm store, the load back (0), an aliased store; one announce
carrying the value.  R6: the six served reads through both controllers; no announce.  R7: through controller 1, a default load, a
memconf load (3) and a memconf store; two announces, both naming controller 1.  R8: a memconf store and a default load set both
latches, then the twelve bytes +0x7c..+0x87 are read one by one; every one reads 0.  Every notice fragment a row matches runs to the
notice's closing " (once) ]".  Row names are at most 16 characters (the gate's two-space anchor).  The multi-access sessions are fifteen:
R3 to R17.  msession() reads r2 and r4..r31 (R16 sends loads up to r27).

REPAIR 5 (p4_20261105/CONS_MYTHOS_local.md section 4; 148 -> 206 rows).  The two announce latches (M = warned_memconf, D =
warned_default) are observed only at memconf stores and default accesses, so the latch states form four phases (M, D) = 00, 10,
01, 11.  R16 (memconf first: phases 00 -> 10 -> 11) and R17 (a default read at +0xf3 first: phase 01) make, in each of their
phases, served byte stores of 0x00 and 0xff with one readback per field per controller and memconf reads through both controllers, with a first
memconf store of 0x07 (controller 0), a controller-1 memconf store of 0x00 and a first default WORD store of 0xffffffff between
R16's phases; R5, R7, R9, R12, R13 and R15 gain tails: a second memconf store after a first store of 0x07 (R7, R15) and of
0xffffffff (R12), a second default access after a first read at 0x0c (R12) and at 0x10c (R7) and after a first word store at 0x118
(R13), a first memconf store of 0x07 made with the default latch set (R5, R13), a first default read through controller 1 after
controller-1 memconf stores (R9), a first default word store with the memconf latch set (R15), and memconf read back after every
0x07 store.  Wants are the ruling's derivation.  These rows are COVERAGE: the closure CONS section 3 claimed for them (every access
kind in every phase, both latches and the three fields read after each) is not what they do -- no controller-0 memconf store occurs
in phase 10 (R16's phase-10 memconf store is ST_B(0,3,0x108), controller 1), no controller-1 default store occurs in phase 11, and
no chipid or chiprev readback follows R16's phase-11 tail (adj_p5_20261105/ADJ_MYTHOS_local.md, R1).

CONTRACT (adj_p5_20261105/ADJ_MYTHOS_local.md section 2, checked line by line against PRETABLE_5.out's survivor summary at
:9460-9697 and tightened where the summary contradicted it: r6_20261105/RECORDS6_NOTE.md).  The FLOOR of this fix is each repair
path's own guard crossed with the state that path reads: the memconf path's {write, !M} x {memconf, M}; the default path's {default
arm, !D} x {D}; each served arm x its own field.  `controller`, len, idata and the offset bits are NOT floor predicates: the fold
rejoins before the switch (dev_mvme187.c:73-76) and no body tests a bit of idata (it is printed at :115 and :133, never tested).
Table 5 (clause (e) below) leaves NO surviving cell in the floor.  COVERED (red in table 5, except the cells disclosed below): any
NONVACUOUS single statement inserted at any of the walk's eleven positions that sets, clears, toggles or value-assigns either announce
latch, or keeps a store into any served field, under no gate or under a conjunction of the position's own tests (direction; controller;
the latch the position's arm reads) or under a single store-value or offset bit the probe's values drive; every NONVACUOUS
single-literal gating or widening of the two latch tests and sets and of the notice's value and direction predicates (identities
such as `!M || !M` are VACUOUS: walked, discarded, never built -- memc_variants_5.py:736-746).  DISCLOSED, NOT CLAIMED --
the five debt families (665 variants green in table 5, every one predicted; filed in r6_20261105/FILING_memccoverdebt.md with the
rows that would close each; a future green variant inside one of them is OUTSIDE this contract, one inside the floor is a breach):
(1) UNFIRED IN-BOUND -- any gate that reads a latch the position's arm does not read (the memconf path never reads D, the default
path never reads M; the served arms, the head and the tail read neither), including the two contexts no row drives: a controller-0
memconf store in state (M, D) = (1, 0) and a controller-1 default store in state (1, 1); and, in the walk's SUPPLEMENTARY alphabet
(walked, not in the ruling's), gates on idata bits 8..31 at the chipid and chiprev arms -- no row makes a word store to +0x00 or
+0x04 (44 UNFIRED representatives, PRETABLE_5.out:9461-9508).  Remedy: complementary store pairs in those two contexts in R16
(0x07 then 0x00; 0xff then 0x00 -- a lone 0x00 is the `|=`/`^=` identity, a lone 0xff the `&=` identity) and word stores of
0xffffffff and 0xffffff00 to +0x00 and +0x04 in two latch states (FILING item 1).  (2) UNOBSERVED -- a kept store into a field the arm does not read, or a latch written from an arm that does not read
it, when gated on a latch or on controller; a `^= idata` or `^= 1` toggle whose selected stores are even in number before the next
observation (R17's two word default stores at +0x1c and +0x11c; R12's and R16's paired served stores), or which lands on a set latch
(1 ^ v is truthy for every store value the rows use: 0x05, 0x07, 0x5a, 0xff, 0xffffffff), or whose only odd driver is R10's 0x5a
default store, after which no memconf store observes M; and `M = idata` at the memconf arm's end under `writeflag == MEM_WRITE &&
!controller` (W.nC, equivalently W.nC.M) -- the WRITE test is part of the survivor: the arm's end lies after the write block
(dev_mvme187.c:105-119), so without it a controller-0 memconf READ (idata 0) clears M and the variant is red (SCORES.txt:570
L_ME_M_idat_nC 201/206 against :2999 L_ME_M_idat_W.nC 206/206) -- whose clearing stores -- the 0x00 controller-0 stores of R3, R7
and R9 -- are each the last memconf store of their session (PRETABLE_5.out:9637, :9639; a group the ruling's own (b) list did not
name).  Remedies: chipid and chiprev readbacks at the tails of R5, R7, R9, R13,
R15 and R17 and after R16's phase-11 tail; a memconf store after R10's 0x5a; an odd count of word default stores in R17; a memconf
store after a controller-0 0x00 store.  (3) NB3 -- a first controller-1 memconf store ORed or XORed into chipid or chiprev: a gate
(controller) x position (first store) x operator three-way joint.  Remedy: chipid and
chiprev readbacks at R7's tail.  (4) NB4 -- `&=` under !controller at the first memconf store, which every controller-0 first store
of 0x07, 0xff or 0xffffffff leaves unchanged on chiprev (0x01) and memconf (0x03): probe-relative only, a 0x00 first store would zero
both.  Remedy: a controller-0 first memconf store of 0x00 followed by chiprev and memconf readbacks.  (5) TO WIDENINGS -- a
widening of either latch test (`!M || G`, `!D || G`) whose G conjoins the other latch (TO_M nC.nD and kin; TO_D W.C.M, W.C.M.D);
every nonvacuous single-literal widening is red.  Remedy: family (1)'s two store pairs.  Also disclosed -- WALKED BUT NOT CLOSED:
the supplementary alphabet named under (1) (idata bits 8..31 at the chipid and chiprev arms; the ME position, the walk's addition,
carries the `M = idata` group under (2)); and the cross-call caveat -- VACUOUS in the walk means no-op under the Boolean-latch
abstraction for ONE access, so `if (idata & 2) D ^= idata` after the default test was walked and DISCARDED as vacuous although
across calls D goes 1 -> 2 -> 0 over default stores of 0x03 then 0x02 and the next default access re-announces; the ungated
`M ^= idata` at the memconf arm's end was BUILT (L_ME_M_xori_any, classed NOCHANGE, 206/206: PRETABLE_5.out:7792, SCORES.txt:2917)
and escapes the same way (M goes 1 -> 2 -> 0 over memconf stores of 0x03 then 0x02).  Neither is a semantic no-op (FILING item 6).
NOT WALKED: disjunctions other than the TO widenings and other non-conjunctive gates, multi-bit masks, len.  WHY L IS WIDER THAN
THE FLOOR: L inserts new side effects and new reads of foreign state at any position; the floor is the repair path's own guard
crossed with its own state, and CONS section 3's "closed enumeration" was a coverage walk, not the floor.

CLAUSE (e) -- catches.  TABLE 5, the record (artifacts/mvme187memcoob/r5_20261105/table5/SCORES.txt; PRETABLE_5.out written before
it): 3,575 variants on these 206 rows -- table 4's 112 and 3,463 L-walk representatives (2,798 red representatives standing for
26,999 predicted-red cells; 665 green, every one predicted and every one in a debt family disclosed in the CONTRACT above); every
table-4 variant red again; 3,518 variants PRED=match, 56 PRED=atleast-ok, one PRED=MISS (D7_fold, detected 175/206: a stale
carry-forward of R7 lines, not an escape).  TABLE 4 (r4_20261105/table4/SCORES.txt, PRETABLE_4.out before it; all 112 of 112
variants red on the then 148-row probe): table 3's 63 (below), the repair-pass-3 seats' 34 measured escapes
(p3_20261105/table_p3; each red on the row repair 4 added for it) and the repair-pass-3 ruling's six families (p3_20261105/
ADJ_MYTHOS.md, 15 cases): a first default store kept, ANDed or ORed (bit 2) into a served field, or kept only through controller 0
(A_B1, M_B4, A_B11, A_B2: R5's and R14's readbacks); a served store kept by =, |=, ^= or &=, only through controller 1, or only
when nonzero (R12's store of 0xff, store of 0x00 and one readback per field and controller -- A_B3, M_B3, A_B4, G_3); a served
access setting the memconf latch (A_B5: R15) or a served store setting the default latch (A_B6: R12's closing default read); the
write notice's value guard or direction conditioned on the controller (A_B7, G_1: R13), on the value (A_B8: R14), on offset bit 4
(M_B2: R14 at +0xe7, the complement of R5's +0x18) or on value bit 8 (M_B1: R13's 0xffffffff); a zero store failing to set the
default latch (A_B9: R14 lines); the printed value truncated to 8 or 16 bits or masked (A_B10, G_5: R12's and R13's 0xffffffff);
a first controller-1 memconf store written into another served field (A_B12: R9); the default latch gated on offset bit 3 (G_6:
R14) or on value bit 8 (M_B1); a non-first store re-announcing on a value bit (M_B5: R5, R9) or ORing bit 2 after the latch (M_B6:
R5's readbacks after its wide aliased store).  Served AND (M_B3) stays red after the 0xff-then-0x00 stores, the ruling's check
that the change to R12 did not open it.  G_2 (the default announce gated on byte width) is OUTSIDE the bound -- len is read by
neither guarded body -- and no row claims width; it reddens anyway, on R13, whose first default access is a word store: an
incidental catch, NOT claimed.  Table 3's 63: each removed defect reinstated verbatim -- the memconf store's exit (B1), the
default arm's exit (B2), the indexed read before the switch (B3: R3 7c r4, R8 7c r4, R8 80 r8 and R11 180 r4); the memconf store kept, whole
(ACCEPT) or above the size code (T2_keepstore); the default arm failing the access (FAULT); either latch's test inverted or its
set dropped; one latch shared by both categories; either latch made per-controller (D6, T2_mlatch_perctl) or the memconf latch
qualified by controller (T2_mlatch_ctl1); the memconf latch set on reads (T2_mlatch_hoist); a served read of chipid, chiprev or
memconf setting the default latch (T2_dlatch_rd00/04/08); the fold mask narrowed; the controller number never set, or replaced
by 0 in the memconf notice (T2_mnotice_ctl0); chiprev reading chipid and chipid reading chiprev (D9, T2_D9b); memconf losing its
field read; the memconf notice keyed on reads; a default-arm store kept and read back; the store notice losing its value, or the
read notice gaining one (T2_valprint); the notice's direction swapped.  Tables 1-3 (the then 56-, 74- and 118-row probes, det_20261104/table1/, table2/ and
r3_20261105/table3/) caught all 19, 29 and 63 of theirs.  THE CELLS CLAIMED (change 7), each enumerated: the first default
announces sit at offsets {0x0c, 0x18, 0x7c, 0xe7, 0xff} (every bit 0-7 both set and clear among them); the first default STORES at
{0x18, 0xe7} (a complement pair) and +0x118 (controller 1); the first store of each notice category is driven at 0x00 (R9, R14),
0xff (R3, R5) and 0xffffffff (R12, R13); non-first stores at 0x05, 0xff and 0xffffffff (R3, R5, R9); every store category
{memconf, default, chipid, chiprev} through each controller is followed by readbacks of the three served fields.  Stores to the
served offsets +0x00 and +0x04 are dropped silently (R12: chipid and chiprev read 0x80 and 0x1 after a store of 0xff and a store
of 0x00, through both controllers).
  discloses, not claimed: multi-axis joints beyond those cells -- three-way joints of a gate, a position (first or non-first) and an
operator among them; an OR-keep of a served field's own set bits (chipid bit 7, chiprev bit 0, memconf bits 0-1), which no store can
make visible because those bits already read 1 (a RAM size whose size code has bit 0 or 1 clear would settle the memconf part);
access width -- G_2 is outside the bound, halfword first accesses are not driven, and wider accesses appear only at +0x00 (a word
load), +0x08 (a word store, a halfword load), +0x108 and +0x118 (word stores); +0x180 reaches the function only because DEVINIT
registers a 0x200-byte window (read at memory_device_register); R8's catch of the reinstated indexed read (B3) holds while the two latches begin within
4 bytes after memcreg -- the struct comment pins that, and the gate's source check (no `memcreg)[` and no `[relative_addr]` in
dev_mvme187.c) covers latches moved before it; and the sanitizer legs (artifacts/mvme187memcoob/det_20261104/asan/, READING.md with
its errata).  Measured: with the indexed read reinstated (B3), the loads at +0x7c and +0xff produce 0 sanitizer reports on both
sanitizer builds.  At +0x7c..+0x83 the byte lies inside the 132-byte allocation, on the latches, so no sanitizer can report it.  At
+0xff the byte lies 123 bytes past the allocation; that it goes unreported is REASONED, not measured (it lands in a neighbouring heap
chunk whose poisoning depends on allocator state, and no shadow dump exists for that access).  R8's loads at +0x84..+0x87 lie in the
allocation's partial granule and are expected to report under ASan on the offline legs (REASONED).  On the plain build the catches
for B3 are R3 7c r4, R8 7c r4, R8 80 r8 and R11 180 r4 (table 4; the same four in table 5, SCORES.txt:8).  MVME187_MEMC_ASAN=n
counts one per "ERROR: AddressSanitizer" or "runtime error:" line; it is informational, read by the offline legs, and no row.  On
these 206 rows the pre-fix build scores 29 of 206 with the symptom PRESENT (33 of the then 148-row probe, 31 of the 118), and the
three null media -- /bin/true 27/206, an absent binary 4/206, /bin/false 5/206 -- each CONTROL=FAIL (r5_20261105/table5/
SCORES.txt:1-5; on the 148 rows 25, 4 and 5, r4_20261105/table4/SCORES.txt).

Sentinel: MVME187_MEMC_PROBE_DONE (plus MVME187_MEMC_RESULT=n/N, MVME187_MEMC_CONTROL=OK|FAIL, MVME187_MEMC_SYMPTOM=PRESENT|ABSENT,
MVME187_MEMC_RED=none|<names>, and the informational MVME187_MEMC_ASAN=n).  Session transcripts go to the optional [workdir].
"""

import os
import re
import subprocess
import sys
import tempfile
import time

if len(sys.argv) < 2:
    sys.stderr.write("usage: mvme187_memc_probe.py <gxemul> [label] [workdir]\n")
    sys.exit(2)

BIN = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "local"
WORK = sys.argv[3] if len(sys.argv) > 3 else None
if WORK:
    os.makedirs(WORK, exist_ok=True)
_TMPDIR = tempfile.mkdtemp(prefix="mvme187_memc_")
DUMMY = os.path.join(_TMPDIR, "dummy.bin")
open(DUMMY, "wb").write(bytes(4))

CODE = 0x00010000
MEMC = 0xfff43000          # MVME187_MEM_CTLR (thirdparty/mvme187.h)
SENT = 0x55555555
FATAL = ("unimplemented read from offset", "unimplemented write to offset", "not yet implemented!")


def LD_BU(rd, rs1, imm):    # m88k ld.bu: op26 0x03, d16 offset (the encoding vme_default_probe.py uses)
    return (0x03 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def ST_B(rs, rs1, imm):     # m88k st.b: op26 0x0b
    return (0x0b << 26) | (rs << 21) | (rs1 << 16) | (imm & 0xffff)


def LD_HU(rd, rs1, imm):    # m88k ld.hu: op26 0x02 (pcc2_width_probe.py's table)
    return (0x02 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def LD_W(rd, rs1, imm):     # m88k ld (word): op26 0x05
    return (0x05 << 26) | (rd << 21) | (rs1 << 16) | (imm & 0xffff)


def ST_W(rs, rs1, imm):     # m88k st (word): op26 0x09
    return (0x09 << 26) | (rs << 21) | (rs1 << 16) | (imm & 0xffff)


assert LD_BU(2, 3, 0x7c) == 0x0C43007C and ST_B(2, 3, 0x08) == 0x2C430008
assert LD_HU(7, 3, 0x08) == 0x08E30008 and LD_W(6, 3, 0) == 0x14C30000 and ST_W(5, 3, 0x08) == 0x24A30008

rows = []
controls = []
symptom_hits = 0
asan_hits = 0                # sanitizer REPORTS across every session (informational: MVME187_MEMC_ASAN, read by the offline legs)


def row(name, got, want, note="", control=False):
    assert name not in [n for n, _ in rows], "DUPLICATE ROW NAME %r" % name
    assert len(name) <= 16, name
    ok = (got == want)
    rows.append((name, ok))
    if control:
        controls.append((name, ok))
    print("%-18s %-20s %-20s %-46s %s" % (name, str(got), str(want), note, "ok" if ok else "FAIL"))
    return ok


def session(name, word, r2, machine="mvme88k", sub="mvme187", timeout=60):
    """One cold run: r3 = MEMC, r2 = `r2`, `word` at CODE, one step, `reg`.  Returns (regs, text, how)."""
    global symptom_hits
    cmds = ["r3=0x%x" % MEMC, "r2=0x%x" % r2, "put w 0x%x, 0x%08x" % (CODE, word), "pc=0x%x" % CODE, "step 1", "reg", "quit"]
    argv = [BIN, "-V", "-x", "-E", machine] + (["-e", sub] if sub else []) + ["-M", "64", "0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:            # an ABSENT binary is a null medium: every row fails, the sentinel still prints
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
    if how != "exit0" and any(f in t for f in FATAL):
        symptom_hits += 1
    count_asan(t)
    regs = {}
    i = t.rfind("GXemul> reg")
    if i >= 0:
        seg = t[i:]
        for k in ("pc", "r2"):
            m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg)
            if m:
                regs[k] = int(m.group(1), 16)
    return regs, t, how


def hx(regs, k):
    return hex(regs[k]) if k in regs else "none"


def count_asan(t):
    """One per report: an "ERROR: AddressSanitizer" line or a UBSan "runtime error:" line (a report's SUMMARY line repeats the
    AddressSanitizer token, so a substring count would score one report twice)."""
    global asan_hits
    asan_hits += sum(1 for line in t.split("\n") if "ERROR: AddressSanitizer" in line or "runtime error:" in line)


def msession(name, words, init, timeout=60):
    """One cold run with SEVERAL accesses: r3 = MEMC and the `init` registers, then each word placed with `put w` at the next word
    from CODE and stepped once, then one `reg`.  Returns (regs, text, how, announce-line count)."""
    global symptom_hits
    cmds = (["r3=0x%x" % MEMC] + ["%s=0x%x" % (r, v) for r, v in init] +
            ["put w 0x%x, 0x%08x" % (CODE + 4 * i, w) for i, w in enumerate(words)] + ["pc=0x%x" % CODE] +
            ["step 1"] * len(words) + ["reg", "quit"])
    argv = [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64", "0x%x:%s" % (CODE, DUMMY)]
    inp = ("\n".join(cmds) + "\n").encode("latin-1")
    try:
        p = subprocess.run(argv, input=inp, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        t = p.stdout.decode("latin-1", "replace").replace("\r", "")
        rc = p.returncode
        how = ("sig%d" % -rc) if rc < 0 else ("exit%d" % rc)
    except subprocess.TimeoutExpired as e:
        t = (e.output or b"").decode("latin-1", "replace").replace("\r", "")
        how = "TIMEOUT"
    except OSError as e:
        t = ""
        how = "NOBIN(%s)" % e.__class__.__name__
    if WORK:
        open(os.path.join(WORK, name.replace(" ", "_") + ".txt"), "w", encoding="latin-1").write(
            "$ " + " ".join(argv) + "\n--- stdin ---\n" + "\n".join(cmds) + "\n--- transcript (%s) ---\n" % how + t)
    if how != "exit0" and any(f in t for f in FATAL):
        symptom_hits += 1
    count_asan(t)
    regs = {}
    i = t.rfind("GXemul> reg")
    if i >= 0:
        seg = t[i:]
        for k in ("pc", "r2") + tuple("r%d" % i for i in range(4, 32)):     # repair 5: R16 reads up to r27
            m = re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg)
            if m:
                regs[k] = int(m.group(1), 16)
    return regs, t, how, str(t.count("mvme187_memc:"))


def has(t, frag):
    return "yes" if frag in t else "no"


def prompt(t):
    return "yes" if ("GXemul> reg" in t and "cpu0:" in t[t.rfind("GXemul> reg"):]) else "no"


print("mvme187memcoob DETECTOR -- binary=%s label=%s" % (BIN, LABEL))
print("machine: -E mvme88k -e mvme187 -M 64 (UNMODIFIED in-tree); MEMC at 0x%x" % MEMC)
print("%-18s %-20s %-20s %-46s %s" % ("row", "got", "want", "note", ""))
t0 = time.time()

#  No `-e` here: measured 2026-11-04, `-E nosuchmachine -e mvme187` CONSTRUCTS the mvme187 (exit 0, chipid read back) --
#  the subtype name selects the machine -- so a negative control that keeps `-e` controls nothing.
nr, _, nhow = session("neg", LD_BU(2, 3, 0), SENT, machine="nosuchmachine", sub=None, timeout=30)
row("neg apparatus", "%s/%s" % (nhow, hx(nr, "r2")), "exit1/none", "a bogus machine runs no guest", control=True)
for nm, off, want, note in (("chipid", 0x00, 0x80, "MEMC_CHIPID"), ("chiprev", 0x04, 0x1, "DEVINIT chiprev = 1"),
                            ("memconf", 0x08, 0x3, "DEVINIT memconf for 64 MB (RTOB(3) = 32 MB)"),
                            ("ctl1id", 0x100, 0x80, "controller 1 aliases chipid")):
    r, T, how = session("ctl " + nm, LD_BU(2, 3, off), SENT)
    row("ctl %s sess" % nm, how, "exit0", "ld.bu +0x%x: exit status" % off, control=True)
    row("ctl %s r2" % nm, hx(r, "r2"), hex(want), note)
    row("ctl %s pc" % nm, hx(r, "pc"), hex(CODE + 4), "one instruction retired", control=True)

for nm, word, note in (("rd 0x0c", LD_BU(2, 3, 0x0c), "ld.bu +0x0c (first unimplemented offset)"),
                       ("rd 0x7c", LD_BU(2, 3, 0x7c), "ld.bu +0x7c (first byte past memcreg: the first latch byte)"),
                       ("rd 0xff", LD_BU(2, 3, 0xff), "ld.bu +0xff (the last offset)"),
                       ("wr cnf", ST_B(2, 3, 0x08), "st.b +0x08 (memconf write)")):
    r, T, how = session(nm, word, 0x7 if nm.startswith("wr") else SENT)
    row(nm + " session", how, "exit0", note + ": survives")
    row(nm + " prompt", prompt(T), "yes", "the debugger ran `reg` afterwards")

# ======================================================= MULTI-ACCESS ROWS (R3-R6) ==
#  R3: a memconf store of 0xff, the memconf load, a load at +0x7c, a controller-1 memconf store, the controller-1 memconf load, a second
#  controller-0 memconf store (0x00, from r0), and loads of memconf, chipid and chiprev -- two announce lines, one per category.  The
#  repair-3 additions (ADJ_MYTHOS.md, mvme187memcoob p2r): every bit of memconf written both set (0xff) and clear (0x00) and read back
#  (N6), a load after the controller-1 store (N7, N19), the served fields read after a memconf store (N9), a second controller-0 store
#  that must stay quiet (N1).
r, T, how, nl = msession("R3", [ST_B(5, 3, 0x08), LD_BU(2, 3, 0x08), LD_BU(4, 3, 0x7c), ST_B(6, 3, 0x108), LD_BU(9, 3, 0x108),
                                ST_B(0, 3, 0x08), LD_BU(11, 3, 0x08), LD_BU(12, 3, 0x00), LD_BU(13, 3, 0x04)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0xff), ("r6", 0x05), ("r9", SENT), ("r11", SENT), ("r12", SENT),
                          ("r13", SENT)])
row("R3 session", how, "exit0", "nine accesses in one run: survives")
row("R3 cnf r2", hx(r, "r2"), hex(0x3), "memconf still reads 3: no bit outside the size code was kept")
row("R3 7c r4", hx(r, "r4"), hex(0), "the load past memcreg (the first latch byte) reads 0")
row("R3 108 r9", hx(r, "r9"), hex(0x3), "memconf via controller 1 after its store: still 3")
row("R3 cnf0 r11", hx(r, "r11"), hex(0x3), "memconf after a 0x00 store: still 3")
row("R3 00 r12", hx(r, "r12"), hex(0x80), "chipid after the memconf stores")
row("R3 04 r13", hx(r, "r13"), hex(0x1), "chiprev after the memconf stores")
row("R3 pc", hx(r, "pc"), hex(CODE + 36), "nine instructions retired")
row("R3 lines", nl, "2", "one announce per category, each latched")
row("R3 cnf line", has(T, "memconf write 0xff (controller 0) ignored, not modelled (once) ]"), "yes",
    "the memconf store is announced")
row("R3 7c line", has(T, "unimplemented read from offset 0x7c (controller 0) (once) ]"), "yes", "the default-arm read is announced")
row("R3 no 0x5", has(T, "memconf write 0x5"), "no", "the controller-1 memconf store is latched quiet")
row("R3 no 0x0", has(T, "memconf write 0x0"), "no", "the second controller-0 store is latched quiet")
#  R4: the chipid and chiprev loads, then four unserved-offset loads, the last through controller 1 -- one announce, the served loads
#  read their fields and no served read sets the default latch (ADJ_MYTHOS.md M26/X1), the rest read 0, pc advances.
r, T, how, nl = msession("R4", [LD_BU(7, 3, 0x00), LD_BU(8, 3, 0x04), LD_BU(2, 3, 0x0c), LD_BU(4, 3, 0x7c), LD_BU(5, 3, 0xff),
                                LD_BU(6, 3, 0x10c)],
                         [("r2", SENT), ("r4", SENT), ("r5", SENT), ("r6", SENT), ("r7", SENT), ("r8", SENT)])
row("R4 session", how, "exit0", "two served, four default-arm loads: survives")
row("R4 00 r7", hx(r, "r7"), hex(0x80), "chipid, read first")
row("R4 04 r8", hx(r, "r8"), hex(0x1), "chiprev, read second")
row("R4 0c", hx(r, "r2"), hex(0), "ld.bu +0x0c reads 0")
row("R4 7c", hx(r, "r4"), hex(0), "ld.bu +0x7c reads 0")
row("R4 ff", hx(r, "r5"), hex(0), "ld.bu +0xff reads 0")
row("R4 10c", hx(r, "r6"), hex(0), "ld.bu +0x10c (controller 1) reads 0")
row("R4 pc", hx(r, "pc"), hex(CODE + 24), "no fault: six instructions retired")
row("R4 lines", nl, "1", "one announce for the device, both controllers")
row("R4 line text", has(T, "unimplemented read from offset 0xc (controller 0) (once) ]"), "yes",
    "the first default offset is the one named")
#  R5: a default-arm store of 0xff, the load back, an aliased WORD store of 0xffffffff through controller 1, then the three served
#  fields read back -- no store is kept, the write is announced once with its value, and no store reaches a served field.  Repair 4
#  (p3_20261105/ADJ_MYTHOS.md, D3(a) and change 4): the first store sets every bit 0-7 (A_B1, A_B2 and A_B11's kept stores); the
#  second store is wide and NON-first, the distinction the default latch draws (B5's re-announce disjunct, B6's post-latch OR); the
#  readbacks come last so they see both stores.  Repair 5 tail: a first memconf store (0x07, controller 0) made with the default latch
#  set, then memconf read back -- the memconf latch is set from phase 01 by a default-first byte store (F4's tail form, F10's `if (D)`).
r, T, how, nl = msession("R5", [ST_B(5, 3, 0x18), LD_BU(2, 3, 0x18), ST_W(6, 3, 0x118), LD_BU(7, 3, 0x00), LD_BU(8, 3, 0x04),
                                LD_BU(9, 3, 0x08), ST_B(10, 3, 0x08), LD_BU(11, 3, 0x08)],
                         [("r2", SENT), ("r5", 0xff), ("r6", 0xffffffff), ("r7", SENT), ("r8", SENT), ("r9", SENT), ("r10", 0x07),
                          ("r11", SENT)])
row("R5 session", how, "exit0", "store, load back, aliased wide store, readbacks, memconf store: survives")
row("R5 r2", hx(r, "r2"), hex(0), "the default-arm store was not kept")
row("R5 00 r7", hx(r, "r7"), hex(0x80), "chipid after both default stores")
row("R5 04 r8", hx(r, "r8"), hex(0x1), "chiprev after both default stores")
row("R5 08 r9", hx(r, "r9"), hex(0x3), "memconf after both default stores")
row("R5 08b r11", hx(r, "r11"), hex(0x3), "memconf after its own 0x07 store: still 3")
row("R5 pc", hx(r, "pc"), hex(CODE + 32), "eight instructions retired")
row("R5 lines", nl, "2", "two announces: the default store, the memconf store")
row("R5 line text", has(T, "unimplemented write to offset 0x18 (controller 0): 0xff (once) ]"), "yes",
    "the write names its value")
row("R5 cnf line", has(T, "memconf write 0x7 (controller 0) ignored, not modelled (once) ]"), "yes",
    "the memconf store after a default store is announced")
#  R6: the six served reads through both controllers -- the fold, the per-field arms, and no announce on a served offset.
r, T, how, nl = msession("R6", [LD_BU(2, 3, 0x00), LD_BU(4, 3, 0x04), LD_BU(5, 3, 0x08), LD_BU(6, 3, 0x100), LD_BU(7, 3, 0x104),
                                LD_BU(8, 3, 0x108)],
                         [("r2", SENT), ("r4", SENT), ("r5", SENT), ("r6", SENT), ("r7", SENT), ("r8", SENT)])
row("R6 session", how, "exit0", "six served loads: survives")
row("R6 00", hx(r, "r2"), hex(0x80), "chipid")
row("R6 04", hx(r, "r4"), hex(0x1), "chiprev")
row("R6 08", hx(r, "r5"), hex(0x3), "memconf")
row("R6 100", hx(r, "r6"), hex(0x80), "controller 1 chipid (the fold)")
row("R6 104", hx(r, "r7"), hex(0x1), "controller 1 chiprev")
row("R6 108", hx(r, "r8"), hex(0x3), "controller 1 memconf")
row("R6 pc", hx(r, "pc"), hex(CODE + 24), "six instructions retired")
row("R6 lines", nl, "0", "no announce on a served offset")
#  R7: through controller 1, a default load, a memconf load and a memconf store -- both notices name controller 1 (the fix's comment
#  says the number is reported in the notices), and the memconf LOAD must not set the memconf latch (ADJ_MYTHOS.md M5, M25).
#  Repair 5 tail: a second memconf store (0x00, controller 0) after a first store made with the default latch set (F1), a second
#  default read (F3: no default-latch clear in the memconf arm) and the memconf readback -- both silent, lines stays 2.
r, T, how, nl = msession("R7", [LD_BU(2, 3, 0x10c), LD_BU(4, 3, 0x108), ST_B(5, 3, 0x108), ST_B(0, 3, 0x08), LD_BU(6, 3, 0x10c),
                                LD_BU(7, 3, 0x108)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0x07), ("r6", SENT), ("r7", SENT)])
row("R7 session", how, "exit0", "three controller-1 accesses, then the tail: survives")
row("R7 r2", hx(r, "r2"), hex(0), "the default load reads 0")
row("R7 108 r4", hx(r, "r4"), hex(0x3), "the controller-1 memconf load reads 3")
row("R7 10c r6", hx(r, "r6"), hex(0), "the second default load reads 0 (and is silent)")
row("R7 108b r7", hx(r, "r7"), hex(0x3), "memconf after the 0x07 and 0x00 stores: still 3")
row("R7 pc", hx(r, "pc"), hex(CODE + 24), "six instructions retired")
row("R7 lines", nl, "2", "two announces: default, then memconf; the tail is silent")
row("R7 line text", has(T, "unimplemented read from offset 0xc (controller 1) (once) ]"), "yes", "the notice names controller 1")
row("R7 cnf line", has(T, "memconf write 0x7 (controller 1) ignored, not modelled (once) ]"), "yes",
    "the memconf notice names controller 1")
#  R8: the reinstated indexed read (B3) on either byte order (ADJ_MYTHOS.md M3, X5): both latches set, then the twelve bytes past
#  memcreg read one by one -- +0x7c..+0x83 are the two latches inside struct mvme187_data (dev_mvme187.c:47-56), +0x84..+0x87 lie
#  past the struct's end.  The fix's default arm forwards no byte of the device struct, so every one reads 0; the old read forwarded
#  the latches.  r5 is the store's source (0x7) and also +0x7d's destination, so it starts non-zero too.
r, T, how, nl = msession("R8", [ST_B(5, 3, 0x08), LD_BU(2, 3, 0x0c)] + [LD_BU(4 + i, 3, 0x7c + i) for i in range(12)],
                         [("r2", SENT), ("r5", 0x07)] + [("r%d" % (4 + i), SENT) for i in range(12) if 4 + i != 5])
row("R8 session", how, "exit0", "both latches set, then twelve loads: survives")
for i in range(12):
    row("R8 %02x r%d" % (0x7c + i, 4 + i), hx(r, "r%d" % (4 + i)), hex(0), "+0x%x reads 0: no struct byte forwarded" % (0x7c + i))
row("R8 pc", hx(r, "pc"), hex(CODE + 56), "fourteen instructions retired")
row("R8 lines", nl, "2", "one announce per category")
#  R9: controller 1 first, memconf: a 0x00 store, then a WORD store of 0xffffffff, then memconf read through controller 1 and
#  controller 0, then chipid and chiprev -- the latch is set by the FIRST store whatever its value (an idata-gated latch announces the
#  second; ADJ_MYTHOS.md change 5), it is set through controller 1 (N2), no store is kept by either controller (N6, N7, N19), the
#  first controller-1 store reaches no other served field (A_B12), and the wide non-first store does not re-announce (B5; repair 4).
#  Repair 5 tail: a first default read through controller 1 AFTER the controller-1 memconf stores (0x00 first, 0xffffffff non-first)
#  -- its notice shows no memconf-arm statement set the default latch (F2, F7) -- then a third memconf store (0x00, controller 0,
#  silent) and the memconf readback.
r, T, how, nl = msession("R9", [ST_B(0, 3, 0x108), ST_W(5, 3, 0x108), LD_BU(2, 3, 0x108), LD_BU(4, 3, 0x08), LD_BU(6, 3, 0x00),
                                LD_BU(7, 3, 0x04), LD_BU(8, 3, 0x10c), ST_B(0, 3, 0x08), LD_BU(9, 3, 0x08)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0xffffffff), ("r6", SENT), ("r7", SENT), ("r8", SENT), ("r9", SENT)])
row("R9 session", how, "exit0", "two controller-1 memconf stores, then the tail: survives")
row("R9 108 r2", hx(r, "r2"), hex(0x3), "memconf via controller 1: still 3")
row("R9 08 r4", hx(r, "r4"), hex(0x3), "memconf via controller 0: still 3")
row("R9 00 r6", hx(r, "r6"), hex(0x80), "chipid after the controller-1 memconf stores")
row("R9 04 r7", hx(r, "r7"), hex(0x1), "chiprev after the controller-1 memconf stores")
row("R9 10c r8", hx(r, "r8"), hex(0), "the first default read, after the memconf stores, reads 0")
row("R9 08b r9", hx(r, "r9"), hex(0x3), "memconf after the third store: still 3")
row("R9 lines", nl, "2", "two announces: the first memconf store, the first default read")
row("R9 no wide", has(T, "memconf write 0xffffffff"), "no", "the second, wide store is latched quiet")
row("R9 cnf line", has(T, "memconf write 0x0 (controller 1) ignored, not modelled (once) ]"), "yes",
    "the first store, value 0, is announced")
row("R9 def line", has(T, "unimplemented read from offset 0xc (controller 1) (once) ]"), "yes",
    "the default latch was still clear after the memconf stores")
row("R9 pc", hx(r, "pc"), hex(CODE + 36), "nine instructions retired")
#  R10: controller 1 first, default: two default loads, a default store through controller 1, then the stored offset read back through
#  both controllers, memconf, chipid and chiprev -- the default latch is set through controller 1 (N3), no default store is kept (N8),
#  and a default store reaches no served field (N9; change 3).
r, T, how, nl = msession("R10", [LD_BU(2, 3, 0x10c), LD_BU(4, 3, 0x110), ST_B(5, 3, 0x118), LD_BU(6, 3, 0x118), LD_BU(7, 3, 0x18),
                                 LD_BU(8, 3, 0x08), LD_BU(9, 3, 0x00), LD_BU(10, 3, 0x04)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0x5a), ("r6", SENT), ("r7", SENT), ("r8", SENT), ("r9", SENT),
                          ("r10", SENT)])
row("R10 session", how, "exit0", "controller-1 default accesses first: survives")
row("R10 118 r6", hx(r, "r6"), hex(0), "the default store was not kept (ctl 1)")
row("R10 18 r7", hx(r, "r7"), hex(0), "nor seen through controller 0")
row("R10 08 r8", hx(r, "r8"), hex(0x3), "memconf after a default store")
row("R10 00 r9", hx(r, "r9"), hex(0x80), "chipid after a default store")
row("R10 04 r10", hx(r, "r10"), hex(0x1), "chiprev after a default store")
row("R10 lines", nl, "1", "one announce: the first default access")
row("R10 line text", has(T, "unimplemented read from offset 0xc (controller 1) (once) ]"), "yes",
    "the first default access names controller 1")
row("R10 pc", hx(r, "pc"), hex(CODE + 32), "eight instructions retired")
#  R11: the first default access is +0xff through controller 0 (a fold test widened by bit 7 would name controller 1: N5), then the
#  fold and selector edges -- +0x180 (a fold clear widened by bit 7 reads chipid: N4), the sub-word aliases +0x01 and +0x0a (N21), the
#  fold-clear bits 0, 1, 5, 6 (+0x101, +0x102, +0x120, +0x140: change 1) and the selector bits 5, 6 (+0x20, +0x40: change 2).  The
#  window is 0x200 bytes (DEVINIT), so +0x180 reaches the function.  Every one reads 0 on the fix.
r, T, how, nl = msession("R11", [LD_BU(2, 3, 0xff), LD_BU(4, 3, 0x180), LD_BU(5, 3, 0x01), LD_BU(6, 3, 0x0a), LD_BU(7, 3, 0x101),
                                 LD_BU(8, 3, 0x102), LD_BU(9, 3, 0x120), LD_BU(10, 3, 0x140), LD_BU(11, 3, 0x20),
                                 LD_BU(12, 3, 0x40)],
                         [("r%d" % i, SENT) for i in (2, 4, 5, 6, 7, 8, 9, 10, 11, 12)])
row("R11 session", how, "exit0", "ten default loads: survives")
row("R11 180 r4", hx(r, "r4"), hex(0), "+0x180 folds to 0x80: reads 0")
row("R11 01 r5", hx(r, "r5"), hex(0), "+0x01 is not chipid")
row("R11 0a r6", hx(r, "r6"), hex(0), "+0x0a is not memconf")
row("R11 101 r7", hx(r, "r7"), hex(0), "+0x101 folds to 0x01: reads 0")
row("R11 102 r8", hx(r, "r8"), hex(0), "+0x102 folds to 0x02: reads 0")
row("R11 120 r9", hx(r, "r9"), hex(0), "+0x120 folds to 0x20: reads 0")
row("R11 140 r10", hx(r, "r10"), hex(0), "+0x140 folds to 0x40: reads 0")
row("R11 20 r11", hx(r, "r11"), hex(0), "+0x20 is not chipid")
row("R11 40 r12", hx(r, "r12"), hex(0), "+0x40 is not chipid")
row("R11 line text", has(T, "unimplemented read from offset 0xff (controller 0) (once) ]"), "yes",
    "the first default access, +0xff, controller 0")
row("R11 lines", nl, "1", "one announce for the device")
row("R11 pc", hx(r, "pc"), hex(CODE + 40), "ten instructions retired")
#  R12: a WORD store of 0xffffffff to memconf first (the notice prints the whole value; every bit 0-31 is set, so a value truncated to
#  any width or gated on any bit shows -- repair 4, change 1 and B1), then for each served field through each controller (+0x00,
#  +0x04, +0x100, +0x104) a byte store of 0xff, a byte store of 0x00 and ONE readback (change 3: one readback after both stores reds a
#  kept store under =, |=, ^= and &=, and an idata-gated one), then chipid by word, memconf by halfword and by byte, and a default read
#  LAST, whose notice shows that no served store set the default latch (A_B6).
#  Repair 5: a memconf byte read after the controller-0 pairs (family C: a served store XORed into memconf would read 0xfc there),
#  then a tail -- a second memconf store (0x00, controller 1) after the 0xffffffff first store (family A; F5's parity under the c1
#  toggles), a second default read (family A) and the memconf readback -- all silent, lines stays 2.
r, T, how, nl = msession("R12", [ST_W(5, 3, 0x08), ST_B(9, 3, 0x00), ST_B(0, 3, 0x00), LD_BU(2, 3, 0x00), ST_B(9, 3, 0x04),
                                 ST_B(0, 3, 0x04), LD_BU(4, 3, 0x04), LD_BU(13, 3, 0x08), ST_B(9, 3, 0x100), ST_B(0, 3, 0x100),
                                 LD_BU(10, 3, 0x100), ST_B(9, 3, 0x104), ST_B(0, 3, 0x104), LD_BU(11, 3, 0x104), LD_W(6, 3, 0x00),
                                 LD_HU(7, 3, 0x08), LD_BU(8, 3, 0x08), LD_BU(12, 3, 0x0c), ST_B(0, 3, 0x108), LD_BU(14, 3, 0x0c),
                                 LD_BU(15, 3, 0x08)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0xffffffff), ("r6", SENT), ("r7", SENT), ("r8", SENT), ("r9", 0xff),
                          ("r10", SENT), ("r11", SENT), ("r12", SENT), ("r13", SENT), ("r14", SENT), ("r15", SENT)])
row("R12 session", how, "exit0", "word, halfword and served-offset accesses, then the tail")
row("R12 cnf line", has(T, "memconf write 0xffffffff (controller 0) ignored, not modelled (once) ]"), "yes",
    "the word store's whole value is announced")
row("R12 00 r2", hx(r, "r2"), hex(0x80), "chipid kept after stores of 0xff and 0x00")
row("R12 04 r4", hx(r, "r4"), hex(0x1), "chiprev kept after stores of 0xff and 0x00")
row("R12 m08 r13", hx(r, "r13"), hex(0x3), "memconf after the controller-0 chipid/chiprev pairs: still 3")
row("R12 100 r10", hx(r, "r10"), hex(0x80), "chipid kept after controller-1 stores")
row("R12 104 r11", hx(r, "r11"), hex(0x1), "chiprev kept after controller-1 stores")
row("R12 w00 r6", hx(r, "r6"), hex(0x80), "chipid by word: 0x00000080")
row("R12 h08 r7", hx(r, "r7"), hex(0x3), "memconf by halfword: 0x0003")
row("R12 08 r8", hx(r, "r8"), hex(0x3), "memconf after the word store: still 3")
row("R12 0c r12", hx(r, "r12"), hex(0), "the default read at the end reads 0")
row("R12 0cb r14", hx(r, "r14"), hex(0), "the second default read, after the c1 memconf store, reads 0")
row("R12 08b r15", hx(r, "r15"), hex(0x3), "memconf after the controller-1 0x00 store: still 3")
row("R12 0c line", has(T, "unimplemented read from offset 0xc (controller 0) (once) ]"), "yes",
    "no served store set the default latch")
row("R12 lines", nl, "2", "two announces: the memconf store, the default read; the tail is silent")
row("R12 pc", hx(r, "pc"), hex(CODE + 84), "twenty-one instructions retired")
#  R13: a controller-1 default WORD store of 0xffffffff FIRST -- the write notice's value guard and direction with controller 1, and the
#  printed value at full width (A_B7, G_1, G_5, A_B10; B1 of the repair-4 ruling) -- then the three served fields.
#  Repair 5 tail: a first memconf store (0x07, controller 0) with the default latch set by a controller-1 WORD default store (the
#  memconf latch set from phase 01: F10's `if (D)`), its readback, and a second default access (family A: the 0xffffffff first
#  default store's gated latch set).
r, T, how, nl = msession("R13", [ST_W(5, 3, 0x118), LD_BU(2, 3, 0x00), LD_BU(4, 3, 0x04), LD_BU(6, 3, 0x08), ST_B(7, 3, 0x08),
                                 LD_BU(8, 3, 0x08), LD_BU(9, 3, 0x10c)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0xffffffff), ("r6", SENT), ("r7", 0x07), ("r8", SENT), ("r9", SENT)])
row("R13 session", how, "exit0", "a controller-1 default word store first, then the tail")
row("R13 line text", has(T, "unimplemented write to offset 0x18 (controller 1): 0xffffffff (once) ]"), "yes",
    "the write names controller 1 and the whole value")
row("R13 00 r2", hx(r, "r2"), hex(0x80), "chipid after the default store")
row("R13 04 r4", hx(r, "r4"), hex(0x1), "chiprev after the default store")
row("R13 08 r6", hx(r, "r6"), hex(0x3), "memconf after the default store")
row("R13 08b r8", hx(r, "r8"), hex(0x3), "memconf after its own 0x07 store: still 3")
row("R13 10c r9", hx(r, "r9"), hex(0), "the second default access reads 0 (and is silent)")
row("R13 cnf line", has(T, "memconf write 0x7 (controller 0) ignored, not modelled (once) ]"), "yes",
    "the memconf store after a default store is announced")
row("R13 lines", nl, "2", "two announces: the default store, the memconf store")
row("R13 pc", hx(r, "pc"), hex(CODE + 28), "seven instructions retired")
#  R14: a ZERO default store FIRST at +0xe7 -- the bitwise complement of R5's +0x18, so every offset bit 0-7 is set at one rowed first
#  default store and clear at another (B2 of the repair-4 ruling) -- then the three served fields (B4: an &= keep reads 0) and a later
#  default read (A_B9: a zero store must still set the latch).  The notice prints the value 0 (A_B8).
r, T, how, nl = msession("R14", [ST_B(0, 3, 0xe7), LD_BU(2, 3, 0x00), LD_BU(4, 3, 0x04), LD_BU(5, 3, 0x08), LD_BU(6, 3, 0x0c)],
                         [("r2", SENT), ("r4", SENT), ("r5", SENT), ("r6", SENT)])
row("R14 session", how, "exit0", "a zero default store first")
row("R14 line text", has(T, "unimplemented write to offset 0xe7 (controller 0): 0x0 (once) ]"), "yes",
    "the zero store is announced with its value")
row("R14 00 r2", hx(r, "r2"), hex(0x80), "chipid after the zero store")
row("R14 04 r4", hx(r, "r4"), hex(0x1), "chiprev after the zero store")
row("R14 08 r5", hx(r, "r5"), hex(0x3), "memconf after the zero store")
row("R14 0c r6", hx(r, "r6"), hex(0), "the later default read reads 0")
row("R14 lines", nl, "1", "the zero store set the latch: one announce")
row("R14 pc", hx(r, "pc"), hex(CODE + 20), "five instructions retired")
#  R15: chipid and chiprev read FIRST, then a memconf store -- a served access must not set the memconf latch (A_B5).
#  Repair 5 tail: a first default WORD store (0xffffffff, controller 0, +0x1c) with the memconf latch set, a second memconf store
#  (0x00, controller 1, silent: no default-arm statement clears the memconf latch) and the memconf readback after the 0x07 store.
r, T, how, nl = msession("R15", [LD_BU(2, 3, 0x00), LD_BU(4, 3, 0x04), ST_B(5, 3, 0x08), ST_W(6, 3, 0x1c), ST_B(0, 3, 0x108),
                                 LD_BU(7, 3, 0x08)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0x07), ("r6", 0xffffffff), ("r7", SENT)])
row("R15 session", how, "exit0", "served reads, a memconf store, then the tail")
row("R15 00 r2", hx(r, "r2"), hex(0x80), "chipid")
row("R15 04 r4", hx(r, "r4"), hex(0x1), "chiprev")
row("R15 08 r7", hx(r, "r7"), hex(0x3), "memconf after the 0x07 and 0x00 stores: still 3")
row("R15 cnf line", has(T, "memconf write 0x7 (controller 0) ignored, not modelled (once) ]"), "yes",
    "the memconf store after served reads is announced")
row("R15 def line", has(T, "unimplemented write to offset 0x1c (controller 0): 0xffffffff (once) ]"), "yes",
    "the first default access, a word store with the memconf latch set, is announced")
row("R15 lines", nl, "2", "two announces: the memconf store, the default store")
row("R15 pc", hx(r, "pc"), hex(CODE + 24), "six instructions retired")
#  R16 (repair 5, NEW): memconf first -- phases 00 -> 10 -> 11.  In each phase, for chipid and then chiprev: ONE store through
#  controller 1 (0x00 in phase 00, 0xff in phases 10 and 11), then a controller-0 pair (0x00 then 0xff in phases 00 and 10; 0xff
#  then 0x00 in phase 11) and one readback, then memconf read through both controllers.  Between the
#  phases: a first memconf store of 0x07 (announces), a silent controller-1 memconf store of 0x00, a first default WORD store of
#  0xffffffff through controller 1 at +0x1c (announces).  Then in phase 11: a default read at +0x83 (the complement of R3's +0x7c), a
#  default word store at +0x1c, a controller-1 default read, a WORD memconf store of 0xffffffff, a default read at +0x1c and the final
#  memconf read -- every tail access silent (lines stays 2) and every field unchanged (CONS_MYTHOS_local.md section 3's product).
r, T, how, nl = msession("R16", [ST_B(0, 3, 0x100), LD_BU(2, 3, 0x100), ST_B(0, 3, 0x00), ST_B(5, 3, 0x00), LD_BU(4, 3, 0x00),
                                 ST_B(0, 3, 0x104), LD_BU(7, 3, 0x104), ST_B(0, 3, 0x04), ST_B(5, 3, 0x04), LD_BU(8, 3, 0x04),
                                 LD_BU(10, 3, 0x08), LD_BU(11, 3, 0x108),
                                 ST_B(6, 3, 0x08),
                                 ST_B(5, 3, 0x100), LD_BU(12, 3, 0x100), ST_B(0, 3, 0x00), ST_B(5, 3, 0x00), LD_BU(13, 3, 0x00),
                                 ST_B(5, 3, 0x104), LD_BU(14, 3, 0x104), ST_B(0, 3, 0x04), ST_B(5, 3, 0x04), LD_BU(15, 3, 0x04),
                                 LD_BU(16, 3, 0x08), LD_BU(17, 3, 0x108),
                                 ST_B(0, 3, 0x108), ST_W(9, 3, 0x11c),
                                 ST_B(5, 3, 0x100), LD_BU(18, 3, 0x100), ST_B(5, 3, 0x00), ST_B(0, 3, 0x00), LD_BU(19, 3, 0x00),
                                 ST_B(5, 3, 0x104), LD_BU(20, 3, 0x104), ST_B(5, 3, 0x04), ST_B(0, 3, 0x04), LD_BU(21, 3, 0x04),
                                 LD_BU(22, 3, 0x08), LD_BU(23, 3, 0x108),
                                 LD_BU(24, 3, 0x83), ST_W(9, 3, 0x1c), LD_BU(25, 3, 0x10c), ST_W(9, 3, 0x08), LD_BU(26, 3, 0x1c),
                                 LD_BU(27, 3, 0x08)],
                         [("r5", 0xff), ("r6", 0x07), ("r9", 0xffffffff)] +
                         [("r%d" % i, SENT) for i in (2, 4, 7, 8) + tuple(range(10, 28))], timeout=120)
row("R16 session", how, "exit0", "forty-five accesses through phases 00, 10, 11: survives")
row("R16 cnf line", has(T, "memconf write 0x7 (controller 0) ignored, not modelled (once) ]"), "yes",
    "the first memconf store, after phase 00's served stores and reads, is announced")
row("R16 def line", has(T, "unimplemented write to offset 0x1c (controller 1): 0xffffffff (once) ]"), "yes",
    "the first default access, after phase 10, is announced with controller 1 and the whole value")
row("R16 lines", nl, "2", "one announce per category; every other access silent")
row("R16 100 r2", hx(r, "r2"), hex(0x80), "phase 00: chipid via controller 1 after a 0x00 store")
row("R16 00 r4", hx(r, "r4"), hex(0x80), "phase 00: chipid after stores of 0x00 then 0xff")
row("R16 104 r7", hx(r, "r7"), hex(0x1), "phase 00: chiprev via controller 1 after a 0x00 store")
row("R16 04 r8", hx(r, "r8"), hex(0x1), "phase 00: chiprev after stores of 0x00 then 0xff")
row("R16 08 r10", hx(r, "r10"), hex(0x3), "phase 00: memconf after the served stores")
row("R16 108 r11", hx(r, "r11"), hex(0x3), "phase 00: memconf via controller 1")
row("R16 100b r12", hx(r, "r12"), hex(0x80), "phase 10: chipid via controller 1 after a 0xff store")
row("R16 00b r13", hx(r, "r13"), hex(0x80), "phase 10: chipid after stores of 0x00 then 0xff")
row("R16 104b r14", hx(r, "r14"), hex(0x1), "phase 10: chiprev via controller 1 after a 0xff store")
row("R16 04b r15", hx(r, "r15"), hex(0x1), "phase 10: chiprev after stores of 0x00 then 0xff")
row("R16 08b r16", hx(r, "r16"), hex(0x3), "phase 10: memconf after the 0x07 store and the served stores")
row("R16 108b r17", hx(r, "r17"), hex(0x3), "phase 10: memconf via controller 1")
row("R16 100c r18", hx(r, "r18"), hex(0x80), "phase 11: chipid via controller 1 after a 0xff store")
row("R16 00c r19", hx(r, "r19"), hex(0x80), "phase 11: chipid after stores of 0xff then 0x00")
row("R16 104c r20", hx(r, "r20"), hex(0x1), "phase 11: chiprev via controller 1 after a 0xff store")
row("R16 04c r21", hx(r, "r21"), hex(0x1), "phase 11: chiprev after stores of 0xff then 0x00")
row("R16 08c r22", hx(r, "r22"), hex(0x3), "phase 11: memconf after the served stores")
row("R16 108c r23", hx(r, "r23"), hex(0x3), "phase 11: memconf via controller 1")
row("R16 83 r24", hx(r, "r24"), hex(0), "phase 11: the default read at +0x83 (complement of +0x7c) reads 0")
row("R16 10c r25", hx(r, "r25"), hex(0), "phase 11: the controller-1 default read after a word default store reads 0")
row("R16 1c r26", hx(r, "r26"), hex(0), "phase 11: the default read after a word memconf store reads 0")
row("R16 08d r27", hx(r, "r27"), hex(0x3), "phase 11: memconf after the word store of 0xffffffff: still 3")
row("R16 pc", hx(r, "pc"), hex(CODE + 180), "forty-five instructions retired")
#  R17 (repair 5, NEW): a default read at +0xf3 FIRST (bits 2 and 3 clear, the complement of R4's +0x0c: family B's read-side
#  offset-bit gates), then phase 01 -- a controller-1 default read, two default word stores (controller 0 and 1), the served
#  stores (per field: 0x00 through controller 1, then 0x00 and 0xff through controller 0) with their readbacks, memconf through both controllers and a default read at
#  +0x7c, all silent; then a first memconf store of 0x07 (announces, with the default latch set), a silent controller-1 memconf store
#  of 0x00, a default read at +0x7d (silent) and the memconf readback.
r, T, how, nl = msession("R17", [LD_BU(2, 3, 0xf3), LD_BU(4, 3, 0x10c), ST_W(9, 3, 0x1c), ST_W(9, 3, 0x11c),
                                 ST_B(0, 3, 0x100), LD_BU(7, 3, 0x100), ST_B(0, 3, 0x00), ST_B(5, 3, 0x00), LD_BU(8, 3, 0x00),
                                 ST_B(0, 3, 0x104), LD_BU(10, 3, 0x104), ST_B(0, 3, 0x04), ST_B(5, 3, 0x04), LD_BU(11, 3, 0x04),
                                 LD_BU(12, 3, 0x08), LD_BU(13, 3, 0x108), LD_BU(14, 3, 0x7c),
                                 ST_B(6, 3, 0x08), ST_B(0, 3, 0x108), LD_BU(15, 3, 0x7d), LD_BU(16, 3, 0x08)],
                         [("r5", 0xff), ("r6", 0x07), ("r9", 0xffffffff)] +
                         [("r%d" % i, SENT) for i in (2, 4, 7, 8) + tuple(range(10, 17))])
row("R17 session", how, "exit0", "a default read at +0xf3 first, then phase 01: survives")
row("R17 def line", has(T, "unimplemented read from offset 0xf3 (controller 0) (once) ]"), "yes",
    "the first default read, bits 2 and 3 clear, is announced")
row("R17 cnf line", has(T, "memconf write 0x7 (controller 0) ignored, not modelled (once) ]"), "yes",
    "the first memconf store, made with the default latch set, is announced")
row("R17 lines", nl, "2", "one announce per category; every other access silent")
row("R17 f3 r2", hx(r, "r2"), hex(0), "the default read at +0xf3 reads 0")
row("R17 10c r4", hx(r, "r4"), hex(0), "the controller-1 default read reads 0")
row("R17 100 r7", hx(r, "r7"), hex(0x80), "phase 01: chipid via controller 1 after a 0x00 store")
row("R17 00 r8", hx(r, "r8"), hex(0x80), "phase 01: chipid after stores of 0x00 then 0xff")
row("R17 104 r10", hx(r, "r10"), hex(0x1), "phase 01: chiprev via controller 1 after a 0x00 store")
row("R17 04 r11", hx(r, "r11"), hex(0x1), "phase 01: chiprev after stores of 0x00 then 0xff")
row("R17 08 r12", hx(r, "r12"), hex(0x3), "phase 01: memconf after the served stores")
row("R17 108 r13", hx(r, "r13"), hex(0x3), "phase 01: memconf via controller 1")
row("R17 7c r14", hx(r, "r14"), hex(0), "phase 01: the default read at +0x7c reads 0 (and is silent)")
row("R17 7d r15", hx(r, "r15"), hex(0), "phase 11: the default read at +0x7d after the memconf stores reads 0")
row("R17 08b r16", hx(r, "r16"), hex(0x3), "phase 11: memconf after the 0x07 and 0x00 stores: still 3")
row("R17 pc", hx(r, "pc"), hex(CODE + 84), "twenty-one instructions retired")
#  R18 (repair 6, NEW; regress_20261105/REG_MYTHOS_local.md section 2(d)): three default stores to +0x18 (0x01, 0x01, 0x00) and the
#  load back, then three memconf stores (0x01, 0x01, 0x00) and the memconf load -- one announce per category, both naming 0x1.
r, T, how, nl = msession("R18", [ST_B(5, 3, 0x18), ST_B(5, 3, 0x18), ST_B(0, 3, 0x18), LD_BU(2, 3, 0x18), ST_B(5, 3, 0x08),
                                 ST_B(5, 3, 0x08), ST_B(0, 3, 0x08), LD_BU(4, 3, 0x08)],
                         [("r2", SENT), ("r4", SENT), ("r5", 0x01)])
row("R18 session", how, "exit0", "default and memconf stores of 0x01, 0x01, 0x00: survives")
row("R18 18 r2", hx(r, "r2"), hex(0), "the default load after the three stores reads 0")
row("R18 08 r4", hx(r, "r4"), hex(0x3), "memconf after its 0x01, 0x01, 0x00 stores: still 3")
row("R18 pc", hx(r, "pc"), hex(CODE + 32), "eight instructions retired")
row("R18 lines", nl, "2", "one announce per category; the later stores are silent")
row("R18 def line", has(T, "unimplemented write to offset 0x18 (controller 0): 0x1 (once) ]"), "yes",
    "the first default store, 0x01, is announced with its value")
row("R18 cnf line", has(T, "memconf write 0x1 (controller 0) ignored, not modelled (once) ]"), "yes",
    "the first memconf store, 0x01, is announced")
n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("MVME187_MEMC_RESULT=%d/%d" % (n_ok, len(rows)))
print("MVME187_MEMC_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("MVME187_MEMC_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("MVME187_MEMC_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("MVME187_MEMC_ASAN=%d" % asan_hits)
print("MVME187_MEMC_PROBE_DONE")
