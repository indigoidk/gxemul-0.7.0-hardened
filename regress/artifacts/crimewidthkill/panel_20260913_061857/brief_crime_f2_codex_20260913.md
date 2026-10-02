This is a routine SOFTWARE-TESTING review of an open-source hardware emulator (GXemul) and its regression test.  Nothing here concerns real systems, networks or security: 'mutant' means a deliberately modified copy of the emulator's C source used to check that the regression test notices the change (standard mutation testing).

# §F2 ADJUDICATION PASS — `crimewidthkill` (#529): the panel shares its findings.  Liveness token `CRIME_F2_20260913`.

VERDICT LINE FIRST (`CLOSES` — the repaired detector has no floor breach — or `GAP: <exact source edit>`), then the token.

This is ordinary correctness review of an emulator device model and its regression test, and it is the THIRD pass: pass 2
answered blind; this packet shows every seat what every other seat found, with my disposition on each.  **Please do not
ratify** — question 2 below is the load-bearing one.  Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` only (any other
`src/` is an unmodified 2021 upstream copy).  File-reading seats: `src/devices/dev_sgi_ip32.c` (`DEVICE_ACCESS(crime)`),
`regress/crime_width_probe.py`, `regress/artifacts/crimewidthkill/` (killtable_20260913/, killtable2_20260913/,
opus_pass2_20260913/OPUS_REPORT.md).

## SETTLED PREMISES (recorded; re-stated because the questions depend on them)

* The fix: `DEVICE_ACCESS(crime)`'s width arm for `len` not 8 or 4 used to `fatal(...); exit(1);`.  It now announces once
  per device instance (`int warned`, bit `CRIME_W_LEN`, text `[ crime: unimplemented len=N at 0xA -- declined.  (once) ]`)
  and `goto crime_declined;` — past the register switch to the common tail, which answers a read 0
  (`memory_writemax64(cpu, data, len, odata)` with `odata` still 0) and returns 1.  No bus error.  Pass 1 ruled this shape
  (member 3; the `#498` `sgi_de` precedent) over FAULT.  Every pass-2 seat found the FIX correct; all findings below are
  about the DETECTOR and the RECORDS.
* `fatal()` never exits and is not verbosity-gated; `debug()` prints while single-stepping and is suppressed when the
  guest free-runs at default verbosity.
* `memory_rw.c` pre-zeroes a device read buffer (`#95`: `if (writeflag == MEM_READ)` / `memset(data, 0, len);` directly
  above `paddr -= mem->devices[i].baseaddr;`), so `goto crime_declined` and `return 1` are equivalent on a declined read.
* The switch arms a refused access would reach if it fell through: `CRIME_REV` (0x00, pc-window hack: `pc = ra` for any
  access from pc 0xbfc051xx, either direction), `CRIME_CONTROL` (0x08, writes only: HARD_RESET stops every CPU, an
  unmodelled bit prints an unlatched fatal), `CRIME_INTSTAT`/`CRIME_INTMASK` (0x10/0x18: `crime_interrupt_reassert()`),
  `CRIME_DOG` (0x30: `break;`), `CRIME_TIME` (0x38: `crime_update_crime_time()`), `default:` (a `debug()` line).

## THE FIX COMMENT, as corrected after pass 2 (the only product-code change since pass 2 — comment text only)

```c
		 *  The goto skips the register switch below, and that is the
		 *  point of it: falling through would let a halfword 0x0800
		 *  written at CRIME_CONTROL stop every CPU, a narrow access to
		 *  CRIME_REV from the PROM probe loop redirect the PC, one at
		 *  INTSTAT or INTMASK reassert the interrupt line, and one at
		 *  CRIME_TIME advance the clock -- all measured.  It is not
		 *  `return 0' either: that raises a guest bus error
		 *  (EXCEPTION_DBE, cpus/memory_rw.c), and what real CRIME does
		 *  on a narrow cycle is not documented here.
