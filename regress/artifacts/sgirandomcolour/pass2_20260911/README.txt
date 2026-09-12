#519 sgirandomcolour -- PASS 2 (Opus measuring seat).  Provenance, results and clearance.
Run 2026-09-10 20:42 -> 22:50 CDT.  (The directory is named 20260911 as the pass-2 brief
specified; every log inside is stamped 2026-09-10.  Recorded rather than silently renamed.)

Scores: SCORES_P2.txt (table A), SCORES_P2B.txt (table B, negative controls), FGAXIS.out
(the M37 discriminating run).

================================================================ WHAT THIS PASS FOUND

SIX MUTANTS SCORED 59/59 ON THE SHIPPED 59-ROW INSTRUMENT -- ZERO RED ROWS, SIX TIMES --
AND EVERY ONE OF THEM WAS MEASURED WRITING UNINITIALISED HOST STACK INTO GUEST MEMORY.

    mutant                  edit                                    59-row   guest memory written at
    M30_tilenrdecline       ok=0  ->  if (tile_nr == 0) ok = 0;     59/59    tile 1   0x70630000
    M31_tilenrguard         if (ok) -> if (ok || tile_nr)           59/59    tile 1   0x6368696e
    M32_tilenrxdecline      ok=0  ->  if (tile_nr_x == 0) ok = 0;   59/59    tile 1   0x706300fe
    M33_tiledorigin         ok=0  ->  if (linear || y == 0) ok = 0; 59/59    tiled (0,1) 0x706300d6
    M28r_permit_othernib    ok=0  ->  if (color_mode==0xf0||0x50)   59/59    nibble 0x60 0x706300c3
    M37_fgvalue             ok=0  ->  if (*color == 0xaabbccdd)     59/59    fg 0x12345678 0x706300fe

`0x6368696e' is ASCII "chin" -- real host stack text reaching guest-visible memory.  The
values differ between mutants and between builds, which is the round's own disclosure (iv)
confirmed: what a permitted store publishes is uninitialised stack.

*** WHAT IS AND IS NOT NEW HERE, stated so this record is not read as a bigger catch than it
is.  THE ROUND HAD ALREADY DISCLOSED TWO OF THESE AXES. *** The probe's own pass-3 contract
(sgi_re_colourdefault_probe.py, the CONTRACT block) lists under "STILL NOT CAUGHT, disclosed
rather than claimed": (ii) x or y beyond the two vertices driven, and (iii) the tile INDEX --
"every cell uses tile 0 of its window, so a condition on tile_nr is unrowed".  So these are
NOT holes the round failed to see.  What this pass adds is (a) the MEASUREMENT that each is a
live guest-memory write rather than a theoretical gap, (b) that the smallest is one token, and
(c) the argument that their CLASSIFICATION as clause-(e) debt is wrong -- `tile_nr' flows into
`tileptr', the store's address operand, which is the same 2026-09-09 flow test the round itself
used to make `tlb_mode' a floor axis.  The disclosure is honest; the grading is what is
disputed.  (The pass-2 brief's "NEW MATERIAL, VERBATIM AND COMPLETE" section omitted that
contract block, which is why the question put to the panel invited rediscovery of a disclosed
item; the coordinator has since confirmed that omission was a brief defect, not a probe defect.)

