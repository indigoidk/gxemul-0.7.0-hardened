# T2 / round #571 (ppcdsformxo) -- BUILD_REPORT.md (the main loop as builder, with one Opus writing agent; 2026-10-24)

## 1. What was done, in order (BUILD_SPEC.md sections 2-9 under 10 and 10b)
* 07:41-07:5x: the Opus BUILDER agent and then a records agent were each stopped by the harness's safety classifier before
  writing anything (checkpoint `## 087a90`); nothing on disk, no tree touched.  The build was split: an Opus WRITING agent
  (S3) produced the detector, the gate block and the MANIFEST keys (no runs); every run, build and record below was done by
  the main loop with scripts in the session scratchpad `t2/build/` (frozen copies for the long jobs).
* 07:54 `BASELINE.out`: HEAD add098b9; `src/cpus/cpu_ppc_instr.c` at md5 87a766e0 in GXEMUL-SEC, est/, build/, build-asan/,
  /tmp/gxsec-build and /tmp/gxt2/base; every binary FRESH; the base binary's md5 equals the witness's (3cd0501c); no sentinel.
* 07:56 `PRETABLE.out` (before any table): sibling parity, claim -> row, guard/body partitions with EXHAUSTED/SAMPLED, the
  CHANNEL per row with the leg it kills, the diff against the brief's 26 cells.
* 08:26 S3 delivered `regress/ppc_dsform_probe.py` (40,883 b, md5 0266228894811ba6c51cff82585753c9, 834 lines, LF; N = 39,
  8 sessions, 108 census words, names <= 14 with the assert changed to 14 and a comment naming the gate pin), the gate-13
  block in `regress/gate_ppc.sh` (working tree == staged copy `staged/gate_ppc.sh.txt`, md5 d361db09), the two MANIFEST keys
  (working tree + `staged/check_probe_wiring.py.txt` from the HEAD blob; identical insertions), `DETECTOR_FREEZE.txt`,
  `staged/INSERTIONS.txt`.  Its logic check with a debugger stand-in (no emulator) predicted 22/39 on BASE and 39/39 fixed.
* 08:29 the detector FROZEN (md5 appended to BASELINE.out), then `prefix_BASE.out` on /tmp/gxt2/base/gxemul:
  **22/39, CONTROL=OK, SYMPTOM=PRESENT 17/17** -- every red row's got-value is the misdirected address, the shifted window
  or the missing stop (read row by row).
* 08:30 `PREDICTIONS.txt` written per leg from the frozen source, before any leg.
* 08:30-08:32 S5: /tmp/gxt2/work = cp -a of base; `patch571.py` applied (+29 lines, two `#571` tags); `rm src/cpus/*.o; make`
  rc 0, 0 warnings, FRESH; `fixed.out` **39/39 ABSENT RED=none**; `fixed_witness8.out` (the untouched witness) **8/8 ABSENT**.
  The same patch applied to GXEMUL-SEC and est/ (all three copies md5 2015e243f7af8e93fc2b5c283223bde5).
* 08:33-08:54 S6: 16 variant legs (`legs571.py`, each a `cp -a` of work with a `.MUTANT` sentinel, rebuilt, measured by the
  frozen detector, then DISCARDED) + L5b; `SCORES.txt`; `/tmp/gxt2/legs` empty at TABLE_DONE.
* 08:56-09:03 S7: the fixed file propagated to build/, build-asan/, /tmp/gxsec-build; each rebuilt; `CLEARANCE.out`.
* 09:0x S8: gate 13 alone (`bash run.sh 13`); `gate13_20261024.out` -- see section 6.
* tools/precommit_check.sh: SCORE_CLAIMS_MANIFEST 38 -> 39 with its dated line (`check_score_claims.py`: PASS, 39 pinned).

