**Your token: `ASTRA_IP30WIRECF_20261018`** -- open your answer with it.

# #566 -- the confirm pass before commit

You answered pass 1, pass 2 and F2.  This pass checks that the F2 repairs landed as meant, that no sentence in the final
diff or the records is false, and that the full gate run supports what the records say.  **Please do not simply ratify.**
The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD 2036a3d5.  READ-ONLY.

**The material (all paths under the tree):**
* the code and records in the working tree: `regress/gate_arm.sh` (the #566 block, after the #564 `sgi_mte` block),
  `regress/artifacts/ip30abortkill/ip30_abort_probe.py` (the dated note above its CONTRACT), `tools/precommit_check.sh` (the
  pin and its comment), `OUTSTANDING_BUGS.md` (the #531 entry's in-place notes and the `#566` section at the end) --
  `git diff HEAD -- <file>` gives exactly #566's change for each of these four;
* `tools/pipeline/check_probe_wiring.py` -- the working copy also carries another unit's lines; the COMMIT copy is
  `regress/artifacts/ip30abortkill/gatewire_20261018/confirm/check_probe_wiring.commit_copy.py.txt` (HEAD + #566's hunks);
* the ledger edits are not in the working tree (the commit builds them from HEAD's blob): see
  `.../confirm/LEDGER_PREVIEW.txt` (the CONFIRM entry there is a placeholder this answer will replace);
* `.../confirm/CHANGELOG_BLOCK_draft.md` and `.../confirm/COMMIT_MSG_draft.txt` ({CONFIRM_LINE} is filled from this pass);
* the receipts: `.../gate14/RUN.txt` and `gate_arm.out` (the full gate 14 run), `.../legs/RESCORE.out`,
  `.../selftest/SELFTEST.out`, `.../controls/R_CONTROLS.out`, `.../fable5_f2_WALL.txt`.

**The F2 repairs to check:** the gate block's stall paragraph (a stall BEFORE an access leaves its `alive`/`no` rows green
and its `yes` row red; a count row reads green only with exactly ONE announce captured; V2_assigntick all-green only when
`xbit rev2`'s session stalls with one ISR announce captured and every other session passes), the two kill sessions named
explicitly; the probe note's latch-cell sentence (six rowed before the section, four there); the `legs566.sh`
annotation; `fableheldform` re-derived on the property (16 entries on ten rows); the wall receipt's wording; the same
corrections in `OUTSTANDING_BUGS.md` and the ledger preview.

**Questions.**
**Q1.**  Did each F2 repair land as meant, and is any sentence in the final diff, the ledger preview, the CHANGELOG draft
or the commit message draft false, over-qualified or inconsistent with another?  Cite `file:line`.
**Q2.**  Does the gate 14 run (`gate14/RUN.txt`, `gate_arm.out`) support the records' claims about it?
**Q3.**  Is anything still owed before commit?

**Format:** your token first, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line
starting `FLAG:`.  Facts and flags only.
