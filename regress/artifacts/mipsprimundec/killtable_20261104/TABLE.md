# mipsprimundec -- the detector's test-variant table (2026-11-04, the main loop)

**Instrument**: `regress/mips_primundec_probe.py`, 121 rows, frozen as `probe_frozen.py` (md5 in `MD5.txt`).  **Baseline**: the round's post-fix
working set `cpu_mips_instr.c.base` (= GXEMUL-SEC working tree, md5 ce746eea483f), cmp'd against the clone before variant 1 and rebuilt there
(`base` row = the freshness proof).  **Clone**: WSL `/tmp/gxmpukt`, a `cp -a` of `build/`, clone-local `.MUTANT`, cleared after the restore was
cmp'd against GXEMUL-SEC and rebuilt fresh (`RUN.log`).  **Order**: `PRETABLE.out` written 17:53:25Z, before the table started.
**Variants**: `mpu_variants.py` (exact-string edits, each asserted once; B5/B6 copy HEAD's own blocks verbatim).

| variant | score | sentinel | rows red | |
|---|---|---|---|---|
| base | 121/121 | yes | 0 | baseline |
| B1_lwc2swc2_del | 95/121 | yes | 26 | red |
| B2_ldc2sdc2_del | 99/121 | yes | 22 | red |
| B3_swc3_del | 104/121 | yes | 17 | red |
| B4_jalx_del | 109/121 | yes | 12 | red |
| B5_lwc3_head | 113/121 | yes | 8 | red |
| B6_mdmx_head | 113/121 | yes | 8 | red |
| D01_ldc2_le2 | 121/121 | yes | 0 | **ESCAPE** |
| D03_ldc2_lt4 | 119/121 | yes | 2 | red |
| D04_ldc2_ge2 | 115/121 | yes | 6 | red |
| D05_ldc2_nogate | 119/121 | yes | 2 | red |
| D06_ldc2_ce3 | 117/121 | yes | 4 | red |
| D07_lwc2_ce3 | 114/121 | yes | 7 | red |
| D08_swc3_ge4 | 120/121 | yes | 1 | red |
| D09_swc3_gt4 | 119/121 | yes | 2 | red |
| D10_swc3_eq3 | 118/121 | yes | 3 | red |
| D11_swc3_ge2 | 121/121 | yes | 0 | **ESCAPE** |
| D12_swc3_ge1 | 120/121 | yes | 1 | red |
| D13_swc3_ce2 | 120/121 | yes | 1 | red |
| D14_lwc3_le3 | 120/121 | yes | 1 | red |
| D15_pref_ge3 | 118/121 | yes | 3 | red |
| D16_pref_ge5 | 118/121 | yes | 3 | red |
| D18_lwc3_ce2 | 120/121 | yes | 1 | red |
| D19_r5900_inv | 113/121 | yes | 8 | red |
| D22a_jalx_nosync | 121/121 | yes | 0 | **ESCAPE** |
| D22b_lwc2_nosync | 121/121 | yes | 0 | **ESCAPE** |
| D23_ldc2_x64 | 119/121 | yes | 2 | red |
| D24_lwc2_x64 | 117/121 | yes | 4 | red |
| D25_swc2_label | 110/121 | yes | 11 | red |
| D26_sdc2_label | 110/121 | yes | 11 | red |

## Reading

* **Floor (a)** pre-fix: HEAD clone 28/121, CONTROL=OK, SYMPTOM=PRESENT (`../detector_20261104/detector121_head.out`).
* **Floor (b)** every removed defect reinstated verbatim at its site -- B1-B6 -- all red.
* **Floor (c)**: measured at `../wiring_20261104/null_true.out` and `null_absent.out` -- 16/121, CONTROL=FAIL each; the 16 green rows are the
  sixteen `stop` absence rows.  Gate 16 reds both through CONTROL=OK and the 121/121 equality pin (`../wiring_20261104/GATE16_REPLAY.out`).
* **Floor (d)**: every DEPENDS-ON variant red except the two ISA II edge moves, D01 (`< 2` -> `<= 2`) and D11 (`>= 3` -> `>= 2`): no ISA II CPU
  constructs on testmips, so the edge cell has no row.  PRETABLE predicted both escapes; the probe's contract discloses them, now citing them.
* **CHANNEL**, checked mechanically (prediction text expanded to row names, compared with the RED lists in `SCORES.txt`): 26 of the 27
  definite predictions match exactly.  B1's named two rows the probe does not have (`24k lwc2 stop`, `24k swc2 stop` -- the 24KEc sessions
  carry no stop row); every predicted row that exists went red and nothing else did.  The two variants PRETABLE marked MEASURE escaped:
