# #539 kill table -- 2026-09-19 02:03-02:06, scratch clone /tmp/gx539

| run | rows | verdict | red rows | what it is |
|---|---|---|---|---|
| prefix_HEAD | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | PRE-FIX WITNESS: the new probe on the HEAD-source baseline (E arm HOST-DIED at E0, exit 1, ENABLE SET) |
| base_fixed | 19 of 19 | PASS | none | POST-FIX BASE: the fix applied, rebuilt (gxemul 7f3293e4) |
| a_verbatim | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | (a) floor (b): the removed fatal()+exit(1) reinstated verbatim |
| b_ifzero | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | (b) exit reinstated only when irq_enable == 0 (E0 sole carrier) |
| c_status | 14 of 19 | FAIL | E1,E2,E3,E6,E5 | (c) body field swapped: odata = d->irq_status |
| d_fiqen | 14 of 19 | FAIL | E1,E2,E3,E6,E5 | (d) body field swapped: odata = d->fiq_enable |
| e_fatalonly | 18 of 19 | FAIL | E4 | (e) fatal() kept, exit(1) dropped |
| f_width | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | (f) a width guard: sub-word reads refused with the old death |
| g_mask | 17 of 19 | FAIL | E2,E5 | (g) readback masked to the low 16 bits |
| h_assign | 16 of 19 | FAIL | E2,E3,E6 | (h) SET write arm: |= -> = |
| i_andidata | 18 of 19 | FAIL | E5 | (i) CLEAR write arm: &= ~idata -> &= idata |
| j_orassert | 19 of 19 | PASS | none | (j) DISCLOSED: SET write arm assert condition irq_status & -> | |
| k_clearexit | 18 of 19 | FAIL | K1 | (k) the exit also removed from the CLEAR read (K1 sole carrier) |
| l_topbits | 10 of 19 | FAIL | EC1,EA1,E0,E1,E2,E3,E6,E5,E4 | (l) fatal()+exit(1) kept only for bits 30/31 of the value |

Pre-fix witness RED (10/19: the E arm dies at E0 so every E row and its two controls are absent), post-fix base 19/19
GREEN, 11 of 12 mutants KILLED, and (j) ESCAPED 19/19 exactly as the contract discloses.  Every restore was cmp'd
CLEAN against SEC and rebuilt fresh before the next mutant (sentinel cleared only then).  Kills by channel: (a)(b)(f)(l)
by HOST DEATH in arm E; (c)(d) by value (E1: 0 != P -- indistinguishable from each other, as PRETABLE said);
(e) by E4 only (fatals=6 -- E4 IS the sole carrier in this arm layout); (g) E2+E5; (h) E2+E3+E6; (i) E5 only;
(k) K1 only.  A first launch of the same driver was aborted mid-(b) (Bash-tool timeout hygiene, not a defect) and its
partial logs are kept under `aborted_first_launch/`; the table above is the complete second run (TABLE.log).

# Tables 2-4 (after the pass-2 and §F2 corrections; three probes frozen per table; clone /tmp/gx539)

| table | instrument | base (sites / drain / witness) | mutants | result |
|---|---|---|---|---|
| 2 (03:45-03:53, `table2_v2/`) | v2: bounded reap, sites drains before close | 19/19 / CONTROL=OK / PASS | x_exit2 (CLEAR read: complaint then exit(2)); y_sigkill (complaint then SIGKILL) | each RED 3/3 K rows (sites K1; drain K exit=2 / signal=9; witness K likewise) |
| 3 (04:04-04:09, `table3_v3/`) | v3: budgets 20 s + 10 s, HARNESS-KILL label, T rows require keys | 19/19 / OK / PASS | z_silentexit (CLEAR read: exit(1) kept, complaint deleted) | RED 3/3 K rows (exit=1, no complaint) |
| 4 (04:09-04:11, `table4_v4/`) | v4: `gone` flag on ECHILD, HARNESS-CLOSE label | 19/19 / OK / PASS | none (instrument change only) | base green |

Every restore cmp'd CLEAN against the SEC working tree and rebuilt fresh; no sentinel left.  (table3_v3's log was written
as TABLE2.log by a driver derived from table 2's and renamed to TABLE3.log afterwards; driver_stdout.log is the same content.)
| 5 (04:17-04:19, `table5_v5/`) | v5: fable5's L4s (E4 contract sentence; distinct ids over green lines; HARNESS-KILL only on SIGKILL; rd() convention stated) | 19/19 / OK / PASS | none (instrument change only) | base green |
