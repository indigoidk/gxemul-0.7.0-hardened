# pvrrenderexit REGRESS stage (2026-11-05) -- the fb_base cell measured; three wording fixes

Review: `../regress_20261105/REG_MYTHOS_local.md` (section 2(d), section 5).  The candidate pair is NOT in the shipped probe: whether the
cell is floor goes to the ruler and the owner first.  dev_pvr.c and gate_arm.sh untouched; no git.

## 1. Measurement (predictions first: `PREDICTIONS.txt`, 08:36:59; results `meas7/SCORES.txt`, clone /tmp/gxpvr9, sentinel first,
## restored cmp-clean and fresh, sentinel cleared)

| variant | shipped 148 rows | candidate pair (fbhi / zfbhi, FB_RENDER_ADDR1 = 0x200000) |
|---|---|---|
| base | 148/148 | 152/152 |
| FB1s `x > fb_base` (:684) | 148/148, as predicted | red: `fbhi s px`, `zfbhi s px` |
| FB2s `y < (int)REG(PVRREG_FB_RENDER_ADDR1)` (:658) | 148/148, as predicted | red: `fbhi s px`, `zfbhi s px` |
| FB1t `x > fb_base` (:769) | 148/148, as predicted | red: `fbhi t px`, `zfbhi t px` |
| FB2t `y < (int)REG(...)` (:731) | 148/148, as predicted | red: `fbhi t px`, `zfbhi t px` |
| PC1t `x > palette_cfg` (:769) | 148/148, as predicted | NOT red (152/152): the pair sets FB_RENDER_ADDR1, not PALETTE_CFG |
| control CTL1s `x < fb_base` (:684) | CAUGHT: 80/148, CONTROL=FAIL | the four candidate rows green, as predicted |
| restored | 148/148 | 152/152 |

The literal `y < fb_base` in the early return does not compile in either rasterizer: fb_base is declared at :662 / :735, after the
early return at :658 / :731 (`syntax_check_7.out`: "'fb_base' undeclared").  The built form reads the same value the guard can reach,
`(int)REG(PVRREG_FB_RENDER_ADDR1)`, the cast keeping the compare signed as fb_base's int is.  Instruments: `probe148_frozen.py`
(cmp-identical to the shipped probe before the wording fixes) and `cand152_probe.py` (the same rows plus the pair).

## 2. Wording (docstring and comments only)

* R1, clause (c): "its null media are predicted in r5_20261105/PRETABLE_5.out" became "its null media 9/148, 0/148 and 1/148, each
  CONTROL=FAIL (r5_20261105/table5/SCORES.txt)".
* R3, the gate block comment only (the probe has no such sentence): "2.2 s" became "2.1 s", probe_base148f.out's `elapsed 2.1s`.
  (2.2 s is the wrapper's `wall=2.2s`, the file's last line.)
* R5: "before running anything" became "before running that session" -- the probe's STDIN CAP paragraph, the same words in
  session()'s comment, and the gate block comment.

Backups `pvr_zwrite_probe.py.pre_reg`, `gate_pvr_block.new.pre_reg`; diffs `probe_reg.diff`, `gate_reg.diff`.  `AST_PROOF_reg.txt`:
the AST without the docstring is the SAME as table 5's frozen instrument (control DIFFERENT).  The gate block still simulates 157
passed / 0 failed on base148f.

# REPAIR 7 (2026-11-05) -- the guards' constant 0 against the d->reg values the body reads; 148 -> 164 rows

Ruling: `../adj_reg_20261105/ADJ_MYTHOS_local.md` (REPAIR-7, reading (i): 12 FLOOR, 1 DEBT, by its pass-8 .errata.md).  dev_pvr.c
and gate_arm.sh untouched; no git.  The PRETABLE is `PRETABLE_7.out` -- the ruling's "PRETABLE_8"; this round numbers its tables by
repair.