```

## FINDINGS F1..F18, with my disposition and what changed

| # | finding | raised by | disposition | change |
|---|---|---|---|---|
| F1 | POSTTABLE 1 "18 of 18 non-equivalent detected" is 17 of 17 (return1 is one of the 18 and equivalent); "17 of 18" in (a) is 16 of 17 | codex, grok, glm, kimi CLI, kimi-k3:cloud | ACCEPTED (L4) | corrected in place, the refuted text quoted |
| F2 | brief: "committed build 3/15, every row red" — the three green are controls; every REFUSAL row was red | grok, kimi CLI | ACCEPTED (records) | the CHANGELOG says "every refusal row" |
| F3 | the brief's reason for the goto — "the tail also restores HARDINT and recomputes INTSTAT" — is inert on the declined path (nothing writes HARDINT/SOFTINT between entry and tail) | glm, kimi CLI, codex; Opus measured `t_nohint` equivalent | ACCEPTED | the probe header now calls them identities; the house shape (`#498`) is the reason |
| F4 | the REV-store cell: `writeflag == MEM_READ \|\| relative_addr != CRIME_REV` passes 40/40 and a refused `sb`/`sh` at +0 from the PROM window sets pc = ra | codex, grok, glm; Opus MEASURED (`a_revw`) | ACCEPTED (L1: the detector is unshipped) | rows `sb rev pc`, `sh rev pc`; header and product comment say "access", not "read" |
| F5 | a fall-through at INTSTAT/INTMASK reasserts the IRQ line (cause.IP2 after a SOFTINT store); at TIME it advances the clock the next read shows — the probe's DISCLOSED "idempotent / overwritten / no observable" was FALSE | minimax named it; Opus MEASURED (`a_istat`, `a_imask`, `a_time`, `a_lo10` 40/40, undetected change probe shows IP2 / TIME ~1.4e8); codex, kimi CLI (TIME wording) | ACCEPTED (L1) | rows `imask/istat pre, lb, sb, ctl`, `time lb/sb (+ctl)`; the disclosure deleted; product comment names both |
| F6 | an address-keyed fall-through into the `default:` arm is unobserved | grok, minimax; Opus (`a_lo10` prints `[ crime: write to 0x1f ...]`) | ACCEPTED (L1) | rows `lb/lh/sb/sh nodflt`, `hi nodflt`, control `dflt ctl` |
| F7 | `fatal(` -> `debug(` passes: every session single-steps, and debug prints while stepping | codex | ACCEPTED (L1) | a FREE-RUNNING session (`continue`, then CTRL-C back to the prompt): `free said`, `free v0` |
| F8 | a refused store that LANDS has no row; "readback non-varying" was true of the candidates, not a protection | codex | ACCEPTED (L1) | `sb keeps`, `sh keeps` (CRIME_DOG seeded by an accepted `sd`) |
| F9 | `sb08 msg` stays green under `exit(0)` — it ignored its own session's round trip | codex | ACCEPTED (L1) | `sb08 run` |
| F10 | table 1's "confined" mutants each admit TWO refusal cells; no single-cell fall-through was measured | codex | ACCEPTED | `only1r/only2r/only1w/only2w` in table 2; POSTTABLE 1 corrected |
| F11 | every 8-byte (and 4-byte accept) row sits at CRIME_DOG: `len == 8 && relative_addr == CRIME_DOG` passes | kimi CLI; Opus MEASURED `x_mc4`/`x_mc8` (`< 0x200`) | ACCEPTED (L1) | accept rows at the window's LAST slot, +0x278: `top8 st+ld`, `top4 rhi`, `top4 rlo`, `top4 w` |
| F12 | an address-keyed announce (`relative_addr & 0x3f`, or `&& relative_addr < 0x40`) passes | kimi CLI; Opus MEASURED `l_addrmask` | ACCEPTED (L1) | a refused `sb` at +0x27f: `hi said` (exact `len=1 at 0x27f`), `hi nodflt`, `hi surv` |
| F13 | the `(once)` marker is never matched | codex; Opus MEASURED `l_noonce` | ACCEPTED (L1) | every `said` pattern includes `(once) ]` |
| F14 | TIME: "overwritten by the tail" is wrong for `last_microseconds` | codex, kimi CLI | ACCEPTED | subsumed by F5 |
| F15 | the function comment says CRIME maps 0x80 bytes; the device maps `DEV_CRIME_LENGTH` 0x280, so the decline also covers memory control (+0x208 announces `at 0x208`) | Opus | REFINED: upstream text describing the register block (it says memory control starts at 0x200); not changed in this round; the decline covering 0x200..0x27f is intended (same width arm) | the far-slot rows sit at +0x278/+0x27f, inside memory control |
| F16 | measured EQUIVALENT: tail label moved, `=` for `\|=`, a function-static latch (IP32 has one CRIME), `uint32_t` casts | Opus | ACCEPTED | disclosed (the static-latch one as: one instance per machine) |
| F17 | the inherited REV comment says "the second time" but there is no access counter | codex | REJECTED for this round: upstream text, unchanged by the fix | none |
| F18 | multi-instance latch independence unmeasured | codex | ACCEPTED as disclosure | header bullet |

## DISAGREEMENTS

