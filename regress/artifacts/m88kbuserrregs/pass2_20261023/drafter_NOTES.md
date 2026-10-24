# NOTES -- #570 / `m88kbuserrregs` pass-2 brief: inconsistencies found while drafting

Drafted 2026-10-24 against HEAD `7fca7187` plus the round's uncommitted edits (working tree, read only).  Every line
below was read at drafting time.  Paths are relative to `GXEMUL-SEC/`.  `A/` = `regress/artifacts/m88kbuserrregs/`,
`T/` = `A/table1_20261023/`, probe = `regress/m88k_buserr_probe.py` (rev 2, md5 `d57c12ab`, 836 lines).

Each item gives WHERE, WHAT disagrees with what, and a DISPOSITION.  Nothing else: no variant, no recipe.  "Pn" is the
brief's section-6 doubt that carries the item to the panel.  "Records-only" means there is nothing for the panel to
rule; the main loop fixes it in its own write-up.  Items are ordered by consequence.

---

## N1 (P15) -- the product comment claims exception delivery for a CMMU-less instruction refusal; no scored row observes it

* **Claim:** `src/cpus/memory_rw.c`:623-625 says "A cpu without a CMMU gets no write and still takes the exception."
  The sentence covers both access labels.
* **Claim-to-row map:** `T/PRETABLE.out`:98-99.  CL6 "no write" maps to `null surv`.  CL7 "still takes the exception"
  maps to `null route`.
* **The rows:**
  * `null route` reads part 1 only, the DATA refusal (probe :173-174).
  * `null surv` (probe :767-780) wants `exit0/readable`.  Its prerequisites require only that cpu 1 is OFF J after part
    2.  No exception being taken also satisfies that.
  * Where cpu 1 ends is printed only by the unscored INFO line (probe :787-788).
* **The evidence:**
  * `T/fixed.out`:35 and `T/prefix_HEAD.out`:35 both print `cpu1 end pc=0x30050` (ERROR vector).
  * `T/L9_excinnull.out`:33,35 and `T/L17_excdrop.out`:33,35 both print `null surv ... ok` with
    `cpu1 end pc=0xfff46010` (no exception taken).
  * In both of those legs, only `null route` reds, and it reds for the DATA part.
* **The ruling:** `A/pass1_20261023/PASS1_RULINGS.md`:225-235 (E, B5c).  Line :233-234 reads: "A survival control with a
  real channel discharges the floor obligation".
  * So by E's own wording, the floor CELL is discharged.
  * The CLAIM -> ROW obligation for the comment's instruction label is addressed by neither E nor PRETABLE
    (`tools/CLAUDE.md`:1725).
  * The probe header (:162) and AM-2 (`T/PRETABLE.out`:393-399) match E.  Only the comment's sentence goes beyond the
    rows.
* **DISPOSITION:** carried to the panel (P15; also Q1(c) [M6], Q2(d), Q2(g)).
  * If the panel rules it a CLAIM -> ROW gap, the round owes one of two things before commit: a scored row for delivery
    in that cell, or an explicit no-row sentence in the header's NOT CLAIMED list and in the CHANGELOG.  Both are
    pre-ship construction (L1), and both touch the frozen instrument (see "Coupling" at the end).
  * If the panel rules E covers it, the CHANGELOG quotes E's sentence.  That makes "not rowed, by ruling" visible beside
    the comment's claim.

## N2 (P3) -- a false rationale for the include's position, in the probe header and in BUILD_SPEC

* **Where:**
  * Probe :33-34: "#include "thirdparty/m8820x.h" after m8820x_pte.h (upstream's placement, the transferred warrant)".
  * `A/pass1_20261023/BUILD_SPEC.md`:186 (section 5.1): "the include goes after `m8820x_pte.h` because that is
    upstream's placement".  Line :106 directs the position.
* **The source:** `regress/artifacts/research_20261022/trunk_src.diff`:1921-1922.  Upstream adds the include BEFORE
  `m8820x_pte.h`.
* **What is already correct:**
  * The product comment (`src/cpus/cpu_m88k.c`:54-56) claims only "upstream adds the same include to this file", which
    is true.
  * The builder disclosed the mismatch as departure 1 (`T/BUILD_REPORT.md`:100-104).
  * E's A6 (`PASS1_RULINGS.md`:213-215) upheld the placement and withdrew a DIFFERENT rationale ("order matters").  It
    did not withdraw this one.
