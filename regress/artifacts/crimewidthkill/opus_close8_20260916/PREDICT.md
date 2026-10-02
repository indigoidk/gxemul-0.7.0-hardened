# PREDICT.md -- #529 closing pass 8, Opus MEASURING seat.  WRITTEN BEFORE ANY BUILD.
Liveness token CRIME_CLOSE8_20260916.  mtime proves the order; the mutator and the driver are written after this file.

Baseline NAMED: `GXEMUL-SEC/src/devices/dev_sgi_ip32.c` at md5 8c1d1545eeddd12fd49f52ccede60262 (the #529 working
set, UNCOMMITTED -- `git status` shows the file M).  Clone /tmp/gxopusc8, cmp-clean, base binary byte-identical
to table 11's (f06efcf64d253a6ba2e279e77ba71566).  Instrument: the SHIPPED probe, 188 rows, md5
2818bd4ea28ac3b6347fec4e219cc4c9 -- byte-identical to killtable11's frozen copy.

## THE CLAIM I AM TESTING

Read off `DEVICE_ACCESS(crime)` (:193-421), the accept path tests SIX partitions of guest-controlled input:

    len          `if (len == 8)' / `else if (len == 4)'                           -- AXIS 2 of the enumeration
    writeflag    three `if (writeflag == MEM_...)'                                -- AXIS 3
    relative_addr as a LABEL      `switch (relative_addr)' :322                   -- AXIS 4
    relative_addr as a LANE       `if (relative_addr & 4)' :282 AND :291          -- ** NOT AN AXIS **
    cpu->pc       `if (((uint32_t)cpu->pc & 0xffffff00) == 0xbfc05100)' :344      -- ** NOT AN AXIS **
    idata bits    `& DOG_ENABLE' :361, `& HARD_RESET' :364, `!= 0' :377           -- disclosed (multi-axis joints)

