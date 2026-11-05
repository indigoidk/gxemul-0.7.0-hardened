# qhslowifetch -- test-variant TABLE 9 (repair 8: 137 rows; no product change since repair 5), 2026-11-05 ~09:53-10:05Z

Driver `../table9_qhs.run.sh` (frozen copy of `../table9_qhs.sh`), two phases as for tables 7 and 8: phase a (`../table9_run_a.log`)
cloned build/ to /tmp/gxqhs15 under a clone-local .MUTANT sentinel, checked the clone's sources against the baseline, ran the legs
and variants 1-35 and put the baseline source back with the sentinel KEPT; phase b (`../table9_run_b.log`) refused unless the
sentinel and the baseline source were still there, ran variants 36-69, restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, and
only then cleared the sentinel.  Every build `fresh`.  Instrument `probe137_frozen.py` == `../base137/probe137_run.py`
(cmp-checked by the driver; 137/137 on build/ after both clearance checks, `../CLEARANCE.txt`'s repair-8 section).  Baseline
`../cpu_ppc_instr.c.fix7` == GXEMUL-SEC.  `../PRETABLE_9.out` was written before anything here.  Table 8 stays the record of the
129-row probe.  Scores: `SCORES.txt`; the mechanical comparison: `COMPARE.out` (`../compare9.py`), **COMPARE9_MISSES=0**.

* **Legs, all exact.**  base 137/137, CONTROL=OK, SYMPTOM=ABSENT.  HEAD 61/137 (76 rows red), CONTROL=OK, SYMPTOM=PRESENT: the red
  set EQUALS table 8's (the pre-fix build exits at the read-ahead fetch with `read failed: TODO`, not UNIMPLEMENTED, so the eight
  new unimpl rows stay green).  Null media: /bin/true 55/137, an absent binary 38/137, /bin/false 39/137 -- each the predicted
  score, CONTROL=FAIL on all three.
* **Repair 8's two, predicted EXACTLY, both matching:** R8_c_meun_bad (pass 7's F1: arm (c) sends a halt with MSR[ME] set at
  pc != addr to bad:) 134/137 -- the unimpl rows of `T ra o1m`, `T ra o2m`, `T ra o3m`; it was 129/129 on the 129-row probe
  (`../B123_NOTE.md`, repair 8).  R8_c_clun_bad (its ME-clear mirror) 133/137 -- those of `T ra odd`, `T ra o2`, `T ra o3` and `T blr
  unimpl`, which alone caught it before.
* **Table 8's 67.**  The 44 predicted AT LEAST their table-8 sets all held; the fourteen predicted GREEN stayed green; the four
  BUILD-DEPENDENT variants are red (W5_dec_tail 91/137, D7_dom_run 97/137, V7_fail_inv 89/137, D12_else_ra 115/137; W5, D7 and D12
  moved again among the read-ahead rows: W5 traded `T_ra_me_srr0` and `T_ra_o2_srr0` for `T_ra_srr0`, `T_ra_o2m_srr0` and
  `T_ra_o3_srr0`, D7 traded `T_ra_me_srr0`, `T_ra_o3_srr0` and `T_ra_odd_srr0` for `T_ra_srr0` and `T_ra_o1m_srr0`, D12 lost the two
  `T_ra_o3m` pc/addr rows and gained eight pc/addr rows); the four failure-test narrowings stayed inside their sessions (23, 17, 38
  and 16 rows); V12_fail_ra, NOT PREDICTED, reddened 24 rows on every read-ahead leg -- counted in neither tally.  The new unimpl
  rows also show the old variants that reach bad: or a zero-word vector on the read-ahead route: W3, W4 and W5 red all eight; V10,
  D1, D2, D8, D13, D15 and V7 the four ME-set ones (V10 sends the halt to bad:; the others' machine check lands on the zero word at
  vector 0x200); R7_fail_unal the three unaligned ME-set ones, for the same reason; D7 and the failure-test narrowings some,
  stack-decided.
* **Tallies for the probe's clause (e):** 69 variants on the 137-row probe; 54 red, every one on this probe; 14 green, the
  predicted fourteen; V12 NOT PREDICTED (red here).

No variant went undetected that PRETABLE_9 did not name in advance, and no prediction missed.
