# T36 / #570 (m88kbuserrregs) -- PRE-COMMIT REPAIR report, 2026-10-24

The builder's report on `../pass2_20261023/REPAIR_SPEC.md`, sections 1-6 plus section 7 (GPT-6 Astra's F2 amendments,
which override where they name an item).  The warrants are in `../pass2_20261023/PASS2_RULINGS.md` B, D and E.

Ground rules kept:
* git: object reads only (`git show`, `git log`, `git ls-files`);
* the peer's five files untouched in every tree (md5s below);
* builds in WSL Gentoo, foreground, one at a time;
* helper scripts in the session scratchpad `t36/repair/`;
* LF preserved.  A byte-level scan of all 48 files this step wrote or edited finds no `\r`.  The one exception,
  `CITATIONS_after_rewrap.txt`, came out CRLF through Windows python's stdout and was converted to LF before this report.

No mutation leg, boot pair or full gate was run.  Every receipt below is a recorded output in this directory.

## 0. Identities

| file | before | after |
|---|---|---|
| `src/cpus/memory_rw.c` | `b36c9e13` (813 lines) | `4b71687469a8b38165f038d3e9171293` (813) |
| `src/devices/dev_m8820x.c` | `c229294f` (551) | `bd616d06d7a2a4da388429ca326c4a5e` (551) |
| `src/cpus/cpu_m88k.c`, `src/devices/dev_luna88k.c` | `0321e2ba`, `e43c39ca` | not edited |
| `regress/m88k_buserr_probe.py` | rev 2 `d57c12ab` (836 lines) | **documentation revision 2b `9046d77432e0e6438c93732ec0cc9827`** (848) |
| `regress/gate_arm.sh` | `5ee94e61` (2162) | `f04fad2c589f9eb10f4a4fc3dc5896d9` (2162) |
| `tools/pipeline/check_probe_wiring.py` (working tree) | `a3548957` (4271) | `7e5beb5df9336f57d8267540226b701e` (4275) |
| `table1_20261023/staged/check_probe_wiring.py.txt` | `4847f8b3` (4256) | `88739fcb0440354e74d74c96a9f72d5a` (4260) |
| `table1_20261023/staged/gate_arm.sh` | `5ee94e61` | renamed `gate_arm.sh.txt`, `f04fad2c` (byte-identical to the working-tree gate) |
| `table1_20261023/SCORES.txt` | `e1924d27` (144) | `4d52dc44295f9b17866595f1c536d0e8` (145) |

These files are byte-for-byte unchanged:
* `PRETABLE.out` (`1936dedc`, mtime 2026-10-23 22:28:08);
* the frozen rev-2 artifact (`d57c12ab`, 22:42:48);
* the rev-1 witness (`d59798b0`);
* `BUILDER_QUESTIONS.md` (`640b40fe`, 22:29:30);
* `gates/gate14_run.out` and `gates/gate11_run.out`.

## 1. Product comments (section 1 + 7) -- `product_comments.diff`, `LINE_CHECK.txt`, `CITATIONS_after_rewrap.txt`

| id | file:line | old -> new |
|---|---|---|
| B1 | `dev_m8820x.c:361` | `(cpu_m88k.c:354-355)` -> `(cpu_m88k.c:358-359)`.  Re-verified: `:358-359` is the `cmmu[]` loop. |
| B4 | `dev_m8820x.c:293-294` | "the model writes only PFSR and / PFAR (...)" -> "the model's FAULT PATHS write only PFSR / and PFAR (...)".  `:295-299` are byte-unchanged. |
| B3 | `dev_m8820x.c:326-333` | The `#570` fold into the `~10^5` sentence is removed.  The new text reads "...~10^5 times per boot (memory_m88k.c:382-405's translation-fault writer alone) -- against 2 guest writes per boot through this handler.  #570's refused-device arm (memory_rw.c) also writes both directly with no purge; its frequency was NOT measured."  It presents no combined count, and the historical citation note is kept (compressed; see D-3). |
| B2 | `memory_rw.c` (`#570` comment, now `:625-627`) | "NO_EXCEPTIONS callers (the debugger) never get here: the test above keeps them out." -> "NO_EXCEPTIONS callers (e.g. the debugger's dump) never get here: the test above keeps them out." |
| B5 | `memory_rw.c` (now `:621-625`) | "A cpu without a CMMU gets no write and still takes the exception." -> section 7's wording, verbatim: "For a CPU without a CMMU, this arm makes no register write; the exception call is unchanged.  \`null route\` scores data-access delivery; instruction-access delivery is unscored (\`null surv\` scores survival only)." |

