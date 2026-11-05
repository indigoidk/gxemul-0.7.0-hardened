# pvrrenderexit repair 5 (2026-11-05) -- the swap body's deletion closure, its right end from above, a negative span start

Ruling: `../adj_p5_20261105/ADJ_MYTHOS_local.md` (pass 5), on `../p5_20261105/codex_codex_pvr_p5.txt`.  3 FLOOR (simpleline's `tmpf = z1;`
deleted; B2t; N1s, `int x = x1 + 0.25`), 26 DEBT (the compound substitutions), R1 and R2 upheld, R3 the ruler's own.  **The product is
untouched**: `src/devices/dev_pvr.c` md5 481755b4f10fc67a8749884a90594ff9 == `dev_pvr.c.fix5`.  Only `regress/pvr_zwrite_probe.py` was
edited; `gate_arm.sh` was not (the fbsdram implementer holds it).  One diff: rows, contract, errata, table 5.

## 1. Measure first -- every prediction held

`pvr_variants_5.py` builds 44 single exact edits (the 17 deletion cells not built before -- DTs_z/r/g/b, DTt_u/v; DAs_z/r/g/b, DAt_z/u/v;
DXs_x1/x2, DXt_x1/x2 -- N1s, and codex's 26 compound survivors); B2t is table 4's file.  `syntax_check_5.out`: all 45 compile, and the
three declarations deleted alone (`double tmpf = x1;`, `int tmp = x1;`, `double tmpf = z1;`) are each refused (`'tmpf' undeclared`,
`'tmp' undeclared`), as the ruling says.  Predictions written first (`meas140/PREDICTIONS.txt`), then `meas140.sh` (clone /tmp/gxpvr7,
sentinel first, restored and verified) on the shipped 140-row probe:

    meas140/CHECK.txt: MEAS140_CHECK hits=47 misses=0

* survived, as predicted: DTs_z (`tmpf = z1;`), N1s, B2t, and all 26 compounds -- 140/140 each;
* red, each on the rows the ruling named and its Z-off twin: DTs_r and DTs_g on `ramp8 r end` (and twelve other swapped-span rows each:
  a wrong r2 or g2 changes every constant-red reversed span), DTs_b on `ramp8 r end` only, DTt_u on `texramp8 r end` (and `texyedges s
  end`), DTt_v on `texramp8 r end`; DAs_* on `ramp l end`, DAt_* on `texramp l end`; DXs_x1 / DXt_x1 on `yedges swap` / `texyedges
  swap`, DXs_x2 / DXt_x2 on those and `s end` (and further swapped-span rows).
* (My first scoring script split `ramp_l_end, zramp_l_end` at the comma-space and reported 11 false misses; fixed before any row was
  written, re-scored 47/47.)

## 2. The rows (140 -> 148): six owed, two optional on a measured delta

| row | pixel | want | session |
|---|---|---|---|
| ramp8hi r end, zramp8hi r end | (448,60) | BLUE | RAMP8 z (3,2,3) magenta/green/magenta, COVERHI [(430,50),(470,50),(450,70)] z 4.0 blue after it (Z-off twin: COVERHI first) |
| ramp8hi l end, zramp8hi l end | (440,60) | BLUE | the same sessions -- OPTIONAL |
| negx n start, znegx n start | (1,60) | RED | NEGX [(-1,60),(1,60),(0,62)], colours (green, red, green), z 2.0 |
| texnegx n start, ztnegx n start | (1,60) | GREEN | NEGX textured, uvs (0,0) (0.5,0) (0,0), the existing texels() |

Every want re-derived from the code first (flat tops: the first loop is empty and `stopx = x2`, dev_pvr.c:973 / :1052; vertices
truncate to int, :1335-1336; the start `int x = x1` at :683 / :768 truncates toward zero; attributes set at :682 / :766 and advanced at
the end of every pass, :721, clipped passes included; texel address :801-802).  The candidate probe with all eight rows was measured
BEFORE the rows were final (`meas_cand/`, predictions first, exact): 16 of 16 legs as predicted -- DTs_z on `ramp8hi r end` + twin, N1s
on `negx n start` + twin, B2t on `texnegx n start` + twin, simpleline's five right-end depth compounds on the r end rows, **`z1 += z2`
and `z1 *= z2` on the l end rows -- the addition licence, so the optional rows stay** -- and texturedline's four depth compounds green
on all 148 rows.  Sizes: 54 sessions; the new ones 1634-3131 bytes; the largest is still ztyedges, 4066 (cap 4096).

Legs: `base148/`, `base148f/` (table 5's instrument) -- build/gxemul, two-part clearance run and recorded first (`CLEARANCE.txt`: cmp
CLEAN, binary newer, no sentinel): **148/148, ~2 s, no timeout**.  `head148/` (pre-fix, clone /tmp/gxpvr7h): **70/148, SYMPTOM=PRESENT**
-- the 140-row probe's 74 red rows plus exactly the four new rows in Z-off sessions.

## 3. Ruling claims checked against the code -- and the ones that did not hold

Verified: every line number written into the contract (:658's `x1 < 0`, :664-668, :683, :721, :737-740, :768, :801-802, :973, :1052,
:1335-1336); the witnesses' arithmetic (448.0 at column 448; 0x7be0 at (1,60) under N1s; texel (2,0) -> linear 0x500000 under B2t);
the texel addresses ((4,4) 0x100024; (2,3) 0x500018; (4,2) 0x100014) and codex's colours (0x218a, 0x3b10); the three declarations.

**Did not hold, so not written as the ruling wrote it:**
1. *"Eleven of the twelve depth survivors ... are nevertheless predicted red by the owed `ramp8hi` rows."*  `ramp8hi` is untextured, so
   texturedline's four depth compounds (`z1 += z2`, `z1 *= z2`, `z2 += tmpf`, `z2 *= tmpf` at :738) cannot red it: MEASURED green on
   the 148-row candidate.  Simpleline's two `z1` members red only the optional l end rows.  PRETABLE_5 predicts 7 red, 4 green as debt.
2. The disclosure's *"screened 80 ... 46 caught"*: 46 is codex's count over 86 forms (its six temporary deletions included); of the 80
   compounds 41 are caught (86 - 27 survivors - 13 undefined - 5 caught deletions).  Written as 41.
3. *"26 survive on zero operands and colour saturation"*: not why the depth members survive (their altered depths fall on the same side
   of every tested threshold) nor `u2 -= tmpf` (the texel mask wraps -0.5).  The reason clause is dropped; the counts stay.
4. *"at any of their 27 statements"*: three are declarations, which take no compound form.  Written as 24 assignment statements.
5. The **13 non-finite forms** were counted by codex and named by no one.  DERIVED here and named in PRETABLE_5 (`/=` by an operand
   that is 0 on a drawn swapped span): simpleline `r1 /= r2`, `tmpf /= g1`, `g1 /= g2`, `g2 /= tmpf`, `tmpf /= b1`, `b1 /= b2`, `b2 /=
   tmpf`; texturedline `tmpf /= u1`, `u1 /= u2`, `u2 /= tmpf`, `tmpf /= v1`, `v1 /= v2`, `v2 /= tmpf` -- thirteen, codex's count.
   Excluded from table 5, not built.

Each correction is quoted in the probe beside the text it replaces.

## 4. Contract (the probe's docstring)

* the 24-cell deletion closure, its three undeletable declarations (compiler-checked) and the row holding each cell with its twin;
* the ruler's corrected D2-F paragraph, replacing the old one (the old SAMPLED and EQUIVALENT sentences quoted in its correction);
* the compound-substitution disclosure, with corrections 1-4 above;
* the COVER8 sentence (R2): "Blue keeps the z2, u2 and v2 signatures distinct; a red COVER8 would merge the first two without hiding
  either."
* the [r5] rows in COVERED, the repair-5 header sentence, and the measured legs.

## 5. Records (R1, R3)

EQUIVALENT struck from B2t and from the start family: `../r4_20261105/PVR4_NOTE.md` (dated correction, in place);
`../r4_20261105/PRETABLE_4.errata.md` and `../r4_20261105/table4/VERDICT.errata.md` (new).

## 6. Denominator

**185 input cells** -- the 181 plus the negative-start cell per rasterizer per Z-state (4); the A1 cells pinned at both ends, and
simpleline's z cells now also from above at both ends (texturedline's are not -- item 1 above); **24 statement-deletion cells**, each
held by a measured row; **codex's 80 compound forms** screened (26 measured survivors on 140 rows, 13 undefined and named, 41 caught by
codex's derivation, not built).

