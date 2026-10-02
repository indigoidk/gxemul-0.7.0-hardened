# #529 crimewidthkill -- §F2 adjudication pass, Opus 5 compile-and-measure seat (2026-09-13)

Liveness token: `OPUS_CRIME_F2_20260913`

**VERDICT: GAP: `d->warned |= CRIME_W_LEN;` -> `d->warned |= len;`** (one token in the latch's set).  It scores
**71/71, CONTROL=OK** on the shipped 71-row detector (`logs/probe_lt_len.raw`).  With it, every refused halfword
prints the `(once)` announce again, because `len == 2` sets bit 1 and the latch tests bit 0: four refused
halfwords give four announces (`logs/obs_lt_len.raw`, `latch lh x4 = 4`).  That breaks contract item 4 as the
header states it ("the latch removed **or never set**"), and it is a clause-(d) operand swap drawn from a field the
guarded body reads (`len` is printed by the announce).  `d->warned |= relative_addr;` (lt_addr) and
`d->warned |= CRIME_W_LEN << writeflag;` (lt_wset) also score 71/71.
**A second floor-grade gap:** `goto crime_declined;` -> `if (relative_addr != CRIME_CONTROL || !(idata &
CRIME_CONTROL_DOG_ENABLE)) goto crime_declined;` (c_dog) scores **71/71**.  With it, a refused `sh 0x0a00` at
+0x08 **stops every CPU** (`logs/rep_c_dog.raw`, `sh08 run = 0xdeadbeef`).  The CONTROL arm tests DOG_ENABLE, and
no refused row ever writes that bit set.
**The product fix: no defect found.  Every gap is in the detector.**  All of them are killed by 10 rows (two new
sessions).  Measured green on base (28/28) and red on each survivor, in a reduced instrument (see "Repair").

## Apparatus

* Scratch clone `/tmp/gxopus529f2` = `cp -a /tmp/gxopuscrime`.  `dev_sgi_ip32.c` cmp-clean against GXEMUL-SEC (md5
  `8c1d1545...`, the file kill table 2 measured) before mutant 1.  Baseline rebuilt in the clone; `[ gxemul -nt
  src ]` checked; the base binary is **byte-identical** to `/tmp/gxopuscrime/gxemul` (`logs/setup.out`).
* Clone-local `.MUTANT` sentinel around both build phases.  After each phase: source restored from SEC, cmp clean,
  rebuilt, binary -nt source, restored == base byte-identical, sentinel removed (`logs/table.out`,
  `logs/phase2.out`).  The clone was deleted at the end after a final cmp.  `/tmp/gxopuscrime` was untouched: no
  sentinel, cmp clean.
* Detector: frozen copy of `regress/crime_width_probe.py`, md5 `48a558b5...`, which is table 2's instrument
  (`logs/INSTRUMENT.md5`).
* `scripts/crime_f2_obs.py` is an observation probe with the same apparatus, 26 rows.  Every row's want is the fixed
  build's behaviour, and each channel has an accepted-width CONTROL.  It scores 26/26 on base.
* `scripts/crime_f2_repairrows.py` is the proposed repair: only the sessions it replaces, written in the probe's own
  idiom.  It scores 28/28 on base.
* Mutant generator `scripts/mutants_f2.py` (find-text must occur exactly once).  Driver scripts were run from frozen
  copies (`f2_table.run-063152.sh`, `f2_phase2.run-074955.sh`).
* ONE probe run at a time throughout.  33 raw logs, every one ending in its sentinel (`CRIMEP_DONE` / `F2OBS_DONE` /
  `F2REP_DONE`), each checked before it was copied.

## Job 1 -- my pass-2 escapes, re-measured against the shipped 71-row detector on my own builds

| mutant | edit | 71-row detector | failing rows | = table 2? |
|---|---|---|---|---|
| base | none | **71/71 CONTROL=OK** | none | yes |
| a_lo10 | `goto crime_declined;` -> `if (relative_addr < CRIME_INTSTAT) goto crime_declined;` | **62/71** | sb nodflt, sh nodflt, imask lb, imask sb, istat lb, istat sb, time lb, time sb, hi nodflt | yes, row for row |
| a_imask | ... `if (relative_addr != CRIME_INTMASK) goto crime_declined;` | **69/71** | imask lb, imask sb | yes (= imaskft) |

Confirmed: both are killed, by exactly the rows table 2 names.  **But the obs probe shows the halfword cells at the
same labels still open under both mutants** (a_lo10: imask lh/sh, istat lh/sh, time lh/sh; a_imask: imask lh/sh).
That is the lead for job 2.

## Job 2 -- the smallest edit that breaks the fix and scores 71/71

| mutant | exact edit (post-fix `dev_sgi_ip32.c`) | 71-row | observable that differs (fix -> mutant) | disposition |
|---|---|---|---|---|
| **lt_len** | `d->warned \|= CRIME_W_LEN;` -> `d->warned \|= len;` | **71/71** | 4 refused halfwords: announces 1 -> **4** (`obs_lt_len.raw`) | **REAL ESCAPE -- floor (contract 4 "never set"; (d) swap from a body-read field)** |
| **lt_addr** | `d->warned \|= CRIME_W_LEN;` -> `d->warned \|= relative_addr;` | **71/71** | same session: 1 -> **4** (even offsets leave bit 0 clear) | **REAL ESCAPE -- same class** |
| **lt_wset** | `d->warned \|= CRIME_W_LEN;` -> `d->warned \|= CRIME_W_LEN << writeflag;` | **71/71** | 3 refused writes then a read: 1 -> **4** (`latch w-first`) | **REAL ESCAPE -- same class** (a half-applied per-direction latch) |
| **c_dog** | `goto crime_declined;` -> `if (relative_addr != CRIME_CONTROL \|\| !(idata & CRIME_CONTROL_DOG_ENABLE)) goto crime_declined;` | **71/71** | refused `sh 0x0a00` +0x08: RAM trip 0x12345678 -> **0xdeadbeef (CPUs stopped)**; refused `sh 0x0201`: CONTROL text 0 -> 1 | **REAL ESCAPE -- floor under the generating-set clause** |
| **h_imask** | `goto crime_declined;` -> `if (len == 1 \|\| relative_addr != CRIME_INTMASK) goto crime_declined;` | **71/71** | refused lh/sh +0x18: cause.IP2 clear -> **set** | **REAL ESCAPE -- width x label joint** |
| **h_lbl** | ... `if (len == 1 \|\| (relative_addr != CRIME_INTSTAT && relative_addr != CRIME_INTMASK && relative_addr != CRIME_TIME)) goto crime_declined;` | **71/71** | lh/sh at +0x10/+0x18: IP2 set; lh/sh at +0x38: next TIME read 66/132 -> **143,670,846 / 143,701,470** | **REAL ESCAPE -- all six halfword-at-label cells** |
| **wst_mc** | ... `if (writeflag == MEM_WRITE && relative_addr >= 0x200) d->reg[relative_addr / 8] = idata; goto crime_declined;` | **71/71** | refused sb 0xff +0x27f, then ld +0x278: 0x0 -> **0xff** | **REAL ESCAPE -- contract 7 narrowed by address** (keeps rows only at CRIME_DOG) |
| sft | ... `if (relative_addr != CRIME_SOFTINT) goto crime_declined;` | 71/71 | guest: IP2, SOFTINT, INTSTAT **identical**; host only: one stepped `[ crime: write to 0x20` debug() line | **EQUIVALENT on every guest channel** (default arm, no body for a declined access) -- disclose, do not row |
| l_brace | the `goto` moved inside the latch's `if { }` (brace slip: only the FIRST refused access declines) | **69/71** | imask sb, istat sb | KILLED, but by those two rows only |

**Why each one escapes, from the rows:**
* **lt_len / lt_addr**: `latch x5` issues `lb +7` first.  `len` = 1 and `relative_addr` = 7 both set bit 0, so the
  test is satisfied and the four refusals after it stay silent: count 1.  No other session holds two refused
  accesses under a text row.  (imask/istat do hold two, `lb +0x18` then `sb`, but they count only IP2.)
* **lt_wset**: `latch x5` is reads-first, and reads set bit 0.  No session holds two refused writes under a text row.
  The keeps session holds `sb +0x37` and `sh +0x30`, but it has no text row.
* **c_dog**: the only refused writes at +0x08 are `sb 0x01` and `sh 0x0800`, and neither carries 0x200.
* **h_***: the F5 repair rowed `lb` and `sb` at 0x10/0x18/0x38.  Those are **exactly the widths my pass-2 escape
  probe used.**  No `lh` or `sh` touches those labels anywhere in the probe.
* **wst_mc**: `sb keeps` and `sh keeps` sit at CRIME_DOG.  The refused `sb +0x27f` in the `hi` session is never
  read back.

**Other candidates the packet listed, checked:**
* **The COMMON TAIL.**  Label moves are equivalent on the declined path (pass 2: t_nohint, t_ret).  Moving the label
  INTO a side-effect arm (for example to `case CRIME_INTMASK:`) is killed by the imask/istat lb rows, by the same
  mechanism as imaskft.  Any tail edit that changes HARDINT or INTSTAT also changes every ACCEPTED access, so it is
  not a narrowing of the decline.  Not built.
* **The TIME rows' timing** (`logs/timing_base.raw`, 10 repeats of the `time lb` session on base): s1 is 66 or 132
  in **10/10** runs, and s2 is 285.9M..287.5M.  SMALL = 6.6M.  So the fixed build false-reds only if the host
  stalls **>= 100 ms** between the first `ld`'s `gettimeofday` and the device tick in the same `step` (the tick
  calls `crime_update_crime_time()` on wall-clock microseconds).  No run approached that.  **Not measured under
  load**: I deliberately did not load the machine while other seats may be measuring.  A false red here is possible
  only under severe host contention, and it would read `large` -- a loud failure, never a false green.
