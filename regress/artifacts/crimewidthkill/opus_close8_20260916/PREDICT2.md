# PREDICT2.md -- #529 closing pass 8, SUPPLEMENTARY run.  WRITTEN BEFORE ANY BUILD OF THESE THREE MUTANTS.
mtime proves the order; `scripts/kill8b.sh` is launched after this file is on disk.
Two questions forwarded by the coordinator from the deepseek and glm seats.

## Q-A.  IS `CONTROL 4R` REALLY EQUIVALENT, OR IS TABLE 11'S `C_ctl4r` LEG VACUOUS?

The deepseek seat is right that the leg is vacuous, and I confirmed it from my own static map before reading their
argument: `scripts/cellmap8.py` puts `CTL 4R lane=0` at `sess=[26]` and NOWHERE ELSE, and session 26 is `rearm once`
-- 95 accesses, 46 of them post-latch, and its only two rows COUNT notices and check a RAM round trip.  So the cell
is driven post-latch exactly once, by a session with no value oracle.  188/188 there is "nothing looked", not
"nothing differs".

**MY PREDICTION: the contract's bucket is nevertheless RIGHT and the cell IS equivalent**, on a derivation I can
state from the source and am about to test:
* `:231` sets `d->reg[CRIME_CONTROL / 8] = CRIME_CONTROL_ENDIANESS` (0x100) at the top of EVERY access, so the
  register's high 32 bits are 0 whenever the width arm runs.
* CRIME_CONTROL is 0x08, so `relative_addr & 4` is 0 and `:294` takes `odata = (int32_t)(odata >> 32)` = 0.
* A declined read leaves `odata` 0 and the tail writes 0.
* The CONTROL switch arm at `:356` acts only on `MEM_WRITE`, so skipping it costs a read nothing.

| row | base | `C_ctl4r` | `G_lane_ctl` |
|---|---|---|---|
| `pre ctl4r` (lw +0x08, latch CLEAR) | `0x0` | `0x0` (the mutant is latch-keyed; it must not fire here) | `0x0` |
| **`post ctl4r` (lw +0x08, latch SET)** | **`0x0`** | **`0x0` -- EQUIVALENT** | **`0x100` -- the control MOVES** |
| `post ctl0c` (lw +0x0c, the other lane) | `0x100` | `0x100` | `0x100` |
| `post ctl8r` (ld +0x08) | `0x100` | `0x100` | `0x100` |

**`G_lane_ctl` is what makes this a measurement rather than another vacuous leg.** If `post ctl4r` does not move
under it, my row does not drive the cell either and I will say the question is still open.  If it moves under
`G_lane_ctl` and not under `C_ctl4r`, the cell is measured EQUIVALENT and the contract's bucket is right -- but its
warrant changes from "table 11 tested it" (false) to "derived, and measured by closing pass 8" (true).

## Q-B.  THE glm SEAT'S LATCH-CLEAR BYPASS AT TIME 4W/4R -- `G_glm_tim4clear`

    if (len == 4 && relative_addr == CRIME_TIME && !(d->warned & CRIME_W_LEN))
            goto crime_declined;

**I PREDICT IT ESCAPES: 188/188 on the shipped probe, CONTROL=OK.**  My reasons, derived here rather than taken
from the seat:
* `scripts/cellmap8.py` puts the post-latch `TIM 4W`/`TIM 4R` cells in sessions 26, 48 and 49 -- 48 and 49 are
  `p t4w gap` and `p t4r gap`, and BOTH open with a refused `lb +0x07`.  This mutant is switched off in exactly
  those sessions.
* The pre-latch drivers of that cell are `latch x5`'s ACCEPTS prologue (`sw 0x38`, `lw 0x38`) and session 26's --
  and `latch x5`'s rows count the *announce*, which a silent `goto` does not touch, while session 26 has no value
  oracle at all.
* I checked the seat's one REASONED step, and it holds by reading: the only surviving difference is the skipped
  `crime_update_crime_time()` at that access, and no probe row reads TIME between a pre-latch 4-byte access and
  anything else.  The `time * ctl` magnitude rows are driven by an accepted **8-byte** `ld` AFTER a refusal.

**IF IT ESCAPES, THE OWED ROW IS `scripts/t4clear.py`** -- the gapped shape MINUS the opening refusal, so every
access runs with the latch clear.  Predictions for it:

| row | base | `G_glm_tim4clear` | `C_ctl4r` (off-cell negative control) |
|---|---|---|---|
| `c t4w gap` | **large** | **small** | large |
| `c t4r gap` | **large** | **small** | large |
| `clear once` | `[0, 0]` | `[0, 0]` | `[0, 0]` |
| `ram` / `devsig` | ok | ok | ok |

`clear once` is the row that makes the shape honest: if it is not `[0, 0]` then a refusal crept in, the latch was
set, and the session is not measuring the latch-CLEAR state at all.

## Q-C.  glm NAMED ONE MEMBER; THE CLASS HAS FOUR, AND I DERIVED THE OTHER THREE BEFORE BUILDING ANY OF THEM

`scripts/preclear8.py` maps the accepted CRIME accesses that run BEFORE a session's first CRIME refusal -- 102 of
them across the 51 sessions -- and `scripts/sessrows.py` prints, for every session that drives a 4-byte access at a
NAMED label in that state, the rows that session feeds.  The result is a complete latch-CLEAR table for the twelve
4-byte-at-a-label cells:

