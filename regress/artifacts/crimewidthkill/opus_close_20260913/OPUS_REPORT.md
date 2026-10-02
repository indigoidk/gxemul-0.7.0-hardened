# #529 crimewidthkill -- CLOSING PASS, Opus compile-and-measure seat (2026-09-13)

Liveness token: `OPUS_CRIME_CLOSE_20260913`

**VERDICT: `GAP: goto crime_declined;` -> `if (!d->reg[CRIME_HARDINT / sizeof(uint64_t)]) goto crime_declined;`**
(the whole decline switched off while a hardware interrupt is latched: 85/85, and a guest-only session shows a refused
`sh 0x0800 +0x08` stopping every CPU). A second, independent gap has the cleanest warrant of all:
**`d->warned = 0;` as the first statement of `} else if (len == 4) {`** (85/85) -- the width-sibling of the ACCEPTED
F2 `rearm` finding, whose repair row only ever makes 8-byte accesses.

## Apparatus

* Scratch clone `/tmp/gxopus529close` (a `cp -a` of `/tmp/gxopuscrime`). `dev_sgi_ip32.c` `cmp`-CLEAN against the SEC
  working set (the uncommitted #529 fix, md5 `8c1d1545...`). Baseline rebuilt in the clone, `gxemul -nt source`.
  Sentinel `.MUTANT` held during both build batches. After each batch: source `cmp` clean, binary `-nt` source, rebuilt
  binary byte-identical to the baseline, then the sentinel was removed. The clone has been DELETED. `/tmp/gxopuscrime`,
  GXEMUL-SEC, build/, build-asan/, est/ and /tmp/gxsec-build were not touched. Nothing ran concurrently (checked).
* Instrument: the SHIPPED `regress/crime_width_probe.py`, frozen at `/tmp/crime_close.FROZEN.py`. Its md5
  `ac5bdb8096db06685c22d8645b0d6430` matches the shipped file and table 3's `crime_width_probe.table3.py`.
  One probe run at a time; each took about 335 s. **All 15 logs end `CRIMEP_DONE`** (`logs/probe_*.raw`).
* Mutants: `mutants_close.py`. Every find-text must occur exactly once, so a find that matches nothing FAILS rather than
  doing nothing. The diffs are in `logs/<m>.diff` and the binaries' md5s in `logs/BINARIES.md5`. Every build was rc 0
  with a fresh object and a distinct binary.
* Discriminators: `disc_close.py`, one guest-only session per survivor, run on base AND mutant with the same script, on
  unmodified `-E sgi -e ip32 -M 64` through the probe's own apparatus (copied). Output is in `logs/disc_close.out`.
* `PRETABLE.out` holds my predictions, written before any mutant run. **Disclosure about its timestamp:** I appended
  the two state-gated mutants at 11:25:03, which moved the file's mtime past `probe_base.raw` (11:24:53). The base
  prediction (85/85) was on disk before the base run started. Every mutant log's mtime is after 11:25:03.

## Table (the 85-row instrument) -- `table_close.out`

| mutant | edit | score | rows red | predicted | discriminator (base -> mutant) |
|---|---|---|---|---|---|
| base | -- | 85/85 CONTROL=OK | none | yes | |
| **lt_len** (spot-check) | latch set `\|= len` | **84/85** | latch x5 | yes | |
| **c_dog** (spot-check) | goto kept unless CONTROL && DOG | **83/85** | sh08b msg, sh08b run | yes | |
| lt_wl | latch bit keyed on writeflag AND len | 83/85 | latch x5, warm once | yes | DETECTED |
| **hi_gate** | `if (!d->reg[CRIME_HARDINT/8]) goto crime_declined;` | **85/85** | none | yes | HARDINT=0x20 (guest-set via MACE); refused sh 0x0800 +0x08: v1 0x12345678 -> **0xdeadbeef (CPUs stopped)** |
| **pa_gate** | `if (!d->prev_asserted) goto crime_declined;` | **85/85** | none | yes | IP2 asserted by SOFTINT+INTMASK; same sh: v1 -> **0xdeadbeef** |
| **rearm4** | `d->warned = 0;` first in `len == 4` branch | **85/85** | none | yes | refused, accepted lw, refused: notices 1 -> **2** |
| **pre4** | `d->warned \|= CRIME_W_LEN;` first in `len == 4` branch | **85/85** | none | yes | accepted lw, refused: notices 1 -> **0** |
| rearm_time | `d->warned = 0;` in `case CRIME_TIME` | 85/85 | none | yes | refused, accepted ld +0x38, refused: 1 -> **2** |
| ctl_collide | CONTROL's fatal latched on CRIME_W_LEN (a future bit collision) | 85/85 | none | yes | accepted sw 0x01 +0x08, refused: notices 1 -> **0** |
| wst_mc2 | refused 2-byte WRITE >= 0x200 lands | 85/85 | none | yes | sh 0xbeef +0x27e, ld +0x278: 0x0 -> **0xbeef** |
| rd_hi | refused READ >= 0x200 answers the register | 85/85 | none | yes | lbu +0x217: 0x0 -> **0x1** |
| lt_blk | latch bit `<< (relative_addr >= 0x200)` | 85/85 | none | yes | lb +7 then sb +0x27f: notices 1 -> **2** |
| wnz_lbl | fall-through for a NONZERO write at INTSTAT/INTMASK/TIME | 85/85 | none | yes | refused sb 0x01 +0x18 after the imask setup: cause 0x0 -> **0x400** |
| acc4_210 | `len == 4 && relative_addr != 0x210` | 85/85 | none | yes | lw +0x210: notices 0 -> **1** (value 0 both) |

Every one of the 15 outcomes matches its written prediction. **No survivor is EQUIVALENT:** each of the 11 has a
differing guest-visible or host-visible observable.

## Q1 -- floor gaps (most severe first), with why no row can see them

1. **hi_gate: the decline gated on HARDINT. A FLOOR breach, I argue.** HARDINT is a device-state lvalue that the fix's
   OWN repair path reads: the tail the goto targets restores and recomputes from it. By the TxICR ruling, the floor
   crosses the guard with the state lvalues the repair path reads, and reachability comes from the writers. HARDINT's
   writers are `crime_interrupt_assert/deassert`, which MACE, MEC and PCI drive. A guest reaches HARDINT != 0 with two
   MACE stores (`sd 1` to `0xbf310010`, then to `0xbf310018`). **Every refusal in all 85 rows runs with HARDINT == 0**,
   so a single conjunct on it sweeps the table.
   * The effect: while any hardware interrupt is pending (routine in a running OS), a refused `sh 0x0800` at +0x08
     stops every CPU. The whole switch is restored: REV pc hack, reassert, TIME, default-arm text.
   * The notice still prints, because the latch runs before the goto. So the one piece a row can see stays green
     while the decline is gone.
   * **pa_gate is the same shape on `prev_asserted`.** That field is read only in the callee
     `crime_interrupt_reassert`, so it is outside the DEPENDS-ON "never into callees" bound: coverage debt by the
     letter. But it is the same hole in the same rows, and one repair covers both.
2. **rearm4 / pre4: the latch's state-across-calls rows cover only the 8-byte accept path.** Width (8 / 4 / else) is
   the function's own top-level tested partition. The accepted F2 `rearm` mutant sat in `if (len == 8)`, and `warm`
   makes only 8-byte accesses (sd, ld, ld). The `len == 4` cell was left open: `#499`'s "repaired at exactly the
   address the mutant used" shape, reproduced inside the repair for my own F2 findings.
   * rearm4 means one announce per narrow access interleaved with normal 32-bit traffic: the flood the latch exists
     to stop.
   * pre4 means the notice is silenced by the first 32-bit CRIME access. The PROM's first CRIME access is an `lw` at
     CRIME_REV, so on a real boot the notice would never print.
   * pre4's 8-byte twin IS caught, but only because `warm` happens to seed DOG with an `sd` first.
3. **Label-keyed latch writers: rearm_time, and ctl_collide (the "future second bit" shape).** `warm` touches only
   the DOG label. A re-arm or pre-set at any other arm (TIME, INTSTAT/INTMASK, REV, CONTROL, default) is invisible.
   * ctl_collide is the plausible future edit: a `crimectllane` round latching CONTROL's unimplemented-control text
     with a bit that equals CRIME_W_LEN.
   * No row can see these because no session that COUNTS announces has an accepted access at those labels between or
     before its refusals. The time and imask sessions have such accesses, but they do not count announces.
4. **The >= 0x200 partition: wst_mc2, rd_hi, lt_blk.** My F2 finding (`wst_mc`: a store landing only at >= 0x200) was
   accepted, and its repair `hi keeps` rows only (1-byte, write).
   * No refused READ, and no refused 2-byte access, happens at >= 0x200 anywhere. No session has refusals on both
     sides of 0x200.
   * **Hardest on my own finding:** 0x200 is NOT a partition the body tests. It is the header comment's hardware
     block boundary, and the prelude writes 0x208..0x240. So either `hi keeps` was owed, and its three siblings are
     owed too, or it was single-partition coverage debt, and CONTRACT 7's credit ("Opus, F2") should say so. The
     record cannot hold both. I lean to DEBT: this is the weakest of my F2 findings.
5. **Value debt (clause (e) by the carrier's rule, but UNDISCLOSED): wnz_lbl.** Every refused store at INTSTAT,
   INTMASK and TIME writes 0, so a fall-through keyed on a nonzero write escapes. The arms there do not test idata,
   which is why this is (e). Still, the rows could write nonzero at no cost.
6. **acc4_210:** a records point, see Q3.

**Cheapest repair covering 1-3:** one extra session, no new channel. It reuses the rows' own idioms:
* **(a)** two MACE stores to latch HARDINT, `print` HARDINT (want 0x20: a control that the state was reached), then a
  refused `sh 0x0a00 +0x08` plus a RAM trip. Want LIVE; hi_gate gives SENT. Then an accepted `lw +0x18` with INTMASK
  enabling a line. That asserts IP2, which is pa_gate's state.
* **(b)** in the counted `warm` session, add an accepted `lw` before the first refusal and between refusals. Add one
  accepted access per remaining label (REV off-window, CONTROL `sw 0x01`, INTSTAT, INTMASK, TIME, default +0x20),
  still wanting exactly one announce.

I have NOT built that repair, so its kill of each mutant is predicted, not measured.

**Shapes the brief named that are NOT gaps:**
* **A byte at CONTROL cannot carry a tested bit.** `memory_readmax64(len=1)` gives 0..0xff. DOG is 0x200, RESET 0x800
  and ENDIANESS 0x100, and bytes at 0x09..0x0f reach the default arm, not the CONTROL label. The only tested
  predicate a byte can reach is residual != 0, which `sb08 msg` rows with 0x01.
* **The HARDINT restore after an accepted HARDINT write is EQUIVALENT by construction.** The tail already undoes an
  accepted `sd +0x28`, so the refused access that follows sees an unchanged HARDINT. For the same reason, a refused
  store that lands at +0x10..0x17 or +0x28..0x2f is overwritten by the tail's recompute and restore. A store landing
  at REV, CONTROL or bank control is rewritten by the prelude before any read. These are reasoned, not built.
* **The notice keyed on writeflag AND len is detected:** lt_wl, 83/85.

## Q2 -- is the repair diff sound?

* Every row I exercised can vary. The two spot-checks redden exactly the rows the record claims.
* `dflt()` keyed on the access's own offset and direction is sound: the default arm prints the refused access's own
  `relative_addr`.
* **The TIME comment misstates its mechanism, and the rows are fine.** `machine.c` sets `ticks_till_next[n] = 0` at
  registration, and `machine_run` decrements and fires the tick at <= 0. So **the first CRIME tick fires in the same
  `machine_run` call as the session's first instruction, the first `ld`**. That tick is what adds the 66/132 the rows
  print.
  * "Nothing else updates TIME before the next ld" is therefore false as written.
  * The disclosed "ASSUMPTION: no tick boundary falls between the first ld and the refused access" is also false as
    written, because one always does, microseconds after the ld. The window that matters also runs to the s1 `ld`,
    not just to the refused access.
  * The true invariant is structural, not assumed: one tick right after instruction 1, and the next one 16383 steps
    later.
  * Measured this pass: s1 raw is 66-990 across 52 cells, against SMALL = 6.6e6. That is a margin of more than
    6,600x, and the controls read about 2.8e8.
  * **Not measured on a loaded host.** Other seats may be running, so I skipped it. By construction, load only
    raises the fall-through and control readings. Making s1 cross SMALL needs a stall of more than 100 ms inside one
    `machine_run` call.
* The imask design depends on the same first tick firing BEFORE the SOFTINT store. It does, because `sd +0x18` is
  instruction 1. That dependence is unstated.

## Q3 -- statements that are wrong

1. **CONTRACT 8 / the F2 table's `rearm` row:** "an accepted access between two refusals does not re-arm the
   announce". That is true only for an 8-byte access at DOG. rearm4 and rearm_time measure 85/85.
2. **CONTRACT 7 / the F2 row "a refused store landing only >= 0x200 -> hi keeps":** that is true for 1-byte stores
   only (wst_mc2 85/85). Refused reads at >= 0x200 are not covered either (rd_hi).
3. **CONTRACT 4:** "keyed on the access (its bit taken from len, relative_addr or writeflag)". That is true for those
   three exact forms. An address-block key escapes (lt_blk).
4. **CONTRACT 3's closing claim, and the DENOMINATOR:** "every observable label carries the whole {1,2} x {R,W}
   refusal floor". That holds only in ONE device state (HARDINT == 0, line deasserted). hi_gate and pa_gate measure
   85/85.
5. **DISCLOSED's "ACCEPT cells at offsets other than +0x30, +0x210 and +0x278":** at +0x210 only 8R is rowed.
   acc4_210 (4-byte narrowed there) scores 85/85.
6. **The TIME comment's "nothing else updates TIME" and its ASSUMPTION sentence** (Q2).
7. The brief's "every red-row set in tables 2 and 3 was predicted in writing BEFORE the table ran" is supported by
   mtime for table 3: PRETABLE at 08:26, first log at 08:36. I did not check table 2.

## What I could not measure

* The TIME rows under host load (skipped, to avoid disturbing other seats).
* The kill power of the repair I suggest.
* Real-guest frequency of HARDINT != 0 at a narrow access: argued from the wiring, not booted.
* Table 2's PRETABLE ordering.
