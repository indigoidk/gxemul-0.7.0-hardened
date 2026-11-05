# qhslowifetch -- test-variant TABLE 10 (repair 9: 153 rows; no product change since repair 5), 2026-11-05 ~10:25-10:35Z

Driver `../table10_qhs.run.sh` (frozen copy of `../table10_qhs.sh`), two phases as for tables 7-9: phase a (`../table10_run_a.log`)
cloned build/ to /tmp/gxqhs16 under a clone-local .MUTANT sentinel, checked the clone's sources against the baseline, ran the legs
and variants 1-37 and put the baseline source back with the sentinel KEPT; phase b (`../table10_run_b.log`) refused unless the
sentinel and the baseline source were still there, ran variants 38-74, restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, and
only then cleared the sentinel.  Every build `fresh`.  Instrument `probe153_frozen.py` == `../base153/probe153_run.py`
(cmp-checked by the driver; 153/153 on build/ after both clearance checks, `../CLEARANCE.txt`'s repair-9 section).  Baseline
`../cpu_ppc_instr.c.fix7` == GXEMUL-SEC.  `../PRETABLE_10.out` was written before anything here.  Table 9 stays the record of the
137-row probe.  Scores: `SCORES.txt`; the mechanical comparison: `COMPARE.out` (`../compare10.py`), **COMPARE10_MISSES=0**.

* **Legs, all exact.**  base 153/153, CONTROL=OK, SYMPTOM=ABSENT.  HEAD 67/153 (86 rows red), CONTROL=OK, SYMPTOM=PRESENT: the red
  set EQUALS the prediction (table 9's + `T blr o1` / `T blr o2`'s session, pc, srr0, msr and lr rows).  Null media: /bin/true
  61/153, an absent binary 42/153, /bin/false 43/153 -- each the predicted score, CONTROL=FAIL on all three.
* **Repair 9's five, predicted EXACTLY, every one matching:** R9_tog_me1 (pass 8's B1, an MSR[ME] toggle on low bits 01 at the top of
  the failed-read block) 152/153 -- `T blr o1 msr`; R9_tog_me2 (its `== 2` form) 152/153 -- `T blr o2 msr`; R9_tog_me0 149/153 --
  the msr rows of `T cont`, `T step`, `T me` and `again`; R9_tog_me3 152/153 -- `T blr msr`; R9_tog_srr0_1 (an SRR0 toggle on 01)
  152/153 -- `T blr o1 srr0`.  R9_tog_me1, R9_tog_me2 and R9_tog_srr0_1 were 137/137 on the 137-row probe (`../B123_NOTE.md`, repair
  9): the two-entry read-ahead sessions toggle twice and cancel; the one-entry sessions see one toggle.  R9_tog_me0 and R9_tog_me3
  were already caught (133/137, 136/137): the 00 and 11 one-entry cells existed before repair 9.
* **Table 9's 69.**  The 46 predicted AT LEAST their table-9 sets all held, and no deterministic variant's red set on the 137 old
  rows changed; the fourteen predicted GREEN stayed green; the four BUILD-DEPENDENT variants are red (W5_dec_tail, D7_dom_run and
  D12_else_ra moved again among the read-ahead rows; V7_fail_inv did not); the four failure-test narrowings stayed inside their
  sessions -- the two whose scope now includes `T blr o1` and `T blr o2` (R7b_f_me, R7b_f_ra) left them green, as they leave `T blr`
  (by inference its stale word, the `blr` just translated, loops on its own slot); V12_fail_ra, NOT PREDICTED, reddened 17 rows,
  every read-ahead leg except `T ra`, `T ra me` and `T ra o1m` -- counted in neither tally.  The old variants that also red the new
  rows are the ones that act on `T blr`: the mask and revert variants of arm (b) (R5_mask1 on `T blr o2`, R5_mask2 on `T blr o1`,
  R5_revert, R6_mask7, R6_mask15 on both), W2, W3, W4, D1, D2, D3, D5, D14, B1, B1c and R8_c_clun_bad.
* **Tallies for the probe's clause (e):** 74 variants on the 153-row probe; 59 red, every one on this probe; 14 green, the
  predicted fourteen; V12 NOT PREDICTED (red here).

No variant went undetected that PRETABLE_10 did not name in advance, and no prediction missed.
