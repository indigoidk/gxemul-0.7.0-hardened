Begin your answer with the token MYTHOSREGMEMC on its own line, then `model: <your model name>`, then your verdict line.  You may
open files under C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/ READ-ONLY to check a claim; write nothing, build nothing, run no git command
that writes.  The tree under review is GXEMUL-SEC/src/ and GXEMUL-SEC/regress/; ignore any other src/ you find (the project root
holds pristine 2021 upstream copies).  The probe and the gate block below are the STAGED copies the commit will carry; the working
tree's regress/gate_arm.sh also holds other rounds' uncommitted blocks and lacks the comment patch, so read the gate block HERE.

# REGRESS REVIEW (the Fable-only stage) -- round #581 `mvme187memcoob`: the detector as it will ship

**PROJECT FRAMING -- this is a defensive software-robustness project.**  GXemul is a computer-architecture emulator: a developer tool
that runs legacy operating systems in a software sandbox for research and preservation.  This fork is a HARDENING effort -- ordinary
software-correctness engineering on the emulator's own C code, each fix shipped with a regression test that keeps it fixed.  There is
no attack, no target system and no affected third party; the guest is a few instruction words under test INSIDE the emulator, and the
host is the emulator process on the developer's own machine.  This round removes an OUT-OF-BOUNDS READ in the C source and two
places where the emulator ended its own process on ordinary guest input.  **Vocabulary**: a *test variant* is a deliberately broken
copy of the fix used to measure whether the regression test notices it; *detected* = a row went red; *green* (a variant) = every
row passed; *NOCHANGE* = the variant changed no field byte and no latch truth value on this probe; a *null medium* is a run with no working
emulator behind the probe (a non-emulator binary, a missing one).

**Your role: the flagship's REGRESS review**, the fable5 slot's step (owner, 2026-11-05: Mythos is that slot, run locally, as for
#575).  By standing owner directive only the flagship seat reviews the `regress` stage.  THE ROUND: `src/devices/dev_mvme187.c`,
DEVICE_ACCESS(mvme187_memc) -- the MVME187 memory controller's register window (0x200 bytes at 0xfff43000; controller 1 at
+0x100..+0x1ff folds onto the same image) -- ended the emulator (fatal() + exit(1)) on a memconf store and on any offset its switch
did not name, and indexed the 124-byte `struct memcreg` with the folded offset (0..0xff) before the switch, an out-of-bounds read in
the C source for 0x7c..0xff.  The rung-3 witness (block H2) measured the two exits on the committed build and NO sanitizer report on
the read: it was latent behind the exits.  The fix (block G, the whole function) reads each served field in its own arm, keeps no
store, announces each category once per device through two latches placed directly after `memcreg`, and has no indexed read left.
The detector is regress/mvme187_memc_probe.py (206 rows; block A, whose header is the CONTRACT) in gate 14 (block B).  It grew
through five numbered test-variant tables on the 56-, 74-, 118-, 148- and 206-row probes (det_20261104/table1/, table2/,
r3_20261105/table3/, r4_20261105/table4/, r5_20261105/table5/) and the review passes on the diff (p2, the repair's own pass p2r, then
p3, p4 and p5); pass 5 swept table 5's survivor families (665 green variants) and the round's ruler ruled ZERO floor families and
FIVE coverage-debt families (block F1: CLOSE-AFTER-RECORDS); the records corrections it ordered were then read FOUR times by GPT-6
Astra, finding 10, then 3, then 1, then 0 items to fix (blocks F2, F3).  NO SEAT HAS REVIEWED THE DETECTOR AS IT WILL LAND as one
object -- the probe after rec9, the gate block with its comment patch, the filing -- and gate 14 last ran the memc block IN SITU on
the 74-row probe (wiring_20261105/gate14_mvme187_memc.log: MVME187_MEMC_RESULT=74/74), so this review is also the first reading of
the 206-row block's pins (block H1 replays them over table 5's banked logs; the in-situ run is owed at landing, RECORDS6_NOTE.md
section 5 item 3).  This review is of the WHOLE detector as it will land and of the records describing it.