NEGATIVE CONTROLS -- the instrument is NOT blind to geometry in general:

    M34_ofsguard            if (ok) -> if (ok || ofs)               58/59    KILLED by `ycrcb x4y1'
    M35_xguard              if (ok) -> if (ok || x)                 58/59    KILLED by `ycrcb x4y1'
    M36_yguard              if (ok) -> if (ok || y)                 58/59    KILLED by `ycrcb x4y1'

One red row each, out of 59 scored.  `ycrcb x4y1' (grok, pass 2) claims in its own comment to
kill "`if (ok || x)' and `|| y'".  Table 3 built NEITHER, and that row's kill set there is a
strict SUBSET of `lin ycrcb d1' -- it discriminated nothing.  These three discharge the claim.

THE AXIS THE ROW CANNOT REACH IS THE TILE INDEX.  Its cell is LINEAR at (4,1), and
`tile_nr = x >> 12' gives 0; a TILED (4,1) would not have helped either, since
`x / tilewidth_in_pixels' is 0 at every bufdepth.  Every one of the 59 rows holds tile_nr == 0
-- proven by enumerating the probe's own call sites: every `setup_put' uses the default
vertex 0 except line 302, and `tiled_prologue' / the lin block store vertex 0 explicitly.

SEVERITY.  At 32 bpp a tile is 128x128 pixels, so `tile_nr == 0' is `x < 128 && y < 128'.
On the default 1280x1024 framebuffer (dev_sgi_gbe.c GBE_DEFAULT_XRES/YRES) that is 16384 of
1310720 pixels.  M30 keeps the #519 fix over 1.25% of the screen and re-opens it over the
other 98.75% -- and all 59 rows sit inside the 1.25%.

================================================================ WHAT THIS PASS DID NOT TOUCH

A DETECTOR question, not a product change.  src/devices/dev_sgi_re.c (md5 6e2c6873) and
regress/sgi_re_colourdefault_probe.py (md5 c5bf209f) were verified byte-identical to the
round's table-3 record at the start of each table, and again by `git status' afterwards.
NO PROJECT TREE WAS WRITTEN except this artifacts directory: not GXEMUL-SEC/src, not est/,
not build/, not build-asan/, not /tmp/gxsec-build.  All three build trees were re-checked
after the run (PART1 CLEAN each; build/ still carried its pre-existing 15:18 binary over a
12:10 source, unchanged from clone time); est/ is a SOURCE tree, so part 2 is N/A, not
merely unchecked.

================================================================ FILES

  BASELINE_FIX519_P2.c                 THE NAMED BASELINE -- a copy of the round's own
                                       killtable3_20260910/BASELINE_FIX519_T3.c, md5 6e2c6873,
                                       verified identical to SEC at each table's start.  Every
                                       leg restores from THIS file, never a script's backup.
  sgi_re_colourdefault_probe.P2FROZEN.py  the round's live 59-row instrument, frozen and
                                       cmp-verified against the live probe.  Both tables ran
                                       ONLY this copy.
  ctrl519p2.P2FROZEN.py                the CONTROL PROBE (10 rows, 3 off-instrument cells).
  ctrl519p2_fg.P2FROZEN.py             the fg-axis discriminator (4 rows, 1 cell, 2 colours).
  mut519p2.P2FROZEN.py                 table A's mutator (5 mutants).
  mut519p2b.P2FROZEN.py                table B's mutator (the same, plus 4).
  BASE*.raw, M*.raw                    one 59-row instrument log per build.
  BASE*.ctrl, M*.ctrl                  one control log per build.
  BASE.fgctrl, M37_fgvalue.fgctrl      the fg-axis logs.
  build_*.log, mutate_*.log            per-leg build and mutation logs.
  table_p2.run-p2.sh, table2_p2.run-p2b.sh, fgaxis.run.sh   the FROZEN drivers as run.
  dryrun_mutants.sh, rowcover_table3.sh, summarise.sh       the analysis, beside its results.
  TABLE_P2.out, TABLE_P2B.out, FGAXIS.out                   the tables.

================================================================ WHAT THE CONTROL PROBE IS AND IS NOT

