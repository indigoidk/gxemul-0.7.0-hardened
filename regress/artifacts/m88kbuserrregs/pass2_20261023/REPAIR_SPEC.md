# T36 / #570 -- the PRE-COMMIT REPAIR spec for the builder (main loop, 2026-10-24; DRAFT pending section E of PASS2_RULINGS.md)

Every item below is a pointer into `PASS2_RULINGS.md` (B1-B5, D2-D5, D10) and the pass-2 seat answers.  Record OUTPUT,
never assertion.  The ground rules of `../pass1_20261023/BUILD_SPEC.md` section 0 are unchanged (git object reads only;
never git add/commit/status/diff; the peer's files untouched; WSL Gentoo builds; foreground only; LF preserved; helper
scripts in the session scratchpad `t36/repair/`; if a response is classifier-stopped, stop and report).  Artifacts dir for
this step: `regress/artifacts/m88kbuserrregs/repair1_20261024/` (create it).  Section 7 carries GPT-6 Astra's F2
amendments; where it names an item, it overrides.

## 1. Product comments -- FOUR files, comment-only, line counts UNCHANGED, est/ mirrored, object compare redone
* **B1** `src/devices/dev_m8820x.c:361`: `(cpu_m88k.c:354-355)` -> `(cpu_m88k.c:358-359)` (same width).
* **B2** `src/cpus/memory_rw.c:625-627`: the parenthetical "(the debugger)" -> "(e.g. the debugger's dump)" and the sentence
  kept true: "NO_EXCEPTIONS callers (e.g. the debugger's dump) never get here: the test above keeps them out."  Keep the
  line count of the comment block (re-wrap within the same number of lines); `memory_rw.c` embeds no `__LINE__` (grep
  `assert\|FAILURE\|CHECK_ALLOCATION` = 0 -- verify and record).
* **B3** `src/devices/dev_m8820x.c:326-333`: scope "~10^5 times per boot" to `memory_m88k.c:382-405`'s translation-fault
  writer; name `memory_rw.c`'s arm without a number ("the arm's per-boot count is unmeasured"); same line count.
* **B4** `src/devices/dev_m8820x.c:293-295`: "the model writes only PFSR and PFAR" -> "the model's FAULT PATHS write only
  PFSR and PFAR" (IDR is initialised at `dev_mvme187.c:139,151` / `dev_luna88k.c:953,964`); same line count.
* **B5** `src/cpus/memory_rw.c:623-625`: "A cpu without a CMMU gets no write and still takes the exception." -> "A cpu
  without a CMMU gets no write; the exception call below is unchanged (the data-access delivery is scored by the
  detector's `null route`; the instruction label's delivery on a CMMU-less cpu is survival-only, not rowed)." -- re-wrapped
  within the comment's existing line budget (add no lines; drop filler words if needed).
* After the edits: `cmp` each file against its `est/` twin after copying; rebuild `/tmp/gxt36/work` (`rm src/cpus/*.o;
  make`), 0 warnings, FRESH; `md5sum` of `dev_m8820x.o`, `cpu_m88k.o`, `dev_luna88k.o` and `gxemul` before and after --
  `dev_m8820x.o` MUST be byte-identical (`repair1_20261024/objmd5_before.txt` / `_after.txt`); `cpu_m88k.o` changes only
  if `memory_rw.c`'s comment edit changed a `__LINE__`-bearing line (it must not -- record the check); run the shipped
  detector once on the rebuilt work binary (31/31) -> `repair1_20261024/fixed_after_comments.out`.

## 2. The shipped detector's docstring -- ONE re-freeze (rev 2b), the frozen rev-2 artifact UNTOUCHED
Edit `regress/m88k_buserr_probe.py`'s header ONLY (no code line changes; `python -c "import ast"` AST-identity of the
module body against `table1_20261023/m88k_buserr_probe.rev2.frozen.py.txt` must hold -- record the check as
`repair1_20261024/rev2b_ast_identity.out`, the `#568` precedent):
* **P3** `:33-34`: delete "(upstream's placement, the transferred warrant)"; say "after m8820x_pte.h (this tree's
  placement, A6; upstream adds the same include BEFORE m8820x_pte.h -- the position is not load-bearing)".
* **P10** `:171-172`: prefix "PREDICTED (source-derived, unmeasured): with R2 fixed the step's own fetch
  (cpu_m88k_instr.c:2989-2990, CACHE_INSTRUCTION, no NO_EXCEPTIONS) reaches the same arm ... (R1's halt)".
* **P6** the NOT CLAIMED list: add "a stepped instruction fetch AT 0x3ffffff0 (LUNA dispatch x instruction label --
  clause (e); HEAD's case wrote cmmu[1]'s PFSR for any access class and served it; the fix deletes that write)".
* **F15** the CHANNEL text of `ok route` / `ok regs`: name the operative channel under a global widening -- the
  prerequisite strings (`prereq:nodev` / `prereq:readback`) -- as the measured L18/L19 reds show.
