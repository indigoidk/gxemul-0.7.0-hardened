# `cxlaunchquotation` + `cxlaunchdaybreak` (2026-10-17): the codex launcher lands in `tools/cxlaunch.sh` -- an rc-0 run with a non-empty stdout is never scored WALLED or REFUSED for what its stderr quotes, a content-filter refusal on Astra is re-run ONCE on Daybreak, and a different model named by codex's OPENING header exits 5 (after the refusal, wall and empty-stdout checks); the controls' CONTRACT is derived from the file (v5: 224 checks, 105 mutants)

**Ruled before any code** by Fable 5.1, GPT-6 Astra and Grok 4.7 (`regress/artifacts/adj_20261016/RULINGS_C_records.md`,
F1): codex's `^ERROR:` lines are classified ONLY when rc != 0 or stdout is empty, and stdout is never grepped for wall
words -- the discriminator is the exit status and the answer, which quoted text cannot forge.  Every real wall and refusal
on record is rc 1 with an empty stdout, and every rc-0 run carries an answer: 474 launch-log rows, 440 rc 0 with stdout and
34 rc 1 empty, nothing else (`CENSUS_v5.txt`).

* `tools/cxlaunch.sh`: until this landing the tracked file ran Astra at `max` with the 2026-09-07 classifier while most farm
  jobs ran an untracked scratchpad copy -- and the carrier described the copy's behaviour as the tracked file's.  The landed
  file: ANSI colour stripped and `grep -a` before the `^ERROR:` anchor (a real coloured refusal read exit 6 unstripped; a
  real NUL-bearing wall read exit 6 without `-a`); the Daybreak fallback (`gpt-daybreak-blue-latest`, the refused run kept
  as `.refused.*`, the answer credited to Daybreak; not fired on an answer, a wall, a refusal asked of Daybreak itself, or
  with the fallback set empty); the model read ONLY from codex's OPENING header block -- banner and first rule by line 12,
  the block for at most 30 lines -- and compared with the model asked for (exit 5 on a mismatch, "model UNVERIFIED", exit
  0, with no opening block); the effort `ultra`.  Its header records the residuals (N4 and its refusal twin), exit 5's
  novelty to the pack runner and the log phrases that runner reads, the usage requirement of ABSOLUTE paths, and the
  controls.  Its executable lines are v3's; v4 and v5 changed comments only.
* Controls `regress/artifacts/cxlaunchland_20261016/run_controls_v5.sh`: every row drives three launchers -- the TRACKED
  file the landing replaced (the pre-fix column), the farm copy, and the landed file -- against a fake codex replaying a
  fixture.  224/224 (`RECEIPT_v5.txt`): N1/N2 8 -> 0 (the quoted-wall false positive), D1 7 -> 0 (the fallback), X8 6 -> 8
  (a NUL in stderr), IR 1 -> 5 (a different model), CH 0 -> 5 (a coloured header), CSI 6 -> 7 (a non-SGR escape).  Its
  header is the CONTRACT, derived from the FILE rather than from the reviews (v5): every predicate, conjunct, pattern
  alternative, redirection, constant, exit-cascade order and caller-read log phrase, each with the rows that pin its edges
  or the reason it is not pinned (`|| exit 9` after the `cd`; `set -u`; a relative path; display-only lines).  The synthetic
  rows pin constants with 0 instances on record, which `CENSUS_v5.txt` counts; the strip's `;` is not synthetic (44 codex
  `.err` files carry a `;`-joined SGR).  Kill table `run_mutants_v5.sh`: 105/105 as recorded (`KILLTABLE_v5.txt`), every
  mutant killed by the controls its line names -- the three escapes pass 2 left unpinned (`m_eq1`, `m_sgr`, `m_prec`) are
  pinned (RC2W, CSI, RW).
* Records: `cxlaunchquotation` and `cxlaunchdaybreak` closed (witness `harness:`; REGRESS reviews HELD for the flagship);
  `cxlaunchwallfp` (2026-09-26, no ledger row) merged with its tail-key fix WITHDRAWN; the bug file's stale "greps stdout
  freely", "has no Daybreak fallback" and "panel.sh's comment is still owed" statements bracketed by content; RULINGS_C's
  drifted line citations re-cited by id.  No row filed.

**Pass 2** (`pass2/`, on v1): Astra SWC 2, GLM SWC 2, Grok SWC 1 (the NUL-bearing wall, measured), Fable SWC 2 (its first run
fell back to claude-opus-4-8 after two refusals -- disclosed, credited as Opus 4.8; resumed, Fable 5.1 wrote v2).
**Adjudication pass** (`f2/`, on v2): Astra SWC 3 (the header awk matched the banner ANYWHERE; E1/E2 matched a substring),
Grok SWC 3 and GLM SWC 3 (records; the receipt citation; `m_eq1`'s reason); Fable SEAT FAILURE (a stall).  **V3 pass**
(`v3pass/`): Astra SWC 3, Grok SWC 3, GLM SWC 2 -- one-edit mutants passing all 70 v3 controls at the window and cap
constants, the multiplicity guards and the fallback predicate, so v4 closed that class; Fable SEAT FAILURE (a second
stall).  **V4 pass** (`v4pass/`): Fable SWC 7, Astra SWC 3, Grok SWC 5, GLM SWC 5 -- the v4 CONTRACT was derived from the
passes' FINDINGS, not the file, and decisions no pass had named had one-edit mutants passing all 116 v4 controls (codex's
own rc, the fallback's second and third conjuncts, the header strip, the stdin redirect, the output names, the pattern
alternatives, the body tests, the default codex path), so v5 derived the CONTRACT from the file.  **V5 pass** (`v5pass/`):
[to be written from its answers].  Opus, agy, kimi, deepseek and minimax not fired, by the owner's roster of 2026-10-16.
