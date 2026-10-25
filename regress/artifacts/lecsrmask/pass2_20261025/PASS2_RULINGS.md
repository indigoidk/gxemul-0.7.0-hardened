# T18 / `lecsrmask` (#573) -- PASS 2 (the diff review) and its adjudication F2b: the rulings of record

Written 2026-10-25 06:0x by the main loop from the six pass-2 answers (`codex_t18p2.txt`, `grok_t18p2.txt`,
`ollama_glm_t18p2_Q12/Q34.txt`, `ollama_deepseek_t18p2_Q12/Q34.txt`: all SHIP WITH CHANGES) and the six F2b answers
(`f2_20261025/codex_t18f2b.txt`, `grok_t18f2b.txt`, `ollama_glm_t18f2b_A/B.txt`, `ollama_deepseek_t18f2b_A/B.txt`: all RATIFY WITH
CHANGES).  The F2b packet is `f2_20261025/F2B_PACKET.md` (F1-F44 with the main loop's dispositions, D1-D3, Q1-Q3).  Argon: SEAT
FAILURE on both (web meter 0 of 2400 until 07:30:45 CDT; re-fired after the reset by the one-sender script, answers filed in the
records commit).  Fable 5.1 HELD (owner hold of 2026-10-21; `pass1_20261025/FABLE_HOLD_QUESTION.md`).  kimi, minimax and the Opus
review seat DELIBERATELY NOT FIRED under the owner's roster.

## The per-finding ledger (F2b asked for the partition to be published rather than counted)

| F | from | disposition | status after F2b |
|---|---|---|---|
| F1 | GLM Q12, Astra | APPLIED: the `default:` comment's subject is "This model" | ratified |
| F2 | GLM Q12 | APPLIED: "says only 'Must be zero' for CSR1 bit 0" | ratified |
| F3 | GLM Q12, Astra | APPLIED: the Ultrix observation attributed to the old comment, hedge kept | ratified |
| F4 | GLM Q12 | APPLIED: the read comment's accepts-both / filed clause | ratified |
| F5 | GLM Q12 | SETTLED TRUE: TM1986.txt:1695 `15:08 RES Reserved.` | ratified |
| F6 | grok | CONFIRMED: "Write as zeroes" not promoted into a store rule | ratified (grok READ am79c90:1222-1223) |
| F7 | grok | SETTLED: dev_le.c md5 3eab9c96 at HEAD = clone; `git diff --stat 0b09e7b6 2956c32d` = CHANGELOG.md + gate_hygiene.sh | ratified |
| F8 | Astra | APPLIED: "each of the CSR1, CSR2 and CSR3 sessions" | ratified |
| F9 | Astra, grok | APPLIED: CONTROL enumerated from `build_rows()` (14 control-kind rows) | ratified; GLM B nit applied: "does not fail CONTROL" (never "by itself") |
| F10 | Astra, grok, GLM | APPLIED: variant classifications are predictions, the table OWED | **GLM A: WRONG as applied** -- the CATCHES bullet "a mask conditioned on any single bit" is refutable: `x & (x & 0x0008 ? 0x0007 : 0x0005)` passes all four CSR3 rows and differs from the fix at 0x0002.  APPLIED 05:5x: CATCHES narrowed to "a store whose MASKING is conditioned on one bit (mask applied or whole value stored)"; the value-conditioned mask moved to OUTSIDE with that example.  Docstring only; code AST-identical |
| F11 | Astra | APPLIED: `build_rows()` comment -- the FIRST value read again | ratified (GLM A: load-bearing for the csr0 session) |
| F12 | grok | APPLIED: the opening and SITES rewritten before/after #573 | ratified |
| F13 | GLM Q34, Q12 | CONFIRMED: `ram:` rows bypass the write path; `stable:` wants are the session's first read | ratified |
| F14 | GLM, DeepSeek | APPLIED: the docstring inlined in F2b | ratified |
| F15 | DeepSeek vs Astra/grok/GLM | D1: build and measure L4 in the final cycle; "(b): leg OWED" until then | ratified by all six (grok: "L0 is not a reinstatement inside the landed structure"); GLM B: "to be built AND MEASURED"; the record states the pass condition and that a GREEN L4 would be a (b) breach |
| F16 | GLM | SETTLED as F7 (tree-scoped) | ratified |
| F17 | GLM | SETTLED: fix clone dev_le.c md5 = banked copy; the generator refuses on mismatch | ratified; GLM B: bank L4's md5s too (bank_final2.sh does) |
| F18 | GLM | SETTLED by grep: one caller (:1002), one reg_select writer (:1015) | ratified (grok READ the same) |
| F19 | GLM Q34 | APPLIED (text): the `probe:` term cites L0 + L1, the directory pinned by stamp | ratified; GLM B tightenings applied: one frozen script for all six legs, L0's CONTROL=OK named, the red set written from the measured file |
| F20 | GLM, DeepSeek | APPLIED: both RUN_IDENTITY files inlined; the witness dir keeps its records | ratified |
| F21 | grok, Astra, GLM, DeepSeek | D2: land `held` + state_note + hold_question (#569 form); NARROWED closure deferred | ratified by all six; grok F2b + GLM B: the close also waits for Argon's answers filed (or an exemption recorded), and an owner ruling must DISCHARGE the hold -- both in the hold question |
| F22 | grok | APPLIED: `rows run` pin; SCORE_CLAIMS_MANIFEST 40 -> 41 in the same commit | ratified (grok READ precommit_check.sh:368 = 40; DeepSeek A: only `rows run` lines are pins -- PIN regex, check_score_claims.py:75) |
| F23 | grok | CHECKED: no fraction in the block's comments | **grok F2b: the RULE I recorded was false** -- a gate comment naming the stem with a fraction fails whenever the denominator differs from the pin; the `N-row` escape is docstring-only (check_score_claims.py:175-204).  The observation (no fraction) stands; the rule text corrected here |
| F24 | Astra | CHECKED, FOUND WORSE: the first matcher matched ZERO rows (BRE `+`); corrected and dry-run | ratified (GLM A, grok READ the L0 file) |
| F25 | grok, Astra, GLM, DeepSeek | PLANNED: the CHANGELOG's distinctions | **GLM A: WRONG in two clauses** -- (i) "both manuals" for STOP-clear undefined/ignored was supported in the packet by the Am79C90 only: SETTLED by TM1986.txt:1572-1582 (the Am7990 manual's own sentence; grok READ it too), cited in the block; (ii) Appendix B's non-preservation must be attributed ("the Am79C90 datasheet characterises the Am7990 as not preserving"; the Am7990 manual says "normally not affected") -- APPLIED, the sources named as differing.  **grok F2b: sentence 4's licence** (see F39) -- APPLIED |
| F26 | grok | SETTLED TRUE: Table B-1 left = Am79C90 preserved, right = Am7990 not (am79c90:3411, 3686-3687) | ratified |
| F27 | grok | ACCEPTED: CSR2 bits 15:8 do not reach init_block_addr (`& 0xff`) | ratified |
| F28 | grok, Astra, GLM, DeepSeek | ACCEPTED: 78 = 77 tracked + 1 untracked at HEAD; after #573: 79 / 47 | **Astra: WRONG** (the pin should bind to the shipped population) / **DeepSeek A: WRONG** (the probe is "promptful") -- NOT ADOPTED: the pins are what `derive_hygiene_pins.sh` writes from the tree the battery runs in (the owner's 2026-09-23 ruling counts the untracked probes; grok READ census_tokens.py:32-35: `pty.fork` with no `endswith` classifies the probe promptless in the hygiene sense).  The numbers are recorded as the deriver's OUTPUT at landing, never asserted |
| F29 | grok | CONFIRMED: section F reads the previous src commit's receipt (0901b388 has one) | ratified |
| F30 | grok | ACCEPTED: pretests R/L/H/O/W/U/P/F on the staged copies; subject without a closure word | ratified (grok READ the closure regex) |
| F31 | grok, Astra, GLM, DeepSeek | CONFIRMED: `artifacts/` excluded from the hygiene censuses | ratified |
| F32 | all six | CONFIRMED: csr3 mix 0x0015 MEASURED on the pre-fix build | ratified |
| F33 | Astra, grok, GLM, DeepSeek | APPLIED: the WARNING sentence scoped to this block | ratified |
| F34 | Astra | APPLIED: PRETABLE's CSR0 coverage statement | ratified |
| F35 | GLM | CONFIRMED COVERED: the whole artifacts tree is added | ratified |
| F36 | GLM | CONFIRMED COVERED: the generator's md5 refusal | ratified |
| F37 | GLM | NOT ADOPTED: four equality checks instead of a literal "20/20" grep | **all six: right** |
| F38 | GLM | APPLIED: the floor sentence restated | ratified |
| F39 | GLM | SETTLED: (d) IS a floor clause; the brief understated it | **grok F2b: WRONG on the licence half** -- the understatement charge holds (an escaped (d) mutant is L2; honest OWED is not an L4); but #567's "land with filed debt" filed NON-floor cells after its floor rows were added (F3_DISPOSITIONS.md:26-48), so it licenses nothing here.  APPLIED: the records say OWED, cite no earlier ruling, and put the landing-with-debt decision to the owner (hold_question item 4).  Astra, GLM B, DeepSeek B had ratified the #567 warrant; grok's READ of the record settles it |
| F40 | grok, Astra, GLM, DeepSeek | ACCEPTED: "the carrier does not forbid a (d)-owed landing" | **grok F2b: WRONG with F39** -- the landing with (d) owed is the owner's ruling for this round, not the carrier's or #567's.  APPLIED as F39 |
| F41 | GLM | ACCEPTED: name the census population | ratified |
| F42 | grok | ACCEPTED: no STOP-preservation reading implemented | ratified; Astra F2b: say what #573 ADDS (nothing about STOP) without denying the model's existing behaviour -- APPLIED: "the model leaves CSR1-3 untouched by a STOP write (CSR3 never cleared, CSR1/CSR2 trivially kept); #573 adds no STOP behaviour" |
| F43 | Astra | ACCEPTED: the PMAD-AA reading is Grok's | ratified |
| F44 | grok, GLM | CONFIRMED: reg[1] bit 0 survives the SRAM mask into init_block_addr | ratified |

Partition after F2b: 17 APPLIED (F1-F4, F8-F12, F14, F19, F20, F22, F33, F34, F38, F42), 8 ACCEPTED/PLANNED (F25, F27, F28, F30,
F40, F41, F43 + F21's landing state), 2 settled by building (F15, F21 are D1/D2), 15 CONFIRMED/SETTLED (F5-F7, F13, F16-F18, F26,
F29, F31, F32, F35, F36, F39, F44), 2 CHECKED (F23, F24), 1 NOT ADOPTED (F37) = 44.  Dispositions found WRONG by at least one F2b
seat and changed: F10, F23 (its rule text), F25 (two clauses + the licence), F39, F40.  Found wrong and NOT changed: F28 (the
deriver's output governs; recorded as output).

## D1-D3

* **D1 (clause (b))** -- settled empirically: L4 = the fix clone with `d->reg[r] = x & 0x0007;` -> `d->reg[r] = x;` inside the new
  `case 3:` (mk_reinst18.sh), rebuilt, GATE mode, the same frozen script as every other leg (run_final2.sh).  The record says
  "(b): measured at final_<stamp>/RESULTS_L4_reinstatement.txt" once the leg exists; its pass condition is L0's shape (csr3
  all/hi/mix red, contract rows green, nonzero exit); a GREEN L4 would be a clause-(b) floor breach, recorded as such.  L4's
  source and binary md5s are banked in RUN_IDENTITY.
* **D2 (closure timing)** -- the row lands `held` with `state_note` and `hold_question` (commit 66920157's form); NARROWED
  closure when the Fable hold is discharged (or the owner rules ON THE HOLD QUESTION, discharging it) AND Argon's owed answers
  are filed or exempted; never `closed` while a `[HELD AWAITING SEAT: ...]` marker is live (check_stage_panels.py
  CLOSED-WHILE-HELD).
* **D3 (CONTROL semantics)** -- the docstring enumerates the control-kind rows from `build_rows()` and says a red SYMPTOM or
  CONTRACT row fails the leg and does not fail CONTROL; the kinds are not changed in code.  GLM B corrected the main loop's stated
  reason: the operative cost of a re-kinding is the AST-identity bridge to the banked 6259ce54 set (the landed detector would be
  semantically new, its legs without pass-1 corroboration), not stale measurements -- the second reason (an accept-side regression
  also reds the control line, disclosed) is the load-bearing one.

## Settled NOT-CHECKABLE items (the seats' settling facts, run)

* the 17-row witness's rows (`witness_20261025/RESULTS_base.txt`): ram:csr0/csr3/csr2/csr1, csr0 reset, rap mask, csr3 all
  [HEAD], csr3 bits, csr2 all [HEAD], csr2 lo, csr1 odd [HEAD], csr1 even (0x1234 then), csr1 top, stable:csr0/csr3/csr2/csr1 --
  14 control + 3 read-back rows; its FIX column carried the three-mask design later withdrawn (CSR2 0x00ff, CSR1 0x1234) and is
  not the contract;
* the diff statistic: `git diff --no-index --numstat` = 29 added, 9 removed (the F2b packet said 28: a `grep -c '^+[^+]'` misses
  an added blank line; GLM counted from the hunk headers and was right) -- the generator now uses numstat;
* TM1986.txt:1572-1582: "CSR1, CSR2 and CSR3 are accessible only when the STOP bit of CSR0 is set ... a READ operation will
  return undefined data. WRITE operation is ignored." (the Am7990 manual's own sentence, F25 i);
* the pins at HEAD, deriver run read-only 05:2x: EXPECT_PTY_PROBES 78/78, promptless 46/46, `lca_isaphys_probe.py` UNTRACKED
  and counted; the probe's hygiene class is promptless (`pty.fork`, no `endswith`: census_tokens.py:32-35, grok).

## What the F2b changed in the scratch copies before the final cycle (all comment/record-only; the probe's code stays
## AST-identical to the measured 6259ce54 revision)

docstring: the CATCHES family narrowed and the value-conditioned mask disclosed OUTSIDE (F10); "does not fail CONTROL" (F9 nit).
Drafts: the TM1986 STOP citations (F25 i); Appendix B attributed, the model's actual STOP behaviour stated (F25 ii, F42); the
(d) licence sentence replaced by OWED + the owner's decision (F39/F40/F25); the witness's superseded FIX column named (Q3 b).
Generator: numstat; the `probe:` term's wording; the hold question's closure trigger (Argon's answers, the owner's ruling
discharging the hold).  killtable_20261025/README.txt: (b) = L4; the licence wording.