* **D1 — are the INTSTAT / INTMASK / TIME fall-throughs observable?**  deepseek: *"The only pass-all variants are
  behavior-equivalent and do not break the fix."*  kimi-k3:cloud: *"the survivors are host-observable only (or not at
  all)."*  minimax: *"Both are guest-observable."*  The Opus seat MEASURED it: after `sd INTMASK = bit 28` and `sd
  SOFTINT = bit 28` (SOFTINT's store goes to the default arm and does NOT reassert), a refused access at the label sets
  cause.IP2 under the fall-through and not on the fix; an accepted `lw` there sets it (control).  TIME: an accepted `ld`
  returns the PREVIOUS update's value, so a refused access that updates TIME shows in the next read (~1.4e8 vs 66..132).
  **Ruling: observable, by measurement; rows added (F5).**  deepseek and kimi-k3:cloud — is anything wrong with the
  measurement as described?
* **D2 — is the address axis a FLOOR BREACH (L2) or coverage debt?**  Opus: *"Under the carrier's join rule, the skipped
  switch re-tests relative_addr, so INTSTAT, INTMASK and TIME are floor cells ... an L2 breach."*  grok: *"Address-
  conditioned fall-through is the hole POSTTABLE already named; PRETABLE §5 correctly filed the unrowed labels as clause
  (e). Do not promote it to L2."*  **Ruling: the licence is L1 either way — the detector has not shipped, so every row
  above is construction — but for the RECORD I side with Opus:** the join rule makes a dispatch label a floor axis when
  the body re-tests the selector after the join, and here the fix's own edit IS the skip of that dispatch; PRETABLE 1's
  §5 put INTSTAT/INTMASK/TIME in clause (e) on a "no observable" premise that was measured false, so it was a wrong
  disclosure, not a correct one.  grok — does that ruling hold?

## MUTATION-TEST TABLE 2 (targeted; on the repaired 71-row detector)

```
POSTTABLE -- #529 mutation-test table 2 (TARGETED), written AFTER the table (PRETABLE.out predates it by mtime)
Driver kill529b.run-*.sh (frozen); summary table2.out; per-run logs/probe_<m>.raw (new 71-row instrument) and
logs/probe_T1INSTR_<m>.raw (table 1's 40-row instrument) -- every one ends CRIMEP_DONE (checked); logs/<m>.diff;
builds/.  Instruments: crime_width_probe.table2.py (= regress/crime_width_probe.py as shipped, md5 in
logs/INSTRUMENT.md5) and ../killtable_20260913/crime_width_probe.table1.py.  Scratch clone /tmp/gxopuscrime, baseline =
the #529 working set with the pass-2 comment edit (BASELINE_CMP CLEAN), rebuilt in the clone; every mutant built rc 0
with a fresh object, none byte-identical to base; restored afterwards: cmp clean, binary -nt source, restored == base
byte-identical, sentinel removed.

NEW INSTRUMENT (71 rows)                                   ROWS REDDENED -- vs PRETABLE 2's prediction
    base        71/71  CONTROL=OK                          none                                          = predicted
    revwrite    69/71                                      sb rev pc, sh rev pc                          = predicted
    addrrc      60/71                                      lb/lh/sb/sh nodflt, hi nodflt, imask lb/sb,
                                                           istat lb/sb, time lb/sb                       = predicted
    mmreads     64/71                                      lb/lh nodflt, imask lb/sb, istat lb/sb, time lb = predicted
    fdebug      70/71                                      free said                                     = predicted
    wstore      68/71  CONTROL=FAIL                        sb keeps, sh keeps, imask ctl                 = predicted
    acc8dog     63/71  CONTROL=FAIL                        top8 st+ld, top4 rhi/rlo/w, imask ctl, istat ctl,
                                                           time lb ctl, time sb ctl                      = predicted
    acc4low     68/71                                      top4 rhi, top4 rlo, top4 w                    = predicted
    annlow      70/71                                      hi said                                       = predicted
    only1r      64/71                                      lb nodflt, lb rev pc, imask lb/sb, istat lb/sb,
                                                           time lb                                       = predicted
    only2r      69/71                                      lh nodflt, lh rev pc                          = predicted
    only1w      64/71                                      sb nodflt, sb08 msg, sb rev pc, imask sb,
                                                           istat sb, time sb, hi nodflt                  = predicted
    only2w      67/71                                      sh nodflt, sh08 pc, sh08 run, sh rev pc       = predicted
    timeft      69/71                                      time lb, time sb                              = predicted
    imaskft     69/71                                      imask lb, imask sb                            = predicted
    a_lo10      62/71                                      sb/sh nodflt, hi nodflt, imask lb/sb,
                                                           istat lb/sb, time lb/sb                       = predicted
    a_istat     69/71                                      istat lb, istat sb                            = predicted
    l_noonce    65/71                                      lb/lh/sb/sh said, hi said, free said          = predicted
    l_addrmask  70/71                                      hi said                                       = predicted
    x_mc4       68/71                                      top4 rhi, top4 rlo, top4 w                    = predicted
    x_mc8       67/71                                      top8 st+ld, top4 rhi, top4 rlo, top4 w        = predicted
    dogft       71/71                                      none -- PREDICTED SURVIVOR, EQUIVALENT (the DOG arm is `break;')
    ctlrdft     71/71                                      none -- PREDICTED SURVIVOR, EQUIVALENT (CONTROL acts only on writes)
    acc8mid     71/71                                      none -- PREDICTED SURVIVOR, disclosed coverage debt (interior slot)
  21 of 21 non-equivalent mutants DETECTED, every red-row set EXACTLY as PRETABLE 2 predicted; the 3 survivors are the 3
  predicted, each with its disposition in the probe header.  (Counted from the list above: 24 mutants + base; 21 + 3 = 24.)

TABLE-1 INSTRUMENT (40 rows) -- the pass-2 seats' claimed undetected changes, MEASURED
    addrrc 40/40   mmreads 40/40   fdebug 40/40   wstore 40/40   acc8dog 40/40   acc4low 40/40   annlow 40/40
  All seven went undetected the 40-row detector, as claimed (kimi CLI, grok, minimax, codex).  The Opus seat's own undetected changes
  (a_revw, a_lo10, a_imask, a_istat, a_time, x_mc4, x_mc8, l_addrmask, l_noonce) were measured 40/40 on the same
  instrument in opus_pass2_20260913/logs/ and are not repeated here.  Every undetected change of the 40-row detector is detected by
  the 71-row one.

THE CHANNEL LINE, checked as the mandate asks: PRETABLE 2 named each mutant's red rows at writing time and all 21 sets
were exact -- including the two that needed a trace through a whole session (wstore's `imask ctl': the refused sb +0x18
stores 0 into INTMASK, so the later accepted lw cannot reassert; acc8dog's four control rows).  Table 1's one miss
(acc8w, a sequential-session trace) was the lesson applied here.

DENOMINATOR, for the closing pass: the refusal cells {1,2} x {R,W}, each by a SINGLE-cell fall-through (only1r, only2r,
only1w, only2w) and jointly (table 1's len1only/len2only/readonly/wronly/fallsw); the switch labels by an address-keyed
fall-through at each observable one (REV both directions: revwrite, table 1's rev rows; CONTROL writes: table 1;
INTSTAT: a_istat; INTMASK: imaskft; TIME: timeft; the default arm: addrrc, mmreads, a_lo10) and at the two equivalent
ones (dogft, ctlrdft); the accept cells at both ends of the window (table 1's six at +0x30; acc8dog, acc4low, x_mc4,
x_mc8 at the far end); a refused store that lands (wstore); the announce's channel (fdebug), text (fmtswap, l_noonce,
l_addrmask, annlow) and latch (nolatch, latchinv); the dispositions (revert, fault, exit0, return1).  NOT swept, and
disclosed: an accept arm narrowed at an INTERIOR slot (acc8mid); two-cell refusal x label joints beyond the rows above.
```

## WHERE I MIGHT BE FOOLING MYSELF

* **I accepted sixteen of eighteen findings.** That is a suspicious number; agreement is not evidence.
* The TIME rows' `small`/`large` split depends on no device tick advancing TIME by a wall-clock-sized delta between the
  first `ld` and the refused access.  Ticks are counted in instructions (one per step while stepping), so this held in
  every run so far (66 or 132) — but it is a timing assumption, and it is the row most exposed to it.
* The free-running rows depend on CTRL-C delivered through the pty breaking back into the debugger; `free said` counts
  text printed after `continue` whether or not the break-in works, so it cannot be starved by the break-in failing —
  only `free v0` can.
* The new rows were written from the seats' findings; PRETABLE 2 predicts each mutant's red rows, and the table is the
  check on those predictions, not the rows' own wording.

## THE FIX, as it stands (`git diff` vs HEAD 9c91999)

```diff
diff --git a/src/devices/dev_sgi_ip32.c b/src/devices/dev_sgi_ip32.c
index fa96bf5..b8f4e11 100644
--- a/src/devices/dev_sgi_ip32.c
+++ b/src/devices/dev_sgi_ip32.c
@@ -82,8 +82,14 @@ struct crime_data {
 	int			prev_asserted;
 
 	int			use_fb;
+
+	/*  #529: warn-once latches for guest-drivable diagnostics, one bit
+	    per site and never shared.  memset(0) at init clears them.  */
+	int			warned;
 };
 
+#define	CRIME_W_LEN		(1 << 0)	/*  #529: the width decline  */
+
 
 void mips_pc_to_pointers(struct cpu *);
 void mips32_pc_to_pointers(struct cpu *);
@@ -288,8 +294,29 @@ DEVICE_ACCESS(crime)
 				odata = (int32_t)(odata >> 32);
 		}
 	} else {
-		fatal("crime access len = %i!\n", len);
-		exit(1);
+		/*
+		 *  #529: THIS USED TO END THE PROCESS.  One guest lb, lbu, lh,
+		 *  lhu, sb or sh anywhere in CRIME did it (witnessed at rung 3
+		 *  on an unmodified -E sgi -e ip32, 6/6).  The width is now
+		 *  DECLINED and announced once, the #498 sgi_de shape: a read
+		 *  is answered 0 through the common tail, a write is dropped.
+		 *
+		 *  The goto skips the register switch below, and that is the
+		 *  point of it: falling through would let a halfword 0x0800
+		 *  written at CRIME_CONTROL stop every CPU, a narrow access to
+		 *  CRIME_REV from the PROM probe loop redirect the PC, one at
+		 *  INTSTAT or INTMASK reassert the interrupt line, and one at
+		 *  CRIME_TIME advance the clock -- all measured.  It is not
+		 *  `return 0' either: that raises a guest bus error
+		 *  (EXCEPTION_DBE, cpus/memory_rw.c), and what real CRIME does
+		 *  on a narrow cycle is not documented here.
+		 */
+		if (!(d->warned & CRIME_W_LEN)) {
+			d->warned |= CRIME_W_LEN;
+			fatal("[ crime: unimplemented len=%i at 0x%x -- declined."
+			    "  (once) ]\n", (int) len, (int) relative_addr);
+		}
+		goto crime_declined;
 	}
 
 	switch (relative_addr) {
@@ -381,6 +408,9 @@ DEVICE_ACCESS(crime)
 		}
 	}
 
