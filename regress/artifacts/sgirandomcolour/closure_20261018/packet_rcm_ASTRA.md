**Your token: `ASTRA_RCMICRO_20261018`** -- open your answer with it.

# `sgirandomcolour`'s closure records -- pass 3, the confirm: only what changed after the delta pass

## 0. What this is

Pass 2 (the delta, `packet_rcd_ASTRA.md` beside this file; its answers are `codex_rcdelta.txt`, `grok_rcdelta.txt`,
`glm_rcdelta.txt`) raised six flags.  Each was settled -- four applied, two refuted by reading the source or the project
carrier -- and the records were rebuilt.  This pass confirms ONLY those changes.  The tree is
`C:/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC` at HEAD 620ddd09; the corrections are NOT in its files yet (they are below).
READ-ONLY: write nothing to any project tree.  Evidence E1-E6 are in `packet_rcd_ASTRA.md`.

## 1. The changes, M1..M6, each with the flag that prompted it

**M1 -- refutes GLM delta FLAG 1, and makes the refutation visible.**  GLM: *"'The amendment's trigger is two
consecutive passes finding BREACHES of one class' appears in no exhibit ... settling fact: the amendment's trigger
sentence."*  The settling fact: the project carrier `C:/DocumentNoSnc/cc/GXEMUL/CLAUDE.md` reads *"WHEN TWO CONSECUTIVE
PASSES FIND BREACHES OF ONE CLASS, THE NEXT REPAIR OWES THE CLASS CLOSURE"*, and the row note itself quotes it in the
sentence right after the one D1 sits beside (*"It says: when two consecutive passes find breaches of ONE CLASS ..."*).
D1 now reads:

> it does not.  The amendment's trigger is two consecutive passes finding BREACHES of one class (its own words, quoted
> next), and M28 is not a breach: it slices WITHIN the one `default:` label that twelve nibbles share, which the
> ruling's table grades clause (e) ('already so ruled') and this note's own partition table, further down, says too.
> The colour-mode closure that followed was L1 strengthening.

**M2 -- applies GLM delta FLAG 3** (the ruling's wording is "equivalent to the fix", E1:99).  In three places the text
now reads *"`if (ok || (tileptr & 0xfff00000))` is equivalent to the fix on every driven row, by inspection"*: the
row note's D7 (pass 1's C4), the probe's end-of-historical-part note, and the RESIDUALS.md R5 note.

**M3 -- applies Grok delta FLAG 1** (D8's "should die" still stated an unmeasured kill).  D8 now reads:

> each slice is predicted one-row closable (derived, never run: an uninitialised-buffer kill needs a run, since an
> identical-byte write is invisible) and only the FAMILY is not, so 'closable by a finite row set' discriminates
> nothing (the 2026-09-04 finiteness bound under a new name); they are clause (e) because the body does not test them
> as a case.

**M4 -- refutes GLM delta FLAG 2, and sharpens the wording.**  GLM: *EXHAUSTED for `tlb_mode` fails unless a row drives
`tlb_mode` in {3,5,6,7}.*  The settling fact: in `src/devices/dev_sgi_re.c` at HEAD the `tlb_mode` switch's `default:`
arm ends in `return;` (after its latched `fatal()`), before the guarded store -- and the probe's own EXHAUSTED list says
*"tlb_mode {0,1,2,4} 4 of 4 (the other four return before the store)"*.  The probe note's last sentence now reads:

> And EXHAUSTED above means every cell of the BODY-TESTED partition of that lvalue is rowed -- not every value of its
> reachable domain, though for these three the two coincide (tiny domains; tlb_mode's other four values return before
> the store).  ***

**M5 -- applies Grok delta FLAG 2: a NEW note in `tools/pipeline/fable_queue.md`**, after the 7n-5 entry's third
paragraph (the "AND A THIRD CASE ... predicted **77/77**." paragraph), beside the "GRADED FLOOR" / "GRADED DEBT" bullets
and that paragraph.  The entry's struck heading already carries the 2026-10-09 answer.  The note:

> *[CORRECTED 2026-10-18 at the row's closure, by this entry's own answer (the heading above;
> `regress/artifacts/fablequeue7n_20261009/fable5_rule7n_35.md`): the GRADED FLOOR bullet was wrong as a grade -- the
> tile-index family is clause (e), like the value slices and the TLB contents -- and the closure it credits was L1
> strengthening on a severity warrant.  "Not closable by any finite row set" separates nothing: each slice is predicted
> one-row closable (derived, never run) and only the family is not.  The contents slice is coverage debt, not owed:
> `if (ok || (tileptr & 0xfff00000))` is equivalent to the fix on every driven row, by inspection.]*

**M6 -- applies GLM delta FLAG 4** (the GLM review entry credited pass 1's C1 with a fix it did not contain).  The entry
now reads: *"... its Q2 risk (c), that the row-note heading still called the 59-row instrument SHIPPED after C1 --
corrected by extending C1."*

Also: the probe's end note and the RESIDUALS.md note were re-flowed to their files' line widths (wording otherwise as
M2-M4).  Every probe edit remains a comment; the module's syntax tree is byte-identical before and after.

## 2. Questions

**Q1.**  For EACH of M1..M6: `M<n>: CORRECT | WRONG | NEW DEFECT -- <why>`, with the evidence.  For M1 and M4, check the
two refutations yourself against the carrier text and the source named above.

**Q2.**  `tools/pipeline/fable_queue.md`'s 7n-5 entry: does anything ELSE in that entry still assert a floor grade or an
owed repair without a correction beside it after M5?

**Q3.**  Name the ONE change most likely to be wrong -- or say none, with the check that rules each out.

**Format:** the token, then ONE line `VERDICT: <n> flags -- <one line>`, then Q1..Q3.  Every defect is a line starting
`FLAG:`.  Facts and flags only.
