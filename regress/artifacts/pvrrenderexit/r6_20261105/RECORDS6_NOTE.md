# pvrrenderexit repair 6 (2026-11-05) -- records only, after the pass-6 ruling

Ruling: `../adj_p6_20261105/ADJ_MYTHOS_local.md` (`0 FLOOR 29 DEBT 1 RECORDS UPHELD VERDICT:CLOSE-AFTER-RECORDS`), on
`../p6_20261105/codex_codex_pvr_p6.txt`.  Text only: no row, no table, no build (no printed string changed), dev_pvr.c and gate_arm.sh
untouched.  Backup first: `pvr_zwrite_probe.py.pre_r6` (md5 0fa83b8191ee01c03ec64545bb569cbe, the repair-5 probe).

## 1. R3 (the pass-6 ruling's section 3), in the probe's D2-F paragraph

The start sentence is replaced by the ruling's wording; the old one is quoted in a dated note beside it, and the repair-5 note's
"one row pins every `int x = x1 + c`, 0 < c <= 1" gains "[repair 6: for 2^-54 < c <= 1 only]".  Arithmetic re-done in binary64
(`r3_arith.py`, output `r3_arith.out`): -1 + 2^-54 is -1.0 (tie to even); just above 2^-54 the sum is -1 + 2^-53 and truncates to 0;
codex's (B) witness row 60 starts at 0.9999999999999999 = 1 - 2^-53 with x2 - x1 = 2.0, so the fix puts (85, 170, 0) = **0x5540** at
(1,60) and `x1 + 2^-54` starts at 1 with vertex 1's green 0x07e0; among the doubles just below 1, 2, 3, 4 only 1 - 2^-53 moves.
**Four precision fixes to the ruling's sentence, each checked:** (i) "for every c > 2^-54" dropped the family's upper bound
(`int(-1 + 2.0)` is 1, not 0) -- written "c in (2^-54, 1]"; (ii) "the sum rounds to -1 + 2^-53" holds for c just above 2^-54 only --
"or nearer zero" added; (iii) texturedline's "an int start plus 2^-54 rounds back to the int" is not true at 0 (0 + 2^-54 is exact) --
"or at 0 truncates to it" added; (iv) its probe line numbers ":297, :776-785" (same-file, shifting with every edit) became the construct
names NEGX and the negx sessions.  The witness is marked DERIVED, not measured (the ruling's section 4: the measurement is not owed).

## 2. Codex pass 6, corrected on record

* **Denominator.**  "108 CELLS SWEPT" was 24 statement deletions plus 84 field substitutions (24 x, 24 depth, 36 RGB).  It omitted UV's
  24 field cells: the field-substitution shape has **108** cells (the ruling's section 2(c)), so the sweep codex described is 132 cells,
  and the shapes named here are the ruling's nine in section 2 [PASS 7: plus (j); this said "the full enumeration"].
* **(B)'s want.**  Codex wrote "midpoint 0x7be0" -- NEGX's midpoint.  This triangle's colour at column 1 is **0x5540** (section 1 above).

## 3. The enumeration (the probe's EDIT SHAPES paragraph, replacing repair 5's COMPOUND ASSIGNMENTS paragraph)

One entry per shape, (a) to (i), each with its grade, count, survivors by name and remedy set, citing the ruling's section 2 for the
derivation; plus the three remedy sets (the UV set amended to (0.375, 0.25) / (0.25, 0.375)) and the value-coincidence note (depth 2.0 =
d->bytes_per_pixel).  Counts checked: (b) 26 + 13 + 41 + 16 + 8 + 4 = 108; (c) 79 + 21 + 8 = 108, the 21 named = 12 depth + 8 RGB + 1 UV,
the 8 undetermined named; (f) 19 + 8 = 27.  Measured statements are marked MEASURED (table 5: the 24 deletion cells, the 7 depth
compounds red on ramp8hi, the 19 compound survivors); everything else stays DERIVED.  The amended UV values were checked: -0.375 masks to
column 5, -0.25 to row 6; `u2 -= tmpf` gives -0.125 (column 7), `u1 *= u2` 0.09375 (column 0), `v1 += v2` 0.625 (row 5).

**Two ruling claims that do not hold, corrected in the probe (DERIVED):**
* (e) "any r2 in [248, 256), any g2 or b1 below the quantum survives": `half swap`'s row 103 is half a pixel wide (100.75..101.25) and
  its loop starts at 100, so column 101 gets twice the endpoint's change -- r = 2 r2 - 255 (248 reads 241: 30, not 31, in RGB565) and
  g = 2 g2 (2 reads 4).  r2 in [248, 251.5) and g2 in [2, 4) are caught; written "r2 in [251.5, 256), g2 below 2, b1 below 8".  (The
  ruling's own section 1 and codex both note the g2 = 2 case at column 101; section 2(e) did not carry it.)
* The tally "codex's 20, (A), (B), the 8 sign survivors, `int tmpf`: 29 named cells" sums to **31** (20 + 1 + 1 + 8 + 1).  The probe
  names each survivor per shape and writes no total.

## 4. Siblings

The universal "every 0 < c <= 1 ... one row pins the whole family" also stood in `../r4_20261105/PVR4_NOTE.md` and, as "the start family
is not SAMPLED below half a pixel", in `../r4_20261105/PRETABLE_4.errata.md`: each gains a dated repair-6 bracket pointing here.  The
gate block (`../r5_20261105/gate_pvr_block.new`) repeats none of the corrected claims: no patch, and its row count stays 148.

## 5. Proof that the edit is text only -- `AST_PROOF.txt`

The shipped probe against table 5's frozen instrument (`../r5_20261105/table5/probe148_frozen.py`): **AST without the docstring SAME**
(153280 chars each), code tokens SAME (7966 each); control, against the 140-row probe: DIFFERENT.  So table 5's 192 hits stand for the
shipped probe.  The whole edit is `probe_r6.diff` (docstring lines only).  No build was needed; as a sanity check the shipped probe ran
once on build/gxemul, read-only, clearance recorded: 148/148 (`base148r6/`).

## 6. Denominator for pass 7 (the ruling's, with the tally corrected)

24 deletion cells (FLOOR, held); 108 compound forms (96 arithmetic, 12 int-only: 26 measured survivors of 140 rows, 19 of 148, 13
non-finite, 4 undefined, the rest caught); 108 field-substitution cells (21 derived survivors, 8 undetermined, 79 caught); 27 sign forms
(8 survivors); reorder and target changes held by (a); the type change at :664 (1 survivor); three open families [PASS 7: four, with (j)] (other local,
constant, insertion) disclosed with their bands.  Named DEBT cells: 31, plus 8 FP-sensitive cells to measure.

## PASS 7 (2026-11-05) -- seven record items, text only

Codex pass 7 (`../p7_20261105/codex_codex_pvr_p7.txt`, section 3): zero floor breaches over 272 cells; seven items in the
enumeration's prose.  Each was deleted or narrowed in the probe's docstring.  Backup `pvr_zwrite_probe.py.pre_p7rec`, diff
`probe_p7rec.diff` (docstring lines only), proof `AST_PROOF_p7.txt`: the AST without the docstring is the SAME as table 5's frozen
instrument (the control, the 140-row probe, DIFFERENT).
* R1, one line added: "(j) other right-hand-side expression changes, casts included -- an open family, DEBT, not enumerated"; (i)'s
  label "other single-site shapes" narrowed to "type change, duplication, insertion, guard"; "the three sets" became "the sets below";
  this note's "the full enumeration" narrowed above.
* R2, mechanism deleted: "(the sum rounds back to x1 for |x1| >= 0.5 and cannot reach an integer below it)" became "(DERIVED: the sum
  truncates to the same integer as x1)".  At x1 = -0.5, -0.5 + 3 * 2^-56 is -0.49999999999999994 and still truncates to 0
  (`p7_checks.out`, which also samples 20,029 values of x1).
* R3, narrowed: "b1 below 8" became "0 <= b1 < 8" (b1 = -8 reads 0xf801 at (101,103), `p7_checks.out`); "g2 below 2", the same
  unbounded form, became "0 <= g2 < 2".
* R4, deleted: "`!tmpf` and `!x` act as the W column of (c)".
* R5, universal deleted: "every move caught" became "texturedline `x2 = tmp` moved after its z exchange is EQUIVALENT".
* R6, rewritten: "a duplicated statement EQUIVALENT" became "adjacent duplication of an assignment is EQUIVALENT; duplicating a
  declaration does not compile" (`dup_check.out`: `redefinition of 'tmpf'`; the duplicated assignment compiles).
* R7, rewritten: the depth remedy keeps RAMP8 depths (3, 2, 3) under a cover at 4.0 beside (1, 1, 1) under COVERHI at 1.5, both
  rasterizers and Z-states; the all-one set alone leaves texturedline `z1 *= z2` and `z2 *= tmpf` at 1.0.
No row, table, build, git or gate_arm.sh.  The gate block repeats none of these claims.
