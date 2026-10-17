# ADJUDICATION PACKET A -- #563 (wdc473floor): REPAIR3's pass-2 findings and the drafted REPAIR4

Prepared 2026-10-16 ~11:3x CDT by the main loop (Opus 5.5, session 087a90).  Owner directive of 2026-10-16:
**"Adjudicate any pending findings with both the Fable, Astra, and Grok."**  Three adjudicators answer this same
packet independently: Fable 5.1 (Agent seat), GPT-6 Astra (codex, ultra), Grok 4.7 (xhigh, plan mode).

This is the ADJUDICATION PASS (BRIEF_TEMPLATE §F2): every seat's pass-2 finding is consolidated below with MY
disposition; disagreements are listed separately with both sides; you rule.  It is an ordinary regression-detector
coverage review for a device-model test suite.  **READ-ONLY: write nothing to any project tree.**

## 0. Ground rules

- Tree under review: `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD **e483d931**.  Read product code as
  `git -C C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC show e483d931:src/devices/dev_wdc.c` (the working tree carries two
  sessions' uncommitted edits, none to `dev_wdc.c`; `regress/diff_wdc_identify.c` in the working tree is NOT REPAIR3).
  The project root's `C:/DocumentNoSnc/cc/GXEMUL/src/` is pristine 2021 upstream -- never read it.
- Rules: `GXEMUL-SEC/tools/CLAUDE.md` (working tree).  Rule D2 ("A REGION IS PINNED AT ITS EDGE") and the 2026-10-09
  rulings (derived input, clause (c), the "code does not move" oracle case) and the 2026-09-25 third disjunct exist
  ONLY in the working tree, not in `e483d931:tools/CLAUDE.md`.  Verbatim excerpt with line numbers:
  `C:/DocumentNoSnc/cc/GXEMUL/_scratchpad/gweb/jobs_20261016_argonpack7/_support/carrier_floor_rules_excerpt.md`.
- Nothing about #563 is committed.  REPAIR3 is a FROZEN CANDIDATE; REPAIR4 is a DRAFT SPEC; no REPAIR4 exists.
- Every distinguishing input in the findings below is REASONED from HEAD unless marked MEASURED.  The measuring seat's
  scratch-row stage (constructing each distinguishing input and measuring HEAD vs mutant) was NOT run
  (`r3pass_20261013/opus5/STATUS.md`, "NOT DONE").  The 159-row scores ARE measured.
- Separate READ (you opened it) from REASONED from MEASURED in your answer.  Count arguments, not seats.

## 1. Evidence index (paths relative to `GXEMUL-SEC/regress/artifacts/` unless absolute)

| short | path | what |
|---|---|---|
| R3 | `wdc473floor/repair3_20261013/` | REPAIR3.c.txt (md5 246b0840, 159 rows, CONTRACT block ~:1120-1220), TABLE3.txt (254 runs), PRETABLE3.out, SUMMARY3.txt, REPAIR3_vs_REPAIR2.diff |
| SC | `wdc473floor/r3pass_20261013/opus5/SCORES.txt`, `STATUS.md`, `mutants/<id>.c` | MEASURED: 48 one-line mutants vs REPAIR3; 15 pass all 159 |
| FR | `wdc473floor/r3pass_20261013/fable5/fable5_r3pass.md` | Fable 5.1 reading seat, pass 2 |
| GP | `wdc473floor/r3pass_20261013/panel_20261013_233050/grok.txt` | grok panel seat, pass 2 |
| GA | `wdc473floor/r3pass_20261013/grok_adversarial_r3pass.txt` | grok adversarial seat, pass 2 |
| CX | `wdc473floor/r3pass_20261013/codex_rerun/codex_r3pass_records.txt` | Astra, records-framed rerun (the panel's codex run was content-filter REFUSED: `panel_20261013_233050/codex.txt` tail) |
| OL | `wdc473floor/r3pass_20261013/panel_20261013_233050/ollama_{glm,minimax,kimi,deepseek}.txt` | packet-fed seats |
| AR | `adj_20261016/inputs/argon_wdc563_r1.out` | Gemini 4 Argon reading (packet-fed), tally `24 ATTACKS 4 BROKEN 11 HOLDS 9 UNSETTLED` |
| S4 | `agypack_20261013/repair4_spec/grok_repair4_spec.txt` | grok's REPAIR4 draft: 2 rows, 17 records, 5 open questions (its `.err` shows grok compacted its own context mid-task) |
| S4A | `agypack_20261013/repair4_spec_adv/grok_repair4_spec_adv.txt` | a second grok run asked to break S4 |
| ADJ | `wdc473floor/adj_20261013/` | the 10-13 adjudication (fable5_563_adjudication.md v1/v2, Astra) that ordered REPAIR3 |
| PS | `adj_20261016/prescreen/prescreen_563.md` | IF PRESENT when you read this: an Opus pre-screen of the agy-pack second readings (grok + Argon) of the #563 briefs, classed DISPOSED / LIVE / REFUTED.  Its LIVE list is part of this adjudication; if the file is absent, say so and skip it. |

Product anchors at e483d931 (verify, do not trust): read arm flag `if (d->atapi_cmd_in_progress)` :1228; consumed
ternary `int consumed = len == 4 ? 4 : (len >= 2 ? 2 : 1);` :1255; #475 clamp :1290; null-transfer latch :1312-1317;
re-arm guard :1318-1319; `received < data_in_len` :1359; re-arm clamp :1427, refill :1460; PIO arm :1468-1477; #495
refusal :1576-1578; wrap normalisation :1649-1651; dispatch guard :1716-1717; reject arm `res == 0` :1765-1776; DATA-IN
arm :1782-1801; DATA-OUT else :1803-1818; reset `wdc_new_command_reset` :915-924 (clears flag, phase,
write_in_progress, ring; leaves `atapi_st`, `atapi_len`, `atapi_received`, every `warned_*`); `atapi_st` sole writer
:1735.

## 2. Findings F1..F25 with MY DISPOSITION

Grades: FLOOR (a row is owed; L1 because REPAIR4 is pre-ship construction) / (e) DISCLOSED (written into the
contract, no row) / EQUIVALENT / OUT OF CONTRACT / RECORD (L4 text fix).

**F1. `D2_st`: :1228 `if (d->atapi_cmd_in_progress)` -> `if (d->atapi_st != NULL)` passes 159/159.**  MEASURED (SC);
predicted by FR before the table (independent); AR "REAL GAP"; S4 FLOOR.  Disagreeing state (flag 0, `atapi_st`
non-NULL) is reached by any dispatched packet command followed by any later command (writers :917 vs :1735).
**MINE: ACCEPT, FLOOR** (clause (d) DEPENDS-ON prong 2: guard operand swapped to a field the guarded body reads at
:1312/:1359/:1424/:1461 -- the carrier's own `#462` shape).  Repair: S4's Row 1 and Row 2 (F3).

