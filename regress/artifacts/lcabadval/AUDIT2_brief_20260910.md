# #518 lcabadval -- SECOND RECORDS AUDIT of the rewritten CHANGELOG round block (read-only)

Nonce: CODEX_518_RECORDS2_20260910.  Open with `VERDICT: GO | NO-GO (n items)` and echo the nonce.

**Please do not simply ratify, and be harder on the rewrite than on the original.**  Your first audit of this
block (`regress/artifacts/lcabadval/codex_audit_20260910.txt`, NO-GO, 27 items) drove a rewrite from the
artifacts; the house rule is that a correction is not safer than the thing it corrects and earns a second
reading.  `*** OWED ***` markers are EXPECTED (tables 3 and 4 are still running) and are not findings; a
number or claim stated as fact that no artifact supports IS a finding, and so is a sentence of the first
audit's 27 that the rewrite claims to have disposed and did not.

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`; ignore any other `src/` under the project root.

## The drafts (copies of the session drafts; read both whole)
* `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\codex_in\changelog_518.md` -- the round block.
* `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\codex_in\changelog_518_pass2.md` -- its pass-2 / tables / repair-chain half.

## The artifacts (all under `regress/artifacts/lcabadval/`)
* `witness_20260909/` (the Opus rung-3 witness, `HEAD_74daefd.out`), `PASS2_brief_20260910.md`, `pass2_20260910/`
  (six seat answers + `SEATS.txt`), `AUDIT_brief_20260910.md` and `codex_audit_20260910.txt` (your first audit).
* `killtable_20260910/`: `PRETABLE.out` (sections 1-9), `SCORES.txt` / `SCORES_B.txt` (table 1), `t2/` (table 2,
  `PREDICTIONS.txt`), `t3/SCORES3.txt` (table 3, in progress), `pre_repair_aborted/README`, the detector runs
  `FIX518_detector_run*.out` and `run3_D9unsplit.out` wherever they sit under `regress/artifacts/lcabadval/`.
* `propagate518.out`, `propagate518b.out` -- the two-part clearances.
* The source `src/devices/dev_lca.c` (grep `lca_ioc_announce`, `LCA_W_IOC_`), the instrument
  `regress/lca_badval_probe.py` (count `row(` sites), and `_scratchpad/21066_66a_hrm.txt` at the project root for
  the manual citations the block makes (Table 6-6, S6.4.14 item 3, the `:9586-9598` / `:10791-10792` lines).

## Questions (verdict line first; one numbered item per finding; cite by grep anchor and file)
1. Every NUMBER outside an OWED marker: which artifact produces it and does the artifact say that -- the witness
   14/20 -> 20/20 -> 40/40 -> 53/53 -> 58/58 -> 64/64 -> 67/67 chain, 52/53, 57/58 (M29), 56/58 (M24), 16/58
   (null medium), 63/64, the "36 distinct mutants", "SIX non-equivalent 58/58 sweepers", "27 items", the
   manual line numbers, the clearance times 00:24 / 04:11.
2. Every QUOTED seat verdict: verbatim from the named file?
3. The roster sentence and the seat-attribution of each finding (kimi substitute: `def read0`; minimax/glm: the
   widened cells; codex: the assignment-vs-accumulation cell, the two corrections of the loop; grok: per-label
   WEN and the CONF bit): check each against the seat files.
4. Your first audit's 27 items: list any that the rewrite still commits, by number.
5. The manual citations: open `21066_66a_hrm.txt` at the cited lines and say whether each supports the sentence
   that cites it.
6. Anything else that is a wrong record -- an ordering claim, a "measured" that was predicted, a claim about what
   a mutant or row does that the artifacts do not show.

Do not propose product-code changes and do not run anything.