* **D22a / D22b -- an RI or CpU raised without the PC sync -- 121/121.**  The probe's contract CLAIMED the delay-slot sessions catch that
  handler; measured false.  A single-stepped word's PC is already in sync when the handler runs, so the sync is invisible to this probe,
  delay slot included.  **Corrected in the probe's contract in-round** (construction, L1; docstring only -- the code's syntax tree equals the
  frozen copy's).  Fable's final ruling (r1 row 9; r2 rows 27-28) names the delay-slot rows' catch as this handler: **the question of
  whether a free-running PC-sync row is owed, or the class is disclosed, goes to the adjudicator.**
* **Gate 16 in situ** on the fixed build: PASS 289 checks (`../wiring_20261104/gate16.out`); the block's replay over all 34 logs is green on
  exactly the six 121/121 logs (`../wiring_20261104/GATE16_REPLAY.out`).

## Supplement (2026-11-04 18:4xZ) -- five variants the pass 2 named, and the ISA II premise

`mpu_variants2.py` (frozen beside this file; md5 in `MD5.txt`), the same clone recipe and baseline (`killtable2_mpu.run.sh`, `RUN2.log`),
`PRETABLE2.out` written 18:42:28Z before the run.  Every prediction held:

| variant | what | score | rows red |
|---|---|---|---|
| D27_lwc3_ge1 | the contract's "LWC3 `>= 1`" | 120/121 | 32 lwc3 exc |
| D28_swc3_eq4 | the contract's "SWC3 `== 4`" | 118/121 | 64, 24k, 5ke swc3 exc |
| D29_lwc3_iii_drop | the contract's "the ISA III RI arm for LWC3 dropped" | 120/121 | 64 lwc3 exc |
| D30_lwc3_ge2 | LWC3 `== 3` -> `>= 2` (pass 2: absent from table 1) | 121/121 **UNDETECTED** | -- (the ISA II cell, disclosed) |
| D31_r5900_false | the MDMX arm's R5900 test made always false (pass 2: absent) | 121/121 **UNDETECTED** | -- [corrected 2026-11-04: this cell said "(no R5900 session, disclosed)"; the R5900 DOES construct on testmips, and the 122-row probe reds D31 -- see the D31 section below] |