* **The free-running rows** (`logs/obs_base.raw`, F1).  The first `continue` in the transcript is the typed command:
  offset 1580, after the first `put w` at 1215, one occurrence in total.  The announce sits at offset 1598, after it.
  The CTRL-C break-in returns the `GXemul>` prompt and `print v0` reads 0x0.  **`free said` cannot be satisfied by
  stepped text**, because that session issues no `step`.  `free v0` depends on the break-in, and a failed break-in
  reads `absent`, which is a false red and never a false green.
* **Two-cell joints the packet named ("only 1-byte writes at INTMASK").**  These are rowed: `imask sb` kills them
  (only1w reds `imask sb` in table 2).  The open joints are the halfword ones above.

## Repair -- 10 rows, 2 new sessions, measured (reduced instrument `scripts/crime_f2_repairrows.py`)

| change to `regress/crime_width_probe.py` | new rows | kills (measured, `logs/rep_*.raw`) |
|---|---|---|
| imask/istat sessions: append `lh +off` then `sh +off` (each followed by `print cause`) **before** the accepted `lw`; wants `clear` | imask lh, imask sh, istat lh, istat sh | h_imask 26/28, h_lbl |
| time: add the `lh` and `sh` sessions (same shape as lb/sb) | time lh, time lh ctl, time sh, time sh ctl | h_lbl 22/28 (all six cells) |
| keeps session: issue **`sh +0x30` FIRST**, then `sb +0x37`, and count the session's announces | keeps once (want 1) | lt_len 27/28, lt_addr 27/28, lt_wset 27/28 |
| hi session: append `ld +0x278` after the refused `sb +0x27f`, want 0x0 | hi keeps | wst_mc 27/28 |
| sh08 session: value `0x0800` -> **`0x0a00`** (DOG_ENABLE set as well as HARD_RESET) | (none; `sh08 run` changes value) | c_dog 26/28 |

