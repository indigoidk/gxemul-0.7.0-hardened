# qhslowifetch -- test-variant TABLE 6 (repair 6: 82 rows; no product change since repair 5), 2026-11-05

Driver `../table6_qhs.run.sh` (frozen copy), WSL scratch clone /tmp/gxqhs11 under a clone-local .MUTANT sentinel; restored, cmp-clean
against GXEMUL-SEC, rebuilt fresh, sentinel cleared (table6_run.log).  Instrument `probe82_frozen.py` == the in-tree probe after
apply_r6.py (82/82 on build/, base82/).  Baseline `../cpu_ppc_instr.c.fix6` (== GXEMUL-SEC: the qhs fix with repair 5, plus #575's two
crandc/crorc lines, which no qhs session executes).  `../PRETABLE_6.out` was written before the driver (the only older file here is
the frozen probe, copied first).  Scores: SCORES.txt.

* base 82/82, CONTROL=OK, SYMPTOM=ABSENT.  HEAD 40/82, CONTROL=OK, SYMPTOM=PRESENT: the red set EQUALS the prediction (table 5's
  HEAD set + T_ra_odd_session, T_ra_odd_pc, T_ra_odd_nonex), checked set-for-set.
* Null media: /bin/true 36/82, an absent binary 24/82, /bin/false 25/82 -- CONTROL=FAIL on all three.
* Repair 6's four, predicted EXACTLY, each matching: R6_mask7 -> T_blr_nonex (81/82); R6_mask15 -> the nonex rows of T ra, T ra me,
  T ra odd and T blr (78/82); R6_a_pceq and R6_a_align -> T_ra_odd_nonex (81/82 each).  These are pass 5's two measured breaches
  (p5_20261105/MASK7_NOTE.md, TRAODD_NOTE.md), now caught.
* Table 5's 42: every one red that was red before, the predicted nine (plus R5_cb and R5_arun) green.  FOUR moved within their
  documented classes rather than keeping their table-5 rows: W5_dec_tail (lost T_ra_srr0, gained T_ra_me_srr0), D7_dom_run (lost
  T_ra_me_srr0), D12_else_ra (lost T_ra_srr0) and V12_fail_ra (lost the T ra me rows, gained the T ra odd rows).  All four ride on
  the uninitialised or stale instruction word (the probe's clause (e): W5, D7, V7 and D12 are BUILD-DEPENDENT; V12 NOT PREDICTED),
  and every one is still red.  PRETABLE_6 exempted D12 and V12 but predicted W5 and D7 "at least" their table-5 sets -- that
  wording was WRONG for two build-dependent variants (the claim the probe makes for them is "some row reds", which holds).
* Old variants that also red a T ra odd row (informational): B1, D12, D15, D3, D5, D7, R5_mask2, R5_revert, V12, V7, V9, W2, W4, W5, W7.

No variant went undetected that PRETABLE_6 did not name in advance (R5_cb equivalent; R5_arun and the nine disclosed).

*Corrected 2026-11-05 (main loop): this file's time-of-day stamp(s) (removed: ~08:5xZ) were GUESSES from the main loop's wrong clock -- later than this file's own creation time, so impossible as written.  The file's own timestamps are the record: created 07:57Z, last written 07:57Z before this note (UTC).*