**Line-count proof.**
* `memory_rw.c` stays at 813 lines and `dev_m8820x.c` at 551; each est/ twin is IDENTICAL.
* Every hunk is an equal-range `c`: `615,627c615,627`; `293,294c293,294`, `326,333c326,333` and `361c361`.  So no line outside the comments moved.
* `dev_m8820x.c:537` is still `CHECK_ALLOCATION` (FAILURE embeds `__LINE__`).

**`__LINE__` check.**  REPAIR_SPEC's literal `grep -c 'assert\|FAILURE\|CHECK_ALLOCATION' memory_rw.c` returns **3**, not 0.
* All three hits are prose inside the comment at `:116`, `:117` and `:122` ("asserted", "asserted", "assertion").
* The macro-call/`__LINE__` token form returns **0**.
* The static assertion at `:125-126` is named from `MEMORY_RW`, not `__LINE__`.

**Citation re-grep (section 7).**  It lists all 25 line citations in the four files with their targets.  The four inside
the edited lines resolve correctly: `:294`, `:326` and `:329` to `memory_m88k.c:382/384/399/405`, and `:361` to
`cpu_m88k.c:358-359`.

**Object identity (work clone, `rm src/cpus/*.o; make`).**  Evidence: `objmd5_before.txt`, `objmd5_after.txt`, `REBUILD_work.out`.
* 0 warnings; binary FRESH against all four files.
* dev_m8820x.c, cpu_m88k.c and dev_luna88k.c were each recompiled.
* **224/224 objects plus the binary are identical**:

| object | md5 (before = after) |
|---|---|
| `dev_m8820x.o` | `e695696d...` |
| `cpu_m88k.o` | `ba859ef0...` |
| `dev_luna88k.o` | `2299b262...` |
| `gxemul` | `3cd0501c...` |

**Shipped detector on the rebuilt binary.**  `fixed_after_comments.out` with rev 2 `d57c12ab` gives 31/31, CONTROL=OK,
SYMPTOM=ABSENT and the sentinel.  Its only differences from `table1_20261023/fixed.out` are the LABEL, the ELAPSED time and
the header label.

## 2. Documentation revision 2b (section 2 as corrected by section 7)

Evidence: `rev2b.docstring.diff`, `rev2b_equivalence.txt`, `rev2b_ast_identity.out`, `rev2b_rowcompare.txt`, `rev2b_fixed.out`, `rev2b_prefix_HEAD.out`.

Items, by rev-2 line:
* **(f)** the identity note, after `:9`: "Documentation revision 2b of the rev-2 detector (runtime/scoring unchanged, N = 31); measured as rev 2, md5 d57c12ab".
* **P3** `:33-35`: "(this tree's placement, A6; upstream adds the same include BEFORE m8820x_pte.h -- the position is not load-bearing)".  Verified: memory_m88k.c and dev_m8820x.c include `m8820x.h` first and cpu_m88k.c after, and all three compile clean.  m8820x.h's only use of a pte-header name is inside `#define NBSG`.
* **(a)** `:45`: "(e.g. the debugger's dump: ...)".
* **(e)** P13 `:104-107`: "PRE-TABLE PREDICTIONS (...), subsequently compared with the measured table (27/27, ...SCORES.txt; L22's prediction at BUILDER_QUESTIONS Q18 / BUILD_SPEC section 11 Q18)".
* **(b)** P10 `:152-155` and `:170-172`: labelled "Predicted, source-derived; not measured"; the re-root obligation kept.
* **P6**: a NOT CLAIMED line for a stepped instruction fetch AT 0x3ffffff0.
* **(c)**: "instruction x NULL exception delivery has no scored row; `null surv' scores survival (...)".
* **(d)**: "preservation of another CPU's CMMU registers during a NULL-owning CPU's fault is not scored (`null owner', filed)".
* **F15**: dropped, per section 7.
* The executable `REVISION = 2` is unchanged.