## 2. Diff stat (working tree vs HEAD add098b9)
| file | change |
|---|---|
| `src/cpus/cpu_ppc_instr.c` | +31 / -2 (two hunks: the `case PPC_HI6_LD:` and `case PPC_HI6_STD:` bodies of the inner switch) -- byte-identical in GXEMUL-SEC, est/ and the three build trees |
| `regress/ppc_dsform_probe.py` | NEW, 834 lines |
| `regress/gate_ppc.sh` | +39 (the `#571` block after `#565`'s, before the NetBSD `need_file`) |
| `tools/pipeline/check_probe_wiring.py` | +2 MANIFEST keys (staged copy from the HEAD blob at `staged/check_probe_wiring.py.txt`) |
| `tools/precommit_check.sh` | +3 / -1 (the coverage pin and its history line) |
| `regress/artifacts/ppcdsformxo/` | witness_20261024/ (+ receipts/), pass1_20261024/ (+ adj/), table1_20261024/, pass2_20261024/ |

## 3. N = 39, the rows
`DETECTOR_FREEZE.txt` lists them in emission order; CONTROL 22, SYMPTOM 17.  Sessions: loads (14 rows), stores (12),
five stop sessions (2 each), global 3 (`unasm census` 108/108, `word pins`, `neg apparatus`).

## 4. Every score, with its instrument and denominator (instrument = the frozen detector unless named)
| run | artifact | score |
|---|---|---|
| pre-fix, BASE binary | `prefix_BASE.out` | 22/39, CONTROL=OK, SYMPTOM=PRESENT 17/17 |
| post-fix, work binary | `fixed.out` | 39/39, ABSENT, RED=none |
| post-fix, the frozen 8-row witness | `fixed_witness8.out` | 8/8, ABSENT |
| L3 both cases reinstated | `L3_armHEAD.out` | 22/39 (predicted 22/39) |
| L4b / L4c one case reinstated | `L4b_case58HEAD.out` / `L4c_case62HEAD.out` | 31/39 / 30/39 (as predicted) |
| L5 identity body | `L5_identity.out` | 17/39, CONTROL=FAIL (as predicted) -- `(c): measured at L5_identity.out` |
| L5b absent binary | `L5b_absent.out` | no sentinel (FileNotFoundError), as predicted |
| L6a / L6b update dropped | `L6a_noupd58.out` / `L6b_noupd62.out` | 37/39 / 36/39 (as predicted) |
| L7 raw imm | `L7_rawimm.out` | 27/39 (as predicted) |
| L8a / L8b / L8c lwa variants | `L8a_lwaxo0flags.out` / `L8b_lwazero1.out` / `L8c_lwasize3zero0.out` | 36/39 / 36/39 / 25/39 with the emulator exit on the loads session and the sentinel present (as predicted) |
| L9a XO 0 as XO 1 | `L9a_xo0asxo1.out` | 33/39 (predicted 35/39: the two liveness rows also red -- the RA = 0 words refuse and stop their sessions) |
| L9b EA + 1 on XO 0 | `L9b_xo0plus1.out` | 33/39 (as predicted) |
| L10 update everywhere | `L10_updall.out` | 31/39 (predicted 33/39: the same two liveness rows) |
| L11 shared-assignment mask | `L11_sharedmask.out` | 37/39 (as predicted) |
| L12a / L12b reserved tests opened | `L12a_xo623open.out` / `L12b_xo583open.out` | 38/39 / 38/39 (as predicted) |
Every leg red; no leg red for a reason other than the one under test (`SCORES.txt` names the reason per leg).

## 5. Two-part clearance (`CLEARANCE.out`, 09:03)
build/: part 1 CLEAN, part 2 FRESH (gxemul a142d92a).  build-asan/: CLEAN, FRESH (79d75442).  /tmp/gxsec-build: CLEAN,
FRESH (14ede3bd).  est/: source tree, part 2 N/A (md5 2015e243 = SEC).  The peer's five dirty files in build/ untouched.

## 6. Gate 13 alone
`gate13_20261024.out` (09:03:54-09:1x, binary build/gxemul md5 a142d92a, `bash run.sh 13`): **PASS (193 checks),
REGRESS_PASS, RUN_RC=0.**  The `#571` block: all 53 checks ok (completed; sentinel last; the four keys counted once each
in any form and once in the accepted form; 39 rows by name; census 108/108; rows run / green / red 39 / 39 / 0).  The
siblings unchanged: rlwimi 28/28, rldimi 29/29, `ppc_rldicl` 24/24 with its single SCORE line, and the image-gated
rounding probe ran ("every rounding-mode write took" 0 misses).  The gate's detector log is preserved as
`gate13_ppc_dsform.log` beside this report (the $LOGDIR copy, `/tmp/gxregress/ppc_dsform.log`).

## 7. Where this build disagreed with the spec or a ruling (by id)
* BUILD_SPEC 10 item 2 said the five legal-access rows "gain nothing red": `lwa ra0 value` is opcode 58 with XO 2, so it is
  a SYMPTOM row (S3's correction; measured red on BASE).  SYMPTOM = 17 rows, not 18 (10b cut two stop sessions) and not 16.
* PREDICTIONS L9a and L10 missed the session-liveness consequence of an RA = 0 word turning into a refusal (2 rows each);
  the detector is redder than predicted, for the reason under test.  Recorded in `SCORES.txt`.
* The builder role was not held by one agent (two harness stops before any write); the measurements were run by the
  main loop from frozen scripts -- the receipts (`s5_fix_build.out`, `s6_all.out`, `CLEARANCE.out`) carry the commands.

## 8. Open items (for pass 2 and the main loop)
* The one ask-again goes to pass 2's panel (the table is clean).
* Landing: the ledger row (witness term scoped to the loads; `prefix_BASE.out` named for the store half; commits), the
  CHANGELOG round block (draft in scratchpad `t2/landing/changelog_571.draft.md`, `<<FILL>>` marks to clear), the four
  filings (C1-C4), OUTSTANDING_BUGS.md's dated section, the pass-2 receipt in `regress/pass2_ledger.tsv`, the MANIFEST
  keys landing with the files they name (the witness directory committed in the same unit).

## Addendum 2026-10-24 10:2x -- after pass 2 (`../pass2_20261024/PASS2_RULINGS.md`); each item quotes what it corrects

* **Line count (K5).**  Sections 1 and 2 say "834 lines"; the frozen, measured detector is **836** lines (40,883 b, md5
  `0266228894811ba6c51cff82585753c9`, as `DETECTOR_FREEZE.txt` says).  The SHIPPED file is **845** lines (41,610 b, md5
  `59e83491a5819a599c610b1aa8e8b847`): a docstring/comment-only revision made on pass 2 (`repair_p2/probe_docfix.diff`),
  verified code-identical and re-measured -- `prefix_BASE2.out` 22/39 PRESENT 17/17 with the identical red set, `fixed2.out`
  39/39 ABSENT, gate 13 alone PASS 193 (`gate13b_20261024.out`, detector log `gate13b_ppc_dsform.log`).
* **Times (K13).**  "08:30 `PREDICTIONS.txt`" -- its mtime is 08:32:01 (still before the first leg at 08:34:28).  Section 6's
  "09:03:54-09:1x" -- the gate log ends `=== 2026-10-24 09:05:23 done`.  `PRETABLE.out`'s header "~08:0x" -- mtime 07:56:54
  (before `prefix_BASE.out`, 08:29).  Every order proof holds.
* **The C4 census (spec section 10 item 7).**  At least FOURTEEN 64-bit-only forms decode with no width test on a 32-bit cpu
  (`cmpdi`/`cmpldi`, `cmpd`/`cmpld`, `ld`, `std`, `rfid`, `mtmsrd`, `ldarx`, `stdcx.`, `stdx`, `stdux`, `extsw`, `sld`; this
  round's `ld`/`ldu`/`lwa`/`std`/`stdu` among them); decoder-ungated is not the same runtime behaviour -- `X(extsw)` under
  MODE32 (`cpu_ppc_instr.c:3125-3131`) diagnoses and returns without writing the register.  Filed as `ppc64on32gate`; the
  filing does not pre-authorise a uniform sweep.
* **No boot A/B is owed (spec section 8).**  No PowerPC guest image in this tree's battery boots through opcodes 58/62
  (Argon's census, `../pass1_20261024/argon_agy_t2p1.txt:217-225`); the stepped detector is the round's only runtime
  instrument.  The gate's detector logs are preserved with their completion lines (`gate13_ppc_dsform.log`,
  `gate13b_ppc_dsform.log`).
* **PRETABLE channels (K6, F7).**  `PRETABLE.out`'s per-row CHANNEL lists are pre-table predictions and are incomplete; the kill
  map is `SCORES.txt`'s RED column.  The corrections (L9b for `lwa ra0 value`; L4b omitted at `ldu value`, `ldu ds0 value`,
  `lwa ds0 value`; L4c omitted at `stdu ds0 value`, `stdu alias val`; `lwz value` red under L8c; `unasm census` absent under
  L5b) are `DETECTOR_FREEZE.txt`'s notes and `SCORES.txt`'s addendum item 4.  `PRETABLE.out` is left unedited.
* **The landing copy of `tools/pipeline/check_probe_wiring.py` (F15).**  The commit stages `staged/check_probe_wiring.py.txt`
  -- the HEAD blob plus exactly the two `#571` keys -- never the working-tree file, which carries a peer's fifteen
  uncommitted lines (`../pass1_20261024/PASS1_RULINGS.md` section E item 6 and `BUILD_SPEC.md` say the same).
* **Gate 13 (K2, F16).**  `gate_ppc.sh`'s `#571` block comment now reads "Seven debugger-stepped guest sessions ... plus one
  bogus-machine session that exits before any step -- eight in all" (it read "Eight debugger-stepped sessions ... and one
  bogus-machine session"), and the gate title gains ` + #571 DS-form` (`repair_p2/gate_fix.diff`; `staged/gate_ppc.sh.txt`
  refreshed; the measured copy is `repair_p2/gate_ppc.sh.measured_d361db09.txt`).  No check line changed.
* **The frozen leg drivers (K4)** are preserved as `drivers/*.txt` with `drivers/MANIFEST.md5`.

## Addendum 2, 2026-10-24 10:4x -- after the F2 adjudication (`../pass2_20261024/adj/`: Astra AMEND, Grok AMEND, both LANDING GO WITH THE CHANGES NAMED)

* **Second docstring-only detector revision (F19, both adjudicators; F26, Astra).**  The first revision's new NOT CLAIMED bullet
  said "the case bodies read neither the sign of DS nor RA" -- false: the mask copies the DS sign bit into `imm`; the bodies
  never BRANCH on it and do not read `ra`.  Reworded in Grok's form, and the two cells Astra found neither rowed nor mentioned
  (`stdu` with RA = RS at DS = 0; the reserved encodings at a positive DS) disclosed as remaining non-floor coverage debt.
  `repair_p2/probe_docfix2.diff` (one hunk); SHIPPED md5 `3efd8cbec746b8224c32d6827b42db46`, 847 lines, 41,811 bytes.
  Re-measured (`repair_p2/remeasure3.out`): `prefix_BASE3.out` 22/39 PRESENT 17/17 with the identical red set, `fixed3.out`
  39/39 ABSENT, gate 13 alone PASS 193 (`gate13c_20261024.out`, `gate13c_ppc_dsform.log`).  The measured revision
  (`0266228...`, 836 lines) and revision 1 (`59e83491...`, 845 lines) are both preserved under `repair_p2/`.
* **The design row's severity (F22).**  Astra upheld `RESEARCH`; Grok overturned it (the ledger's one `RESEARCH` row is a
  census-without-witness label; 249 rows carry no severity).  Ruled for Grok: `ppc64on32gate` lands with NO severity and the
  OUTSTANDING_BUGS entry reads "(design, open; no severity assigned)".