A mutant that scores 59/59 has three possible explanations (carrier: "a mutant that will not
die is a result"): mis-built, target dead, or rows mis-cut.  The control separates them.  It
drives three cells the 59 rows do not span, and pins each with a LIVENESS row (an accept at
the same cell lands where predicted) and an ATTRIBUTION row (a neighbouring cell is untouched,
so the index/offset really is what is claimed).  Its `want' column is pinned to the FIX, so a
red row under a mutant means: this mutant writes guest memory where the instrument cannot see.

It is NOT a proposed detector and it is NOT in the tree.  It is offered as material the round
may lift if it chooses; the row design is the round's decision, not this seat's.

CONTROL INVARIANCE, measured.  The two accept cells drive DE_MODE_TYPE_RGBA and never reach
the edited default arm, so all four liveness/attribution rows must read identically on BASE
and on every mutant.  They did, in all eleven legs.  And each mutant moved EXACTLY ONE control
cell -- M28r only nib60, M30/M31/M32 only t1, M33 only ty1 -- so the axes are orthogonal and
each write is attributable to the axis its mutant names.

The `ty1' pair additionally pins `ofs = 512*y + xofs': a tiled accept at (0,1) lands at phys
0x10000 + 512 while the y == 0 word stays painted.  That is the arithmetic pass-2 question 5
records as unexercised.

================================================================ CLONE, SENTINEL, FREEZING

/tmp/gxop519p2, a `cp -a' of build/.  Clone-local .MUTANT written BEFORE mutant 1 in each of
the three runs, naming BASELINE_FIX519_P2.c as its restore source.  Drivers ran from FROZEN
COPIES so the originals stayed editable.  Per build: `rm -f src/devices/dev_sgi_re.o gxemul;
make -j4', then [ gxemul -nt dev_sgi_re.c ].  The make return code is NOT the test; the
timestamp pair is.  The baseline build doubles as the freshness proof, and it was needed --
the clone inherited build/'s 15:18 binary over a 12:10 source.

All three runs ended with PART1 CLEAN + PART2 FRESH and the sentinel cleared.  Table B's
BASE_B leg is an independent BEHAVIOURAL confirmation of table A's restore: 59/59 and 10/10,
not merely a `cmp'.  Every one of the 24 logs was verified to end in its completion sentinel.

================================================================ APPARATUS DEFECTS, DISCLOSED

1. THE PRESENCE PIN IS WEAKER THAN IT READS -- in my mutator as first written, and in the
   round's own mut519c.py.  cond() keys on the 3-tab "ok = 0;\n" and replaces it with a 4-tab
   "ok = 0;\n"; a plain substring count still finds the find-string in the ALREADY-MUTATED
   text, so `count == 1' cannot detect a double application.  LATENT, not live -- every leg
   copies a fresh baseline, so no measurement here or in table 3 is affected -- but
   DRYRUN.out's "26 apply with EXACTLY ONE match" proves single application, not idempotence.
   Closed here by newline-anchoring every find-string, negative-controlled in both directions
   (bogus name -> rc 8, double application -> rc 9).  See dryrun_mutants.sh.

2. A ROW-NAME PARSE OF MINE MATCHED NOTHING AND REPORTED "killed by NOTHING" FOR ALL 59 ROWS.
   The probe prints "%-16s"; I cut at 18 and sliced into the `got' column.  Caught by the
   contradiction -- the table plainly lists reds -- not by any check.  Re-run at width 16:
   58 of 59 rows are red under at least one of table 3's 26 mutants.

3. MY OWN CONTROL INHERITED THE INSTRUMENT'S BLIND SPOT ON ONE AXIS.  M37_fgvalue scored
   59/59 AND 10/10, because ctrl519p2.py sets DE_FG to the same 0xaabbccdd every one of the
   59 rows uses.  That is not evidence the mutant is harmless; it is the same single-value
   blind spot, reproduced by me, by copying the instrument's constant.  Settled by a separate
   run (FGAXIS.out) driving one cell at two foreground colours: the fix declines at both
   (4/4); M37 declines at 0xaabbccdd and writes 0x706300fe at 0x12345678.

4. TABLE B's MUTATOR GAINED FOUR DICT ENTRIES WHILE TABLE A WAS RUNNING.  Table A ran from a
   frozen copy taken at its start; that copy is in this directory and contains 5 mutants with
   the additions absent, verified by grep, and no find/replace string changed, verified by
   diffing the keying of both copies.  Table A is a frozen-instrument measurement.

5. TABLE A AND TABLE B SHARE ONE CLONE AND WERE RUN STRICTLY SERIALLY -- table B was gated on
   table A's own completion line and started 13 seconds after it.  They never overlapped.
