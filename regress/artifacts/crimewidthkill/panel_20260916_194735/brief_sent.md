# CLOSING PASS 8 -- `crimewidthkill` (#529): VERIFY the accept-side enumeration.  Liveness token `CRIME_CLOSE8_20260916`.

VERDICT LINE FIRST: `CLOSES` (no floor gap remains in the 157-row test) or `GAP: <exact source edit to dev_sgi_ip32.c>`
or `ENUMERATION WRONG: <the cell>`, then the token.

This is a routine software-testing review of an open-source hardware emulator (GXemul) and its regression test.
"Mutant" means a deliberately modified copy of the emulator's C source used to check that the test notices the change
(standard mutation testing).  Please check the premises, not only the reasoning, and say what you could not check.
Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` only.  File-reading seats: `src/devices/dev_sgi_ip32.c`
(`DEVICE_ACCESS(crime)`), `regress/crime_width_probe.py`, `regress/artifacts/crimewidthkill/`.

## WHY THIS PASS EXISTS, AND WHAT IT IS ASKED TO DO

Closing pass 6 found the two rows the 46-entry `ACCEPTS' list feeds (`rearm once', `latch x5') blind to the ACCEPT side of
those same cells: they COUNT notices, so an accept guard grown by one conjunct -- a cell wrongly declined -- takes the
session's one notice itself and the count stays 1 (codex's C1 and the Opus seat's G1-G5, each 141/141, four of them
guest-visible).  The flagship ruling (part A below) graded it a FLOOR breach and a CLASS, and fixed repair 12: codex's
`latch said' row (the announced form, at every ACCEPTS cell by construction -- all 46 accesses precede latch x5's lh
+0x06); item 6 narrowed to the guard-growth form with the SILENT bypass disclosed by class; value rows at the twelve cells
where a silent bypass is guest-visible, derived per cell; `free revP said'; wording.  **This pass VERIFIES the accept-side
enumeration -- every ACCEPTS cell x {announced (guard growth), silent (bypass)} -- and the generality argument for `latch
said'.  It hunts nothing else, and does not reopen the landing, lane or re-map classes that earlier passes closed.**

## SETTLED (recorded; re-stated because the questions depend on it)

* **The fix** (unchanged since pass 2; every seat of eight passes found it correct): a refused width is announced once per
  device instance (`int warned`, bit `CRIME_W_LEN`) and `goto crime_declined;` past the register switch to the common
  tail, which restores HARDINT, recomputes INTSTAT (it does NOT call crime_interrupt_reassert, so the line is untouched),
  answers a read 0 and returns 1.
