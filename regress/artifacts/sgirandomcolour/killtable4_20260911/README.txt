#519 sgirandomcolour -- KILL TABLE 4, the CLASS CLOSURE.  Opus measuring seat, 2026-09-10/11.
Scores: SCORES4.txt.  Pre-table check: PRETABLE.out (written 23:19, before the first build at
23:22:58 -- the mtime is the proof of order).

WHAT THIS TABLE SCORES
  A DETECTOR diff.  src/devices/dev_sgi_re.c is UNCHANGED -- md5 6e2c6873, the same product file
  table 3 named, verified by the driver before mutant 1.  Only the probe changed: 59 rows -> 77,
  twenty-two added and four deleted.

WHY A CLASS CLOSURE RATHER THAN ANOTHER CELL
  Three consecutive passes found ONE shape: a decline conditioned on an input the rows hold at a
  single value.  Table 3 pass 1/2 found it on bufdepth (M13) and tlb_mode (M14) and closed those
  two axes over their whole domain.  Pass 2 of this round then measured SIX mutants at 59/59 on
  the resulting instrument -- M30/M31/M32 (tile index), M33 (tiled y), M28 (nibble), M37
  (foreground value) -- each writing uninitialised host stack into guest memory, the smallest
  being ELEVEN CHARACTERS (`if (ok)' -> `if (ok || tile_nr)').  The rule forbids buying a fourth
  cell, so this closes the class.

THE ENUMERATION, AND THE BOUND THAT MAKES IT FINITE
  The guarded store reads exactly four lvalues -- tileptr, ofs, buf, bufdepth -- whose free
  inputs, walked up only to the enclosing function boundary, are
      { bufdepth, tlb_mode, color_mode, *color, x, y }.
  tile_nr, tile_nr_x, tile_nr_y, xofs and ofs are NOT additional axes: each is a pure function of
  (x, y, bufdepth, tlb_mode).  So "close every derived coordinate" IS "close the pair (x, y)".
  Table 3 closed the first two inputs; table 4 closes the other four.  The set is read off the
  function and cannot grow by argument -- which is the answer to "is this #392?".  It is not.

THE ADDED ROWS (22)
  Ten nibbles + accept + announce (12), at LIN_A/bufdepth 4/(0,0), DRAWN IN A SECOND FOREGROUND
  COLOUR.  Twelve nibbles reach the default arm; TWO were already driven (0xf0 by `ycrcb put',
  0x50 by `reserved put', both at that same cell), so the new count is TEN, not the eleven the
  reading panel costed -- it counted one already-rowed nibble rather than two.  Because the
  session draws in FG_ALT, it closes the *color axis at ZERO extra rows.

  Four coordinate cells + four accept anchors + a tile-0 anchor + an announce (10), tiled TLB_A
  at bufdepth 4:
      C1 (132,  0)  tile_nr 1   xofs 16  ofs  16  -> re_tlb_a[1]  phys 0x20010
      C2 (  0,  1)  tile_nr 0   xofs  0  ofs 512  -> re_tlb_a[0]  phys 0x10200
      C3 (  0,128)  tile_nr 16  xofs  0  ofs   0  -> re_tlb_a[16] phys 0x40000
      C4 (132,129)  tile_nr 17  xofs 16  ofs 528  -> re_tlb_a[17] phys 0x50210
  against the existing (0,0) where all of them are zero.  Each cell has its OWN tile, so each
  accept is a clause-(f) anchor: it pins which tile and which offset the decode chose, not merely
  that something was written.  `xy anchor t0' re-reads tile 0's own word so a cell that silently
  collapsed onto tile 0 reddens even though its own cell looks untouched.

  x IS 132 AND NOT 128 ON PURPOSE.  At x = 128, `x % tilewidth_in_pixels' is 0, so xofs stays
  zero and `if (xofs == 0) ok = 0;' would sweep the table even with a tile_nr row present.  My
  own pass-2 control used 128 and had exactly that hole; it was found by enumerating the derived
  set against the cells, not by running another table.  y IS 129 AND NOT 128 in C4 because
  `y &= 127' runs before the colour switch.
  C4 IS THE JOINT CELL: `tile_nr == 0 || y == 0' is true at (0,0), C1, C2 and C3 and false only
  at C4, so a corner-free design is swept by the pairwise disjunctions.

THE DELETED ROWS (4)
  `tA/tB/tC ann cum' and `lin ann cum'.  Measured over table 3's 26 mutants each of their kill
  sets is {M1,M11,M5,M7}, a STRICT SUBSET of the matching `ann1' row's -- no kill of its own.
  Checked BEFORE deleting that no mutant loses its only kill.  What they pinned is still pinned:
  `once' is also a whole-transcript announce count and is retained, and the two new blocks add
  `nib ann' and `xy ann'.

  `tA/tB/tC silent' were KEPT, and rather than judging it the table BUILDS the discriminator --
  M38_acceptannounce adds an announce to the RGBA accept arm, which should red `silent' and not
  `ann1'.

  `ycrcb x4y1' was KEPT and is DISCHARGED: pass 2 built the mutants its comment claims to kill
  (`|| ofs', `|| x', `|| y') and each scored 58/59 with that row the sole red.

THE CONTROL-CONSTANT RULE, generalised from my own pass-2 defect
  My pass-2 control set DE_FG to the same 0xaabbccdd the instrument uses, and therefore scored
  M37_fgvalue 10/10 -- reproducing the blind spot it was built to expose.  The rule that follows
  is: FOR EVERY CONSTANT A CONTROL HOLDS FIXED, EITHER VARY IT OR DISCLOSE IT.  Applied here:
  fg is VARIED (FG_ALT); bufdepth and tlb_mode are held fixed for the coordinate cells and are
  DISCLOSED in the contract as (b).  DST_PAINT is held fixed and is not a hazard -- the PUT path
  never reads the destination, so no mutant can condition on it.

================================================================ FILES
  PRETABLE.out                         the pre-table check, written 23:19 -- BEFORE the first
                                       build at 23:22:58.  The mtime is the proof of order.
  BASELINE_FIX519_T4.c                 THE NAMED BASELINE: dev_sgi_re.c, md5 6e2c6873, the same
                                       product file table 3 named.  The driver refuses to run if
                                       it is anything else.  Every leg restores from THIS file.
  sgi_re_colourdefault_probe.T4FROZEN.py  the 77-row instrument, frozen at table start and
                                       cmp-verified against the live probe.  Only this copy ran.
  mut519d.T4FROZEN.py                  table 3's mutator plus the pass-4 mutants.
  BASE.raw, M*.raw                     one instrument log per build.
  build_*.log, mutate_*.log            per-leg build and mutation logs.
  table4.run-t4.sh                     the FROZEN driver as run.
  SCORES4.txt                          THE SCORES.  Read numbers from here, not from this file.
  TABLE4.out                           the table.

================================================================ CLONE, SENTINEL, CLEARANCE
  /tmp/gxop519p2, a `cp -a' of build/.  Clone-local .MUTANT written BEFORE mutant 1, naming
  BASELINE_FIX519_T4.c as its restore source.  The driver ran from a FROZEN COPY.  Per build:
  `rm -f src/devices/dev_sgi_re.o gxemul; make -j4', then [ gxemul -nt dev_sgi_re.c ] -- the make
  return code is not the test, the timestamp pair is.  Restore + two-part clearance at the end;
  the sentinel is cleared only if BOTH parts pass, recorded as output rather than asserted.

  NO PROJECT TREE WAS WRITTEN except this artifacts directory and the probe itself (the round's
  own deliverable).  Product code is untouched.  Propagation is N/A WITH ITS REASON rather than
  blank: est/ carries no regress/, and the build trees compile no regress/, so a probe change is
  owed to neither.

================================================================ THE DIFF IS APPEND-ONLY FOR OLD SESSIONS
  Diffed against the 59-row frozen instrument: 13 lines removed, and every one of them is either
  the superseded contract prose or a row() call -- NO command-emitting code was removed.  So every
  pre-existing session's command stream is byte-identical, and the only change to an old session
  is that four of its rows are no longer scored.

================================================================ GATE WIRING IS OWED, NOT EXEMPT -- CORRECTED
  What I first wrote here was that the probe "is not wired into a gate today".  That is true, and
  I left it sounding like an exemption.  A read-only audit seat challenged the implication and it
  is RIGHT, verified by opening the file rather than taking the seat's word:

      regress/gate_arm.sh:1283   python3 sgi_re_randompixel_probe.py "$PMAX" gate

  That is the SIBLING probe -- same function (horrible_getputpixel), same file, same machine --
  with its own gate block starting at :1267.  So this probe has an obvious home AND a template to
  model on.  The exemptions granted to other recent rounds rested on "no gate runs this CPU
  family", which is NOT true here.

  TWO THINGS FOLLOW, and they are owed rather than optional:
    * wire it into gate_arm.sh beside its sibling, modelled on the :1267 block;
    * PIN 77 ROWS, not 59.  No pinned denominator exists to break today -- a grep for
      sgi_re_colourdefault over regress/ and tools/ matches only the probe's own usage line --
      so the count can be pinned correctly the first time rather than corrected later.

================================================================ A PREDICTION OF MINE THAT THE TABLE CORRECTED
  PRETABLE.out section 4 predicts `M39_xofsguard' (`ok = 0;' -> `if (xofs == 0) ok = 0;') would
  red TWO rows: `xy dec c1' and `xy dec c4', the two coordinate cells with xofs = 16.

  MEASURED: THREE.  The third is `ycrcb x4y1'.

  The reason is a code fact I had not carried into the prediction: `xofs' is computed at
  dev_sgi_re.c:247, BEFORE the `switch (tlb_mode)'.  The LINEAR arm later overrides `ofs' with
  `x & 4095' -- but it does NOT recompute `xofs', which is already (4 % 128) * 4 = 16 at that
  cell.  So M39 permits there too and the row reds.

  Recorded rather than quietly re-fitted, and the prediction in PRETABLE.out is deliberately
  LEFT AS WRITTEN: a prediction edited after the run to match the run is indistinguishable from
  a prediction that was right.  The error was in the SAFE direction -- the instrument killed
  more than I claimed it would -- but it is still an error, and it is the same shape as the one
  the closure exists to fix: I reasoned about a derived quantity without re-reading where it is
  computed relative to the branch that overrides its sibling.
