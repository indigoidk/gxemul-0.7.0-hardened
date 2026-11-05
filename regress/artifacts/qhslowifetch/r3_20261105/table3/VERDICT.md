# qhslowifetch -- test-variant TABLE 3 verdict (repair 3), run 2026-11-04 22:25:53-22:29:30 local, -0600 (2026-11-05 04:25-04:29Z)

Instrument: table3/probe62_frozen.py (62 rows).  Baseline: ../cpu_ppc_instr.c.fix4 (fix3 + the ruled Q8 comment; no code change).
Driver: ../table3_qhs.run.sh (a frozen copy), scratch clone /tmp/gxqhs3 under a clone-local sentinel, restored, cmp-clean against
GXEMUL-SEC, rebuilt fresh, sentinel cleared (../table3_run.log).  ORDER: ../PRETABLE_3.out mtime 22:25:35.57; the driver's first
output, table3/build_base.log, 22:25:53.63.

LEGS: base 62/62 CONTROL=OK SYMPTOM=ABSENT; HEAD 36/62 CONTROL=OK SYMPTOM=PRESENT (predicted 36); null media -- /bin/true 31/62,
an absent binary 21/62, /bin/false 22/62 -- CONTROL=FAIL each (floor (a) and (c)).

VARIANTS: 32; 23 red, 9 green.  30 of 32 scored EXACTLY the predicted red set.  The two that differ are BUILD-DEPENDENT -- the
uninitialised or stale instruction word decides which rows red:
  D12_else_ra  predicted T_ra_pc,T_ra_nonex,T_ra_addr,T_ra_me_pc,T_ra_me_nonex (carried from table 2's measured T ra reds); measured
               59/62 -- T_ra_nonex,T_ra_me_pc,T_ra_me_nonex.  Table 2's PRETABLE flagged D12 build-dependent; PRETABLE_3 did not
               carry the flag forward (an errata line, PRETABLE_3.errata.md).
  V12_fail_ra  predicted T_ra_nonex,T_ra_me_nonex (flagged BUILD-DEPENDENT); measured 59/62 -- T_ra_nonex,T_ra_pc,T_ra_addr.
Both are DETECTED.  (Repair-pass-3 ruling F4, 2026-11-05: V12 is NOT PREDICTED -- the stale stack word decides its outcome, and
table 4 reddened the opposite leg -- so it is counted in neither tally: 22 predicted red and red, 9 predicted green and green.)
Every variant predicted to red did; the nine green are the predicted nine (below).  (Corrected 2026-11-05,
repair pass 3, GPT-6 Astra R3: this line said "No variant went undetected", which the nine green variants refute.)

THE RULED ADDITIONS, each caught on its predicted row: V8 (arm (a) && ME clear) -> T_ra_me_nonex; V9 (&& ME set) -> T_ra_nonex;
V10 (ME set -> bad:) -> T_me_unimpl alone; V11 (ME set -> the checkstop fallback; the shape grid's gap) -> T_me_chkstop,
T_ra_me_chkstop.  The nine green are the predicted nine: D6, D9, D10, V4, V5, V6 (arm (d) / the fallback, measured unreached),
D11, V2 (arm (b), reached on no measured session), V3 (equivalent: running is 0 at every reachable entry).
