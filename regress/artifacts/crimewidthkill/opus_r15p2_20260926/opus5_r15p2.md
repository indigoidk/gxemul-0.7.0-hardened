OPUS5_R15P2_ALIVE_0926

`C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`, first line, verbatim:

> # CHECKPOINT -- 2026-09-26 00:35 (087a90 sections rewritten; the peer's sections below are untouched)

**VERDICT: THE RULED FLOOR IS CLOSED; THE CONTRACT'S CLAIM IS NOT.** All five latch-SET label swaps are killed. But TEN
non-equivalent mutants inside {observable label} x {latch state} score 218/218 on the frozen probe. Each has a
one-session discriminator that shows its guest-visible (or host-text) difference. A census of a full probe run finds 8 of
the 36 observable label x width x direction x latch cells exercised by NO session, all at INTSTAT/INTMASK. Whether those
cells are owed is the adjudicators' call: clause (e) by PRETABLE14's letter, owed by the probe's own contract text.

- **Q1(a)** TRUE for every row. Only three things cross sessions: the 16-byte dummy image (read-only), the host clock and
  host load. Load moves only the magnitude rows. Their measured margins: the largest non-leak s1 is 1914, SMALL/3448,
  and the smallest leak is 1.42e8, 21.6 x SMALL. Measured: 66 sessions, 66 fresh pids, and every session's device TIME
  and latch start at 0.
