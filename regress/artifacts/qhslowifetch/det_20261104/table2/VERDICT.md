# qhslowifetch -- test-variant table 2: verdict against PRETABLE_2

Instrument: `probe56_frozen.py` (56 rows, md5 0cae1c8e2884). Baseline: `../cpu_ppc_instr.c.fix3` + `../cpu_ppc.h.fix`, the final
candidate, cmp-equal to GXEMUL-SEC. Run in the WSL clone /tmp/gxqhs2. Record: `SCORES.txt` in this directory, where every line names
the row count it ran on (FINAL_FABLE.md F8). `../PRETABLE_2.out` was written first: its mtime precedes this directory's files.

- **Legs**: base 56/56, CONTROL=OK, SYMPTOM=ABSENT. The HEAD leg scored 33/56 with SYMPTOM=PRESENT and CONTROL=OK (predicted 33/56).
  /bin/true scored 27/56, an absent binary 18/56 and /bin/false 19/56, each with CONTROL=FAIL.
- **Red: 18 of 27 variants.** B1 (33/56, identical to the HEAD leg), W2, W3, W4, W5, D1, D2, D3, D4, D5, D7, D8, D12, D13, D14, D15,
  W7 and V7.
- **Green: 9 of 27, every one in a cell measured unreached on pmppc.** D6, D9, D10, V4, V5 and V6 edit arm (d) or the checkstop
  fallback: no fetch reaches them at any 4-byte offset of any device window (`../window_sweep.out`) or in the slack above RAM
  (`../slack_sweep.out`). D11 and V2 edit arm (b), which no measured session reaches. V3 forces arm (c)'s guard true, which changes
  nothing on pmppc, because every failing fetch that reaches arm (c) already has running at 0.
- **The read-ahead rows caught two variants table 1 could not.** *(Corrected 2026-11-05, repair-pass-2 adjudication Q14: this said "row"; W7 is caught by `T ra nonex` and D12 by three `T ra` rows.)* W7 (arm (a)'s guard deleted) scored 55/56 with RED=T_ra_nonex, and D12
  (the slow path skipped during read-ahead) scored 53/56. Both were disclosed as unreachable until the window sweep found cpc700_pci's
  read-ahead (FINAL_FABLE.md F4).
- **Every enumerated variant kept CONTROL=OK.** None moved any of the 19 controls.
- **Prediction misses** are recorded in `../PRETABLE_2.errata.md`. They are W5 and D7 (13 red where 11 were predicted) and D12 (the
  same count with a different row set). Each is red either way, so none changes a catch.
- **The clone was restored**: cmp clean against GXEMUL-SEC, binary fresh, sentinel cleared (the run log's last lines).
