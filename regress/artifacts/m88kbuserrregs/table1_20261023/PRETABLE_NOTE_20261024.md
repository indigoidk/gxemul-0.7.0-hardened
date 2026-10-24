# PRETABLE.out -- dated note, 2026-10-24

T36 / `#570` pre-commit repair (`../pass2_20261023/PASS2_RULINGS.md` D5 and section E; `../pass2_20261023/REPAIR_SPEC.md`
sections 4 and 7).  `PRETABLE.out` is **not edited**: its mtime (2026-10-23 22:28:08 -0500, before table 1's first leg) is
the order proof.  What pass 2 found about it is recorded here, beside it.

## 1. L22's prediction is not in PRETABLE.out

L22 ("the LUNA case deleted") is in neither the PRETABLE body nor AMENDMENT 1.  Its prediction is at
`BUILDER_QUESTIONS.md:135-138` (Q18: "luna route, pfsr, pfar and icmmu red through `prereq:handler`, 27/31"; file mtime
2026-10-23 22:29:30 -0500), approved at `../pass1_20261023/BUILD_SPEC.md:233-234` (section 11 Q18; file mtime 22:31:49).
The leg was built at 23:08:15 (`L22.diff`) and measured at 23:08:43 (`L22_casedel.out`: 27/31, red set
`luna route, luna pfsr, luna pfar, luna icmmu`), after both.  `SCORES.txt` line 4's criterion now names this source as well.

## 2. Draft question ids -> final ids

`PRETABLE.out` cites `BUILDER_QUESTIONS.md` by a DRAFT numbering; the final file renumbered the questions.

| PRETABLE.out reference | subject | final id |
|---|---|---|
| body `:293` "Q5" | L20 behaves like L4 | Q13 |
| body `:207`, `:274` "Q6"; AM-4 `:415` "[Q12]" | L6b, the always-instruction selector | Q16 |
| body `:284` "Q7"; AM-4 `:419` "[Q13]" | L16, which device is excluded | Q17 |
| body `:287` "Q8" | L18's form | Q14 |
| body `:122` "Q9" | a "case deleted" leg | Q18 |
| AM-5 `:425` "[Q7: CONTROL_ROWS or not]" | `ifetch route` as a CONTROL | Q8 |

These already match their final ids: body `:45` Q1; AM-1 `[Q1]` `:371`, `[Q3]` `:374` and `[Q4]` `:386`; `[Q2]` `:381`
(AM-1) and `:449` (AM-7); AM-4 `[Q14]` `:420` and `[Q15]` `:418`; AM-6 `[Q9]` `:443` and the unbracketed Q4 at `:444`.

Body `:329` "Q10" has **no final counterpart**.  It qualified the body's sentence "instruction x NULL is not rowed", and
AMENDMENT 1 replaced that design (AM-1, AM-2: `null surv` holds the instruction x CMMU-absent cell).  Final Q10 is SYMPTOM.

## 3. AMENDMENT 1's time

The heading at `PRETABLE.out:362` says "2026-10-23 ~22:3x -0500".  The file's mtime is 22:28:08.  Both are recorded as
they stand.  This note does not reconcile them, and nothing is backdated.

## 4. R-d and AM-7 are SUPERSEDED

R-d (`PRETABLE.out:351-353`) says the design "pauses cpu 0 before cpu 1 runs".  AM-7 (`:446-447`) says "R-c/R-d stand".
The probe as built does not pause cpu 0.  cpu 0 runs its 19 steps and parks in H's `br .`, where it **remains running**,
as AM-1 itself says at `:372`.  The session sends `pause 1`, which starts cpu 1, and **never** `pause 0`.  See rev 2,
the frozen artifact of record, at `m88k_buserr_probe.rev2.frozen.py.txt:711-715` (the `pause 1` is at `:714`).  In the
shipped documentation revision 2c the same lines are `regress/m88k_buserr_probe.py:723-727` (`:726`).

## 5. CL7 establishes data delivery only

CL7 (`PRETABLE.out:99`) maps the comment's "... and still takes the exception" to `null route`.  That row scores only the
**data** label's delivery: cpu 1's vector 3, with HANDLED set, FELL clear, SXIP and DMA0.

Instruction-access delivery on a CMMU-less cpu is **unscored**.  `null surv` scores survival through part 2's refused
fetch, not the vector taken.  The INFO null cpu0 line prints cpu 1's end pc, unscored.

The product comment was narrowed to match (`memory_rw.c`'s `#570` comment, B5, in `../repair1_20261024/product_comments.diff`),
and the probe's contract now says so (documentation revision 2c).

## 6. "No leg in the table builds 'case deleted'" is superseded by L22

`PRETABLE.out:121-122` says no leg builds "case deleted" (CL15's counterfactual).  BUILD_SPEC section 11 Q18 added L22,
which does exactly that.  It measured 27/31 as predicted (`SCORES.txt`, `L22_casedel.out`).