* **History**: 40 -> ... -> 141 -> 157 rows; TEN mutation-test tables, each with a written PRETABLE and a mechanical
  prediction checker.  (The sixth-pass brief called the Opus fifth-closing seat's mutants "P1-P7"; table 9 ran four.)
* **ACCEPTS** = 46 ENTRIES: the 40-cell pre-set/re-arm floor + 2 ENDIANESS strengthenings + 4 positional repeats.
* **Free-running vs stepped**: a stepped probe cannot tell debug() from fatal(); a free-running one can (verbose == 0).
* **TIME** updates add 66 x elapsed microseconds -- always EVEN -- so an odd seed stays odd.

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
CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
artifacts/crimewidthkill/ (killtable_20260913/ through killtable10_20260915/):
  1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                       <op> surv (six widths), hi surv, latch surv, sb08 run
  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)   lb/lh/sb/sh pc and exc, lb/lh/lbu/lhu v0
  3. the refused access FALLING INTO THE REGISTER SWITCH -- the goto lost, or narrowed by width, direction, or ADDRESS.
     The switch's observable arms, per refusal cell:
        CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
                                          sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
                                          and the arm's two TESTED idata bits (DOG 0x200, RESET 0x800) each
                                          both ways at 2W, plus ENDIANESS 0x100, which the arm CLEARS
                                          UNCONDITIONALLY and never branches on (written anyway): sh 0x0201,
                                          0x0900, 0x0a00 with sh08 0x0800       sh08b msg, sh08b run
                                          [This said "three TESTED idata bits (... ENDIANESS 0x100)" until
                                          repair 12 -- false; agy, grok, closing pass 6.]
                                          plus ALL-ONES refused writes, sb 0xff and sh 0xffff (kimi CLI,
                                          closing pass), so a fall-through keyed on any bit a 1- or 2-byte
                                          store can carry shows (bits above 15 never reach a refused access,
                                          so a conjunct on them is equivalent)  sb08 msg, sh08b msg/run
        and the refused stores at INTSTAT, INTMASK and TIME carry all-ones (0xff / 0xffff) for the same reason
        CRIME_REV (+0x00), reads AND writes, from pc 0xbfc05180: the PROM-probe hack sets pc = ra (it does not test
                                          the direction)                                    lb/lh/sb/sh rev pc
        CRIME_INTMASK (+0x18), CRIME_INTSTAT (+0x10), all four cells: the arm calls crime_interrupt_reassert(),
                                          which raises cause.IP2 after a SOFTINT store   imask/istat lb, sb, lh, sh
        CRIME_TIME (+0x38), all four cells: the arm advances TIME, which the NEXT read shows   time lb, sb, lh, sh
        the default arm (any unlabelled offset): a debug() line, printed while stepping      lb/lh/sb/sh nodflt,
                                          at +0x07, +0x06, +0x1f, +0x1e, +0x27f  hi nodflt, and
                                          +0x1ff, +0x1fe, +0x1fc                 mid nodflt
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
  4. the latch removed, never set, or KEYED ON THE ACCESS -- the class closed on its single axes after two passes
     found members (F2: `|= len', `|= relative_addr', `<< writeflag'; closing pass: keyed on CRIME_CONTROL, on
     `relative_addr >= 0x40', on address parity).  A keyed latch shows only when the first refusal in a session falls
     where it does not set, so every axis value is a FIRST refusal followed by another, with an announce count:
        width 1 or 2 and direction R or W  warm once (sb, write, odd), latch x5 (lh, read, even)
        each label first                   rev once, sh08b once (CONTROL), istat once, imask once, dog once,
                                           time once, latch x5 (default-arm, low), hi once (the far block,
                                           followed by refusals there and one below 0x40), mid once
     and every label-first session refuses again at ANOTHER label (codex, second closing pass: a latch whose bit is
     keyed on one label, `CRIME_W_LEN << (relative_addr == CRIME_INTMASK)', passed the 111-row version: the imask,
     istat and sh08b sessions refused only at their own label; codex, third closing pass: the middle block likewise
     for address bits 7 and 8 -- mid once now refuses at +0x07 as well)
     and the FIRST refusal's own TEXT in every label-first session (codex, third closing pass: a notice SUPPRESSED at
     one label, or at one address-bit value, and printed by the follow-up instead, still counted one; every said row
     sat at an offset with bit 1 set -- rev said is at +0x00, every address bit clear)
                                            rev said, sh08b said, imask said, istat said, time said, dog said
     and the latch TEST that lets one label through (`|| relative_addr == L'): every label is refused again AFTER the
     latch is set somewhere -- REV and TIME in latch x5's tail (the Opus third-closing seat, measured: they were each
     refused once per session, first, so `|| == CRIME_REV' and `|| == CRIME_TIME' passed)
     and the latch PRE-SET before any refusal, over the KIND x LABEL CROSS (`ACCEPTS'): {8W, 8R, 4W, 4R} at every
     case label, REV also from the PROM-probe window at all four kinds (`ldP' since repair 11 -- this said "in both
     directions" and the window had no 8R; the flagship ruling, closing pass 5), CONTROL's writes at both widths x
     {0x0201, 0x0001, 0, 0x0200} (DOG x leftover, all four; plus 0x0100 ENDIANESS at both widths, a clause-(e)
     strengthening -- the arm never branches on it), and the default arm's six kinds in both 4-byte lanes -- all in
     latch x5's prologue, before its first refusal; also warm once (sd first) and time once (ld first).  HARD_RESET's
     true side: disclosed (it stops the CPUs).  *** This said "DERIVED FROM THE FUNCTION'S OWN BRANCHES ... both sides
     of every `if'" after repair 9, and the fourth closing pass measured it short: each branch's sides were taken
     SOMEWHERE, not crossed with the label -- a pre-set on an accepted 8-byte WRITE at +0x10 and on CONTROL's 0x0200 cell
     each scored 131/131 on the 131-row test (the Opus seat; deepseek, kimi CLI by reading). ***
  5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
     session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
     debug() would not -- on EVERY axis of the refusal: bits 0-2 (free said, +0x07), bits 3-8 and len 2 (free 2r said,
     +0x1f8), bit 9 and a write (free 1w said, +0x27f), a 2-byte write at a label (free 2w said, CONTROL), and each
     remaining label (free rev/istat/imask/dog/time said), and the ISSUING PC -- a refusal from the PROM-probe window
     (free revP said, repair 12; glm, closing pass 6: `(pc in the window ? debug : fatal)(' scored 141/141 on the 141-row
     test -- clause (e)
     by the DEPENDS-ON bound, rowed as a strengthening).  *** Until repair 10 the channel was pinned at ONE cell (+0x07):
     `(relative_addr & 8 ? debug : fatal)(' and `(len == 2 ? debug : fatal)(' each scored 131/131 on the 131-row test (codex, the Opus
     seat, fourth closing pass).  One refusal per free-running session -- the latch silences any second one. ***
  6. the ACCEPT SET shrunk at any single cell IN THE GUARD-GROWTH FORM -- an accept guard grown by a conjunct, so the
     cell falls into the announcing decline arm (the de-escalation clause: the deleted exit(1) used to announce exactly
     this) -- at EVERY ACCEPTS cell by `latch said': latch x5 runs all 46 ACCEPTS accesses before the lh +0x06, so a
     wrongly declined accepted cell steals that lh's own announce (repair 12; codex's C1 and the Opus seat's G1-G5 each
     scored 141/141 on the 141-row test, because `latch x5' and `rearm once' COUNT notices and a stolen notice keeps the
     count at 1).  *** This item said "the ACCEPT SET shrunk at any single cell" with no form, and it was false at
     CONTROL 4R/8R/8W, INTSTAT 8, TIME 4, INTMASK 4W and the REV window 4W (closing pass 6, measured). ***
     The SILENT form -- a bypass inserted before the width test that declines an accepted cell with NO announce (the
     Opus seat's G6) -- is outside the de-escalation class and DISCLOSED by class; it is CAUGHT where a bypassed cell is
     guest-visible AND THE CATCHING ROW RUNS IN THE BYPASS'S OWN LATCH STATE, by the value rows derived per cell
     (repair 12): REV window 4W/8W/8R (revP sw/sd/ld pc), CONTROL 8R
     (acc ctl ld) and 8W (acc ctl sd), INTSTAT 8R (acc istat ld), 8W and 4W (istw sd, istw sw), INTMASK 4W (acc imask
     sw), TIME 8W (acc time sd), the default arm's 4W/4R at +0x40 (acc 40 sw, acc 40 lw); and it is EQUIVALENT at REV
     8W/4W/4R outside the window (the prelude rewrites REV; its high half is 0) and CONTROL 4R (reads 0 either way).
     *** THIS SENTENCE ALSO LISTED "TIME 4W/4R (the high half is 0; updates accumulate)" AS EQUIVALENT, AND BOTH THE
     CLAIM AND ITS STATED REASON ARE MEASURED FALSE -- closing pass 7, artifacts/crimewidthkill/opus_close7_20260915/
     OPUS_REPORT.md, mutant E2 at 157/157 on the 157-row test, with the difference on FOUR channels.  A read takes `odata' BEFORE its own
     crime_update_crime_time(), so an update skipped at the 4-byte access ARRIVES ONE ACCESS LATE rather than
     accumulating: free-running ld;sw;ld reads 0xc6 then 0x108 on base and 0x0 under the bypass, six times out of six
     each way.  TIME 4W/4R is
     GUEST-VISIBLE AND UNROWED -- a single-axis floor cell, owed by repair 13 in the GAPPED step shape
     (opus_close7_20260915/scripts2/post7c.py; the two obvious shapes were measured VACUOUS by the seat that wrote
     them, which is why the CHANNEL line has to be CHECKED against its mutant and not merely written). ***
     *** AND THE "CAUGHT" CLAUSE ABOVE CARRIED NO LATCH QUALIFIER UNTIL THAT SAME PASS, WHICH MADE IT FALSE OF A
     LATCH-CONDITIONED BYPASS.  K1/K2/K3 -- `&& !(<cell> && (d->warned & CRIME_W_LEN))' at INTMASK 4W, at the REV
     4-byte cell and at CONTROL 8R -- EACH SCORE 157/157 on the 157-row test, because the value row for each cell is measured
     only while the latch is CLEAR.  Eight of the guest-visible cells ARE already pinned post-latch and the rest are
     not; the map is derived in opus_close7_20260915/scripts2/session_map2.py, not asserted here. ***
     *** AND "The remaining ACCEPTS cells' accept side is pinned by the rows below" IS FALSE IN THREE PLACES, all
     measured in the same pass, all on the 157-row test: sw +0x04 (F3, 157/157 -- guest-equivalent, a host WRITE line nothing
     counts), CONTROL 0x0201 at BOTH widths (F1/F1b, 157/157 on the 157-row test -- host-log only, a multi-axis idata joint, so clause-(e)
     debt rather than floor), and EIGHT cells whose only pin is an INCIDENTAL access in another session that no
     enumeration names.  The honest statement: the cells enumerated above are ROWED; the others are pinned where a row
     happens to touch them, and which those are is a derivation, not a claim. ***  The ACCEPT set also at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
     prelude writes; grok, closing pass: `len == 8 && relative_addr != 0' passed the 85-row version, whose rows sat at
     +0x30 -- an interior slot, not an end), with devsig the 4R-low cell there and `rev pc ctl' the 4R-high one (its
     redirect needs the access ACCEPTED; `devsig hi' reads 0 either way -- grok, codex, second closing pass, correcting
     this sentence, which credited devsig hi); CRIME_DOG +0x30 -- acc8 st+ld
     (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi; the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w.  Those rows are ROUND TRIPS and cannot see an
     accept arm that re-maps its register index (kimi-k3:cloud, F2: `d->reg[(relative_addr & 0x3f) / 8]' passed the
     71-row version), so one row is ANCHORED: `top8 anchor' reads bank-1 control at +0x210, a value the PRELUDE writes
     by bank index (1 for -M 64), not by the decode under test; `top4 anchor' reads its low half with a 4R.  The 4R
     of its HIGH half answers 0 accepted or refused, so that cell is pinned by the ANNOUNCE instead (Opus closing:
     `len == 4 && relative_addr != 0x210' passed the 85-row version): every accept cell the top session touches
     before its one refusal is pinned the same way                                                      top said
     *** It pins the model's CURRENT bank layout, which the
     filed `crimebankorder' disputes; a round that re-orders the banks owes this row's re-derivation. ***
  7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps;
     and a seeded slot with address bit 4 CLEAR (+0x40; the Opus third-closing seat, measured: every read-back refused
     store had bit 4 set, so a landing keyed on bit 4 clear passed), including a refused HALFWORD with address bit 1
     SET at +0x42 (codex, the Opus seat, fourth closing pass: every read-back refused 2-byte store cleared bit 1, and a
     2W landing keyed on it scored 131/131 on the 131-row test)                                                             lo keeps
     and at the far block, a refused sb +0x27f and sh +0x27c leave the SEEDED +0x278 as seeded (Opus, F2 and closing: a
     store landing only >= 0x200, of either width; this said "reading 0" until the fourth closing pass -- repair 8
     seeded the slot)                                                                                   hi keeps
     and in the middle of the window (+0x1ff / +0x1fc, every address bit 0-8 set)                       mid keeps
     and at INTMASK, read back by an accepted ld (kimi CLI, second closing pass: a landing that ORs into INTMASK kept
     bit 28, so imask ctl could not see it)                                                             imask keeps
  8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
     `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
     warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
     4-byte arm's re-arm open on the closing pass -- now the KIND x LABEL CROSS, the SAME list as item 4's pre-set
     (`ACCEPTS', 46 ENTRIES since repair 11 (SIX kinds -- see the repair-12 bullet; this said `46 kinds' and the same header said `46 ENTRIES, not 46 kinds' twenty lines down: grok's nit, confirmed and corrected at BOTH sites) -- 43 before `ldP' and the two ENDIANESS writes; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing seat:
     CONTROL's read, DOG-clear and zero-leftover sides; the fourth closing pass: a re-arm on an accepted WRITE at
     INTSTAT/INTMASK or REV and on CONTROL's 0x0200 cell, each 131/131 on the 131-row test) -- each accepted kind between two refusals
                                                                                            rearm once, rearm surv
     and in the middle block (an accepted sd between two refusals there)                                mid once
  9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
     (codex, closing pass: `if (relative_addr == CRIME_REV) odata = 1;' passed the 85-row version -- the REV rows
     checked only the pc)          lb/lh rev v0, ctl v0, ctl lb v0, istat/imask lb/lh v0, dog v0, dog lh v0, time lb/lh v0
     every one at 2 bytes (lh sees every value lb sees) and over a register whose LOW BYTES ARE NONZERO, so a decline
     that answers the register shows (kimi CLI, second closing pass: INTSTAT, INTMASK and DOG held 0 in their low
     bytes and `odata = d->reg[relative_addr / 8]' there passed; codex: `odata = 0x100' at DOG passed the lb-only row)
     -- REV 0x11, CONTROL 0x100, TIME 66-990 (low bytes); INTSTAT/INTMASK 0x0101010111010101 and DOG
     0x0123456789abcdef, nonzero in EVERY byte, so any SHIFT of the register's bytes into the answer shows (Opus, second
     closing pass: the ADDRESSED lanes passed the 0x10000001 seed 121/121 on the 121-row test; glm, third closing pass:
     the 4-byte path's half, `reg >> 32', passed the 0x0101000010000001 one).  [A selection CONFINED above byte 1 --
     `& 0xffff0000' -- answers 0 to every lb/lh by construction and is EQUIVALENT; this said "ANY selection ... shows"
     until the kimi CLI seat, fourth closing pass.]  And the answer SOURCE other than the addressed register: every
     lvalue the function reads that is NONZERO in some session is nonzero where a refused answer is read in that
     session, HARDINT included -- latched only in the gate session, where refused lb/lh now read it -- and SOFTINT
     (nonzero in the imask/istat/gate sessions; the Opus fifth-closing seat measured `odata = SOFTINT' red there).
     [Corrected 2026-09-14, flagship ruling on closing pass 5: this said "every lvalue the function reads is nonzero
     where a refused answer is read" -- FALSE: `d->use_fb', `flag_for_128MB' and `idata' are 0 at every refused read,
     and `odata = d->use_fb' scored 141/141 on the 141-row test (the Opus seat).  Those are DISCLOSED below.]  The HARDINT source (kimi-k3:cloud, the Opus seat, fourth closing pass: a decline answering
     `d->reg[CRIME_HARDINT / 8]' scored 131/131 on the 131-row test)                                          gate lb v0, gate lh v0.
     CONTROL is answered at both widths (ctl lb v0, ctl v0; the Opus
     third-closing seat, measured: `odata = 1' keyed on len 1 at CONTROL passed the lh-only row); its low byte is 0, so
     only a CONSTANT answer can show at lb there.  TIME: at the time rows' refused reads TIME is a multiple of 66 and is
     0 in 42 of 800 logged cells (the same seat -- this said "0.3% of runs, 66-990 includes 256, 512, 768", and those
     are not multiples of 66), so the register cell is pinned by a SEEDED odd TIME instead     time sd lb v0, time sd lh v0
     and in the far block and the middle block over a NONZERO slot, at both widths (Opus closing: a refused read
     >= 0x200 answering the register; Opus, second closing pass: the 2-byte cell there)
                                                                   top rd v0, top rd2 v0, mid lb v0, mid lh v0
  10. the decline HOLDS WHILE AN INTERRUPT IS LATCHED: HARDINT set by the guest through MACE and the CRIME line
      asserted, a refused sh 0x0800 at CONTROL still does not stop the CPUs (the Opus closing seat: `if
      (!d->reg[CRIME_HARDINT / 8])' -- a field the tail reads -- and `if (!d->prev_asserted)' passed the 85-row
      version)                                        gate run, with gate hardint and gate line as its controls
      and a refused READ answers 0 while HARDINT is latched -- the answer SOURCE item 9 names (fourth closing pass)
                                                                                                 gate lb v0, gate lh v0

*** THE LATCH-KEYED ACCEPT SHRINK (the K-CLASS) AND ITS CLOSURE -- repair 13, and it is the reason this probe grew
from 157 rows to 188. ***

An accept guard grown with a conjunct on THIS FIX'S OWN LATCH -- `&& !(<cell> && (d->warned & CRIME_W_LEN))' -- declines
SILENTLY at that cell once any refusal has happened, because the latch is exactly what suppresses the announce.  Three
instances were MEASURED at 157/157 with a guest loss on the 157-row instrument (closing pass 7, opus_close7_20260915/
OPUS_REPORT.md): K1 at INTMASK 4W, K2 at the REV 4-byte cell, K3 at CONTROL 8R.  Every value row this probe had was
measured with the latch CLEAR, so none of them could see it.

*** THE GRADE IS FLOOR, NOT CLAUSE (e), and that OVERTURNED THE PRIOR RULING (FABLE_C5_RULING_20260915.md, S-A.7;
FABLE_C4_RULING's RA3 corrected in place).  The reason is in the fix's own diff: the width dispatch's `else' arm READS
`d->warned', in a hunk this diff ADDS -- so the latch is a device-state lvalue the fix's own repair path reads, which
the pass-11 floor definition and the M_ICLR precedent make a floor axis. ***

THE ENUMERATION is the four-axis product {latch clear, set} x {len 4, 8} x {read, write} x {the 7 labels the switch
distinguishes: REV, CONTROL, INTSTAT, INTMASK, DOG, TIME, default} = 56 cells.  The latch-CLEAR half is table 10's
twelve S_* silent bypasses.  **THE ROWS OWED ARE NOT ALL 28 LATCH-SET MUTANTS AND NOT ALL 56 CELLS**: a mutant at an
equivalent or already-pinned cell teaches nothing and a row at a cell no mutant reaches is unfalsifiable, so the FLOOR
is the INTERSECTION.  Over the 46 ACCEPTS entries:

    23  ROWED HERE, post-latch, by the `p *' sessions below (the REV window, the value session, the INTSTAT reassert
        channel, the TIME pair, and the residual ACCEPT cells).  Every one runs AFTER a refused lb at +0x07, so the
        latch is SET while the row is measured -- which is the whole point.
     8  ALREADY PINNED post-latch by an incidental access in an existing session.  Derived, not asserted:
        opus_close7_20260915/scripts2/session_map2.py (static, no emulator) maps all 45 sessions and finds 72 accepted
        accesses after their session's first refusal, in 11 sessions, 10 carrying an oracle.
    10  EQUIVALENT at the guest -- nothing to observe, so no row is owed or possible.
     5  HOST-DIAGNOSTIC ONLY: clause-(e) debt, DISCLOSED with its measurements rather than rowed -- CONTROL 0x0201 at
        both widths (F1/F1b, 157/157 on the 157-row test: the `unimplemented' count drops to one, `CTL after ld' is 0x100 either way, and
        the guard is a MULTI-AXIS idata joint, which the 2026-09-04 pass-11 amendment puts in debt) and the `sw +0x04'
        write line (F3, 157/157 on the 157-row test: guest-equivalent; `dflt ctl' counts READS at +0x04, none counts writes).
    --
    46  = the ACCEPTS entry count (46 ENTRIES, six KINDS).

*** THE TIME 4W/4R PAIR IS A FLOOR CELL AND ITS ROWS NEEDED A PARTICULAR SHAPE, which is this repair's own evidence
that a CHANNEL line must be RUN against its mutant and not merely written.  The seat that proposed the rows measured
its own first two shapes VACUOUS, and one gave a FALSE RED on a control.  Only the GAPPED form discriminates: the
refused lb and the first 8R in one `step 2', the 4-byte cell in its own `step 1', the final 8R in another -- the
debugger's pause BETWEEN steps is the gap, so an update that happens lands before the final read and one that is
skipped arrives after it.  ~13,000x separation (base 0x13414f8 against the bypass's 0x5ee), reproduced here. ***

DISCLOSED, not rowed:
  * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
    (#95, src/cpus/memory_rw.c -- `if (writeflag == MEM_READ)' then `memset(data, 0, len);', immediately above
    `paddr -= mem->devices[i].baseaddr;'), and on a declined access nothing between the entry and the tail writes
    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 (the then 40-row test) in kill table 1.
  * a fall-through confined to the THREE label cells whose arms have NO body for that access, all EQUIVALENT:
      CRIME_DOG (0x30)          `No warning.' -- the arm is `break;'
      CRIME_CONTROL, reads      the arm acts only on MEM_WRITE
      CRIME_REV, outside the PROM-probe window   the arm acts only when the pc is in the window
    The first two measured as survivors in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through); the REV
    cell is the `lb/lh rev pc' rows' converse, read from the arm.  [This said "the two label cells" until repair 12 --
    kimi CLI, closing pass 6.]
  * ACCEPT cells at unrowed slots: the rows touch accepted accesses at +0x00, +0x04, +0x08, +0x10, +0x18, +0x30,
    +0x34, +0x38, +0x40, +0x210, +0x214, +0x1f8 and +0x278 (not an exhaustive list of what the window accepts); an
    accept arm narrowed by an address strictly INSIDE the window at an unrowed slot (e.g. `len == 8 && relative_addr !=
    0x100', kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.  TOUCHING a slot in ACCEPTS pins its LATCH
    behaviour, never its acceptance -- what pins acceptance is item 6 (`latch said' for the announced form, the value
    rows for the silent form).  [This bullet implied a touched slot was pinned until repair 12 -- the Opus seat, closing
    pass 6.]
  * an effect ADDED to the decline arm and keyed on ONE UNNAMED offset (item 9 rows the READ answer at every named
    label) -- a refused store that lands only at
    +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only at
    +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at eight default-arm
    offsets; the keeps rows catch a landing at CRIME_DOG, INTMASK, the far block and the middle block.  An effect
    keyed on a single ADDRESS BIT is NOT in this class: every bit 0-9 is carried both ways by a refused access of each
    kind that can carry it (the mid session sets bits 0-8, the far block bit 9; an aligned 2-byte access never sets
    bit 0; kimi-k3:cloud, second closing pass, found bits 7 and 8 carried by no refusal at all; codex and the Opus seat,
    fourth closing pass, found 2W LANDING at bit 1 set carried by no read-back store -- now +0x42, `lo keeps').  Note
    `relative_addr / 8': a refused halfword at +0x1e would land on INTMASK's slot, not at +0x1e; the 2W session's
    +0x1e store is not read back, and the INTMASK landing is carried by `imask keeps'.  A landing at
    CRIME_SOFTINT (0x20, not a switch label) is in this class (deepseek, third closing pass).  ONE NAMED CELL IS
    OPEN AND SAID SO (kimi-k3:cloud, closing pass): a refused sb/sh that LANDS only at CRIME_TIME stores <= 0xffff,
    which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
    (the tail recomputes it), CONTROL and REV (the prelude rewrites them) such a landing is EQUIVALENT.
  * a ROUND TRIP cannot observe an accepted WRITE at +0x00 or +0x08 (the prelude rewrites CRIME_REV and CRIME_CONTROL
    on every access) -- but the write's EFFECTS can, and are rowed: from the PROM-probe window an accepted write
    REDIRECTS the pc (revP sw pc, revP sd pc), and at CONTROL the arm's effects (sw08 halts, sw08 msg ctl at 4 bytes;
    acc ctl sd at 8).  [This bullet said "no round trip there can observe whether the store was accepted" as though
    nothing could, and it was wrong twice: the window redirect (measured by the Opus seat, G4) and the 8-byte CONTROL
    write, which no row carried until repair 12 -- closing pass 6.]  The 4R-high cell at +0x00 is carried by `rev pc
    ctl' (its redirect needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
  * `odata = idata' in the decline arm: EQUIVALENT by construction -- `idata' is set only under MEM_WRITE and `odata' is
    consumed only under MEM_READ (measured 141/141 on the 141-row test by the Opus seat, closing pass 6).  `cpu->is_32bit' (the REV arm's
    pc-pointer refresh) holds one value per machine, like the configuration lvalues above.  Accepted-side address bits 7
    and 8: the mid session's accepted sd +0x1f8 carries both, before and between its refusals (a latch keyed on them is
    killed -- kimi-k3's C3, 139/141 on the 141-row test); an ACCEPT arm keyed on them is the unrowed-slot class above.
  * ACCEPTS has 46 ENTRIES, not 46 kinds: the 40-cell pre-set/re-arm floor, the two ENDIANESS strengthenings, and four
    positional repeats of default-arm kinds (`sw/lw 0x04' repeat 0x34's low lane; `sd/ld 0x278' repeat 0x40's 8-byte
    kinds, and are the prologue's only accepted access with address bit 9 set -- an unrecorded strengthening until
    repair 12; kimi CLI, closing pass 6).
  * a decline answering a selection of the register's bytes at CRIME_REV, CRIME_CONTROL or CRIME_TIME CONFINED to
    bytes the model holds at 0 there -- REV = 0x11: bytes 1-7; CONTROL = 0x100: byte 0 and bytes 2-7; TIME: the 4-byte
    half above the low word -- is EQUIVALENT (the prelude rewrites REV and CONTROL on every access; TIME is kept to 32
    bits).  [Corrected 2026-09-14 from closing pass 5 (glm): this read "the ADDRESSED lanes (bytes 0-1 at a label)",
    which at REV and CONTROL include a NONZERO byte -- item 9's v0 rows exist to catch exactly that selection.]  At
    INTSTAT, INTMASK and DOG every byte is seeded nonzero, so any selection shows (Opus, second closing pass; glm, third).
  * a latch keyed on a JOINT predicate (e.g. only 2-byte refusals at CRIME_TIME), or on one unnamed offset other than the
    default-arm cells the latch rows refuse at: clause (e), the single-axis generating set being the floor.
  * (closing pass 5; the Opus seat measured each at 141/141 on the 141-row test; the flagship ruling graded each clause
    (e)) a latch re-armed or pre-set by a CONTROL write's ENDIANESS bit (0x100) -- the arm clears it unconditionally and
    never branches on it; the two ENDIANESS writes in ACCEPTS since repair 11 are a strengthening, not a floor claim
    over value bits; the announce CHANNEL keyed on a JOINT of axes (e.g. `(relative_addr == CRIME_INTSTAT && len == 2 ?
    debug : fatal)(') -- item 5 rows the channel on each SINGLE axis; and a decline answering a MACHINE-CONFIGURATION
    lvalue (`d->use_fb', `flag_for_128MB'), which holds one value per machine and is 0 on this probe's -M 64 non-graphics
    ip32 -- a graphics O2 (use_fb = 1) would see `odata = d->use_fb' answer 1.  Unrowable on one machine, like the
    function-static latch below.
  * a re-arm or pre-set inside the HARD_RESET branch of the CONTROL arm: an accepted write that takes it stops every
    CPU, so nothing can follow it in the session.  Unrowable, not merely unrowed.
  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 (the 71-row test) by the Opus seat
    (F2, `sft'); it is the single-unnamed-offset class of the bullet above.
  * a FUNCTION-STATIC latch in place of `d->warned' is NOT equivalent in general -- two IP32 machines in one gxemul
    process would share it -- and this single-machine probe cannot see it (kimi-k3:cloud, F2; the pass-2 Opus seat had
    recorded it "equivalent", which holds only for one machine per process).
  * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
    not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.
  * independence between two CRIME instances (the latch is per instance by construction; IP32 has one CRIME).

```

## THE REPAIR DIFF -- repair 11 -> repair 12 (141 -> 157 rows) (`git diff --no-index`, verbatim; 8 hunks)

```diff
diff --git "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable10_20260915\\crime_width_probe.table10.py" "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
index ccb780d..df49dab 100644
--- "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable10_20260915\\crime_width_probe.table10.py"
+++ "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
@@ -89,5 +89,6 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable10_20260915/):
      +0x1f8), bit 9 and a write (free 1w said, +0x27f), a 2-byte write at a label (free 2w said, CONTROL), and each
      remaining label (free rev/istat/imask/dog/time said), and the ISSUING PC -- a refusal from the PROM-probe window
-     (free revP said, repair 12; glm, closing pass 6: `(pc in the window ? debug : fatal)(' scored 141/141 -- clause (e)
+     (free revP said, repair 12; glm, closing pass 6: `(pc in the window ? debug : fatal)(' scored 141/141 on the 141-row
+     test -- clause (e)
      by the DEPENDS-ON bound, rowed as a strengthening).  *** Until repair 10 the channel was pinned at ONE cell (+0x07):
      `(relative_addr & 8 ? debug : fatal)(' and `(len == 2 ? debug : fatal)(' each scored 131/131 on the 131-row test (codex, the Opus
@@ -102,10 +103,29 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable10_20260915/):
      The SILENT form -- a bypass inserted before the width test that declines an accepted cell with NO announce (the
      Opus seat's G6) -- is outside the de-escalation class and DISCLOSED by class; it is CAUGHT where a bypassed cell is
-     guest-visible, by the value rows derived per cell (repair 12): REV window 4W/8W/8R (revP sw/sd/ld pc), CONTROL 8R
+     guest-visible AND THE CATCHING ROW RUNS IN THE BYPASS'S OWN LATCH STATE, by the value rows derived per cell
+     (repair 12): REV window 4W/8W/8R (revP sw/sd/ld pc), CONTROL 8R
      (acc ctl ld) and 8W (acc ctl sd), INTSTAT 8R (acc istat ld), 8W and 4W (istw sd, istw sw), INTMASK 4W (acc imask
      sw), TIME 8W (acc time sd), the default arm's 4W/4R at +0x40 (acc 40 sw, acc 40 lw); and it is EQUIVALENT at REV
-     8W/4W/4R outside the window (the prelude rewrites REV; its high half is 0), CONTROL 4R (reads 0 either way) and TIME
-     4W/4R (the high half is 0; updates accumulate).  The remaining ACCEPTS cells' accept side is pinned by the rows
-     below.  The ACCEPT set also at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
+     8W/4W/4R outside the window (the prelude rewrites REV; its high half is 0) and CONTROL 4R (reads 0 either way).
+     *** THIS SENTENCE ALSO LISTED "TIME 4W/4R (the high half is 0; updates accumulate)" AS EQUIVALENT, AND BOTH THE
+     CLAIM AND ITS STATED REASON ARE MEASURED FALSE -- closing pass 7, artifacts/crimewidthkill/opus_close7_20260915/
+     OPUS_REPORT.md, mutant E2 at 157/157 on the 157-row test, with the difference on FOUR channels.  A read takes `odata' BEFORE its own
+     crime_update_crime_time(), so an update skipped at the 4-byte access ARRIVES ONE ACCESS LATE rather than
+     accumulating: free-running ld;sw;ld reads 0xc6 then 0x108 on base and 0x0 under the bypass, six times out of six
+     each way.  TIME 4W/4R is
+     GUEST-VISIBLE AND UNROWED -- a single-axis floor cell, owed by repair 13 in the GAPPED step shape
+     (opus_close7_20260915/scripts2/post7c.py; the two obvious shapes were measured VACUOUS by the seat that wrote
+     them, which is why the CHANNEL line has to be CHECKED against its mutant and not merely written). ***
+     *** AND THE "CAUGHT" CLAUSE ABOVE CARRIED NO LATCH QUALIFIER UNTIL THAT SAME PASS, WHICH MADE IT FALSE OF A
+     LATCH-CONDITIONED BYPASS.  K1/K2/K3 -- `&& !(<cell> && (d->warned & CRIME_W_LEN))' at INTMASK 4W, at the REV
+     4-byte cell and at CONTROL 8R -- EACH SCORE 157/157 on the 157-row test, because the value row for each cell is measured
+     only while the latch is CLEAR.  Eight of the guest-visible cells ARE already pinned post-latch and the rest are
+     not; the map is derived in opus_close7_20260915/scripts2/session_map2.py, not asserted here. ***
+     *** AND "The remaining ACCEPTS cells' accept side is pinned by the rows below" IS FALSE IN THREE PLACES, all
+     measured in the same pass, all on the 157-row test: sw +0x04 (F3, 157/157 -- guest-equivalent, a host WRITE line nothing
+     counts), CONTROL 0x0201 at BOTH widths (F1/F1b, 157/157 on the 157-row test -- host-log only, a multi-axis idata joint, so clause-(e)
+     debt rather than floor), and EIGHT cells whose only pin is an INCIDENTAL access in another session that no
+     enumeration names.  The honest statement: the cells enumerated above are ROWED; the others are pinned where a row
+     happens to touch them, and which those are is a derivation, not a claim. ***  The ACCEPT set also at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
      prelude writes; grok, closing pass: `len == 8 && relative_addr != 0' passed the 85-row version, whose rows sat at
      +0x30 -- an interior slot, not an end), with devsig the 4R-low cell there and `rev pc ctl' the 4R-high one (its
@@ -136,5 +156,5 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable10_20260915/):
      warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
      4-byte arm's re-arm open on the closing pass -- now the KIND x LABEL CROSS, the SAME list as item 4's pre-set
-     (`ACCEPTS', 46 kinds since repair 11 -- 43 before `ldP' and the two ENDIANESS writes; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing seat:
+     (`ACCEPTS', 46 ENTRIES since repair 11 (SIX kinds -- see the repair-12 bullet; this said `46 kinds' and the same header said `46 ENTRIES, not 46 kinds' twenty lines down: grok's nit, confirmed and corrected at BOTH sites) -- 43 before `ldP' and the two ENDIANESS writes; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing seat:
      CONTROL's read, DOG-clear and zero-leftover sides; the fourth closing pass: a re-arm on an accepted WRITE at
      INTSTAT/INTMASK or REV and on CONTROL's 0x0200 cell, each 131/131 on the 131-row test) -- each accepted kind between two refusals
@@ -158,5 +178,5 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable10_20260915/):
      [Corrected 2026-09-14, flagship ruling on closing pass 5: this said "every lvalue the function reads is nonzero
      where a refused answer is read" -- FALSE: `d->use_fb', `flag_for_128MB' and `idata' are 0 at every refused read,
-     and `odata = d->use_fb' scored 141/141 (the Opus seat).  Those are DISCLOSED below.]  The HARDINT source (kimi-k3:cloud, the Opus seat, fourth closing pass: a decline answering
+     and `odata = d->use_fb' scored 141/141 on the 141-row test (the Opus seat).  Those are DISCLOSED below.]  The HARDINT source (kimi-k3:cloud, the Opus seat, fourth closing pass: a decline answering
      `d->reg[CRIME_HARDINT / 8]' scored 131/131 on the 131-row test)                                          gate lb v0, gate lh v0.
      CONTROL is answered at both widths (ctl lb v0, ctl v0; the Opus
@@ -175,4 +195,45 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable10_20260915/):
                                                                                                  gate lb v0, gate lh v0
 
+*** THE LATCH-KEYED ACCEPT SHRINK (the K-CLASS) AND ITS CLOSURE -- repair 13, and it is the reason this probe grew
+from 157 rows to 188. ***
+
+An accept guard grown with a conjunct on THIS FIX'S OWN LATCH -- `&& !(<cell> && (d->warned & CRIME_W_LEN))' -- declines
+SILENTLY at that cell once any refusal has happened, because the latch is exactly what suppresses the announce.  Three
+instances were MEASURED at 157/157 with a guest loss on the 157-row instrument (closing pass 7, opus_close7_20260915/
+OPUS_REPORT.md): K1 at INTMASK 4W, K2 at the REV 4-byte cell, K3 at CONTROL 8R.  Every value row this probe had was
+measured with the latch CLEAR, so none of them could see it.
+
+*** THE GRADE IS FLOOR, NOT CLAUSE (e), and that OVERTURNED THE PRIOR RULING (FABLE_C5_RULING_20260915.md, S-A.7;
+FABLE_C4_RULING's RA3 corrected in place).  The reason is in the fix's own diff: the width dispatch's `else' arm READS
+`d->warned', in a hunk this diff ADDS -- so the latch is a device-state lvalue the fix's own repair path reads, which
+the pass-11 floor definition and the M_ICLR precedent make a floor axis. ***
+
+THE ENUMERATION is the four-axis product {latch clear, set} x {len 4, 8} x {read, write} x {the 7 labels the switch
+distinguishes: REV, CONTROL, INTSTAT, INTMASK, DOG, TIME, default} = 56 cells.  The latch-CLEAR half is table 10's
+twelve S_* silent bypasses.  **THE ROWS OWED ARE NOT ALL 28 LATCH-SET MUTANTS AND NOT ALL 56 CELLS**: a mutant at an
+equivalent or already-pinned cell teaches nothing and a row at a cell no mutant reaches is unfalsifiable, so the FLOOR
+is the INTERSECTION.  Over the 46 ACCEPTS entries:
+
+    23  ROWED HERE, post-latch, by the `p *' sessions below (the REV window, the value session, the INTSTAT reassert
+        channel, the TIME pair, and the residual ACCEPT cells).  Every one runs AFTER a refused lb at +0x07, so the
+        latch is SET while the row is measured -- which is the whole point.
+     8  ALREADY PINNED post-latch by an incidental access in an existing session.  Derived, not asserted:
+        opus_close7_20260915/scripts2/session_map2.py (static, no emulator) maps all 45 sessions and finds 72 accepted
+        accesses after their session's first refusal, in 11 sessions, 10 carrying an oracle.
+    10  EQUIVALENT at the guest -- nothing to observe, so no row is owed or possible.
+     5  HOST-DIAGNOSTIC ONLY: clause-(e) debt, DISCLOSED with its measurements rather than rowed -- CONTROL 0x0201 at
+        both widths (F1/F1b, 157/157 on the 157-row test: the `unimplemented' count drops to one, `CTL after ld' is 0x100 either way, and
+        the guard is a MULTI-AXIS idata joint, which the 2026-09-04 pass-11 amendment puts in debt) and the `sw +0x04'
+        write line (F3, 157/157 on the 157-row test: guest-equivalent; `dflt ctl' counts READS at +0x04, none counts writes).
+    --
+    46  = the ACCEPTS entry count (46 ENTRIES, six KINDS).
+
+*** THE TIME 4W/4R PAIR IS A FLOOR CELL AND ITS ROWS NEEDED A PARTICULAR SHAPE, which is this repair's own evidence
+that a CHANNEL line must be RUN against its mutant and not merely written.  The seat that proposed the rows measured
+its own first two shapes VACUOUS, and one gave a FALSE RED on a control.  Only the GAPPED form discriminates: the
+refused lb and the first 8R in one `step 2', the 4-byte cell in its own `step 1', the final 8R in another -- the
+debugger's pause BETWEEN steps is the gap, so an update that happens lands before the final read and one that is
+skipped arrives after it.  ~13,000x separation (base 0x13414f8 against the bypass's 0x5ee), reproduced here. ***
+
 DISCLOSED, not rowed:
   * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
@@ -217,8 +278,8 @@ DISCLOSED, not rowed:
     ctl' (its redirect needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
   * `odata = idata' in the decline arm: EQUIVALENT by construction -- `idata' is set only under MEM_WRITE and `odata' is
-    consumed only under MEM_READ (measured 141/141 by the Opus seat, closing pass 6).  `cpu->is_32bit' (the REV arm's
+    consumed only under MEM_READ (measured 141/141 on the 141-row test by the Opus seat, closing pass 6).  `cpu->is_32bit' (the REV arm's
     pc-pointer refresh) holds one value per machine, like the configuration lvalues above.  Accepted-side address bits 7
     and 8: the mid session's accepted sd +0x1f8 carries both, before and between its refusals (a latch keyed on them is
-    killed -- kimi-k3's C3, 139/141); an ACCEPT arm keyed on them is the unrowed-slot class above.
+    killed -- kimi-k3's C3, 139/141 on the 141-row test); an ACCEPT arm keyed on them is the unrowed-slot class above.
   * ACCEPTS has 46 ENTRIES, not 46 kinds: the 40-cell pre-set/re-arm floor, the two ENDIANESS strengthenings, and four
     positional repeats of default-arm kinds (`sw/lw 0x04' repeat 0x34's low lane; `sd/ld 0x278' repeat 0x40's 8-byte
@@ -766,5 +827,6 @@ x, _ = ld(A, "lb", CRIME + 0x07, "v0"); c += x
 #  0x0100 (ENDIANESS) writes are a CLAUSE-(e) STRENGTHENING, not floor: the arm clears ENDIANESS unconditionally and
 #  never branches on it, so it is outside CONTROL's generating set {DOG, HARD_RESET, leftover}; they are here only
-#  because the Opus seat measured them killing an ENDIANESS-keyed latch with no row disturbed.  46 kinds. ***
+#  because the Opus seat measured them killing an ENDIANESS-keyed latch with no row disturbed.  46 ENTRIES, six
+#  KINDS -- this line said `46 kinds', the second of the two sites grok's nit named. ***
 ACCEPTS = (("sd", 0x00, 0), ("ld", 0x00, 0), ("sw", 0x00, 0), ("lw", 0x00, 0),
            ("lwP", 0x00, 0), ("swP", 0x00, 0), ("sdP", 0x00, 0),
@@ -1085,4 +1147,176 @@ row("istw mid", ip2(nth(t, "cause", 2)), "clear", "CONTROL: lowered again (SOFTI
 row("istw sw", ip2(nth(t, "cause", 3)), "set", "accepted sw +0x10 reasserts: IP2 set")
 
+# ============================================================================================
+#  REPAIR 13 DRAFT -- NOT APPLIED.  Splice this block into crime_width_probe.py immediately
+#  before its `npass = sum(...)' tail, once Fable has ruled on the CLOSURE SHAPE (question A4.1
+#  of _scratchpad/fable_adj_20260915b.md).  Every session below is owed under ANY ruling: they
+#  are the rows that catch the K-class at the cells the close-7 seat MEASURED, in the shapes it
+#  measured them in (opus_close7_20260915/scripts2/post7.py, post7c.py -- base 29/29, K1 28/29,
+#  K2 27/29, K3 28/29, four negative controls 29/29).  What Fable's answer changes is how many
+#  MORE cells the closure product adds, not whether these belong.
+#
+#  THE ONE STRUCTURAL IDEA, and it is the whole repair: every existing value row is measured
+#  with `d->warned & CRIME_W_LEN' CLEAR, so a guard grown with a conjunct on that latch is
+#  invisible to all of them.  `POST()' below opens each session with a REFUSED lb at +0x07, so
+#  every access after it is measured with the LATCH SET.  New sessions only -- the targeting
+#  rule therefore selects no earlier kill for re-running (no existing session's command list
+#  changes).
+#
+#  CHANNEL lines: each row names its mutant and the observable, and EVERY ONE WAS CHECKED
+#  AGAINST ITS MUTANT rather than merely written -- the seat's first two TIME shapes were
+#  measured VACUOUS and one gave a FALSE RED on a control, which is this block's own evidence
+#  for why the PRETABLE CHANNEL line has to be run, not asserted.
+# ============================================================================================
+
+
+def POST(A):
+    """A refused lb at +0x07 sets d->warned & CRIME_W_LEN before anything else in the session."""
+    x, _ = ld(A, "lb", CRIME + 0x07, "v0")
+    return x
+
+
+# ---- P1: the REV PROM-probe window, POST.  CHANNEL: pc = ra, which only an ACCEPTED access
+#      reaches.  KILLS K2 (the REV 4-byte cell conjoined with the latch). ----
+A = Addr(CODE)
+c = ["ra=0x%x" % RA] + POST(A)
+for op in ("sw", "sd", "ld", "lw"):
+    if op[0] == "s":
+        x, _ = st(A, op, CRIME + 0, 0, at=PROBE_PC)
+    else:
+        x, _ = ld(A, op, CRIME + 0, "s0", at=PROBE_PC)
+    c += x + ["print pc"]
+t, clean = session(c)
+for i, k in enumerate(("sw", "sd", "ld", "lw")):
+    v = nth(t, "pc", i)
+    row("p revP %s pc" % k, "absent" if v is None else "0x%x" % v, "0x%x" % RA,
+        "POST: accepted %s CRIME_REV from the window -> ra" % k)
+row("p revP once", count(t, "-- declined.", clean), 1, "CONTROL: the session refused exactly once (the lb)")
+
+# ---- P2: the twelve-cell value session, POST.  KILLS K1 (INTMASK 4W) and K3 (CONTROL 8R).
+#      The two CONTROL writes at the end drive the clause-(e) 0x0001 and 0x0201 cells into the
+#      `unimplemented' count row, so one count row covers three accesses. ----
+A = Addr(CODE)
+c = POST(A)
+x, _ = ld(A, "ld", CRIME + 0x08, "s0"); c += x
+x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
+x, _ = ld(A, "ld", CRIME + 0x10, "s1"); c += x
+x, _ = st(A, "sw", CRIME + 0x18, 0x10000000); c += x
+x, _ = ld(A, "ld", CRIME + 0x18, "s2"); c += x
+x, _ = st(A, "sd", CRIME + 0x38, 0x11111111); c += x
+x, _ = ld(A, "ld", CRIME + 0x38, "s3"); c += x
+x, _ = st(A, "sd", CRIME + 0x40, 0); c += x
+x, _ = st(A, "sw", CRIME + 0x40, 0x0a0b0c0d); c += x
+x, _ = ld(A, "lw", CRIME + 0x40, "a1"); c += x
+x, _ = ld(A, "ld", CRIME + 0x40, "a2"); c += x
+x, _ = st(A, "sd", CRIME + 0x08, 0x01); c += x
+x, _ = st(A, "sw", CRIME + 0x08, 0x0001); c += x          # EXTRA: CONTROL 4W 0x0001
+x, _ = st(A, "sw", CRIME + 0x08, 0x0201); c += x          # EXTRA: CONTROL 4W 0x0201 (clause-(e) cell)
+t, clean = session(c + ["print s0", "print s1", "print s2", "print s3", "print a1", "print a2"])
+tv = nth(t, "s3", 0)
+row("p acc ctl ld", pr(t, "s0"), "0x100", "POST: accepted ld +0x08 answers CONTROL")
+row("p acc istat ld", pr(t, "s1"), "0x%x" % BIT, "POST: accepted ld +0x10 answers INTSTAT")
+row("p acc imask sw", pr(t, "s2"), "0x1000000000000000", "POST: accepted sw +0x18 lands high")
+row("p acc time sd", "absent" if tv is None else ("odd" if tv & 1 else "even"), "odd",
+    "POST: accepted sd +0x38 odd seed stays odd (raw %s)" % tv)
+row("p acc 40 lw", pr(t, "a1"), "0xa0b0c0d", "POST: accepted lw +0x40 answers the stored half")
+row("p acc 40 sw", pr(t, "a2"), "0xa0b0c0d00000000", "POST: accepted sw +0x40 lands high")
+row("p acc ctl msg", count(t, "CRIME_CONTROL: unimplemented", clean), 3,
+    "POST: the three accepted CONTROL writes (0x01 sd, 0x0001 sw, 0x0201 sw) each print")
+row("p acc once", count(t, "-- declined.", clean), 1, "CONTROL: exactly one refusal (the lb)")
+
+# ---- P3: INTSTAT's reassert channel (cause.IP2), POST.  The reassert is an EFFECT channel a
+#      value row cannot see, which is why this session exists separately. ----
+A = Addr(CODE)
+c = POST(A)
+x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
+x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
+c += ["print cause"]
+x, _ = st(A, "sd", CRIME + 0x10, 0); c += x
+c += ["print cause"]
+x, _ = st(A, "sd", CRIME + 0x20, 0); c += x
+x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
+x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
+c += ["print cause"]
+x, _ = st(A, "sw", CRIME + 0x10, 0); c += x
+c += ["print cause"]
+t, clean = session(c)
+row("p istw pre", ip2(nth(t, "cause", 0)), "clear", "CONTROL: IP2 low after SOFTINT default-arm store")
+row("p istw sd", ip2(nth(t, "cause", 1)), "set", "POST: accepted sd +0x10 reasserts")
+row("p istw mid", ip2(nth(t, "cause", 2)), "clear", "CONTROL: lowered again")
+row("p istw sw", ip2(nth(t, "cause", 3)), "set", "POST: accepted sw +0x10 reasserts")
+
+# ---- P4/P5: THE TIME 4-BYTE CELLS, POST, IN THE **GAPPED** SHAPE.  *** THE TWO OBVIOUS SHAPES
+#      WERE MEASURED VACUOUS (post7b.py) and one gave a FALSE RED on a control; only this one
+#      discriminates, at ~13,000x (base 0x13414f8 vs the bypass's 0x5ee). ***  The gap is the
+#      debugger's own pause BETWEEN steps: host time passes, so an update that is performed
+#      arrives before the final 8R and one that is skipped arrives after it.  CHANNEL: a read
+#      takes odata BEFORE its own crime_update_crime_time(). ----
+def gapped_post(kind):
+    ops = [enc("lb", "a3", "t1"),                                            # REFUSED lb -- sets the latch
+           enc("ld", "at", "v1"),                                            # TIME 8R, TIME still ~0
+           enc("sw", "at", "t0") if kind == "w" else enc("lw", "at", "a0"),  # the cell under test
+           enc("ld", "at", "v0")]                                            # what it left behind
+    c = ["at=0x%x" % (CRIME + 0x38), "a3=0x%x" % (CRIME + 0x07), "t0=0x0a0b0c0d",
+         "v0=0x%x" % SENT, "v1=0x%x" % SENT, "a0=0x%x" % SENT, "t1=0x%x" % SENT]
+    for i, op in enumerate(ops):
+        c.append("put w 0x%x, 0x%08x" % (CODE + 4 * i, op))
+    c += ["put w 0x%x, 0x%08x" % (CODE + 4 * len(ops), OP_B_SELF),
+          "put w 0x%x, 0x%08x" % (CODE + 4 * len(ops) + 4, OP_NOP), "pc=0x%x" % CODE]
+    c += ["step 2", "step 1", "step 1", "print v0", "print v1"]
+    t, clean = session(c)
+    return nth(t, "v0", 0), nth(t, "v1", 0), (t.count("-- declined.") if clean else "unclean")
+
+
+_gapnote = []
+for kind in ("w", "r"):
+    v0, v1, n = gapped_post(kind)
+    _gapnote.append(n)
+    row("p t4%s gap" % kind, mag(v0), "large",
+        "step2[lb,ld] step1[%s] step1[ld] (raw %s, first ld %s)"
+        % ("sw" if kind == "w" else "lw", None if v0 is None else hex(v0), None if v1 is None else hex(v1)))
+row("p t gap once", _gapnote, [1, 1], "CONTROL: each gapped session announced its one refusal")
+
+# ---- P6: the remaining post-latch ACCEPT cells that carry a value, plus the two EXTRA accesses
+#      (DOG 4W high, the +0x04 write line). ----
+A = Addr(CODE)
+c = POST(A)
+x, _ = ld(A, "ld", CRIME + 0x00, "s0"); c += x                      # REV 8R from CODE
+x, _ = ld(A, "lw", CRIME + 0x04, "s1"); c += x                      # REV 4R low lane (devsig cell)
+x, _ = st(A, "sw", CRIME + 0x04, 0x0c0ffee0); c += x                # EXTRA: the +0x04 WRITE line
+x, _ = st(A, "sd", CRIME + 0x30, 0x1122334455667788); c += x        # DOG 8W
+x, _ = ld(A, "ld", CRIME + 0x30, "s2"); c += x                      # DOG 8R
+x, _ = ld(A, "lw", CRIME + 0x30, "a0"); c += x                      # DOG 4R high
+x, _ = ld(A, "lw", CRIME + 0x34, "a1"); c += x                      # DOG 4R low
+x, _ = st(A, "sw", CRIME + 0x34, 0x0badcafe); c += x                # DOG 4W low
+x, _ = ld(A, "ld", CRIME + 0x30, "s3"); c += x
+x, _ = st(A, "sw", CRIME + 0x30, 0x0feedbac); c += x                # EXTRA: DOG 4W HIGH
+x, _ = ld(A, "ld", CRIME + 0x30, "ra"); c += x
+x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x                       # INTMASK 8W
+x, _ = ld(A, "ld", CRIME + 0x18, "a2"); c += x                      # INTMASK 8R
+x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x       # far block 8W
+x, _ = ld(A, "ld", CRIME + 0x278, "t1"); c += x
+t, clean = session(c + ["print s0", "print s1", "print s2", "print a0", "print a1", "print s3",
+                        "print ra", "print a2", "print t1"] + roundtrip(A))
+row("p rev ld", pr(t, "s0"), "0x11", "POST: accepted ld +0x00 answers CRIME_REV")
+row("p rev lw4", pr(t, "s1"), "0x11", "POST: accepted lw +0x04 answers REV low lane")
+row("p dog st+ld", pr(t, "s2"), "0x1122334455667788", "POST: 8W then 8R at CRIME_DOG")
+row("p dog rhi", pr(t, "a0"), "0x11223344", "POST: 4R of the high half (+0x30)")
+row("p dog rlo", pr(t, "a1"), "0x55667788", "POST: 4R of the low half (+0x34)")
+row("p dog wlo", pr(t, "s3"), "0x112233440badcafe", "POST: 4W low half lands, high half kept")
+row("p dog whi", pr(t, "ra"), "0xfeedbac0badcafe", "POST: 4W HIGH half lands, low half kept")
+row("p imask st+ld", pr(t, "a2"), "0x%x" % BIT, "POST: 8W then 8R at CRIME_INTMASK")
+row("p top st+ld", pr(t, "t1"), "0x102030405060708", "POST: 8W then 8R at +0x278")
+row("p resid once", count(t, "-- declined.", clean), 1, "CONTROL: exactly one refusal (the lb)")
+row("p resid surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "CONTROL: the host survives (a RAM trip)")
+
+#  *** REGISTER COLLISION, CAUGHT WHILE DRAFTING AND RECORDED RATHER THAN SILENTLY FIXED: the
+#  prototype's residual-survival row reads `v1', which roundtrip() writes.  The DOG 4W-high
+#  readback added here therefore CANNOT use v1 -- it would make one of the two rows read the
+#  other's register and go green for the wrong reason, which is exactly the vacuity this repair
+#  exists to close.  It is parked in `t2' above.  BEFORE APPLYING: check t2 is not otherwise
+#  live in this session (st() uses a3/t0, ld() uses at; t1 is the far-block readback), and
+#  re-run the negative controls -- a register collision is invisible to a green run.
+
+
 npass = sum(1 for _, ok in rows if ok)
 st_ = dict(rows)
```

## THE FLAGSHIP RULING, PART A (closing pass 6)

## PART A -- #529 crimewidthkill, closing pass 6, repair 11, 141 rows

### R1 -- A1 is a FLOOR breach, L2, and it is a CLASS.  Verified against the source, not taken from the seat.

The width arm (`dev_sgi_ip32.c:275-296`) branches on `len == 8`, `len == 4`, `writeflag` and `relative_addr & 4`; every
accepted access then reaches `switch (relative_addr)` (`:322`) and `d->reg[relative_addr / 8]` (`:277-290`).  So the
LABEL is a floor axis of the width guard under the JOIN clause (the selector flows into an lvalue the guarded body reads
and writes, and the switch re-tests it after the join).  A growth `len == 8 && relative_addr != CRIME_CONTROL` is the
canonical accept-row-failability mutant -- the joint guard-growth form -- and item 6 CLAIMS the accept side is pinned
"at any single cell".  Measured: C1, G1-G5 each 141/141, and G1/G2/G4/G5 change what the guest sees (an 8R of CONTROL
answers 0 not 0x100; an 8R of INTSTAT answers 0 with an interrupt pending; a 4W to REV from the window no longer
redirects; a 4W to INTMASK does not land).  All four of the seat's grounds hold on reading: the de-escalation clause
(pre-fix this edit ended the process at the first such access), the JOIN clause, item 6's own sentence, and the
`#499` shape (grok's `len == 8 && relative_addr != 0` was repaired at +0x00 by `acc8 near` and nowhere else).

**Why it is a class and not six cells:** `rearm once` and `latch x5` COUNT `-- declined.` (probe `:765`, `:949`).  A
wrongly declined accepted cell either comes after the first refusal (silenced) or IS the first refusal (takes the one
notice the lh +0x06 should have had).  Either way the count is 1.  So ACCEPTS carries the latch cross and carries nothing
about acceptance -- for any of its 46 cells.  Six seats read the enumeration and said CLOSES; none of the six engaged
with what the two ACCEPTS-fed rows can OBSERVE.  Counting arguments: one measured clean sweep outweighs seven readings
that did not look at the channel.

### R2 -- codex's row is the class closure for the ANNOUNCED form, and it is general by construction.

`row("latch said", said(t, 2, 0x06, clean), 1, ...)` in latch x5 (`said` at `:381` counts the exact announce text).  All
46 ACCEPTS accesses precede the lh +0x06 in that session (`:934-940`), so any guard growth at any of them sends that cell
into the announcing decline arm (`:314-319`) and the lh's own text is absent.  The window kinds are covered too: the
width arm declines BEFORE the pc test, so `swP/sdP/ldP/lwP` announce like any other (G4 measured red).  Base 149/149, red
on C1 and G1-G5, no shipped row moved, no command list changed.  **Take it as written; do not fold it into `latch x5`**
(a folded row loses the attribution of WHICH half failed).

### RA1 -- the SILENT bypass (G6).  (i) is REQUIRED; (ii) is LICENSED; the cell set is the ENUMERATION's or none.

G6 (`if (len == 8 && relative_addr == CRIME_CONTROL) goto crime_declined;` before the width test) is outside the
de-escalation class -- pre-fix an inserted `return 1;` was equally silent, so the deleted `exit(1)` never announced it --
and outside the DEPENDS-ON enumeration (it inserts a predicate; it weakens none).  So it is NOT floor, and no row can be
DEMANDED for it.  But item 6's literal "any single cell" is false of it, and a false record is L4 whatever the grade.

* **(i) REQUIRED:** narrow item 6 to "the ACCEPT SET shrunk at any single cell IN THE GUARD-GROWTH (announcing) FORM --
  carried by `latch said` over every ACCEPTS cell", and DISCLOSE the silent bypass BY CLASS, naming the cells where a
  value row catches it anyway (below) and the cells where it is EQUIVALENT at the guest (REV 8W/4W/4R out of the window,
  CONTROL 4R: the prelude rewrites or the high half is 0).
  *** THIS CLAUSE ALSO NAMED **TIME 4W/4R** AS EQUIVALENT, AND CLOSING PASS 7 MEASURED IT GUEST-VISIBLE -- mutant E2 at
  157/157, differing on four channels (`regress/artifacts/crimewidthkill/opus_close7_20260915/OPUS_REPORT.md', E2).
  The reason the ruling gave is wrong in the same place: a read takes `odata' BEFORE its own crime_update_crime_time(),
  so a skipped update ARRIVES ONE ACCESS LATE instead of accumulating.  Corrected here rather than only in the probe
  because item 6's wrong sentence was COPIED FROM THIS ONE, and correcting one of the two leaves the record
  inconsistent -- the seat that measured it said so explicitly.  The ruling's own disposition is otherwise untouched:
  TIME 4W/4R is now an unrowed single-axis FLOOR cell owed by repair 13. ***
  *** RA3 of this ruling -- "It is clause (e) by the DEPENDS-ON bound (`d->warned' is not a field the accept bodies
  read)" -- IS **OVERTURNED TO FLOOR** BY THE 2026-09-16 ADJUDICATION (FABLE_C5_RULING_20260915.md, S-A.7), ON FOUR
  INDEPENDENT GROUNDS, THE FIRST OF WHICH IS IN THE DIFF ITSELF: the fix's own decline arm READS `d->warned' at
  dev_sgi_ip32.c:314, in a hunk THIS DIFF ADDS, so the latch is a device-state lvalue the fix's own repair path reads --
  a floor axis by the pass-11 floor definition and the M_ICLR precedent, and by this round's own practice, since it
  built and measured the shrink.  Bounded, and not #392: the floor is the diff-closed 56-cell product, of which the
  ROWS OWED are the 23 open guest-visible cells.  *The measuring seat disputed this clause and was right; the ruling
  that adopted it was mine, and a ruling in one's own favour is the one least likely to be tested.* ***
* **(ii) LICENSED (measured delta: `dg ld ctl`, `dg ld istat`, `dg sw imask`, `dg swP pc` each red on its cell, green on
  base, new sessions only).**  If value rows are added -- and I RECOMMEND it, because at those cells the silent form has
  the SAME guest effect as the growth form and a detector that sees one and not the other is claiming more than it
  pins -- the set is the Opus per-cell table's guest-visible "no" cells, all of them, in ONE diff: REV window 4W/8W/8R
  (the redirect), CONTROL 8R/8W, INTSTAT 8W/8R/4W, INTMASK 4W, TIME 8W, default `sw/lw 0x40`.  Twelve cells, each with
  a CHANNEL line in `PRETABLE.out` naming the mutant and the observable.  A five-cell set drawn from the mutants the
  seat happened to build is licensed too, but then the record says "5 of 12 rowed, 7 disclosed" -- it may not say the
  silent class is closed.  What I reject is only the half-set presented as closure.
* The coordinator's worry about incoherence is answered: (i) states what the CONTRACT claims; (ii) states what the
  DETECTOR additionally pins.  Different questions, both answered, no contradiction.

### RA2 -- repair 12 owes TARGETED TABLE 10 and CLOSING PASS 7.  The seat's augmentation run does not discharge either.

* **Table 10, and why the run is not it:** the seat APPENDED rows to a frozen copy; repair 12 re-types them into the
  shipped probe.  A re-typed row is a new instrument and is measured, not assumed.  Legs: base; C1, G1-G6, C2 (the new
  rows' own kills, including G6 for any value rows); the 17 table-9 pre-set kills IF POSTTABLE 10 will state their new
  scores (the "they also red `latch said`" prediction is REASONED -- the seat says so -- and a predicted score in a
  measured column is the frozen-number class; run them or omit them from the record, ~17 legs, about an hour in four
  lanes).  The 12 re-arm kills and every kill outside the two sessions cannot move: no command list changed (the
  targeting rule), and I checked that `latch said` reads latch x5's existing transcript only.
* **Pass 7 is owed** because the first VALID pass with zero floor breaches surviving adjudication is not pass 6.  It is
  LIGHT and it VERIFIES rather than hunts: (a) for each of the 46 ACCEPTS cells, name the row that reds under an
  ANNOUNCED decline (`latch said`, by construction) and under a SILENT decline (a value row, or "equivalent", or
  "disclosed") -- 92 cells, derivable by reading; (b) confirm by reading latch x5's command list that every ACCEPTS
  access precedes the lh (the generality argument); (c) nothing else.  Full roster, per the every-stage rule.

### RA3 -- is there a further accept-side class?  Yes, and it is the one pass 7 enumerates; plus one thing to BUILD.

* The accept side of the 46-cell cross has exactly two forms a single edit can produce: ANNOUNCED decline (closed by
  `latch said`) and SILENT decline (RA1).  That is the enumeration pass 7 verifies: cell x {announced, silent}.
* **A `d->warned`-keyed shrink must be BUILT before it is disclosed.**  The seat reasoned it clause (e) and did not build
  it.  Two forms: keyed on 8R (`len == 8 && (writeflag == MEM_WRITE || !(d->warned & CRIME_W_LEN))`) -- I predict
  KILLED: `sb keeps`/`sh keeps`/`lo keeps`/`hi keeps`/`mid keeps` (`:691-842`) each read a seeded slot with an accepted ld
  AFTER a refusal, which such a shrink answers 0; and keyed on 8W -- may escape (the only accepted 8W after a refusal
  whose value is read back by an accepted read is unclear from the rows).  It is clause (e) by the DEPENDS-ON bound
  (`d->warned` is not a field the accept bodies read); if it escapes, DISCLOSE it by name.  "Reasoned, not built" is a
  prediction and this chain has had enough of those.
* Classes NOT to reopen: accepted-but-mishandled (landing, lane, re-map) are items 6/7's anchor rows and earlier tables'
  material, outside this chain's class.  Pass 7 is told so explicitly, or the chain does not terminate.

### A1-A9 dispositions
| # | ruling |
|---|---|
| A1 | **FLOOR breach, L2, a CLASS; also L4 (item 6).**  Coordinator upheld. |
| A2 | **REPAIR 12 takes codex's row as written.**  Upheld. |
| A3 | **RA1: (i) REQUIRED; (ii) licensed and recommended over the 12-cell derived set.**  Coordinator's lean corrected. |
| A4 | Clause (e) by the bound (the decline arm reads no `pc`); ADD `free revP said` as a licensed strengthening; item 5 gains a rowed line for pc at that one cell and a disclosed line for pc JOINTS.  Upheld. |
| A5 | Killed 139/141 both forms; premise true, conclusion refuted.  Upheld (none). |
| A6 | Killed 131/141; minimax's premise false (default-arm answer rows sit at unaligned offsets).  Upheld (none). |
| A7 | EQUIVALENT by construction (`idata` set only on writes, `odata` consumed only on reads); one DISCLOSED line.  Upheld. |
| A8 | All corrected in repair 12; two additions below (item 3 / `:495` "tested").  Upheld. |
| A9 | 40 floor + 2 clause-(e) strengthenings + 4 positional repeats = 46 (I recounted the tuple at `:731-743`).  deepseek's "six vs eight" is not an error: six KINDS, eight ENTRIES.  Upheld. |

### L4 wrong records in Part A (file: `regress/crime_width_probe.py` unless noted)
1. **Item 6, "the ACCEPT SET shrunk at any single cell"** -- false at every cell the Opus per-cell table marks "no".
2. **Item 3 (`:26-27`) "the arm's three TESTED idata bits (DOG 0x200, RESET 0x800, ENDIANESS 0x100)" and the comment at
   `:495` "ENDIANESS (0x0100) is the arm's third tested bit"** -- FALSE at both sites: `:375` is `idata &=
   ~CRIME_CONTROL_ENDIANESS;` with no `if`.  The header's own repair-11 note (`:728`) says the opposite correctly.  Two
   sites; the grep-for-siblings rule.
3. **DISCLOSED "ACCEPT cells at unrowed slots"** -- implies a touched slot is pinned; touching pins the LATCH, never the
   acceptance.
4. **DISCLOSED "an accepted WRITE at +0x00 or +0x08 shrunk away ... no round trip there can observe"** -- wrong twice: the
   window 4W redirects (G4 measured), and the 8-byte CONTROL write is unrowed (G1).
5. **Repair-11 comment (`:725-726`) "crossed the window with the DIRECTION on writes only"** -- the missing cell was the
   8-byte WIDTH on the READ side; say that.
6. **"the two label cells whose arms have NO body"** -- three: REV from OUTSIDE the window is a label cell with no body
   for that access.  Name it.
7. **`killtable9_20260914/POSTTABLE.out` FLOOR line** -- true for pre-set/re-arm; add the note "the ACCEPT side of the
   same cross is NOT closed by ACCEPTS (closing pass 6)" in the style it already uses.
8. **`panel_20260915_011138/brief_sent.md` "mutants of table 9, verbatim"** shows P3-P7; table 9 ran P1/P1b/P2/P2b only
   (`mutants529i.py` imports exactly those; codex and agy both caught it).  A frozen artifact; the ledger entry for this
   panel carries the correction.
9. **The adjudication brief itself:** "Six seats CLOSE (...)" lists SEVEN names.  Not a shipped record; noted so the
   ledger entry does not copy it.
10. `free_one` ignoring `clean` (codex): a truncated transcript can only produce a false RED there (count 0 against want
    1), never a false green -- not a vacuity, but fix it for consistency with `said`.

---


## THE MUTANTS OF TABLE 10, verbatim (table 9's by name; the Opus close-6 seat's C1/C2/G1-G6; this table's own)

```python
M = dict(J.M)

LEN8 = "\tif (len == 8) {\n"
LEN4 = "\t} else if (len == 4) {\n"
W, R_ = "writeflag == MEM_WRITE", "writeflag == MEM_READ"

#  ---- the three the close-7 seat MEASURED, verbatim (each 157/157 against repair 12) ----------------------------
M.update({
    "K1": [(LEN4, "\t} else if (len == 4 && !(%s &&\n\t    relative_addr == CRIME_INTMASK && (d->warned & CRIME_W_LEN))) {\n" % W)],
    "K2": [(LEN4, "\t} else if (len == 4 && !(relative_addr == CRIME_REV && (d->warned & CRIME_W_LEN))) {\n")],
    "K3": [(LEN8, "\tif (len == 8 && !(%s &&\n\t    relative_addr == CRIME_CONTROL && (d->warned & CRIME_W_LEN))) {\n" % R_)],
    #  codex's TIME mutant, verbatim: the cell item 6 and the ruling's RA1 both called EQUIVALENT and which is
    #  measured guest-visible on four channels.  Killed only by the GAPPED row shape.
    "E2": J.bypass("len == 4 && relative_addr == CRIME_TIME"),
})

#  ---- THE CLOSURE, GENERATED.  28 latch-set cells; the generator IS the enumeration. ---------------------------
LABELS = (("rev", "relative_addr == CRIME_REV"),
          ("ctl", "relative_addr == CRIME_CONTROL"),
          ("ist", "relative_addr == CRIME_INTSTAT"),
          ("imk", "relative_addr == CRIME_INTMASK"),
          ("dog", "relative_addr == CRIME_DOG"),
          ("tim", "relative_addr == CRIME_TIME"),
          #  the `default' arm is the COMPLEMENT of the six, and it is written as one so the mutant cannot be
          #  satisfied by a label the switch already names -- the enumeration's own negative space.
          ("dfl", "relative_addr != CRIME_REV && relative_addr != CRIME_CONTROL &&\n\t    "
                  "relative_addr != CRIME_INTSTAT && relative_addr != CRIME_INTMASK &&\n\t    "
                  "relative_addr != CRIME_DOG && relative_addr != CRIME_TIME"))


def klatch(anchor, head, dir_expr, label_expr):
    """the K-form: keep the width guard, null its repair at ONE cell ONCE THE LATCH HAS FIRED (silent by construction,
    because the announce is what the latch suppresses)"""
    return [(anchor, "%s && !(%s && (%s) &&\n\t    (d->warned & CRIME_W_LEN))) {\n" % (head, dir_expr, label_expr))]


for lab, expr in LABELS:
    for ln, anchor, head in ((8, LEN8, "\tif (len == 8"), (4, LEN4, "\t} else if (len == 4")):
        for d, dex in (("w", W), ("r", R_)):
            name = "C_%s%d%s" % (lab, ln, d)
            if name not in M:                       # K1/K2/K3 are members of this product; do not shadow them
                M[name] = klatch(anchor, head, dex, expr)

#  K2 is the (rev, 4, both-directions) cell -- deliberately NOT direction-split, because that is the form the seat
#  MEASURED.  The generated C_rev4w / C_rev4r are its two halves and are kept: a cell whose two halves are covered
#  separately is not thereby covered jointly, and this table is the one that says so.

```

## MUTATION-TEST TABLE 10 -- results (`POSTTABLE.out`)

```
POSTTABLE 11 -- #529 crimewidthkill, repair 13 (188 rows).  Written AFTER the table; PRETABLE.out predates it and the
mtimes prove the order (PRETABLE 15:48:34, mutator 15:48:43, table launched 15:49:51).

RESULT   33 legs, every one ending CRIMEP_DONE with done=1.  Driver token KILL529K_DONE present.  table11.out.
         BASE 188/188 CONTROL=OK.  Clone RESTORED and verified before the probe phase even began: cmp-clean against
         GXEMUL-SEC, binary newer than source, sentinel cleared, and `restored == base (byte-identical)'.

THE GAP CLOSING PASS 7 FOUND IS CLOSED, AND IT IS MEASURED RATHER THAN ARGUED
         K1 187/188  reds `p acc imask sw'                      (was 157/157 -- an ESCAPE -- before repair 13)
         K2 186/188  reds `p revP sw pc', `p revP lw pc'        (was 157/157)
         K3 187/188  reds `p acc ctl ld'                        (was 157/157)
         E2 186/188  reds `p t4w gap', `p t4r gap'              (was 157/157; the TIME cell item 6 and the prior
                     ruling's RA1 both called EQUIVALENT, measured guest-visible on four channels)

THE ENUMERATION VERIFIES: 28 of 28 GENERATED CLOSURE CELLS BEHAVED AS THE CONTRACT SAYS THEY MUST
         27 cells KILLED, each reddening rows at its own (len, direction, label) cell.
          1 cell at 188/188 -- `C_ctl4r' -- AND THAT IS THE CONTRACT'S OWN NEGATIVE CONTROL PASSING, NOT AN ESCAPE.
            The contract lists CONTROL 4R among the EQUIVALENT cells ("reads 0 either way"), so a latch-keyed shrink
            there has nothing to observe and MUST move nothing.  It moved nothing.  *** This is the enumeration
            checking itself: the same generator emitted the cells that must red and the cell that must not, and both
            came out as written.  A closure that only produced kills would not have tested its own EQUIVALENT claim
            at all. ***

*** MY PER-ROW PREDICTION FOR K2 WAS WRONG, AND THE MEASUREMENT IS RIGHT.  PRETABLE 11 predicted K2 would red "the
FOUR `p revP * pc' rows"; it reds TWO -- `sw' and `lw'.  K2 is `} else if (len == 4 && !(...))', on the len == 4 ARM,
so it can only reach the 4-BYTE ops; `sd' and `ld' are 8-byte, go through the len == 8 arm, and cannot be affected by
it.  I wrote the prediction from the CELL (REV) without carrying the WIDTH the mutant is gated on. ***
         K1, K3 and E2 matched their per-row predictions EXACTLY.
         This is the predict-then-measure discipline earning its keep in the direction it is meant to: the error was
         in the prediction, the detector and the mutant are both correct, and nothing was fitted to the answer.

THREE LEGS CARRY `CRIMEP_CONTROL=FAIL', AND IT IS INFORMATIONAL RATHER THAN A DEFECT -- but it is a finding about the
INSTRUMENT and is written down rather than waved past.
         C_ist4r 187/188  the ONLY red is `istat ctl'
         C_imk4r 187/188  the ONLY red is `imask ctl'
         C_tim8r 181/188  reds `time lb/sb/lh/sh' and the new `p acc', `p t4w', `p t4r'
         In each case the red rows ARE the cell's own channel, so every kill is ATTRIBUTABLE -- the mutant failed for
         the reason under test.  What the aggregate cannot do is tell "the mutant broke a control row" apart from
         "this session was invalid", because `CRIMEP_CONTROL' is a conjunction over a fixed row set and some of those
         rows are the very channels a latch-keyed shrink at INTSTAT/INTMASK/TIME is supposed to move.
         *** THE GATE IS UNAFFECTED: it pins CONTROL=OK on the BASE build, and base is 188/188 CONTROL=OK.  The FAIL
         appears only under mutants, where a moved control row is the expected outcome. ***
         FILED, not fixed: the control aggregate could name WHICH control rows moved instead of collapsing to a
         boolean.  That is an instrument change owing its own negative controls, and this round takes one site.

NOT RE-MEASURED, with the reason: every table 1-10 kill.  Repair 13 added NEW SESSIONS ONLY -- no existing session's
         command list changed -- so by the targeting rule an adds-only repair moves no kill and none is re-run.

RECORDS   the three gate pins moved 157 -> 188 with the precommit comment; the score-claims checker then reported NINE
         stale claims in the new contract text and was RIGHT -- seven were historical quotes needing an era tag ("on
         the 157-row test"), and TWO were FALSE score-claims (`0xc6/0x108' and `6/6 each way' parse as N/M), which
         were REPHRASED rather than tagged, because an era tag on a hex value would be a lie told to quiet a checker.
         SCORE_CLAIMS_PASS now.

WHAT THIS DOES NOT SETTLE: closing pass 8 still has to run, and by the repair-chain amendment its job is to VERIFY
         THE ENUMERATION rather than hunt cells -- does a clean-sweep latch-SET mutant exist in the 56-cell product
         that this table did not build?  It must be a VALID pass and must close on a zero carried WITH its
         denominator (which cells, which shapes were swept), never a bare zero.
```

## QUESTIONS -- *** THIS PASS VERIFIES AN ENUMERATION.  IT DOES NOT HUNT CELLS. ***

The repair-chain amendment governs this pass, and the flagship ruling repeats it: when two consecutive passes find
breaches of ONE class, the next repair owes the CLASS CLOSURE in one diff, and **the closing pass then VERIFIES THE
ENUMERATION rather than hunting**.  Three passes found this class (pass 6 the announced accept-guard growth, table 10
the width-level latch shrink, pass 7 the per-cell latch shrink); repair 13 is the closure; table 11 measured it.

**A BARE ZERO DOES NOT CLOSE THE CHAIN.**  If your answer is "no gap", it must carry its DENOMINATOR -- which cells,
which mutant shapes you swept -- because "zero found" and "zero looked for" must not render the same.

1. **IS THE ENUMERATION ITSELF RIGHT?**  It is `{latch clear, set} x {len 4, 8} x {read, write} x {the SEVEN labels the
   switch distinguishes: REV, CONTROL, INTSTAT, INTMASK, DOG, TIME, default}` = 56 cells, read off `DEVICE_ACCESS(crime)`
   and generated mechanically (the `klatch`/`LABELS` block above emits all 28 latch-SET cells by construction).
   **Is there an AXIS it is missing**, or a label the switch distinguishes that the seven do not cover?  Check it
   against the function, not against my description of the function.
2. **DOES A CLEAN-SWEEP LATCH-SET MUTANT EXIST THAT TABLE 11 DID NOT BUILD?**  Table 11 built 28 generated cells plus
   K1/K2/K3 and E2: 27 killed, and `C_ctl4r` scored 188/188 because the contract calls CONTROL 4R EQUIVALENT ("reads 0
   either way") -- that is the enumeration's own negative control passing.  Give an exact edit to
   `src/devices/dev_sgi_ip32.c` that scores **188/188**, and name the row you expected to catch it.
3. **IS THE PER-CELL DISPOSITION HONEST?**  The contract splits the 46 ACCEPTS entries as **23 ROWED / 8 ALREADY PINNED
   post-latch / 10 EQUIVALENT / 5 HOST-DIAGNOSTIC (clause-(e), disclosed)**.  The 8 come from a STATIC session map
   (`opus_close7_20260915/scripts2/session_map2.py`), not from a measurement.  **Is any cell in the wrong bucket?**  A
   cell called EQUIVALENT that a guest can observe is a floor breach; a cell called ROWED whose row cannot vary under
   its own mutant is vacuous.
4. **THREE LEGS REPORT `CRIMEP_CONTROL=FAIL`** (`C_ist4r`, `C_imk4r`, `C_tim8r`).  In each the red rows are that cell's
   own channel, so I read every kill as ATTRIBUTABLE and the gate as unaffected (it pins CONTROL=OK on BASE, which is
   188/188 OK).  **Is that reading wrong** -- is any of those three kills actually an invalid session rather than a
   caught mutant?
5. **WHICH STATEMENT IN THIS BRIEF, IN `POSTTABLE 11`, OR IN THE PROBE HEADER IS WRONG?**  One is already known and is
   recorded rather than hidden: PRETABLE 11 predicted K2 would red FOUR `p revP * pc` rows and it reds TWO, because K2
   sits on the `len == 4` arm and the 8-byte ops cannot reach it.  That was a prediction error, not a detector defect.
   Find the next one.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