- **Q1(b)** TRUE, measured from the device side. In all four `tl` sessions: s0 latches `last_microseconds` and adds 0; the
  first-step tick adds 66 x 9-12 us; the +0x07 and +0x38 refusals make NO update; s1 returns exactly the tick's value
  (726/792/726/594, identical to the probe's printed `raw`). **One premise is wrong as stated:** the brief says
  "exactly ONE CRIME tick per session", and every stepped session (56 of 56) has THREE. The other two are
  `cpu_run_deinit`'s "two last ticks" after `quit` (`src/cpus/cpu.c:404-416`). They are harmless here because they come
  after the last print.
- **Q1(c)** TRUE, measured. `M5_revlatch` and `M1_gotolatch` red all four `rl` rows with pc = ra = 0x80004000 (table 14
  logs). The arm's only test is `cpu->pc` (`:344`), so width and direction cannot matter.
- **Q1(d)** FALSE. `D_nodogclear` was not the only DOG-partition mutant the 204 rows missed. `D_doglen8` (DOG cleared
  only at 8 bytes) also escaped them, and the pair kills it at `sw`. Both of those are derived from its measured
  discriminator and replay; it had no probe run. `D_doglatch` and `D_dogbit0` escape even the 218, and that is measured
  (Q2).
  PRETABLE14's own example of "DOG -> stop" (the `:364` test widened to DOG|HARD_RESET) is **EQUIVALENT**: `:362` has
  already cleared DOG before `:364` tests it. Measured: the CPU runs on and the texts match base in all three DOG
  sessions.
- **Q1(e)** The label list is complete. A narrow access at any non-label offset lands in `default:`, and the tail answers
  0 for every narrow read, fall-through or not. But "observable" depends on state:
  * REV only from the PROM window;
  * CONTROL only on writes, and only as host text when HARD_RESET is clear;
  * INTSTAT/INTMASK only when the reassert changes the line. **The probe exercises only the RAISE.** No refused access at
    those labels ever runs with the line already asserted (census), so the LOWER direction is unobserved even for the
    plain M6.
- **Q2** NOT ZERO. Ten measured 218/218 escapes, each with its log in `runs/` and every log ending `CRIMEP_DONE`:
  * `P_ist1r_set`, `P_imk1r_set`: INTSTAT/INTMASK, 1R, latch SET;
  * `C_istW_clr`, `C_ist2_clr`, `C_imkW_clr`, `C_imk2_clr`: INTSTAT/INTMASK, latch CLEAR, direction-only or width-only;
  * `P_ctl2wrc_set`: CONTROL 2W, latch SET, HARD_RESET clear;
  * `P_istprev_set`: INTSTAT, latch SET, line already asserted;
  * `D_doglatch`, `D_dogbit0`: the DOG partition.

  Positive control for the latch-CLEAR shape: `C_ist1r_clr` scored 214/218, red on exactly `istat lb/sb/lh/sh`, as
  pre-registered in `PRED_b3.out`.

  Denominator: 36 observable cells, 28 exercised by a rowed refusal, 8 exercised by none (table in section 4). Plus the
  value, state and DOG shapes listed there. Every candidate I did not build is listed with its reason.
- **Q3** The pair is the right member by the ruling's conditional, and its channel is sound against every single-edit
  DOG mutant I built. It can read ONE with the 0x0200 write printed only if the 0x0201 twin's print is also lost, and
  `p acc ctl msg` sees that loss. **Two members nobody named:**
  * a CONTROL-text COUNT row on the two EXISTING ACCEPTS sessions, which already hold the 0x0200 writes in BOTH latch
    states. It needs no new session and it kills `D_doglatch`, which the pair cannot see. Replay-measured, as
    pre-registered, as `rearm`/`latch x5`: base 4/4, `D_nodogclear` 6/6, `D_doglatch` 6/4, `D_doglen8` 5/5.
  * a value-anchored text: count `unimplemented control 0x0000000000000001` rather than the prefix. It kills
    `D_dogbit0` (measured: that build prints 0x201 where base prints 0x1, at both widths).
- **Q4** No difference. All 18 legs are EXACT, re-derived independently from each raw log's own row lines (`q4_check.py`),
  and all 18 logs end in `CRIMEP_DONE`. No row reds on a leg whose hunk does not reach it.

---

## 1. WHAT I RAN (every path below is under this seat's artifacts dir unless absolute)

* **Clone.** `/tmp/gxopus_r15p2` is a `cp -a` of `/tmp/gxopus_r14`. Before any edit, `dev_sgi_ip32.c` `cmp`-clean
  against the working tree (md5 8c1d1545) and the binary byte-identical to `/tmp/gxopus_r14_bins14/base`. Mutators:
  `mutants_r15p2.py`, exact-string edits in which text-not-found is fatal. Builds: `build_r15p2.sh`, with a
  sentinel-guarded restore; every build has `[ gxemul -nt src ]`, `[ .o -nt src ]`, and its binary copied to
  `/tmp/gxopus_r15p2_bins/`. Diffs are in `mutants/`, build logs in `builds/`.
* **Controls on the construction.**
  * `P_ist_set` and `P_imk_set` are my `latch_set()` shape with the bare label condition. Their binaries are
    **byte-identical** to table 14's `M6_istlatch` and `M7_intmasklatch` (`cmp`), so table 14's kills (215/218 each)
    apply to my construction unchanged.
  * `restored` is byte-identical to table 14's base, and so is every rebuild after a mutant.
  * `C_ist1r_clr` is the latch-CLEAR shape landing on a ROWED cell, the positive control for the `C_` escapes.
* **Discriminators** (`disc_r15p2.py`, the probe's own `session()`/`ld()`/`st()` copied verbatim). One short session
  per candidate cell, run on every binary: `disc/`, and the table is `disc_matrix.out`. Each mutant differs from base
  ONLY at the cells it was built to open. `restored` (= base) and `census` read identically on all ten. The three DOG
  discriminators are in `disc/dog_*.out`.
* **Full probe runs.** The frozen `crime_width_probe.table14.py` (md5 f5e915f6, verified by the driver), four lanes per
  batch, logs in `runs/`, drivers `probe_batch.run-b{1,2,3}.sh`. Batch 3's predictions are in `PRED_b3.out`, written at
  03:02:13, before batch 3 started at 03:17:42. **Batches 1 and 2 had no pre-written prediction file;** each mutant was
  built as a candidate escape, which is the whole of the prediction.
* **Census.** `census` is the base plus an append-only log of every CRIME access and every TIME update at device entry:
  latch, `prev_asserted`, SOFTINT, INTMASK, HARDINT, TIME and pc. I ran the full probe on it (218/218, OK). The full log
  is `census_probe_run.log.gz` (5.6 MB). `census_probe_run.trimmed.log` (60 KB) collapses the free-running sessions'
  ticks to a count and reproduces `census_analyze.out` byte for byte (`diff`-checked). The session order and row mapping
  were read off the probe itself with `session()`
  stubbed (`rec_sessions.py` -> `sessions_f5e915f6.json`). The analysis is `census_analyze.py` -> `census_analyze.out`,
  plus `census_facts.out`. A symbolic replay of the recorded commands (`static_census.py` -> `static_census.out`) agrees
  with the measured census on all 66 of 66 sessions.
* **Q4:** `q4_check.py` -> `q4_check.out`. **ACCEPTS replays:** `replay_accepts.py` / `replay_all.sh` -> `replay/`.
* **File versions.** `mutants_r15p2.py` and `disc_r15p2.py` gained entries (the DOG and `C_ist1r_clr` legs, the DOG
  discriminators) after their first use; each later version only ADDED entries. The builds ran the mutator as it stood
  at 02:28, 02:36 and 02:59, and the discriminator and probe runs used frozen copies. What was built is exactly
  `mutants/<leg>.diff`.

## 2. THE PROBE RUNS (frozen f5e915f6, 218 rows; every log ends `CRIMEP_DONE`, checked with `tail -1`)

    leg              score    CONTROL  failing rows        cell it opens (the discriminator that shows it: disc_matrix.out)
    census (base+log) 218/218 OK       none                -- (the base: logging only)
    P_ist1r_set      218/218  OK       none                INTSTAT, 1R, latch SET          ist_lb_set: IP2 raised
    P_imk1r_set      218/218  OK       none                INTMASK, 1R, latch SET          imk_lb_set: IP2 raised
    C_istW_clr       218/218  OK       none                INTSTAT, W (1W+2W), latch CLEAR ist_sb_clr, ist_sh_clr
    C_ist2_clr       218/218  OK       none                INTSTAT, len 2 (2R+2W), CLEAR   ist_lh_clr, ist_sh_clr
    C_imkW_clr       218/218  OK       none                INTMASK, W (1W+2W), CLEAR       imk_sb_clr, imk_sh_clr
    C_imk2_clr       218/218  OK       none                INTMASK, len 2 (2R+2W), CLEAR   imk_lh_clr, imk_sh_clr
    P_ctl2wrc_set    218/218  OK       none                CONTROL 2W, SET, HARD_RESET clr ctl_sh0201_set: 2 texts, base 0
    P_istprev_set    218/218  OK       none                INTSTAT, SET, line up (LOWER)   ist_prev_set: IP2 dropped
    D_doglatch       218/218  OK       none                DOG clear only w/ latch CLEAR   dog_sw_set: 0x200 printed
    D_dogbit0        218/218  OK       none                DOG test && !(idata & 1)        0x0201 prints 0x201, not 0x1
    C_ist1r_clr      214/218  OK       istat lb, istat sb, istat lh, istat sh   POSITIVE CONTROL: the C_ shape on a ROWED cell
    (not run: P_ist_set = M6_istlatch and P_imk_set = M7_intmasklatch byte for byte -- table 14 has them at 215/218)

Batches: b1 02:37:09-02:57:20, b2 02:57:30-03:17:41, b3 03:17:42-03:37:53 (load average under 0.25 at each start). Batch
3 and the replays came out exactly as `PRED_b3.out` (03:02:13) predicted.

## 3. Q1 IN DETAIL

**(a)** `session()` forks and `execv`s a new emulator per call, and the census shows 66 distinct pids for the probe's 66
`session()` calls. Every session's first CRIME access sees TIME = 0, latch = 0 and SOFTINT = INTMASK = HARDINT = 0, so
no device state carries over. The only `fopen` calls in `src/core/` are read-mode (`emul.c:576`, `emul_parse.c:706`).
The terminal is set with `TCSANOW` at all five `tcsetattr` sites in `console/console.c`, so queued input is never
flushed.

What does cross sessions:

* **`/tmp/dummy_crimep.bin`.** 16 zero bytes, created once. There is a creation race only if it is absent while
  several lanes start.
* **The host clock and load.** These move ONLY the magnitude rows. The margins, measured over table 14's 18 logs and
  this seat's runs:
  * green s1: n = 192, range 0-1914, against SMALL = 6.6e6;
  * leaked s1: n = 16, range 1.42e8-2.86e8, so the tightest margin is 21.6x;
  * control s2: 2.84e8-4.30e8;
  * the gap rows: the probe records about 13,000x. I did not re-measure that.

  Four lanes ran three batches here, and no row went red that was not predicted.

**(b) The walk, from the device's own log** (`census_analyze.out`, sessions S25-S28 = `tl lb/sb/lh/sh`; S25 shown):

    A len=8 rel=0x38 latch=0 time=0x0      s0's ld: odata = 0 read FIRST (:279), then the TIME arm's update:
    T acc  last0=0 ... t1=0                   last_us == 0 -> latched, delta 0, nothing added
    T tick last0=..533524 now=..533535 t1=726  the first-step tick (machine.c:726-737, ticks_till_next starts at 0): +66 x 11 us
    A len=1 rel=0x7  latch=0 time=0x2d6    the +0x07 refusal: declined, NO T line
    A len=1 rel=0x38 latch=1 time=0x2d6    the refusal at CRIME_TIME: declined, NO T line
    A len=8 rel=0x38 latch=1 time=0x2d6    s1's ld: returns 0x2d6 = 726 = the tick's value (the probe printed `raw 726`)
    T acc  ... t1=429351780                   ...then its own update adds 66 x 6.5 s
    A len=8 rel=0x38 latch=1 time=0x19976364  s2 = 429351780
    T tick x2 (after every print)          cpu_run_deinit at `quit' (cpus/cpu.c:404-416)

`crime_update_crime_time()` has exactly two callers, the TIME arm (`:393`) and `dev_crime_tick` (`:188`) -- grep of the
whole tree. So on a fix build s1 is the tick's value by construction. Table 14's base printed 66/66/132/66; the census
build, which logs to a file, printed 726/792/726/594 because its tick lands 9-12 us after the access. **The premise as
written is FALSE in one word:** there are three CRIME ticks per stepped session (56 of 56, `census_facts.out`), not one.
`cpu_run_deinit()`'s own comment names them: "Two last ticks of every hardware device". It fires every device's tick
function twice. Both come after `quit`, which is after every `print`, so no row is affected. The 10 free-running
sessions see 40,000-58,000 ticks each.

**(c)** Measured in table 14's own logs: `M5_revlatch` and `M1_gotolatch` read pc = 0x80004000 on `rl lb`, `rl lh`,
`rl sb` and `rl sh` alike. `:344` tests only `cpu->pc`, and the lh and write cells redirect exactly as the lb does.

**(d)** Built and measured with one session per cell (`disc/dog_*.out`). The session writes 0x0200 then 0x0201 at +0x08,
optionally after a refusal, and reports the CONTROL texts and their values. Base prints 1 text (0x1) in all three
sessions.

    D_nodogclear (t14)   2/2/2  (0x200, 0x201)          -- the pair's mutant
    D_doglen8            sw 2, sd 1, sw+latch 2         -- escaped the 204 rows and killed by `ctldog sw msg' (DERIVED:
                                                           that row's session is this one minus the RAM trip; no probe run)
    D_doglatch           1 / 1 / 2 (only latch SET)     -- escapes the 218: the pair runs latch CLEAR
    D_dogbit0            1 / 1 / 1, value 0x201 not 0x1 -- escapes the 218: every row counts, none reads the value
    D_dogstopwiden       identical to base, CPU runs on  -- EQUIVALENT (DOG is cleared at :362 before :364 tests it)

The brief named three other shapes. A **re-arm in the DOG branch** is killed by `rearm once`: S36 writes 0x0201 and
0x0200 with the latch SET, and each is followed by a refusal. **DOG suppressing the residue print** (e.g.
`idata = 0` in the branch) takes 0x0201's print away, which reds `p acc ctl msg` (4 -> 2) and both `ctldog` rows (1 -> 0).
That one is by reading; I did not build it. **"DOG treated as a stop bit"** is live only if it acts inside the DOG
branch or ahead of it; the widening PRETABLE14 gives as its example is dead code. A live stop at 0x0200 stops the CPU in
`rearm`/`latch x5` (`rearm surv`/`latch surv`), and in `ctldog` the 0x0201 twin then never runs (count 0).

**(e)** `switch (relative_addr)` names 0x00, 0x08, 0x10, 0x18, 0x30 and 0x38. A narrow access anywhere else lands in
`default:`, which is `debug()` only. `odata` is never written for a narrow access, so a fall-through read still answers
0, and the v0 rows cannot see any suppression. The observable effects and their conditions:

* REV: pc = ra, only from 0xbfc051xx (`:344`).
* CONTROL: writes only (`:356`). HARD_RESET stops the CPUs; otherwise there is only host text for a nonzero residue.
* INTSTAT/INTMASK: `crime_interrupt_reassert()` is observable only when it CHANGES the line (`:118` raise, `:120` lower).
  In the census, every refused access at 0x10/0x18 ran with prev_asserted = 0. S18/S19 ran with SOFTINT = INTMASK =
  0x0101010111010101; the free-running S46/S47 ran with both at 0. So the raise is covered and **the lower is never
  exercised**. The discriminator shows that even the plain M6
  (= `P_ist_set`) lowers IP2 when the line is up. The rows kill M6 only through the raise.
* TIME: an update, visible at the next accepted read.

## 4. Q2 -- THE SWEEP AND ITS DENOMINATOR

**The ruled floor** is {observable label} x {latch SET}, discharged by the label-swap variant. It is **CLOSED**: M6, M7,
M8, M3 and M5 are killed in table 14 (215, 215, 215, 214 and 214 of 218), and my re-derived `P_ist_set`/`P_imk_set` are
byte-identical to M6/M7.

**The contract's own claim is wider.** The probe header, item 3 (`crime_width_probe.table14.py:52`): "every observable
label carries the whole {1,2} x {R,W} refusal floor". Repair 15's block (`:896-898`): "All four narrow ops at each
label ... the four are the width x direction cells a leak keyed on either could use". Crossed with the latch axis the
ruling added, that is the 36-cell table below. **MEASURED** by the census of a full 218/218 run, 66 sessions, the
latch state being the device's own `d->warned` at entry:

    label       1R-CLR   1R-SET   1W-CLR   1W-SET   2R-CLR   2R-SET   2W-CLR       2W-SET          exercised
    REV (win)   S14 S51  S29      S16      S31      S15      S30      S17          S32             8/8
    CONTROL     (reads: arm acts only on writes -- EQUIVALENT)  1W CLR/SET: S12/S12   2W CLR/SET: S11 S13 S44/S13 S20  4/4
    INTSTAT     S19 S46  --       --       S19      --       S19      --           S19             4/8
    INTMASK     S18 S47  --       --       S18      --       S18      --           S18             4/8
    TIME        S21 S49  S25 S40 S50  S22  S26      S23      S27 S40  S24          S28             8/8
    (S45/S50's REV refusals run from CODE, where the arm is inert; S40/S50's TIME refusals have no TIME sample after)

**The 8 empty cells are all at INTSTAT/INTMASK:** 1R with the latch SET, and 1W, 2R and 2W with the latch CLEAR. The
latch-CLEAR half is the sharper finding. There, not even the SINGLE-axis marginals are carried: `C_istW_clr` and
`C_imk2_clr` are one-conjunct narrowings. That is the shape of the F2 pass's `len != 2 || relative_addr != CRIME_INTSTAT`,
which the probe records (item 3) as having forced the 2-byte cells, plus a latch conjunct. In the latch-SET state every
single-axis marginal is carried, and only the (1, R) joint is empty.

**How to grade it** (a reading; the adjudicators rule):

* **By the ruling's letter it is clause (e).** Width and direction are not partitioned at the decline (`len` is only
  "not 8, not 4" there, and `writeflag` is not tested), so any width- or direction-keyed exemption is a joint.
  PRETABLE14's SIBLING PARITY check saw half of this, the latch-SET 1R pair, and disposed it exactly so
  (`PRETABLE14.out:117-124`). The same reasoning covers the six latch-CLEAR cells, but **nobody named them**.
* **By the probe's own text they are owed, or the text is a wrong record.** Item 3 (`:52`) and the repair-15 comment
  (`:896-898`) claim the {1,2}x{R,W} floor at every observable label. The only place that says it is latch-agnostic is PRETABLE14.out, and **the contract
  block in the probe (section 5 of the brief) discloses neither half**. As shipped, a reader of the contract believes
  INTSTAT/INTMASK carry all four cells in the sense TIME/REV now do. The project's own precedent (the F2 2-byte cells)
  rowed a label x width narrowing rather than disclosing it.
* **If owed, the cheapest closure is 6 new sessions.** One per latch-CLEAR cell at INTSTAT/INTMASK, since a session has
  only one first refusal. The two latch-SET 1R cells ride in two of them, after that first refusal. Each session carries
  the `pre`/`ctl` controls the istat/imask sessions use, and costs about 8-10 s. **If clause (e),** the probe's contract
  block must name the 8 cells and cite these runs.

**The other shapes measured** are all clause (e) by my reading, and are listed so a disclosure can name them:

* `P_ctl2wrc_set`: 2W x HARD_RESET-clear at CONTROL, latch SET. The only effect is host text, and every latch-SET 2W
  write in the probe carries 0x0800.
* `P_istprev_set`: INTSTAT, latch SET, falling through only while the line is already asserted. It scores 218/218
  because no refused access at 0x10/0x18 ever runs with `prev_asserted = 1`. It is a callee-state joint, which the Q3
  bound excludes, but its effect is guest-visible (IP2 dropped).
* `D_doglatch` scores 218/218. It is the "latch x DOG joint" the contract already discloses. Its only effect, the 0x0200
  text with the latch SET, sits in S36, where no row counts CONTROL text.
* `D_dogbit0` scores 218/218. It is a DOG x bit-0 idata joint: the count is unchanged and only the residue VALUE moves.

**Considered, NOT built, with the reason:**

1. **The latch-CLEAR plain label swap** at each label is killed by derivation: every observable label has a rowed
   latch-CLEAR refusal (table above), and `C_ist1r_clr` is the measured positive control for the shape.
2. **Width-only or direction-only narrowings of the latch-SET swap** are killed by derivation: every single-axis value is
   carried by a rowed latch-SET refusal at all five labels (table).
3. **CONTROL read-side exemptions** are EQUIVALENT (`:356`). CONTROL 2R-CLEAR is the one unexercised CONTROL cell, and it
   is one of these.
4. **REV exemptions outside the window** are EQUIVALENT (`:344`).
5. **DOG** is EQUIVALENT (`break;`). **`default`** is host text only. A latch-SET default exemption keyed on address bits
   7-8 clear would escape `mid nodflt`, whose latch-SET refusals all set those bits. It is clause (e) by the contract's
   own DOG/default disclosure.
6. **HARDINT-keyed label swaps** at INTSTAT/INTMASK/TIME/REV score 218/218 by construction: the only refusals with
   HARDINT != 0 are S20's three, all at CONTROL (`census_facts.out`). This is the same class as `P_istprev_set`.
7. **pc-keyed swaps at the non-REV labels** score 218/218 by construction: every refusal at TIME/INTSTAT/INTMASK/CONTROL
   runs from CODE. Those arms never read the pc, so it is not an axis under the DEPENDS-ON bound.
8. **Configuration-keyed swaps** (`use_fb`, RAM size) are dead code on `-M 64` non-graphics ip32. They are unrowable on
   one machine, which is the contract's existing class.
9. **TIME exemptions keyed on TIME or last_us values** leave nothing to row. The arm's own partitions are
   `last_us == 0`, never true at a latch-SET refusal (the first-step tick sets it in 56 of 56 sessions), and
   `delta < 0`, which is the host clock.
10. **`D_doglen8` and `D_dogstopwiden`** are built and discriminator-measured but NOT run through the probe. The first is
    predicted killed (`ctldog sw msg` only); the second is equivalent.
11. **The composite `D_nodogclear` + a latch on the CONTROL text** is two edits, outside the licensed multi-part shapes.
    Its latch half alone is killed by `p acc ctl msg` (4 -> 1).

## 5. Q3

The ruling's conditional ("if a body-tested-partition mutant escapes -> L2, IN as the pair") is met exactly. Table 14
reds only the pair under `D_nodogclear`, and sessions are independent, so it was 204/204 on the old rows. The pair is
the right member **of the two the ruling offered**, and its channel is sound. The measured DOG builds that print for
0x0200 read 2, never 1. A ONE with 0x0200 printed needs the 0x0201 twin's print lost as well, and that is a second
defect `p acc ctl msg` already counts. A dead channel reads 0 and a torn transcript reads `unclean`; both are red.

**Two members neither the ruling nor the brief named:**

* **Count rows on the existing ACCEPTS sessions.** S36 (`rearm`) holds all ten accepted CONTROL writes with the latch
  SET, 0x0200 at both widths included, and S50 (`latch x5`) holds them with the latch CLEAR (`accepts_ctl_writes.out`).
  Adding a CONTROL-text count to those two sessions changes no command list, needs no new session, and pins entries
  13/17 in BOTH latch states. The pair covers only latch CLEAR. Replay-measured with the probe's own command lists
  (`replay/`, all clean, one `-- declined.` each), as `rearm`/`latch x5`:

      base 4/4    D_nodogclear 6/6    D_doglatch 6/4    D_doglen8 5/5

  All four are exactly as pre-registered. **Cost:** the want is an aggregate over ten writes, and every future ACCEPTS
  edit moves it.
* **A value-anchored text** in the pair itself: `unimplemented control 0x0000000000000001` rather than the prefix. It
  kills `D_dogbit0` (measured: 0x201 printed where base prints 0x1, at both widths and in both latch states) at zero
  session cost. That is clause (f) applied to text: the count is a relative observable and the value is an anchored one.

## 6. Q4

Every leg matches its pre-registered red set, score and CRIMEP_CONTROL: 18 of 18 (`q4_check.out`). I parsed
PRETABLE14's block and each raw log's `FAIL` row lines, not `check14.py` and not the FAILING summaries. My first parser
run showed one "mismatch", which was my own parser attaching M1's continuation lines to the leg above; the fixed parser
agrees. No leg reds a row its hunk cannot reach. Two examples: `G_clr_imk4r`'s `gate line` is the 4R `lw +0x18` in S20
with the latch CLEAR (census), and `M3`'s four are exactly the four latch-SET TIME refusals with a sample after them
(S25-S28).

## 7. FOUND WHILE VERIFYING

1. **The brief's section 2 says TIME's latch-SET refusal happens in "the one session ... (`latch x5`)". There are two.**
   S40, the `dog` session, refuses `lb +0x38` and `lh +0x38` with the latch SET, after `lb +0x30`. Its rows are answer
   rows (`time sd lb v0`, `time sd lh v0`) with no TIME sample after, so the conclusion (no channel) stands and the count
   does not.
2. **"Exactly ONE CRIME tick per probe session" is false: there are three** (section 3b). It is harmless for every row
   today. But a future row that counts text printed after `quit` would also see the output of those two ticks, and they
   fire for every device, not only CRIME.
3. **PRETABLE14's "DOG -> stop" example is an equivalent mutant.** PRETABLE14 is not to be edited, but POSTTABLE or the
   records should not repeat it.
4. **The gate pin is THREE lines, not one:** `regress/gate_arm.sh:1916`, `:1921` and `:1922` all read 204. The gate's
   own comment already warns about exactly these siblings.
5. **Even the plain M6 is killed only through the raise direction** (section 3e). A future edit that keeps the raise and
   breaks the lower would not be seen.

## 8. WHAT I DID NOT OR COULD NOT DO

* I did not run a plain base leg of the probe in this environment. `restored` is byte-identical to table 14's base
  (218/218); the census leg (base plus logging) read 218/218.
* Batches 1 and 2 had no pre-written prediction file (section 1).
* `D_doglen8`, `D_dogstopwiden`, and the DOG-residue-suppression and composite shapes did not get full probe runs.
  `D_doglen8` is measured by discriminator and ACCEPTS replay only, and its `ctldog sw msg` kill is derived.
  `D_dogstopwiden` is equivalent by discriminator, not by binary identity: its binary differs (0d5e13fc).
* No HARDINT-, pc- or configuration-keyed mutant was built; their escapes follow from the census, not from runs.
* The census and discriminators use my copies of the probe's helpers (verbatim `session()`), not the probe itself.
* I read the Fable re-ruling, the repair-14 ruling, PRETABLE14, POSTTABLE14 and the table-14 logs. I did not read the
  other seats' pass-2 answers.

## 9. RESTORE

Checked after the last run:

* `/tmp/gxopus_r15p2/src/devices/dev_sgi_ip32.c` is `cmp`-CLEAN against
  `/mnt/c/DocumentNoSnc/cc/GXEMUL/GXEMUL-SEC/src/devices/dev_sgi_ip32.c` (md5 8c1d1545).
* Its binary is newer than the source and byte-identical to `/tmp/gxopus_r14_bins14/base`.
* There is no `.MUTANT` in either clone.
* `/tmp/gxopus_r14` was never written: its `dev_sgi_ip32.c` is still `cmp`-clean and it has no sentinel.

Nothing under `C:\DocumentNoSnc\cc\GXEMUL` was written except this directory. The mutant binaries in
`/tmp/gxopus_r15p2_bins/` are volatile; the durable evidence is `runs/`, `disc/`, `replay/`, `mutants/` and the census
files here.