+ crime_declined:
+	/*  #529: a declined access jumps here, skipping the register switch,
+	    and is still answered.  */
 	d->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;
 	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
 		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
```

## THE WHOLE ENCLOSING FUNCTION (every exit path and the common tail)

```c
DEVICE_ACCESS(crime)
{
	/*
	 *  The CRIME is memory mapped as 0x80 bytes, starting at
	 *  physical 0x14000000.
	 *
	 *  On my real O2:
	 *
	 *  0x14000080..0x140000ff is the same as 0x14000000..0x1400007f.
	 *  0x14000100..0x1400017f is the same as 0x14000000..0x1400007f.
	 *  0x14000180..0x140001ff is the same as 0x14000000..0x1400007f.
	 *
	 *  (I assume that real code will never access the above "mirrors",
	 *  but it would be trivial to add redirection so that such code
	 *  would work too.)
	 *
	 *  Memory control then starts at 0x14000200.
	 */
	struct crime_data *d = (struct crime_data *) extra;
	uint64_t idata = 0, odata = 0;
	uint64_t preserved_CRIME_HARDINT = d->reg[CRIME_HARDINT / sizeof(uint64_t)];
	size_t i;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	/*
	 *  Set crime version/revision:
	 *
	 *  This might not be the most elegant or correct solution, but it
	 *  seems that the IP32 PROM likes 0x11 for machines without graphics,
	 *  and 0xa1 for machines with graphics.
	 *
	 *  NetBSD 2.0 complains about "unknown" crime for 0x11, but I guess
	 *  that's something one has to live with.  (TODO?)
	 */
	d->reg[CRIME_REV / sizeof(uint64_t)] = d->use_fb? 0xa1 : 0x11;

	d->reg[CRIME_CONTROL / sizeof(uint64_t)] = CRIME_CONTROL_ENDIANESS;

	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
		d->reg[CRIME_HARDINT / sizeof(uint64_t)]);

	/*
	 *  Amount of memory.  Bit 8 of bank control set ==> 128MB instead
	 *  of 32MB per bank (?)
	 *
	 *  According to OpenBSD, "Empty banks are reported as duplicates of
	 *  bank #0."
	 */
	if (cpu->machine->physical_ram_in_mb > 1024) {
		fatal("[ sgi_crime: SGI O2 can not have more than 1024 MB RAM ]\n");
		exit(1);
	}

	int mb_per_bank;
	if (cpu->machine->physical_ram_in_mb <= 256)
		mb_per_bank = 32;
	else
		mb_per_bank = 128;

	if (cpu->machine->physical_ram_in_mb % mb_per_bank) {
		fatal("[ sgi_crime: for up to 256 MB RAM, RAM size needs to be divisible "
			"by 32 MB. for larger RAM sizes (up to 1024 MB), it needs to be "
			"divisible by 128 MB. ]\n");
		exit(1);
	}

	int flag_for_128MB = mb_per_bank == 128 ? 0x100 : 0x000;
	size_t total_mb = 0;
	for (int bank = 0; bank < 8; ++bank) {
		int b = mb_per_bank == 128 ? (bank << 2) : bank;
		if (total_mb >= cpu->machine->physical_ram_in_mb)
			d->reg[CRIME_MEM_BANK_CTRL0 / sizeof(uint64_t) + bank] =
				d->reg[CRIME_MEM_BANK_CTRL0 / sizeof(uint64_t) + 0];
		else
			d->reg[CRIME_MEM_BANK_CTRL0 / sizeof(uint64_t) + bank] = flag_for_128MB | b;

		total_mb += mb_per_bank;
	}
	
	if (len == 8) {
		if (writeflag == MEM_WRITE)
			d->reg[relative_addr / 8] = idata;
		else
			odata = d->reg[relative_addr / 8];
	} else if (len == 4) {
		if (writeflag == MEM_WRITE) {
			if (relative_addr & 4) {
				d->reg[relative_addr / 8] &= ~0xffffffffULL;
				d->reg[relative_addr / 8] |= (uint32_t)idata;
			} else {
				d->reg[relative_addr / 8] &= 0xffffffffULL;
				d->reg[relative_addr / 8] |= (uint64_t)(idata << 32ULL);
			}
		} else {
			odata = d->reg[relative_addr / 8];
			if (relative_addr & 4)
				odata = (int32_t)odata;
			else
				odata = (int32_t)(odata >> 32);
		}
	} else {
		/*
		 *  #529: THIS USED TO END THE PROCESS.  One guest lb, lbu, lh,
		 *  lhu, sb or sh anywhere in CRIME did it (witnessed at rung 3
		 *  on an unmodified -E sgi -e ip32, 6/6).  The width is now
		 *  DECLINED and announced once, the #498 sgi_de shape: a read
		 *  is answered 0 through the common tail, a write is dropped.
		 *
		 *  The goto skips the register switch below, and that is the
		 *  point of it: falling through would let a halfword 0x0800
		 *  written at CRIME_CONTROL stop every CPU, a narrow access to
		 *  CRIME_REV from the PROM probe loop redirect the PC, one at
		 *  INTSTAT or INTMASK reassert the interrupt line, and one at
		 *  CRIME_TIME advance the clock -- all measured.  It is not
		 *  `return 0' either: that raises a guest bus error
		 *  (EXCEPTION_DBE, cpus/memory_rw.c), and what real CRIME does
		 *  on a narrow cycle is not documented here.
		 */
		if (!(d->warned & CRIME_W_LEN)) {
			d->warned |= CRIME_W_LEN;
			fatal("[ crime: unimplemented len=%i at 0x%x -- declined."
			    "  (once) ]\n", (int) len, (int) relative_addr);
		}
		goto crime_declined;
	}

	switch (relative_addr) {

	case CRIME_REV:		/*  0x000  */
		/*
		 *  A contender for winning a prize for the worst hack
		 *  in history:  the IP32 PROM probes the CPU caches during
		 *  bootup, but they are not really emulated, so it fails.
		 *  During the probe, the CRIME_REV is read a lot. By
		 *  "returning" from the probe function, i.e. jumping to ra,
		 *  when this register is read the second time, the probe
		 *  can be skipped, and the PROM thus runs further.
		 *
		 *  The address where this happens is:
		 *	0xbfc0517c	PROM v2.3
		 *	0xbfc051ac	PROM v4.13
		 *
		 *  4.18 works too.
		 *
		 *  By extrapolating a bit (allowing for variations for other
		 *  versions of the PROM), let's return if the read of the
		 *  CRIME_REV register occurs anywhere near 0xbfc051XX.
		 */
		if (((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100) {
			cpu->pc = cpu->cd.mips.gpr[MIPS_GPR_RA];
			if (cpu->is_32bit)
				mips32_pc_to_pointers(cpu);
			else
				mips_pc_to_pointers(cpu);
		}
		break;

	case CRIME_CONTROL:	/*  0x008  */
		/*  TODO: 64-bit write to CRIME_CONTROL, but some things
		    (such as NetBSD 1.6.2) write to 0x00c!  */
		if (writeflag == MEM_WRITE) {
			/*
			 *  0x200 = watchdog timer (according to NetBSD)
			 *  0x800 = "reboot" used by the IP32 PROM
			 */
			if (idata & CRIME_CONTROL_DOG_ENABLE) {
				idata &= ~CRIME_CONTROL_DOG_ENABLE;
			}
			if (idata & CRIME_CONTROL_HARD_RESET) {
				int j;

				/*  This is used by the IP32 PROM's
				    "reboot" command:  */
				for (j=0; j<cpu->machine->ncpus; j++)
					cpu->machine->cpus[j]->running = 0;

				idata &= ~CRIME_CONTROL_HARD_RESET;
			}

			idata &= ~CRIME_CONTROL_ENDIANESS;

			if (idata != 0)
				fatal("[ CRIME_CONTROL: unimplemented "
				    "control 0x%016llx ]\n", (long long)idata);
		}
		break;

	case CRIME_INTSTAT:	/*  0x010, Current interrupt status  */
	case CRIME_INTMASK:	/*  0x018, Current interrupt mask  */
		crime_interrupt_reassert(d);
		break;

	case CRIME_DOG:		/*  0x030  */
		// No warning.
		break;

	case CRIME_TIME:	/*  0x038  */
		crime_update_crime_time(d);
		break;

	default:
		if (writeflag==MEM_READ) {
			debug("[ crime: read from 0x%x, len=%i:",
			    (int)relative_addr, len);
			for (i=0; i<len; i++)
				debug(" %02x", data[i]);
			debug(" ]\n");
		} else {
			debug("[ crime: write to 0x%x:", (int)relative_addr);
			for (i=0; i<len; i++)
				debug(" %02x", data[i]);
			debug(" (len=%i) ]\n", len);
		}
	}

 crime_declined:
	/*  #529: a declined access jumps here, skipping the register switch,
	    and is still answered.  */
	d->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;
	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
		d->reg[CRIME_HARDINT / sizeof(uint64_t)]);

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

## THE DETECTOR REPAIR -- `regress/crime_width_probe.py`, table 1's 40-row instrument -> the 71-row one (`diff -u`, verbatim)

```diff
--- GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable_20260913/crime_width_probe.table1.py	2026-09-13 02:21:48.976503700 -0500
+++ GXEMUL-SEC/regress/crime_width_probe.py	2026-09-13 03:57:17.531150200 -0500
@@ -14,43 +14,59 @@
 
 Every access here is a real MIPS guest instruction through real address decode and memory_rw, one `step' at a time.
 
-CONTRACT -- the edits this detector is designed to catch (clause (e)):
-  1. the detect reinstated verbatim, or any other emulator process exit at the width arm       <op> surv (all six widths), latch surv
+CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a mutation-test table under
+artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/):
+  1. the detect reinstated verbatim, or any other emulator process exit at the width arm, before or after the announce
+                                                       <op> surv (six widths), hi surv, latch surv, sb08 run
   2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)      <op> pc, <op> exc, lb/lh/lbu/lhu v0