**The ISA II premise, measured** (`ISA2.txt`, `isa2_R6000.out`, `isa2_Allegrex.out`): the table's two ISA II CPUs do not construct on
`-E testmips` -- each exits 1 before the prompt with "Internal error: No initialization code for config0? cpu rev = 0x3" (R6000) / "0x0"
(Allegrex).  So the three undetected ISA II cells (D01, D11, D30) have no constructible session on this machine.  [Corrected 2026-11-04: this sentence said "the four undetected ISA II and R5900 cells (D01, D11, D30, D31) have no constructible session"; the R5900 was never tested here, and it constructs (`-E testmips -C R5900`: exit 0, the prompt reached; `_scratchpad/w_mpu/r5900_probe.out`, copied to `d31_20261104/`).  The premise reached cloud Fable's pass-2 adjudication packet, and its follow-up ruling corrected it.]
**Numbering gaps** in table 1, for traceability: D02 (`< 2` -> `< 3`) was not built, being the same edit as D01 for an integer level;
D17 (LWC3 `== 3` -> `>= 1`) was deferred and is now D27; D20 would have repeated B6; D21 (JALX re-routed to the CpU helper) is not a
weakening of any predicate the fix depends on.

## D31 row (2026-11-04 20:2xZ) -- cloud Fable's follow-up ruling, measured

Cloud Fable 5.1's follow-up (`../adj_20261104/ADJ2_D31_FABLE.md`, on the corrected premise): D31 is OWED a row in a form that does not pin the R5900's UNIMPLEMENTED stop -- `-C R5900`, step 0x1e, exit 0, the prompt reached, Reserved Instruction marker ABSENT -- with the fallback that, should the row not red under D31, D31 reverts to a policy disclosure.  The row is `r59 mdmx notRI` (the probe's 122nd).  Measured in the scratch clone `/tmp/gxmpud31` (`d31_20261104/d31_mpu.run.sh`, `RUN.log`), on the round's post-fix working set WITH the adjudicated product comments (`cpu_mips_instr.c.base122`; code identical to table 1's base with comments stripped), `PRETABLE_D31.out` written before the run, every prediction held:

| build | score | rows red |
|---|---|---|
| base122 (the fix) | 122/122, CONTROL=OK | none |
| D31 | 121/122 | `r59 mdmx notRI` only (it read `RI`) |
| HEAD | 29/122 | the 121-row HEAD set (28/121); the new row green -- HEAD's MDMX arm already sends the R5900 to its LQ branch |
| /bin/true | 16/122, CONTROL=FAIL | all but the sixteen `stop` rows (vacuous on empty output); the new row read `noread/exit0` |
| absent binary | 16/122, CONTROL=FAIL | as above; the new row read `noread/NOBIN(...)` |

**Catches: table 1 plus the supplement plus the D31 row, 29 of 34 variants red.**  Undetected and disclosed: D01, D11, D30 (the ISA II cells -- no constructible session) and D22a, D22b (the PC sync, invisible to a single-stepped probe).

**The question this table left open, ruled.**  Cloud Fable's pass-2 adjudication: D22 stays DISCLOSED (P20 annotates r1 row 9 and r2 rows 27-28 as superseded by measurement, `../adj_20261104/ANNOTATIONS.md`); a free-running PC-sync row is FILED in the shape Fable named (a breakpoint at the vector, reusing the exc/epc/pc reader), with its four-part admission test written as a prediction -- no seat owes it to this fix.

**Gate 16 in situ** with the 122-row probe on the fixed build: PASS 293 checks (`../wiring122_20261104/gate16.out`; 290 before the landing added the block's three denominator checks -- `rows run`, `rows green`, `rows red` -- in the form check_score_claims reads, as #578 and #579 have).  P16's replay (`../wiring122_20261104/gate16_replay122.sh`, extracted verbatim from the gate but for two marked lines; `GATE16_REPLAY122.out`): GREEN on the gate's log and on base122; RED on D31, HEAD and both dead legs; and RED on each of the four synthetic logs for its own reason -- a truncated log and a doubled sentinel fail the parse check, a line after the sentinel fails the last-line check, and a nonzero probe exit fails the exit check.

## The regress review, and what the landing measured for it

Cloud Fable's regress review (`../adj_20261104/FABLE_REGRESS.md`, Fable-only stage): 26 checks, 0 floor breaches, 2 record
findings, REGRESS-WITH-FINDINGS.

* **Record findings 1 and 2 (L4), applied in its words, docstring only.**  The catches clause said D15 "reds the 64 lwc3 rows"; it
  reds the 64 lwc3 exc, epc and pc rows (the stop row is an absence row and stays green: `SCORES.txt`, `D15_pref_ge3`).  And the
  clause omitted two measured catches: D16 (`>= 5`: the R5000 session takes CpU, `RED=r5k_lwc3_exc,r5k_lwc3_epc,r5k_lwc3_pc`) and
  D24 (x64 set on the LWC2/SWC2 arm: `RED=32_lwc2_exc,32_swc2_exc,24k_lwc2_exc,24k_swc2_exc`).  The probe's docstring-stripped
  syntax tree is unchanged (`SOURCE_IDENTITY.md`, regenerated: equal to `d31_20261104/probe122_frozen.py`'s).
* **UNSETTLED 1** (the shipped probe against the measured 122-row copy): that was P19's record, `SOURCE_IDENTITY.md`, which the
  review's packet did not carry; regenerated after the docstring edit, still equal.
* **UNSETTLED 2** (the gate totals): consistent, and the packet was what misled.  Its line put the 293 beside the 80-row witness;
  293 is gate 16 with the 122-row probe.  289 (`../wiring_20261104/gate16.out`) = 161 other checks + the 121-row block's 128;
  293 (`../wiring122_20261104/gate16.out`) = the same 161 + 132 (122 rows, 7 block checks, the 3 denominator checks); the 161
  non-block check lines of the two runs diff empty.  A fresh in-situ run on the final bytes (probe md5 `dae62682`, the docstring
  corrections in): PASS 293, 0 FAIL, 122 rows ok, every check line identical to the earlier 293 run
  (`../landing_20261104/gate16_final.out`, `gate16_final.time`, `MD5_gate16_final.txt`).
* **Its extra null medium, measured instead of filed.**  The review predicted that `/bin/false` (exit 1, no output) greens the
  sixteen stop rows and the neg row, 17/122, CONTROL=FAIL.  Written down before the run (`../landing_20261104/PREDICTION_false.md`,
  14:37:17 local, two seconds before `false.out`) and measured on the shipped probe: **17/122, CONTROL=FAIL**, the green rows
  exactly the neg row and the sixteen stop rows (`../landing_20261104/false.out`).  A third dead leg beside `/bin/true` and the
  absent binary; no row was owed and none was added.
