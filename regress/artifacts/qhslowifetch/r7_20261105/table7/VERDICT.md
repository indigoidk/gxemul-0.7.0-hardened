# qhslowifetch -- test-variant TABLE 7 (repair 7: 103 rows; no product change since repair 5), 2026-11-05 ~08:46-08:57Z

Driver `../table7_qhs.run.sh` (frozen copy of `../table7_qhs.sh`), run in two phases because one pass is ~450 s against the Bash
tool's 600 s cap: phase a (`../table7_run_a.log`) cloned build/ to /tmp/gxqhs13 under a clone-local .MUTANT sentinel, checked the
clone's sources against the baseline, ran the legs and variants 1-30 and put the baseline source back with the sentinel KEPT; phase
b (`../table7_run_b.log`) refused unless the sentinel and the baseline source were still there, ran variants 31-59, restored,
cmp-clean against GXEMUL-SEC, rebuilt fresh, and only then cleared the sentinel.  Every build `fresh`.  Instrument
`probe103_frozen.py` == `../base103/probe103_run.py` (cmp-checked by the driver; 103/103 on build/, `../base103/`).  Baseline
`../cpu_ppc_instr.c.fix7` == GXEMUL-SEC == table 6's fix6.  `../PRETABLE_7.out` was written before the driver ran; the frozen
probe is the only older file here (copied with `cp -p`, so it keeps the base-run copy's mtime).  Scores: `SCORES.txt`; the
mechanical comparison against PRETABLE_7: `COMPARE.out` (`../compare7.py`), **COMPARE7_MISSES=0**.

* **Legs, all exact.**  base 103/103, CONTROL=OK, SYMPTOM=ABSENT.  HEAD 40/103 (63 rows red), CONTROL=OK, SYMPTOM=PRESENT: the red
  set EQUALS the prediction (table 6's HEAD set + the 21 new rows), checked set-for-set.  Null media: /bin/true 41/103, an absent
  binary 24/103, /bin/false 25/103 -- each the predicted score, CONTROL=FAIL on all three.
* **Repair 7's thirteen, predicted EXACTLY, every one matching:**

  | variant | edit | score | red rows |
  |---|---|---|---|
  | R7_a_bit1 (codex B1) | guard && `!(cpu->pc & 2)` | 99/103 | nonex of `T ra o2`, `o2m`, `o3`, `o3m` |
  | R7_a_bit0 | guard && `!(cpu->pc & 1)` | 99/103 | nonex of `T ra odd`, `o1m`, `o3`, `o3m` |
  | R7_a_meun (codex B2) | guard && `(!ME \|\| pc == addr)` | 100/103 | nonex of `T ra o1m`, `o2m`, `o3m` |
  | R7_a_clun | guard && `(ME \|\| pc == addr)` | 100/103 | nonex of `T ra odd`, `o2`, `o3` |
  | R7_a_msrset (codex B3) | arm (a) sets ME when pc != addr | 100/103 | msr of `T ra odd`, `o2`, `o3` |
  | R7_a_msrclr | arm (a) clears ME when pc != addr | 100/103 | msr of `T ra o1m`, `o2m`, `o3m` |
  | R7_x_alcl | guard && !(aligned && ME clear) | 102/103 | `T ra nonex` |
  | R7_x_alme | guard && !(aligned && ME set) | 102/103 | `T ra me nonex` |
  | R7_x_uncl | guard && !(unaligned && ME clear) | 100/103 | nonex of `T ra odd`, `o2`, `o3` (= R7_a_clun, its De Morgan form) |
  | R7_x_unme | guard && !(unaligned && ME set) | 100/103 | nonex of `T ra o1m`, `o2m`, `o3m` (= R7_a_meun) |
  | R7_fail_unal (codex R3) | failure test `\|\| cpu->pc != addr` | 91/103 | pc and nonex of the six unaligned sessions |
  | R7_G1_b_lt (Gemini G1) | arm (b) `cpu->pc < addr` | 103/103 | none -- GREEN, as predicted (disclosed) |
  | R7_G2_d_msr (Gemini G2) | arm (d) `if (cpu->cd.ppc.msr)` | 103/103 | none -- GREEN, as predicted (disclosed) |

  So the closure holds on the composite: each of the four (aligned, unaligned) x (ME clear, ME set) cells, excluded ALONE from arm
  (a)'s guard, reds exactly its own sessions' nonex rows; each low pc bit tested alone reds exactly the sessions carrying it; an
  MSR write in arm (a) at pc != addr reds the msr rows of exactly the cells whose ME it flips; and the De Morgan pairs scored
  identically, which is a consistency check on the instrument.  Codex pass 6's three breaches (B1, B2, B3), 82/82 on the 82-row
  instrument (`../B123_NOTE.md`), are now caught, and R3's widening, a FILED disclosure until this repair, is caught by 12 rows.
* **Table 6's 46.**  The 30 predicted AT LEAST their table-6 sets all held -- and no deterministic variant's red set on the 82 old
  rows changed from table 6 (checked set-for-set); 22 of them also red new rows (informational: e.g. V9 adds the ME-clear `o2`,
  `o3` nonex rows, V8 the ME-set ones, R6_a_pceq/R6_a_align the five new unaligned nonex rows).  The eleven predicted GREEN (D6, D9,
  D10, D11, V2, V3, V4, V5, V6, R5_cb, R5_arun) stayed green.  The four BUILD-DEPENDENT variants are all red: W5_dec_tail 76/103
  (lost `T_ra_me_srr0` on the old rows), D7_dom_run 75/103 (gained it), V7_fail_inv 72/103 (old rows unchanged) and D12_else_ra
  87/103 (lost `T_ra_odd_pc`, gained `T_ra_me_pc` and `T_ra_srr0`) -- each moving within the read-ahead rows, as their disclosure
  says.  V12_fail_ra, NOT PREDICTED, reddened 14 rows (89/103): the `T ra`, `T ra odd`, `o1m`, `o2`, `o2m` and `o3` legs, gaining
  `T_ra_srr0`; its `T ra me` and `T ra o3m` legs stayed green -- the stale-word pattern again, counted in neither tally.
* **Tallies for the probe's clause (e):** 59 variants on the 103-row probe; 45 red, every one on this probe; 13 green, the
  predicted thirteen (the eleven above plus R7_G1_b_lt and R7_G2_d_msr); V12 NOT PREDICTED (red here).

No variant went undetected that PRETABLE_7 did not name in advance, and no prediction missed.