* **DISPOSITION:** L4 in the detector header.  Correct it before commit (P3; Q1(b)).
  * BUILD_SPEC section 5.1 is a dated pass-1 artifact.  Either correct it in place with the refuted text quoted, or
    correct it only in the CHANGELOG block (Q3(a) already asks for the include's rationale).
  * Because the header is part of the frozen instrument, the fix triggers the Coupling note.

## N3 (P2) -- this diff makes a citation stale, in a file the same diff edits to fix citations

* **The stale citation:** `src/devices/dev_m8820x.c`:361 reads "(cpu_m88k.c:354-355)".
  * At HEAD those lines are the `for (cmmu_nr = 0; ...)` loop over `cpu->cd.m88k.cmmu[cmmu_nr]`.
  * After the four lines this diff adds above them, the loop is at `src/cpus/cpu_m88k.c`:358-359.
  * The same diff corrects this file's citations at four other sites (:293-295, :325-333, :451-455, :498-502), but not
    this one.
* **Five tracked regress comments shift by the same four lines.**  Each matched HEAD:

  | file:line | cites `cpu_m88k.c` | now at |
  |---|---|---|
  | `regress/diff_m8820x.c`:996 | :362-375 | 366-379 |
  | `regress/diff_m8invread.c`:161 | :121-122 | 125-126 |
  | `regress/luna_intmask_probe.py`:23 | :991-1019 | 995-1023 |
  | `regress/m8820x_sites_probe.py`:27 | :991-1019 | 995-1023 |
  | `regress/readiness_predicate_test.py`:70 | :277 | 281 |

* **DISPOSITION for the `dev_m8820x.c` citation:** an L4 this round owes before commit (R18).  Renumber it or re-key it
  by construct name.  Two constraints apply:
  * The line count of `dev_m8820x.c` must not change.  `FAILURE()` embeds `__LINE__` through `CHECK_ALLOCATION` at :537
    (`T/BUILD_REPORT.md`:117-118, departure 6; `src/include/misc.h`:181-188).
  * The "comment-only, object identical" measurement (S21) was made on the uncorrected text, so it must be re-measured
    after this edit.
* **DISPOSITION for the five regress comments:** FILE them under the citation-form rule; do not sweep them in this
  round.  No gate reads a line citation, and editing two gate-run probes would change md5s that gate logs print.

## N4 (P1) -- "(the debugger)" in the new `memory_rw.c` comment

* **Where:** `src/cpus/memory_rw.c`:625-627 reads "NO_EXCEPTIONS callers (the debugger) never get here: the test above
  keeps them out."
* **What is true:** the guard at :603 does keep out every NO_EXCEPTIONS caller.
* **What the parenthetical gets wrong:**
  * The debugger's single-step pre-read is `CACHE_INSTRUCTION` WITHOUT NO_EXCEPTIONS (`src/cpus/cpu_dyntrans.c`:287-288,
    R2), and it DOES reach the arm.  It is the channel of the four stepped `ifetch` rows and of the null session's part 2.
  * A non-debugger NO_EXCEPTIONS caller exists: `src/devices/dev_luna88k.c`:613-614.
  * The probe header's disclaimer uses the same shorthand (:44-45).
* **DISPOSITION:** true but misleading (P1; Q1(c) [M7]).  Recommended: reword before commit.
  * This is a comment-only edit to a shared product file.  Propagate it to `est/` and the three build trees, then rerun
    the two-part clearance.
  * The object is unaffected.  `memory_rw.c` uses no macro that embeds `__LINE__`: it calls no `assert`, `FAILURE` or
    `CHECK_ALLOCATION` (grep count 0).

## N5 (P5) -- the PRETABLE / BUILDER_QUESTIONS cross-references do not line up

