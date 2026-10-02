# RESUME.md -- #529 closing pass 8, Opus MEASURING seat.  PAUSED 2026-09-16 ~20:40 at the user's request.
**NO VERDICT HAS BEEN ISSUED.  `OPUS_REPORT.md` IS DELIBERATELY NOT WRITTEN** -- writing one now would freeze a
verdict on four of fourteen measured legs, which is the provisional-adjudication failure this project already names.

## STATE OF THE WORLD AT THE PAUSE

    clone /tmp/gxopusc8            SRC cmp-CLEAN vs GXEMUL-SEC, NO .MUTANT sentinel, binary -nt source.
                                   Baseline NAMED: the #529 working set, md5 8c1d1545eeddd12fd49f52ccede60262
                                   (UNCOMMITTED -- `git status` shows dev_sgi_ip32.c as M).
    binaries  /tmp/gxopusc8_bins/  base + 13 table-A mutants.  **VOLATILE** -- /tmp evaporates.  Everything a
                                   record will cite is already under this artifacts dir; binaries are rebuildable
                                   from `scripts/mutants8.py` + `scripts/mutants8b.py` in seconds each.
    NO PROJECT TREE WAS WRITTEN.   GXEMUL-SEC/, build/, est/ untouched except for this artifacts directory.

## *** BOTH BACKGROUND JOBS WERE **SIGTERM**ed AT ~20:52 (exit 15).  NOTHING IS RUNNING. ***

**THE KILL WAS DELIBERATE, NOT A FAILURE** -- the owner asked for the pause and then for anything still running to
be closed.  `STOPPED.md` in this directory is the coordinator's record of the stop and is the authority on HOW it
was done (a `pkill -f` from a script deliberately not matching its own patterns, verified in a separate
invocation, all eight trees reporting no sentinel / p1 CLEAN / p2 FRESH).  **The two files were written
independently and agree on every material fact** -- 8 valid legs, the same four truncated logs, table B never
started, no verdict.  Read `STOPPED.md` for the stop; read this for the pickup.

Diagnosed here before touching anything, per the carrier's rule that a killed wrapper does not imply killed work:

    KILL8_DONE in logs/table8.out ...... ABSENT -- table A did NOT finish
    kill8 / chain.sh / probe python .... NO PROCESSES ALIVE (the work is dead, not orphaned)
    /tmp/gxopusc8/.MUTANT .............. ABSENT, and the clone SRC cmp's CLEAN vs SEC
    binaries /tmp/gxopusc8_bins ........ base + all 13 table-A mutants still present

**Nothing is owed on the clone.** Table A restored and rebuilt it, and verified `restored == base
(byte-identical)`, BEFORE its probe phase started -- so the kill landed during probing, when no tree was mutated.

### *** FOUR LEGS ARE TRUNCATED AND MUST NOT BE CITED.  The sentinel rule caught exactly the case it exists for. ***

    COMPLETE (195 lines, tail == CRIMEP_DONE):  base, L_dfl4w_hi, L_dfl4w_lo, L_dfl4r_hi, L_dfl4r_lo,
                                                W_rev8r_out, W_rev8w_out, W_rev4w_out          -- 8 legs, VALID
    TRUNCATED (123 lines, NO sentinel):         W_rev4r_out, G_lane_ist, G_lane_tim, G_lane_all -- RE-RUN THESE
    NEVER STARTED:                              D1_landpost, D2_remappost

A truncated leg ends mid-table on an `ok` row and **looks like a healthy partial result**; only `tail -1` tells
them apart.  `scripts/check_pred8.py` is safe here by construction -- it reads the LANE files, and a lane line is
written only after a probe returns -- so it reports all four as NOT RUN rather than scoring a partial log.

### APPARATUS NOTE, worth one line because it is a NEW shape of an old trap
`ps -ef | grep -c "[g]xemul"` returned **1 with no gxemul running**.  The bracket trick stops *grep* matching
itself, but the check was issued as `wsl -- bash -c '...[g]xemul...'`, and `ps` prints that wrapper's whole argv --
which contains the literal pattern.  **The bracket trick does not protect a pattern that appears inside the
command line you are running.**  Read the matched LINES, never the count.

## HOW TO RESTART (binaries survive in /tmp; a rebuild is ~1 s each if /tmp has been cleared)

    # table A, remaining six legs only -- rebuilds them, re-restores and re-verifies the clone
    LIST="W_rev4r_out G_lane_ist G_lane_tim G_lane_all D1_landpost D2_remappost" \
      wsl -d Gentoo -- bash <abs>/scripts/kill8.sh
    # then table B (its own 8 mutants + the three purpose-built probes)
    wsl -d Gentoo -- bash <abs>/scripts/kill8b.run-202251.sh

