STATIC / OFFLINE MATERIAL (no mutant scores here -- those come only from KTR5*.out)

Records verified by reading:
- fix5.diff changed lines == SEC working-tree diff (9 hunks), sorted-line compare clean.
- killtable5: 110 mutant RESULT lines, 104 distinct names, only M_msr_argmask 47/47; 16 baselines 47/47.
  Six shared names: H_narrow_17 textually identical; the other five textually different, semantically equal.
- frozen (8a9a9cac) vs 97555f3a vs edd47c92 (SEC at 03:26:42): AST minus module docstring identical, all three.
- HEAD diag: grid rows die in Load at mode 14 (0x0e) -- PRETABLE5's claim holds.
- debugger.c 781-797: clear at entry to interaction, skipped while n_steps_left > 0 (and `step call' early return at 767-777).
- X(msr) reloads ic->arg[0] from the register every execution (cpu_arm_instr.c X(msr)) -- glm's R1 refuted.
- codex's 126/160 label x latch x mode-bit and 48/72 first-clear x bits 31:8: re-derived by my own enumeration, agree.

Gate (harness with lib.sh's real check/gate_end, `python3' shadowed by the fixture):
- fixed: 7/7 PASS; HEAD: FAIL 2 of 7 (rows correct 18, reds list); 29 FAIL rows displayed.
- dead (report_dead shape): parse FAIL (no REDS line) -- fails closed, misdiagnosed.
- truncated / two DONE / REDS empty: FAIL.  inconsistent FAIL row with 47/47+none: PASS.  duplicated row: PASS.
- AFTER gate_end with an earlier failing check + HEAD log: script exit 0 (run.sh scores PASS).
- check_score_claims with the section inserted before gate_end: SCORE_CLAIMS_PINNED=33, PASS; precommit U manifest is 32.

grid cov scope (offline, generator perturbed, probe's own grid_obs/grid_cov text):
- shipped 0; G3 minus 0x18 -> 0; minus 0x18-0x1a -> 0; msr labels minus SYS -> 0; restore labels minus ABT -> 4.
