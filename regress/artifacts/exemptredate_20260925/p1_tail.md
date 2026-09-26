
## 4. MEASURED (on a `git archive` export of HEAD's `tools/` and `regress/*.py|*.sh`, with the proposed checker swapped in)

Control first: HEAD's own checker on that export -- `--today 2026-09-27` PASS; `--today 2026-09-28` FAIL with 10
problems, all `EXPIRED EXEMPTION`.  Then the proposed checker (`measured/schedule.out`, abridged to the transitions):

    2026-09-25 .. 2026-10-08   rc=0  PROBEWIRING_PASS
    2026-10-09  rc=1  expired: ip30_abort_probe.py
    2026-10-16  rc=1  + ppc_rldicl_probe.py
    2026-10-21  rc=1  + alpha_tbi_probe.py
    2026-10-22  rc=1  + lca_badval_probe.py
    2026-10-23  rc=1  + lca_widewrite_probe.py
    2026-10-24  rc=1  + lca_isalane_probe.py
    2026-11-03  rc=1  + wdc_altoffset_probe.py
    2026-11-04  rc=1  + wdc_altoffset_4bit_probe.py
    2026-11-17  rc=1  + wdc_altoffset_sig_probe.py
    2026-11-18  rc=1  + wdc_addtoinbuf_probe.py   (all ten)

`--selftest` on the proposed checker: `PROBEWIRING_SELFTEST_PASS  22/22 mutants behaved as specified`
(`measured/selftest_550_onHEAD.out`), M5a/M5b now derived from 2026-10-08.
Gate 2's `exempt_expired` helper, extracted and run on the proposed SC_EXEMPT: 09-27 none; 09-28 wdc_identify;
11-30 wdc_identify; 12-01 ieee_store wdc_identify.

## 5. QUESTIONS

1. **Premise audit.**  Each `#550` comment line states a FACT about the owed work and a REASON for its date.  Check the
   facts against the tree: is `ip30_abort_probe.py` really binary-only (no rig image, no disk)?  Is the rldimi-oracle
   repair of `ppc_rldicl_probe.py` really parked in the working tree (`git diff -- regress/ppc_rldicl_probe.py`)?  Do the
   four LCA/Alpha probes really share one missing gate?  Is `ieee_store`'s "six inline counters" right?  Any comment
   this diff edits or leaves that is now FALSE is a finding.
2. **What is the smallest edit to THIS diff that the checker, its selftest and gate 2 would all still pass, while the
   intent (each entry falls due ALONE, on a date someone chose) is broken?**  Name the edit and what stays green.
3. **Option-set completeness.**  Individual dates were chosen by the owner; within that, is anything in this diff a
   choice that should have been different -- a date order that will collide with the work queue, an entry that should
   be DELETED rather than re-dated because its prerequisite already exists, a comment that should name a queue row?
4. **The two lists are handled differently on purpose** (the checker blocks commits; gate 2 reds one row).  Is there any
   path by which the proposed SC_EXEMPT change blocks a commit or hides a red it should show?

If, while verifying a claim, you found something ELSE -- say so.
