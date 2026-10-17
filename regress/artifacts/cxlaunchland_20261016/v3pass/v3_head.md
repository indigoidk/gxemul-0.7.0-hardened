# V3 PASS -- `cxlaunchquotation` / `cxlaunchdaybreak`: the codex launcher `tools/cxlaunch.sh`, v3 after the adjudication pass

Four seats, by the owner's roster of 2026-10-16: Fable 5.1, GPT-6 Astra, Grok 4.7, GLM 5.3.  Opus, agy, kimi, deepseek and
minimax are DELIBERATELY NOT FIRED under that roster.  An ordinary review of a shell wrapper that launches a read-only
review CLI and classifies its exit, and of the test harness that pins it.  READ-ONLY: write nothing to any project tree.
The tree is `C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC`; the v3 launcher is `tools/cxlaunch.sh` in the WORKING TREE (uncommitted,
md5 5314dc5c...); v2 is preserved as `regress/artifacts/cxlaunchland_20261016/cxlaunch_landed_v2.sh`; the controls and the
mutant table are `run_controls_v3.sh`, `run_mutants_v3.sh` and `mut_launcher_v3.py` beside it; the adjudication-pass answers
are in `f2/`.  Everything a packet-fed seat needs is inlined below.

**This is the repair chain's pass on v3.**  It closes on the first pass whose zero floor breaches survive adjudication --
so if you find none, say which cells and mutant shapes you swept (a zero needs its denominator).  Review EFFORT is scoped to
the v2 -> v3 diff; the FLOOR question -- is there a one-edit mutant of the shipped launcher that passes every control and
breaks a ruled property? -- is asked of the whole v3 file.  Check the premises below, do not ratify them: a recent panel
had seven of nine seats confirm a premise a brief stated wrongly.

<TOKEN_LINE>

## 1. The adjudication-pass verdicts (on v2)

* **GPT-6 Astra -- SHIP WITH CHANGES (3)** (`f2/codex_cxlandf2.txt`).
* **Grok 4.7 -- SHIP WITH CHANGES (3)** (`f2/grok_cxlandf2.txt`).
* **GLM 5.3 -- SHIP WITH CHANGES (3)** (`f2/glm_cxlandf2.txt` -- it answered under the Fable seat's token, because that
  packet listed all four; the transport was glm-5.3:cloud).
* **Fable 5.1 -- SEAT FAILURE**: the agent stalled after its opening line (stream watchdog, no progress for 600 s) and left
  no answer.  Not counted as agreement; re-fired on this pass.

## 2. Every finding, numbered, with my disposition

| # | seats | finding | disposition |
|---|---|---|---|
| G1 | Astra | v2's header awk matched the codex banner ANYWHERE in stderr; N1's own stderr quotes four complete header blocks from line 5528, so with the opening block absent v2 read a QUOTED `model:` -- a false verification, or a false exit 5 | **FIXED**: v3 reads only the OPENING block -- the banner and its first `--------` rule by line 12, the block for at most 30 lines.  X9 (no opening header; a quoted block naming gpt-6-astra after 20 streamed lines: must report UNVERIFIED, exit 0) and X10 (the same naming gpt-6-other: must not exit 5) pin it; mutant `m_v2awk` restores v2's awk |
| G2 | Astra, GLM | E1/E2 matched an unanchored substring, so `"$2x"` (effort `ultrax`) passed all 63; `--sandbox read-only` was unpinned and the brief was not even logged (`${*:1:8}`) | **FIXED**: the fake logs EVERY argument, one per line; E1/E2 `cmp` the whole sequence -- exec, --sandbox read-only, --skip-git-repo-check, -m <model>, -c model_reasoning_effort=ultra, the brief text -- once for N1, twice (Astra then Daybreak) for D1.  Mutants `m_effortx`, `m_sandbox`, `m_brief` added |
| G3 | Astra, Grok | the record edits the adjudication packet called done -- both closures with witnesses and HELD regress reviews, F10's two bug-file corrections, F19's state-note and `cxlaunchwallfp` merge, the `cxlaunchunpinned` filing -- are NOT in the tree | **ACCEPTED**: they are applied AT COMMIT by one script (both rows stay open until then).  Section 5 inlines the exact text it writes, so this pass checks it BEFORE it lands |
| G4 | GLM | the v2 header cites `(RECEIPT.txt)`, v1's receipt; the v2 driver's usage line names `run_controls.sh` | **FIXED**: the header cites `run_controls_v3.sh (RECEIPT_v3.txt; the kill table is KILLTABLE_v3.txt -- RECEIPT.txt and RECEIPT_v2.txt are ... earlier versions)`; the v3 usage line names `run_controls_v3.sh` |
| G5 | GLM | `m_eq1`'s reason "observable only inside the recorded N4 residual" is false: N4 is rc 1, where `-ne 0` and `-eq 1` agree; the observable shape is an rc outside {0, 1} WITH an answer | **CORRECTED** in the driver comment, `mut_launcher_v3.py`'s line and the `cxlaunchunpinned` filing (section 5) |
| G6 | GLM | a header block whose closing rule never comes was read to EOF by v2 | **FIXED** by G1's 30-line cap; the launcher header says so |
| G7 | GLM | "a `model:` line anywhere else ... never names the model" overclaims -- X6's quoted line names one | **FIXED**: the comment says such a line "is never READ" |
| G8 | GLM | E0's per-row `miss` loop only decorates its message | **KEPT**: the counts decide E0 (63 runs pinned, 63 argument logs); the list only names a row that did not reach the fake |
| G9 | Grok | `RULINGS_C_records.md` tells the reader to correct `OB:24714-24716` and ledger `:62489`; those lines now land on other rows | **CORRECTED AT COMMIT**: a dated bracket after that sentence re-cites them by id (`cxlaunchquotation`'s bug-file entry and ledger row) -- section 5 |
| G10 | Grok | `cxlaunchwallfp` still prescribes the withdrawn end-of-stream remedy and does not record the merge | in G3's records: its bug-file entry gains a MERGED note naming the withdrawal (section 5) |

## 2b. Premises to CHECK (stated as questions)

* The line-12 window: on record a codex stderr's `model:` line is line 5 in 599 of 600 `.err` files and line 7 in one (two
  lines before the banner; Astra's census on pass 2).  **Is there a real codex stderr whose banner or first rule comes
  after line 12** -- a longer preamble, a warning block, an update notice?  If so v3 reports UNVERIFIED and exits 0 there
  (fail-open, never a false exit 5), but say so.
* X9/X10 model the quoted block after 20 streamed lines.  **Is "no opening header, a quoted one later" the shape that
  matters**, or can a real run carry BOTH an opening block and a quoted one, so that only the first is read?  (v3 reads
  the first block that starts by line 12; `grep -m1 '^model:'` takes its first `model:`.)
* The three escapes left unpinned by ruling (`m_eq1`, `m_sgr`, `m_prec`) rest on 0 instances on record each.  Check that
  claim if you can.