| cell | sessions driving it with the latch CLEAR | a row that can see a SILENT decline there |
|---|---|---|
| REV 4W in window | 40, **42** | `revP sw pc` |
| REV 4W out of window | 40 | none -- but EQUIVALENT (the prelude rewrites reg[0]) |
| REV 4R in window | 40, **1** | `rev pc ctl` (its redirect needs the access ACCEPTED) |
| REV 4R out of window | 40, **0** | `devsig hi` reads 0 either way -- blind, but EQUIVALENT |
| CTL 4W | 40, **2, 3** | `sw08 halts`, `sw08 msg ctl` |
| **CTL 4R** | **40 ONLY** | **NONE** -- but predicted EQUIVALENT (Q-A) |
| IST 4W | 40, **44** | `istw sw` |
| **IST 4R** | **40 ONLY** | **NONE -- and GUEST-VISIBLE: it skips `crime_interrupt_reassert()`** |
| IMK 4W | 40, **43** | `acc imask sw` |
| IMK 4R | 40, **20** | UNCERTAIN -- session 20's `gate line`/`gate run` may or may not observe the reassert |
| DOG 4W | 40, **4** | `acc4 whi` |
| DOG 4R | 40, **4** | `acc4 rhi` |
| **TIM 4W** | **40 ONLY** | **NONE -- and GUEST-VISIBLE (this is glm's cell; close-7's E2 measured it)** |
| **TIM 4R** | **40 ONLY** | **NONE -- and GUEST-VISIBLE** |

Session 40 is `latch x5`, and its ONLY three rows are `latch x5`, `latch surv` and `latch said` -- two announce
COUNTS and a RAM round trip.  **A silent `goto crime_declined` touches none of the three.**

| mutant | PREDICTION on the shipped 188-row probe | on `t4clear.py` |
|---|---|---|
| `G_glm_tim4clear` (TIME 4W+4R, latch clear) | **188/188 ESCAPE** | `c t4w gap` AND `c t4r gap` both **small** -> caught |
| `G_clr_ist4r` (INTSTAT 4R, latch clear) | **188/188 ESCAPE** | 4/4 -- off-cell, so `t4clear.py` does NOT catch it either; it needs its own row |
| `G_clr_ctl4r` (CONTROL 4R, latch clear) | **188/188** -- and EQUIVALENT, the class's negative control | 4/4 |
| `G_clr_imk4r` (INTMASK 4R, latch clear) | **UNCERTAIN.  I predict KILLED by `gate line` or `gate run`** -- this is the one I genuinely do not know, and I am writing that down rather than picking the tidy answer | 4/4 |

If `G_clr_ist4r` also escapes then the owed repair is a CLASS, not glm's single cell, and the closing pass that
verifies it must enumerate `{latch clear} x {4} x {R, W} x {label}` the way table 11 enumerated the latch-SET half.

## Q-D.  THE codex SEAT'S CELL -- `K_ctl4w_reset_post` AND ITS 8-BYTE TWIN.  A LATCH-SET cell, and a GENERATING-SET breach

codex points at CONTROL 4W narrowed by the HARD_RESET branch.  This is on the OTHER half of the product from glm's
-- latch SET, inside table 11's own 28 cells -- and it is a floor breach by a DIFFERENT clause: the 2026-09-04
generating-set amendment, *"at each floor cell, every idata bit the guarded body TESTS is written both clear and
set"*.  The CONTROL arm tests three (`:361` DOG 0x200, `:364` HARD_RESET 0x800, `:377` the leftover).  Derived from
`scripts/cellmap8b.py`: post-latch the probe writes CONTROL with **0x01** (8W, session 46), **0x0001** and
**0x0201** (4W, session 46), and session 26's ACCEPTS values 0x0201 / 0x0001 / 0 / 0x0200 / 0x0100.
**HARD_RESET is CLEAR in every one**, and the only session that writes 0x800 -- `sw08 halts`, session #2 -- writes
it BEFORE any refusal.

| mutant | PREDICTION on the shipped 188-row probe | on `ctlreset.py` (the owed row) |
|---|---|---|
| `K_ctl4w_reset_post` | **188/188 ESCAPE** | `post rst 4w` **`0x12345678`** (the guest runs on) against a wanted SENTINEL -> caught |
| `K_ctl8w_reset_post` | **188/188 ESCAPE** | `post rst 8w` **`0x12345678`** -> caught |
| base | 188/188 | 5/5 -- both writes halt, and `post alive` shows a session with no CONTROL write survives |
| `G_glm_tim4clear` | (see Q-B) | 5/5 -- off-cell, so `ctlreset.py` does NOT catch glm's cell; each owes its own row |

`post alive` is the row that keeps `ctlreset.py` honest: without it, a probe whose guest never runs at all would
score both halt rows green for the wrong reason.

**AND ONE MORE PREDICTION I EXPECT TO BE WRONG-FOOTED ON, recorded because that is the point of writing these
first:** I expect `G_lane_ctl` to score **188/188** on the shipped probe too -- for the SAME reason as `C_ctl4r`
(no post-latch 4-byte read at +0x08 anywhere in the 188 rows).  If so, the CONTROL-4R cell is unrowed in BOTH
directions -- equivalent under a decline and unpinned under a lane change -- and that pairing is worth stating
plainly, because it is the difference between "no row is owed" and "no row exists".
