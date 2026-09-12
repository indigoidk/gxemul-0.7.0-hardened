#519 sgirandomcolour -- KILL TABLE 3 (the pass-3 CLOSURE of M13/M14), provenance and clearance.
Opus 5 measuring seat, 2026-09-10.  Scores and per-mutant edits: SCORES3.txt and TABLE3.out.

WHAT THIS TABLE SCORES
  A DETECTOR change, not a product change.  src/devices/dev_sgi_re.c is UNTOUCHED by this pass and
  was verified byte-identical to the frozen baseline at freeze time and again mid-table.  The only
  file changed is regress/sgi_re_colourdefault_probe.py, this round's own uncommitted deliverable:
  19 rows -> 59, appended only (diff vs the pre-edit copy: 0 deleted lines, 152 added), so every
  pre-existing session's command stream is byte-unchanged.

FILES IN THIS DIRECTORY
  PRETABLE.out                        the pre-table check, written 16:13:39 -- BEFORE the freeze
                                      (16:14:09) and before table 3's first build (16:14:24).  Its
                                      mtime is the proof of order.
  EXPLORE_BASE.out                    the CHANNEL check, MEASURED: the throwaway explorer run
  EXPLORE_M13.out                     against the fix and against two permitting mutants, to find
  EXPLORE_M15.out                     out what a PERMITTED store actually writes at each cell
                                      before any row was written.  See PRETABLE.out section 6.
  o519_explore2.py                    that explorer, copied beside its results.
  DRYRUN.out                          every one of the 26 mutants applied to a fresh copy of SEC's
                                      file: 26 apply with EXACTLY ONE match, 0 MUTANT-TEXT-NOT-FOUND.
  o519_dryrun.sh                      the dry-run driver.
  BASELINE_FIX519_T3.c                THE NAMED BASELINE.  GXEMUL-SEC/src/devices/dev_sgi_re.c
                                      frozen 16:14:09, md5 6e2c6873 -- HEAD 1ce8296 plus the round's
                                      uncommitted fix, unchanged since 04:26.
  sgi_re_colourdefault_probe.T3FROZEN.py  the instrument, frozen 16:14:09, cmp-clean against the
                                      live probe at freeze time.  The table ran ONLY this copy.
  mut519c.py                          the mutator, RE-KEYED to the current SEC text (the 04:26
                                      bracket-balance edit had broken mut519.py's M1/M7/M12
                                      find-strings -- the presence pin working as designed).
  BASE.raw, M*.raw                    one probe log per build, each verified to end in
                                      SGICOLOUR_DONE.  A preserved log is verified by its
                                      completion sentinel, not by its existence.
  build_*.log, mutate_*.log           per-leg build and mutation logs.
  SCORES3.txt                         the incremental score record, written as the table ran.
  TABLE3.out                          the table.

CLONE, SENTINEL, FREEZING
  /tmp/gxo519i, a `cp -a' of build/.  NO PROJECT TREE WAS WRITTEN: not GXEMUL-SEC/src, not est/,
  not build/, not build-asan/, not /tmp/gxsec-build.  Because this pass changes no product code
  there was nothing to propagate, and that is recorded as N/A-with-reason rather than left blank.
  build/ already held the fix, so the clone came up cmp-identical to both the named baseline and
  SEC -- both printed before mutant 1 rather than assumed.
  /tmp/gxo519i/.MUTANT was written BEFORE mutant 1 and names BASELINE_FIX519_T3.c as its restore
  source -- never the script's own backup.
  The driver ran from a FROZEN COPY (o519_table3.run-t3.sh) so the original stayed editable.
  Per build: `rm -f src/devices/dev_sgi_re.o gxemul; make -j4', then [ gxemul -nt dev_sgi_re.c ].
  The make return code is NOT the test; the timestamp pair is.  The baseline build doubles as the
  freshness proof, and it was needed -- before it the clone's binary was 15:18 over a 12:10 source,
  i.e. inherited from build/ and not built from the baseline the table names.

WHAT THE PRE-CHECK IS AND IS NOT
  The three EXPLORE_*.out runs are NOT frozen-instrument measurements: the mutator was edited
  between the M13 and M15 legs (one dictionary entry added, no find/replace string changed,
  re-verified by dry run).  They are recorded as what they are -- a channel check that answered
  "what does a permitted store write?" with a number instead of a guess.  TABLE 3 is the frozen
  measurement.

RESTORE AND TWO-PART CLEARANCE
  Restore from the FROZEN BASELINE, then rebuild, then clear -- and the sentinel is cleared only if
  BOTH parts pass, recorded as output rather than asserted.  See the tail of SCORES3.txt.