* Cells: `pvr_cells_7.py` -> `cells/` (16 variants: 12 FLOOR cells and 4 PALETTE checks outside the class; meas7's five regenerate
  byte-identical).  Rows: `mk_cand164.py` (input: the 148-row probe, now `pvr_zwrite_probe.py.pre_r7`) -> `cand164_probe.py`, 8
  sessions of 2,824-3,278 bytes (STDIN_CAP 4096).  Fix
  164/164 (`base164/`, both clearance parts), pre-fix 78/164 (`head164/`).  `PRETABLE_7.out` (09:11:05) precedes every result in
  `meas7b/` and `table7/`; its frozen instrument `table7/probe164_frozen.py` (09:10:56) is older.
* Step 2, `meas7b/`: 22 of 22 predictions hit -- the eleven cells 148/148 on the 148 rows, and red on exactly their predicted rows on
  the 164 (`meas7b/CHECK.txt`).
* Table 7, `table7/` (09:13:54-09:30:08): 208 hits, 207 full and 1 partial (Nt on 160 of 164 rows), 0 misses -- six legs, 172
  variants red on exactly their predicted rows, 30 green; 4 wholly unpredicted (Y2s, Y2t, Y4s, Y4t); and not predicted (named in the
  PRETABLE before the run) Nt_inner_or's four palcfg rows, because the raised LEFT3's row 0 spans -3..3 and `x > 0 || x <
  d->xsize` stores at ofs -3..-1, before vram_z and vram.  Measured: the palcfg sessions died in the render under Nt and under Y2t
  (row -1), all four rows red (`table7/CHECK.txt`, `sessions_*`).
* Records: `../r3_20261105/CLOSURE3.errata.md`; `../adj_p6_20261105/ADJ_MYTHOS_local.errata.md`;
  `../adj_reg_20261105/ADJ_MYTHOS_local.errata.md`; `PRETABLE_7.errata.md`; the probe docstring by
  `mk_probe_r7.py` (the contract's operand-swap sentence with the two register sources, the [r7] rows, the DEBT and the excluded
  sources; F3's PROBE-DESIGN NOTE; and what this diff made false: the repair list, "this probe's 148 rows", the legs sentence,
  "FB_RENDER_ADDR1 is 0 here").  `AST_PROOF_r7.txt`: code SAME as table 7's instrument (AST and tokens).  Backup
  `pvr_zwrite_probe.py.pre_r7`, diff `probe_r7.diff`.  OWED: the installed probe's run on build/, after #575's landing window --
  `installed164_window.out` (164/164, 09:37) ran on a build/gxemul relinked at 09:35:57 inside that window and is not attributed.
* Gate block: `gate_pvr_block.new` (`mk_gate_r7.py`, diff `gate_r7.diff` against ../r5_20261105/): 164 rows, 173 checks; simulated
  173/0 on base164 and table 7's base leg, 83/90 on the pre-fix log (`gate_sim_*.txt`).
* Ruling details checked against dev_pvr.c: `x2 < 0` is on :658 / :731 with `x1 < 0`, not on :659 / :732.
  Shape (c) of the probe's EDIT SHAPES extended on the coordinator's direction: the register sources, 39 cells (DERIVED), DEBT,
  and 12 PALETTE forms disclosed apart.
* Clones /tmp/gxpvr10h, /tmp/gxpvr11, /tmp/gxpvr12 removed after the sentinel and cmp checks (`clones_rm_r7b.out`).  Left, clean
  and sentinel-free, from earlier rounds: /tmp/gxpvr2 (table 2), /tmp/gxpvr4 (table 3), /tmp/gxpvr_det (det_20261104).
* Pass 8 (codex, ../p8_20261105/): this note said "16 FLOOR", "(16; the five meas7 measured ...)", "208 of 208 predictions
  hit", "the three register sources" and "51 cells (DERIVED)".  :842 forms the palette's address; its loads are VRAM-indexed.

OWED (added 2026-11-05 by the main loop, from the REGRESS follow-up ../regress_20261105/REG2_MYTHOS_local.md, R-A): the landing kit (_scratchpad/wpvr/landing/) is still pinned to the 148-row probe.  Before R2 can be banked it must be RE-PINNED to the 164-row detector: kit_pvr.py's FROZEN / PIN constants -> r7_20261105/table7/probe164_frozen.py and 164; the staged gate block -> r7_20261105/gate_pvr_block.new; the dry run replayed over table7/'s logs; and the F3 ledger row's text carrying the register extension that the shipped docstring now states.