**base 28/28; sft 28/28** (it stays green, as it should).  Caveats, stated plainly:
* This is a REDUCED instrument: the replaced sessions only.  The transplanted 81-row probe **has not been run**.  It
  owes a base run and a re-table of the 21 table-2 kills.
* My script did not carry the `sh08 pc` row.  With 0x0a00, a plain fall-through at CONTROL still clears DOG and hits
  HARD_RESET, so only2w/a_ctl should still die there.  That is predicted, not measured.
* Why the keeps reorder and not a reordered `latch x5`: set-only-by-writes needs a READ before the first write, which
  `latch x5` already provides.  Set-only-by-reads, set-by-len and set-by-address need a write, a halfword and an even
  offset FIRST; `sh +0x30` is all three.  The two sessions together cover all four shapes.
* Side effect of the imask/istat append: l_brace's kill margin grows from 2 rows to 6.  I predicted this from the
  mechanism and did not measure it.

## Answers

**Q1 -- F1..F18, D1, D2**
* F1 UPHOLD (arithmetic).  F2 UPHOLD.  F3 UPHOLD (my t_nohint).  F4 UPHOLD (revwrite 69/71).
* **F5 UPHOLD the finding, REFINE the repair.**  It rowed lb/sb only, and h_lbl sweeps all six lh/sh-at-label cells
  71/71 (below, and Q2).