Run them SERIALLY -- both carry wall-clock oracles (`p t4w/t4r gap`, `time * ctl`, and table B's `c t4*` rows).
Launch each from a FROZEN copy and with `run_in_background`, not a foreground timeout.

## WHAT WAS RUNNING BEFORE THE KILL

* **Table A** -- `scripts/kill8.run-200658.sh`, 14 legs of the SHIPPED 188-row probe in 4 lanes.
  **8 of 14 done as of ~20:52; every one ends `CRIMEP_DONE`, CONTROL=OK, and `check_pred8.py` scores
  PREDICTIONS MATCHED 8, WRONG 0.** Builds finished and the clone was restored+rebuilt+verified BEFORE the probe
  phase began (`logs/table8.out` records `CLONE RESTORED cmp=clean binary-nt-source=yes` and
  `restored == base (byte-identical)`).  Ends with `KILL8_DONE` in `logs/table8.out`.
* **Table B** -- `scripts/chain.sh` was waiting for `KILL8_DONE`, which never came, so **table B NEVER STARTED**
  and `logs2/` holds nothing but `INSTRUMENT.md5`'s directory.  It runs `scripts/kill8b.run-202251.sh` (8 mutants +
  3 purpose-built probes); ends with `KILL8B_DONE`.
  **Table B mutates the clone during its build phase and drops a `.MUTANT` sentinel first.**  If a future run dies
  mid-build, the sentinel will say so; restore with `cp GXEMUL-SEC/src/devices/dev_sgi_ip32.c` into the clone,
  `rm src/devices/dev_sgi_ip32.o`, `make -j4`, then `cmp` + `[ gxemul -nt <src> ]` before clearing it.
  *The chain was a convenience, not a requirement -- on restart just run the two scripts serially by hand.*

## HOW TO PICK UP

1. `cat logs/lane*.out logs2/*.out` -- the raw leg results.
2. `wsl -d Gentoo -- python3 <abs>/scripts/check_pred8.py` -- scores every leg MECHANICALLY against the
   predictions in `PREDICT.md` / `PREDICT2.md`, both of which were written BEFORE any build (mtimes prove it:
   PREDICT.md 20:04:24, first build log 20:07:03).  It reports a prediction error AS a prediction error.
3. Verify each preserved leg by its sentinel, not its existence: `tail -1 logs/probe_<m>.raw` must be
   `CRIMEP_DONE` (and `CTL4R_DONE` / `T4CLEAR_DONE` / `CTLRESET_DONE` for the three small probes).
4. Then write `OPUS_REPORT.md` -- verdict line first, with the denominator.

## WHAT IS ALREADY SETTLED (measured or derived; none of it depends on the pending legs)

### A. The enumeration's FOUR axes are not the handler's SIX.  `DERIVATION.md` §1, derived from `:193-421`.
The accept path also partitions on **`relative_addr & 4`** (the LANE, tested at `:282` AND `:291`, inside the
`len == 4` arm) and on **`cpu->pc`** (the PROM window, `:344`).  Neither is named as an axis anywhere in the
enumeration, PRETABLE 11, POSTTABLE 11 or the probe header.

### B. The LANE is covered IN EFFECT, so (A) is a records defect and not a breach -- ALL FOUR MEASURED, all killed.
At the six named labels the lane is **unsatisfiable** (REV 0x00 ... TIME 0x38 are all 8-aligned).  At the default
arm both lanes are driven post-latch with an oracle each, and every lane-split mutant dies on the rows I named:
`L_dfl4w_hi` 185/188 (`top4 w`, `p acc 40 lw`, `p acc 40 sw`), `L_dfl4w_lo` 185/188 (`top4 w`, `p dog wlo`,
`p dog whi`), `L_dfl4r_hi` 186/188 (`top4 rhi`, `p acc 40 lw`), `L_dfl4r_lo` 185/188 (`top4 rlo`, `p rev lw4`,
`p dog rlo`).  **The lane axis is not a floor gap.**

### B2. The PC-WINDOW axis is covered too, and its negative controls are CONTROLLED rather than merely clean.
`W_rev8r_out` (REV 8R narrowed to pc OUTSIDE the PROM window, latch set) scores **187/188, reddening `p rev ld`
ONLY** -- not `p revP ld pc`.  That is the positive control: the out-of-window predicate is satisfiable and
observable.  With it in hand, `W_rev8w_out` and `W_rev4w_out` at **188/188** are genuine EQUIVALENCE (the prelude
rewrites reg[0] at `:229` before any read can see the store), not vacuity.  `W_rev4r_out` pending.
*This is the clause-(c) identity-row discipline applied to my own negative controls, and it is why the W group
proves something: three clean sweeps with no positive control would have proved nothing at all.*

### C. *** THE LATCH-CLEAR HALF OF THE PRODUCT WAS NEVER CLOSED.  This is the finding of the pass. ***
`scripts/preclear8.py`, `scripts/sessrows.py`, `scripts/buckets8.py` -- **8 of the 46 ACCEPTS entries are driven in
the latch-CLEAR state by session 40 (`latch x5`) ALONE**, and `latch x5` carries exactly three rows: `latch x5`
and `latch said` (announce COUNTS/TEXT) and `latch surv` (a RAM round trip).  **A silent `goto crime_declined` in
that prologue moves none of them** -- it prints nothing, it does not set the latch, and the host stays alive.