**F2. `D2_or_st`: `flag || atapi_st != NULL` passes 159/159.**  MEASURED (SC); FR, AR, S4.  **MINE: ACCEPT, FLOOR**,
same cell, same rows.

**F3. Cell (flag 0, `atapi_len` > 0) unrowed** (reset clears the flag and keeps the count; `D2_len` was killed only on
the other cell).  S4 G3, REASONED.  **MINE: ACCEPT, FLOOR** (`atapi_len` is a repair-path lvalue, :1424-1427) ->
S4's Row 2 (`stale count, PIO boundary irq`: the shipped PIO body with `atapi_len = data_in_len = 1000`,
`atapi_received` 0, `atapi_st` non-NULL; oracle copied unchanged `a255 == 0 && a256 == 1 && occ == 512 &&
warned_null_xfer == 0`).

**F4. `D2_and_st` (`flag && atapi_st != NULL`) passes 159/159.**  MEASURED (SC).  The (flag 1, st NULL) cell differs
only in the host latch `warned_null_xfer`: pops precede the flag, a CMDOUT ring cannot sit on a 512-byte boundary
before dispatch at occupancy 12, CYL/ireason follow the flag (S4 §2).  AR calls the latch a "real gap".  **MINE:
EQUIVALENT ON GUEST CHANNELS, disclosed; no row** (the null decline's purpose -- no NULL dereference -- is achieved by
both arms; only a host diagnostic differs).

