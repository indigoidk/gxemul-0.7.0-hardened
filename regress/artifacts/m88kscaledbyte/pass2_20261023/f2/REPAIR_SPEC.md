# `#569` repair pass (R1-R5 + F25) -- the builder's spec.  RULED by GPT-6 Astra's F2 adjudication (`f2/codex_t1f2.txt`,
# 2026-10-23 ~12:15: SHIP WITH THE NAMED REPAIRS).  Amendments from the ruling, which override section 1 where they differ:
#  * R1 placement CONFIRMED (after `CC=`, before `need_file`; the "before #412" idea would sit behind the unconfigured-tree skip).
#  * R3 applies to the GENERATOR comment only (F9/F16/F23: the gate block's comment says "the table" is indexed unchecked and
#    then "calls the slot" / "installs it" in the singular -- it does NOT claim a caller for all 24; leave it as it is).  Its
#    verification is a SOURCE READING of the corrected wording against the consumers (cpu_m88k_instr.c:2377, :2411, :3606,
#    :3622), not "rows do not observe comments"; and the comment change is PROPAGATED to est/ and the build trees (A5).
#  * R4: do NOT append a clause beside the weighted formula.  REPLACE the driver's `:119-120` explanation with the sum form
#    `index = no_pc_sync + registeroffset + usr + scaledness + endianness + signedness + store + size`, identified as the
#    generator's flag-VALUED variables (256/128/64/32/16/8/4 and the size 0..3), consistent with the existing indices.
#  * M2's run is NOT a clean committed-tree run: the foreign `diff_wdc_identify.c` stays in the tree; describe exactly what
#    the tree held; keep the earlier 502 receipt and GATE 11's limitations as recorded.
#  * Each repair closes on its first VALID zero-breach pass (the delivered diff inspected, roster absences named, the
#    cells/shapes inspected stated, the floor question asked of the composite).
#  * F28: "18 outputs" = 16 v3 outputs + v1 PRE/FIX (the root RUNS.log holds no v1 runs) -- say so in the repair report.

Ground rules: BUILD_SPEC.md section 0 (same sandbox: git object reads only, never the index; never the peer's files or
`tools/`; WSL `-d Gentoo`, `/mnt/c` paths; foreground only; LF preserved; variant work in files only).  Artifacts dir:
`regress/artifacts/m88kscaledbyte/repair1_20261023/` (create).  Record output, never assertion.

## 1. The edits (each as the proposal `f2/repair_proposal.md` says; nothing else changes)
R1  `regress/gate_offline.sh` -- the `# ---- #569:` block MOVES from after the `#375` reader to immediately after
    `CC=$(command -v cc || command -v gcc)` (HEAD `:185`) and before `need_file "$HERE/diff_ieee_store.c" ...` (HEAD `:186`).
    Its invocation becomes `GEN= TABLE= CC="$CC" "$HERE/diff_m88k_loadstore_gen.sh" > "$MLSLOG" 2>&1`.  Its comment gains the
    placement sentence and the reworded consumer sentence (R3).  Produce BOTH: (a) the staged copy
    `repair1_20261023/staged/gate_offline.sh` = HEAD + the block at the new place (the old `table1_20261022/staged/` copy
    is superseded and left as the record of pass 2); (b) the same change on the working-tree file, which keeps its foreign
    hunks: remove the block from its old place and insert it at the new one -- `diff` the two insertions to prove they are
    identical, and `diff HEAD-blob staged` must be ONE hunk at `:185/186` of +N -0 (record N).
R2  `regress/diff_m88k_loadstore_gen.sh:92`: `CC=${CC:-cc}` -> `CC=${CC:-$(command -v cc >/dev/null 2>&1 && echo cc || echo gcc)}`;
    the header line about `CC=<compiler>` (`:82`) gains "(default cc, else gcc; gate 2 passes its own)".
R3  `src/cpus/generate_m88k_loadstore.c` `#569` comment (`:258-261`): the consumer sentence reworded exactly as the proposal
    says (twelve slots installed by the register-form ld/st decoder, four called by `xmem_slow()`, eight with no caller
    today, repaired with them); the gate block's comment likewise.
R4  driver `:119-120` comment: add the clause about the flag SUMS (the generator's loop variables already hold 256/128/...).
F25 driver NOT-OBSERVED paragraph (`:66-74`): one line -- "a name swap among UNPINNED cells (e.g. the scaled word/halfword
    cells not in the accept set, 185/186) keeps every row green: outside the contract".
No row, no expected name, no leg changes.  The regenerated table is UNCHANGED (R3 edits a comment in the generator source,
not its output): verify by re-running the fixed generator in `/tmp/gxt1/repair/` and `cmp` against the committed table.

## 2. Measurements
M1  The driver on the repo files (defaults): `repair1_20261023/fixed_r1.out` -- `ROWS=123 FAIL=0`, sentinel; byte-identical
    to `table1_20261022/fixed.out` except the driver's own version/CC lines if it prints any (say which).
M2  GATE 2 on the COMMITTED FORM: swap the working-tree `regress/gate_offline.sh` for the new staged copy (keep the
    working-tree file as `repair1_20261023/wt_gate_offline.sh.bak`, md5 recorded), run GATE 2 once, alone, via `run.sh`'s
    single-gate form, then restore the working-tree file and `cmp` it against the backup.  Record the tail
    (`GATE2_committedform_tail.out`): expected `PASS (485 checks)` on this tree IF the foreign `diff_wdc_identify.c` is
    also HEAD's -- it is NOT (another session's modified copy sits in the working tree), so record the number you get and
    what the tree held; the round's block must show its 126 checks ok.  Do NOT touch `diff_wdc_identify.c`.
M3  GATE 2 on the working tree as it stands after the move (the dirty tree, as the battery runs it): `GATE2_wt_tail.out`.
M4  Propagation: the generator source (comment-only change) and the driver are copied to `est/`, `build/`, `build-asan/`,
    `/tmp/gxsec-build` (the driver only exists in GXEMUL-SEC/est -- regress is not in the build trees; say so); the three
    build trees rebuilt (`rm src/cpus/*.o; make`, foreground, one at a time) so part 2 of the clearance holds again;
    `CLEARANCE_r1.out` for all four trees, est part 2 N/A.  GATE 11 is NOT re-run (no product-code change).
M5  `REPAIR_REPORT.md`: the diff stat of the repair (HEAD -> working tree for the generator and the driver; HEAD -> new
    staged copy for the gate), M1-M4 by file, and anything that disagreed with this spec.

## 3. The scoped pass on the repair diff
The repair diff (R1-R5 + F25) gets ONE review pass scoped to it (the repair-chain rule; effort on the diff, the floor
question on the composite): the main loop drafts `pass3_20261023/` from the repair report with the diff inlined; roster
GLM 5.3 + DeepSeek + Grok (+ Argon not fired: lockout); Astra adjudicates.  The chain closes on the first pass that finds
zero breaches with its denominator stated.
