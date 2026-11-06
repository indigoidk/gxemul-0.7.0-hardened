# fbsdrampair -- test-variant table 1, verdict (2026-11-05, 10:29-10:34 local)

Written after every log was in this directory and verified: TABLE.log ends `TABLE1_DONE`; 46 probe outputs, each
ending in `PROBE_WALL` (DONE=1 on all 46 SCORES lines); every line's NRED equals total minus green.

**Predictions against measurements: 46 of 46 lines match their EXACT predicted red set and control
(COMPARE.txt) -- 0 misses.**  PRETABLE_1.out (mtime 10:28) precedes TABLE.log, runs/ and SCORES.txt (10:29 on).

| leg / family | predicted | measured |
|---|---|---|
| base (fix1, rebuilt in the clone) | 56/56, CONTROL=OK | 56/56, CONTROL=OK |
| HEAD (pre-fix source, built in the clone) -- clause (a) | 46/56, red M1 M2 M3 O1 O2 O3 X1 B1 B2 B3 | same |
| null_absent, null_true, null_false -- clause (c) | 1/56 (D1 only), CONTROL=FAIL | same, all three |
| b_exit_mask, b_exit_offset -- clause (b), HEAD's two lines verbatim | 7 rows each | same |
| 38 further variants (clause (d) null-repair forms, the rulings' latch-collision and announce variants) | exact sets in PRETABLE_1.out | same, every one |
| restored (cp from GXEMUL-SEC, rebuilt) | 56/56 | 56/56 |

* **34 of 40 variants killed.  The 6 green were all predicted green:** five EQUIVALENT -- d_exchanged (a latch
  renaming), d_predlatch_mask/offset (under a 0 decline a later read diverted to the write arm is silent and still
  reads 0), d_earlyret_mask/offset (memory_rw.c #95 zeroes the read buffer and the decline is 0) -- and one
  disclosed clause-(e) escape, d_predlen_mask (no row varies width; the decline tests none).
* **The CHANNEL check held**: every row reds under exactly the variants PRETABLE listed for it (KILLS.txt).  The
  seven controls (MC OC XC WC BC UC U1) red only on the null media.
* **Single-row carriers (KILLS.txt), worth knowing for pass 2:** B3 alone catches d_predorlatch_mask/offset (a write
  after a read diverted into the read path) -- B3 is the row added beyond the rulings, so without it those two
  sweep the ruling rows clean; W1 alone catches the clause-(d) operand swaps d_opswap_mask/offset; B1/B2 alone catch
  d_wsetlatch_* and d_backing_*.
* Clone /tmp/gxfbs2: baseline cmp'd against the working copy and the clone before mutant 1 and rebuilt fresh;
  restored from GXEMUL-SEC, cmp clean, rebuilt, binary newer -- only then the sentinel was cleared and the clone
  removed (TABLE.log, last lines).

## Files

PRETABLE_1.out, fbs_variants_1.py (the 40 edits, the predictions, `compare`), dev_footbridge.c.fix1 (baseline),
probe56_frozen.py (instrument, md5 a52267ff), table1_fbs.sh / table1_fbs.run.sh (driver and the frozen copy run),
MD5.txt, VARIANT_MD5.txt (40 distinct sources), TABLE.log, SCORES.txt, COMPARE.txt, KILLS.txt, runs/ (46 probe
outputs + build logs), table1_run.console.

## Owed

Pass 2.  check_probe_wiring.py MANIFEST lines if committed: fbs_variants_1.py (tool), probe56_frozen.py (the frozen
probe a table ran), and impl_20261105/fbsdram_witness.py.  `#NNN` -> the round number at landing.