* **L22's prediction is not where the criterion says.**
  * `T/SCORES.txt`:4 names "PRETABLE section 5's predicted set as amended (AMENDMENT 1)".  L22 is scored MATCH at :131.
  * L22 is in neither of those.  Its prediction is in `T/BUILDER_QUESTIONS.md`:135-136 (Q18, file mtime 22:29:30) and
    `A/pass1_20261023/BUILD_SPEC.md`:233 (Q18 APPROVED, mtime 22:31:49).  Both precede the leg (`T/L22_casedel.out`,
    23:08:43).
  * `T/PRETABLE.out`:121-122 still says "No leg in the table builds "case deleted" (BUILDER_QUESTIONS Q9 offers one)".
* **PRETABLE's question ids follow a DRAFT numbering.**  PRETABLE.out's mtime (22:28:08) is earlier than
  BUILDER_QUESTIONS.md's (22:29:30).  The table maps each PRETABLE id to the final file's id:

  | subject | PRETABLE id(s) | line(s) | final id |
  |---|---|---|---|
  | L6b | body Q6; AM-4 [Q12] | :207, :274; :415 | Q16 |
  | L16 | body Q7; AM-4 [Q13] | :284; :419 | Q17 |
  | L18's form | body "Q8 form" | :287 | Q14 |
  | L20 = L4 | body Q5 | :293 | Q13 |
  | "case deleted" (L22) | body Q9 | :122 | Q18 |
  | `ifetch route` as CONTROL | AM-5 [Q7] | :425 | Q8 |

  AM-1's [Q1]-[Q4], AM-4's [Q14] and [Q15], and AM-6's [Q9] match the final ids.
* **A timestamp mismatch:** AMENDMENT 1 self-dates "~22:3x" (:362).  The file's mtime is 22:28:08.  That is before the
  BUILD_SPEC section 11 rulings it cites were written (22:31:49).
* **DISPOSITION:** records only.  Do NOT edit PRETABLE.out: it is the order proof, and its header forbids edits in place
  (:13-15).
  * Add one dated note beside it, or in SCORES.txt.  The note should say that L22's prediction is Q18, map the ids, and
    cite mtimes rather than the self-stated time.
  * The order claim ("before table 1", which started 22:58) is unaffected.
  * The MANIFEST entry's "27 of 27 measurements as predicted" (`tools/pipeline/check_probe_wiring.py`:3229; staged diff
    :14) stays true if Q18 is accepted as L22's prediction.
  * The FULL brief's section 3.5 now carries the id map.

## N6 -- the ledger row records no stages at all, though pass 1 ran

* **Where:** `tools/pipeline/ledger.json`, at HEAD and in the working tree.  Row `m88kbuserrregs`: state `open`, witness
  `none`, commits `''`, no stages.
* **Unrecorded pass 1:** `A/pass1_20261023/` holds these answers:
  * `codex_t36p1.txt`, `grok_t36p1.txt`;
  * `ollama_glm_t36p1_Q12.txt` / `_Q34.txt` and `ollama_deepseek_t36p1_Q12.txt` / `_Q34.txt`;
  * the adjudication `adj/codex_t36p1adj.txt`;
  * the notes `roster_NOT_FIRED.txt`, `fable5.HELD.txt` and `argon.NOT_FIRED.txt`.
* **Unrecorded pass 2:** `A/pass2_20261023/` already holds its NOT FIRED and HELD notes.  The ledger cites neither
  directory.
* **DISPOSITION:** records owed before commit (precommit sections G and H).  Add stage entries naming both panel
  directories, plus the NOT FIRED entries and the HELD entry with Fable's hold question.  Q3(c) asks for this.

## N7 (P4) -- a count restated over a set it was never measured on

* **Where:** `src/devices/dev_m8820x.c`:326-333.  The PFSR and PFAR writer lists now add "memory_rw.c's arm".  The same
  sentence continues: "DIRECTLY through reg[], with no purge, ~10^5 times per boot -- against 2 guest writes per boot".
* **The gap:** the ~10^5 described the translation-fault writer (`memory_m88k.c`).  Nothing counts how often the arm
  writes.  The boot A/B counts none (`T/boot_base.out`, `T/boot_work.out`).
* **DISPOSITION:** P4 (Q1(c) [D2]).  Scope the number to the writer it measured, or mark it unmeasured for the arm.  The
  edit is comment-only, under the same line-count constraint as N3.  Not a floor matter.