Mark each claim CHECKED-IN-PACKET (block + line), CHECKED-IN-TREE (file:line you opened), REASONED, or UNSETTLED (name the one
measurement that settles it -- the main loop runs it).  A finding is fixed in this round only if it is a floor breach (L2), an
undischarged obligation (L3) or a wrong record (L4); everything else is FILED with its warrant.  Rows are owed per enumerated wrong
version of the fix inside the DEPENDS-ON bound (the predicates dominating the edited lines, walked to the enclosing function; operand
swaps only from fields the guarded body reads; joint cells only where the body's own tests distinguish them, and the FLOOR is the
guard's dominating predicates crossed with the device-state lvalues the repair path reads that are jointly reachable), never per
possible state; a filter may reject or repair a row, never demand one outside the bound.  Count the arguments, not the seats: an
agreement that only restates a packet's premise is no evidence.

**PREMISES PUT AS QUESTIONS -- please do not simply ratify; on this project seven of nine seats once confirmed a premise a brief
stated wrongly.  Check each against the tree:**
* P1. I believe the fix's floor is exactly the ruler's: the memconf path {write, !warned_memconf} x {memc_memconf, warned_memconf};
  the default path {default arm, !warned_default} x {warned_default}; each served arm x its own field -- and that `controller`, len,
  idata and the offset bits are not floor predicates because the fold rejoins before the switch and no body tests an idata bit.  Is
  any predicate or body-read lvalue of the shipped function missing from that list?
* P2. I believe no table-5 green variant lies inside that floor.  Is there one?
* P3. I believe B3 (the indexed read reinstated) is caught at run time only by R3 7c r4, R8 7c r4, R8 80 r8 and R11 180 r4, and only
  while the latches sit directly after memcreg; and that the gate's source check (`memcreg\)[[:space:]]*\[|\[relative_addr\]`) is
  the layout-free guard.  Does the source check see EVERY spelling of the old read?  (e.g. pointer arithmetic,
  `*((uint8_t *)&d->memcreg + relative_addr)`, carries neither pattern.)  If not, is that a floor matter or a contract disclosure?
* P4. I believe the probe's claim of a clause-(c) null medium is discharged by /bin/true, an absent binary and /bin/false, each
  CONTROL=FAIL on every table.  For a DEVICE round the carrier also names a build without the device.  Is the binary form enough here,
  and should the record say `(c): measured at <artifact>` or `(c): by construction via <pin>`?
* P5. I believe every one of the gate block's pins can fail (block H1 replays it over the banked logs).  Can any not?

**Write your answer in this order** (it is banked as regress/artifacts/mvme187memcoob/regress_20261105/REG_MYTHOS_local.md):
1. Evidence basis (which blocks and which files you opened).
2. The vacuity floor, clause by clause, each with the artifact that discharges it or the breach: (a) the pre-fix build fails;
   (b) a verbatim reinstatement of the removed defect at EVERY fixed site fails (B1 the memconf exit, B2 the default exit, B3 the
   indexed read -- P3); (c) a null medium fails (P4); (d) null-repair over the DEPENDS-ON floor (P1, P2); (e) the contract in the
   probe header: true as written, and complete for what table 5 measured -- the five disclosed families, NB3, NB4, the cross-call
   caveat; (f) anchors -- which rows pin WHICH register or byte a load reached rather than only that something changed (ask: if every
   offset shifted one word, which row reds?  if the fold mask or the window shrank, which row reds?).
3. Gate 14's memc block (block B, with the comment patch): does every pin red under (i) a dead probe, (ii) a probe that silently
   loses rows, (iii) a probe that adds a row, (iv) a probe whose sentinel prints but whose RESULT line is missing?  Name any pin that
   cannot fail.  Does block H1 show what it claims?  Is the comment (the patched text included) true?
4. The tables (blocks C1, C2; PRETABLE_5.out by path): is any row VACUOUS by construction (its observable cannot vary under the
   variant it is meant to catch)?
   Is any detection credited to a different row than the record claims?  Are the 665 green variants correctly disclosed -- each in
   one of the five families, none inside the floor?
5. Records: wrong numbers or claims in the probe header (block A), the gate comment (block B), VERDICT.md and its errata (block C2),
   the filing (block E) and the dispositions (F2, F3).  The ruling (F1) is quoted as written: its disclosure (c) sentence "R9's 0x00
   first store exposes only `=`" was found false by the fourth reading (SCORES.txt:1334, K_MB_chipid_and_C 205/206) and deleted from
   the probe; say whether any other ruling sentence the probe or the filing still carries is false.
6. The main loop's dispositions: which accepted disposition is wrong?  Counted: pass 5 -- codex 0 floor cells and 10 false records,
   all 10 upheld by the ruling; Gemini twice (CLOSE; REPAIR on one wording item, folded into the ruling); the records chain rec6 (7
   accepted, 10 to fix), rec7 (7, 3), rec8 (2, 1), rec9 (2, 0), each fixed or accepted.  Is the zero-floor disposition right?
7. Which of your own findings is weakest, and what would overturn it.
Final line: `MYTHOSREGMEMC: <n> CHECKS <b> FLOOR-BREACHES <r> RECORD-FINDINGS VERDICT:<REGRESS-CLEAN|REGRESS-WITH-FINDINGS|REGRESS-BREACH>`

Files you may open (READ-ONLY) if a block is not enough: regress/artifacts/mvme187memcoob/r5_20261105/PRETABLE_5.out (the predictions; survivor summary at
:9460-9697), .../r5_20261105/table5/SCORES.txt (all 3,580 lines), .../r5_20261105/memc_variants_5.py (the walker), .../r5_20261105/
T5_PREP.md and .../r6_20261105/ERRATA_T5_PREP_20261105.md, .../r6_20261105/ERRATA_PRETABLE_5_20261105.md, .../r6_20261105/
RECORDS6_NOTE.md (every records correction with the text it replaced), .../p4_20261105/CONS_MYTHOS_local.md (the consolidated
ruling repair 5 implemented), .../p5_20261105/codex_codex_memc_p5.txt, .../LATE_REPLICATIONS_20261105.md.

---

### A. the probe as it will ship (regress/mvme187_memc_probe.py, the staged copy: the working copy with its docstring's `#NNN` set to #581; landing_20261105/PROBE_IDENTITY_memc.md proves the syntax tree minus the docstring unchanged and, strings normalised, equal to table 5's frozen instrument)

```
#!/usr/bin/env python3
"""mvme187memcoob -- DETECTOR (built on its rung-3 witness) for the MVME187 memory controller, dev_mvme187.c.

DEFECT (filed 2026-10-02).  DEVICE_ACCESS(mvme187_memc) ended the emulator (fatal() + exit(1)) on a store to memconf (+0x08) and on any
offset its switch did not name, and indexed the 124-byte register struct with the folded offset (0..0xff) before the switch -- an
out-of-bounds read in the C source for 0x7c..0xff whose value the exiting arms never used.

THE FIX (#581).  Each served offset reads its own field (chipid +0x00, chiprev +0x04, memconf +0x08); controller 1 (+0x100..0x1ff)
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
n_ok = sum(1 for _, ok in rows if ok)
red = [n for n, ok in rows if not ok]
print("elapsed %.1fs" % (time.time() - t0))
print("MVME187_MEMC_RESULT=%d/%d" % (n_ok, len(rows)))
print("MVME187_MEMC_CONTROL=%s" % ("OK" if all(ok for _, ok in controls) else "FAIL"))
print("MVME187_MEMC_SYMPTOM=%s" % ("PRESENT" if symptom_hits else "ABSENT"))
print("MVME187_MEMC_RED=%s" % (",".join(n.replace(" ", "_") for n in red) if red else "none"))
print("MVME187_MEMC_ASAN=%d" % asan_hits)
print("MVME187_MEMC_PROBE_DONE")
```

### B. gate 14's memc block (the staged regress/gate_arm.sh: HEAD's file plus exactly this block, after the #570 block; r6_20261105/gate_memc_comment.patch applied to its comment, the header's #NNN set to #581)

```
#  ------------------------------------------------------------ mvme187memcoob (#581)
#  dev_mvme187.c's memory controller ended the emulator (fatal() + exit(1)) on a memconf store and on any unnamed offset, and indexed
#  its 124-byte register struct with the folded offset before the switch.  Now each served offset reads its own field, controller 1
#  folds onto the same image, a memconf store and any other offset's access are not kept, and each category is announced once per
#  device.  The rung-3 witness (regress/artifacts/mvme187memcoob/witness_20261104/) is NOT run here; this is its detector: 206 rows,
#  the witness's 21 plus fifteen multi-access sessions -- R3 to R17: several accesses in one emulator lifetime, one
#  register per load (the latch rows, and R8's twelve bytes past memcreg).  A source check beside it: no `memcreg)[' and no
#  `[relative_addr]' may appear in dev_mvme187.c, the layout-free guard against the old indexed read (R8 covers it at run time
#  only while the latches sit just after memcreg).  Needs only the binary: mvme187 -M 64 with a 4-byte dummy image at 0x10000.
#  Test-variant tables: regress/artifacts/mvme187memcoob/det_20261104/table1/ (the then 56-row probe), table2/ (the 74-row probe),
#  r3_20261105/table3/ (the 118-row probe), r4_20261105/table4/ (the 148-row probe) and r5_20261105/table5/ (this probe, the record:
#  3,575 variants, 665 green, every one in a debt family the probe's CONTRACT discloses and r6_20261105/FILING_memccoverdebt.md
#  files with sketched closing rows, unwalked -- zero floor cells survive); sanitizer legs: .../det_20261104/asan/ (offline evidence; MVME187_MEMC_ASAN is
#  informational and not checked here).
#  Like #568's and #570's blocks above, it runs only if none of this gate's earlier skip points fired.
MEMCLOG=$LOGDIR/mvme187_memc.log
python3 -u mvme187_memc_probe.py "$PMAX" gate > "$MEMCLOG" 2>&1 || true
if ! grep -q "MVME187_MEMC_PROBE_DONE" "$MEMCLOG"; then
    check "mvme187 memc probe completed" "no" "yes"
else
    check "mvme187 memc probe completed" "yes" "yes"
    check "mvme187 memc sentinel once" "$(grep -c '^MVME187_MEMC_PROBE_DONE$' "$MEMCLOG")" "1"
    mcres=$(sed -n 's/^MVME187_MEMC_RESULT=//p' "$MEMCLOG")
    check "mvme187_memc rows run"     "${mcres#*/}" 206
    check "mvme187_memc rows correct" "${mcres%/*}" "206"
    check "mvme187 memc controls" "$(grep -c '^MVME187_MEMC_CONTROL=OK$' "$MEMCLOG")" "1"
    check "mvme187 memc symptom absent" "$(grep -c '^MVME187_MEMC_SYMPTOM=ABSENT$' "$MEMCLOG")" "1"
    for v in "neg apparatus" "ctl chipid sess" "ctl chipid r2" "ctl chipid pc" "ctl chiprev sess" "ctl chiprev r2" "ctl chiprev pc" "ctl memconf sess" "ctl memconf r2" "ctl memconf pc" "ctl ctl1id sess" "ctl ctl1id r2" "ctl ctl1id pc" "rd 0x0c session" "rd 0x0c prompt" "rd 0x7c session" "rd 0x7c prompt" "rd 0xff session" "rd 0xff prompt" "wr cnf session" "wr cnf prompt" "R3 session" "R3 cnf r2" "R3 7c r4" "R3 108 r9" "R3 cnf0 r11" "R3 00 r12" "R3 04 r13" "R3 pc" "R3 lines" "R3 cnf line" "R3 7c line" "R3 no 0x5" "R3 no 0x0" "R4 session" "R4 00 r7" "R4 04 r8" "R4 0c" "R4 7c" "R4 ff" "R4 10c" "R4 pc" "R4 lines" "R4 line text" "R5 session" "R5 r2" "R5 00 r7" "R5 04 r8" "R5 08 r9" "R5 08b r11" "R5 pc" "R5 lines" "R5 line text" "R5 cnf line" "R6 session" "R6 00" "R6 04" "R6 08" "R6 100" "R6 104" "R6 108" "R6 pc" "R6 lines" "R7 session" "R7 r2" "R7 108 r4" "R7 10c r6" "R7 108b r7" "R7 pc" "R7 lines" "R7 line text" "R7 cnf line" "R8 session" "R8 7c r4" "R8 7d r5" "R8 7e r6" "R8 7f r7" "R8 80 r8" "R8 81 r9" "R8 82 r10" "R8 83 r11" "R8 84 r12" "R8 85 r13" "R8 86 r14" "R8 87 r15" "R8 pc" "R8 lines" "R9 session" "R9 108 r2" "R9 08 r4" "R9 00 r6" "R9 04 r7" "R9 10c r8" "R9 08b r9" "R9 lines" "R9 no wide" "R9 cnf line" "R9 def line" "R9 pc" "R10 session" "R10 118 r6" "R10 18 r7" "R10 08 r8" "R10 00 r9" "R10 04 r10" "R10 lines" "R10 line text" "R10 pc" "R11 session" "R11 180 r4" "R11 01 r5" "R11 0a r6" "R11 101 r7" "R11 102 r8" "R11 120 r9" "R11 140 r10" "R11 20 r11" "R11 40 r12" "R11 line text" "R11 lines" "R11 pc" "R12 session" "R12 cnf line" "R12 00 r2" "R12 04 r4" "R12 m08 r13" "R12 100 r10" "R12 104 r11" "R12 w00 r6" "R12 h08 r7" "R12 08 r8" "R12 0c r12" "R12 0cb r14" "R12 08b r15" "R12 0c line" "R12 lines" "R12 pc" "R13 session" "R13 line text" "R13 00 r2" "R13 04 r4" "R13 08 r6" "R13 08b r8" "R13 10c r9" "R13 cnf line" "R13 lines" "R13 pc" "R14 session" "R14 line text" "R14 00 r2" "R14 04 r4" "R14 08 r5" "R14 0c r6" "R14 lines" "R14 pc" "R15 session" "R15 00 r2" "R15 04 r4" "R15 08 r7" "R15 cnf line" "R15 def line" "R15 lines" "R15 pc" "R16 session" "R16 cnf line" "R16 def line" "R16 lines" "R16 100 r2" "R16 00 r4" "R16 104 r7" "R16 04 r8" "R16 08 r10" "R16 108 r11" "R16 100b r12" "R16 00b r13" "R16 104b r14" "R16 04b r15" "R16 08b r16" "R16 108b r17" "R16 100c r18" "R16 00c r19" "R16 104c r20" "R16 04c r21" "R16 08c r22" "R16 108c r23" "R16 83 r24" "R16 10c r25" "R16 1c r26" "R16 08d r27" "R16 pc" "R17 session" "R17 def line" "R17 cnf line" "R17 lines" "R17 f3 r2" "R17 10c r4" "R17 100 r7" "R17 00 r8" "R17 104 r10" "R17 04 r11" "R17 08 r12" "R17 108 r13" "R17 7c r14" "R17 7d r15" "R17 08b r16" "R17 pc"; do
        check "mvme187 memc row: $v" "$(count "$MEMCLOG" "^$v  .*ok$")" "1"
    done
    check "mvme187 memc rows emitted" "$(( $(count "$MEMCLOG" " ok$") + $(count "$MEMCLOG" " FAIL$") ))" "206"
    check "mvme187 memc rows green"   "$(count "$MEMCLOG" " ok$")"   "206"
    check "mvme187 memc rows red"     "$(count "$MEMCLOG" " FAIL$")" "0"
fi
check "mvme187 memc no indexed read" "$(grep -cE 'memcreg\)[[:space:]]*\[|\[relative_addr\]' ../src/devices/dev_mvme187.c)" "0"
```

### C1. the leg scores of every table (base, HEAD, the null media, and the three verbatim reinstatements)

```
(table 5, r5_20261105/table5/SCORES.txt, the record; RED lists replaced by their counts)
base [206 rows] 206/206 CONTROL=OK SYMPTOM=ABSENT ASAN=0 MVME187_MEMC_PROBE_DONE RED=none PRED=match
HEAD [206 rows] 29/206 CONTROL=OK SYMPTOM=PRESENT ASAN=0 MVME187_MEMC_PROBE_DONE RED=<177 rows> PRED=match
null_true [206 rows] 27/206 CONTROL=FAIL SYMPTOM=ABSENT ASAN=0 MVME187_MEMC_PROBE_DONE RED=<179 rows> PRED=match
null_absent [206 rows] 4/206 CONTROL=FAIL SYMPTOM=ABSENT ASAN=0 MVME187_MEMC_PROBE_DONE RED=<202 rows> PRED=match
null_false [206 rows] 5/206 CONTROL=FAIL SYMPTOM=ABSENT ASAN=0 MVME187_MEMC_PROBE_DONE RED=<201 rows> PRED=match
B1_cnf_exit [206 rows] 79/206 CONTROL=OK SYMPTOM=PRESENT ASAN=0 MVME187_MEMC_PROBE_DONE RED=<127 rows> PRED=match
B2_def_exit [206 rows] 42/206 CONTROL=OK SYMPTOM=PRESENT ASAN=0 MVME187_MEMC_PROBE_DONE RED=<164 rows> PRED=match
B3_idx_read [206 rows] 202/206 CONTROL=OK SYMPTOM=ABSENT ASAN=0 MVME187_MEMC_PROBE_DONE RED=<4 rows> PRED=atleast-ok

variants run: 3575
PRED=match:      3523
PRED=atleast-ok: 56
PRED=MISS:       1
PRED=none:       0
BUILD failures:  0
text not found:  0
variants scoring 206/206 (survivors, base excluded): 665
MISS lines:
D7_fold

(tables 1-4 and the 52-row first detector: det_20261104/table1/, table2/, SCORES.txt, r3_20261105/table3/ and r4_20261105/table4/ -- the probe header's clause (e) quotes their totals)
```

### C2. table 5's verdict (r5_20261105/table5/VERDICT.md, the verdict of record, unedited) and its errata (r6_20261105/ERRATA_table5_VERDICT_20261105.md)

# mvme187memcoob -- test-variant TABLE 5 (repair 5, 206 rows; the consolidated ruling's L-walk), 2026-11-05 ~10:5x-12:2xZ

Driver `../table5_memc.run.sh` (frozen copy of table5_memc.sh, written by the local Mythos 5.1 preparer), WSL scratch clone /tmp/gxmemc6
under a clone-local .MUTANT; restored to GXEMUL-SEC and rebuilt fresh, sentinel cleared (../table5_run.log).  Instrument
`probe206_frozen.py`, cmp-identical to the in-tree probe; `../PRETABLE_5.out` (02:32:32 local) and its machine form PRED_MAP.txt predate
every table output; `check4.out` re-verified the preparer's device model against all 60 table-4 measurements before the variants ran.
Scores: SCORES.txt; tally: TALLY.txt.

* base 206/206 CONTROL=OK SYMPTOM=ABSENT; HEAD 29/206 SYMPTOM=PRESENT; null media /bin/true 27/206, an absent binary 4/206, /bin/false
  5/206 -- each CONTROL=FAIL; every leg as predicted.
* 3,575 variants (112 from table 4 + 3,463 L-walk representatives): PRED=match 3,523, PRED=atleast-ok 56, PRED=MISS 1, build failures 0,
  text-not-found 0.
* The one MISS, `D7_fold`, is DETECTED (175/206, 31 rows red); its carried-forward "at least" set from table 4 included `R7_lines`, which
  stays green under D7 now that repair 5 extended the R7 session (IMPL_NOTE.md: "R7 EXTENDED ... lines stays 2").  A carry-forward
  error in the prediction, not an escape.
* 665 variants score 206/206, and EVERY ONE was predicted green: the representatives of the 517 predicted SURVIVOR groups inside the
  ruling's own denominator (UNFIRED 106, of which 58 in-bound; UNOBSERVED 411) and of the 148 NOCHANGE statements.  So the measurement
  CONFIRMS T5_PREP's finding: the 206 rows do not close the L-walk as the consolidated ruling defined it.  Whether those cells are floor
  cells owed rows, or clause-(e) coverage debt under the 09-04 floor bound, is the question pass 5 and the next ruling must answer.
* Carried into pass 5 BY NAME (from LATE_REPLICATIONS_20261105.md): NB3 -- a `|=`/`^=` keep into chipid/chiprev in the memconf-latch
  arm, controller-gated (predicted and measured a survivor); NB4 -- an `&=` keep under !controller, which PRETABLE_5 classes NOCHANGE,
  so the tally does not report it as a survivor although it passes every row.


# ERRATA for r5_20261105/table5/VERDICT.md -- records 6, 2026-11-05 (adj_p5_20261105/ADJ_MYTHOS_local.md R4, R5, R10)

table5/VERDICT.md is the table's verdict of record and is not rewritten; each item quotes the sentence it corrects.  Line numbers
are VERDICT.md's.

1. **:11 (R5).**  Quoted: "3,575 variants (112 from table 4 + 3,463 L-walk representatives): PRED=match 3,523, PRED=atleast-ok 56,
   PRED=MISS 1, build failures 0, text-not-found 0."
   Correction: 3,523 + 56 + 1 = 3,580, which is 3,575 variants plus the five control legs -- SCORES.txt:1-5 (base, HEAD,
   null_true, null_absent, null_false) each carry PRED=match and TALLY.txt counts them.  For the VARIANTS: 3,518 PRED=match, 56
   PRED=atleast-ok, 1 PRED=MISS (D7_fold, detected 175/206).  The legs: 5 of 5 as predicted (:9-10 stands).

2. **:16-17 (R4).**  Quoted: "the representatives of the 517 predicted SURVIVOR groups inside the ruling's own denominator (UNFIRED
   106, of which 58 in-bound; UNOBSERVED 411)".
   Correction: 452 of the 517 representatives are inside CONS section 3's alphabet (62 UNFIRED and 390 UNOBSERVED); 65 are the
   walk's implemented superset -- 44 UNFIRED representatives at CI/CR under idata bits 8..31 (T5_PREP.md:68-69; 48 summary lines,
   PRETABLE_5.out:9461-9508) and 21 UNOBSERVED representatives at ME, the position the walk added (12 summary lines, :9632-9643;
   T5_PREP.md:31-32).  The quoted "of which 58 in-bound" is the count of ALL UNFIRED summary lines (:9461-9518), 48 of them the
   supplementary CI/CR lines; the in-bound UNFIRED representatives are 62, in 10 summary lines (:9509-9518).  The 665 = 517 + 148
   NOCHANGE stands.  (Second reading, rec6 R4: this item first said "457 (58 + 399) / 60", counting summary lines as groups.)

3. **:18-19 (answered).**  Quoted: "Whether those cells are floor cells owed rows, or clause-(e) coverage debt under the 09-04 floor
   bound, is the question pass 5 and the next ruling must answer."
   Answered by adj_p5_20261105/ADJ_MYTHOS_local.md: ZERO floor families, FIVE debt families -- every green family lies outside the
   repair paths' own guard-by-state product (the memconf path's {write, !M} x {memconf, M}; the default path's {default arm, !D}
   x {D}; each served arm x its own field).  The round closes on pass 5's denominator; the debt is filed with its remedies
   (r6_20261105/FILING_memccoverdebt.md) and the probe's header now carries the contract and the disclosures.

4. **:21-22 (R10).**  Quoted: "NB4 -- an `&=` keep under !controller, which PRETABLE_5 classes NOCHANGE, so the tally does not
   report it as a survivor although it passes every row."
   Correction: "NB4 -- an `&=` keep under !controller at the first memconf store: its representatives (K_MB_chiprev_and_D and
   K_MB_memconf_and_D, with nC and W.nC among their listed equivalents, PRETABLE_5.out:8199 and :8211) are among the 665 green
   variants, classed NOCHANGE and so absent from the UNFIRED/UNOBSERVED survivor summary."  The tally does report them -- inside
   its 665 (TALLY.txt:8) -- under a class name the summary at :9460 does not list.  Probe-relative: every controller-0 first
   memconf store the rows make (0x07, 0xff, 0xffffffff) leaves chiprev 0x01 and memconf 0x03 unchanged under `&=`; a 0x00 first
   store would zero both.

### E. the filing (r6_20261105/FILING_memccoverdebt.md; the main loop files it as the `memccoverdebt` row at landing)

# FILING for OUTSTANDING_BUGS.md -- `memccoverdebt` (the main loop files it at landing)

Written 2026-11-05 (records 6, r6_20261105) from adj_p5_20261105/ADJ_MYTHOS_local.md (CLOSE-AFTER-RECORDS: zero floor families,
five debt families) and PRETABLE_5.out's survivor summary (:9460-9697), checked group by group against the probe's instruction
lists.  Row sketches use the probe's own encoders (LD_BU/ST_B/ST_W(reg, 3, offset)); msession() already reads r2 and r4..r31; names
are at most 16 characters and unique against the 206.  None of these rows is owed in-round: every family lies outside the fix's
floor (the repair path's own guard crossed with its own state), and the standing rule says a filter may not demand coverage.

* **`memccoverdebt` (LOW, coverage debt on a closed round) -- new.**  `#NNN` mvme187memcoob's 206-row detector
  (`regress/mvme187_memc_probe.py`) leaves 665 of table 5's 3,575 test variants green (`regress/artifacts/mvme187memcoob/
  r5_20261105/table5/`, every one predicted green by PRETABLE_5.out before the table ran).  Pass 5 ruled all of them clause-(e)
  coverage debt, none a floor breach.  The probe's CONTRACT discloses them by family; this row carries the untested contexts and
  the rows that would close each.  Six items (the ruling's five families and
  the cross-call caveat the ruling attached to its VACUOUS count):
  1. **UNFIRED in-bound (62 representatives in 10 (position, gate) summary lines, PRETABLE_5.out:9509-9518; TO widenings ride here
     too).**  Untested
     contexts: a controller-0 memconf store in latch state (M, D) = (1, 0) -- R16's phase-10 memconf store is `ST_B(0,3,0x108)`,
     controller 1, and R3's, R7's and R9's second controller-0 stores all follow a default access -- and a controller-1 default
     store in state (1, 1): R16's phase-11 default accesses are LD 0x83, ST_W 0x1c (controller 0), LD 0x10c, LD 0x1c.  Each context
     needs a COMPLEMENTARY PAIR of values, not one store: a lone 0x00 is the identity of the `|=`/`^=` keeps behind the gate
     (K_MT_chipid_or under W.nC.M.nD, PRETABLE_5.out:9510) and a lone 0xff the identity of the `&=` keeps (K_DT_chipid_and under
     W.C.M.D, :9509); triggering a gate does not detect every statement behind it.  Rows (all in R16): after `LD_BU(17,3,0x108)`
     insert `ST_B(6,3,0x08)` (controller 0, 0x07, silent: M is set), `ST_B(0,3,0x08)` (0x00, silent) and `LD_BU(28,3,0x08)` ->
     `R16 08e r28` want 0x3 -- a changed chipid or chiprev is read by the existing phase-11 readbacks `LD_BU(18..21)` (the served
     stores between are not kept), a changed memconf by r28; after `LD_BU(25,3,0x10c)` insert `ST_B(5,3,0x118)` (controller 1,
     0xff, silent) and `ST_B(0,3,0x118)` (0x00, silent) -- the existing `LD_BU(26,3,0x1c)` then observes D, the existing
     `ST_W(9,3,0x08)` observes M, `LD_BU(27,3,0x08)` memconf, and item 2(i)'s tail readbacks (r29, r30) chipid and chiprev.
     `R16 lines` stays "2"; five instructions, so `R16 pc` moves by +20 (0x100b4 -> 0x100c8) for this item alone and by +28
     (-> 0x100d0) with item 2(i)'s two tail readbacks (probe:264-266 places one word per instruction); seed r28 with SENT.  The same
     pairs close family 5 (TO_M `!M || (!C && !D)` re-announces on the phase-10 pair, TO_D `!D || (W && C && M)` on the phase-11
     pair) and the `M = idata`-under-W.nC group of item 2(vi).  SUPPLEMENTARY ALPHABET (walked, UNFIRED, not in the ruling's
     alphabet): 44 representatives for 1,056 cells in 48 summary lines (:9461-9508) at the chipid and chiprev arms under idata bits
     8..31 -- no row makes a WORD store to +0x00/+0x04.  Rows: word stores of 0xffffffff AND of 0xffffff00 (bits 8..31 set, low
     byte clear: `&= 0xff` preserves every field, so 0xffffffff alone cannot close the `&=` keeps, and 0xffffff00 alone is the
     `|=`/`^=` identity), each followed by a byte readback, in TWO latch states: in R12 after its byte pairs ((M, D) = (1, 0)) --
     `ST_W(5,3,0x00)`, `ST_W(16,3,0x00)`, `LD_BU(17,3,0x00)` want 0x80, `ST_W(5,3,0x04)`, `ST_W(16,3,0x04)`, `LD_BU(18,3,0x04)`
     want 0x1, with r16 = 0xffffff00 (R12's r5 is 0xffffffff and its r9 is 0xff, probe:509: the source must be r5, not r9), observed
     through R12's final default read (D) and its controller-1 memconf store (M); and in R17's phase 01 after its byte pairs ((0, 1))
     -- the same six with r9 (0xffffffff in R17) and r20 = 0xffffff00, readbacks r21, r22, observed through R17's first memconf
     store (M) and its +0x7c default read (D).  All silent on the fix; pc rows move accordingly.  NOT closed by this sketch: the
     `^= 1` latch toggles behind these gates (L_CI/L_CR_[MD]_xor1, in the :9483 line) run twice per pair and cancel before either
     latch is observed.  Sketch, checked by hand against the instruction lists; the re-walk at the end is the proof.
  2. **UNOBSERVED (411 representatives in 179 summary lines): state changed, nothing read it or the change cancelled.**  (i) Keeps
     into chipid/chiprev from arms that do not read them, gated on a latch or on controller: the sessions whose first memconf store
     is made with D set (R5, R7, R13, R17), R9's THIRD memconf store (controller 0, 0x00, made after its default read: its
     controller-1 stores ARE followed by chipid and chiprev reads, probe:440-447 `R9 00 r6`, `R9 04 r7`) and R16's phase-11 tail
     are never followed by a chipid/chiprev read; chiprev accesses with D set are never followed by a chipid read.  Rows:
     `LD_BU(n,3,0x00)` want 0x80 and `LD_BU(n,3,0x04)` want 0x1
     at the END of R5 (r12, r13), R7 (r8, r9), R9 (r10, r11), R13 (r10, r11), R15 (r8, r9), R17 (r17, r18) and after R16's
     phase-11 tail (r29, r30); pc rows move accordingly.  (ii) A latch written from an arm that does not read it under its own
     gates (`L_DT_M_idat` under nC.D and kin): closed by the same readbacks plus item 1's stores.  (iii) `M ^= idata` at
     DT/DA/H/TL under idata bits 0, 2, 5 or 7 CLEAR: the only odd driver is R10's 0x5a default store (bits 0, 2, 5, 7 clear) and
     no memconf store follows it.  Row: at R10's end `ST_B(11,3,0x08)` with r11 = 0x07 (+0x08 is controller 0; it must
     announce: `R10 cnf line` has "memconf write 0x7 (controller 0) ignored, not modelled (once) ]" and `R10 lines` becomes "2";
     under the escape M is already 0x5a and the store is silent) and `LD_BU(12,3,0x08)` -> `R10 08b r12` want 0x3.  (iv) `M ^= idata` / `D ^= idata` /
     `memconf ^= idata` under offset bit 2 set (DA/DT ob2s, :9579, :9609) or bit 3 clear or bit 4 clear (H/TL ob3c, ob4c, :9615,
     :9696-9697): R17's two word default stores at +0x1c/+0x11c toggle twice and cancel; R12's and R16's paired served stores
     likewise.  Two rows, one per offset class: a THIRD `ST_W(9,3,0x1c)` in R17 after `ST_W(9,3,0x11c)` (silent; `R17 lines` stays
     "2") makes the bit-2-SET count odd before `ST_B(6,3,0x08)` observes M -- it does nothing for bits 3 and 4 clear, since 0x1c
     has bits 2, 3 and 4 SET; those gates fire on the served offsets +0x00/+0x04 (bits 3 and 4 clear), and item 1's word-store
     pairs there net to zero as well (two pairs of 0xffffffff ^ 0xffffff00).  So a LONE byte store of 0xff to +0x00: in R17's phase
     01 after its served pairs (`ST_B(5,3,0x00)`; M is clear there, `M ^= 0xff` makes it truthy and the first memconf store falls
     silent -> `R17 cnf line` red) and in R12 after its served pairs and before `LD_BU(13,3,0x08)` (`ST_B(9,3,0x00)`; D is clear
     there, `D ^= 0xff` makes it truthy and the final default read falls silent; `memconf ^= 0xff` reads 0xfc at r13).  (v) `D = 0`
     / `D ^= 1` at the default latch body under W.nC.M: R15's first default access (`ST_W(6,3,0x1c)`, M set) is its last.  Row:
     `LD_BU(10,3,0x1c)` after it -> `R15 1c r10` want 0, silent (r8, r9 are taken by 2(i)'s readbacks).  Its READ-side twin,
     `D = 0` / `D = idata` / `D ^= 1` at the default latch body under nW.C.M (a controller-1 default READ made with M set,
     :9586-9587): R9's first default read `LD_BU(8,3,0x10c)` is its last default access, and 2(i)'s served readbacks do not observe
     D.  Row: a second default read right after it, `LD_BU(12,3,0x10c)` -> `R9 10cb r12` want 0, silent on the fix (`R9 lines`
     stays "2"; under the escape it re-announces).  (vi) `d->warned_memconf = idata` at the
     memconf arm's end under `writeflag == MEM_WRITE && !controller` (W.nC, equivalently W.nC.M; PRETABLE_5.out:9637, :9639) --
     the WRITE test belongs to the survivor: ME lies after the write block, a controller-0 memconf READ has idata 0, so `M = idata`
     under `!controller` alone clears M on reads and is red (SCORES.txt:570 L_ME_M_idat_nC 201/206) while under W.nC it is green
     (:2999, 206/206).  Every controller-0 0x00 memconf store (R3's second, R7's second, R9's third) is the last memconf store of
     its session.  Remedy sketch: item 1's phase-10 pair and item 4's session.  (vii) `M ^= 1` at the chipid arm under C.D (:9519): it toggles on every controller-1 chipid access made
     with D set, and R16's phase 11 and R17's phase 01 each make exactly two (a store and its readback), which cancel; appended
     controller-0 readbacks do not disturb that.  Row: in R17, between `ST_B(6,3,0x08)` and `ST_B(0,3,0x108)`, one more
     controller-1 chipid read `LD_BU(19,3,0x100)` -> `R17 100b r19` want 0x80 -- under the escape M toggles to 0 and the
     controller-1 memconf store re-announces (`R17 lines` 3).
  3. **NB3: a first controller-1 memconf store ORed or XORed into chipid or chiprev** (PRETABLE_5.out:8167-8178; gate x first-store x
     operator).  R9's 0x00 first controller-1 store is the OR/XOR identity; R7's 0x07 first controller-1 store is followed only by
     default and memconf reads.  Rows: item 2(i)'s R7 readbacks -- `|=` gives chipid 0x87 / chiprev 0x07, `^=` gives 0x87 / 0x06.
  4. **NB4: `&=` into chiprev or memconf at the first memconf store under `!controller`** (PRETABLE_5.out:8199, :8211, NOCHANGE).
     Every controller-0 first memconf store the rows make is 0x07, 0xff or 0xffffffff, and 0x01 & 0x07 = 0x01, 0x03 & 0x07 = 0x03.
     Row: a new session R18 -- `ST_B(0,3,0x08)` (controller 0, 0x00, FIRST: announces "memconf write 0x0 (controller 0) ignored,
     not modelled (once) ]"), `LD_BU(2,3,0x04)` -> `R18 04 r2` want 0x1, `LD_BU(4,3,0x08)` -> `R18 08 r4` want 0x3, `LD_BU(5,3,0x00)`
     -> `R18 00 r5` want 0x80, then `ST_B(6,3,0x08)` with r6 = 0x07 (silent), `LD_BU(7,3,0x08)` -> `R18 08b r7` want 0x3,
     `LD_BU(8,3,0x00)` -> `R18 00b r8` want 0x80 and `LD_BU(9,3,0x04)` -> `R18 04b r9` want 0x1 (the 0x07 store is a controller-0
     memconf store in state (1, 0), item 1's first context, so its keeps must be read AFTER it, not before); `R18 lines` "1";
     `R18 pc` CODE + 32.  The second store also closes item 2(vi).
  5. **TO widenings** (`!M || (nC && nD)`, `!D || (W && C && M)` and the equivalents at PRETABLE_5.out:9513-9518): closed by item 1.
  6. **The cross-call caveat (one example inside the 6,676 VACUOUS, one inside the 665).**  semantic_vacuous judges ONE access over
     Boolean latch states (memc_variants_5.py:703-728), so `if (idata & 2) d->warned_default ^= idata;` after the default test is
     DISCARDED as vacuous (1 ^ v is truthy for every v with bit 1 set) although across calls D goes 1 -> 2 -> 0 and the category
     re-announces.  The ungated `d->warned_memconf ^= idata;` at the memconf arm's end is NOT among the discarded: the walker's
     idata = 1 sample clears a set latch (:698, :716-721), so it was built as L_ME_M_xori_any, classed NOCHANGE and measured 206/206
     (PRETABLE_5.out:7792-7794, SCORES.txt:2917) -- the same cross-call escape (M: 1 -> 2 -> 0 over memconf stores of 0x03 then
     0x02), recorded under a different class.  Rows:
     a new session R19 -- `ST_B(5,3,0x18)` (0x03, announces), `ST_B(6,3,0x18)` (0x02, silent), `LD_BU(2,3,0x18)` -> `R19 18 r2` want 0
     and `R19 lines` "1" (the escape gives "2"); then `ST_B(5,3,0x08)` (0x03, announces), `ST_B(6,3,0x08)` (0x02), `ST_B(7,3,0x08)`
     (0x07, silent) -> `R19 lines` "2" on the fix, "3" under the escape; `R19 pc` CODE + 24.
  Also disclosed and not rowed (unchanged from clause (e)): disjunctions other than the TO widenings and other non-conjunctive gates, multi-bit value and offset
  masks, len.  Closing all six items would be repair 6 -- coverage,
  not floor -- and must re-run table 5's 665 green representatives (`memc_variants_5.py list | apply`) against the widened probe.
  The rows above are hand-checked sketches, not a closure proof: the second reading of this filing (rec6_20261105, F3-F6) found the
  first sketches short in four places (a pc count, a source register, two identity values, three unobserved read-side cases), each
  corrected in place; the third reading (rec7_20261105, F2 and F4) found two of the rewritten explanations false (an exhaustive
  "each inserted statement either ..." sentence and a "changes truth only in one state" account) and they were removed, not
  replaced; only the re-walk can say the widened probe closes a family.

### F1. the final ruling (adj_p5_20261105/ADJ_MYTHOS_local.md), whole but for its section 2

MYTHOSADJP5MEMC

VERDICT: CLOSE-AFTER-RECORDS. Zero floor families, five debt families, codex's ten records upheld (plus one older wording item folded in). My pass-4 ruling was wrong where it mattered: section 3 called class L a CLOSED ENUMERATION and section 4's rows were justified by a product-exposure argument that the walk itself refuted (two minterm contexts never exposed, served readbacks not made after every phase). The 58 rows stand as coverage, the closure claim and the contract sentence do not. No row is owed in-round; the round closes on pass 5's denominator once the records below are corrected.

PREMISES CHECKED AGAINST THE TREE
- The function is as the packet quotes it: src/devices/dev_mvme187.c:59-144. The memconf path reads memc_memconf (:104) and warned_memconf (:112) and nothing else of device state; the default path reads warned_default (:127) only; the chipid and chiprev arms read their own field (:96, :100). The fold at :73-76 rejoins before the switch (:93), so `controller` dominates no arm. No body masks or compares an idata bit: idata is printed (:115, :133), never tested. The latches are `int` (:54-55); the fields `volatile u_char` (src/include/thirdparty/mvme_memcreg.h:32-36).
- The walker inserts MB after `d->warned_memconf = 1;` and DB after `d->warned_default = 1;` (r5_20261105/memc_variants_5.py:88, :93, :116-117, :122-123); its reachable states at MB have M = 1 (:688) and at DB/DA have D = 1 (:691-692).
- The table: SCORES.txt lines 1-5 are base, HEAD, null_true, null_absent, null_false, each tagged PRED=match; 3,523 PRED=match lines of 3,580 PRED lines; TALLY.txt:1-8 reports 3,575 variants and 665 at 206/206.

1. THE FLOOR QUESTION, family by family

The rule I hold myself to: the floor is the cross-product of the guard's dominating predicates with the device-state lvalues the fix's own repair path reads that are jointly reachable through its own data flow; joint cells outside it are clause-(e) debt; idata is graded by what the body tests, and no body tests it. From the code, the floor of this fix is small: memconf path {write :105, !M :112} x {memc_memconf, warned_memconf}; default path {default arm, !D :127} x {warned_default}; served arms {arm} x {own field}. Neither latch is jointly reachable with the other on any path, no served field is reachable from the memconf or default path, and `controller` and the idata/offset bits are not floor predicates. Against that floor every survivor fails on at least one axis.

(a) UNFIRED in-bound (58 groups; PRETABLE_5.out survivor summary, the `UNFIRED DT W.C.M.D`, `UNFIRED MT/MW W.nC.M.nD`, `UNFIRED MW nC.M.nD` lines after :9460). Every gate conjoins the OTHER path's latch: nD on the memconf side, M on the default side. DEBT. Disclosure: "Any gate that reads the other arm's latch is outside the floor: the memconf path never reads warned_default and the default path never reads warned_memconf. The two contexts the probe never drives are a controller-0 memconf store with (M,D) = (1,0) and a controller-1 default store with (M,D) = (1,1)." The 48 CI/CR high-idata-bit groups are outside the ruling's own alphabet (T5_PREP.md:68-69; CONS section 3 :42 places idata-bit gates at MT/MW/MB/DT/DB/DA/H/TL only) and outside the floor (no body tests idata). DEBT.

(b) UNOBSERVED by kind (411 groups). Scanning the summary lines: every group is one of (i) a cross-field keep (chipid from CR; chipid/chiprev from MB, MT, MW, ME, DT, DB, DA, H, TL) gated on a latch or controller, (ii) a latch written from an arm that does not read it (L_CI_*, L_CR_*, L_DT/DA/TL_M_*, L_H_*), (iii) `^= idata` parity under single idata-bit gates (ib0c/ib2c/ib5c/ib7c: R10's 0x5a sets M with no memconf store after) or under single offset-bit gates whose selected stores are even in number (ob2s, ob3c, ob4c), or (iv) D cleared or toggled at DB under W.nC.M. Each has a foreign target, a foreign latch in the gate, or an untested idata/offset bit as its only discriminator. DEBT. Disclosure: "A kept store into a field the arm does not read, a latch written from an arm that does not read it, and any value-toggle (`^= idata`, `^= 1`) whose selected stores are even in number before the next observation are disclosed, not claimed." Note against my own ruling: section 3 :52 disclosed even-count toggles only for two-predicate gates; the walk found them under single offset-bit gates (R17's two word default stores at +0x1c/+0x11c; R16's paired 0xff served stores). The disclosure must be widened to any gate.

(c) NB3 (`|=`/`^=` into chipid or chiprev at MB under controller; PRETABLE_5.out:8167-8176 UNOBSERVED). The memconf latch body reads memconf, M, idata, controller; chipid and chiprev are not its state. This is gate (controller) x position (first store) x operator, the three-way joint the shipped clause (e) already discloses (probe :69-70). DEBT, and my section 3 keep-form map (:51, "controller ... -> R3/R9 (memconf 0x00 stores)") was wrong for it, as the late replication said: R3's 0x00 store is non-first and R9's 0x00 is the OR/XOR identity. Disclosure: "A first controller-1 memconf store ORed or XORed into chipid or chiprev is a disclosed three-way joint; R9's 0x00 first store exposes only `=`." Remedy named for filing: chipid and chiprev readbacks at R7's tail.

(d) NB4 (`&=` under !controller at MB). Codex's byte arithmetic is right: every controller-0 first memconf store is 0x07, 0xff or 0xffffffff (R3, R5, R8, R12, R13, R15, R16, R17, wr_cnf), and 0x01 & 0x07 = 0x01, 0x03 & 0x07 = 0x03; chipid (0x80 & 0x07 = 0) is red on R16 100b r12, 00b r13, 100c r18, 00c r19. For chiprev and memconf this is probe-relative NOCHANGE, not semantic equivalence: a controller-0 first store of 0x00 would zero both. memconf is the memconf path's own state, so the ungated and write-gated `&=` keeps ARE floor, and they are red (K_MB_memconf_and_any on R9 108 r2, 08 r4, 08b r9; PRETABLE_5.out:3202). The surviving cell adds `!controller`, which dominates no arm. DEBT, same disclosure as NB2's filed residual (CONS section 1 E). Remedy named for filing: a controller-0 first memconf store of 0x00 followed by chiprev and memconf readbacks.

(e) TO_M / TO_D widenings (`!M || (nC.nD)` and equivalents; `!D || W.C.M` and W.C.M.D; summary `UNFIRED TO` lines). These edit the in-bound predicate, which is why I looked hardest here. Every single-literal widening is red (W, nW, C, nC, D, nD on the memconf test; W, C, M, nM on the default test, by R16's phase-10 controller-1 store, R3's second store, R7's tail and the like); only disjuncts that conjoin the OTHER latch survive, and that read does not exist on the fix's path. DEBT. Disclosure: "A widening of either latch test that reads the other latch is outside the floor; the two unexposed contexts are those of (a)."

On codex's bound argument: the outcome is right, the general premise is too strong. An inserted statement is not out of bound merely because it is inserted; earlier rulings admitted and rowed inserted gated latch sets at served arms (A_B5, A_B6, NB6-NB8, F1-F10) because they write the path's own state under in-path predicates. The test is whether the gate's predicates and the target are the path's own, and by that test every survivor is debt.

2. THE CORRECTED CONTRACT TEXT (replaces CONS section 3's sentence at :53 and the probe's repair-5 paragraph at :29-36; the clause (e) at :38-85 must also be regenerated with table 5's numbers, since it still reads "148-row probe" and "112 of 112")

[the section's quoted contract text is elided here: records 6 rewrote it into the probe header (block A, CONTRACT), corrected by the four readings (F3); the original stays in the file]

3. RECORDS R1-R10

[R1, R2, R3, R4, R5, R6, R7, R8, R9, R10 each UPHELD; their text is elided here -- where each correction now lives, with the sentence it replaced: r6_20261105/RECORDS6_NOTE.md section 2; the rulings themselves: adj_p5_20261105/ADJ_MYTHOS_local.md section 3.  The section's last paragraph, the +0x7c wording item, follows.]

Also folded in (the late replication's OPEN row 28, raised again by Gemini's second reading): the `rd 0x7c`, `R3 7c r4` and R8 notes say "past the struct"; +0x7c is past memcreg and on the latches inside struct mvme187_data (:47-56). Wording only.

4. CLOSE OR REPAIR 6

CLOSE-AFTER-RECORDS. The pass is valid: the diff shipped and runs 206/206 with the controls as predicted; the zero carries its denominator (37,974 cells over seven shapes and eleven positions, 3,575 variants, PRETABLE_5 before the table, calibrated on all 60 table-4 measurements). Zero floor breaches survive adjudication: every green family lies outside the repair paths' own guard-by-state product. The false records are records, fixed now; the survivors are FILED with their remedies named (a controller-0 memconf store in phase 10, a controller-1 default store in phase 11, chipid/chiprev readbacks after R7's tail, a 0x00 controller-0 first memconf store with readbacks, a memconf store after R10's 0x5a, an odd count of word default stores in R17). Repair 6 would be coverage, not floor, and the standing rule says a filter may not demand it.

MYTHOSADJP5MEMC: 0 FLOOR FAMILIES 5 DEBT FAMILIES 10 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS

### F2. pass 5's disposition (p5_20261105/DISPOSITION.md)

# mvme187memcoob PASS 5 -- disposition (main loop, 2026-11-05 ~11:2xZ)

Seats: GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_memc_p5.txt; `CODEXP5MEMC: 7 FAMILIES SWEPT 0 FLOOR CELLS OWED 10 FALSE RECORDS
VERDICT:REPAIR`): class L as the consolidated ruling defined it EXCEEDS the DEPENDS-ON bound -- an inserted statement is in bound only
when it restores a removed operation or is a direct null repair -- so every survivor family (the UNFIRED and UNOBSERVED groups, NB3,
NB4, the TO_M / TO_D widenings) is clause-(e) DEBT, not floor; NB4 is probe-relative NOCHANGE (byte arithmetic on volatile u_char
fields); the 58 new rows' wants are all correct; TEN false records R1-R10 (the universal class-L contract claim; variant totals that
include the five control legs -- 3,518 + 56 + 1 for variants; groups vs cells; NOCHANGE tracks latch truthiness; UNOBSERVED includes
cancellation; the VACUOUS prefilter's claim, refuted by L_DA_D_xori_ib1s across calls; NB4 IS in the green tally).  Gemini 4 Argon x2:
being sent.  glm-5.3 and grok-4.7: walled.

This is a RULE QUESTION between the round's ruler (whose consolidated ruling defined class L as the closed enumeration) and the standing
floor bound codex applies; the main loop records and does not rule.  Sent to the ruler (local Mythos 5.1, asked to be harder on its own
ruling) once the Gemini readings land: mythos_local/prompt_memc_adj5.md -> ../adj_p5_20261105/ADJ_MYTHOS_local.md.

ADDENDUM: Gemini x2 banked (gemini_p5_memc.md: CLOSE -- all 517 groups plus NB3/NB4 are clause-(e) debt; gemini_p5_memc_r2.md:
REPAIR -- the same floor answer, plus the `+0x7c past the struct` wording: it is past memcreg, on the latch bytes, inside the struct).
Three seats now argue debt, not floor; the ruler, whose class L this is, rules next.

### F3. the four readings of the records corrections (rec6..rec9_20261105/DISPOSITION.md)

# mvme187memcoob -- second reading of the records corrections (main loop, 2026-11-05 ~12:4xZ)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_memc_rec6.txt; `CODEXREC6MEMC: 7 ACCEPTED 10 TO FIX VERDICT:FIX`): of the original
items R2, R3, R5, R7, R8, R10 and the +0x7c wording are now true; R1 ("one readback per field" -- two, one per controller), R4 (the
457/60 split counts summary LINES, not representatives: 452 inside the alphabet, 65 supplementary), R6 (the unbuilt-green partition:
2,406 NOCHANGE + 1,228 UNFIRED/UNOBSERVED) and R9 (L_ME_M_xori_any is a BUILT NOCHANGE variant, 206/206 at SCORES:2917, not a discarded
VACUOUS cell) still need correcting; and six grouped findings on the new contract and filing (F1 scope/quantifiers -- walked-then-
discarded is not "outside the walk"; F2 the ME own-state debt needs its write predicate, measured: nC 201/206 vs W.nC 206/206; F3 the
proposed R16 pc; F4 the high-bit closing rows' register and the &= cases they cannot close; F5, F6).  The zero-floor disposition is
unchanged -- all are records and remedy descriptions.  The correction-is-not-safer rule, landing for the second time today on a
correction pass.  Sent back to the round's implementer (local Mythos, prompt mythos_local/prompt_memc_rec7.md), asked to check each
finding before correcting it.  Gemini was not sent this reading (the proxy's control checks are timing out).
[the rest: rec6_20261105/DISPOSITION.md]

# mvme187memcoob -- third (closing) reading of the records corrections (main loop, 2026-11-05 ~13:3xZ)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_memc_rec7.txt; `CODEXREC7MEMC: 7 ACCEPTED 3 TO FIX VERDICT:FIX`): R1, R4, R6, R9,
F3, F5 and F6 are now true.  F1, F2 and F4 each INTRODUCED a new false claim in the rewrite:
* F1 -- the NOT WALKED sentence lists controller x phase x operator three-way joints, which were walked and built (PRETABLE:9341-9342,
  SCORES:3523; :9283-9284, :3494); the first COVERED clause still lacks the nonvacuous qualifier.
* F2 -- the filing still claims its list of reasons covers every survivor (L_ME_M_idat_W.nC fits none of them), and names the wrong
  observing store (the earlier controller-1 byte store at probe:593 is the one that re-announces).
* F4 -- "changes truth in only one state" is false for M ^= 1 and D ^= 1, and the paired high-bit stores cancel each ^= 1.
[the rest: rec7_20261105/DISPOSITION.md]

# mvme187memcoob -- fourth reading, scoped to F1/F2/F4 (main loop, 2026-11-05 ~14:2xZ)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_memc_rec8.txt; `CODEXREC8MEMC: 2 ACCEPTED 1 TO FIX VERDICT:FIX`).  F2 and F4 are
accepted: the deletions left nothing dangling.  F1's probe edits are accepted.  Two RETAINED sentences were found false; codex notes
both are retained wording, not new explanations from rec8.  The deletion discipline held: rec8 introduced no new false claim.
* FILING :102 -- "disjunctions and other non-conjunctive gates" not rowed, without excluding the TO widenings (detected at
  SCORES:2886-2887 and given remedy rows).  Qualified with the probe :86 wording.
* probe :74 -- "R9's 0x00 first store exposes only `=`" is false: SCORES:1334, K_MB_chipid_and_C 205/206 RED=R9_00_r6.  DELETED.
Both were checked against the cited scores and applied by the main loop; text-only PASS; see r6_20261105/RECORDS6_NOTE.md section 8.
The premise put as a question was confirmed: :125-126 and ERRATA_PRETABLE :37-38 are coverage claims, true.  A fifth reading,
scoped to these two edits, is fired (rec9_20261105/).

# mvme187memcoob -- fifth reading, the two one-clause edits (main loop, 2026-11-05 ~14:4xZ)

GPT-6 Astra (codex, `ultra`) ANSWERED (codex_codex_memc_rec9.txt; `CODEXREC9MEMC: 2 ACCEPTED 0 TO FIX VERDICT:ACCEPT`): both edits
are true and their sentences complete, and RECORDS6_NOTE.md section 8 is accurate.  THE RECORDS CHAIN CLOSES HERE, on a valid zero-
finding reading with its denominator (the two edits, and section 8).  Chain: rec6 (10 to fix) -> rec7 (3, each NEW in the rewrite)
-> rec8 (1: two RETAINED sentences; the deletion discipline introduced nothing new) -> rec9 (0).  The zero-floor disposition
(adj_p5_20261105) stood throughout.  memc goes to landing: the kit is being built in _scratchpad/wmemc/landing/, and the REGRESS stage
is still owed.

### G. the fix: src/devices/dev_mvme187.c, HEAD against the staged file (= the working copy, the source table 5 measured), with enough context to show the whole struct and the whole function

```
(lines 47-97 of HEAD's file against lines 47-144 of the staged file: `struct mvme187_data` through the end of DEVICE_ACCESS(mvme187_memc); nothing outside that span differs -- STAGED_DIFFS_memc.md)
--- a/src/devices/dev_mvme187.c (HEAD cbd916d1)
+++ b/src/devices/dev_mvme187.c (staged = working copy, md5 97e983872a72)
@@ -1,51 +1,98 @@
 struct mvme187_data {
     struct memcreg        memcreg;
+    /*  mvme187memcoob: once-per-device announce latches.
+        DEVINIT memsets this struct, so they start at 0.  Keep
+        them directly after memcreg: regress/mvme187_memc_probe.py
+        detects a return of the old indexed read by reading these
+        bytes back at +0x7c (rows R3 and R8).  */
+    int            warned_memconf;
+    int            warned_default;
 };
 
 
 DEVICE_ACCESS(mvme187_memc)
 {
     uint64_t idata = 0, odata = 0;
     struct mvme187_data *d = (struct mvme187_data *) extra;
 
-    // TODO: not used yet
+    /*  Controller 1 (offsets 0x100-0x1ff) presents the same
+        register image as controller 0: DEVINIT derives one size
+        code from RAM/2 for both, and the model keeps one image.
+        The number is reported in the notices below.  */
     int controller = 0;
 
     if (writeflag == MEM_WRITE)
         idata = memory_readmax64(cpu, data, len);
 
     if (relative_addr & 0x100) {
         controller = 1;
         relative_addr &= ~0x100;
     }
 
-    odata = ((uint8_t*)&d->memcreg)[relative_addr];
-
+    /*  mvme187memcoob: struct memcreg is 124 bytes, but after the
+        fold relative_addr is 0..0xff.  The old code indexed the
+        struct with it before the switch for every access: for
+        0x7c..0xff an out-of-bounds read in the C source, whose
+        value the exiting default arm never used, so the compiler
+        could omit it (no AddressSanitizer report on the old build
+        at -O3).  Once the exit was removed it forwarded whatever
+        byte sits at that offset in the device struct: at
+        +0x7c..+0x83 the two announce latches, and beyond the
+        struct's end, memory outside the allocation (measured on an
+        x86_64 host with the indexed read reinstated: after a
+        memconf store, a load of +0x7c returns 0x1, the first byte
+        of warned_memconf).  No indexed read remains: the three
+        served arms read their own fields and the default arm
+        reads none.  */
     switch (relative_addr) {
 
-    case 0x00:    /* chipid */
-    case 0x04:    /* chiprev */
+    case 0x00:    /*  chipid  */
+        odata = d->memcreg.memc_chipid;
+        break;
+
+    case 0x04:    /*  chiprev  */
+        odata = d->memcreg.memc_chiprev;
         break;
 
     case 0x08:    /*  memconf  */
+        odata = d->memcreg.memc_memconf;
         if (writeflag == MEM_WRITE) {
-            fatal("mvme187_memc: Write to relative_addr %i (controller %i) not yet"
-                " implemented!\n", (int)relative_addr, controller);
-            exit(1);
+            /*  Bits 0-2 hold the size code that DEVINIT fixes
+                from the configured RAM; no other bit of this
+                register is modelled, so a store has nothing to
+                change and is not kept: the register keeps the
+                value DEVINIT gave it.  Announced once per
+                device; it used to end the emulator.  */
+            if (!d->warned_memconf) {
+                fatal("[ mvme187_memc: memconf write 0x%x"
+                    " (controller %i) ignored, not modelled"
+                    " (once) ]\n", (int)idata, controller);
+                d->warned_memconf = 1;
+            }
         }
         break;
 
-    default:fatal("[ mvme187_memc: unimplemented %s offset 0x%x",
-            writeflag == MEM_WRITE? "write to" : "read from",
-            (int) relative_addr);
-        if (writeflag == MEM_WRITE)
-            fatal(": 0x%x", (int)idata);
-        fatal(" ]\n");
-        exit(1);
+    default:
+        /*  No register is modelled at this offset.  A read
+            returns 0, which is also the value DEVINIT leaves in
+            every byte of the image other than chipid, chiprev
+            and memconf; a write is not kept.  Announced once
+            per device; it used to end the emulator.  */
+        if (!d->warned_default) {
+            fatal("[ mvme187_memc: unimplemented %s offset 0x%x"
+                " (controller %i)", writeflag == MEM_WRITE ?
+                "write to" : "read from", (int)relative_addr,
+                controller);
+            if (writeflag == MEM_WRITE)
+                fatal(": 0x%x", (int)idata);
+            fatal(" (once) ]\n");
+            d->warned_default = 1;
+        }
+        break;
     }
 
     if (writeflag == MEM_READ)
         memory_writemax64(cpu, data, len, odata);
 
     return 1;
 }
```

### H1. gate 14's memc block replayed over table 5's banked logs (dryrun_memc.py; the probe call replaced, marked, by a copy of each log; ../src/devices/dev_mvme187.c the staged source except in the last leg)

```
Gate 14's memc block replayed over table 5's banked logs, the probe call replaced by each log (`regress/artifacts/mvme187memcoob/landing_20261105/DRYRUN_memc.out`): base (the fix) green; HEAD red (181 of 216 checks); /bin/true red (183 of 216 checks); absent binary red (206 of 216 checks); /bin/false red (205 of 216 checks); B1 memconf exit reinstated red (131 of 216 checks); B2 default exit reinstated red (168 of 216 checks); B3 indexed read reinstated red (7 of 216 checks); A memconf store accepted red (23 of 216 checks); F default faults red (128 of 216 checks); D7 fold narrowed (the MISS) red (34 of 216 checks); HEAD source red (1 of 216 checks).

--- base (the fix) (probe_base.out; source staged): REPLAY_DONE checks=216 fails=0
--- HEAD (probe_HEAD.out; source staged): REPLAY_DONE checks=216 fails=181
--- /bin/true (probe_null_true.out; source staged): REPLAY_DONE checks=216 fails=183
--- absent binary (probe_null_absent.out; source staged): REPLAY_DONE checks=216 fails=206
--- /bin/false (probe_null_false.out; source staged): REPLAY_DONE checks=216 fails=205
--- B1 memconf exit reinstated (probe_B1_cnf_exit.out; source staged): REPLAY_DONE checks=216 fails=131
--- B2 default exit reinstated (probe_B2_def_exit.out; source staged): REPLAY_DONE checks=216 fails=168
--- B3 indexed read reinstated (probe_B3_idx_read.out; source staged): REPLAY_DONE checks=216 fails=7
--- A memconf store accepted (probe_A_cnf_accept.out; source staged): REPLAY_DONE checks=216 fails=23
--- F default faults (probe_F_def_fault.out; source staged): REPLAY_DONE checks=216 fails=128
--- D7 fold narrowed (the MISS) (probe_D7_fold.out; source staged): REPLAY_DONE checks=216 fails=34
--- HEAD source (probe_base.out; source HEAD's): REPLAY_DONE checks=216 fails=1
DRYRUN_MEMC_OK

(B3's failing checks:)
    FAIL mvme187_memc rows correct                            got=202 want=206
    FAIL mvme187 memc row: R3 7c r4                           got=0 want=1
    FAIL mvme187 memc row: R8 7c r4                           got=0 want=1
    FAIL mvme187 memc row: R8 80 r8                           got=0 want=1
    FAIL mvme187 memc row: R11 180 r4                         got=0 want=1
    FAIL mvme187 memc rows green                              got=202 want=206
    FAIL mvme187 memc rows red                                got=4 want=0
(the HEAD-source leg:)
--- HEAD source (probe_base.out; source HEAD's): REPLAY_DONE checks=216 fails=1
    FAIL mvme187 memc no indexed read                         got=1 want=0
(every leg's list: landing_20261105/DRYRUN_memc.out)
```

### H2. the rung-3 witness (witness_20261104/WITNESS.md, measured 2026-11-04 before any edit)

[its first two paragraphs -- the held design ruling and the instrument (the frozen probe, md5 69b4d98bfccb, on UNMODIFIED -E mvme88k -e mvme187 -M 64) -- are elided; the file has them]

| run | binary | RESULT | CONTROL | SYMPTOM | red rows |
|---|---|---|---|---|---|
| `prefix_head.out` | the scratch clone /tmp/gx579 rebuilt with HEAD `ebe5af82`'s `dev_pcc2.c`, `mvme_pcctworeg.h` and `cpu_ppc_instr.c`; `dev_mvme187.c`, `machine_mvme88k.c`, `memory_rw.c` checked `== HEAD` (`RUN.log`) | 13/21 | OK | PRESENT | the eight witness rows |
| `prefix_build.out` | `build/gxemul` (its `dev_pcc2.c` and `mvme_pcctworeg.h` are the tree's UNCOMMITTED copies, not this round's; the memc files are HEAD's) | 13/21 | OK | PRESENT | the eight witness rows |
| `null.out` | `/bin/true` | 8/21 | FAIL | ABSENT | -- |
| `nobin.out` | a missing path | 0/21 | FAIL | ABSENT | -- |

Controls: `ld.bu` at +0x00 reads 0x80 (MEMC_CHIPID), +0x04 reads 0x1, +0x08 reads 0x3 (memconf for 64 MB), and the controller-1 alias
+0x100 reads 0x80 -- values only the device supplies (a read at 0xfff43000 with no device there would be zero-filled by memory_rw.c:700-702).  Witness: `ld.bu` at +0x0c, +0x7c and +0xff each end the
process with `[ mvme187_memc: unimplemented read from offset 0x.. ]`, and `st.b` to +0x08 with `mvme187_memc: Write to relative_addr 8
(controller 0) not yet implemented!` (exit status 1; `prefix_head_sessions/`).

**Measured facts the ruling should weigh:**

1. **The host out-of-bounds read is LATENT, not live.**  On the ASAN build (`build-asan/`, `-O3 -fsanitize=address,undefined`) the loads
   at +0x7c and +0xff produced NO AddressSanitizer report: the default arm's `exit(1)` came first, and (REASONED from the missing report, not observed) the compiled handler does not perform that read on the exiting path (BANKED 02:5x at `asan_head/` -- `ld_bu_7c.txt`, `ld_bu_ff.txt`, `RUN.txt`: exit status 1, zero
   AddressSanitizer reports, the handler's text present; this sentence first cited the 01:1x smoke runs, which were never preserved --
   a wrong record an Opus reading seat caught, corrected here).  So removing the exit
   without bounding the index would make it live -- the bound must land with or before any change to the exits, and the detector owes an
   ASAN leg on the fix.
[the apparatus note and the owed list: witness_20261104/WITNESS.md]