* **P13** `:105-106`: "DATED PREDICTIONS ... UNTIL THE TABLE RUNS" -> "DATED PREDICTIONS (written before the table); the
  table ran 2026-10-23 and matched 27/27 -- table1_20261023/SCORES.txt".
* **B5's no-row sentence** also in the header's contract: "instruction x NULL exception DELIVERY is not scored (survival
  and the data label's delivery are); the INFO null cpu0 line prints cpu 1's end pc".
Then: md5 of the new file (rev 2b); run it on `/tmp/gxt36/work/gxemul` (31/31 ABSENT) and on `/tmp/gxt36/base/gxemul`
(21/31 PRESENT 10/10, the same ten reds) -> `repair1_20261024/rev2b_fixed.out`, `rev2b_prefix_HEAD.out`; the docstring
diff rev2 -> rev2b as `repair1_20261024/rev2b.docstring.diff`.  The MANIFEST line names rev 2b's md5 beside rev 2's.

## 3. The gate comment (D3) and the MANIFEST sentence (D4)
* `regress/gate_arm.sh`'s `#570` block comment: add "unsuppressed (NO_EXCEPTIONS callers excluded)" and "when the faulting
  side's CMMU exists (a CMMU-less cpu gets no write)" to the opening sentence -- in the WORKING-TREE file and in
  `table1_20261023/staged/gate_arm.sh` IDENTICALLY (diff the two insertions; the two files must stay byte-identical).
  Record in `repair1_20261024/GATE_COMMENT.txt` that gate 14's run (`gates/gate14_run.out`) used the pre-edit file md5
  `5ee94e61...` and that a comment edit does not re-run the gate.
* Rename `table1_20261023/staged/gate_arm.sh` -> `gate_arm.sh.txt` (after the edit) and write `staged/README.txt`: what
  each staged copy is, why the `.txt` suffix, that `gate_arm.staged.diff`'s `+++` path text predates the rename.
* `tools/pipeline/check_probe_wiring.py` (working tree AND `staged/check_probe_wiring.py.txt`, identically): the
  detector line's "27 of 27 measurements as predicted" -> "27 of 27 measurements as predicted (L22's prediction at
  BUILD_SPEC section 11 Q18, dated before the leg)"; the sentence about `*.py.txt` / `*.sh.txt` becomes true after the
  rename; name BOTH probe md5s (rev 2 measured `d57c12ab`, rev 2b shipped <new>) with "docstring-only re-freeze".

## 4. Dated notes beside the measured artifacts (never edit PRETABLE.out or SCORES.txt's measured lines)
* `table1_20261023/PRETABLE_NOTE_20261024.md`: L22's prediction lives at BUILDER_QUESTIONS Q18 / BUILD_SPEC section 11
  Q18 (mtimes 22:29:30 / 22:31:49, before the 23:08 leg); the draft-question-id map (PRETABLE body Q5-Q9, AM-4
  [Q12]/[Q13], AM-5 [Q7] -> final Q13, Q18, Q16, Q17, Q14, Q8); AMENDMENT 1's self-stated "~22:3x" vs the file mtime
  22:28:08; `R-d`'s "pauses cpu 0" vs the probe's parked `br .` loop (Argon F5.2); PRETABLE section 2's "no leg builds
  'case deleted'" superseded by L22.
* `SCORES.txt`: APPEND one dated line: "NOTE 2026-10-24: the SYMPTOM column is cut at 60 characters by mk_scores570; the
  leg .out files carry the full M88K_BUSERR_SYMPTOM line."  (Do not regenerate the measured lines.)

## 5. Clearance and propagation
Propagate the four comment-edited product files to est/, build/, build-asan/, /tmp/gxsec-build; rebuild the three build
trees (`rm src/cpus/*.o; make`, foreground, one at a time); `CLEARANCE_repair1.out` with both parts per tree (`est/:
source tree, part 2 N/A`); the peer's five dirty files in build/ untouched (md5 before/after).

## 6. Report -- `repair1_20261024/REPAIR_REPORT.md`, then STOP
Every edit by file:line (old -> new), the line-count proof per file, the object md5s, the AST-identity check, rev 2b's two
runs, the gate-comment diff, the rename, the notes written, the clearance; anything that disagreed with this spec (by id).