## 7. Gate block

`gate_pvr_block.new`: 148 names, the four counts at 148, the comment updated (fifty render sessions; tables 4 and 5).
`gate_block_sim.sh` against finished logs: `base148f` 157 passed / 0 failed; `head148` 75 / 82; the 140-row log 145 / 12 (the eight
absent names and four counts).  gate_arm.sh is NOT edited.

## 8. Table 5

`pvr_table5.py` (190 variants: table 4's 146, each md5-checked against what table 4 built, and repair 5's 44 from meas140); old rows
predicted by the MEASURED red sets of table 4 and meas140, the eight new rows DERIVED per variant (`NEW5`, every twin by name);
`PRETABLE_5.out` written first and exact (frozen probe 06:28:22, PRETABLE_5 06:29:02, first result 06:29:50; instrument md5 checked by
the driver).  Driver `table5_pvr.run.sh`, clone /tmp/gxpvr8 under its sentinel, restored and verified, then removed.

    table5/CHECK.txt: TABLE5_CHECK hits=192 misses=0 not_predicted=4      (TABLE.log 06:29:53-06:40:24 local, 196 legs, no timeout)

* legs: base 148/148; HEAD 70/148 SYMPTOM=PRESENT; null media 9/148, 0/148, 1/148 (CONTROL=FAIL); restored 148/148;
* 156 variants red, each on exactly its predicted set: the three FLOOR cells on their new rows only; all 24 deletion cells on their
  named row AND its Z-off twin (checked cell by cell); simpleline's seven depth compounds on the ramp8hi rows;
* 30 green, each predicted and named: EQUIVALENT M17, L1s, L1t, It, H65, B1t, B13t, B14t; DEBT B3s, B11s, B12t and 19 compounds
  (texturedline's four depth members -- the ruling's "red on ramp8hi" refuted -- and the 15 colour and UV members);
* NOT PREDICTED: Y2s, Y2t, Y4s, Y4t (undefined behaviour), the same sets as before; EXCLUDED: the 13 non-finite forms.

Verdict: `table5/VERDICT.md`.  The probe now cites the table; `base148g/` runs the shipped probe on build/ (148/148, clearance
recorded), and `code_same_final_vs_table5.txt` shows it is token-identical to table 5's instrument outside comments and the docstring
(`probe_final_vs_table5.diff`: 15 changed lines, all comments).