**F5. `D2_phase`** EQUIVALENT (flag and phase written together, :917-918 / :1046-1047; every other phase store sits in
a flag arm).  FR, SC prediction, S4; AR left it UNSETTLED for want of :951-1167.  **MINE: ACCEPT EQUIVALENT.**

**F6. `D3_ge0`** EQUIVALENT ((`atapi_len` > 0, st NULL) unreachable; sole `atapi_st` writer :1735).  **MINE: ACCEPT.**

**F7. `D7_lt1`, `D8_lt2`** EQUIVALENT (`diskimage_scsicommand` returns only 0, 1, 2: `diskimage_scsicmd.c` :282 :295
:302 :315 :327 / :892 :1291 / :1388).  **MINE: ACCEPT.**

**F8. `D0_nocmd`: :1176 `!io_enabled` qualified `&& relative_addr != wd_command` passes 159/159.**  MEASURED (SC).
Guest delta (S4, REASONED): a disabled STATUS read with a disk present returns 0 on HEAD (`goto ret`, :1171 :1176-1177
:2051-2065) and 0x50 under the mutant (:2024-2031, :584-589).  AR's "EQUIVALENT" answered a different question.
**MINE: (e) DISCLOSED with that delta written into the contract** -- the committed label clause applies (the selector
`relative_addr` flows into none of the three repair bodies); the 2026-09-25 third disjunct binds "the EDITED guard's
repair", and `!io_enabled` is a dominator, not a guard #473/#495 edited.

**F9. `D6_head`: :1717 `inbuf_len == 12` -> `d->inbuf_head == 12` passes 159/159.**  MEASURED (SC).  Differs whenever
`tail != 0` (push 6, a CMDOUT read pops 2, push 8: head 14, tail 2, length 12 -- HEAD dispatches, the mutant does not;
S4, REASONED).  AR's "equivalent because reset zeroes both" is refuted by that path.  **MINE: (e) DISCLOSED**, the
`tail != 0` state named in the contract (`inbuf_head` is read only through the callee `wdc_get_inbuf`; the DEPENDS-ON
bound stops at the callee; the body tests the derived local only `== 12`).

**F10. `D7_latch`: :1765 `res == 0` -> `res == 0 && !d->warned_atapi_err` passes 159/159.**  MEASURED (SC).  GP graded
it BREACH (its verdict); AR "REAL GAP"; FR's sentence "the reject arm reads no field, so no swaps" (FR §Q1 :60) is
REFUTED by :1766.  Guest delta (REASONED): a second rejected packet command on one device -- HEAD COMPLETED, ireason
0x03, DRQ clear; mutant falls into the DATA-OUT else: DATAOUT, ireason 0x00, DRQ set; INTRQ the same both ways.
**MINE: (e) DISCLOSED, class-wide** -- pass 11's floor is the cross-product of the dominating predicates with the
device-state lvalues "the fix's own repair path reads"; `warned_atapi_err` is read only by the reject arm, not by the
clamp/refill/push or the #495 refusal; the mutant does not null the repair (it reroutes a sibling exit).  Written into
the contract as one member of the LATCH-OPERAND class (F10, F11, F18, F19, F4), each with its guest delta.  See D2.

**F11. `D8else_latch`: the DATA-OUT `else` -> `else if (!d->warned_atapi_dataout)` passes 159/159.**  MEASURED (SC).
GP (sibling), AR.  Second DATA-OUT command: HEAD DATAOUT (0x00), mutant stays CMDOUT (0x01).  **MINE: (e), the latch
class (F10).**

**F12. `bepop_ge4`, `lepop_ge4`: the pop `if (len == 4)` -> `if (len >= 4)` (:1210 BE, :1203 LE) pass 159/159.**
MEASURED (SC).  GA: an 8-byte DATA read pops 4 where HEAD pops 2 (:1233); on a 2-byte DATA-IN the two extra pops hit
an empty ring, return -1 and set `warned_inbuf_overread`; `consumed` is untouched.  Reachability of width 8: MIPS64
`lld`/`ld` (`cpu_mips_instr.c`, X(lld)), `DEV_WDC_LENGTH` 8, and the #337 comment near :1597 (REASONED by GA).
**MINE: (e) DISCLOSED** -- the pop tests do not dominate the edited sites, and width 8 sits in the body's width-2 case;
name the 8-byte delta.  Contested: see D4.

