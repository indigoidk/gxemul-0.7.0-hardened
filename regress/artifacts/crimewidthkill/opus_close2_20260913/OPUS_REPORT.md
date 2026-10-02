# #529 crimewidthkill -- SECOND CLOSING PASS, Opus compile-and-measure seat (2026-09-13)

Liveness: `OPUS_CLOSE2_ALIVE_20260913`. First line of `_scratchpad/CHECKPOINT.md`:
`# CHECKPOINT -- 2026-09-13 ~13:4x   HEAD 9c91999 (records)   crimewidthkill #529: TABLE 4 PROBE LANES RUNNING (clone restored)`

**VERDICT: `GAP: if (writeflag == MEM_READ && relative_addr == CRIME_INTSTAT) odata = d->reg[relative_addr / 8];`
inserted before `goto crime_declined;`** in `DEVICE_ACCESS(crime)`.

A refused read at the named label CRIME_INTSTAT answers the register instead of 0. It scores **111/111**
(`logs/probe_istat_leak.raw`). A guest-only session shows it is not equivalent: base `0x0`, mutant
`0xffffffffffffffff` (`logs/disc_c2.out`). The same shape at **CRIME_DOG** also scores 111/111
(`logs/probe_dog_leak.raw`). So does a byte-lane-aware form of the INTSTAT leak (`logs/probe_istat_lane.raw`).

**Against the main loop's 121-row repair (`BIT = 0x10000001`), the naive form is now caught (119/121). The byte-lane
form still scores 121/121:**
`if (writeflag == MEM_READ && relative_addr == CRIME_INTSTAT) odata = d->reg[relative_addr / 8] >> (8 * (8 - len - (relative_addr & 7)));`
(`batch3/probe121_istat_lane.raw`; see the ADDENDUM).

This is item 9 of the contract, "the ANSWER at each named label". It is a floor cell, and DISCLOSED explicitly
says it is rowed. So it is not disclosed debt: the disclosure is wrong.

## *** ADDENDUM: the gap SURVIVES the main loop's repair (the 121-row probe) in its byte-lane form. MEASURED. ***

While batches 1 and 2 ran, the main loop edited `regress/crime_width_probe.py` to 121 rows (md5 `7f286f51`, mtime
17:21). It set `BIT = 0x10000001` (the kimi CLI seat had found the same class), seeded DOG before the dog reads, and
added `top rd2 v0`. Kill table 5 (running concurrently) carries the NAIVE leak `c2_reg_istat` / `imask` / `dog`.
**It does not carry the byte-lane form**, so I measured that against the frozen 121-row probe in a fresh clone
(`batch3/`; `PRETABLE3.out` written at 18:08:52, before the batch was launched):

| run (121-row instrument) | predicted | measured (log) | red rows |
|---|---|---|---|
| base | 121/121 | **121/121** `batch3/probe121_base.raw` | none |
| **istat_lane** `odata = d->reg[relative_addr / 8] >> (8 * (8 - len - (relative_addr & 7)))` at CRIME_INTSTAT | 121/121 | **121/121** `batch3/probe121_istat_lane.raw` | **none** |
| istat_leak (the naive form the repair targets) | 119/121: istat lb v0, istat lh v0 | **119/121** `batch3/probe121_istat_leak.raw` | istat lb v0 (0x1), istat lh v0 (0x1) |

**Why the repair misses the lane form.**
* The refused lb/lh read at the slot BASE (+0x10, +0x18), and the lanes there are the MOST significant bytes of
  the 64-bit slot. That is the model's own rule: the 4-byte read path answers a base-offset access with the HIGH
  half.
* `0x0000000010000001` still has `0x00 0x00` in those lanes, so `BIT = 0x10000001` moved the nonzero byte to the
  one lane only the naive leak reads.
* The lane form is shown NOT equivalent in `logs/disc_c2.out`: `0x0` -> `0xffffffffffffffff`.
* **The same holds at INTMASK by the identical seeded value (reasoned, not built).**
* DOG's new seed `0x0123456789abcdef` has a nonzero top byte, so the lane form there is closed (reasoned, not
  built).

**Repair (predicted, not measured):** seed SOFTINT and INTMASK with a value that is nonzero in the TOP lanes as well,
e.g. `0x0101000010000001`. The reassert still sees bit 28, and the top bits only make `status & mask` more nonzero.
The alternative is to refuse at a lane that holds the nonzero byte, but +0x13/+0x17 are not the INTSTAT label (they
reach the default arm), so a label-keyed mutant would not fire there. **Seed the value; do not move the read.**

This is `#499`'s shape again: the repair closed the cell at exactly the lane the reported mutant used.

## Why no row can see it (the CHANNEL defect)

* Table 4 killed item 9 only with the **constant** form, `odata = 1` (`rev_od1`, `istat_od1`, `time_od1` in
  `../killtable4_20260913/mutants529d.py`).
