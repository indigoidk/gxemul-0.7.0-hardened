# qhslowifetch -- test-variant TABLE 8 (repair 7b: 129 rows; no product change since repair 5), 2026-11-05 ~09:22-09:34Z

Driver `../table8_qhs.run.sh` (frozen copy of `../table8_qhs.sh`), two phases as for table 7: phase a (`../table8_run_a.log`)
cloned build/ to /tmp/gxqhs14 under a clone-local .MUTANT sentinel, checked the clone's sources against the baseline, ran the legs
and variants 1-34 and put the baseline source back with the sentinel KEPT; phase b (`../table8_run_b.log`) refused unless the
sentinel and the baseline source were still there, ran variants 35-67, restored, cmp-clean against GXEMUL-SEC, rebuilt fresh, and
only then cleared the sentinel.  Every build `fresh`.  Instrument `probe129_frozen.py` == `../base129/probe129_run.py`
(cmp-checked by the driver; 129/129 on build/ after both clearance checks, `../CLEARANCE.txt`'s repair-7b section).  Baseline
`../cpu_ppc_instr.c.fix7` == GXEMUL-SEC.  `../PRETABLE_8.out` was written before anything here (every file in this directory is
newer, the frozen probe included).  Table 7 stays the record of the 103-row probe.  Scores: `SCORES.txt`; the mechanical
comparison: `COMPARE.out` (`../compare8.py`), **COMPARE8_MISSES=0**.

* **Legs, all exact.**  base 129/129, CONTROL=OK, SYMPTOM=ABSENT.  HEAD 53/129 (76 rows red), CONTROL=OK, SYMPTOM=PRESENT: the red
  set EQUALS the prediction (table 7's HEAD set + the 13 new stopped and srr0 rows; the new addr and chkstop rows stay green on the
  pre-fix build, whose one halt report names 0xfec00008 before it exits).  Null media: /bin/true 47/129, an absent binary 30/129,
  /bin/false 31/129 -- each the predicted score, CONTROL=FAIL on all three.
* **Repair 7b's eight, every one as predicted:**

  | variant | edit | score | outcome |
  |---|---|---|---|
  | R7b_a_srr0un | arm (a) writes SRR0 when pc != addr | 123/129 | exactly the six unaligned srr0 rows |
  | R7b_a_chkun | the checkstop line printed when pc != addr | 123/129 | exactly the six unaligned chkstop rows |
  | R7b_a_pcalign | arm (a) aligns pc when pc != addr | 123/129 | exactly the six unaligned pc rows |
  | R7b_a_runun | arm (a) restores running when pc != addr | 129/129 | GREEN, as predicted (R5_arun's class) |
  | R7b_f_me | failure test `&& (msr & ME)` | 110/129 | 19 rows, all in T cont, T step, again, T ra, T ra odd, o2, o3 |
  | R7b_f_meclr | failure test `&& !(msr & ME)` | 113/129 | 16 rows, all in T me, T ra me, o1m, o2m, o3m |
  | R7b_f_ra | failure test `&& translation_readahead` | 93/129 | 36 rows, all in sessions with a non-read-ahead failing fetch |
  | R7b_f_unal | failure test `&& cpu->pc != addr` | 112/129 | 17 rows, all in T cont, T step, T me, again, T ra, T ra me |

  The first two were 103/103 on the 103-row probe (`../B123_NOTE.md`, repair 7b) -- the gaps the coordinator asked to close -- and
  are now caught by exactly the rows written for them.  The four failure-test narrowings (LATE_REPLICATIONS_20261105.md rows 33,
  41: never built in tables 1-7) are stack-decided in their rows, as PRETABLE_8 said, and each stayed inside its sessions; `T blr`
  stayed green under R7b_f_me and R7b_f_ra again (its stale word, by inference the `blr` just translated, loops on its own slot).
* **Table 7's 59.**  The 41 predicted AT LEAST their table-7 sets all held, and no deterministic variant's red set on the 103 old
  rows changed from table 7 (checked set-for-set).  The thirteen predicted GREEN stayed green.  The new rows show where the old
  variants also act -- W2 and D3 red every read-ahead addr row; B1 every new stopped row and the unaligned srr0 rows; D1 and D2
  the ME-clear unaligned chkstop rows and the ME-set unaligned srr0 rows (never `T me chkstop` or an ME-set read-ahead chkstop
  row); B2 the ME-clear unaligned chkstop rows; V11 the ME-set ones; R5_srr0_a all six unaligned srr0 rows; R7_fail_unal their
  addr rows, the ME-clear chkstop and the ME-set srr0 rows.  The four BUILD-DEPENDENT variants are red: W5_dec_tail 92/129 (on the
  103 old rows it regained `T_ra_me_srr0`), D7_dom_run 92/129 and V7_fail_inv 85/129 (old rows unchanged), D12_else_ra 113/129
  (dropped `T_ra_pc`, `T_ra_addr`, `T_ra_srr0`, `T_ra_o1m_pc`, `T_ra_o3_pc`, gained `T_ra_o2m_pc`).  V12_fail_ra, NOT PREDICTED,
  reddened 22 rows on every read-ahead leg except `T ra` and `T ra o2` -- counted in neither tally.
* **Tallies for the probe's clause (e):** 67 variants on the 129-row probe; 52 red, every one on this probe; 14 green, the
  predicted fourteen (table 7's thirteen and R7b_a_runun); V12 NOT PREDICTED (red here).

No variant went undetected that PRETABLE_8 did not name in advance, and no prediction missed.