* **Two more PRETABLE claims by erratum (F20, F21):** `PRETABLE.out:31` "32-bit CPUs decode unchanged" and `:66` "sources = 8
  distinct bytes" -- `SCORES.txt` addendum 2 items 7-8.  `PRETABLE.out` stays unedited.
* **The first addendum's over-wide sentence (D1 record, Astra):** corrected by `DETECTOR_FREEZE.txt` item 4.
* **Argon (F25):** both adjudicators widened the fabricated scope (Q2(c)-(e), Q3(d), Q3(e); `lwa neg value`, "11/39", a fake
  freeze md5, the `examine` command); the credit decision (Q1 only) stands.
* **Chain:** both adjudicators close the floor-bound repair chain with zero floor breaches; denominator: the first probe diff's
  three hunks, the second's one, the gate diff's two, and the six re-measured runs.

## Addendum 3, 2026-10-24 11:1x -- after GPT-6 Astra's exact-text clearance of the landed texts (`../pass2_20261024/adj/final/codex_t2final.txt`: GO WITH THE EDITS BELOW / LANDING HOLD, twelve record corrections)

* **Eleven applied, one rejected.**  Applied: a THIRD docstring-only detector revision (the tail's `ra == 0` zero-base test was
  missing from revision 2's parenthesis; `repair_p2/probe_docfix3.diff`, one line; SHIPPED md5 `e0a1e67eb0283abccde3bbd53952487a`,
  848 lines, 41,889 bytes; re-measured `prefix_BASE_r3.out` 22/39 PRESENT 17/17 identical red set, `fixed_r3.out` 39/39,
  gate 13 alone PASS 193 -- `gate13r3_20261024.out`, `gate13r3_ppc_dsform.log`); the ledger state-note prefix names the shipped
  revision and "three revisions"; "four reviewing seats" / "seven seats" -> seven answers from five reviewing seats; the pass-1
  Grok adjudication note's false 15-character rationale corrected; the pass-2 Astra note's "no base update with the RT = RA
  case" -> "ld/lwa/std perform no base update; an aliasing load still changes RA through its destination write"; the design
  row's "licensed fix shape ... applied uniformly" -> "a prospective design for its own round ... does not pre-authorise a
  uniform sweep"; "twenty-eight findings, every one a defect" -> "twenty-eight numbered findings whose required changes concern
  records, comments and contract wording"; F26's attribution excludes Argon; the CHANGELOG's wiring-checker bullet now carries
  the HEAD-plus-two-keys provenance it was said to carry; `DETECTOR_FREEZE.txt` item 6 separates `fixed_witness8.out` (the
  WITNESS's run) from the detector runs.  Rejected, on precedent: re-classing the frozen witness copy from CLASS_WITNESS to
  CLASS_RESEARCH -- HEAD's MANIFEST classes the two preceding rounds' frozen rung-3 witnesses and #539's post-fix-green witness
  as CLASS_WITNESS (`PASS2_RULINGS.md`, the final-clearance paragraph).  Astra also withdrew its F22 endorsement of RESEARCH:
  the row lands with no severity, as both adjudicators now say.
* **Addendum 2's chain sentence corrected.**  "Both adjudicators close the floor-bound repair chain ... denominator: the first
  probe diff's three hunks, the second's one, the gate diff's two, and the six re-measured runs" overstated what they reviewed:
  the adjudicators closed the chain over revision 1's diff (three hunks), the gate diff (two hunks) and revision 1's three runs.
  Revision 2 (one hunk, requested by both adjudicators) and revision 3 (one line, requested by the clearance) came after, each
  verified docstring-only and each re-measured (`prefix_BASE3`/`fixed3`/`gate13c`; `prefix_BASE_r3`/`fixed_r3`/`gate13r3`), and
  are recorded here separately; the corrected texts went back to Astra for a second exact-text clearance before the commit.

## Addendum 4, 2026-10-24 12:0x -- the clearance history corrected (Astra's third exact-text reading, `../pass2_20261024/adj/final/codex_t2final3.txt`)

* Addendum 3 says "Eleven applied, one rejected."  The true count for the first reading is TEN completed, ONE left incomplete
  ("four reviewing seats" survived in two ledger-ops sentences) and ONE wrongly rejected -- the frozen witness copy's MANIFEST
  class.  The checker's own line (`check_probe_wiring.py:55-57`: a WITNESS asserts the pre-fix symptom and is RED once the
  defect is gone) governs; the copy asserts the repaired property (5/8 on HEAD, 8/8 post-fix), so it is CLASS_RESEARCH, as
  Astra said twice; the class was changed in the staged and working-tree checker, and the precedents that conflict with the
  line -- `m88kbuserrregs`'s frozen witness and #539's post-fix-green entries, NOT `vmedefaultkill`'s (its sites probe reports
  outcomes without grading the defect; its free-run companion asserts the pre-fix symptom) -- are filed as `wiringwitnessclass`.
* The second reading named ten records; nine were applied and one (the stale "eleven applied" counts) was not, which the third
  reading found with six more (this addendum's subjects).  `PASS2_RULINGS.md`'s FINAL EXACT-TEXT CLEARANCES paragraph carries
  the full history; the reading that says GO is the clearance the commit rests on.