## 7. AMENDMENTS from GPT-6 Astra's F2 adjudication (`f2/codex_t36f2.txt`, VERDICT AMEND; PASS2_RULINGS.md section E)
## -- these OVERRIDE the sections they name
* **§1 B5 -- use this wording** (re-wrapped within the comment's line budget): "For a CPU without a CMMU, this arm makes
  no register write; the exception call is unchanged.  `null route` scores data-access delivery; instruction-access
  delivery is unscored (`null surv` scores survival only)."  Never call the delivery itself "survival-only".
* **§1 B3 -- form:** scope the historical "~10^5 times per boot" explicitly to `memory_m88k.c:382-405`'s translation-fault
  writer; state that the `#570` refused-device arm also writes directly without a purge but its frequency was not
  measured; keep the historical provenance; present NO combined count.
* **§1 -- after the final re-wrap, re-grep every same-file citation** in the four files (the citation-form rule); the
  est/ twin is the SIBLING tree `C:\DocumentNoSnc\CC\GXEMUL\est\src\...` (not under GXEMUL-SEC).
* **§2 -- the docstring list is CORRECTED:** DROP the F15 item (the prerequisite channels are already explicit at `:118`;
  leave `:118-121` as they are).  ADD: (a) `:45` "(the debugger)" -> "(e.g. the debugger's dump)"; (b) P10 at BOTH
  `:152-155` and `:170-172`, labelled "predicted, source-derived; not measured", the re-root obligation kept; (c) the
  CONTRACT sentence "instruction x NULL exception delivery has no scored row; `null surv` scores survival"; (d) the
  CONTRACT sentence "preservation of another CPU's CMMU registers during a NULL-owning CPU's fault is not scored
  (`null owner`, filed)"; (e) P13 at `:104-106` -> "pre-table predictions, subsequently compared with the measured table
  (27/27, SCORES.txt; L22's prediction at BUILDER_QUESTIONS Q18 / BUILD_SPEC §11 Q18)"; (f) a one-line identity note:
  "documentation revision 2b of the rev-2 detector (runtime/scoring unchanged, N = 31); measured as rev 2, md5 d57c12ab".
  The executable `REVISION = 2` at `:238` MUST stay unchanged.  The two rev-2b receipts are compared ROW BY ROW against
  `fixed.out` and `prefix_HEAD.out` (every row's name and status identical, the CONTROL/SYMPTOM/sentinel lines
  identical) -> `repair1_20261024/rev2b_rowcompare.txt`; the AST/docstring-only verification -> `rev2b_equivalence.txt`
  (the module body outside the docstring byte-identical: show it by stripping the docstring from both files and `cmp`).
* **§3 -- gate prose wording:** the opening sentence says that "a CLAIMED, REFUSED, UNSUPPRESSED access that passes the
  running-transition check records its bus error in the faulting side's CMMU WHEN THE SELECTED CMMU EXISTS"; keep the
  LUNA routing sentence and the skip disclosure; executable gate text unchanged; record the new gate md5 and that the
  historical run used `5ee94e61`.  A dated `table1_20261023/gates/PROVENANCE_20261024.md` says the gate receipt names
  binary `931e69fa`, gate `5ee94e61`, probe `d57c12ab`, and that the shipped files are the comment-edited gate and the
  documentation revision 2b (identities listed) -- the raw receipt is NOT relabelled.
* **§3 MANIFEST text:** distinguish "measured rev 2 (md5 d57c12ab)" from "shipped documentation revision 2b (md5 <new>)";
  qualify "27 of 27 measurements as predicted (L22's prediction: BUILDER_QUESTIONS Q18 / BUILD_SPEC §11 Q18)"; keep the
  classifications and denominators.
* **§4 PRETABLE note -- add explicitly:** R-d's "pauses cpu 0 before cpu 1 runs" and AM-7's "R-d stands" are SUPERSEDED
  -- cpu 0 parks in `H`'s `br .` and remains running; the probe sends `pause 1`, never `pause 0` (`PRETABLE.out:351-353,
  372, 447`; probe `:711-715`); CL7's `null route` mapping establishes DATA delivery only (instruction delivery
  unscored); L22's source `BUILDER_QUESTIONS.md:135-138` approved at `BUILD_SPEC.md:233-234`; the question-id map as
  listed in REPAIR_SPEC §4; AMENDMENT 1's self-date vs mtime stated, not reconciled.
* **§4 SCORES.txt:** ALSO amend line 4's criterion sentence itself -- append ", plus BUILD_SPEC §11 Q18 for L22" -- beside
  the appended truncation notice; measured scores and red sets untouched.
* **§5 -- "old freshness receipts cannot certify newly copied sources":** the clearance is re-run AFTER the propagation of
  the comment-edited files (both parts, all three build trees; est/ N/A).
* **No further mutation leg, boot pair or full gate is required**, provided the documented code equivalence (rev 2b) and
  the object identity (`dev_m8820x.o`) hold; the probe reruns, the object comparison and the clearance are required.
* **Citation census for the records (not for you to edit):** EIGHT shifted sites (`diff_m8820x.c:996`;
  `diff_m8invread.c:161,643`; `luna_intmask_probe.py:2,23`; `m8820x_sites_probe.py:23,27`; `readiness_predicate_test.py:70`)
  and `repro_m8sarpurge.c:14` (names the removed LUNA PFSR writer) -- all FILED, none swept.