At CELL granularity the open set is:

| cell | status |
|---|---|
| **INTSTAT 4R** | **GUEST-VISIBLE** -- skips `crime_interrupt_reassert()` |
| **TIME 4W** | **GUEST-VISIBLE** -- skips `crime_update_crime_time()`; close-7's E2 measured this cell visible with NO refusal in the sequence |
| **TIME 4R** | **GUEST-VISIBLE** -- same channel |
| CONTROL 4R | EQUIVALENT (the prelude writes 0x100 at `:231`; the high lane is 0) |
| REV 8W / 4W / 4R out of window | EQUIVALENT (the prelude rewrites reg[0] at `:229`) |
| INTMASK 4R | driven by session 20 too; `gate line` depends on that `lw +0x18` reasserting (`:723`, `:736`) -- predicted KILLED, pending |

The 8-byte column is fully covered (every 8-byte-at-a-label cell has a second driving session with a value oracle
-- `scripts/sessrows8.py`), so the hole is exactly the 4-byte column and exactly four of its twelve cells.

**This is the K-class's own argument with CLEAR and SET exchanged**, and the contract's amended clause -- *"CAUGHT
... AND THE CATCHING ROW RUNS IN THE BYPASS'S OWN LATCH STATE"* -- fails for these cells by its own words.
The glm seat named ONE member (TIME); the class has four.  **Mutants built and queued in table B:**
`G_glm_tim4clear`, `G_clr_ist4r`, `G_clr_ctl4r` (the class's own negative control), `G_clr_imk4r`.
The owed row is built and queued too: `scripts/t4clear.py`, the GAPPED shape MINUS the opening refused `lb`.

### D. A SECOND, INDEPENDENT hole on the latch-SET side -- the codex seat's cell, and it is a GENERATING-SET breach.
The 2026-09-04 clause: *"at each floor cell, every idata bit the guarded body TESTS is written both clear and
set."*  The CONTROL arm tests DOG 0x200, HARD_RESET 0x800 and the leftover.  Derived from `scripts/cellmap8b.py`:
every post-latch CONTROL write in the 188-row probe carries **HARD_RESET CLEAR** (0x01, 0x0001, 0x0201, and
session 26's ACCEPTS values), and the only 0x800 write -- `sw08 halts`, session #2 -- is PRE-latch.
Mutants queued: `K_ctl4w_reset_post`, `K_ctl8w_reset_post`.  Owed row built: `scripts/ctlreset.py`.

### E. `C_ctl4r`'s 188/188 leg IS vacuous -- confirmed independently, with the reason corrected.
`scripts/cellmap8.py` puts `CTL 4R lane=0` post-latch in **session 26 only** (`rearm once`), which has no value
oracle.  So the leg tested nothing.  **Precision note: the relayed claim "there is no 4-byte READ at CRIME_CONTROL
post-latch at all" is wrong in detail** -- ACCEPTS entry 8 is `("lw", 0x08, 0)` and session 26 runs it.  The right
statement is *driven once, by the one session that cannot observe it*.  Whether the cell is nevertheless
EQUIVALENT is queued (`scripts/ctl4r.py`, base vs `C_ctl4r` vs the `G_lane_ctl` liveness control).

### F. Records findings, both checked rather than argued.
* **PRETABLE 11 line 82 says the predictions were "transcribed into check_pred.py BEFORE the run, compared
  after".  `killtable11_20260916/` HAS NO `check_pred.py`** -- tables 4,5,6,7,8,9,10 each have one.  So table 11's
  predictions were compared BY EYE, which is exactly the condition under which its second prediction error (the
  "four negative controls" line, one materialised) survived until the grok seat found it on this pass.
  *A missing mechanical checker is a structural finding, not a citation nit.*
* **The P6 register-collision audit is DISCHARGED, mechanically and for the whole probe**
  (`scripts/regcollide8.py`): across all 51 sessions, **zero** printed registers are written by more than one
  load, so no row can read another row's value.  The repair-13 comment's own checklist named the wrong register
  (`t2` vs `ra`) and covered one session; this answers it for every register in every session.

## WHAT THE PENDING LEGS DECIDE

Table A still owes SIX: `W_rev4r_out`, `G_lane_ist`, `G_lane_tim`, `G_lane_all`, `D1_landpost`, `D2_remappost`.
Table B owes all eight.  The verdict hinges on table B: if `G_glm_tim4clear` / `G_clr_ist4r` /
`K_ctl*w_reset_post` score 188/188 as predicted, the verdict is **GAP** with those exact edits; if they are
killed, the enumeration closes on those axes too and the verdict is **CLOSES** with the denominator in
`DERIVATION.md`.