**F13. `cons_eq2`: :1255 `len >= 2` -> `len == 2` passes 159/159.**  MEASURED (SC).  GA's ESCAPE (REASONED): an 8-byte
DATA read of a 2-byte DATA-IN -- HEAD consumes 2, completes, SECCNT 0x03, CYL_LO 0x00; mutant consumes 1, stays
DATA-IN, SECCNT 0x02, CYL_LO 0x01.  GA: "Rule D2's edge for that compare is length 3 ... No row sits on either."
**MINE: (e) DISCLOSED**, consistent with the contract's (e) for `n_C6` and `n_E_cons_ge4`, which FR AGREED to on the
reason that "the ternary BUCKETS width 8 with width 2".  Contested: D4.

**F14. `cmdlen_ms10`: the MODE SENSE(10) operand dropped from the `cmd_len = 10` test (:1747-1750) passes.**
MEASURED (SC).  FR, GA, AR, S4 agree: the stub copies 12 bytes and never reads `cmd_len`; the real MODE SENSE(10)
handler switches on it (`diskimage_scsicmd.c` ~:569).  **MINE: OUT OF CONTRACT, stated** (S4 record R7).

**F15. `n_F_VD1_width1_consumes2` (`len == 4 ? 4 : 2`) -- already a disclosed (e) survivor in REPAIR3's TABLE3.**
FR disputes the grade: `len >= 2 ? 2 : 1` makes width 1 its own CASE; the one width-1 row (`write route: 1-byte store is
refused`) reads occupancy and a constant fill, which VD1 cannot move, so the case is driven and unobserved.  Guest
delta (REASONED): arm a 36-byte DATA-IN, one 8-bit DATA read, read CYL_LO: HEAD 35, VD1 34.  S4 open question 5.
**MINE: UPHOLD FR -> FLOOR.**  My added warrant: VD1 is exactly the downward bound move `len >= 2` -> `len >= 1`, the
least-observable non-equivalent move of that bound, and the only row at the region below the bound cannot vary under
it.  Repair: one count read (CYL_LO/CYL_HI) after the first 1-byte DATA read in the existing 1-byte write-route walk
(want 32767), or FR's two-call leg (arm 4, one 1-byte read: count 3, DATA-IN).  See D3 for the consistency question
with F13.

