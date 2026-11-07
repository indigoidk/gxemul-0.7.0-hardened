# `regress/artifacts/ghostround/wired_20261106/` -- the controls of precommit section P2 as wired (`#587`, ledger `ghostround`)

Banked by the `#587` landing.  The census, the replay of 141 landing commits and the prototype's 35 controls are in `../census_20261106/` (`DECISION.md` first); this directory holds what the WIRED section added, rebuilt after the pass-2 review (`PASS2_RULING.md`), again after the repair's own pass 2 (`REPAIR_RULING.md`), and again after the closing pass (`CLOSE_RULING.md`) and its repair's pass (`PASS4_RULING.md`), records only.

| file | what it is |
|---|---|
| `P2_GREEN.out` | the full `tools/precommit_check.sh`, run as the hook runs it (no message argument, no `GX*` overrides), in a scratch clone: the real HEAD, the clone-only stand-ins below, and the unit staged |
| `P2_RED.out` | the same tree with one more staged round block, `SYNTHETIC_BLOCK.md` (`#588`, dated `2026-11-06`), naming the open row `codeqlscope`: its record does not name `#588`, and it carries an entry dated `2026-11-06`, so only the mention rule fails it |
| `SYNTHETIC_BLOCK.md` | that block, verbatim; it existed only in the clone |
| `CHECKER_CONTROLS.out` | `run_checker_controls.sh` on the clone-built checker and hook (rc 0): legs 1-7 the census's 35 controls and leg 4's `c4d` (an --at blame git cannot do), legs 8 the index-mode controls and both reviews' (a staged dated block, a temporary index, an unreadable index, an impossible blame, a blame that dates none of the lines -- a SHA-256 repository, `c8j` and `c8k`), leg 9 section P2's own block cut from the hook and run as the hook runs it, by a harness that counts `fail` under `set -u` (`c9a`-`c9e`); and `c8l`, `c8m` (one read absent from the index) |
| `run_checker_controls.sh`, `synth/` | that driver and its fixtures (`synth_ledger.json`: the census's synthetic ledger, plus a `held` row and a row whose only round number is in an entry dated before the round) |
| `MUTANTS.out`, `run_mutants.sh` | every single-edit mutant the three reviews traced (and the code before the first repair), each run against the controls: which legs went BAD, and whether the leg built for it did |
| `MUTANTS_NEGCTL.out` | the driver's negative control: a mutant whose text is in no checker, over a stale copy left as an earlier run would leave it -- NOT BUILT, and the run exits nonzero |
| `EQUIV.out`, `run_equiv.sh` | the installed checker against the census prototype on four measured commits x three cutoffs x six option sets, outputs compared minus the line naming what was read |
| `HEADER_REDATE.out`, `run_header_redate.sh` | the hazard the review measured: an edited header line of an archived block blames to the all-zero sha |
| `PASS2_RULING.md` | the pass-2 ruling (Fable 5.1, VERDICT HOLD, 57 accepted, 8 rejected), verbatim from `_scratchpad/fable_20261106/ghost/RULING.md` (md5 `25a4f478`); this unit is its repair |
| `REPAIR_RULING.md` | the ruling on the repair's own pass 2 (Fable 5.1, VERDICT HOLD, 24 accepted, 5 amended, 1 rejected), verbatim from `_scratchpad/fable_20261107/ghostrepair/RULING.md` (md5 `37feaec3`): the class closure this bank measures |
| `CLOSE_RULING.md` | the ruling on the class closure's own pass (Fable 5.1, VERDICT HOLD, 15 accepted, 2 amended, 1 rejected), verbatim from `_scratchpad/fable_20261107/ghostclose/RULING.md` (md5 `4ed4fe352cc68978f66dd2a09c46adb0`): the index guard's two reads, rowed as one cell, and the two legs and two mutants that close the product -- the correction of `REPAIR_RULING.md`, which is banked and dated and not edited |
| `PASS4_RULING.md` | the ruling on the repair's pass, Fable 5.1, VERDICT LAND, 18 accepted, 5 amended, 0 rejected: the nonempty-short blame slice is clause (e), disclosed; one record corrected |
| `pretest_ghost.py.txt` | the pretest driver as this run executed it (md5 `edab4923aaac2a1709ea1d1f4f59e69f`, read at the run's START); `.txt` because a `.py` under `regress/artifacts/` needs a section-R class |

## The clone

* the real HEAD: `8d9df65844c43c689be81218c7a34cc8de67ff83`.
* S1 skipped: the real HEAD already carried the 2026-11-06 records commit (`../census_20261106/`).
* S2 skipped: the real HEAD's probe-wiring EXEMPT table no longer dated `wdc_altoffset_probe.py` 2026-11-05.
* the real working tree's other dirty tracked files overlaid unstaged (16), the spec's neutral files left at the clone's HEAD (neutral: `regress/gate_arm.sh`, `regress/gate_sh_rounding.sh`, `regress/gate_offline.sh`, `regress/gdrom_default_probe.py`); the untracked files copied in.
* the unit staged: 9 files, built by `build_ghost.py` on the clone's HEAD (md5s below).  This directory was not part of that unit: a directory cannot hold the output of the run that stages it.

## The builds before this one

The unit the repair's pass 2 reviewed was banked on 2026-11-06 in a clone whose base had a lower highest round (`#586`, dated `2026-11-06`) and finalized on 2026-11-07 for the landing `#587`.  Its date and round are FILLS, so each was compared by an exact token replacement of that fill alone, the differing lines counted before and after: the today-dated rebuild against the unit GREEN tested, 8 -> 0 (`CHANGELOG.md` 1 -> 0; `OUTSTANDING_BUGS.md` 2 -> 0; `tools/pipeline/ledger.json` 4 -> 0; `tools/pipeline/matrix.html` 1 -> 0); the checker and section P2's hook block filled with `#587` against the measured ones, the checker 1 -> 0 and section P2's block of the hook 1 -> 0; the rebuild with the date pinned, 9 files identical and 0 differing.  That build's FINAL run passed; this bank replaces it (the class closure, `REPAIR_RULING.md`).

The unit the closing pass reviewed (the class closure) was banked and finalized on 2026-11-07 (`#587`, dated `2026-11-07`): the today-dated rebuild against the unit GREEN tested 0 -> 0 differing lines, the rebuild with the date pinned 9 files identical and 0 differing; its FINAL run: rc=0, `PRECOMMIT_PASS   0 hard`.  This bank replaces it (`CLOSE_RULING.md`).

## What happened between the banked runs and the landing

Nothing moved: the banked runs and `finalize.py` ran on 2026-11-07, on the unit `#587` dated `2026-11-07` -- the round and the date the landing takes.  The fill comparisons are recorded anyway (`CALENDAR.json` in the kit): the today-dated rebuild against the unit GREEN tested, 0 -> 0 differing lines; the checker and section P2's hook block filled with `#587` as the builder fills them (`fill_parts.py`) against the measured ones, the checker 0 -> 0 and section P2's block of the hook 0 -> 0; the rebuild with the date pinned (`build_ghost.py --date`), 9 files identical, 0 differ, 0 missing, only this directory added (30 files).  The FINAL run tests the unit as it lands, on the real HEAD; `after_final.py` refuses unless its checker and block are these bytes: the checker md5 `f20d249eeb217276606d35396c76f1c8`; section P2's block of the hook md5 `9e234aa865863876b7d75910dc03799b`.

## Results, verbatim

GREEN -- `PRECOMMIT_PASS   0 hard, 6 soft`:
```
P2. a round block's subject and in-work rows record the round
  ok    GHOST_ROUNDS_PASS  13 archived (landed on/before 2026-11-05), 0 new
```

RED -- `PRECOMMIT_FAIL   1 hard, 6 soft`:
```
P2. a round block's subject and in-work rows record the round
  FAIL  A ROUND BLOCK'S ROWS DO NOT RECORD THE ROUND:
            GHOST    codeqlscope            open     named in the header of #588 (round 2026-11-06, landed 2026-11-07, line 1) -- no mention of #588
          GHOST_ROUNDS_FAIL  1 row(s) named by a round block that landed after 2026-11-05 carry no write-back
          fix: close the row, or name the round (#NNN) in its state_note or an entry
```

Hard lines only in RED: 1.  Only in GREEN: 0.  Hard lines in GREEN: 0.
```
only in RED:   FAIL  A ROUND BLOCK'S ROWS DO NOT RECORD THE ROUND:
```

The controls: `CONTROLS: 69 ok, 0 BAD`.  The mutants: `MUTANTS: 16 mutants, 16 killed by their own leg, 0 escaped`.  The equivalence: `EQUIV: 72 comparisons, 0 DIFFERENT`.

## md5

The unit as staged in the clone:
```
7923d8e5c9827eeec75e2b8cc66a43ac  CHANGELOG.md
fe50f6a2ace3e3c64f3027309bde4268  OUTSTANDING_BUGS.md
5cfaaa506027ec42233a9580cf26a03e  tools/README.md
f20d249eeb217276606d35396c76f1c8  tools/pipeline/check_ghost_rounds.py
eecec635b03426e76d2d3873f74e6820  tools/pipeline/check_probe_wiring.py
307f050c71e9a0709f7b8753df804727  tools/pipeline/fable_queue.md
62094713d19721d0a12d26a8ca03933c  tools/pipeline/ledger.json
9a2706b0e069bce5d56941a58348d7a5  tools/pipeline/matrix.html
b678efd6e3151b5c03a97bc9c7eb5a05  tools/precommit_check.sh
```
The landing build re-derives the unit on the landing HEAD.  The checker is byte-identical whenever the round number is the same (the round and this directory's name are its only fills); every other file is that HEAD's copy plus this unit's edits, filled with the round and the date of the build, so its md5 follows that HEAD and that day.

This directory:
```
225f7b48ed62349a1d02e7fb093e413b     5470  CHECKER_CONTROLS.out
4ed4fe352cc68978f66dd2a09c46adb0    27455  CLOSE_RULING.md
3f42b66763420ecaf143cd92ba6e8fa2     6797  EQUIV.out
b3448235c61f476bb7b19eeff1a7ab99      537  HEADER_REDATE.out
88a8c9362770d6fa30e71b65a7658dc2     4917  MUTANTS.out
d241c0df46fe833eb28971e3aa26d0f2      302  MUTANTS_NEGCTL.out
70c5491fac221c21e24671f993d7ece1    12026  P2_GREEN.out
b9a87e487c063f679e56c233787582b1    12289  P2_RED.out
25a4f4780a852e34bc00a929c0b24fe2    22276  PASS2_RULING.md
595a268f7258f4816cddb5d5231de865    28731  PASS4_RULING.md
37feaec30c8e836a4ce0cbc469dfcabc    23107  REPAIR_RULING.md
633abd07629e78b20a3b2e4e277c0770      402  SYNTHETIC_BLOCK.md
edab4923aaac2a1709ea1d1f4f59e69f    32717  pretest_ghost.py.txt
14c229af13dbf94f551249bfe8151f3d    27864  run_checker_controls.sh
76ee6265a62ca5cada821c4530e3418c     1412  run_equiv.sh
49a0be146177a160fe3334514b916736     1606  run_header_redate.sh
3131adb1817d5b6e9a6400cf1e8e480b     8773  run_mutants.sh
080283b10dad089fe0fcfed6070c9cdf      142  synth/c1a_open.md
ceff00b05b6393d3e84e1ef13c408150      139  synth/c1b_sameday.md
7f695325a2127585a9d5b2f1520dfec1      185  synth/c1c_claimed.md
2ce8e66614f6454499e7a43e015d3f05      189  synth/c1d_held.md
9ed402a05803fa3583891a7b185b7124      205  synth/c1e_prior.md
4f92ec891c3ea70f5d385e1c7c701eca      143  synth/c2a_closed.md
5d76e7615212fd784cd71b861f49aa8c      150  synth/c2b_recorded.md
bd08379fa25992a3cb23b32850fbc6a4      187  synth/c2c_reference.md
d41d8cd98f00b204e9800998ecf8427e        0  synth/c3a_empty.md   (EMPTY ON PURPOSE: the empty-CHANGELOG control's input)
53d718cda21c42696eb62b332ed7559e       65  synth/c3c_records_only.md
6ff686fe7e740abfb4410d0a2d7c1504     1776  synth/synth_ledger.json
7f5b28f957010af4d3cdfaebd7eb09b4       12  synth/synth_ledger_norows.json
```