* F6 UPHOLD.  REFINE: a default-arm fall-through at an unrowed offset (sft) is guest-EQUIVALENT, and should be
  disclosed the way DOG and CONTROL-read are.
* F7 UPHOLD (verified: the break-in works, and the split point is the typed `continue`).
* **F8 REFINE -- the weakest, see Q2.**
* F9, F10 UPHOLD.  F11 UPHOLD.  F12 UPHOLD.  F13 UPHOLD.  F14 UPHOLD.
* F15 UPHOLD the refinement.
* **F16 REFINE**: l_static is equivalent for ONE MACHINE PER PROCESS.  `src/core/emul.c` allocates `n_machines`
  per emul, so a config holding two ip32 machines would silence the second machine's announce under a
  function-static latch.  Disclose it as "one machine per emulator process", not "IP32 has one CRIME".  (Not
  measured.)
* F17 UPHOLD the rejection.  F18 UPHOLD.
* **D1 UPHOLD**, re-measured here.  On base the refused lb/sb/lh/sh at 0x10/0x18 leave IP2 clear, while the accepted
  lw sets it.  a_lo10 sets it at the refused access.  Nothing is wrong with the measurement.  The one premise it
  rests on -- SOFTINT's default-arm store does not reassert -- is pinned by the `imask pre`/`istat pre` controls.
* **D2 REFINE (my own position, held harder).**  The ruling holds for {INTSTAT, INTMASK, TIME} x {R, W}: floor cells,
  now rowed.  **It does not extend to width.**  The guard's body-tested partition of `len` is {8}, {4}, {else}, so
  lh versus lb at a label is not a floor axis under the joint-cells rule.  So h_* is clause-(e) debt *by that rule*
  -- **but** (a) contract 3's text, "narrowed by width, direction, **or** ADDRESS", reads as claiming the joint, and
  the header nowhere discloses it (only POSTTABLE does); and (b) the repair closed exactly the cells my mutant used.
  That is `#499`'s pattern, and the class-closure amendment says the next repair closes the class.  The cost is four
  appended steps and two sessions.  **c_dog and lt_* are floor on their own terms**: the generating-set clause for
  c_dog, and contract item 4 plus the (d) swap from a body-read field for lt_*.  None of them depends on D2.

**Q2 -- the weakest accepted disposition.**  **F5 as implemented**, and it is my own recommendation.  My pass-2
report said "the reassert session with `lb +0x18` then `sb +0x10` ... the TIME session", and the repair rowed
exactly those widths.  h_lbl then escapes 71/71 at all six halfword cells.  The breach reappeared inside its own
repair, at the cells adjacent to where the mutant had been.
A close second is **F8**: keeps is rowed at CRIME_DOG only, which is the same near-end blindness F11 was accepted
for on the accept side; wst_mc 71/71.
And the gap no finding touched: **no seat, me included, enumerated the latch SET's operand.**  Table 1 swept
nolatch/latchinv, pass 2 swept `=` for `|=` and the static form, and lt_len is one token away from all of them.

**Q3 -- what all nine of us missed.**  `d->warned |= CRIME_W_LEN;` -> `d->warned |= len;` (71/71).  The row I
expected to catch it was `latch x5`, and it cannot: its first access is a byte at an odd offset, which sets the
tested bit under all three latch mutants.

## What I could not measure

* The transplanted full probe (81 rows) on base and on the 21 table-2 kills.
* `sh08 pc` under the 0x0a00 value.
* The TIME rows under host load.
* l_static in a two-machine config.
* Widths 3/5/6/7 and lwl/lwr/swl/swr (disclosed, unchanged).