**F16. The wrap-normalisation survivors `n_E_norm_le0` / `n_E_norm_ltm1` / `n_E_norm_deleted`.**  (e) grade stands;
the contract's REASON "the ring is reset at every command, so a CDB never wraps it" is FALSE: one CMDOUT can wrap it
with 262655 one-byte store/read pairs and then 12 bytes -- HEAD normalises to 12 and dispatches, the deletion does not
(FR Q4.1, CX §3, REASONED).  glm and the kimi substitute made the survivors' grade conditional on whether the sector
drain reads the normalised local.  **I CHECKED IT BY READING e483d931:** the drain's guest-visible arm (:1846-1851)
requires `inbuf_len > 0 && !badlen_this && write_in_progress == WDCC_WRITE|WRITEMULTI`; `wdc_new_command_reset` clears
`write_in_progress` (:919) on EVERY command including ATAPI_PKT_CMD; an empty ring after a store therefore needs a
refused push (only #495 in ATAPI phases, where `write_in_progress` is 0) or `badlen_this` (which blocks the drain).
The only `<= 0` difference left is the host announce latch `warned_empty_drain` (:1881-1885) for WRITEMULTI with
`write_count >= 2` -- FR's finding.  **MINE: (e) stands; RECORD the corrected reason (S4 R4) and the drain-latch
precision; the conditional breach is REFUTED.**

**F17. Records from CX / FR Q4 / S4 R1-R17.**  The widths sentence ("widths 2 and 4 are read by every walk" -- the six
walks read 2, 4, 2, 1, 2, 2); "CDB copy `> 1` killed (every arm row)"; the guard-edge comment "the count reads 1" (the
row reads internal `atapi_len`, not CYL); "whose dominators are the arm's" (the refusal precedes the CDB/result/pointer
guards); "Every 2-byte store that LANDED ... carried two equal bytes" (the LE liveness row stores 0x34, 0x12); SUMMARY3
hunk line counts (+1129/-83 and +734/-105); uncommitted-ruling citations at the consumed line and the refusal line;
the reject-arm "breaks before the tail" sentence; FR Q4.5's note that a bare `grep FAIL` of gate2.out gives 63 hits
(the gate's anchored sense gives 0).  **MINE: ACCEPT all 17 + FR's two extras as RECORDS**, and UPGRADE two of them from
wording to oracle additions, because both fixtures already read the channel and the addition is free (L1):
R14 -> the DATA-OUT dispatch row's predicate also checks the guest byte count it already reads (`lo`, `hi`); R15 -> the
io row samples INTRQ after the disabled DATA read.

**F18. S4A ESCAPE: :1228 `flag` -> `flag || d->warned_null_xfer`** passes the 159 and both drafted rows (REASONED).
First input: a null-transfer latch set earlier (ATAPI_PKT_CMD, one DATA read before any CDB), then any ATA command,
514 bytes queued, one width-2 read: HEAD asserts the PIO boundary interrupt (`int_assert` 1), the mutant takes the null
arm (0).  **MINE: (e), the latch-operand class (F10)** -- `warned_null_xfer` is read by the guarded body (:1313) but
not by the repair path; S4A itself says "a strict pass-11 grading would call the cell (e)".  Contested: D2.

**F19. S4A ELSE: :1197 `writeflag == MEM_READ` -> `... || d->warned_null_xfer`.**  Latch set, flag still 1, phase
CMDOUT, one 2-byte DATA write: HEAD pushes (occupancy 2), the mutant pops an empty ring (0).  **MINE: (e), latch class.**

**F20. S4A joint cell (flag 0, `atapi_len` 0, `atapi_received` < `data_in_len`, `atapi_st` non-NULL)** -- neither
drafted row holds it; a null-safe disjunct `flag || (st != NULL && atapi_len == 0 && received < data_in_len)` passes
both.  Reachability DERIVED by S4A (arm 40000 bytes, read down to 2 left, ATAPI_PKT_CMD, one width-2 read in CMDOUT,
then a non-packet command).  **MINE: ACCEPT, FLOOR CELL** -- every operand is a repair-path lvalue, so it is inside
pass 11's floor cross-product; the composite disjunct is not itself an enumerated mutant ("never arbitrary boolean
functions"), but a cell-exempting mutant on a reachable floor cell is a breach.  Row N3: synthesise that state (the
idiom of Rows 1/2), one DATA read, oracle = HEAD's PIO behaviour (no refill: occupancy and INTRQ unchanged).  Its
reachability gets MEASURED in REPAIR4's PRETABLE.

**F21. glm (NOT CHECKABLE, E_norm drain premise)** -> settled by F16.  **F22. minimax CLEAN** -> REFUTED on its Q1 by
measurement (it reasoned only about the (flag 1, st NULL) cell and missed (flag 0, st non-NULL)).  kimi substitute
NOT CHECKABLE (E_norm) -> F16.  deepseek NOT CHECKABLE (denominator not inlined).  agy and the kimi CLI did not answer
(SEATS.txt: SUSPECT 410 b / 284 b) -- seat failures, not agreement.

**F23. codex panel seat REFUSED (content filter); the records-framed rerun answered (CX: "INCONSISTENT").**  Seat
ledger only.

**F24. AR's four BROKEN points** are F4, F1/F2, F10/F11, F12/F13; its D0_nocmd and D6_head "EQUIVALENT" are refuted
(F8, F9).  Nothing new beyond F1-F20.

**F25. The scratch-row stage was never run.**  **MINE: REPAIR4's PRETABLE.out must MEASURE every new row on HEAD and on
its named mutants (`D2_st`, `D2_or_st`, `D2_and_st`, `D2_phase`, VD1, and the F20 disjunct) BEFORE table 1** -- the rows
become the measurement that pass 2 did not make.

### My REPAIR4 as disposed (for you to attack)

New rows (fixtures synthesised; every existing row byte-identical): **N1** `PIO: stale xfer, no early irq` (S4 Row 1);
**N2** `stale count, PIO boundary irq` (S4 Row 2); **N3** the F20 joint cell; **N4** the VD1 count read on the 1-byte
walk (F15).  Oracle additions on existing rows: DATA-OUT count (R14), disabled-DATA-read INTRQ (R15).  Contract: the
operand-swap class closure table (S4 §1 G0-G13, with S4A's three additions), the latch-operand class as (e) with five
named members and deltas, the width-8 cell (e) with its MIPS64 delta, `D0_nocmd` (e) with 0 vs 0x50, `D6_head` (e)
with `tail != 0`, `cmd_len` OUT, the four EQUIVALENTs, S4 R1-R17.  Order: PRETABLE.out first (mtime proves it), then
the table, then the pass on REPAIR4.

## 3. DISAGREEMENTS D1..D7 -- rule on each; parties, adjudicate your own

**D1. Is `D2_st` floor?**  FOR: FR, SC (measured), AR, S4.  AGAINST: minimax ("EQUIVALENT BY REACHABILITY").
**Ruling (mine): FLOOR** -- minimax's argument addressed only (flag 1, st NULL); the measured 159/159 and the
reachable (flag 0, st non-NULL) state settle it.

**D2. The latch-operand class (F10, F11, F18, F19; F4's latch).**  FLOOR side -- GP: "a clause-(d) hole on a predicate
that dominates #473's arm"; S4 open Q1 cites the generating-set sentence ("every ... bit the guarded body TESTS is
written both clear and set") and that the reject arm tests the latch; AR: "REAL GAP"; the second-reject delta is
ordinary driver traffic.  (e) side -- pass 11: the floor is the repair path's lvalues, and no latch is read by the
clamp/refill/push/refusal; S4A: "a strict pass-11 grading would call the cell (e)"; the mutants reroute sibling exits
and do not null the repair.  The cost question: if the class is FLOOR, it is not five rows -- every `warned_*` read by
any guarded body dominating the three sites becomes a member (the write arm's `warned_badlen`, `warned_empty_drain`,
...), and the enumeration must say which.  **Ruling (mine): (e), disclosed as a class with the five measured or derived
members' deltas.**  Grok: GP and S4A are yours -- be HARDER on the FLOOR reading than you were.  Fable: FR's
"reads no field" sentence is refuted -- does that change your grade?

**D3. VD1 (F15) vs `cons_eq2`/pops (F12/F13): one rule, two grades?**  Three readings are on the record:
(i) the GENERATING SET with D1's relational reading ("its generating set is its three regions, below / at / past the
bound") applies to the body's compares on the access width `len`: then BOTH are owed -- width 1 with a live readback,
and the past region (widths 3, 5-8) by a row, i.e. a width-8 row (if widths 3/5-7 are unreachable);
(ii) the 2026-10-09 DERIVED-INPUT ruling: `consumed` is a derived local, graded by what the body tests on IT
(`consumed > atapi_len`), so BOTH are (e);
(iii) CASE PARTITION (FR's reading; S4 calls them mirrors): the body's tests induce the cases {1}, {2,3,5-8}, {4};
VD1 changes a whole case whose only row is blind -> FLOOR; `cons_eq2` and the pops change values INSIDE the
{2,3,5-8} case -> (e), as `n_C6`/`n_E_cons_ge4` already are.
**Ruling (mine): (iii)** -- VD1 FLOOR, F12/F13 (e).  I am least sure of this ruling of any in the packet: D1's text says
"three regions" and does not say "cases", and D2 (which my VD1 warrant borrows) binds only compares "a fix DEPENDS ON",
which the non-dominating ternary may not be.  If (i) wins, the repair is ONE width-8 row on a short DATA-IN checking
count, phase, the returned bytes and `warned_inbuf_overread` (it kills F12, F13, `n_C6`, `n_E_cons_ge4` at once) plus a
derivation of which widths in 3/5/6/7 any CPU here can issue.  Rule the reading, and say whether widths 3, 5, 6, 7 are
reachable.

**D4. GA's D2-edge claim for `cons_eq2`** ("Rule D2's edge for that compare is length 3").  Is the ternary's `len >= 2`
a compare the fix DEPENDS ON (prong 1: it does not dominate the edited lines; both outcomes reach them)?  **Ruling
(mine): NO -- D2 does not bind it**; folded into D3.

**D5. `D0_nocmd` (F8): (e) or floor under the third disjunct?**  S4 open Q3.  **Ruling (mine): (e)** -- the disjunct
binds the edited guard's repair; `!io_enabled` is not edited.

**D6. Repair shape for F1/F2: FR's one-line edit of the shipped `row_pio_sector_irq` (allocate `atapi_st` before the
preload) vs S4's two NEW rows leaving the shipped row byte-identical.**  **Ruling (mine): S4's new rows** -- they keep
the measured row's oracle and fixture intact and also hold F3's cell, which the one-line edit leaves open.

**D7. `D2_and_st` (F4): host latch only -- disclose (mine, S4) or row it (AR)?**  **Ruling (mine): disclose.**

## 4. What is still owed, and where I may be fooling myself

- **I accepted 21 of 25 findings as stated or refined, and rejected only minimax's CLEAN and two AR "EQUIVALENT"s.
  That is a suspicious count.  Agreement is not evidence.**
- Every guest delta in F8-F13, F15, F18-F20 is REASONED.  None was constructed and measured.
- My (e) grades in D2 and D3 lean on pass 11's "repair path" wording; a reader who takes the generating-set sentence
  literally reaches FLOOR for both classes, and REPAIR4's pass would then find them again.  If that is right, say so
  now: the class-closure amendment says the NEXT repair closes the class in ONE diff.
- Width-8 reachability rests on GA's reading of `lld` and the #337 comment; I did not open `cpu_mips_instr.c`.
- S4 was written by a grok run that auto-compacted mid-task (`repair4_spec/grok_repair4_spec.err`).  Its citations
  were not all re-derived by me.
- The agy-pack second readings (PS) may hold a LIVE item none of us has seen.

## 5. QUESTIONS (answer all; VERDICT LINE FIRST)

Open with your seat token and ONE verbatim line from `wdc473floor/repair3_20261013/REPAIR3.c.txt` (from the block that
begins `CONTRACT (vacuity floor clause (e))`), so the packet's delivery and your file access are both proven.

`VERDICT: UPHOLD ALL / UPHOLD WITH CHANGES (<n> rulings changed) / OVERTURN (<the load-bearing ruling>) -- <one line>`

1. Adjudicate F1..F25 and D1..D7: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with the reason (a file
   and line where one settles it).
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  I accepted or refined 21 of 25 findings.  That count is
   suspicious, and agreement is not evidence.
3. **WHAT DID ALL OF US MISS?**  You now have every pass-2 seat's output.  Is the class REPAIR4 must close named
   correctly ("the operand-swap axis of every dominating guard"), and is S4 §1's G0-G13 plus S4A's additions the
   complete enumeration of it?  Name any member missing, with the input that reaches it.
4. Is my REPAIR4 (N1-N4, the two oracle additions, the contract table) sufficient for the CLOSING pass to verify an
   enumeration rather than hunt cells?  If not, what is the smallest change that makes it so?
5. If PS exists: rule on each LIVE item in its `## LIVE items for the adjudicators` list.

Seat-specific:
- **Fable 5.1**: FR is your own pass-2 reading.  This is self-review -- be HARDER on F1 and F15 than you were, and check
  that my REPAIR (N1-N4) is right, not only that your finding was.
- **Grok**: GP, GA, S4 and S4A are four of your own runs.  Self-review: attack S4 first.  D2 and D3 adopt S4's
  framing in part -- scrutinise them more, not less.
- **Astra**: CX is your records rerun.  You cannot run code -- say where a claim needs a run.
