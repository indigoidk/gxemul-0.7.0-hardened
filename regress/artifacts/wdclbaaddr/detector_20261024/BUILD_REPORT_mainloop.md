# `#572` (wdclbaaddr) -- BUILD REPORT, written 2026-10-24 21:2x by the main loop (087a90) FROM THE ARTIFACTS in this directory
# (the builder sub-agent produced every artifact below and then went idle without writing its report; nothing here is asserted
# that a named file does not show).

## 1. The product edit

`src/devices/dev_wdc.c` (working tree; `git diff HEAD -- src/devices/dev_wdc.c` is the pass-2 packet's section 2): five `#572`
sites -- the SDH arm's decode (`lba` from bit 6, the reserved bits 7/5 kept in the field renamed `sectorsize` -> `sdh_resv`, drive
bit 4, head bits 3-0) and its byte-exact readback composition, the LBA28 arm in `wdc__read()` and in `wdc__write()` (each
`512 * (int64_t)(((d->head & 0xf) << 24) + (cyl << 8) + d->sector)`, the old `printf` gone), the word-49 comment.  `grep -c '#572'`
= 5; `grep -c sectorsize` = 0.  The twin `est/src/devices/dev_wdc.c` is byte-identical (checked at packet time; the landing script
re-checks).  Fix clone `/tmp/gxt2/fix` built from it (`make_fix.log`); every table's `final:` line records the fix tree `cmp CLEAN vs
SEC`.

## 2. The detector

`regress/wdc_lba_probe.py`: 827 lines, md5 `5e4ecd477c2a4acbcb79d4382ffa4183` at pass-2 packet time; **the SHIPPED bytes are
revision `96e5fbc5817ab26e19edd4f5335a184f`, 840 lines, 35,862 bytes (21:4x, after pass 2: the module docstring's BLIND list
extended -- head nibble 2..15, sector counts 0 and above 1, the joint cells of the address fields; a NOTE on the applicator's
V14r/V14w suffix convention; V17v added to CATCHES; the "every want is a literal" sentence corrected).  Docstring-only over
5e4ecd47: `final_96e5fbc5/ast_equivalence.txt` shows its AST with the module docstring excluded differs from the kill-table
instrument only in the `id geo` predicate and that function's docstring legend -- the same change `rev_equivalence.txt` recorded
for 5e4ecd47 (whose bytes were not preserved; the equivalence is transitive through the instrument).  Its own runs:
`final_96e5fbc5/RESULTS_gate.txt` GATE vs FIX 33/33 CONTROL=OK and `RESULTS_twoleg.txt` base 33/33 vs HEAD / fix 33/33 vs FIX
(21:44-21:50; `RUN_IDENTITY.txt`).**  Seven debugger-driven guest
sessions on the unmodified `evbmips -e malta` with the tagged 4096-sector image (`identify`, `chs`, `sdh`, `lba`, `lba0`, `lbah1`,
`lbawr`), 33 scored rows = 7 ram-liveness + 2 IDENTIFY + 4 CHS + 4 SDH readbacks + 4 LBA reads + 1 LBA-0 + 2 head-1 + 9 write-session
rows (the derivation is in `HUNKS_gate_sh_rounding.sh.diff`'s pin comment).  Modes: `<bin> - <outdir>` (witness), `<base> <fix>
<outdir>` (two legs), `<bin> GATE <outdir>` (one leg vs the FIX column; `WDC_LBA_RESULT=p/n`, `WDC_LBA_CONTROL=OK|FAIL`, sentinel
`WDCLBA_PROBE_DONE`).  `None` observations and wants fail their row; the constant `neg appar` row is out of the score (a startup
comparator self-check replaces it); the pty driver survives a dead child and still prints the result lines and the sentinel
(`dead_run.out`).

Revisions: the kill-table instrument is `wdc_lba_probe.frozen.py` here, md5 `fc878c423319892979271d87b47666b8` (frozen before table
1); the shipped `5e4ecd47` differs from it in ONE row's predicate -- `id geo` now requires `S >= 10` (mode `geo`) instead of `S != 0`
(mode `nz`), 8 executable lines (`rev_equivalence.txt` (a)); every one of the 41 preserved run logs read `(16, 63)` for that row
except the dead run's `(None, None)`, so both predicates return the same verdict on every preserved observation and the table scores
transfer row for row (`rev_equivalence.txt` (b), "VERDICT: scores transfer row-for-row").  The shipped bytes additionally carry
their OWN measurements: GATE 33/33 CONTROL=OK (`final_5e4ecd47/RESULTS_gate.txt`, 20:53) and the two-leg base 33/33 vs HEAD /
fix 33/33 vs FIX (`final_5e4ecd47/RESULTS_twoleg.txt`, 21:19-21:23, run by the main loop from a frozen copy).  Intermediate
revisions `b0c7498c` and `d9b93abe` have their own GATE + two-leg results under `final_<md5>/`.

## 3. Measurements (every number from the named file)

* Witness instrument (`../witness_20261024/wdc_lba_probe.frozen.py`, md5 8f3632ff): base leg 19/19 vs HEAD, 17:03, BEFORE any edit
  (`RESULTS_base.txt`); the frozen instrument's two-leg run dated 19:02:13 (`RESULTS_fix.txt`; `twoleg/RESULTS.txt`, dated
  19:04:46, is the REVISED detector's run, a different file): fix leg 19/19 CONTROL=PASS vs FIX -- the `probe:` term's two
  halves on the SAME script.
* Revised detector two-leg: base 33/33 vs HEAD, fix 33/33 vs FIX (`twoleg/RESULTS.txt`; also `final_b0c7498c/`, `final_d9b93abe/`,
  `final_5e4ecd47/RESULTS_twoleg.txt`).
* GATE mode on the fix binary: 33/33 CONTROL=OK (`gate/RESULTS.txt`; `final_*/RESULTS_gate.txt`).
* Dead run (`/bin/false` as the binary, GATE mode): `WDC_LBA_RESULT=0/33`, `WDC_LBA_CONTROL=FAIL`, sentinel present (`dead_run.out`,
  19:11-19:25) -- clause (c): measured at `detector_20261024/dead_run.out`.
* `PRETABLE.out` (19:01, before table 1): sibling parity, claim->row, guard field vs body field with the body-induced partition,
  CHANNEL per scored row.
* Kill table 1 (`SCORES.txt`, 19:25-20:05, instrument fc878c42, GATE mode vs the FIX column, baseline 33/33 OK): 18/18 KILLED, no
  escape -- V1 17/33, V2 17/33, V3 31/33, V4r 32/33, V4w 32/33, V5w 31/33, V6w 31/33, V8 32/33, V11 29/33, V13r 19/33, V13w 31/33,
  V14r 28/33, V14w 28/33, V15 32/33 (the unwidened product: killed on THIS gcc -O3 build by the head-1 row; undefined in general,
  recorded as a measurement that does not generalise), V16 31/33, V17 31/33, V18 31/33, V20 28/33.
* Kill table 2, contract claims at both sites (`SCORES2.txt`, 20:06-20:3x): 9/9 KILLED -- V5r 32/33, V6r 31/33, V8w 32/33, V11w
  30/33, V9r8 (head shift by 8, lands in the file) 32/33, V10r 32/33 and V10w 32/33 (the cylinder-low-only arms, killed by the two
  high-cylinder rows), T_m1 26/33 and T_p1 26/33 (the +-1 translations; the shipped rows see more than the witness's four).
* Single builds (`SCORES_V12_V7.txt`, 20:45-20:51): V12 (`& 0xf` dropped) 33/33 SURVIVED -- EQUIVALENT, as expected (one masked
  writer of `d->head`); V7 (the cylinder-high-conditioned arm) 33/33 SURVIVED -- the disclosed BLIND cell on this image.
* Single build after pass 2 (`SCORES_V17v.txt`, 21:3x; Astra's K2 -- clause (b) at the readback site): V17v, the VERBATIM
  pre-#572 readback composition `(sdh_resv << 6) + (lba << 5) + (drive << 4) + head` over the new decode, 30/33 CONTROL=FAIL
  -> KILLED by the three readback rows (`raw_mut/V17v.out`).
* Applicators: `mutants572.py` (final), `mutants572_table1.py.txt`, `mutants572_table2.py.txt`; per-mutant logs `raw_mut/*.out`.
* Gate 2's offline harness `regress/diff_wdc_identify.c` built WITH this round's hunk against the fixed model: 128 rows, 0 failures,
  `WDC_IDENTIFY_PASS` (`offline_identify_hunk.out`).

## 4. The hunks for the four files the landing stages from HEAD-based copies

`HUNKS_gate_sh_rounding.sh.diff` (+52: the gate-10 block, denominator pinned to 33 with its derivation, CONTROL=OK, sentinel),
`HUNKS_check_probe_wiring.py.diff` (+25 as of 20:35 -- a historical figure; +31 in the 21:4x regeneration with corrected
description strings, re-regenerated 01:2x so the instrument's blurb names the dead run's (None, None) reading as the one
exception both predicates reject, and 01:3x at +33 so the applicator's blurb says V17v was applied by the separate script
`run_v17v.sh.txt`, not by `mutants572.py`; `HUNKS_APPLY_RECEIPT.txt` records each hunk's dry-apply, CR count and syntax check:
`wdc_lba_probe.py`
CLASS_DETECTOR, the witness frozen copy CLASS_WITNESS, this directory's frozen instrument and applicator CLASS_TOOL), `HUNKS_diff_wdc_identify.c.diff` (+4 net: the `row_no_lba_claim()` comment and FAIL
text re-authored; assertion, name and "ok" string unchanged), `HUNKS_gate_offline.sh.diff` (one comment line).  All four dry-applied
cleanly to HEAD's copies by the main loop at 19:4x (the later 20:35 revisions of the first two re-checked at landing).

## 5. Not done / caveats

* The builder's own six-line report was not delivered; this file stands in, from the artifacts only.
* The gate-10 SCRIPT with the block in place was run end to end AFTER pass 2 (its seats asked for it): HEAD's
  `gate_sh_rounding.sh` + this round's hunk (an LF copy, md5 3f932e0f), `PMAX` = the fix clone's binary (provenance measured in
  `../pass2_20261024/CLONE_PROVENANCE.txt`: 496 of 505 tracked src files identical to HEAD plus this round's `dev_wdc.c`; the
  PowerPC decoder at its pre-#571 revision and the pmax layout's six declared divergence paths, none on the wdc path), no build
  tree touched
  -- the block's five checks OK, 33/33 CONTROL=OK, sentinel once; the gate's own verdict FAIL 1 of 405 on the peer session's
  uncommitted 62-row `gdrom_default_probe.py` against HEAD's 60 pin, not this round's file
  (`../pass2_20261024/GATE10_RUN.txt`, 2026-10-24 23:24 -> 2026-10-25 00:57; `gate10_wdc_lba.log`).  The first attempt died in
  2 s on a CRLF copy written by `git apply` outside the repo (system `core.autocrlf=true`); the landing script now refuses that.