-  3. the refused access FALLING INTO THE REGISTER SWITCH (the goto lost, or a
-     narrower decline), at each width x direction cell:
-        1-byte write  sb 0x01   -> +0x08   the CRIME_CONTROL arm's unimplemented-control fatal   sb08 msg
-        2-byte write  sh 0x0800 -> +0x08   the CRIME_CONTROL arm's HARD_RESET stops every CPU    sh08 run, sh08 pc
-        1-byte read   lb  at +0 from pc 0xbfc05180   the CRIME_REV PROM-probe hack sets pc = ra  lb rev pc
-        2-byte read   lh  at +0 from pc 0xbfc05180                                               lh rev pc
+  3. the refused access FALLING INTO THE REGISTER SWITCH -- the goto lost, or narrowed by width, direction, or ADDRESS.
+     The switch's observable arms, per refusal cell:
+        CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
+                                          sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
+        CRIME_REV (+0x00), reads AND writes, from pc 0xbfc05180: the PROM-probe hack sets pc = ra (it does not test
+                                          the direction)                                    lb/lh/sb/sh rev pc
+        CRIME_INTMASK (+0x18), CRIME_INTSTAT (+0x10), reads and writes: the arm calls crime_interrupt_reassert(),
+                                          which raises cause.IP2 after a SOFTINT store       imask lb/sb, istat lb/sb
+        CRIME_TIME (+0x38), reads and writes: the arm advances TIME, which the NEXT read shows   time lb, time sb
+        the default arm (any unlabelled offset): a debug() line, printed while stepping      lb/lh/sb/sh nodflt,
+                                          at +0x07, +0x06, +0x1f, +0x1e and +0x27f           hi nodflt
      Each channel carries a LIVE control on an accepted width that shows it can vary:
