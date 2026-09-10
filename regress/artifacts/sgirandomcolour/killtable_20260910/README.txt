#519 sgirandomcolour -- KILL TABLE 1, provenance and clearance record.
Opus 5 measuring seat, 2026-09-10, 04:06 - 05:12.  Scores and per-mutant edits: TABLE1.out.

FILES IN THIS DIRECTORY
  PRETABLE.out                        the pre-table check, written 03:51 -- BEFORE table 1 ran, and
                                      its mtime is the proof (this table's first build began 04:06).
  BASELINE_FIX519.c                   THE NAMED BASELINE.  SEC's src/devices/dev_sgi_re.c frozen at
                                      04:06, i.e. HEAD 1ce8296 plus the round's uncommitted fix.
  BASELINE_FIX519_v2.c                SEC's dev_sgi_re.c re-frozen at 05:08.  See THE DIVERGENCE.
  sgi_re_colourdefault_probe.FROZEN.py  the instrument, frozen 04:06, cmp-clean against
                                      regress/sgi_re_colourdefault_probe.py at freeze time.  The
                                      table ran ONLY this copy, never the live file.
  mut519.py                           the M1..M12 mutator, copied beside the results (it was handed
                                      to the seat; this copy is the one the record cites).
  mut519b.py                          the M13/M14 mutator -- the measuring seat's own.  A SEPARATE
                                      FILE on purpose: the driver re-reads its mutator between
                                      mutants, so editing mut519.py mid-table would have changed the
                                      instrument underneath the run.
  BASE.raw, M*.raw, BASE2_currentSEC.raw   one probe log per build.  Each verified to END in
                                      SGICOLOUR_DONE -- a preserved log is verified by its
                                      completion sentinel, not by its existence.
  TABLE1.out                          the table.

BASELINE NAMING, and why a clone inherits the wrong file if you skip this
  build/ still held the PRE-FIX dev_sgi_re.c (the round had not propagated the fix), verified by
  cmp against scratchpad/dev_sgi_re.pre519.c -- BYTE IDENTICAL.  So a bare `cp -a build /tmp/...'
  would have measured the PRE-fix file and every mutant would have scored against the wrong base.
  The clone therefore had BASELINE_FIX519.c copied in over it, and the result was cmp'd against both
  the baseline and SEC before mutant 1:  CLONE == BASELINE, CLONE == SEC.  Both printed.

CLONE, SENTINEL, FREEZING
  /tmp/gxopus519, a `cp -a' of build/.  No project tree was written at any point: not GXEMUL-SEC/src,
  not est/, not build/, not build-asan/.  The main loop's own tables in /tmp/gxopus518, /tmp/gxopus518b
  and /tmp/gx519 were not touched.
  /tmp/gxopus519/.MUTANT was written BEFORE mutant 1 and named its restore source.
  The driver was run from a FROZEN COPY (run519.run-t1.sh / run519b.run-t1.sh) so the original stayed
  editable while the table ran.
  Per build: `rm -f src/devices/dev_sgi_re.o gxemul; make -j4', then [ gxemul -nt dev_sgi_re.c ].
  All 15 builds printed FRESH.  The baseline build doubles as the freshness proof, per the clone
  recipe -- and it was needed: before the first build the clone's binary was OLDER than its source
  (00:19 binary over a 04:06 source), which the driver reported rather than measured through.

*** THE DIVERGENCE -- SEC's dev_sgi_re.c CHANGED AT 04:26, MID-TABLE.  REPORTED, NOT ABSORBED. ***
  The end-of-table re-cmp of BASELINE_FIX519.c against SEC came back DIFFERENT at line 367.  The
  whole diff is two bytes, inside the announce string literal:

      -  fatal("[ put: color mode = 0x%x ] sgi_re: unimplemented "
      +  fatal("[ put: color mode = 0x%x ] [ sgi_re: unimplemented "

  i.e. the main loop balanced the message's brackets at 04:26, while mutants M2..M12 were building.

  WHAT IT DOES AND DOES NOT COST, and the second half is measured rather than reasoned:
   * TABLE 1 MEASURED THE 04:06 BASELINE.  That is stated here rather than papered over; every score
     in TABLE1.out is against BASELINE_FIX519.c, which is HEAD 1ce8296 + the fix as it stood at 04:06.
   * The instrument keys on THREE literals, and the edit touches none of them:  `ycrcb attrib' greps
     "[ put: color mode = 0xf0 ]" (the prefix, before the edit point); `announce text' greps
     "store declined (once)" (after it); `once' / `latch indep' / `live silent' grep
     "unimplemented colour type in horrible_getputpixel" (after it).
   * SO THE INFERENCE WAS "no row can move" -- AND IT WAS CONVERTED INTO A MEASUREMENT rather than
     left as an inference.  The clone was re-based onto the current SEC file, rebuilt, and the frozen
     instrument re-run:  BASE2_currentSEC.raw = 14/14, zero FAIL rows.  The detector still passes on
     what is actually in the tree.
   * ONE CONSEQUENCE FOR ANY RE-RUN: mut519.py's find-strings for M1, M7 and M12 quote the OLD
     literal, so against the current SEC file they will exit 9, MUTANT-TEXT-NOT-FOUND.  That is the
     driver's presence-pin working as intended -- it fails loudly rather than silently mutating
     nothing -- but a table 2 must re-key those three or run from BASELINE_FIX519.c.

RESTORE AND TWO-PART CLEARANCE
  Restore was from the FROZEN BASELINE (never from a script's own backup), then rebuilt, then cleared.
  Final state, all outputs recorded rather than asserted:

      clone source cmp vs SEC ............ CLEAN   (PART 1)
      [ gxemul -nt dev_sgi_re.c ] ........ CLEAN   (PART 2)
      /tmp/gxopus519/.MUTANT ............. removed, only after BOTH parts were clean
      BASE2_currentSEC ................... 14/14, SGICOLOUR_DONE

  *** A DEFECT IN MY OWN RESTORE SCRIPT, RECORDED BECAUSE IT NEARLY SET THE PRECEDENT IT WARNS
  AGAINST. ***  The first restore script gated its `rm .MUTANT' on PART 2 ALONE -- it printed
  "PART 1: FAIL" (the SEC divergence above) and cleared the sentinel anyway.  That is precisely the
  cleared-sentinel-over-an-unclean-tree shape the carrier records, reached by writing the guard on
  one of the two parts.  It was caught immediately because the script PRINTS both parts instead of
  only acting on them.  The tree was then re-based onto current SEC under a re-dropped sentinel, and
  the second script gates on P1 AND P2; the state above is that script's output.
  Blast radius was nil in any case -- the tree is a /tmp clone, not a project build tree -- but the
  logic was wrong and would not have been nil in build/.

*** A NAME COLLISION IN THIS DIRECTORY -- READ THIS BEFORE CITING ANY "M13" OR "M14" OF #519. ***
  The main loop ran its OWN tables CONCURRENTLY with mine, in the subdirectory t2/ here, against
  /tmp/gx519 and against a REPAIRED instrument (17 -> 19 -> 20 row sites; see t2/SCORES2.txt).  Its
  mutant numbering continues past table 1's twelve and therefore COLLIDES with mine:

      THIS directory (killtable_20260910/*.raw)   |   t2/ (killtable_20260910/t2/*.raw)
        M13_widthdecline   -- mine, bufdepth      |     M13_okorx    -- theirs, ok || x
        M14_lineardecline  -- mine, linear        |     M14_okory    -- theirs, ok || y
                                                  |     M15_texrd, M16_dropcase_rgb, M17_dropcase_rgba

  NO FILE WAS OVERWRITTEN -- the two sets live in different directories and I wrote nothing into t2/
  -- but "M13 of #519" is ambiguous in prose.  Cite mine as M13_widthdecline / M14_lineardecline, by
  filename, and note the instrument: MINE ARE AGAINST THE 14-ROW TABLE-1 INSTRUMENT.

  Two other things follow from the concurrency, and both are recorded rather than smoothed over:
   * PRETABLE.out GREW WHILE TABLE 1 RAN.  It was 5665 bytes / 63 lines at 03:51 when I read it and
     quoted its line 1; it is 18846 bytes / 198 lines now, section 6 having been APPENDED ~04:3x with
     the pass-2 panel's corrections to sections 1-5.  Sections 1-5 are unedited, so nothing this table
     was built on moved -- but a reader diffing "the PRETABLE" against this table must know the file
     is two documents.  Section 6a corrects a channel-line assignment that MY M8 measurement
     independently confirms; see TABLE1.out's channel-line block.
   * SCHEDULING.  Their table 2c was still running when I finished, so the follow-up measurement
     below was SERIALISED behind it -- a script that waits for 60 s of quiet before its first build,
     rather than loading the host while a pty-timed probe holds wall-clock oracles.

THE FOLLOW-UP MEASUREMENT (BASE19 / M13w / M14l)
  Because the round's instrument had MOVED under me -- the main loop repaired it from 14 rows to 19
  while table 1 ran -- reporting M13/M14 only against the 14-row copy would have been a finding about
  a detector nobody is shipping.  So both mutants were re-scored against t2/'s REPAIRED19 probe
  (md5 2662ef3a, the instrument its own table 2c is running), in my clone, on SEC's current file:

      BASE19                    19/19   -- identical to their BASE_19, so the clone reproduces their baseline
      M13w_widthdecline_vs19    19/19   -- STILL A CLEAN SWEEP
      M14l_lineardecline_vs19   19/19   -- STILL A CLEAN SWEEP

  This is the difference between a reading and a measurement, and it was worth paying for: I had
  READ their repaired probe and concluded "no new row drives a declined type off bufdepth 4 or onto
  a tiled path".  The reading was right, but a reading of a 19 KB instrument is exactly the kind of
  claim that turns out to have an exception three hundred lines down.  Now it is measured.

WHAT I COULD NOT DO
  * Nothing was blocked.  All 18 builds and 19 probe runs completed.
  * The two escapes are reported as MEASUREMENTS with their reachability read out of the source.  I
    did NOT re-aim either mutant, and I did NOT add or modify any row -- row demand and the L1/L2
    grading are the round's call, not the measuring seat's.
  * The repair, if the round takes one, should close the CLASS rather than the two instances: the
    same axis reappeared twice in ONE table, which is the class-closure trigger arriving early.  The
    joint space is {declined type} x {bufdepth 1,2,4,8} x {tlb_mode 0,1,2,4}; today's rows occupy
    exactly one cell of it (bufdepth 4, LIN_A).  Closing it at bufdepth 1 only -- the width the
    mutant happened to use -- is the #499 repaired-at-the-address-the-mutant-used trap.