**Equivalence.**
* With the docstring stripped, both files are 28,722 bytes, md5 `62235b1e...`, and `cmp` exits 0.
* Rev-2 lines 221..836 equal rev-2b lines 233..848, line by line.
* The AST holds: 209 top-level statements after the docstring, 0 differing, body-dump md5 `1e8e417a...` in both.  Both files compile with warnings as errors.

**Two runs, row by row.**
* `rev2b_fixed.out` on the work binary `3cd0501c`: 31/31, ABSENT.
* `rev2b_prefix_HEAD.out` on the base binary `2efeec55`: 21/31, PRESENT 10/10, the same ten reds.
* Every one of the 33 row/INFO lines is identical to `fixed.out` and to `prefix_HEAD.out` (name, got, want, note, status), and so are RESULT/CONTROL/SYMPTOM/REVISION/RED, the SCORE line and the sentinel.
* **OVERALL: BOTH COMPARISONS IDENTICAL ROW BY ROW.**

**Code lines moved by +12** (the docstring grew).  `REVISION = 2` is now at `:250`, and the null session's `pause 1`
block is at `:723-727` (rev 2's `:711-715`).  Any citation into the probe's CODE must name its revision.

## 3. Gate comment, staged copies, MANIFEST (section 3 + 7)

* **Gate comment** (`GATE_COMMENT.txt`):
  * `regress/gate_arm.sh` and the staged copy were edited identically and stay byte-identical (`f04fad2c`).
  * Only lines 1917-1925 changed (nine lines -> nine), so `M88KBELOG=` stays at `:1926` and the probe call at `:1927`.
  * The 918 non-comment lines are identical (`cmp` clean), and `bash -n` passes on both copies.
  * New opening sentence: "A CLAIMED, REFUSED, UNSUPPRESSED m88k device access that passes the running-transition check (the device returns 0 with the cpu still running; NO_EXCEPTIONS callers excluded) now records its bus error in the faulting side's CMMU WHEN THE SELECTED CMMU EXISTS (...)".  The LUNA routing sentence and the skip disclosure are kept.
  * Gate 14's receipt names gate `5ee94e61`, probe `d57c12ab` and binary `931e69fa`; it is not re-run.
* **Rename:** `staged/gate_arm.sh` -> `staged/gate_arm.sh.txt`.  `staged/README.txt` says what each staged file is, why the suffix exists, and that `gate_arm.staged.diff`'s `+++` path predates the rename.
* **Provenance addendum:** `table1_20261023/gates/PROVENANCE_20261024.md`.  The raw receipts are not relabelled.  `build/gxemul` rebuilt from the comment-edited sources is still `931e69fa`, so the binary the gates ran is the binary of the shipped sources.
* **MANIFEST** (`MANIFEST_TEXT.txt`; both copies identical in every changed line, and the 16-line `#570` block is byte-identical):
  * it names measured rev 2 `d57c12ab` and the shipped documentation revision 2b `9046d774` (docstring-only re-freeze);
  * "27 of 27 measurements as predicted" is qualified with "(L22's prediction: BUILDER_QUESTIONS Q18 / BUILD_SPEC section 11 Q18)";
  * the `.py.txt` / `.sh.txt` sentence names the staged copies;
  * classifications and denominators are kept, and the witness entry is unchanged.

## 4. Dated notes (section 4 + 7)

* `table1_20261023/PRETABLE_NOTE_20261024.md` records:
  * L22's source, `BUILDER_QUESTIONS.md:135-138` (22:29:30), and its approval, `BUILD_SPEC.md:233-234` (22:31:49), both before the leg (23:08:15 / 23:08:43);
  * the draft -> final question map;
  * AMENDMENT 1's "~22:3x" against the mtime 22:28:08, stated and not reconciled;
  * R-d and AM-7 SUPERSEDED: cpu 0 parks in H's `br .` and stays running, and only `pause 1` is sent (`PRETABLE.out:351-353, 372, 447`; rev 2 `:711-715` = rev 2b `:723-727`);
  * that CL7 establishes DATA delivery only;
  * that "no leg builds 'case deleted'" is superseded by L22.
* `SCORES.txt`:
  * line 4 gains ", plus BUILD_SPEC section 11 Q18 for L22";
  * the dated NOTE line is inserted before the `SCORES_DONE` sentinel;
  * lines 5-143 are byte-identical.

## 5. Propagation and clearance (section 5 + 7) -- `PROPAGATE_*.out`, `prop_*.log`, `CLEARANCE_repair1.out`

| tree | part 1 | part 2 | binary (before = after) | objects identical |
|---|---|---|---|---|
| est/ | CLEAN | N/A (source tree) | -- | -- |
| build/ | CLEAN | FRESH | `931e69fa` | 224/224 |
| build-asan/ | CLEAN | FRESH | `9d0e0680` | 225/225 |
| /tmp/gxsec-build | CLEAN | FRESH | `8d882c05` | 225/225 |
| /tmp/gxt36/work | CLEAN | FRESH | `3cd0501c` | 224/224 |

Every build gave 0 warnings, and there are no sentinels.  None of the four files is in the derived divergence set.

The peer's five files are identical before and after in every tree and in SEC:
* `30c05d15` cpu_alpha_palcode.c
* `e2201bb4` dev_lca.c
* `21f6b135` dev_pcc2.c
* `15d43afd` dev_sh4.c
* `93258626` mvme_pcctworeg.h

## 6. Where this step disagreed with the spec, by id

* **D-1 (section 1 header):** "FOUR files" is inaccurate as an edit list.  B1-B5 touch two files, `memory_rw.c` and `dev_m8820x.c`.  All four were propagated and cleared.
* **D-2 (B2's grep):** the literal grep returns 3 (prose), not 0.  The token form returns 0, and object identity was measured.
* **D-3 (B2/B5/B3 wrap):** no unflagged word could be dropped and still keep the line counts, so the comments were widened instead.
  * `memory_rw.c`'s comment now reaches 97 display columns (it was 85; HEAD's file maximum is 107).
  * B3's block stays within its existing 104.
  * B3 also compresses the historical scancode note.  It drops the old "-- no longer dev_luna88k.c" clause; dev_luna88k.c's own case comment records the deleted write.
* **D-4 (B2 punctuation):** I kept REPAIR_SPEC section 1's colon, so only the parenthetical changed.  PASS2_RULINGS and Astra print a semicolon.
* **D-5 (beyond the list, D3's sibling, CLAUDE.md mechanical rule 2):** the probe's first docstring sentence and the MANIFEST comment carried the same categorical "a refused m88k device access records its bus error" claim that D3 corrected in the gate.  Both gained D3's two conditions ("CLAIMED, REFUSED, unsuppressed ... when that CMMU exists").
  * For the probe this made an intermediate rev 2b, `fe8cc784`.
  * Its receipts, which also matched row by row, are kept in `superseded_fe8cc784/`.
  * The final rev 2b is `9046d774`.
* **D-6 (section 2):** the probe's code lines moved +12, so "`REVISION = 2` at `:238`" is a rev-2 locator; the statement itself is unchanged.  I placed `rev2b.docstring.diff` in `repair1_20261024/` as REPAIR_SPEC section 2 says; PASS2_RULINGS D2 and Astra name `table1_20261023/`.  It was not duplicated.
* **D-7 (section 3 wording):** section 7's sentence is used.  Section 3's separate "(a CMMU-less cpu gets no write)" is subsumed by "WHEN THE SELECTED CMMU EXISTS" and was not added; the block still names the CMMU-less rows.  The gate comment is wrapped at up to 122 columns to keep nine lines; gate_arm.sh already has comment lines of 129 and 158 columns.
* **D-8 (section sign):** I wrote "section 11" for "§11" in SCORES.txt, the MANIFEST and the probe, because all three files are ASCII.
* **D-9 (PRETABLE map):** body `:329` "Q10" is not in the spec's map.  It has no final counterpart, and the note says so.
* **D-10 (outside #570, blocks the landing commit):** the simulated probe-wiring check now FAILS on both checker copies.  The `#570` entries are still wired: the detector is run by `gate_arm.sh:1927` and the witness is not run (correct).
  * The cause is the peer's `lca_badval_probe.py` exemption.  It came due 2026-10-23 and has now expired; the BUILD step's identical run on 2026-10-23 passed.
  * The working-tree copy also has five GHOST entries.  They are the peer's uncommitted MANIFEST lines.
  * Neither is #570's to change.

## 7. ADDENDUM 2026-10-24 -- documentation revision 2c (the coordinator's follow-up for precommit section U)

**Why.**  Section U (`tools/pipeline/check_score_claims.py`, run from GXEMUL-SEC) returned `SCORE_CLAIMS_FAIL` on rev 2b's
docstring: four score-shaped `N/M` strings whose `M` is not the gate pin 31.
* `27/27` at `:110`: the P13 sentence that rev 2b added.
* `46010/0` twice at `:127`: the address list "0xfff46010 / 0xfff46010 / 0xfff40090".
* `10/10` at `:224`: the quoted marker "PRESENT 10/10".

The second and third groups were already in rev 2 (its `:122` and `:212`).  Section U reads only `regress/<stem>_probe.py`,
so no simulation before the shipped copy existed could have shown them.  Both outputs are in `SCORE_CLAIMS_rev2c.txt`.

**The four edits** (docstring only, exactly once each).  The line count is kept at 848, so every code line keeps its rev-2b
number: `REVISION = 2` at `:250`, the null session's `pause 1` block at `:723-727`.
* **`:11-12`**: "Documentation revision 2b" -> "Documentation revision 2c", and "2b: header sentences only" -> "2b, 2c: header text only".  The identity note would otherwise be a wrong record in the 2c file.
* **`:110-112`**: "(27/27, ..." -> "(27 of 27 measurements, ...", re-wrapped in place within the same three lines.
* **`:127`**: "at 0xfff46010 / 0xfff46010 / 0xfff40090" -> "at 0xfff46010, 0xfff46010 and 0xfff40090".
* **`:224`**: "the ten symptom rows are red (M88K_BUSERR_SYMPTOM=PRESENT 10/10)" -> "the 10-row symptom set is red (M88K_BUSERR_SYMPTOM=PRESENT 10/10)".  The quoted marker is kept, and the checker's own escape now sits on the same line.

**Rev 2c: md5 `a49f417d37484071143de7e13637f4a4`** (848 lines).

**Section U now passes**: `SCORE_CLAIMS_PASS  38 gate comment set(s) checked; 16 of 38 stems also have a probe docstring
checked` (with `SCORE_CLAIMS_PINNED=38`).

**Nothing else trips** (`scan_trips.py`, which imports the checker's own `SCORE` regex):
* The `#570` gate comment has one match, `16/24` at `:1921`.  That is the witness's own 24-row score, and the line does not name the stem, so the checker does not read it.
* Both `#570` MANIFEST blocks match `21/31`, `31/31`, `1/31`, `16/24` and `24/24`.  The checker does not read check_probe_wiring.py at all.
* `TRIPS_TOTAL=0`.
* The wiring simulation is unchanged: `#570` is wired in both copies, and the only failures are the two pre-existing non-#570 causes.

**The rev-2b verification, re-run for 2c.**  `rev2c_verify.py` is `rev2b_verify.py` with only its output names and labels renamed.
* **Strip and compare** against the frozen rev 2 (`rev2c_equivalence.txt`): IDENTICAL, 28,722 bytes, md5 `62235b1e...`, `cmp` exit 0.  Rev-2 lines 221..836 equal rev-2c lines 233..848.
* **AST** (`rev2c_ast_identity.out`): holds.  209 statements, 0 differ, body-dump md5 `1e8e417a...`; `REVISION = 2` at `:250`; both compile with warnings as errors.
* **Reruns, row by row** (`rev2c_rowcompare.txt`).  Every row/INFO line, marker, SCORE line and sentinel is identical: **OVERALL: BOTH COMPARISONS IDENTICAL ROW BY ROW**.
  * `rev2c_fixed.out` on `/tmp/gxt36/work/gxemul` (`3cd0501c`): 31/31, ABSENT.
  * `rev2c_prefix_HEAD.out` on `/tmp/gxt36/base/gxemul` (`2efeec55`): 21/31, PRESENT 10/10, the same ten reds.
* **Docstring diffs:**
  * `rev2c.docstring.diff` (2b -> 2c): four hunks, seven lines each side, all inside the docstring.  2b and 2c are identical outside the docstring, and the line count is unchanged (`rev2c_vs_2b.txt`).
  * `rev2_to_2c.docstring.diff`: the cumulative diff from rev 2 to 2c.

**MANIFEST, both copies, identical edit** (`MANIFEST_TEXT_rev2c.txt`): "shipped as documentation revision 2b (md5 9046d774, a
docstring-only re-freeze: repair1_20261024/rev2b_equivalence.txt)" -> "... revision 2c (md5 a49f417d, ...
repair1_20261024/rev2c_equivalence.txt)".
* Working tree `7e5beb5d` -> `8d46fdf5ca2c1cc6d37239d9c5ecc807`.
* Staged copy `88739fcb` -> `9386fe2558eff6a2c4716bfd968d413a`.
* The 16-line `#570` block is byte-identical across the two copies.

**Superseded.**  Rev 2b's eight receipts moved to `superseded_9046d774/`, with a README, as `superseded_fe8cc784/` was done.
Sections 0-3 above describe rev 2b and stand as the record of that revision; this section supersedes them for the shipped file.

**D-11.**  "27 of 27 **measurements**", not the suggested "legs".  SCORES.txt:141 reads "SUMMARY: 27 measurements MATCH",
and the 27 include `pre`, `fix` and `L1`, which are not variant legs.  "legs" would change the meaning; "measurements" also
matches the MANIFEST's wording.

**D-12, NOT EDITED ("no other file changes") -- each now names rev 2b or older as shipped, or points at a moved receipt.
Proposed one-line corrections, for the coordinator to apply or authorize:**
* **`table1_20261023/gates/PROVENANCE_20261024.md:21`** names `9046d774 (documentation revision 2b)` and cites `rev2b_equivalence.txt` and `rev2b_ast_identity.out`.  `:32` cites `rev2b_rowcompare.txt`.  All three files now live in `superseded_9046d774/`.  Proposed: name `a49f417d37484071143de7e13637f4a4 (documentation revision 2c)` and the `rev2c_*` files.
* **`repair1_20261024/GATE_COMMENT.txt:18-20`** names "documentation revision 2b of the probe (fe8cc784)" and points at `repair1_20261024/rev2b_equivalence.txt`.  Proposed: name `a49f417d` (revision 2c) and `rev2c_equivalence.txt`.
* **`table1_20261023/PRETABLE_NOTE_20261024.md:45`** ("shipped documentation revision 2b") and **`:56`** ("(documentation revision 2b)").  Proposed: "2c".  The cited lines `:723-727` / `:726` are unchanged in 2c.
* **`repair1_20261024/superseded_fe8cc784/README.txt:3`** ("SUPERSEDED by the shipped rev 2b (md5 9046d774...)").  Proposed: "by rev 2b (9046d774), itself superseded by rev 2c (a49f417d)".
* `MANIFEST_TEXT.txt` is the receipt of the first MANIFEST edit and was true when written; `MANIFEST_TEXT_rev2c.txt` records the second.

**D-13, landing obligation, NOT EDITED.**  `check_score_claims.py` now prints `SCORE_CLAIMS_PINNED=38`, and `tools/precommit_check.sh`
carries `SCORE_CLAIMS_MANIFEST=37`.  The new pin is #570's own `check "m88k_buserr rows run" ... 31` (gate_arm.sh:1934).  So
section U reports "SCORE-CLAIM COVERAGE GREW" until the landing commit raises the manifest 37 -> 38, with a dated line
beside the #566/#567/#568 precedents.

### 7a. D-12 APPLIED, 2026-10-24 -- on the coordinator's authorisation

The four notes now name the probe revisions consistently: revision 2c (`a49f417d`) as SHIPPED, revision 2b (`9046d774`)
as SUPERSEDED (`superseded_9046d774/`), and `fe8cc784` as the INTERMEDIATE (`superseded_fe8cc784/`).  Each pointer to a moved
rev-2b receipt now names the `rev2c_*` receipt.  The edits were exactly-once replacements (scratchpad `t36/repair/apply_d12.py`;
pre-edit copies in `t36/repair/pre/d12/`), and every file is LF.

| file | lines before -> after |
|---|---|
| `table1_20261023/gates/PROVENANCE_20261024.md` | 37 -> 38 |
| `repair1_20261024/GATE_COMMENT.txt` | 49 -> 50 |
| `table1_20261023/PRETABLE_NOTE_20261024.md` | 61 -> 61 |
| `repair1_20261024/superseded_fe8cc784/README.txt` | 4 -> 5 |

Two files still mention rev 2b, both deliberately and both outside the four:
* `MANIFEST_TEXT.txt`, the dated receipt of the first MANIFEST edit, which was true when written.  `MANIFEST_TEXT_rev2c.txt` records the second edit.
* `SCORE_CLAIMS_rev2c.txt`'s BEFORE header, which correctly says the failing run was against rev 2b.

D-13 (`SCORE_CLAIMS_MANIFEST` 37 -> 38 in `tools/precommit_check.sh`) belongs to the coordinator, at landing.  This step did
not write that file.  The coordinator's own edit is already in the working tree (mtime 04:50:21, "RAISED 37 -> 38 ON
2026-10-24").

The four diffs:

```diff
--- a/table1_20261023/gates/PROVENANCE_20261024.md
+++ b/table1_20261023/gates/PROVENANCE_20261024.md
@@ -18,7 +18,7 @@
 | file | at the gate run | shipped | relation, and where it is shown |
 |---|---|---|---|
 | `regress/gate_arm.sh` | `5ee94e61` | `f04fad2c589f9eb10f4a4fc3dc5896d9` | the `#570` block's opening comment only (lines 1917-1925, nine lines kept); every non-comment line identical (`../../repair1_20261024/GATE_COMMENT.txt`) |
-| `regress/m88k_buserr_probe.py` | `d57c12ab` (rev 2) | `9046d77432e0e6438c93732ec0cc9827` (documentation revision 2b) | docstring only: everything outside the module docstring byte-identical, AST identical, `REVISION = 2` unchanged (`../../repair1_20261024/rev2b_equivalence.txt`, `rev2b_ast_identity.out`) |
+| `regress/m88k_buserr_probe.py` | `d57c12ab` (rev 2) | `a49f417d37484071143de7e13637f4a4` (documentation revision 2c) | docstring only: everything outside the module docstring byte-identical, AST identical, `REVISION = 2` unchanged (`../../repair1_20261024/rev2c_equivalence.txt`, `rev2c_ast_identity.out`).  Revision 2b (`9046d774`) is superseded, its receipts in `../../repair1_20261024/superseded_9046d774/`; `fe8cc784` was the intermediate (`superseded_fe8cc784/`) |
 | `src/cpus/memory_rw.c` | `b36c9e13` | `4b71687469a8b38165f038d3e9171293` | the `#570` comment only (B2, B5), 13 lines kept (`../../repair1_20261024/product_comments.diff`, `LINE_CHECK.txt`) |
 | `src/devices/dev_m8820x.c` | `c229294f` | `bd616d06d7a2a4da388429ca326c4a5e` | comments only (B1, B3, B4), 551 lines kept |
 | `src/cpus/cpu_m88k.c`, `src/devices/dev_luna88k.c` | `0321e2ba`, `e43c39ca` | unchanged | -- |
@@ -27,9 +27,10 @@
 `build/gxemul` md5 `931e69fa...` again, with all 224 objects and the binary identical before and after
 (`../../repair1_20261024/PROPAGATE_build.out`).  So the binary these receipts ran is the binary of the shipped sources.
 
-**Rev 2b's own receipts.**  Rev 2b was run once on the fixed work binary (`3cd0501c`, 31/31, SYMPTOM=ABSENT) and once on
+**Rev 2c's own receipts.**  Rev 2c was run once on the fixed work binary (`3cd0501c`, 31/31, SYMPTOM=ABSENT) and once on
 the HEAD binary (`2efeec55`, 21/31, SYMPTOM=PRESENT 10/10).  Every row, marker and sentinel matches rev 2's
-`../fixed.out` and `../prefix_HEAD.out` (`../../repair1_20261024/rev2b_rowcompare.txt`).
+`../fixed.out` and `../prefix_HEAD.out` (`../../repair1_20261024/rev2c_rowcompare.txt`).  Revision 2b's receipts,
+which matched the same way, are kept in `../../repair1_20261024/superseded_9046d774/`.
 
 **The caveat, from the adjudication (GPT-6 Astra, F2), kept verbatim:** "The two reruns alone do not demonstrate every
 old mutation result or make the old gate receipt a rev-2b measurement; the verified documentation-only relationship
--- a/repair1_20261024/GATE_COMMENT.txt
+++ b/repair1_20261024/GATE_COMMENT.txt
@@ -15,9 +15,10 @@
     regress/gate_arm.sh md5 5ee94e61a100473ba95db05f43f34a96; m88k_buserr_probe.py md5 d57c12ab7ade903946c7d80a8e153ab7
   i.e. gate 14 ran gate_arm.sh 5ee94e61 (the pre-edit file), probe d57c12ab (rev 2), binary build/gxemul 931e69fa;
   its PASS (1310 checks, wall 7974 s) is a receipt for THOSE bytes.  The comment-edited gate (above) and the shipped
-  documentation revision 2b of the probe (fe8cc784) differ from them in comment/docstring text only: the gate's
+  documentation revision 2c of the probe (a49f417d; revision 2b, 9046d774, is superseded -- superseded_9046d774/ -- and
+  fe8cc784 was the intermediate -- superseded_fe8cc784/) differ from them in comment/docstring text only: the gate's
   non-comment lines are identical (above) and the probe's outside-docstring bytes are identical
-  (repair1_20261024/rev2b_equivalence.txt).  The raw receipt is not relabelled; see table1_20261023/gates/PROVENANCE_20261024.md.
+  (repair1_20261024/rev2c_equivalence.txt).  The raw receipt is not relabelled; see table1_20261023/gates/PROVENANCE_20261024.md.
 
 == the comment diff (unified) ==
 --- a/regress/gate_arm.sh
--- a/table1_20261023/PRETABLE_NOTE_20261024.md
+++ b/table1_20261023/PRETABLE_NOTE_20261024.md
@@ -42,7 +42,7 @@
 The probe as built does not pause cpu 0.  cpu 0 runs its 19 steps and parks in H's `br .`, where it **remains running**,
 as AM-1 itself says at `:372`.  The session sends `pause 1`, which starts cpu 1, and **never** `pause 0`.  See rev 2,
 the frozen artifact of record, at `m88k_buserr_probe.rev2.frozen.py.txt:711-715` (the `pause 1` is at `:714`).  In the
-shipped documentation revision 2b the same lines are `regress/m88k_buserr_probe.py:723-727` (`:726`).
+shipped documentation revision 2c the same lines are `regress/m88k_buserr_probe.py:723-727` (`:726`).
 
 ## 5. CL7 establishes data delivery only
 
@@ -53,7 +53,7 @@
 fetch, not the vector taken.  The INFO null cpu0 line prints cpu 1's end pc, unscored.
 
 The product comment was narrowed to match (`memory_rw.c`'s `#570` comment, B5, in `../repair1_20261024/product_comments.diff`),
-and the probe's contract now says so (documentation revision 2b).
+and the probe's contract now says so (documentation revision 2c).
 
 ## 6. "No leg in the table builds 'case deleted'" is superseded by L22
 
--- a/repair1_20261024/superseded_fe8cc784/README.txt
+++ b/repair1_20261024/superseded_fe8cc784/README.txt
@@ -1,4 +1,5 @@
 T36 / #570 REPAIR step, 2026-10-24 ~03:53-04:00: receipts of an INTERMEDIATE documentation revision 2b (md5
 fe8cc784fa339d73b40d6c7e4afa5697), made before the D3-sibling title qualifier was added to the probe's first sentence
-(scratchpad t36/repair/apply_rev2b_title.py).  SUPERSEDED by the shipped rev 2b (md5 9046d774...; repair1_20261024/).
+(scratchpad t36/repair/apply_rev2b_title.py).  SUPERSEDED by rev 2b (md5 9046d774...; repair1_20261024/superseded_9046d774/),
+itself superseded by the shipped documentation revision 2c (md5 a49f417d...; repair1_20261024/rev2c_*).
 Kept, not cited: every row, marker and sentinel matched the rev-2 receipts here too (rev2b_rowcompare.txt).
```
