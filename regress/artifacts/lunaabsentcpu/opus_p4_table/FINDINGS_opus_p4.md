# Opus 5 seat -- #503 `lunaabsentcpu` pass 4.  MEASURED, not read.

Clone `/tmp/gxopusluna_p4` (`cp -a` of `build/`, `cmp`-clean vs SEC before the copy); baseline re-derived from SEC +
`fix_lunaabs.py` and `cmp`-IDENTICAL to `killtable4/baseline_dev_luna88k.c` (md5 245dffb7); driver run from a frozen
copy `killtable_opus_p4.run-143413.sh`; sentinel per mutant, cleared only after `cmp` + rebuild.  No project tree
written.  Predictions in `PRETABLE_opus_p4.out`, mtime 14:32:55, BEFORE the 14:34:13 start.
CONTENTION NOTE: the main loop's `killtable5` ran concurrently in `/tmp/gxlunaabs_kill` from ~14:33.  Separate clones,
but both instruments carry 15 s wall-clock oracles -- read any UNEXPECTED `STOP` in either table with that in mind.

## The instrument is NOT the one the brief describes
`_scratchpad/lunaabs/luna_absentcpu_probe.py` was edited at **14:31:06** (session E2 added; md5 3fd0198f -> 3be01e9d,
34 rows -> 37).  The brief (12:21) describes the 34-row v5.  Row sets nest exactly: v6 = v5's 34 + `cpu3 deliver23`,
`cpu2 deliver23`, `others idle23`, with no v5 row dropped (verified by `comm`).

## Table A -- v6 instrument (37 rows), BASE 37/37 PASS
| mutant | score | reds |
|---|---|---|
| M_ENP1  `interrupt_enable[cpu & 1]` + `software_interrupt_status[cpu & 1]` | **35/37 FAIL** | `cpu3 deliver23`, `cpu2 deliver23` -- BOTH new in v6 |
| M_ENP1E `interrupt_enable[cpu & 1]` alone | **35/37 FAIL** | the same two |
| M_EXIT8 `ncpus > 4` -> `> 8` at DEVINIT | **37/37 PASS** | none -- see the equivalence below |
| M_SWEQ1 `software_interrupt_status[cpu] == 1` | **37/37 PASS** | ESCAPES -- clause-(e) DEBT, see below |

**Therefore M_ENP1 is 34/34 on the SHIPPED v5** -- every v5 row is green and the only reds are rows v5 did not have.
kimi's and grok's prediction is CORRECT.  It is a clause-(d) operand swap on a body-read lvalue, a TOTAL escape, and
so a FLOOR BREACH of the composite the brief asks about.  The repair already in the working probe (session E2) KILLS
it: measured, and it kills the ENABLE-only half too, so the repair covers the class rather than the instance.

## M_EXIT8 is an EQUIVALENT MUTANT, and it makes a claim in the SHIPPED FIX COMMENT false
The fix comment says: *"(delete that exit and a 5-cpu machine would walk cpu_irq[4])"*.  Built and run:

    baseline, -n 5:  rc=1, "LUNA 88K can't have more than 4 CPUs."          <- dev_luna88k.c's exit
    M_EXIT8,  -n 5:  rc=1, "More than 4 CPUs is not supported for LUNA 88K." <- machine_luna88k.c:103-106

`src/machines/machine_luna88k.c` carries a **second `ncpus > 4` exit**.  `MACHINE_SETUP(luna88k)` does
`device_add(machine, "luna88k")` at `:54` and the guard at `:103`, so DEVINIT runs first and the device's exit is
load-bearing at the capture -- but if it is relaxed the machine layer exits before any guest instruction runs, so the
walk is never reached with `ncpus > 4`.  No reachable command line distinguishes the two builds: `-n` parses 1..256
(`main.c` `parse_int_option('n', optarg, 1, 256)`), and every value > 4 is refused by one guard or the other.
Record it as EQUIVALENT WITH ITS WARRANT, alongside M_NULLAB.  **The warrant expires if the device is ever
instantiated outside `machine_luna88k.c`** (a config-file `device()` line), which is the only route that skips `:103`.

