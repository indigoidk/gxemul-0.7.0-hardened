# #562 armmsrmodekill -- Fable 5.1 ADJUDICATION of the main loop's rulings, before the local commit

**Liveness, first two lines of your answer:** (1) the token `FABLE_SEAT_ALIVE_20261009_562`; (2) the FIRST LINE of
`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`, quoted verbatim.  Then `VERDICT: RATIFY / RATIFY WITH
CHANGES (<n>) / DO NOT RATIFY -- <one line>`.

You are the ADJUDICATING seat.  Fable was held out of this round by the owner from 2026-10-07 until 2026-10-09 13:1x,
so every pass of #562 was adjudicated by the main loop itself (Opus 5.5 -- badge A, author self-review).  The
owner has now lifted the hold.  **Do not simply ratify.**  The load-bearing question is: **which of the main loop's
NINE rulings below is wrong?**  A correction is worth more than agreement, and "none" is an answer you must earn.

## Ground rules

* Tree under review: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` WORKING TREE, HEAD `ef577140` plus #562's uncommitted
  edits.  Ignore any other `src/` under the project root (pristine 2021 upstream).  Ignore the other session's
  unrelated uncommitted files: `cpu_alpha_palcode.c`, `dev_lca.c`, `dev_pcc2.c`, `dev_sh4.c`, `mvme_pcctworeg.h`,
  `gate_sh_rounding.sh`, `gdrom_default_probe.py`, `sh4_chcr_probe.py`, `tools/adjudicate.sh`, and their ledger and
  wiring lines.
* **READ-ONLY on every project tree.**  Do not edit anything under `GXEMUL-SEC`, `est`, `build`, `build-asan` or WSL
  `/tmp/gxsec-build`.  No `git add/commit/stash/checkout/reset`, and no plain `git status` (it can write the index,
  and a commit precheck is holding staged files) -- use `git show`, `git log`, `git --no-optional-locks status`, or
  plain `diff`.  Do not run any gate.
* You MAY measure if a ruling can only be settled by running something: copy the tree to your OWN WSL scratch clone
  (e.g. `/tmp/gxfable562`), build with `MSYS_NO_PATHCONV=1 wsl -d Gentoo -- bash -c '...'` (the default distro has
  no make), `rm src/cpus/*.o` first, and check `[ gxemul -nt src/cpus/cpu_arm.c ]` after -- `make` has reported 0 on
  failed builds.  The four #562 files must come from the WORKING tree, not HEAD.  Say plainly what you ran.
* Write your FULL answer to
  `C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\c562\fable\fable5_adjudication562.md`
  and also return it as your final message.

## The package (read these)

Scratch dir `S = C:\Users\User00\AppData\Local\Temp\claude\C--DocumentNoSnc-cc-GXEMUL\8e474f41-4d47-4c99-bf11-3406a84c4fcd\scratchpad\c562\`;
artifacts `A = GXEMUL-SEC\regress\artifacts\armmsrmodekill\`.

* The product diff: `S\fable\diff562_src.diff` (HEAD vs working tree: `cpu_arm.c`, `cpu_arm_instr.c`,
  `cpu_arm_instr_dpi.c`, `cpu_arm.h`).  Read the enclosing functions in the tree, not only the hunks.
* The detector: `GXEMUL-SEC\regress\arm_msrmode_probe.py` (its module docstring is the CONTRACT and NOT CLAIMED list),
  and the gate section in `GXEMUL-SEC\regress\gate_arm.sh` (search `#562 armmsrmodekill`).
* The records: `S\changelog_block.md`, `S\bugs_section.md`, `S\msg562.txt`, `S\vals562_draft.json` (the ledger values
  the commit writes).
* The evidence: `A\killtable5_20261008\` (`run_head.out`, `run_fixed.out`, `PRETABLE5.out` with its appended
  CORRECTIONS, `SHIPPED_vs_FROZEN.txt`, lane outputs), `A\PASS2R5_brief_20261009.md` (the last packet),
  `A\panel_pass2r5_20261009\` (the seat answers), `A\opus_pass2r5_20261009\opus_pass2r5.md` and `KTR5*.out` (the
  measuring seat's final report), `A\gate14_20261009\` (`gate14_run1.out`, `xscale_ab.out`, `cleanbuild.out`,
  `xscale_clean.out`, `gate14_run2.out`), `A\astra_confirm_20261009\codex_confirm562.txt` (GPT-6 Astra's records
  confirmation, 13 corrections).  Earlier passes: `A\PASS2*_brief_*.md`, `A\opus_pass2*`, `A\killtable*`.
* The rules: `C:\DocumentNoSnc\cc\GXEMUL\CLAUDE.md` -- the vacuity floor clauses (a)-(f), DEPENDS-ON and its bound,
  JOINT CELLS and the floor/debt split, "TESTS means masks or compares as a case", the dispatch-LABEL clauses, the
  repair chain and its stop condition, L1-L4, the option set (members 1-7).

## The nine rulings to adjudicate

* **R1 (fix shape).**  Option-set member 3, DECLINE + LATCHED ANNOUNCE, at the three guest writers of CPSR.M
  (`msr_imm`, `arm_pop`'s `^` restore, the DPI S-to-PC restore): the mode field is declined when it names a mode the
  model does not bank, the rest of the write applies, one announce per site per CPU (`mode_warned` bits).  Declined
  as a POLICY for UNPREDICTABLE behaviour (DDI 0100I A2.5.7, "must not halt or hang"); member 5 (UNDEFINED) was not
  chosen.  *Premise to check, not to accept:* is any of the three declines wrong for a value a real guest writes?
* **R2 (backstops).**  `arm_save_register_bank()` / `arm_load_register_bank()` `default:` arms keep a latched
  announce and `return` instead of `exit(1)`, as backstops.  *Question:* after R1, can any GUEST path still put an
  unmodelled mode into CPSR.M and reach them?  If yes, is a backstop that only announces and returns correct there?
* **R3.**  `msr_imm` declines through a LOCAL copy of the mask and never writes `ic->arg[]` (a cached translation).
* **R4.**  `arm_pop`'s `^` restore keeps the current M[4:0] and takes every other bit from the SPSR, no early return;
  the DPI S-to-PC restore goes through a `new_cpsr` local and declines only when an SPSR was actually copied.
* **R5 (detector).**  47 rows over 43 sessions; a generated grid (G1 complementary (path, outcome, bit, polarity)
  cells, G2 label ^ 0x1f, G3 all 25 unmodelled values per path, G4 the four `arm_pop` enclosing cells); `grid cov`
  asserts G1 only.  HEAD 18/47 with 29 named reds; fix 47/47; kill table 5: 110 runs, 104 distinct mutants, 103
  killed.
* **R6 (THE FINAL-PASS DISPOSITION -- the ruling most worth attacking).**  Pass r5 measured five escapes that act
  only while a site's latch is CLEAR, at CPSR bits the decline bodies never test (31:8), plus two `msr` label x latch
  cells, plus the cached-translation mutant `M_msr_argmask` that no shipped row sees.  The main loop graded all of
  them OUTSIDE the floor (clause-(e) coverage debt, not L2), so the contract was narrowed COMMENT-ONLY and the
  measured closures (a session reorder; a 48th row that loops inside one `step N`) were filed as `armmsrmodedebt`.
  The OWNER then ruled "commit, file the rest".  *Your job here is the floor question, not the owner's choice:* under
  the carrier's rules as written, is ANY of these a FLOOR cell (DEPENDS-ON closure, generating set, dispatch-label
  clauses) -- an L2 breach that clause (e) may not absorb?  If so, quote the rule, name the cell, and say so plainly;
  the owner will be asked again with that fact in hand.
* **R7 (gate 14).**  Run 1 went red on xscale 28/30 from a STALE `dev_i80321.o` (#562 grew `struct arm_cpu`; no
  header dependencies); all three build trees were rebuilt clean; run 2 PASS 1110/1110; the msrmode kill tables are
  unaffected because `-E testarm` attaches no i80321.  Filed as `headerstaleobj`.
* **R8 (filed rows).**  `armusrstop`, `armspsrthumb` (T honoured LATE: Thumb is chosen at run-loop entry and
  `arm_pop` word-aligns the PC), `armmmuvehicle`, `armmsrmodedebt`, `headerstaleobj`, and `armthumbabortkill`'s
  pre-brief note.  Is each filed for the right reason, and is anything that should have been filed missing?
* **R9.**  All 13 of GPT-6 Astra's corrections (`codex_confirm562.txt`) were applied.  Check that they were.

## Answer format

`R<n> | UPHELD / CORRECT: <the exact fix> / OVERTURNED: <why, with the rule or measurement>` for R1-R9, then any
other finding.  Separate what you READ from what you RAN.  **If you found something ELSE -- say so.**