-        rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text).
+        rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text),
+        imask/istat pre + ctl (IP2 low after the setup; an accepted lw sets it), time lb/sb ctl (an accepted ld moves
+        TIME), dflt ctl (lw +0x04 prints the default-arm line).
+     The INTSTAT/INTMASK/TIME rows came from the pass-2 Opus seat, which MEASURED a decline narrowed to skip those
+     labels passing the 40-row version of this detector 40/40 (opus_pass2_20260913/OPUS_REPORT.md).
      *** THE sh08 AND sw08 CHANNELS EXIST BECAUSE OF A SEPARATE DEFECT, `crimectllane' (filed): the switch matches
      CRIME_CONTROL by its exact label 0x08 and reads the RAW idata, so a 32-bit write to the high half, or a halfword at
      +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
      removes or moves these channels and owes their re-derivation -- the sw08 controls will go red to say so. ***
   4. the latch removed or never set: five refused accesses in one session owe EXACTLY ONE announce      latch x5
-  5. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this):
-        8W acc8 st, 8R acc8 ld, 4R high half acc4 rhi, 4R low half acc4 rlo, 4W low half acc4 wlo, 4W high half acc4 whi
-     on CRIME_DOG (0x030), a register the switch gives no side effect ("No warning.").
-  6. the announce text: each width's own session prints `unimplemented len=N at 0xA -- declined.' exactly once   <op> said
+  5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
+     session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
+     debug() would not (free said)
+  6. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this),
+     at BOTH ends of the window:  CRIME_DOG +0x30 -- acc8 st+ld (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi;
+     the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w
+  7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps
 
 DISCLOSED, not rowed:
   * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
-    (#95, `if (writeflag == MEM_READ) memset(data, 0, len);' in src/cpus/memory_rw.c), so the tail's write of odata = 0
-    and no write at all leave the same bytes.  Measured by the pass-1 Opus seat (opus_pass1_20260913/out/rows_return1.out).
-  * a refused store's READBACK is non-varying across every candidate (the store is dropped by decline, FAULT and the
-    switch's default arm alike -- measured 0xbadcafe unchanged in all of rows_*.out), so it carries no row.
-  * the INTSTAT/INTMASK (reassert), TIME (update) and HARDINT (restore) cells a fall-through could reach: effects are
-    idempotent or overwritten by the tail, and no observable here separates them.
-  * FREE-RUNNING: fatal() is not verbosity-gated, so the announce prints free-running too (measured by the Opus seat);
-    this detector steps only.
+    (#95, src/cpus/memory_rw.c -- `if (writeflag == MEM_READ)' then `memset(data, 0, len);', immediately above
+    `paddr -= mem->devices[i].baseaddr;'), and on a declined access nothing between the entry and the tail writes
+    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 in mutation-test table 1.
+  * a fall-through confined to the two label cells whose arms have NO body for that access, both EQUIVALENT:
+      CRIME_DOG (0x30)       `No warning.' -- the arm is `break;'
+      CRIME_CONTROL, reads   the arm acts only on MEM_WRITE
+    Each measured as a survivor in mutation-test table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
+  * ACCEPT cells at offsets other than +0x30 and +0x278: an accept arm narrowed by an address strictly INSIDE the
+    window (e.g. `len == 8 && relative_addr != 0x100') is not seen; the two rowed slots pin the near and far ends.
   * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
     not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.
+  * independence between two CRIME instances (the latch is per instance by construction; IP32 has one CRIME).
 
 Sentinel: CRIMEP_DONE (plus CRIMEP_RESULT=n/N and CRIMEP_CONTROL=OK|FAIL).
 """
-import os, pty, re, select, sys, time
+import os, pty, re, select, signal, sys, time
 
 BIN = sys.argv[1]
 LABEL = sys.argv[2] if len(sys.argv) > 2 else "?"
@@ -122,10 +138,17 @@
     rd(settle)
     for i, c in enumerate(cmds):
         try:
-            os.write(fd, (c + "\n").encode("latin-1"))
+            if c == "<RUN>":        # free-run: `continue', let the guest run, then break back in with CTRL-C
+                os.write(fd, b"continue\n")
+                ok = rd(2.0)
+                os.write(fd, b"\x03")
+                ok = ok and rd(1.5)
+            else:
+                os.write(fd, (c + "\n").encode("latin-1"))
+                ok = rd(spin if i == len(cmds) - 1 else 0.25)
         except OSError:
             break
-        if not rd(spin if i == len(cmds) - 1 else 0.25):
+        if not ok:
             break
     eof = True                      # a process already gone before `quit' has closed the pty; its status says how
     try:
@@ -133,6 +156,11 @@
         eof = not rd(10.0)          # to EOF, so anything printed on the way out is in the transcript
     except OSError:
         pass
+    if not eof:
+        try:
+            os.detect(pid, signal.SIGKILL)    # a session that never reached EOF is ended, never waited on forever
+        except OSError:
+            pass
     try:
         os.close(fd)
     except OSError:
@@ -184,8 +212,8 @@
     return ["at=0x%x" % addr, "%s=0x%x" % (rt, SENT)] + run_ops([enc(op, "at", rt)], here), here
 
 
-def st(A, op, addr, val):
-    here = A.take(1)
+def st(A, op, addr, val, at=None):
+    here = A.take(1) if at is None else at
     return ["a3=0x%x" % addr, "t0=0x%x" % val] + run_ops([enc(op, "a3", "t0")], here), here
 
 
@@ -200,7 +228,16 @@
 
 
 def said(t, ln, off, clean):
-    return count(t, "unimplemented len=%d at 0x%x -- declined." % (ln, off), clean)
+    """the whole announce, `(once)' marker included -- a reworded or unmarked announce reads 0"""
+    return count(t, "unimplemented len=%d at 0x%x -- declined.  (once) ]" % (ln, off), clean)
+
+
+def dflt(t, clean):
+    """the register switch's default-arm debug() lines -- printed while stepping, so a refused access that falls into
+    the switch at an unlabelled offset says so here"""
+    if not clean:
+        return "unclean"
+    return t.count("[ crime: read from") + t.count("[ crime: write to")
 
 
 print("CRIME WIDTH PROBE (#529) -- rung 3, unmodified -E sgi -e ip32   binary=%s  label=%s" % (BIN, LABEL))
@@ -215,6 +252,7 @@
 row("live", pr(t, "v1"), "0x%x" % LIVE_VAL, "LIVENESS: RAM round trip, same apparatus")
 row("devsig", pr(t, "s1"), "0x11", "CRIME_REV low half = rev 0x11: a device")
 row("devsig hi", pr(t, "s2"), "0x0", "CRIME_REV high half reads 0")
+row("dflt ctl", count(t, "[ crime: read from 0x4,", clean), 1, "CONTROL: default-arm text prints when stepped")
 
 # ---- the switch channels are LIVE on an accepted width (else rows 3.x could not vary) ----
 A = Addr(CODE)
@@ -261,6 +299,7 @@
         row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
         row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
         row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
+        row("%s nodflt" % op, dflt(t, clean), 0, "switch default arm NOT reached at 0x%x" % off)
     row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
 
 for op, off, val in (("sb", 0x1f, 0xff), ("sh", 0x1e, 0xffff)):
@@ -271,6 +310,7 @@
     row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
     row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
     row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
+    row("%s nodflt" % op, dflt(t, clean), 0, "switch default arm NOT reached at 0x%x" % off)
     row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
 
 # ---- the switch is NOT entered by a refused width, per cell (contract 3) ----
@@ -284,6 +324,7 @@
 x, here = st(A, "sb", CRIME + 0x08, 0x01)
 t, clean = session(x + AFTER + roundtrip(A))
 row("sb08 msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "1W sb 0x01 +0x08: no CONTROL text")
+row("sb08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "1W: the session completes (a RAM trip)")
 
 for op in ("lb", "lh"):
     A = Addr(CODE)
@@ -292,6 +333,125 @@
     row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dR at CRIME_REV from 0xbfc05180: pc NOT ra"
         % (1 if op == "lb" else 2))
 
+#  the CRIME_REV arm's PROM-probe hack does not test writeflag, so the WRITE cells at +0 are side-effect cells too
+for op, val in (("sb", 0xa5), ("sh", 0xa5a5)):
+    A = Addr(CODE)
+    x, _ = st(A, op, CRIME + 0, val, at=PROBE_PC)
+    t, clean = session(["ra=0x%x" % RA] + x + AFTER)
+    row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dW at CRIME_REV from 0xbfc05180: pc NOT ra"
+        % (1 if op == "sb" else 2))
+
+# ---- the INTSTAT / INTMASK labels: their arm calls crime_interrupt_reassert(), which is NOT idempotent -- ----
+#  INTMASK = bit 28 and SOFTINT = bit 28 are stored with 8-byte writes; SOFTINT's store goes to the default arm and does
+#  NOT reassert, so the CPU's IP2 (cause bit 0x400) stays low until something reasserts.  A refused access at the label
+#  must leave it low; the accepted `lw' that follows is the CONTROL that the arm reasserts at once.  (Measured by the
+#  pass-2 Opus seat, opus_pass2_20260913/scripts/crime_p2_escape.py E1/E2: a fall-through at the label sets IP2.)
+BIT = 0x10000000
+
+
+def nth(t, reg, n):
+    ms = re.findall(r"print\s+%s\s*\n\s*(0x[0-9a-f]+)" % reg, t)
+    return int(ms[n], 16) if len(ms) > n else None
+
+
+def ip2(v):
+    return "absent" if v is None else ("set" if v & 0x400 else "clear")
+
+
+for lbl, off in (("imask", 0x18), ("istat", 0x10)):
+    A = Addr(CODE)
+    c = []
+    x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
+    x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
+    c += ["print cause"]
+    x, _ = ld(A, "lb", CRIME + off, "v0"); c += x
+    c += ["print cause"]
+    x, _ = st(A, "sb", CRIME + off, 0); c += x
+    c += ["print cause"]
+    x, _ = ld(A, "lw", CRIME + off, "v0"); c += x
+    c += ["print cause"]
+    t, clean = session(c)
+    row("%s pre" % lbl, ip2(nth(t, "cause", 0)), "clear", "IP2 low after SOFTINT's default-arm store")
+    row("%s lb" % lbl, ip2(nth(t, "cause", 1)), "clear", "refused lb +0x%x: no reassert" % off)
+    row("%s sb" % lbl, ip2(nth(t, "cause", 2)), "clear", "refused sb +0x%x: no reassert" % off)
+    row("%s ctl" % lbl, ip2(nth(t, "cause", 3)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)
+
+# ---- the TIME label: an accepted read returns the value of the PREVIOUS update, then updates -- so a refused access
+#  that reached crime_update_crime_time() would show in the NEXT read.  The first `ld' latches last_microseconds; on the
+#  fixed build the next `ld' reads what the device tick added (measured 66 or 132), far below SMALL (0.1 s of TIME);
+#  a fall-through at 0x38 makes it the wall-clock interval of the intervening debugger commands, ~1e8.  The third `ld'
+#  is the CONTROL that the channel moves.  (Opus pass 2, E3.)
+SMALL = 66 * 100000
+
+
+def mag(v):
+    return "absent" if v is None else ("small" if v < SMALL else "large")
+
+
+for op in ("lb", "sb"):
+    A = Addr(CODE)
+    c = []
+    x, _ = ld(A, "ld", CRIME + 0x38, "s0"); c += x
+    if op == "lb":
+        x, _ = ld(A, "lb", CRIME + 0x38, "v0"); c += x
+    else:
+        x, _ = st(A, "sb", CRIME + 0x38, 0); c += x
+    x, _ = ld(A, "ld", CRIME + 0x38, "s1"); c += x
+    x, _ = ld(A, "ld", CRIME + 0x38, "s2"); c += x
+    t, clean = session(c + ["print s1", "print s2"])
+    row("time %s" % op, mag(nth(t, "s1", 0)), "small", "ld after a refused %s +0x38: TIME not updated" % op)
+    row("time %s ctl" % op, mag(nth(t, "s2", 0)), "large", "CONTROL: the accepted ld moved TIME")
+
+# ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----
+A = Addr(CODE)
+c = []
+x, _ = st(A, "sd", CRIME + 0x30, 0x0123456789abcdef); c += x
+x, _ = st(A, "sb", CRIME + 0x37, 0xa5); c += x
+x, _ = ld(A, "ld", CRIME + 0x30, "a0"); c += x
+x, _ = st(A, "sh", CRIME + 0x30, 0x5a5a); c += x
+x, _ = ld(A, "ld", CRIME + 0x30, "a1"); c += x
+t, clean = session(c + ["print a0", "print a1"])
+row("sb keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x37 leaves CRIME_DOG as seeded")
+row("sh keeps", pr(t, "a1"), "0x123456789abcdef", "refused sh +0x30 leaves CRIME_DOG as seeded")
+
+# ---- ACCEPT cells at the window's LAST 8-byte slot (+0x278; no case label, no prelude write) -- the far bound ----
+A = Addr(CODE)
+c = []
+x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x
+x, _ = ld(A, "ld", CRIME + 0x278, "a0"); c += x
+x, _ = ld(A, "lw", CRIME + 0x278, "a1"); c += x
+x, _ = ld(A, "lw", CRIME + 0x27c, "a2"); c += x
+x, _ = st(A, "sw", CRIME + 0x27c, 0x0a0b0c0d); c += x
+x, _ = st(A, "sw", CRIME + 0x278, 0x11112222); c += x
+x, _ = ld(A, "ld", CRIME + 0x278, "s0"); c += x
+t, clean = session(c + ["print a0", "print a1", "print a2", "print s0"])
+row("top8 st+ld", pr(t, "a0"), "0x102030405060708", "8W then 8R at +0x278")
+row("top4 rhi", pr(t, "a1"), "0x1020304", "4R high half at +0x278")
+row("top4 rlo", pr(t, "a2"), "0x5060708", "4R low half at +0x27c")
+row("top4 w", pr(t, "s0"), "0x111122220a0b0c0d", "4W both halves at +0x278/+0x27c")
+
+# ---- a refused width at the window's LAST byte: declined, announced, default arm not reached ----
+A = Addr(CODE)
+x, here = st(A, "sb", CRIME + 0x27f, 0xff)
+t, clean = session(x + AFTER + roundtrip(A))
+row("hi said", said(t, 1, 0x27f, clean), 1, "sb +0x27f: own announce, once")
+row("hi nodflt", dflt(t, clean), 0, "switch default arm NOT reached at 0x27f")
+row("hi surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
+
+# ---- FREE-RUNNING: the announce is a fatal(), so it prints when the guest is NOT single-stepped (a debug() would not) ----
+A = Addr(CODE)
+here = A.take(2)
+c = ["at=0x%x" % (CRIME + 7), "v0=0x%x" % SENT,
+     "put w 0x%x, 0x%08x" % (here, enc("lb", "at", "v0")),
+     "put w 0x%x, 0x%08x" % (here + 4, OP_NOP),
+     "put w 0x%x, 0x%08x" % (here + 8, OP_B_SELF),
+     "put w 0x%x, 0x%08x" % (here + 12, OP_NOP),
+     "pc=0x%x" % here, "<RUN>", "print v0"]
+t, clean = session(c)
+ran = t.split("continue", 1)[1] if "continue" in t else ""
+row("free said", ran.count("unimplemented len=1 at 0x7 -- declined.  (once) ]"), 1, "free-running lb +7: announce printed")
+row("free v0", pr(t, "v0"), "0x0", "free-running lb +7: declined read answers 0")
+
 # ---- the latch: five refused accesses, one session, exactly one announce ----
 A = Addr(CODE)
 c = []
@@ -305,7 +465,9 @@
 
 npass = sum(1 for _, ok in rows if ok)
 st_ = dict(rows)
-control = all(st_.get(n, False) for n in ("live", "devsig", "devsig hi", "rev pc ctl", "sw08 halts", "sw08 msg ctl"))
+control = all(st_.get(n, False) for n in ("live", "devsig", "devsig hi", "dflt ctl", "rev pc ctl", "sw08 halts",
+                                          "sw08 msg ctl", "imask pre", "imask ctl", "istat pre", "istat ctl",
+                                          "time lb ctl", "time sb ctl"))
 print("")
 print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
 print("CRIMEP_RESULT=%d/%d" % (npass, len(rows)))
```

## QUESTIONS

1. Adjudicate F1..F18 and D1..D2: UPHOLD / OVERTURN / REFINE / CANNOT SETTLE, one line each with a reason.
2. **WHICH OF MY ACCEPTED DISPOSITIONS IS WRONG?**  Sixteen accepted; name the weakest.
3. **WHAT DID ALL NINE OF US MISS?**  You now have the whole panel's output and the repaired detector.  Name the smallest
   source edit to `dev_sgi_ip32.c` that undoes the fix's behaviour and passes all 71 rows — as an exact edit — and which row you
   expected to catch it.