* A constant has a nonzero low byte. The **register** form, which is the accept path's own expression, reads
  whatever the register holds in the lanes the refused lb/lh touch, and in these sessions those lanes are 0:
  * **The istat/imask sessions:** they seed SOFTINT = INTMASK = `BIT` = 0x10000000. So INTSTAT and INTMASK
    hold `0x0000000010000000`, whose bytes 0..1 (big-endian lanes) and low byte/halfword are all zero.
  * **The dog session:** it never seeds DOG, so DOG is 0.
* So `istat lb v0`, `istat lh v0`, `imask lb v0`, `imask lh v0` and `dog v0` read 0 under the leak exactly as
  under the decline.
* The discriminator shows the blindness directly. With the probe's own `BIT`, base and mutant both read `0x0`
  (lb and lh). With SOFTINT = 0xff, the mutant reads `0xffffffffffffffff`.
* **In a real guest this is not a corner case.** The `gate` session itself shows HARDINT = 0x20 once a MACE
  interrupt is latched. So INTSTAT's low byte is nonzero whenever a hardware interrupt is pending, and the
  leak hands it to the guest.

## Mutant table (frozen instrument `/tmp/cwp_close2.py`, md5 `1b1bb8fb` = shipped `regress/crime_width_probe.py`)

Scratch clone `/tmp/gxopus529c2` (`cp -a build/`). Its `dev_sgi_ip32.c` was `cmp`-clean vs SEC (md5 `8c1d1545`).
The baseline was rebuilt in the clone and passed `-nt`. The sentinel was held during both build batches. Both
restores are verified: `cmp` clean, binary `-nt`, binary byte-identical to the baseline. The clone has been
deleted. Every log ends `CRIMEP_DONE`. Binary md5s are in `logs/BINARIES.md5` and diffs in `logs/<m>.diff`.

| mutant | edit (inserted before `goto crime_declined;` unless noted) | predicted | measured (log) | red rows | equivalent? discriminator (base -> mutant) |
|---|---|---|---|---|---|
| base | -- | 111/111 | **111/111** `probe_base.raw` | none | -- |
| **istat_leak** | `if (writeflag == MEM_READ && relative_addr == CRIME_INTSTAT) odata = d->reg[relative_addr / 8];` | 111/111 | **111/111** `probe_istat_leak.raw` | none | **NOT equivalent**: SOFTINT=0xff, lb +0x10: `0x0` -> `0xffffffffffffffff`. With BIT: `0x0` -> `0x0` (the blindness) |
| **dog_leak** | same, `relative_addr == CRIME_DOG` | 111/111 | **111/111** `probe_dog_leak.raw` | none | **NOT equivalent**: sd DOG 0x0123456789abcdef, lb +0x30: `0x0` -> `0xffffffffffffffef`; lh: `0x0` -> `0xffffffffffffcdef` |
| **istat_lane** | `... == CRIME_INTSTAT) odata = d->reg[relative_addr / 8] >> (8 * (8 - len - (relative_addr & 7)));` | 111/111 | **111/111** `probe_istat_lane.raw` | none | **NOT equivalent**: SOFTINT=0xff00.., lb +0x10: `0x0` -> `0xffffffffffffffff`; lh: `0x0` -> `0xffffffffffffff00` |
| **rd_hi_lh** | `if (writeflag == MEM_READ && len == 2 && relative_addr >= 0x200) odata = d->reg[relative_addr / 8];` | escape | **111/111** `probe_rd_hi_lh.raw` | none | **NOT equivalent**: sd +0x278, lh +0x27a: `0x0` -> `0x708` |
| rd_hi_lb (control) | the same with `len == 1`: o_rd_hi narrowed to its own row's width | caught by top rd v0 | 110/111 `probe_rd_hi_lb.raw` | top rd v0 | -- (exact) |
| rd_lh_all (control) | `if (writeflag == MEM_READ && len == 2) odata = d->reg[relative_addr / 8];` | caught; I named istat lh v0 and time lh v0 | 106/111 `probe_rd_lh_all.raw` | lh v0, lhu v0, lh rev v0, time lh v0, ctl v0 | -- **istat lh v0 / imask lh v0 stayed GREEN, and my named row was wrong. That is what led to batch 2.** |
| soft_gate | `if (d->reg[CRIME_SOFTINT / sizeof(uint64_t)])` (decline only when SOFTINT is set) | caught by sh08 run | 93/111 `probe_soft_gate.raw` | 18 rows incl. sh08 run, sh08b run, sb08 msg, all rev pc, all time, nodflt x5 | -- (the state floor holds at the SOFTINT operand; not in table 4) |

