# pvrrenderexit repair 4 (2026-11-05) -- rule D2-F's half-pixel rows and the swap body's far end

Ruling: `../adj_p4_20261105/ADJ_MYTHOS_local.md` (pass 4), on `../p4_20261105/codex_codex_pvr_p4.txt`.  B4-B10 FLOOR; B1, B2, B13,
B14 FLOOR under rule D2-F; B3, B11, B12 clause-(e) DEBT; texturedline's fractional moves EQUIVALENT [struck for the START, B2t: see the
2026-11-05 repair-5 correction at the end of this note]; F1-F8 upheld (F1 and F3 with the
ruling's corrections).  **The product is untouched**: `src/devices/dev_pvr.c` is the fix as shipped (md5 481755b4f10fc67a8749884a90594ff9,
== `dev_pvr.c.fix4` == `../r3_20261105/dev_pvr.c.fix3`).  Only `regress/pvr_zwrite_probe.py` was edited; `gate_arm.sh` was not.

## 1. Measure first (before any row was added)

`pvr_variants_B.py` builds codex's fourteen as eighteen single exact edits (B1s B2s B13s B14s, the seven half-exchange deletions
B4s-B10t, B3s B11s B12t, and the texturedline forms B1t B2t B13t B14t); `meas_B.sh` (frozen copy `meas_B.run.sh`, scratch clone
/tmp/gxpvr5 under a clone-local .MUTANT, restored, cmp-clean, rebuilt fresh, sentinel cleared) ran them on the frozen 128-row probe
(`meas_B/probe128_frozen.py`, cmp-identical to `pvr_zwrite_probe.py.pre_r4`):

    meas_B/SCORES.txt: base 128/128; every one of the 18 variants 128/128 RED=none; restored 128/128

So all fourteen of codex's edits survive the 128-row probe, as codex derived: 14 survivors and the 4 texturedline forms green (the ruling
predicted exactly that).  After the rows, `meas_B140.sh` (clone /tmp/gxpvr5b, same discipline) ran the three DEBT variants on the
140-row probe: `meas_B140/SCORES.txt` -- B3s, B11s, B12t each 140/140, base and restored 140/140.  Still green: the disclosed debt.

## 2. The twelve rows (128 -> 140), each want re-derived from the code before it was written

