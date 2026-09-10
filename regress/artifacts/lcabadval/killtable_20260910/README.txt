#518 lcabadval -- KILL TABLE, Opus 5 measuring seat, 2026-09-10.
================================================================================================

WHAT RAN, WHERE, AND AGAINST WHAT.  Everything in this directory was produced in a SCRATCH
CLONE (/tmp/gxopus518, a `cp -a' of build/).  No file under GXEMUL-SEC/src, est/, build/ or
build-asan/ was written by this seat at any point.

--------------------------------------------------------------------------------------------
1.  THE BASELINE, AND WHY IT IS A FROZEN COPY RATHER THAN "the SEC working tree"
--------------------------------------------------------------------------------------------

  BASELINE_FIX518c.c    21372 bytes   md5 d5549c2fd83a6f79da3282c55ed77af0   mtime 00:19:23
                        == GXEMUL-SEC/src/devices/dev_lca.c at 00:19:23 (the round's post-fix
                        working set, uncommitted, HEAD e73623a)

  *** THE FIRST RUN OF THIS TABLE WAS INVALIDATED MID-RUN AND THE RUN DID NOT NOTICE. ***

  The driver's mutator restored from GXEMUL-SEC/src/devices/dev_lca.c on every iteration, per
  the brief's "NAME THE BASELINE = the SEC working tree".  At 00:19:23 the main loop shipped a
  REPAIR of the fix in response to its own pass-2 panel -- FIX518c: 20681 -> 21372 bytes, the
  diff growing 106 -> 116 insertions -- while the table sat between mutants.  So BASE, M1 and
  M2 were built over one fix and M3 over another.

  Every clearance the run performs PASSED THROUGHOUT, because they all compared against the
  thing that was moving:
      - `cmp clone/dev_lca.c SEC/dev_lca.c'  -> CLEAN (both were the new file)
      - `[ gxemul -nt dev_lca.c ]'           -> OK    (each build was genuinely fresh)
      - MUTANT-TEXT-NOT-FOUND                -> never fired (every find-string survived)
  The tell was none of these.  It was a LINE NUMBER: a re-read of dev_lca.c for an unrelated
  review question printed `odata = d->tlb_enable' at :368 where an earlier read in the same
  session had it at :364.

  A KILL TABLE OWES ONE BASELINE THE WAY A COMPARISON RUN OWES ONE INSTRUMENT.  The carrier's
  frozen-copy rule is written for the PROBE; the baseline SOURCE needs it for exactly the same
  reason -- and in a live round the source is the MORE likely of the two to move, because the
  round exists in order to edit that file.  Freezing costs one `cp'.

  The first run's logs are kept, quarantined and never cited as results, in
  pre_repair_aborted/ (BASE 40/40, M1 36/40, M2 38/40 on the PRE-repair fix; M3 partial).

--------------------------------------------------------------------------------------------
2.  THE INSTRUMENTS -- there are TWO, and the round's own probe grew mid-table as well
--------------------------------------------------------------------------------------------

  lca_badval_probe.asrun.py    md5 3d2ead94a7ffb90496d470a6ed7ab30d   40 rows (20 witness +
                               20 detector).  This is the instrument the brief describes.
                               Frozen at 00:06, BEFORE mutant 1.

  lca_badval_probe.asrun2.py   md5 b6104f47a4bf37225f5bd538f563335a   58 rows.  The REPAIRED
                               probe as of 00:19:23: D2 gained `wmask0 f2' (codex) and
                               `wmask1 once' (glm); D5 gained `def width' (codex) and had
                               `def read0' re-indexed; D6, D7 and D8 are new blocks.
                               Frozen at 00:19:23.

  The live regress/lca_badval_probe.py changed at least TWICE while this seat was measuring
  (an intermediate md5 e16a3c068ff5c305e9cd085d7f78f723 was observed).  The frozen copies are
  what every number here was produced with; neither has moved since (re-checked at the end).

  BOTH were scored on the frozen baseline before any mutant ran:
      BASE_40row.raw   LCABADVAL_RESULT=40/40   (the repair regressed NO original row)
      BASE.raw         LCABADVAL_RESULT=58/58

  THE TABLE IS SCORED AGAINST asrun2 (58 rows), because the question a kill table has to answer
  is whether the detector THAT WILL SHIP catches the mutant.  Where a mutant behaves differently
  under the two instruments that is reported explicitly, and it is the most useful thing in the
  table: it measures whether a pass-2 row addition earns its place.

--------------------------------------------------------------------------------------------
3.  THE MUTATOR
--------------------------------------------------------------------------------------------

  mutate518.py    restores from BASELINE_FIX518c.c, then applies ONE named mutant by exact
                  find/replace.  MUTANT-TEXT-NOT-FOUND exits 9 -- a hard FAIL, never a silent
                  skip -- so every mutant additionally PINS the presence of the text it edits.
                  Backslashes destined for the C file are built with chr(92).
  mutate518b.py   batch B.  A SEPARATE FILE because python re-reads a script at every
                  invocation, so editing the batch-A mutator mid-table would hand different
                  mutants different mutators.

  MULTI-EDIT is licensed only for the (b) verbatim reinstatements, which replace a whole switch
  arm with its pre-#518 source taken from the preserved pre-fix file.  That file was verified
  byte-identical to `git show HEAD:src/devices/dev_lca.c' (17763 bytes) before use, so M1-M7 and
  M22 reinstate SHIPPED code and not a reconstruction.

  Per build: `rm -f src/devices/dev_lca.o; make -j4', then BOTH `MAKE_RC' and
  `[ gxemul -nt src/devices/dev_lca.c ]' -- MAKE_RC alone has been observed reading 0 on a
  failed build.  Per probe run: the last line must be LCABADVAL_DONE or the score is refused
  rather than read.

--------------------------------------------------------------------------------------------
4.  RESULTS
--------------------------------------------------------------------------------------------

  See TABLE1.out (mutant, edit, score, reddened rows, log name) and SCORES.txt / SCORES_B.txt.
  Every mutant's log is <mutant>.raw in this directory.
