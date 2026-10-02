# CLOSING PASS — `crimewidthkill` (#529): is the repaired regression test complete?  Liveness token `CRIME_CLOSE_20260913`.

VERDICT LINE FIRST: `CLOSES` (no floor gap remains in the 85-row test) or `GAP: <exact source edit to dev_sgi_ip32.c>`,
then the token.

This is a routine software-testing review of an open-source hardware emulator (GXemul) and its regression test.
"Mutant" means a deliberately modified copy of the emulator's C source used to check that the test notices the change
(standard mutation testing).  Please check the premises, not only the reasoning, and say what you could not check.
Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` only.  File-reading seats: `src/devices/dev_sgi_ip32.c`
(`DEVICE_ACCESS(crime)`), `regress/crime_width_probe.py`, `regress/artifacts/crimewidthkill/`.

## SETTLED (recorded; re-stated because the questions depend on it)

* **The fix** (unchanged since pass 2, and every seat of three passes found it correct): `DEVICE_ACCESS(crime)` used to
  stop the emulator on any access of length other than 8 or 4.  It now prints one latched `(once)` notice per device
  instance (`int warned`, bit `CRIME_W_LEN`) and `goto crime_declined;` past the register switch to the function's common
  tail, which answers a read 0 and returns 1.
* **Why the switch must be skipped** (each MEASURED): a refused access that reached it would, at CRIME_CONTROL (0x08,
  writes), stop every CPU or print an unlatched diagnostic; at CRIME_REV (0x00, either direction, from pc 0xbfc051xx)
  set pc = ra; at CRIME_INTSTAT/INTMASK (0x10/0x18) re-assert the interrupt line (cause.IP2 after a SOFTINT store); at
  CRIME_TIME (0x38) advance the clock the next read shows; at an unnamed offset print a `debug()` line; at CRIME_DOG
  (0x30) nothing (`break;`); CONTROL reads nothing.
* **The test's history**: 40 rows (table 1, 17 of 17 non-equivalent mutants detected) -> 71 rows after pass 2 (table 2,
  20 of 21, the 21st disclosed) -> 85 rows after the shared-findings pass (table 3, below).  Every red-row set in tables
  2 and 3 was predicted in writing BEFORE the table ran.
* **The standard this pass applies**: the test must detect any single-label or single-cell change at every OBSERVABLE
  switch label for each refused {1-byte, 2-byte} x {read, write} cell, every accept cell's shrinkage at both window ends
  plus one anchored cell, the notice's text, channel and latch, and state carried across calls.  An effect keyed on ONE
  offset the switch does not name, or on an interior accept slot, is DISCLOSED coverage debt (the probe header lists
  them) -- a finding there is not a gap unless you show the disclosure is wrong.

## THE SHARED-FINDINGS PASS (F2) AND WHAT CHANGED

Seven scriptable seats + the compile-and-measure seat reviewed the 71-row test with every other seat's findings in hand.
Undetected changes they found, each MEASURED at 71/71 on the 71-row test and each now DETECTED by the 85-row test:

| finding | from | now caught by |
|---|---|---|
| 2-byte refused cells at INTSTAT, INTMASK, TIME (`len != 2 \|\| relative_addr != CRIME_INTSTAT` ...) | grok, glm, codex, Opus | imask/istat lh, sh; time lh, sh |
| accept arms re-mapping their register index (`d->reg[(relative_addr & 0x3f) / 8]`) | kimi-k3:cloud | top8 anchor (reads bank-1 control at +0x210, a value the prelude writes) |
| `static uint64_t idata = 0, odata = 0;` (a refused read answering a stale value) | codex | warm v0 |
| `d->warned = 0;` in an accept arm (notice re-armed by an accepted access) | codex | warm once |
| the latch's bit taken from `len`, `relative_addr`, or `CRIME_W_LEN << writeflag` | Opus | latch x5 (reordered, lh first), warm once |
| CONTROL's tested DOG_ENABLE bit never written set by a refused row | Opus | sh08b msg, sh08b run (sh 0x0201, sh 0x0a00) |
| a refused store landing only at offsets >= 0x200 | Opus | hi keeps |

Also recorded: my own records errors that seats caught (two miscounts in the tables' summaries, both corrected in
place with the refuted text quoted); a construction bug of mine in the repair (a session-wide default-arm count that an
accepted access in the same session tripped -- fixed by keying each count on the refused access's own offset and
direction, measured 85/85 before the table).

## THE WHOLE ENCLOSING FUNCTION (the fix in place; every exit path and the common tail)

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

## THE TEST'S HEADER -- CONTRACT and DISCLOSED, verbatim

```