No want differed from the ruling's.  Checked against `dev_pvr.c` (simpleline, texturedline, pvr_render_triangle{,_textured}): vertices
reach both sweeps as ints; a flat top's first row carries both vertices' values exactly; simpleline's loop is `for (int x = x1; x <= x2;
++x)` with `x > 0 && x < d->xsize` inside and the steps (`z += dz12` ...) at the END of each pass, so column x1 + k carries the start
value plus k steps; the colour is clamped to 0..255 per channel before the RGB565 pack; texturedline's texel is `(int)(u * 8) & 7`,
`(int)(v * 8) & 7`, at linear `((a & 4) << 20) | (a & 3) | ((a & 0x7ffff8) >> 1)`; the right clause is tested BEFORE the swap.

| row | pixel | want | geometry (all exact in binary) |
|---|---|---|---|
| swap s start, zswap s start | (399,249) | RED | SWAP row 249 arrives 400.5 / 399.5; swapped, `int x = 399.5` = 399 |
| half swap, zhalf swap | (101,103) | RED | HALF [(102,100),(100,100),(101,104)]: row 103 arrives 101.25 / 100.75, swapped, draws 100, 101 |
| half r x1, zhalf r x1 | (639,401) | RED | HALFR1 [(639,400),(700,400),(640,402)]: row 401 arrives 639.5 / 670.0, drawn from 639 |
| half r x2, zhalf r x2 | (639,411) | RED | HALFR2 [(700,410),(639,410),(640,412)]: row 411 arrives 670.0 / 639.5, swapped, drawn from 639 |
| ramp8 r end | (448,60) | 0xf81f | RAMP8 [(448,60),(440,60),(444,64)] z (2,1,2), magenta/green/magenta, then COVER8 [(438,50),(458,50),(448,70)] z 1.5 blue |
| zramp8 r end | (448,60) | 0xf81f | COVER8 (Z-on) first, then RAMP8 Z-off: 2.0 passes over 1.5 |
| texramp8 r end | (448,60) | GREEN | RAMP8 textured, uv (0.5,0) (0,0.125) (0.5,0), texel (4,0); COVER8 through TEX_01 = 0x200010 (texel (0,0) = TEXEL01, blue) |
| ztramp8 r end | (448,60) | GREEN | COVER8 textured (Z-on) first, then RAMP8 textured Z-off |

Two things the derivation found that the ruling did not state, both carried into PRETABLE_4 as predictions, not claims: **B2s also
reddens the four half-r rows** (639.5 + 0.5 truncates to 640, so nothing is drawn), and **As (`x1 - 1`) and V5s (Z-off `x1 - 2`) do NOT
red the ramp8 rows**: column 448 then carries z 2.125 / 2.25 and colour (286.875, -31.875, 286.875) / (318.75, -63.75, 318.75), which
CLAMP to magenta (At likewise stays on texel (4,0)).  Those edits are held by `ramp l end` / `zramp l end`, as table 3 measured.

Sizes (an absent-binary run of the probe, every session built and cap-checked; scratchpad sizing): 48 sessions (4 witness + 44
render); new and changed: swap 4011, zswap 4017, half 3937, zhalf 3943, ramp8 2738, zramp8 3092, texramp8 3235, ztramp8 3241; the
largest is still ztyedges, 4066 -- every one under STDIN_CAP 4096.

Legs (on the probe with its legs sentence still blank; every later probe differs from that one in DOCSTRING lines only, and each was
re-run on build/: `base140f/` is table 4's instrument, `base140g/` the shipped probe, whose diff from table 4's instrument is
`probe_final_vs_table4.diff` -- checked to lie wholly inside the module docstring, the code after it identical):
* `base140/`, `base140f/`, `base140g/` -- build/gxemul, read-only, with the two-part clearance RUN and recorded first each time
  (`CLEARANCE.txt`): dev_pvr.c is
  a shared file (not in tools/est_divergence.txt); `cmp build/src/devices/dev_pvr.c GXEMUL-SEC/...`: CLEAN; `build/gxemul -nt
  build/src/devices/dev_pvr.c`: YES; no build/.MUTANT.  **140/140, CONTROL=OK, SYMPTOM=ABSENT, ~2 s, no session timed out.**
* `head140/` -- the pre-fix build (det_20261104/dev_pvr.c.HEAD) in clone /tmp/gxpvr4h (sentinel first; restored 140/140, cmp-clean,
  fresh, sentinel cleared): **66/140, SYMPTOM=PRESENT, CONTROL=OK** -- the 128-row probe's 68 red rows plus exactly the six repair-4
  rows whose session carries a Z-off header (zswap s start, zhalf swap / r x1 / r x2, zramp8 r end, ztramp8 r end).

## 3. Records (F1-F8)

| finding | where it landed |
|---|---|
| F1 | `../r3_20261105/CLOSURE3.md`: section 2's sentence now reads "...without a row or a named clause-(e) disclosure"; A3's "least move" now says INTEGER, with the half-pixel sentence (`< 0.5` EQUIVALENT, `< 1.5` caught by `edges2 l tip` / `edges2 x2 tip`); section 6's fractional-swap item WITHDRAWN (struck, kept) and its first-pixel clause corrected -- each correction quoting what it replaces.  The probe's own left-clause line said "a move by TWO" too and now says INTEGER, with the same half-pixel sentence.  The ruling DERIVED the left clause's half-pixel moves; they were then BUILT (`pvr_variants_L.py`, four single edits) and measured on the 140-row probe, predictions written first (`meas_L/PREDICTIONS.txt`): `x1 < 1.5` red exactly `edges2 l tip`, `zedges2 l tip`; `x2 < 1.5` exactly `edges2 x2 tip`, `zleft tip`; `x1 < 0.5`, `x2 < 0.5` green (`meas_L/SCORES.txt`, clone /tmp/gxpvr5c restored) |
| F2 | the probe docstring (table 3 RAN: 04:10:23-04:19:18 local, 129 of 130 hits, the Vt miss) and `gate_pvr_block.new`'s comment |
| F3 | CLOSURE3 section 8: "each would have survived the 68-row probe" (table 3 measured every V variant red on repair-3 rows only), with the ruling's correction to codex -- the 91-row zleft drew ONE triangle, LEFT2, and four V representatives (V1s, V6s, V2t, V7t), not five, would have been red there; V5t survives |
| F4 | the probe docstring's STDIN CAP paragraph and the comment above STDIN_CAP: byte 100 is true of RENDER sessions; id and neg step at byte 93 |
| F5, F6 | `../r3_20261105/PVR3_NOTE.md`: a dated ADDENDUM (the 85-row and 3972/4060 lines left as written) |
| F7 | `../r3_20261105/table3/VERDICT.errata.md` (new): the table ran 10:10-10:19Z, not "~10:4x" |
| F8 | `../r3_20261105/PRETABLE_3.errata.md`: a second, dated erratum -- the reason corrected, the class kept |

**F8's false reason had a sibling in the live probe** (the docstring's M17 disclosure: "the render loop has no early exit after the
reset's old position"), corrected in place with the same reason.  **Not corrected, outside repair 4's write scope:**
`../det_20261104/table1/VERDICT.md` line 13 carries the same false reason; the frozen probe copies under base*/, head*/, meas_*/ and
table*/ carry it too and stay as the records of what was run.

## 4. Denominator

**181 input cells**: CLOSURE3's 173 plus eight half-pixel cells -- simpleline's four position compares that the 173 did not cut at the
half pixel (the swap `x1 > x2`, the start `int x = x1`, the right clause's x1 and x2 compares), each with Z-write on and off.  (The span
end's half-pixel cell was already one of the 173: simpleline's fractional end, `swap frac past`.)  And **the fourteen A1 cells** (z, r,
g, b; z, u, v; each Z-state) **are each pinned at TWO edges**: the reversed span's left end (`l end`, the `a1 = a2` half) and its right
end (`r end`, the `a2 = tmpf` half).  Codex's 177 counted two of the four compares (the swap and the start), each in both Z-states;
the right clause's two it reached as edit shapes in already-counted cells.

## 5. codex's ELSE (not a false record)

`regress/gate_arm.sh` still holds the 68-row block.  That is the disposition, not a defect: the block is applied after the fbsdram
release.  `gate_pvr_block.new` here is now the 140-row block (140 names on one line, the four counts at 140) and supersedes
`../r3_20261105/gate_pvr_block.new`, whose line 17 still says table 3 is "prepared, not yet run" as the record of repair 3's state.
`gate_block_sim.sh` (copied from repair 3) runs the block against a finished log: `base140f` 149 passed / 0 failed
(`gate_sim_base140f.txt`), `head140` 71 passed / 78 failed (`gate_sim_head140.txt`), and the old 128-row log 133 passed / 16 failed --
the twelve absent names and four counts (`gate_sim_old128.txt`).  gate_arm.sh is NOT edited.

## 6. Table 4

`pvr_variants_4.py` (146 variants: table 3's 128 copied, each checked against the md5 table 3 built; codex pass 4's 18 from meas_B,
checked likewise); `PRETABLE_4.out` written FIRST and exact -- the frozen instrument `table4/probe140_frozen.py` 05:26:24.98,
PRETABLE_4.out 05:26:25.40, the first result 05:27:16 -- with its instrument md5 (790b5ac3...) checked by the driver before leg 1.
The 128 carried-over rows are predicted by table 3's MEASURED red sets (meas_B's for the 18); the 12 new rows by a per-variant
derivation that names every Z-on row and every Z-off twin -- no twin rule, which is how table 3 lost Vt's twin (a `startswith("V")`
filter swept Vt_swap_nov into the V family's empty twin list).  Driver `table4_pvr.run.sh` (frozen copy), clone /tmp/gxpvr6 under a
clone-local .MUTANT, restored cmp-clean and fresh, sentinel cleared; the clone was then removed (`clones_rm_r4.second.txt`).

    table4/CHECK.txt: TABLE4_CHECK hits=148 misses=0 not_predicted=4     (TABLE.log 05:27:20-05:36:16 local, 152 legs, no timeout)

* legs: base 140/140; HEAD 66/140 SYMPTOM=PRESENT; null media 9/140, 0/140, 1/140 (CONTROL=FAIL); restored 140/140;
* 130 variants red, each on exactly its predicted set: the eleven FLOOR edits on their repair-4 rows only (B1s `half swap` + twin;
  B2s `swap s start` + twin and the four half-r rows; B13s `half r x1` + twin; B14s `half r x2` + twin; B4s-B7s ramp8 + zramp8;
  B8t-B10t texramp8 + ztramp8), and every swap-body exchange deletion, whole or half, on BOTH twins;
* 12 green, each predicted and named: EQUIVALENT M17, L1s, L1t, It, H65; EQUIVALENT by D2-F (iv) B1t, B2t [EQUIVALENT struck: see the
  repair-5 correction below], B13t, B14t; DEBT by D2-F
  (ii)/(iii) B3s, B11s, B12t;
* NOT PREDICTED: Y2s, Y2t, Y4s, Y4t (undefined behaviour), red on the same sets as in table 3.

Verdict: `table4/VERDICT.md`.  The probe's contract and the gate block's comment now cite this table.

## Correction (2026-11-05, repair 5 -- codex pass 5 R1, the pass-5 ruling's R3; ../adj_p5_20261105/ADJ_MYTHOS_local.md sections 3-4)

**EQUIVALENT is struck from B2t and from the span-start family.**  This note called texturedline's fractional moves EQUIVALENT, B2t
among them, and the D2-F disclosure repair 4 wrote into the probe put `int x = x1 + c` among the moves SAMPLED below half a pixel.
Both are false for the
START: `int x = x1 + c` truncates toward zero (dev_pvr.c:683, :768), so at a NEGATIVE start it begins at x1 + 1 for every 0 < c <= 1, and
the attributes -- set at :682 / :766 and advanced at the end of every pass, clipped passes included -- then arrive one step behind.  One
row pins the whole family.  [2026-11-05, repair 6: "every 0 < c <= 1" and "the whole family" hold only down to the start's double
resolution -- -1 + 2^-54 rounds back to -1.0, and c = 2^-54 is SAMPLED (the pass-6 ruling's R3): ../r6_20261105/RECORDS6_NOTE.md.]
B2t's green measurement on 140 rows stands (table 4); its class does not: it is a floor breach, rowed by
repair 5 (`texnegx n start`), and simpleline's start owes the same row (`negx n start`; N1s, `int x = x1 + 0.25`, survived 140 rows).
B1t, B13t and B14t stay EQUIVALENT -- every texturedline position COMPARE has int operands, negative ends included.  Errata beside the
other two records: `PRETABLE_4.errata.md`, `table4/VERDICT.errata.md`; repair 5's record: `../r5_20261105/PVR5_NOTE.md`.