Consequences for the records, both L4:
* the parenthetical above is FALSE and is in PRODUCT CODE.  Correct it in place (e.g. *"...the machine layer carries
  the same test at machine_luna88k.c:103, after the device_add at :54, so this exit is the first of two"*).
* CHANGELOG (draft line 18) records kimi's and grok's pass-3 refutation of the pass-2 comment -- *"delete the exit and
  `-n 256` walks past the 4-entry arrays"* -- as accepted.  **That refutation is measured FALSE.**  Both seats read
  only the device file.  The pass-2 wording it displaced (*"<= MAX_CPUS by construction, not by that exit"*) was
  closer to right than the wording that replaced it.

## The `others idle` deletion cost a measured kill
M_AND1 scored **29/32 on v4** (`cpu3 deliver` STOP, `cpu2 deliver` STOP, `others idle` BADREGS) and **32/34 on v5**
(two reds).  I ALSO derived that v4's E would have killed M_IRQACTIVEP1 by itself, making the rewrite unnecessary.
**TABLE B MEASURED THAT DERIVATION FALSE** -- and the correction is the better finding.

    instrument   M_ENP1 (READ alias)      M_IRQACTIVEP1 (WRITE alias)
    v4 (32)      30/32 FAIL  <- KILLS     32/32 PASS  <- escapes
    v5 (34)      34/34 PASS  <- escapes   32/34 FAIL  <- KILLS
    v6 (37)      35/37 FAIL  <- KILLS     (both sessions present)

My arithmetic error: I wrote that slots 2 and 3 "share latch index 1".  They do not -- `2 & 1 == 0` and `3 & 1 == 1`,
so slots 2 and 3 are in DIFFERENT parity classes (the pairs are {0,2} and {1,3}, as the probe's own docstring says).
In v4's E, with only 2 and 3 pending, the latch collision never occurs and M_IRQACTIVEP1 escapes; in v5's E, with all
four pending, both same-parity pairs collide and it dies.

**So the two configurations are COMPLEMENTARY and NEITHER DOMINATES.** v4's E has idle alias TARGETS, which is what a
READ alias needs to be visible; v5's E has same-parity pairs both pending, which is what a WRITE alias needs.  The
pass-3 disposition is wrong not because the rewrite was unnecessary but because it was made as a **REPLACEMENT of a
session that was killing something**, when the right move was to ADD one -- which is what v6 does.

> **The cheap guard, and it is the one this round did not have: when a session's STATE is CHANGED rather than added
> to, ask what the OLD state discriminated that the new one does not.** Table 4 correctly re-ran the previously
> killed mutants, and they stayed killed -- but M_ENP1 did not exist yet, so nothing measured what the deleted
> configuration had been buying.  The deletion of `others idle` was the visible symptom and it was not investigated.

## Also checked
* premise 5's warrant (M_NULLAB): `INTERRUPT_CONNECT` cannot leave a slot silently unconnected --
  `interrupt_handler_lookup` `abort()`s on an unknown name -- BUT an EMPTY name fills the template with
  `no_interrupt_assert`/`no_interrupt_deassert`, which are NON-NULL.  So "has a callback" and "slot < ncpus" are not
  the same predicate in the mechanism; they are the same in THIS device only because slots 1..3 are connected with
  literal non-empty names.  Add that clause and the warrant is complete.
* the comment's other claims all hold: the capture is below the exit; the walk and the per-count connects ARE the
  0.7.0 import (pristine copy at the project root has the same walk and the same exit); the mask/soft registers do
  stay guest-writable.  One INCOMPLETENESS: it names `interrupt_assert` only, while the round's own W1 row records
  that three mutants die on the READBACK, i.e. the DEASSERT side.
* no gate or probe anywhere in `regress/` runs luna-88k with `-n 5`, so neither exit is pinned by anything today.

## M_SWEQ1 escapes and is DEBT, not floor -- one disclosure line owed
`if (d->software_interrupt_status[cpu] == 1)` scores **37/37**.  The store arm is
`d->software_interrupt_status[cpunr] = idata;` -- any 32-bit guest word -- while the body tests the field for
NONZERO-NESS only and never partitions the nonzero class.  Under the carrier's joint-cell ruling a value the body
does not test as a case is clause-(e) disclosure, not a floor cell, and the probe already drives both sides of the
partition the body DOES test (1 via the store, 0 via the read-clear).  So: not a breach; add one contract line --
*"does NOT catch a narrowing of the software-interrupt test to a particular value"*.

## THE DENOMINATOR I CLOSE ON -- derived, not enumerated, for the axis that broke
The alias axis is closed by an ARGUMENT about two sessions rather than by a list of mutants, which is what makes it
checkable.  Let `f` be the index map an operand swap installs on the per-cpu READS (`interrupt_enable`,
`software_interrupt_status`).

* **session C** (`-n 2`; slot 0 IDLE, slot 1 PENDING; rows `cpu1 deliver` and `cpu0 parked`) reds unless
  `f(0) = 0` and `f(1) = 1`.  It therefore kills `[0]`, `[cpu^1]`, `[cpu>>1]`, `[cpu|1]`, `[cpu&2]`, `[cpu|2]`,
  `[3-cpu]` -- every single-token map except the identity and `[cpu&1]`, which are identical on {0,1}.
* **session E2** (`-n 4`; slots 2,3 PENDING, slots 0,1 IDLE; rows `cpu3 deliver23`, `cpu2 deliver23`,
  `others idle23`) reds unless `f({2,3}) subset {2,3}`.  It therefore kills `[cpu&1]` -- the one C cannot see.
* Session E (all four pending, identical values) constrains `f` NOT AT ALL on this axis: every map into a pending
  slot is green there.  That is precisely why the v5 instrument was blind.

Together C and E2 force `f` to be the identity on {0,1} and a map of {2,3} into {2,3}.  The residue is a map that
permutes or folds 2 and 3 among themselves (`[cpu >= 2 ? 2 : cpu]`), which needs a slot-specific conditional rather
than a single-token index edit, and which nothing rows.  **DISCLOSE that residue; do not row it.**

The other axes of the (d) enumeration were already closed by tables 1-4 and I add nothing to them: the loop bound in
ten forms; `status & enable` narrowed (M_MASK30) and replaced (M_SWONLY); the latch dropped, collapsed and
parity-aliased (M_NOCLEAR, M_NODEASSERT, M_IRQACTIVE0, M_DEASSERT0, M_IRQACTIVEP1); the sw test conjoined with the
latch (M_SWLATCH); the callers (M_CALLGUARD, M_NOREASSERT); the `ncpus > 4` exit (M_EXIT8 -- EQUIVALENT, above).
Value-domain narrowings on a single lvalue are clause-(e) debt (M_SWEQ1, measured).

## Row-set archaeology (verified with `comm`, not read off the diffs)
    v4 (32) -> v5 (34):  +cpu0 deliver4, +cpu1 deliver4, +sio5 deliver1, **-others idle**   (exactly one deletion)
    v5 (34) -> v6 (37):  +cpu3 deliver23, +cpu2 deliver23, +others idle23                  (no deletion)
v6 restores BOTH things v5 removed -- the disagreeing 2/3-pending-with-0/1-idle configuration AND the
must-not-enter attribution row -- while keeping everything v5 added.  That is the right shape for the repair.

Table A ended clean: `BASE_final` 37/37 PASS, no sentinel, clone source `cmp`-identical to the baseline.
Artifacts: `_scratchpad/lunaabs/opus_p4_table/` (driver.log, PRETABLE, per-mutant .out, base_n5.out, mut_n5.out).
**Copy this directory into `regress/artifacts/lunaabsentcpu/` before any durable record cites these numbers** --
`_scratchpad/` is not a durable path and `probe_*.out` names get reused.

## Table B (`opus_p4_table_v5/`) -- the SHIPPED instrument, direct
Clone `/tmp/gxopusluna_p4b`, frozen v5 md5 **3fd0198f** (the brief's) and frozen v4 md5 552a81da, both run on every
binary.  BASE 34/34 (v5) and 32/32 (v4); BASE_final the same; no sentinel; source `cmp`-identical to the baseline.
(The driver's exit status is 1 because the launching `tee` could not create its log directory; the run itself carries
`OPUS_P4_V5_TABLE_DONE` and a green BASE_final -- read the sentinel, not the exit code.)

    M_ENP1         on v5: 34/34 PASS   on v4: 30/32 FAIL (cpu3 deliver, cpu2 deliver STOP)
    M_IRQACTIVEP1  on v5: 32/34 FAIL   on v4: 32/32 PASS

## Hygiene
Nothing outside the two `/tmp` clones was written.  `build/`, `build-asan/`, `est/` and `/tmp/gxsec-build` all
`cmp` CLEAN against SEC for `dev_luna88k.c` after both tables.  The main loop's `/tmp/gxlunaabs_kill` was not touched.