crime_width_probe.py BIN [LABEL] -- #529 crimewidthkill DETECTOR, rung 3, cold debugger, UNMODIFIED `-E sgi -e ip32'.

src/devices/dev_sgi_ip32.c, DEVICE_ACCESS(crime): an access whose length is neither 8 nor 4 used to reach

        fatal("crime access len = %i!\n", len);
        exit(1);

so one guest lb/lbu/lh/lhu/sb/sh anywhere in CRIME (physical 0x14000000, KSEG1 0xb4000000) ended the emulator
(witnessed 6/6 at rung 3: regress/artifacts/crimewidthkill/crime_width_witness_20260913.py).  #529 DECLINES the width
with one latched `(once)' announce and a `goto' to the function's common tail, skipping the register switch -- the
#498 sgi_de shape.  A read is answered 0 by the tail, a write is dropped, the PC advances, no exception is raised.

Every access here is a real MIPS guest instruction through real address decode and memory_rw, one `step' at a time.

CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3_20260913/):
  1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                       <op> surv (six widths), hi surv, latch surv, sb08 run
  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)      <op> pc, <op> exc, lb/lh/lbu/lhu v0
  3. the refused access FALLING INTO THE REGISTER SWITCH -- the goto lost, or narrowed by width, direction, or ADDRESS.
     The switch's observable arms, per refusal cell:
        CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
                                          sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
                                          and the arm's TESTED idata bits both ways at 2W: sh 0x0201 (DOG set,
                                          RESET clear) and sh 0x0a00 (both set)             sh08b msg, sh08b run
        CRIME_REV (+0x00), reads AND writes, from pc 0xbfc05180: the PROM-probe hack sets pc = ra (it does not test
                                          the direction)                                    lb/lh/sb/sh rev pc
        CRIME_INTMASK (+0x18), CRIME_INTSTAT (+0x10), all four cells: the arm calls crime_interrupt_reassert(),
                                          which raises cause.IP2 after a SOFTINT store   imask/istat lb, sb, lh, sh
        CRIME_TIME (+0x38), all four cells: the arm advances TIME, which the NEXT read shows   time lb, sb, lh, sh
        the default arm (any unlabelled offset): a debug() line, printed while stepping      lb/lh/sb/sh nodflt,
                                          at +0x07, +0x06, +0x1f, +0x1e and +0x27f           hi nodflt
     Each channel carries a LIVE control on an accepted width that shows it can vary:
        rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text),
        imask/istat pre + ctl (IP2 low after the setup; an accepted lw sets it), time lb/sb/lh/sh ctl (an accepted ld
        moves TIME), dflt ctl (lw +0x04 prints the default-arm line).
     The INTSTAT/INTMASK/TIME rows came from the pass-2 Opus seat, which MEASURED a decline narrowed to skip those
     labels passing the 40-row version of this detector 40/40 (opus_pass2_20260913/OPUS_REPORT.md); their 2-byte cells
     from the F2 pass (grok, glm): `len != 2 || relative_addr != CRIME_INTSTAT' passed the 71-row version.  So every
     observable label carries the whole {1,2} x {R,W} refusal floor (CONTROL's reads and DOG have no body: below).
     *** THE sh08 AND sw08 CHANNELS EXIST BECAUSE OF A SEPARATE DEFECT, `crimectllane' (filed): the switch matches
     CRIME_CONTROL by its exact label 0x08 and reads the RAW idata, so a 32-bit write to the high half, or a halfword at
     +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
     removes or moves these channels and owes their re-derivation -- the sw08 controls will go red to say so. ***
  4. the latch removed, never set, or keyed on the access (its bit taken from len, relative_addr or writeflag --
     Opus, F2): five refused accesses in one session, a 2-byte read at an even address FIRST, owe EXACTLY ONE
     announce (latch x5); a session whose first refusal is a store owes one too (warm once)
  5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
     session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
     debug() would not (free said)
  6. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this),
     at BOTH ends of the window:  CRIME_DOG +0x30 -- acc8 st+ld (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi;
     the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w.  Those rows are ROUND TRIPS and cannot see an
     accept arm that re-maps its register index (kimi-k3:cloud, F2: `d->reg[(relative_addr & 0x3f) / 8]' passed the
     71-row version), so one row is ANCHORED: `top8 anchor' reads bank-1 control at +0x210, a value the PRELUDE writes
     by bank index (1 for -M 64), not by the decode under test.  *** It pins the model's CURRENT bank layout, which the
     filed `crimebankorder' disputes; a round that re-orders the banks owes this row's re-derivation. ***
  7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps;
     and at the far block, a refused sb +0x27f leaves +0x278 reading 0 (Opus, F2: a store landing only >= 0x200)
                                                                                                        hi keeps
  8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
     `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
     warm once  (the codex seat, F2)

DISCLOSED, not rowed:
  * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
    (#95, src/cpus/memory_rw.c -- `if (writeflag == MEM_READ)' then `memset(data, 0, len);', immediately above
    `paddr -= mem->devices[i].baseaddr;'), and on a declined access nothing between the entry and the tail writes
    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 in kill table 1.
  * a fall-through confined to the two label cells whose arms have NO body for that access, both EQUIVALENT:
      CRIME_DOG (0x30)       `No warning.' -- the arm is `break;'
      CRIME_CONTROL, reads   the arm acts only on MEM_WRITE
    Each measured as a survivor in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
  * ACCEPT cells at offsets other than +0x30, +0x210 and +0x278: an accept arm narrowed by an address strictly INSIDE
    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71) is not seen.
  * an effect ADDED to the decline arm and keyed on ONE offset the switch does not name -- a refused store that lands
    only at +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only
    at +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at five default-arm
    offsets; an arbitrary single offset inside a partition the body does not distinguish is clause (e) debt.
  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 by the Opus seat
    (F2, `sft'); it is the single-unnamed-offset class of the bullet above.
  * a FUNCTION-STATIC latch in place of `d->warned' is NOT equivalent in general -- two IP32 machines in one gxemul
    process would share it -- and this single-machine probe cannot see it (kimi-k3:cloud, F2; the pass-2 Opus seat had
    recorded it "equivalent", which holds only for one machine per process).
  * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
    not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.
  * independence between two CRIME instances (the latch is per instance by construction; IP32 has one CRIME).

Sentinel: CRIMEP_DONE (plus CRIMEP_RESULT=n/N and CRIMEP_CONTROL=OK|FAIL).

```

## THE REPAIR DIFF -- the 71-row test -> the 85-row test (`diff -u`, verbatim)

```diff
--- GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable2_20260913/crime_width_probe.table2.py	2026-09-13 04:04:35.094249900 -0500
+++ GXEMUL-SEC/regress/crime_width_probe.py	2026-09-13 08:24:32.459720400 -0500
@@ -15,7 +15,7 @@
 Every access here is a real MIPS guest instruction through real address decode and memory_rw, one `step' at a time.
 
 CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
-artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/):
+artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3_20260913/):
   1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                        <op> surv (six widths), hi surv, latch surv, sb08 run
   2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)      <op> pc, <op> exc, lb/lh/lbu/lhu v0
@@ -23,31 +23,46 @@
      The switch's observable arms, per refusal cell:
         CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
                                           sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
+                                          and the arm's TESTED idata bits both ways at 2W: sh 0x0201 (DOG set,
+                                          RESET clear) and sh 0x0a00 (both set)             sh08b msg, sh08b run
         CRIME_REV (+0x00), reads AND writes, from pc 0xbfc05180: the PROM-probe hack sets pc = ra (it does not test
                                           the direction)                                    lb/lh/sb/sh rev pc
-        CRIME_INTMASK (+0x18), CRIME_INTSTAT (+0x10), reads and writes: the arm calls crime_interrupt_reassert(),
-                                          which raises cause.IP2 after a SOFTINT store       imask lb/sb, istat lb/sb
-        CRIME_TIME (+0x38), reads and writes: the arm advances TIME, which the NEXT read shows   time lb, time sb
+        CRIME_INTMASK (+0x18), CRIME_INTSTAT (+0x10), all four cells: the arm calls crime_interrupt_reassert(),
+                                          which raises cause.IP2 after a SOFTINT store   imask/istat lb, sb, lh, sh
+        CRIME_TIME (+0x38), all four cells: the arm advances TIME, which the NEXT read shows   time lb, sb, lh, sh
         the default arm (any unlabelled offset): a debug() line, printed while stepping      lb/lh/sb/sh nodflt,
                                           at +0x07, +0x06, +0x1f, +0x1e and +0x27f           hi nodflt
      Each channel carries a LIVE control on an accepted width that shows it can vary:
         rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text),
-        imask/istat pre + ctl (IP2 low after the setup; an accepted lw sets it), time lb/sb ctl (an accepted ld moves
-        TIME), dflt ctl (lw +0x04 prints the default-arm line).
+        imask/istat pre + ctl (IP2 low after the setup; an accepted lw sets it), time lb/sb/lh/sh ctl (an accepted ld
+        moves TIME), dflt ctl (lw +0x04 prints the default-arm line).
      The INTSTAT/INTMASK/TIME rows came from the pass-2 Opus seat, which MEASURED a decline narrowed to skip those
-     labels passing the 40-row version of this detector 40/40 (opus_pass2_20260913/OPUS_REPORT.md).
+     labels passing the 40-row version of this detector 40/40 (opus_pass2_20260913/OPUS_REPORT.md); their 2-byte cells
+     from the F2 pass (grok, glm): `len != 2 || relative_addr != CRIME_INTSTAT' passed the 71-row version.  So every
+     observable label carries the whole {1,2} x {R,W} refusal floor (CONTROL's reads and DOG have no body: below).
      *** THE sh08 AND sw08 CHANNELS EXIST BECAUSE OF A SEPARATE DEFECT, `crimectllane' (filed): the switch matches
      CRIME_CONTROL by its exact label 0x08 and reads the RAW idata, so a 32-bit write to the high half, or a halfword at
      +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
      removes or moves these channels and owes their re-derivation -- the sw08 controls will go red to say so. ***
-  4. the latch removed or never set: five refused accesses in one session owe EXACTLY ONE announce      latch x5
+  4. the latch removed, never set, or keyed on the access (its bit taken from len, relative_addr or writeflag --
+     Opus, F2): five refused accesses in one session, a 2-byte read at an even address FIRST, owe EXACTLY ONE
+     announce (latch x5); a session whose first refusal is a store owes one too (warm once)
   5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
      session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
      debug() would not (free said)
   6. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this),
      at BOTH ends of the window:  CRIME_DOG +0x30 -- acc8 st+ld (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi;
-     the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w
-  7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps
+     the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w.  Those rows are ROUND TRIPS and cannot see an
+     accept arm that re-maps its register index (kimi-k3:cloud, F2: `d->reg[(relative_addr & 0x3f) / 8]' passed the
+     71-row version), so one row is ANCHORED: `top8 anchor' reads bank-1 control at +0x210, a value the PRELUDE writes
+     by bank index (1 for -M 64), not by the decode under test.  *** It pins the model's CURRENT bank layout, which the
+     filed `crimebankorder' disputes; a round that re-orders the banks owes this row's re-derivation. ***
+  7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps;
+     and at the far block, a refused sb +0x27f leaves +0x278 reading 0 (Opus, F2: a store landing only >= 0x200)
+                                                                                                        hi keeps
+  8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
+     `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
+     warm once  (the codex seat, F2)
 
 DISCLOSED, not rowed:
   * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
@@ -58,8 +73,17 @@
       CRIME_DOG (0x30)       `No warning.' -- the arm is `break;'
       CRIME_CONTROL, reads   the arm acts only on MEM_WRITE
     Each measured as a survivor in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
-  * ACCEPT cells at offsets other than +0x30 and +0x278: an accept arm narrowed by an address strictly INSIDE the
-    window (e.g. `len == 8 && relative_addr != 0x100') is not seen; the two rowed slots pin the near and far ends.
+  * ACCEPT cells at offsets other than +0x30, +0x210 and +0x278: an accept arm narrowed by an address strictly INSIDE
+    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71) is not seen.
+  * an effect ADDED to the decline arm and keyed on ONE offset the switch does not name -- a refused store that lands
+    only at +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only
+    at +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at five default-arm
+    offsets; an arbitrary single offset inside a partition the body does not distinguish is clause (e) debt.
+  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 by the Opus seat
+    (F2, `sft'); it is the single-unnamed-offset class of the bullet above.
+  * a FUNCTION-STATIC latch in place of `d->warned' is NOT equivalent in general -- two IP32 machines in one gxemul
+    process would share it -- and this single-machine probe cannot see it (kimi-k3:cloud, F2; the pass-2 Opus seat had
+    recorded it "equivalent", which holds only for one machine per process).
   * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
     not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.
   * independence between two CRIME instances (the latch is per instance by construction; IP32 has one CRIME).
@@ -232,12 +256,14 @@
     return count(t, "unimplemented len=%d at 0x%x -- declined.  (once) ]" % (ln, off), clean)
 
 
-def dflt(t, clean):
-    """the register switch's default-arm debug() lines -- printed while stepping, so a refused access that falls into
-    the switch at an unlabelled offset says so here"""
+def dflt(t, clean, off, write):
+    """the register switch's default-arm debug() line FOR THIS REFUSED ACCESS -- `[ crime: read from 0xOFF,' or
+    `[ crime: write to 0xOFF:' -- printed while stepping, so a refused access that falls into the switch at an
+    unlabelled offset says so here.  Keyed on the access's own offset and direction, because an ACCEPTED access at a
+    default-arm offset in the same session prints the same kind of line (hi keeps' ld +0x278 does)."""
     if not clean:
         return "unclean"
-    return t.count("[ crime: read from") + t.count("[ crime: write to")
+    return t.count(("[ crime: write to 0x%x:" if write else "[ crime: read from 0x%x,") % off)
 
 
 print("CRIME WIDTH PROBE (#529) -- rung 3, unmodified -E sgi -e ip32   binary=%s  label=%s" % (BIN, LABEL))
@@ -299,7 +325,7 @@
         row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
         row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
         row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
-        row("%s nodflt" % op, dflt(t, clean), 0, "switch default arm NOT reached at 0x%x" % off)
+        row("%s nodflt" % op, dflt(t, clean, off, False), 0, "switch default arm NOT reached at 0x%x" % off)
     row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
 
 for op, off, val in (("sb", 0x1f, 0xff), ("sh", 0x1e, 0xffff)):
@@ -310,7 +336,7 @@
     row("%s pc" % op, pr(t, "pc"), "0x%x" % (here + 4), "pc advances, no vector")
     row("%s exc" % op, exc(t), "0", "cause.ExcCode 0 (a bus error is 7)")
     row("%s said" % op, said(t, ln, off, clean), 1, "own announce, len=%d at 0x%x, once" % (ln, off))
-    row("%s nodflt" % op, dflt(t, clean), 0, "switch default arm NOT reached at 0x%x" % off)
+    row("%s nodflt" % op, dflt(t, clean, off, True), 0, "switch default arm NOT reached at 0x%x" % off)
     row("%s surv" % op, pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
 
 # ---- the switch is NOT entered by a refused width, per cell (contract 3) ----
@@ -326,6 +352,18 @@
 row("sb08 msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "1W sb 0x01 +0x08: no CONTROL text")
 row("sb08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "1W: the session completes (a RAM trip)")
 
+#  THE CONTROL ARM TESTS BITS OF idata, so the 2-byte write cell owes each tested bit written both clear and set (the
+#  generating-set clause; the Opus seat, F2: `relative_addr != CRIME_CONTROL || !(idata & CRIME_CONTROL_DOG_ENABLE)'
+#  passed the 71-row version because no refused row carried DOG_ENABLE).  sh08 above writes HARD_RESET set / DOG clear;
+#  here 0x0201 writes HARD_RESET clear / DOG set / bit 0 (the arm would print its unimplemented-control text) and 0x0a00
+#  writes both set (the arm would stop every CPU).  A 1-byte write cannot carry either bit.
+A = Addr(CODE)
+x, _ = st(A, "sh", CRIME + 0x08, 0x0201)
+y, _ = st(A, "sh", CRIME + 0x08, 0x0a00)
+t, clean = session(x + y + AFTER + roundtrip(A))
+row("sh08b msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "2W sh 0x0201 +0x08 (DOG set): no CONTROL text")
+row("sh08b run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W sh 0x0a00 +0x08 (DOG+RESET): CPUs NOT stopped")
+
 for op in ("lb", "lh"):
     A = Addr(CODE)
     x, _ = ld(A, op, CRIME + 0, "v0", at=PROBE_PC)
@@ -368,19 +406,28 @@
     c += ["print cause"]
     x, _ = st(A, "sb", CRIME + off, 0); c += x
     c += ["print cause"]
+    x, _ = ld(A, "lh", CRIME + off, "v0"); c += x
+    c += ["print cause"]
+    x, _ = st(A, "sh", CRIME + off, 0); c += x
+    c += ["print cause"]
     x, _ = ld(A, "lw", CRIME + off, "v0"); c += x
     c += ["print cause"]
     t, clean = session(c)
     row("%s pre" % lbl, ip2(nth(t, "cause", 0)), "clear", "IP2 low after SOFTINT's default-arm store")
     row("%s lb" % lbl, ip2(nth(t, "cause", 1)), "clear", "refused lb +0x%x: no reassert" % off)
     row("%s sb" % lbl, ip2(nth(t, "cause", 2)), "clear", "refused sb +0x%x: no reassert" % off)
-    row("%s ctl" % lbl, ip2(nth(t, "cause", 3)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)
+    row("%s lh" % lbl, ip2(nth(t, "cause", 3)), "clear", "refused lh +0x%x: no reassert" % off)
+    row("%s sh" % lbl, ip2(nth(t, "cause", 4)), "clear", "refused sh +0x%x: no reassert" % off)
+    row("%s ctl" % lbl, ip2(nth(t, "cause", 5)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)
 
 # ---- the TIME label: an accepted read returns the value of the PREVIOUS update, then updates -- so a refused access
 #  that reached crime_update_crime_time() would show in the NEXT read.  The first `ld' latches last_microseconds; on the
-#  fixed build the next `ld' reads what the device tick added (measured 66 or 132), far below SMALL (0.1 s of TIME);
-#  a fall-through at 0x38 makes it the wall-clock interval of the intervening debugger commands, ~1e8.  The third `ld'
-#  is the CONTROL that the channel moves.  (Opus pass 2, E3.)
+#  fixed build nothing else updates TIME before the next `ld' -- the device tick (machine_add_tickfunction, CRIME_TICKSHIFT
+#  14) fires every 2^14 cycles and a session steps only a few dozen instructions -- so that read is far below SMALL (0.1 s
+#  of TIME; each row prints its raw value -- the Opus seat's separate apparatus read 66 or 132); a fall-through at 0x38
+#  makes it the wall-clock interval of the intervening debugger commands, ~1e8.  The third `ld' is the CONTROL that the
+#  channel moves.  (Opus pass 2, E3; the tick-spacing wording corrected by the kimi CLI seat on the F2 pass.)
+#  ASSUMPTION, disclosed: no tick boundary falls between the first `ld' and the refused access.
 SMALL = 66 * 100000
 
 
@@ -388,19 +435,20 @@
     return "absent" if v is None else ("small" if v < SMALL else "large")
 
 
-for op in ("lb", "sb"):
+for op in ("lb", "sb", "lh", "sh"):
     A = Addr(CODE)
     c = []
     x, _ = ld(A, "ld", CRIME + 0x38, "s0"); c += x
-    if op == "lb":
-        x, _ = ld(A, "lb", CRIME + 0x38, "v0"); c += x
+    if op in ("lb", "lh"):
+        x, _ = ld(A, op, CRIME + 0x38, "v0"); c += x
     else:
-        x, _ = st(A, "sb", CRIME + 0x38, 0); c += x
+        x, _ = st(A, op, CRIME + 0x38, 0); c += x
     x, _ = ld(A, "ld", CRIME + 0x38, "s1"); c += x
     x, _ = ld(A, "ld", CRIME + 0x38, "s2"); c += x
     t, clean = session(c + ["print s1", "print s2"])
-    row("time %s" % op, mag(nth(t, "s1", 0)), "small", "ld after a refused %s +0x38: TIME not updated" % op)
-    row("time %s ctl" % op, mag(nth(t, "s2", 0)), "large", "CONTROL: the accepted ld moved TIME")
+    s1, s2 = nth(t, "s1", 0), nth(t, "s2", 0)
+    row("time %s" % op, mag(s1), "small", "after refused %s +0x38 (raw %s)" % (op, s1))
+    row("time %s ctl" % op, mag(s2), "large", "CONTROL: accepted ld moved TIME (raw %s)" % s2)
 
 # ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----
 A = Addr(CODE)
@@ -410,13 +458,21 @@
 x, _ = ld(A, "ld", CRIME + 0x30, "a0"); c += x
 x, _ = st(A, "sh", CRIME + 0x30, 0x5a5a); c += x
 x, _ = ld(A, "ld", CRIME + 0x30, "a1"); c += x
-t, clean = session(c + ["print a0", "print a1"])
+#  the codex seat, F2: every other refused read runs in a COLD session, so an `odata' that survived from the previous
+#  call (`static uint64_t idata = 0, odata = 0;') answered 0 there by luck.  Here a refused lbu follows accepted reads
+#  of a nonzero register; and the announce count across refused-accepted-refused catches a latch re-armed by an
+#  accepted access (`d->warned = 0;' in an accept arm), which `latch x5' -- no accepted access -- cannot.
+x, _ = ld(A, "lbu", CRIME + 0x07, "v0"); c += x
+t, clean = session(c + ["print a0", "print a1", "print v0"])
 row("sb keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x37 leaves CRIME_DOG as seeded")
 row("sh keeps", pr(t, "a1"), "0x123456789abcdef", "refused sh +0x30 leaves CRIME_DOG as seeded")
+row("warm v0", pr(t, "v0"), "0x0", "refused lbu AFTER accepted reads of 0x0123..: still 0")
+row("warm once", count(t, "-- declined.", clean), 1, "refused, accepted, refused: still one announce")
 
 # ---- ACCEPT cells at the window's LAST 8-byte slot (+0x278; no case label, no prelude write) -- the far bound ----
 A = Addr(CODE)
 c = []
+x, _ = ld(A, "ld", CRIME + 0x210, "s2"); c += x
 x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x
 x, _ = ld(A, "ld", CRIME + 0x278, "a0"); c += x
 x, _ = ld(A, "lw", CRIME + 0x278, "a1"); c += x
@@ -424,7 +480,8 @@
 x, _ = st(A, "sw", CRIME + 0x27c, 0x0a0b0c0d); c += x
 x, _ = st(A, "sw", CRIME + 0x278, 0x11112222); c += x
 x, _ = ld(A, "ld", CRIME + 0x278, "s0"); c += x
-t, clean = session(c + ["print a0", "print a1", "print a2", "print s0"])
+t, clean = session(c + ["print s2", "print a0", "print a1", "print a2", "print s0"])
+row("top8 anchor", pr(t, "s2"), "0x1", "8R +0x210: bank-1 ctrl the PRELUDE wrote (-M 64)")
 row("top8 st+ld", pr(t, "a0"), "0x102030405060708", "8W then 8R at +0x278")
 row("top4 rhi", pr(t, "a1"), "0x1020304", "4R high half at +0x278")
 row("top4 rlo", pr(t, "a2"), "0x5060708", "4R low half at +0x27c")
@@ -433,10 +490,12 @@
 # ---- a refused width at the window's LAST byte: declined, announced, default arm not reached ----
 A = Addr(CODE)
 x, here = st(A, "sb", CRIME + 0x27f, 0xff)
-t, clean = session(x + AFTER + roundtrip(A))
+y, _ = ld(A, "ld", CRIME + 0x278, "a0")        # the refused byte's register, read back by an ACCEPTED ld
+t, clean = session(x + AFTER + roundtrip(A) + y + ["print a0"])
 row("hi said", said(t, 1, 0x27f, clean), 1, "sb +0x27f: own announce, once")
-row("hi nodflt", dflt(t, clean), 0, "switch default arm NOT reached at 0x27f")
+row("hi nodflt", dflt(t, clean, 0x27f, True), 0, "switch default arm NOT reached at 0x27f")
 row("hi surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
+row("hi keeps", pr(t, "a0"), "0x0", "refused sb +0x27f does not land (ld +0x278)")
 
 # ---- FREE-RUNNING: the announce is a fatal(), so it prints when the guest is NOT single-stepped (a debug() would not) ----
 A = Addr(CODE)
@@ -455,7 +514,10 @@
 # ---- the latch: five refused accesses, one session, exactly one announce ----
 A = Addr(CODE)
 c = []
-for op, off in (("lb", 7), ("lh", 6), ("lbu", 0x3f)):
+#  lh FIRST (Opus seat, F2): a latch whose bit is taken from the access -- `d->warned |= len' or `|= relative_addr' --
+#  sets bit 0 only for a 1-byte access or an odd address, so the lh at +0x06 would leave it clear and the lb after it
+#  would announce again.  With lb first, both shapes passed.
+for op, off in (("lh", 6), ("lb", 7), ("lbu", 0x3f)):
     x, _ = ld(A, op, CRIME + off, "v0"); c += x
 for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd)):
     x, _ = st(A, op, CRIME + off, val); c += x
@@ -467,7 +529,7 @@
 st_ = dict(rows)
 control = all(st_.get(n, False) for n in ("live", "devsig", "devsig hi", "dflt ctl", "rev pc ctl", "sw08 halts",
                                           "sw08 msg ctl", "imask pre", "imask ctl", "istat pre", "istat ctl",
-                                          "time lb ctl", "time sb ctl"))
+                                          "time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl"))
 print("")
 print("FAILING: " + ", ".join(n for n, ok in rows if not ok))
 print("CRIMEP_RESULT=%d/%d" % (npass, len(rows)))
```

## MUTATION-TEST TABLE 3 -- results (`POSTTABLE.out`)

```
POSTTABLE -- #529 kill table 3 (TARGETED), written AFTER the table (PRETABLE.out predates it by mtime)
Driver kill529c.run-*.sh (frozen); summary table3.out; logs/probe_<m>.raw (the 85-row instrument) and
logs/probe_T2INSTR_<m>.raw (table 2's 71-row instrument) -- every one ends CRIMEP_DONE (checked); logs/<m>.diff;
builds/.  Instruments: crime_width_probe.table3.py (= regress/crime_width_probe.py as shipped; md5 in
logs/INSTRUMENT.md5) and ../killtable2_20260913/crime_width_probe.table2.py.  Scratch clone /tmp/gxopuscrime, baseline =
the #529 working set (BASELINE_CMP CLEAN), rebuilt in the clone; every mutant built rc 0 with a fresh object; restored
afterwards: cmp clean, binary -nt source, restored == base byte-identical, sentinel removed.

COUNTS, derived from table3.out (grep -c '^NEW' = 22 = base + 21 mutants; 7 T2INSTR lines):
  21 mutants = 19 DETECTED + 2 predicted SURVIVORS (sft, wstore31 -- both disclosed in the probe header).
  Every one of the 19 red-row sets is EXACTLY the set PRETABLE 3 named.

NEW INSTRUMENT (85 rows)                ROWS REDDENED (all = predicted)
    base        85/85  CONTROL=OK       none
    istat2      83/85                   istat lh, istat sh
    imask2      83/85                   imask lh, imask sh
    time2       83/85                   time lh, time sh
    istatsh     84/85                   istat sh
    remap       84/85                   top8 anchor  (no tick landed in the top session, so the +0x278 round trips
                                        stayed green -- the prediction marked those "not predicted", and they did not red)
    static_od   84/85                   warm v0
    rearm       84/85                   warm once
    h_imask     83/85                   imask lh, imask sh
    h_lbl       79/85                   imask lh/sh, istat lh/sh, time lh/sh
    lt_len      84/85                   latch x5
    lt_addr     84/85                   latch x5
    lt_wset     84/85                   warm once
    wst_mc      84/85                   hi keeps
    c_dog       83/85                   sh08b msg, sh08b run
    c_hrclr     83/85                   sb08 msg, sh08b msg
    nolatch     83/85                   latch x5, warm once           (re-run: its table-2 kill rested on the reordered
    latchinv    77/85                   lb/lh/sb/sh said, hi said,     latch session; both still detected)
                                        latch x5, warm once, free said
    wstore      81/85  CONTROL=FAIL     sb keeps, sh keeps, imask ctl, hi keeps   (re-run: rested on the imask session)
    acc8dog     74/85  CONTROL=FAIL     top8 anchor, top8 st+ld, top4 rhi/rlo/w, imask ctl, istat ctl,
                                        time lb/sb/lh/sh ctl; hi keeps GREEN as predicted (its ld is refused, answers 0)
    sft         85/85                   none -- PREDICTED SURVIVOR: a fall-through only at SOFTINT, an offset the switch
                                        does not name (the Opus F2 seat measured it guest-identical: one stepped debug line)
    wstore31    85/85                   none -- PREDICTED SURVIVOR: a refused store landing only at +0x31 (clause (e))

TABLE 2's 71-ROW INSTRUMENT -- the F2 escapes not already measured by the Opus F2 seat, MEASURED
    istat2 71/71  imask2 71/71  time2 71/71  istatsh 71/71  remap 71/71  static_od 71/71  rearm 71/71
  All seven escaped the 71-row detector, as claimed (grok, glm, codex, kimi-k3:cloud; remap with no tick in the top
  session, as kimi-k3:cloud said).  The Opus F2 seat measured its own (h_imask, h_lbl, lt_len, lt_addr, lt_wset, c_dog,
  wst_mc, sft) on the same instrument in opus_f2_20260913/logs/.  Every F2 escape is detected by the 85-row detector
  except the two disclosed survivors.

THE CHANNEL LINE: all 19 predicted sets exact, including the four that needed a whole-session trace (rearm's and
lt_wset's three announces; wstore's imask ctl; acc8dog's hi keeps staying green).

DENOMINATOR for the closing pass, cumulative over tables 1-3: the refusal floor {1,2} x {R,W} at EVERY observable
label -- REV (4 cells), CONTROL writes (2 cells, with the arm's tested DOG and RESET bits both ways at 2W), INTSTAT,
INTMASK and TIME (4 cells each), the default arm (4 cells at named offsets) -- each by a single-cell or single-label
fall-through; DOG and CONTROL reads by equivalent fall-throughs; the accept cells at +0x30 and +0x278 plus one anchored
row (+0x210) against a re-map; a refused store that lands (all cells, and >= 0x200); the announce's text, channel,
latch presence, and latch keying on len / address / direction; state carried across calls (static odata, latch
re-arm); the dispositions (revert, fault, exit0, return1).  NOT swept, disclosed: interior accept slots (acc8mid),
effects keyed on one unnamed offset (sft, wstore31, and the class), a function-static latch (two machines per process).
```

## QUESTIONS

1. **Is there a floor gap in the 85-row test?**  Name the smallest source edit to `dev_sgi_ip32.c` that undoes part of
   the fix's behaviour and still scores 85/85 -- as an exact edit -- with the row you expected to detect it and why it
   cannot.  A candidate inside the DISCLOSED list (interior accept slot, one unnamed offset, a function-static latch,
   widths 3/5/6/7, unaligned-pair instructions) is not a gap unless you show the disclosure is wrong.
2. **Is the repair diff above sound?**  Any row whose oracle cannot vary under the change it names; any control that is
   not live; any timing assumption stated wrongly; any contract sentence in the header the rows do not support.
3. **Which statement in this brief, or in the probe header's CONTRACT / DISCLOSED text, is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