## N8 (P6) -- the LUNA instruction-fetch cell: PRETABLE prescribes a CHANGELOG sentence; no NOT CLAIMED line exists

* **Where PRETABLE prescribes it:**
  * `T/PRETABLE.out`:80-82 (1.B(3)): HEAD's case wrote cmmu[1] even for an instruction access, and the fix deletes that
    write, so there is "no LUNA instruction-fetch row ... -> one CHANGELOG sentence".
  * `T/PRETABLE.out`:115-116 (CL13): a store and an instruction fetch at this address "are NOT rowed".
* **What NOT CLAIMED says** (probe :187-205): it names the LUNA STORE (:194) and FREE-RUNNING instruction fetches
  (:197-198).  It does not name a stepped instruction fetch at 0x3ffffff0.
* **DISPOSITION:** the CHANGELOG block owes PRETABLE 1.B(3)'s sentence (Q3(a)).  Whether NOT CLAIMED should also gain a
  line is P6.  If it should, that edit belongs in the same re-freeze as N2.

## N9 (P10) -- an unmeasured prediction worded as fact in the header

* **Where:** probe :171-172 reads "with R2 fixed the step's own fetch reaches the same arm, so the NULL-check observable
  survives and only the after-fault flow changes (R1's halt)".
* **The gap:** nothing measured this.  E's D2 (`PASS1_RULINGS.md`:246-247) rules on the fate of the `ifetch` rows only,
  and that is source-derived.
* **DISPOSITION:** a candidate L4 in the header.  Mark it "predicted (source-derived), unmeasured" at the re-freeze.  The
  CHANGELOG must not state it as measured.

## N10 (P8) -- gate-level clause (a) was never run

* **Where:** `T/BUILD_REPORT.md`:108-110 (departure 3).  The gate block was inserted after propagation, so gate 14 never
  ran it on a pre-fix build.
* **What does exist:**
  * The probe-level receipt: `T/prefix_HEAD.out`:39-41 (21/31, PRESENT 10/10).
  * Two gate pins that would red on a pre-fix build: `regress/gate_arm.sh`:1935 (`rows correct` == 31) and :1937
    (`SYMPTOM=ABSENT` x1).
* **DISPOSITION:** P8.  Record it as "(a): measured at prefix_HEAD.out; at the gate by construction via :1935/:1937, leg
  not run".
  * The panel must say whether that form, which R2 defines for clause (c), is admissible for clause (a).
  * If it is not, the gate-level pre-fix leg is owed before commit.

## N11 (P9) -- A3's licence is now measured, and E's wording is out of date

* **Where:**
  * `PASS1_RULINGS.md`:211-212: A3 stays "transferred warrant" until the B5c rows MEASURE the delta.
  * `T/L8_nullrm.out`:33-34: `null surv` and `null route` both `died:sig11`.
  * `T/L8b_nulldata.out`:33: `null surv` `died:sig11`.
* **DISPOSITION:** records only.  The CHANGELOG states the NULL check's licence as a measured delta (L8, L8b) and cites
  those two outputs.

## N12 (P7) -- the boot A/B supports "no regression to login:" and nothing more

* **Where:** `T/boot_base.out`:5-6 and `T/boot_work.out`:5-6.
  * Both runs end `reason=MARKER` with markers 1:1:1.
  * Instruction counts: 7,651,336,103 (base) against 7,550,665,157 (fixed), a drop of 100,670,946 (1.3 %).
  * There is no base-against-base control.
  * `3ffffff0` occurs zero times in either log and in `T/boot_ab/*`.
* **DISPOSITION:** records only.  The CHANGELOG must not interpret the instruction delta, and must not claim the boot
  exercised the LUNA case.

## N13 (P14) -- the gate comment drops two of A8's qualifiers

* **Where:** `regress/gate_arm.sh`:1917-1919 reads "A REFUSED m88k device access -- a device CLAIMS it and returns 0
  with the cpu still running -- now records its bus error in the faulting side's CMMU".
* **The gap:** it omits two qualifiers that A8 (probe :40-47) carries: "unsuppressed" (NO_EXCEPTIONS callers) and the
  CMMU-less exclusion.
* **DISPOSITION:** P14.  Low priority.  An edit changes `gate_arm.sh`'s md5 (`5ee94e61`, printed at
  `T/gates/gate14_run.out`:3).  Record that the gate ran the pre-edit file; a comment change does not justify re-running
  the gate.