**Prediction record, stated plainly.**
* **Batch 1 (the last four rows):** the predictions are the comments in `mutants_c2.py`. They were frozen at
  16:57:15, before the first build (16:57:17) and the first probe (`probe_base.raw` ended 17:05; see
  `logs/ORDER.txt`). They name the outcome and one row each, not full red sets. One of them was wrong in a row
  it named (rd_lh_all: istat lh v0).
* **Batch 2 (the three leak mutants):** `PRETABLE2.out` was written at 17:38:41, before the batch-2 builds
  (17:39:25). All three outcomes and all three discriminator values matched it.

## Q1 -- floor gaps, most severe first

1. **The answer at a named label, register form: INTSTAT (measured), DOG (measured), INTMASK (reasoned only, not
   built).** The rows pin 0 against registers whose read lanes are 0. The imask session's reg[INTMASK] is the
   same `0x10000000`, so `imask lb/lh v0` are blind in the same way. The cheapest repair is predicted, not measured:
   * **The istat and imask sessions:** seed SOFTINT and INTMASK with `BIT | 0xffff` instead of `BIT`.
     `status & mask` still asserts under the same condition, and the default-arm store still does not reassert,
     so the `pre`/`ctl` rows should not move.
   * **The dog session:** add an accepted `sd +0x30, 0x0123456789abcdef` before its lb +0x30. It is not a
     refusal, so `dog once` still has its first refusal at DOG.
   * No new session and no new row is needed; only the seeded values change.
2. **The far-block read answer, 2-byte (rd_hi_lh).**
   * Contract item 9 claims "a refused read >= 0x200 answering the register" and rows it with `top rd v0`, which
     is an **lb** only. The repair widened `hi keeps` to both widths for the store side (sb +0x27f and sh +0x27c)
     but not the read side. That is the #499 symmetric cell, reproduced inside the repair for it.
   * I rank it below (1) because the far block is not a named label, so it can be argued as a width x region
     joint (clause e).
   * But it is NOT in the DISCLOSED list: the joint-predicate bullet covers only the latch. So it must be either
     rowed or disclosed. The cheapest row is one refused `lh +0x27a` in the top session after the sd, wanting 0.

**Not gaps, measured:** soft_gate (93/111). **Candidates reasoned about and not built:** a re-arm keyed on an
accepted WRITE at the INTSTAT/INTMASK/TIME/REV arms. The rearm session enters those arms with reads only, and
enters CONTROL with a write only. This is a direction x label joint, so clause (e); I did not measure it.

## Q2 -- is the repair diff sound?

* **The item-9 rows `imask lb v0`, `imask lh v0` and `dog v0` have no measured kill anywhere.** In table 4 they
  were reddened by 0 of 47 runs (`grep -c` over `../killtable4_20260913/table4.out`), and `ctl v0` also by 0.
  My rd_lh_all now reddens `ctl v0`, so that row is shown able to vary. The other three are still unkilled, and
  for the register form they cannot vary by construction (above). By the accept-row failability standard (a row
  is discharged by a measured kill, not by existing), they are undischarged.
* `istat lb/lh v0` are killed only by the constant form. They pass the register form.
* Everything else I exercised varied as its record claims: `top rd v0`, the lh/rev/time answer rows, and the
  state-gate rows (soft_gate).

## Q3 -- statements that are wrong

1. **DISCLOSED, "(item 9 rows the READ answer at every named label)":** false for the register-answer form at
   INTSTAT and DOG (both measured 111/111), and at INTMASK by the identical value.
2. **POSTTABLE 4's DENOMINATOR, "the answer of a refused read at REV, CONTROL, INTSTAT, INTMASK, DOG, TIME and the
   far block":** the table swept REV, INTSTAT and TIME only with `odata = 1`. **No mutant in tables 1-4 was aimed
   at the INTMASK, DOG or CONTROL answer cells** (0 of 47 runs reddened their rows). The denominator lists cells
   that were never looked at, so "zero looked for" is rendered as "zero found".
3. **Contract item 9's far-block clause:** true for 1-byte refused reads only (rd_hi_lh).
4. **Checked and TRUE:** "57 of 57 predicted red-row sets exact". `check_pred.out` reads
   `CHECKPRED exact=57 differs=0`, all 57 logs end `CRIMEP_DONE`, and PRETABLE 13:03 predates `probe_base.raw`
   13:16.

## What I could not measure

* **Only istat_lane and istat_leak were run against the 121-row probe.** rd_hi_lh and dog_leak were not re-run
  against it. They are predicted killed by `top rd2 v0` (0x708) and `dog v0` (0xef), and table 5 carries
  `c2_reg_dog`.
* The INTMASK leak, both forms (not built; inferred from the identical seeded value).
* The kill power of the suggested repairs.
* The write-direction re-arm at the read-only-entered arms.
* Host-load sensitivity of the TIME rows (runs were serial, on a quiet host).
