# qhslowifetch -- test-variant TABLE 5 (repair 5: the aligned compare in arm (b); 79 rows), 2026-11-05

Driver `../table5_qhs.run.sh` (frozen copy of `table5_qhs.sh`), scratch clone /tmp/gxqhs8 under a clone-local .MUTANT sentinel, cleared
only after the restore cmp'd against GXEMUL-SEC and rebuilt fresh (table5_run.log, last lines).  Instrument `probe79_frozen.py` (the
in-tree probe after `_scratchpad/w_qhs/apply_r5.py`).  Baseline `../cpu_ppc_instr.c.fix5` (== GXEMUL-SEC).  `../PRETABLE_5.out` was
written before the driver started (its mtime precedes every file in this directory).  Scores: `SCORES.txt`; per-variant raw logs beside it.

* base 79/79, CONTROL=OK, SYMPTOM=ABSENT.
* HEAD 40/79, CONTROL=OK, SYMPTOM=PRESENT -- the red set EQUALS the prediction (table 4's HEAD set + T_blr_session, T_blr_pc, T_blr_srr0,
  T_blr_msr, T_blr_lr + T_ra_srr0, T_ra_me_srr0; checked set-for-set, nothing predicted-only, nothing measured-only).
* null media (null_true, null_absent, null_false): CONTROL=FAIL on all three.
* Repair 5's six, each predicted EXACTLY in PRETABLE_5 and each matching: R5_revert, R5_mask1, R5_mask2 -> T_blr_nonex only (78/79);
  R5_srr0_a -> T_ra_srr0, T_ra_me_srr0 (77/79); R5_cb 79/79 (EQUIVALENT, as predicted: running is 0 at each -T entry); R5_arun 79/79
  (the pass-4 review's arm (a) finding, DISCLOSED, predicted green).
* Table 4's 36, adapted to fix5: every one kept its whole table-4 red set (0 of 36 lost a row); the nine green in table 4 (D6, D9, D10,
  D11, V2, V3, V4, V5, V6 -- the disclosed classes) are green again.  V12 (NOT PREDICTED) is red, 74/79 (T_ra_pc, T_ra_nonex,
  T_ra_addr, T_ra_me_pc, T_ra_me_nonex).  D12 (BUILD-DEPENDENT) is red, 74/79.  New rows reddened by old variants (informational):
  T_blr_* under W2, W3, W4, D1, D2, D3, D5, D14, B1c; T_ra_srr0/T_ra_me_srr0 under W4, W5, D1, D2, D7, D8, D12, D13, D15, V7.
* D4_b_inv's adapted form is the UNMASKED inverse `if (cpu->pc == addr)` (its replacement text carries no old test to rewrite), so
  T blr's unaligned pc does not take arm (b) under it and T_blr_nonex stays green; D4 is red on its table-4 rows.  The MASKED inverse
  `(pc & ~3) == addr` is not in the table.

No variant went undetected that PRETABLE_5 did not name in advance (R5_cb equivalent; R5_arun and the nine disclosed).