The enumeration names FOUR axes {latch} x {len} x {dir} x {label} = 56 cells.  The LANE and the PC WINDOW are
partitions the guarded body's OWN CODE induces on `relative_addr' and `cpu->pc', so by the 2026-09-04 joint-cells
rule the `relative_addr' partition owed is the JOIN {label} x {lane}, not {label} alone.  **My prediction is that
the enumeration is INCOMPLETE AS STATED and, for the SHRINK shape, COMPLETE IN EFFECT** -- because at the six named
labels the lane is UNSATISFIABLE (REV 0x00, CONTROL 0x08, INTSTAT 0x10, INTMASK 0x18, DOG 0x30, TIME 0x38 are all
8-aligned, so `relative_addr == CRIME_X' implies `(relative_addr & 4) == 0'), and at the default arm both lanes are
carried post-latch with an oracle each.

## THE DENOMINATOR I DERIVED FIRST (scripts/cellmap8.py, run BEFORE these predictions)

118 accepted CRIME accesses run post-latch across 18 of the 45 sessions.  On the FINER product
{len} x {dir} x {label} x {lane} x {REV window} every SATISFIABLE cell has at least one post-latch access; the 14
empty ones are all `lane=1 at a named label', which is the unsatisfiable set above.  A K-form mutant can only act
through a post-latch access at its own cell, so occupancy is a necessary condition and it is met everywhere.

## PER-MUTANT PREDICTIONS.  Base = 188/188 CONTROL=OK.

| # | mutant | edit | PREDICTION | row I expect to red |
|---|---|---|---|---|
| 1 | `L_dfl4w_hi` | C_dfl4w narrowed by `!(relative_addr & 4)` | KILLED ~185 | `p acc 40 sw`, `p acc 40 lw`, `top4 w` |
| 2 | `L_dfl4w_lo` | C_dfl4w narrowed by `(relative_addr & 4)` | KILLED ~186 | `p dog wlo`, `p dog whi` |
| 3 | `L_dfl4r_hi` | C_dfl4r narrowed by `!(relative_addr & 4)` | KILLED ~186 | `top4 rhi`, `p acc 40 lw` |
| 4 | `L_dfl4r_lo` | C_dfl4r narrowed by `(relative_addr & 4)` | KILLED ~185 | `top4 rlo`, `p rev lw4`, `p dog rlo` |
| 5 | `W_rev8r_out` | C_rev8r narrowed to pc OUTSIDE the window | KILLED 187 | `p rev ld` ONLY (not `p revP ld pc`) |
| 6 | `W_rev8w_out` | C_rev8w narrowed to pc OUTSIDE the window | **188/188** and EQUIVALENT | none -- the prelude rewrites reg[0] at the next access |
| 7 | `W_rev4w_out` | C_rev4w narrowed to pc OUTSIDE the window | **188/188** and EQUIVALENT | none -- same, high lane |
| 8 | `W_rev4r_out` | C_rev4r narrowed to pc OUTSIDE the window | **188/188** and EQUIVALENT | none -- `(int32_t)(0x11 >> 32)' is 0, and a decline answers 0 |
| 9 | `G_lane_ist` | latch-keyed LANE FLIP at INTSTAT 4R: `if ((relative_addr & 4) \|\| (relative_addr == CRIME_INTSTAT && (d->warned & CRIME_W_LEN)))` at :291 | **188/188 ESCAPE, GUEST-VISIBLE** | I expect NONE.  `C_ist4r' is killed by `istat ctl' ONLY -- a SIDE-EFFECT row (reassert raises IP2).  No row reads the VALUE a post-latch 4R at INTSTAT returns |
| 10 | `G_lane_tim` | same flip at CRIME_TIME | **188/188 ESCAPE, GUEST-VISIBLE** | NONE.  `p t4r gap' reads v0/v1; the `lw +0x38' result lands in a0 and a0 is never printed.  TIME's high half is always 0 (`(uint32_t)' at :172), so base reads 0 and the mutant reads the live low word |
| 11 | `G_lane_all` | the same flip with NO label conjunct (every post-latch 4R) | KILLED | `p dog rhi`, `top4 rhi`, `p acc 40 lw`, `p rev lw4` -- **the NEGATIVE CONTROL for 9/10**: it proves the lane-flip shape is observable in general, so a clean sweep at 9/10 is a property of the CELL, not of the shape |
| 12 | `D1_landpost` | a refused store LANDS once the latch is set (`else if (writeflag == MEM_WRITE) d->reg[relative_addr/8] = idata;` in the decline arm) | KILLED | `sh keeps`, `lo keeps`, `hi keeps`, `mid keeps`, `imask keeps` -- tests whether the keeps rows are measured POST-latch |
| 13 | `D2_remappost` | latch-keyed register re-map, all four `d->reg[relative_addr / 8]` sites: `(d->warned & CRIME_W_LEN) ? (relative_addr & 0x3f) : relative_addr` | KILLED | `top8 st+ld` (its `sd +0x278' is PRE-latch, the read-backs POST), `p rev ld`, `p acc ctl ld` -- tests whether `top8 anchor'/`top4 anchor', the ONLY re-map rows, being PRE-latch is a hole |

## WHAT EACH OUTCOME MEANS, stated before the run so it cannot be fitted afterwards

* 1-4 all KILLED  -> the LANE is covered in effect at the default arm; the axis omission is a WRONG RECORD (L4), not a breach.
* any of 1-4 ESCAPES -> the LANE is a missing floor axis and this is a GAP.
* 5 KILLED and 6-8 CLEAN -> the out-of-window REV halves are genuinely EQUIVALENT and 5 proves the predicate is
  satisfiable, so 6-8's clean sweeps are equivalence and not vacuity.  If 5 ALSO comes back clean, my whole
  W-group is vacuous and proves nothing -- I will say so.
* 9/10 ESCAPE and 11 KILLED -> a guest-visible latch-set mutant exists that table 11 did not build, at a cell the
  contract calls ROWED, and the row that "rows" it cannot see the value.  GAP (grading for the adjudicator: the
  shape is a LANE mis-selection, which RA3 puts outside the shrink class -- but RA3's exclusion rests on the anchor
  rows, and I predict those are measured with the latch CLEAR, which is the very argument that made the K-class floor).
* 9/10 KILLED -> I am wrong about `a0'/`istat ctl' and the enumeration closes on this axis too.
* 12/13 KILLED -> the landing and re-map classes are already measured post-latch and need no reopening.
