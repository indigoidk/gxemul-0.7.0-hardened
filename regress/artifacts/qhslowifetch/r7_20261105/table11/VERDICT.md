# qhslowifetch -- test-variant TABLE 11 (repair 10: 177 rows; no product change since repair 5), 2026-11-05 ~10:48-11:00Z

Driver `../table11_qhs.run.sh` (frozen copy of `../table11_qhs.sh`), two phases as for tables 7-10: phase a (`../table11_run_a.log`)
cloned build/ to /tmp/gxqhs17 under a clone-local .MUTANT sentinel, checked the clone's sources against the baseline, ran the legs
and variants 1-40 and put the baseline source back with the sentinel KEPT; phase b (`../table11_run_b.log`) refused unless the
sentinel and the baseline source were still there, ran variants 41-79, restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, and
only then cleared the sentinel.  Every build `fresh`.  Instrument `probe177_frozen.py` == `../base177/probe177_run.py`
(cmp-checked by the driver; 177/177 on build/ after both clearance checks, `../CLEARANCE.txt`'s repair-10 section).  Baseline
`../cpu_ppc_instr.c.fix7` == GXEMUL-SEC.  `../PRETABLE_11.out` was written before anything here.  Table 10 stays the record of the
153-row probe.  Scores: `SCORES.txt`; the mechanical comparison: `COMPARE.out` (`../compare11.py`), **COMPARE11_MISSES=0**.

* **Legs, all exact.**  base 177/177, CONTROL=OK, SYMPTOM=ABSENT.  HEAD 76/177 (101 rows red), CONTROL=OK, SYMPTOM=PRESENT: the red
  set EQUALS the prediction (table 10's + `T blr m1` / `m2` / `m3`'s session, pc, srr0, msr and lr rows).  Null media: /bin/true
  70/177, an absent binary 48/177, /bin/false 49/177 -- each the predicted score, CONTROL=FAIL on all three.
* **Repair 10's five, predicted EXACTLY, every one matching:** R10_tog_srr0_meun (pass 9's B1, an SRR0 toggle gated on MSR[ME] and
  pc != addr) 174/177 -- the srr0 rows of `T blr m1`, `T blr m2`, `T blr m3`; R10_tog_srr0_me1 / _me2 / _me3 176/177 each -- one of
  those rows each; R10_tog_srr0_2 (R2's own variant, the 10 toggle) 175/177 -- `T blr o2 srr0` and `T blr m2 srr0`.  The first four
  were 153/153 on the 153-row probe (`../B123_NOTE.md`, repair 10): the two-entry ME-set read-ahead sessions toggle twice and cancel,
  and before repair 10 no unaligned one-entry failure was ME-set.
* **Table 10's 74.**  The 51 predicted AT LEAST their table-10 sets all held, and no deterministic variant's red set on the 153 old
  rows changed; the fourteen predicted GREEN stayed green; the four BUILD-DEPENDENT variants are red; the four failure-test
  narrowings stayed inside their sessions (R7b_f_meclr and R7b_f_ra, whose scopes now include `T blr m1`-`m3`, left them green, as
  they leave `T blr`); V12_fail_ra, NOT PREDICTED, reddened 25 rows, every read-ahead leg except `T ra o2` -- counted in neither
  tally.  The old variants that also red the new rows are those acting on a one-entry ME-set or unaligned halt: the arm (b) mask
  and revert variants, W2, W3, W4, D1, D2, D3, D5, D8, D13, B1, B1a, V10, V11, R8_c_meun_bad, R9_tog_me1/2/3 and R9_tog_srr0_1.
* **The grid is held whole** -- every (low bits, ME) cell has a two-entry and a one-entry failure session: 00 clear `T ra` /
  `T cont`, `T step`, `again`; 00 set `T ra me` / `T me`; 01 clear `T ra odd` / `T blr o1`; 01 set `T ra o1m` / `T blr m1`; 10 clear
  `T ra o2` / `T blr o2`; 10 set `T ra o2m` / `T blr m2`; 11 clear `T ra o3` / `T blr`; 11 set `T ra o3m` / `T blr m3`.
* **Tallies for the probe's clause (e):** 79 variants on the 177-row probe; 64 red, every one on this probe; 14 green, the
  predicted fourteen; V12 NOT PREDICTED (red here).

No variant went undetected that PRETABLE_11 did not name in advance, and no prediction missed.