## N14 (P12) -- `staged/gate_arm.sh` keeps its `.sh` suffix

* **Where:** `T/staged/gate_arm.sh` is byte-identical to the working-tree `regress/gate_arm.sh` (cmp).
* **The mismatch:**
  * Q19 (`BUILD_SPEC.md`:235) says frozen copies and drivers under `regress/artifacts/` are `*.py.txt` / `*.sh.txt`.
  * `T/BUILD_REPORT.md`:105-107 (departure 2) names the checker copy's `.py.txt` and says nothing about the gate copy.
  * The suffix is inert for `check_probe_wiring.py` (it reads `.py` only) and for `run.sh`.
* **DISPOSITION:** before commit, rename it to `.sh.txt` or drop it (`staged/gate_arm.staged.diff` already carries the
  change).  Record which.

## N15 (P11) -- SCORES.txt truncates SYMPTOM at 60 characters

* **Where:** `T/drivers/mk_scores570.py.txt`:132 has `kv.get("SYMPTOM", "?")[:60]`.  Compare L3's line in SCORES.txt
  with the full value at `T/L3_armHEAD.out`:41.
* **DISPOSITION:** records hygiene.  Add one line to SCORES.txt saying the field is cut and the leg outputs carry it
  whole.  Not an L4, because SCORES does not claim the field is complete.

## N16 (P13) -- "DATED PREDICTIONS ... UNTIL THE TABLE RUNS" is stale

* **Where:** probe :105-106.
* **DISPOSITION:** if N1, N2, N8 or N9 forces a re-freeze, fold this in.  Otherwise leave it, to keep byte identity with
  the frozen copy, and say so.

## N17 -- HEAD-numbered `cpu_m88k.c` and `memory_rw.c` citations in dated artifacts

* **Where:**
  * `cpu_m88k.c:811-819` (SFRZ; working tree :815-823) is cited at `BUILD_SPEC.md`:205, `T/BUILDER_QUESTIONS.md`:42 and
    `T/PRETABLE.out`:448.
  * Other HEAD-numbered `cpu_m88k.c` citations: `T/PRETABLE.out`:29 (:912), :43 (:354-357), :348 (:141-153) and :378
    (:870-879).
  * E cites `memory_rw.c:620-622` (`PASS1_RULINGS.md`:222).  That is HEAD numbering; the working tree has it at :639-641.
* **DISPOSITION:** no action on the dated artifacts, which were written against HEAD before the edit.  The CHANGELOG
  block cites post-fix lines or anchors.  Section S15 of the brief gives both numberings.

## N18 -- residue in the `dev_m8820x.c` comment

* **Where:** `src/devices/dev_m8820x.c`:327-329 still explains that "the file named again because a bare ":399-405"
  after a dev_luna88k.c citation read as a keyboard scancode switch".  The citation it refers to now reads "no longer
  dev_luna88k.c".
* **Note:** HEAD's removed citation `dev_luna88k.c:614` was already stale at HEAD.  The write was at HEAD :626, and
  PRETABLE CL17 (:125) calls it stale.
* **DISPOSITION:** no action.  The history is still literally true, and the stale citation is gone.

---

**Coupling.**  N1 (if rowed or disclosed), N2, N8 (if adopted), N9 and N16 all edit the frozen probe's docstring.  Do
them in ONE re-freeze, never piecemeal.  The re-freeze has three consequences:
* The committed probe will differ from the measured instrument.  SCORES.txt, the gate-14 receipt
  (`T/gates/gate14_run.out`:3, md5 `d57c12ab7ade903946c7d80a8e153ab7`) and the MANIFEST entry all identify rev 2 by that
  md5.  The records must name both md5s and give the docstring-only diff.
* Re-running the probe alone on the fixed and HEAD binaries shows the 31 rows are unchanged.  That costs seconds; gate
  14's run took 7974 s.
* N3, N4 and N7 are product-comment edits.  Do them together under the same rules: the line count of `dev_m8820x.c`
  must not change, the object compare must be redone, the edit must reach `est/`, and the two-part clearance must be
  rerun on all three build trees.
