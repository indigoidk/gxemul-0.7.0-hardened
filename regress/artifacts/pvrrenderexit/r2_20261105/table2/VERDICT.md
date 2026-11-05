# pvrrenderexit -- test-variant TABLE 2 (repair 2: the class closure, 68 rows), 2026-11-05 ~07:1x-08:1xZ

Driver `../table2_pvr.run.sh` (frozen copy), WSL scratch clone /tmp/gxpvr2 under a clone-local .MUTANT sentinel; restored, cmp-clean
against GXEMUL-SEC, rebuilt fresh, sentinel cleared (TABLE.log).  Instrument `probe68_frozen.py` == the in-tree probe after repair 2
(cmp-identical to base68/probe68b_run.py, 68/68 on build/; the first base run timed out a 16-command mask session, split in two:
base68/SPLIT_NOTE.md).  `../PRETABLE_2.out` was written before the driver (the only older file here is the frozen probe, copied
first).  Variants `../variants/` (table 1's 36 reused verbatim, 26 new from `../pvr_variants_2.py`).  Scores: SCORES.txt.

* base 68/68, CONTROL=OK.  HEAD 42/68: the Z-off sessions end the process, as in table 1.  Null media: /bin/true 9/68, an absent
  binary 0/68, /bin/false 1/68 -- CONTROL=FAIL on all three.
* ZERO misses: table 1's 36 each kept (at least) its table-1 red set; the 22 new variants predicted EXACTLY all matched -- the y
  bounds (Y1, Y3 -> t in / b in), the left/right `&&` -> `||` (O1, O2), the right-clause tightening (R1 -> rspan), the span end
  (E1 -> s end; E2 -> s past), the span start (X1 -> rspan), the swap deleted (S1 -> swap + s end), each per rasterizer; the two
  decode-mask widenings (K1 -> mask overlap; K2 -> mask25 overlap -- the row repair 2 added BEYOND the four rulings, whose premise
  that texon already catches K2 was false: no probe header sets word 1 bit 25); L1s/L1t (left-clause tightening) GREEN as predicted
  EQUIVALENT.
* NOT PREDICTED (undefined behaviour), all red: Y2s/Y2t (`y < -1`: the colour store and depth read land before their buffers) red
  the whole yedges / texyedges session (6 rows each); Y4s/Y4t (`y > ysize`: the depth read past the frame-exact vram_z) red only
  `b out` (row 480 drawn) on this build.
