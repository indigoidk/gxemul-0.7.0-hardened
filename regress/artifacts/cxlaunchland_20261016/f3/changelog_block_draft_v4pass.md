# `cxlaunchquotation` + `cxlaunchdaybreak` (2026-10-17): the codex launcher lands in `tools/cxlaunch.sh` -- a complete answer is never scored WALLED for quoting a wall line, a content-filter refusal on Astra is re-run ONCE on Daybreak, and a different model named by codex's OPENING header exits 5; the controls carry a CONTRACT naming every decision's pinned edges (v4, 116 checks, 32 mutants)

**Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
F1): codex's `^ERROR:` lines are classified ONLY when rc != 0 or stdout is empty, and stdout is never grepped for wall
words -- the discriminator is the exit status and the answer, which quoted text cannot forge.  Every real wall and refusal
on record is rc 1 with an empty stdout, and every rc-0 run carries an answer.

* `tools/cxlaunch.sh`: until this landing the tracked file ran Astra at `max` with the 2026-09-07 classifier while most farm
  jobs ran an untracked scratchpad copy -- and the carrier described the copy's behaviour as the tracked file's.  The landed
  file: ANSI colour stripped and `grep -a` before the `^ERROR:` anchor (a real coloured refusal read exit 6 unstripped; a
  real NUL-bearing wall read exit 6 without `-a`); the Daybreak fallback (`gpt-daybreak-blue-latest`, the refused run kept
  as `.refused.*`, the answer credited to Daybreak); the model read ONLY from codex's OPENING header block -- banner and
  first rule by line 12, the block for at most 30 lines -- and compared with the model asked for (exit 5 on a mismatch,
  "model UNVERIFIED", exit 0, with no opening block); the effort `ultra`.  Its header records the residuals (N4 and its
  refusal twin), exit 5's novelty to the pack runner, and the controls.
* Controls `regress/artifacts/cxlaunchland_20261016/run_controls_v4.sh`: every row drives three launchers -- the TRACKED file
  the landing replaced (the pre-fix column), the farm copy, and the landed file -- against a fake codex replaying a fixture.
  116/116 (`RECEIPT_v4.txt`): N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the fallback), X8 6 -> 8 (a NUL in
  stderr), and the v4 edges (W12/W13 the window, K30/K31 the cap, R2X/D3 a real doubled refusal at both guards, W1L one wall
  line, FB1/FB2 the fallback left on, D4 exactly two calls, X14/X15 the argv cap).  Its header is the CONTRACT: each decision
  the launcher makes, the rows that pin its edges, and what is deliberately not pinned, with `CENSUS_v4.txt` (2,422 codex
  `.err` files: 0 of 972 opening blocks without exactly one model line; 0 of 410 classified runs carrying both a refusal and
  a wall line) behind the disclosures.  Kill table `run_mutants_v4.sh`: 32/32 as recorded (`KILLTABLE_v4.txt`) --
  29 one-edit mutants killed by the controls their lines name, the three escapes filed as `cxlaunchunpinned`.
* Records: `cxlaunchquotation` and `cxlaunchdaybreak` closed (witness `harness:`; REGRESS reviews HELD for the flagship);
  `cxlaunchwallfp` (2026-09-26, no ledger row) merged with its tail-key fix WITHDRAWN; the bug file's stale "greps stdout
  freely" and "has no Daybreak fallback" statements bracketed by content; `cxlaunchunpinned` (LOW) filed; RULINGS_C's
  drifted line citations re-cited by id.

**Pass 2** (`pass2/`, on v1): Astra SWC 2, GLM SWC 2, Grok SWC 1 (the NUL-bearing wall, measured), Fable SWC 2 (its first run
fell back to claude-opus-4-8 after two refusals -- disclosed, credited as Opus 4.8; resumed, Fable 5.1 wrote v2).
**Adjudication pass** (`f2/`, on v2): Astra SWC 3 (the header awk matched the banner ANYWHERE -- N1's own stderr quotes four
headers; E1/E2 matched a substring), Grok SWC 3 and GLM SWC 3 (records described as written; the receipt citation;
`m_eq1`'s reason); Fable SEAT FAILURE (a stall).  **V3 pass** (`v3pass/`): Astra SWC 3, Grok SWC 3, GLM SWC 2 -- each found
one-edit mutants passing all 70 v3 controls (the window and cap constants, the refusal and wall multiplicity guards, the
fallback predicate), the same class as the two passes before, so v4 is the CLASS CLOSURE; Fable SEAT FAILURE (a second
stall).  **V4 pass** (`v4pass/`): [to be written].  Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster
of 2026-10-16.
