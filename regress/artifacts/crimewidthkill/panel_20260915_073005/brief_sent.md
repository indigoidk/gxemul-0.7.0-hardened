# CLOSING PASS 7 -- `crimewidthkill` (#529): VERIFY the accept-side enumeration.  Liveness token `CRIME_CLOSE7_20260915`.

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
     guest-visible, by the value rows derived per cell (repair 12): REV window 4W/8W/8R (revP sw/sd/ld pc), CONTROL 8R
     (acc ctl ld) and 8W (acc ctl sd), INTSTAT 8R (acc istat ld), 8W and 4W (istw sd, istw sw), INTMASK 4W (acc imask
     sw), TIME 8W (acc time sd), the default arm's 4W/4R at +0x40 (acc 40 sw, acc 40 lw); and it is EQUIVALENT at REV
     8W/4W/4R outside the window (the prelude rewrites REV; its high half is 0), CONTROL 4R (reads 0 either way) and TIME
     4W/4R (the high half is 0; updates accumulate).  The remaining ACCEPTS cells' accept side is pinned by the rows
     below.  The ACCEPT set also at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
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
     (`ACCEPTS', 46 kinds since repair 11 -- 43 before `ldP' and the two ENDIANESS writes; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing seat:
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
     and `odata = d->use_fb' scored 141/141 (the Opus seat).  Those are DISCLOSED below.]  The HARDINT source (kimi-k3:cloud, the Opus seat, fourth closing pass: a decline answering
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

## THE REPAIR DIFF -- repair 11 -> repair 12 (141 -> 157 rows) (`git diff --no-index`, verbatim; 10 hunks)

```diff
diff --git "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable9_20260914\\crime_width_probe.table9.py" "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
index 3412750..3e5e32c 100644
--- "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable9_20260914\\crime_width_probe.table9.py"
+++ "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
@@ -16,5 +16,5 @@ Every access here is a real MIPS guest instruction through real address decode a
 
 CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
-artifacts/crimewidthkill/ (killtable_20260913/ through killtable8_20260914/):
+artifacts/crimewidthkill/ (killtable_20260913/ through killtable10_20260915/):
   1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                        <op> surv (six widths), hi surv, latch surv, sb08 run
@@ -24,7 +24,10 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable8_20260914/):
         CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
                                           sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
-                                          and the arm's three TESTED idata bits (DOG 0x200, RESET 0x800,
-                                          ENDIANESS 0x100) each both ways at 2W: sh 0x0201,
+                                          and the arm's two TESTED idata bits (DOG 0x200, RESET 0x800) each
+                                          both ways at 2W, plus ENDIANESS 0x100, which the arm CLEARS
+                                          UNCONDITIONALLY and never branches on (written anyway): sh 0x0201,
                                           0x0900, 0x0a00 with sh08 0x0800       sh08b msg, sh08b run
+                                          [This said "three TESTED idata bits (... ENDIANESS 0x100)" until
+                                          repair 12 -- false; agy, grok, closing pass 6.]
                                           plus ALL-ONES refused writes, sb 0xff and sh 0xffff (kimi CLI,
                                           closing pass), so a fall-through keyed on any bit a 1- or 2-byte
@@ -85,9 +88,25 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable8_20260914/):
      debug() would not -- on EVERY axis of the refusal: bits 0-2 (free said, +0x07), bits 3-8 and len 2 (free 2r said,
      +0x1f8), bit 9 and a write (free 1w said, +0x27f), a 2-byte write at a label (free 2w said, CONTROL), and each
-     remaining label (free rev/istat/imask/dog/time said).  *** Until repair 10 the channel was pinned at ONE cell (+0x07):
+     remaining label (free rev/istat/imask/dog/time said), and the ISSUING PC -- a refusal from the PROM-probe window
+     (free revP said, repair 12; glm, closing pass 6: `(pc in the window ? debug : fatal)(' scored 141/141 on the 141-row
+     test -- clause (e)
+     by the DEPENDS-ON bound, rowed as a strengthening).  *** Until repair 10 the channel was pinned at ONE cell (+0x07):
      `(relative_addr & 8 ? debug : fatal)(' and `(len == 2 ? debug : fatal)(' each scored 131/131 on the 131-row test (codex, the Opus
      seat, fourth closing pass).  One refusal per free-running session -- the latch silences any second one. ***
-  6. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this),
-     at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
+  6. the ACCEPT SET shrunk at any single cell IN THE GUARD-GROWTH FORM -- an accept guard grown by a conjunct, so the
+     cell falls into the announcing decline arm (the de-escalation clause: the deleted exit(1) used to announce exactly
+     this) -- at EVERY ACCEPTS cell by `latch said': latch x5 runs all 46 ACCEPTS accesses before the lh +0x06, so a
+     wrongly declined accepted cell steals that lh's own announce (repair 12; codex's C1 and the Opus seat's G1-G5 each
+     scored 141/141 on the 141-row test, because `latch x5' and `rearm once' COUNT notices and a stolen notice keeps the
+     count at 1).  *** This item said "the ACCEPT SET shrunk at any single cell" with no form, and it was false at
+     CONTROL 4R/8R/8W, INTSTAT 8, TIME 4, INTMASK 4W and the REV window 4W (closing pass 6, measured). ***
+     The SILENT form -- a bypass inserted before the width test that declines an accepted cell with NO announce (the
+     Opus seat's G6) -- is outside the de-escalation class and DISCLOSED by class; it is CAUGHT where a bypassed cell is
+     guest-visible, by the value rows derived per cell (repair 12): REV window 4W/8W/8R (revP sw/sd/ld pc), CONTROL 8R
+     (acc ctl ld) and 8W (acc ctl sd), INTSTAT 8R (acc istat ld), 8W and 4W (istw sd, istw sw), INTMASK 4W (acc imask
+     sw), TIME 8W (acc time sd), the default arm's 4W/4R at +0x40 (acc 40 sw, acc 40 lw); and it is EQUIVALENT at REV
+     8W/4W/4R outside the window (the prelude rewrites REV; its high half is 0), CONTROL 4R (reads 0 either way) and TIME
+     4W/4R (the high half is 0; updates accumulate).  The remaining ACCEPTS cells' accept side is pinned by the rows
+     below.  The ACCEPT set also at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
      prelude writes; grok, closing pass: `len == 8 && relative_addr != 0' passed the 85-row version, whose rows sat at
      +0x30 -- an interior slot, not an end), with devsig the 4R-low cell there and `rev pc ctl' the 4R-high one (its
@@ -125,5 +144,5 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable8_20260914/):
   9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
      (codex, closing pass: `if (relative_addr == CRIME_REV) odata = 1;' passed the 85-row version -- the REV rows
-     checked only the pc)          lb/lh rev v0, ctl v0, istat/imask lb/lh v0, dog v0, dog lh v0, time lb/lh v0
+     checked only the pc)          lb/lh rev v0, ctl v0, ctl lb v0, istat/imask lb/lh v0, dog v0, dog lh v0, time lb/lh v0
      every one at 2 bytes (lh sees every value lb sees) and over a register whose LOW BYTES ARE NONZERO, so a decline
      that answers the register shows (kimi CLI, second closing pass: INTSTAT, INTMASK and DOG held 0 in their low
@@ -162,12 +181,18 @@ DISCLOSED, not rowed:
     `paddr -= mem->devices[i].baseaddr;'), and on a declined access nothing between the entry and the tail writes
     HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 (the then 40-row test) in kill table 1.
-  * a fall-through confined to the two label cells whose arms have NO body for that access, both EQUIVALENT:
-      CRIME_DOG (0x30)       `No warning.' -- the arm is `break;'
-      CRIME_CONTROL, reads   the arm acts only on MEM_WRITE
-    Each measured as a survivor in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
+  * a fall-through confined to the THREE label cells whose arms have NO body for that access, all EQUIVALENT:
+      CRIME_DOG (0x30)          `No warning.' -- the arm is `break;'
+      CRIME_CONTROL, reads      the arm acts only on MEM_WRITE
+      CRIME_REV, outside the PROM-probe window   the arm acts only when the pc is in the window
+    The first two measured as survivors in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through); the REV
+    cell is the `lb/lh rev pc' rows' converse, read from the arm.  [This said "the two label cells" until repair 12 --
+    kimi CLI, closing pass 6.]
   * ACCEPT cells at unrowed slots: the rows touch accepted accesses at +0x00, +0x04, +0x08, +0x10, +0x18, +0x30,
-    +0x34, +0x38, +0x210, +0x214, +0x1f8 and +0x278 (not an exhaustive list of what the window accepts); an accept arm
-    narrowed by an address strictly INSIDE the window at an unrowed slot (e.g. `len == 8 && relative_addr != 0x100',
-    kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.
+    +0x34, +0x38, +0x40, +0x210, +0x214, +0x1f8 and +0x278 (not an exhaustive list of what the window accepts); an
+    accept arm narrowed by an address strictly INSIDE the window at an unrowed slot (e.g. `len == 8 && relative_addr !=
+    0x100', kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.  TOUCHING a slot in ACCEPTS pins its LATCH
+    behaviour, never its acceptance -- what pins acceptance is item 6 (`latch said' for the announced form, the value
+    rows for the silent form).  [This bullet implied a touched slot was pinned until repair 12 -- the Opus seat, closing
+    pass 6.]
   * an effect ADDED to the decline arm and keyed on ONE UNNAMED offset (item 9 rows the READ answer at every named
     label) -- a refused store that lands only at
@@ -185,8 +210,20 @@ DISCLOSED, not rowed:
     which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
     (the tail recomputes it), CONTROL and REV (the prelude rewrites them) such a landing is EQUIVALENT.
-  * an accepted WRITE (4 or 8 bytes) at +0x00 or +0x08 shrunk away: the prelude rewrites CRIME_REV and CRIME_CONTROL on
-    every access, so no round trip there can observe whether the store was accepted (the CONTROL arm's effects are
-    rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
-    needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
+  * a ROUND TRIP cannot observe an accepted WRITE at +0x00 or +0x08 (the prelude rewrites CRIME_REV and CRIME_CONTROL
+    on every access) -- but the write's EFFECTS can, and are rowed: from the PROM-probe window an accepted write
+    REDIRECTS the pc (revP sw pc, revP sd pc), and at CONTROL the arm's effects (sw08 halts, sw08 msg ctl at 4 bytes;
+    acc ctl sd at 8).  [This bullet said "no round trip there can observe whether the store was accepted" as though
+    nothing could, and it was wrong twice: the window redirect (measured by the Opus seat, G4) and the 8-byte CONTROL
+    write, which no row carried until repair 12 -- closing pass 6.]  The 4R-high cell at +0x00 is carried by `rev pc
+    ctl' (its redirect needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
+  * `odata = idata' in the decline arm: EQUIVALENT by construction -- `idata' is set only under MEM_WRITE and `odata' is
+    consumed only under MEM_READ (measured 141/141 on the 141-row test by the Opus seat, closing pass 6).  `cpu->is_32bit' (the REV arm's
+    pc-pointer refresh) holds one value per machine, like the configuration lvalues above.  Accepted-side address bits 7
+    and 8: the mid session's accepted sd +0x1f8 carries both, before and between its refusals (a latch keyed on them is
+    killed -- kimi-k3's C3, 139/141 on the 141-row test); an ACCEPT arm keyed on them is the unrowed-slot class above.
+  * ACCEPTS has 46 ENTRIES, not 46 kinds: the 40-cell pre-set/re-arm floor, the two ENDIANESS strengthenings, and four
+    positional repeats of default-arm kinds (`sw/lw 0x04' repeat 0x34's low lane; `sd/ld 0x278' repeat 0x40's 8-byte
+    kinds, and are the prologue's only accepted access with address bit 9 set -- an unrecorded strengthening until
+    repair 12; kimi CLI, closing pass 6).
   * a decline answering a selection of the register's bytes at CRIME_REV, CRIME_CONTROL or CRIME_TIME CONFINED to
     bytes the model holds at 0 there -- REV = 0x11: bytes 1-7; CONTROL = 0x100: byte 0 and bytes 2-7; TIME: the 4-byte
@@ -493,5 +530,6 @@ row("sb08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "1W: the session completes (a RA
 A = Addr(CODE)
 x, _ = st(A, "sh", CRIME + 0x08, 0x0201)
-e, _ = st(A, "sh", CRIME + 0x08, 0x0900)       # glm, closing pass: ENDIANESS (0x0100) is the arm's third tested bit
+e, _ = st(A, "sh", CRIME + 0x08, 0x0900)       # glm, closing pass: ENDIANESS (0x0100) -- CLEARED by the arm, never
+                                               # branched on (this said "the arm's third tested bit" until repair 12)
 y, _ = st(A, "sh", CRIME + 0x08, 0x0a00)
 f, _ = st(A, "sh", CRIME + 0x08, 0xffff)        # all-ones: every bit a data-keyed narrowing could key on, set
@@ -724,5 +762,6 @@ x, _ = ld(A, "lb", CRIME + 0x07, "v0"); c += x
 #  *** REPAIR 11 (closing pass 5; flagship ruling regress/artifacts/lcaisalane/FABLE_C3_RULING_20260914.md, part A):
 #  the window was crossed with 4R/4W/8W and NOT 8R -- this said "in both directions (the pc test ignores the
-#  direction)", which crossed the window with the DIRECTION on writes only; five seats and the Opus seat's measurement
+#  direction)", and the missing cell was the 8-byte WIDTH on reads [this read "the DIRECTION on writes only" until
+#  repair 12 -- kimi-k3:cloud, closing pass 6]; five seats and the Opus seat's measurement
 #  (a re-arm/pre-set keyed on an accepted 8R from the window, 141/141) put `ldP' in, as a FLOOR cell.  The two CONTROL
 #  0x0100 (ENDIANESS) writes are a CLAUSE-(e) STRENGTHENING, not floor: the arm clears ENDIANESS unconditionally and
@@ -905,4 +944,8 @@ def free_one(op, off, val):
     ran = t.split("continue", 1)[1] if "continue" in t else ""
     ln = 1 if op in ("lb", "lbu", "sb") else 2
+    #  `clean' honoured since repair 12 (the flagship ruling, closing pass 6: a count from an unclean transcript is not
+    #  evidence -- ignoring it could only false-RED, but every other count row already said `unclean')
+    if not clean:
+        return "unclean"
     return ran.count("unimplemented len=%d at 0x%x -- declined.  (once) ]" % (ln, off))
 
@@ -949,4 +992,97 @@ t, clean = session(c + roundtrip(A))
 row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses, then +0x00, +0x38 -> one (once)")
 row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")
+#  REPAIR 12 (closing pass 6; flagship ruling regress/artifacts/lcaisalane/FABLE_C4_RULING_20260915.md, part A): the two
+#  rows ACCEPTS feeds COUNT notices, so an ACCEPTED cell wrongly declined -- an accept guard GROWN by one conjunct, the
+#  de-escalation clause's own shape -- takes the session's one notice itself and the count stays 1: codex's C1 (CONTROL
+#  4R) and the Opus seat's G1-G5 (CONTROL 8R/8W, INTSTAT 8, TIME 4, REV window 4W, INTMASK 4W) each scored 141/141
+#  (regress/artifacts/crimewidthkill/opus_close6_20260915/).  All 46 ACCEPTS accesses run BEFORE the lh +0x06 here, and
+#  the width arm declines before the REV pc test, so that lh must still carry its OWN announce: any grown accept guard
+#  at any ACCEPTS cell steals it.  CHANNEL: the announce text of the session's first GENUINE refusal (codex's row).
+row("latch said", said(t, 2, 0x6, clean), 1, "lh +0x06, after all 46 ACCEPTS cells: ITS OWN announce")
+
+#  The same announce, FREE-RUNNING from the PROM window (glm, closing pass 6: `(pc in the window ? debug : fatal)('
+#  scored 141/141 -- every free-running refusal ran from CODE).  Clause (e) by the DEPENDS-ON bound (the decline arm does
+#  not read the pc); rowed as a licensed strengthening because the PROM's probe loop is the one real caller that issues
+#  CRIME accesses from that window.  CHANNEL: the fatal() text, which a debug() would not print while free-running.
+A = Addr(CODE)
+c = ["ra=0x%x" % RA, "at=0x%x" % CRIME, "v0=0x%x" % SENT,
+     "put w 0x%x, 0x%08x" % (PROBE_PC, enc("lb", "at", "v0")),
+     "put w 0x%x, 0x%08x" % (PROBE_PC + 4, OP_NOP),
+     "put w 0x%x, 0x%08x" % (PROBE_PC + 8, OP_B_SELF),
+     "put w 0x%x, 0x%08x" % (PROBE_PC + 12, OP_NOP),
+     "pc=0x%x" % PROBE_PC, "<RUN>", "print v0"]
+t, clean = session(c)
+ran = t.split("continue", 1)[1] if "continue" in t else ""
+row("free revP said", ran.count("unimplemented len=1 at 0x0 -- declined.  (once) ]") if clean else "unclean", 1,
+    "free-running lb +0x00 FROM the PROM window")
+
+#  THE SILENT FORM (repair 12, licensed): an accepted cell bypassed with NO announce -- `if (len == 8 && relative_addr ==
+#  CRIME_CONTROL) goto crime_declined;' before the width test (the Opus seat's G6, 141/141 with `latch said' green) --
+#  is outside the de-escalation class (the deleted exit(1) would not have announced it either) and is DISCLOSED by class
+#  in item 6; these VALUE rows carry the cells where such a bypass is GUEST-VISIBLE, derived per cell from the switch and
+#  the width arm (the flagship ruling: from the enumeration, never from the mutants that happened to be built):
+#    REV window 4W/8W/8R, CONTROL 8R/8W, INTSTAT 8W/8R/4W, INTMASK 4W, TIME 8W, the default arm's 4W/4R at +0x40.
+#  The other ACCEPTS cells are either pinned elsewhere or EQUIVALENT when bypassed (item 6).
+#  REV window: CHANNEL = the PROM-probe redirect (pc = ra), which only an ACCEPTED access reaches.
+A = Addr(CODE)
+c = ["ra=0x%x" % RA]
+x, _ = st(A, "sw", CRIME + 0, 0, at=PROBE_PC); c += x + ["print pc"]
+x, _ = st(A, "sd", CRIME + 0, 0, at=PROBE_PC); c += x + ["print pc"]
+x, _ = ld(A, "ld", CRIME + 0, "s0", at=PROBE_PC); c += x + ["print pc"]
+t, clean = session(c)
+for i, k in enumerate(("sw", "sd", "ld")):
+    v = nth(t, "pc", i)
+    row("revP %s pc" % k, "absent" if v is None else "0x%x" % v, "0x%x" % RA,
+        "accepted %s CRIME_REV from 0xbfc05180: pc = ra" % k)
+#  CONTROL 8R: CHANNEL = its value, 0x100 (the prelude's ENDIANESS; a declined read answers 0).  INTSTAT 8R: its value
+#  SOFTINT | HARDINT, recomputed by every access's tail.  INTMASK 4W: the high half lands (ld +0x18).  TIME 8W: an ODD
+#  seed stays odd (every update adds a multiple of 66), and the register is even before it -- so parity says whether
+#  the store landed, whatever the host clock added.  Default arm +0x40 4W (the high lane) and 4R: the value round trip.
+#  CONTROL 8W: its arm prints the unimplemented-control text for a leftover bit (0x01), which a declined store cannot.
+A = Addr(CODE)
+c = []
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
+t, clean = session(c + ["print s0", "print s1", "print s2", "print s3", "print a1", "print a2"])
+tv = nth(t, "s3", 0)
+row("acc ctl ld", pr(t, "s0"), "0x100", "accepted ld +0x08 answers CONTROL (0x100)")
+row("acc istat ld", pr(t, "s1"), "0x%x" % BIT, "accepted ld +0x10 answers INTSTAT = SOFTINT")
+row("acc imask sw", pr(t, "s2"), "0x1000000000000000", "accepted sw +0x18 lands in the high half")
+row("acc time sd", "absent" if tv is None else ("odd" if tv & 1 else "even"), "odd",
+    "accepted sd +0x38 of an odd seed: TIME stays odd (raw %s)" % tv)
+row("acc 40 lw", pr(t, "a1"), "0xa0b0c0d", "accepted lw +0x40 answers the high half the sw stored")
+row("acc 40 sw", pr(t, "a2"), "0xa0b0c0d00000000", "accepted sw +0x40 lands in the high half (ld)")
+row("acc ctl sd", count(t, "CRIME_CONTROL: unimplemented", clean), 1, "accepted sd 0x01 +0x08 prints the text")
+#  INTSTAT 8W and 4W: CHANNEL = cause.IP2.  With INTMASK = SOFTINT = BIT and the line low (SOFTINT's store goes to the
+#  default arm, which does not reassert), an ACCEPTED store at +0x10 reasserts and raises IP2; a declined one reaches the
+#  tail, which recomputes INTSTAT but does NOT touch the line.  Between the two, SOFTINT = 0 and an INTMASK store lower it.
+A = Addr(CODE)
+c = []
+x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
+x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
+c += ["print cause"]
+x, _ = st(A, "sd", CRIME + 0x10, 0); c += x
+c += ["print cause"]
+x, _ = st(A, "sd", CRIME + 0x20, 0); c += x
+x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
+x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
+c += ["print cause"]                                # immediately before the sw, as `pre' is before the sd
+x, _ = st(A, "sw", CRIME + 0x10, 0); c += x
+c += ["print cause"]
+t, clean = session(c)
+row("istw pre", ip2(nth(t, "cause", 0)), "clear", "CONTROL: IP2 low after SOFTINT's default-arm store")
+row("istw sd", ip2(nth(t, "cause", 1)), "set", "accepted sd +0x10 reasserts: IP2 set")
+row("istw mid", ip2(nth(t, "cause", 2)), "clear", "CONTROL: lowered again (SOFTINT 0, INTMASK store), SOFTINT set")
+row("istw sw", ip2(nth(t, "cause", 3)), "set", "accepted sw +0x10 reasserts: IP2 set")
 
 npass = sum(1 for _, ok in rows if ok)
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
  CONTROL 4R, TIME 4W/4R: the prelude rewrites or the high half is 0).
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
M = {
    "base": [],
    # C1 (codex): the accepted 4R at CRIME_CONTROL declined
    "C1_ctl4r": [(LEN4, "\t} else if (len == 4 && (relative_addr != CRIME_CONTROL || writeflag != MEM_READ)) {\n")],
    # C2 (glm): the announce channel keyed on the PROM-window pc
    "C2_chan_win": [(FATAL, "\t\t\t(((uint32_t)cpu->pc & 0xffffff00) == (uint32_t)0xbfc05100 ? debug : fatal)"
                            "(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n")],
    # C3 (kimi-k3): pre-set on an accepted access with address bit 7 or 8, before the switch
    "C3p_pre_b78": [(GOTOSW, "\t\tgoto crime_declined;\n\t}\n\n\tif (relative_addr & 0x180)\n"
                             "\t\td->warned |= CRIME_W_LEN;\n\n\tswitch (relative_addr) {\n")],
    # C3r: the re-arm twin
    "C3r_rearm_b78": [(GOTOSW, "\t\tgoto crime_declined;\n\t}\n\n\tif (relative_addr & 0x180)\n"
                               "\t\td->warned = 0;\n\n\tswitch (relative_addr) {\n")],
    # C4 (minimax): a declined read answers relative_addr & 7
    "C4_ans_ra7": [(GOTO, "\t\todata = (relative_addr & 7);\n" + GOTO)],
    # C5 (kimi CLI): a declined read answers idata
    "C5_ans_idata": [(GOTO, "\t\todata = idata;\n" + GOTO)],
    # G1 (own hunt): the 8-byte accept guard narrowed at CRIME_CONTROL (8W and 8R there declined)
    "G1_acc8_ctl": [(LEN8, "\tif (len == 8 && relative_addr != CRIME_CONTROL) {\n")],
    # G2: the 8-byte accept guard narrowed at CRIME_INTSTAT
    "G2_acc8_istat": [(LEN8, "\tif (len == 8 && relative_addr != CRIME_INTSTAT) {\n")],
    # G3: the 4-byte accept guard narrowed at CRIME_TIME
    "G3_acc4_time": [(LEN4, "\t} else if (len == 4 && relative_addr != CRIME_TIME) {\n")],
    # G4: the 4-byte accept guard narrowed at CRIME_REV writes (sw +0x00, swP -- the window's redirect)
    "G4_acc4w_rev": [(LEN4, "\t} else if (len == 4 && (relative_addr != CRIME_REV || writeflag != MEM_WRITE)) {\n")],
    # G5: the 4-byte accept guard narrowed at CRIME_INTMASK writes
    "G5_acc4w_imask": [(LEN4, "\t} else if (len == 4 && (relative_addr != CRIME_INTMASK || writeflag != MEM_WRITE)) {\n")],
    # G6: a SILENT accept-set shrink (a bypass, not guard growth): 8-byte CONTROL skips to the tail, no announce
    "G6_skip8_ctl": [(LEN8, "\tif (len == 8 && relative_addr == CRIME_CONTROL)\n\t\tgoto crime_declined;\n\n" + LEN8)],
}

M = dict(I.M)
_ns = {}
exec(io.open(os.path.join(HERE, "mutants_c6_opus.py"), encoding="utf-8").read().split("```

## MUTATION-TEST TABLE 10 -- results (`POSTTABLE.out`)

```
POSTTABLE -- #529 kill table 10 (TARGETED, repair 12; 157 rows).  Written after the table (table10.out ends KILL529J_DONE);
PRETABLE.out 04:54:51 predates the launch (kill529j.run-045508.sh, frozen) and every log (probe_base.raw 05:11:07).

DRIVER   kill529j.run-045508.sh, clone /tmp/gxopuscrime, BASELINE_CMP CLEAN, own .MUTANT during the builds; 40 legs BUILD_OK
         + restored; `CLONE RESTORED cmp=clean binary-nt-source=yes', `restored == base (byte-identical)'; no mutant binary
         identical to base.  Re-checked by hand after the run: no .MUTANT, dev_sgi_ip32.c cmp-clean vs GXEMUL-SEC, gxemul
         newer than the source.
INSTRUMENT  crime_width_probe.table10.py (frozen at launch).  The shipped regress/crime_width_probe.py changed AFTER the
         freeze in its DOCSTRING only -- three score quotes gained their era ("on the 141-row test") for the score-claims
         scan; the code AST without the docstring is IDENTICAL (checked).  The fixed build: 157/157, CONTROL=OK
         (../probe_first13_fix.out, build/gxemul, dev_sgi_ip32.c CMP_CLEAN).
LOGS     40 logs/probe_*.raw, every one ends CRIMEP_DONE; CRIMEP_CONTROL=OK on 39, FAIL on W_8r (predicted).
LOAD     four probe lanes; #530's kill table 6 (two lanes) ran concurrently in its own clone -- no leg off prediction.

check_pred.out:  CHECKPRED exact=40 differs=0 of 40 measured (40 predicted)
   base 157/157.
   The 16 PRE-SET kills 155/157, each red on exactly {latch x5, latch said}: the Opus sixth-closing seat's "they will also
   red latch said" is now MEASURED, not reasoned; r_byp_rev 156/157 on {latch x5} alone (its REV refusals re-announce,
   so the lh +0x06 keeps its own text -- as predicted from table 9's count of 2).
   The Opus seat's escapes, now DETECTED on exactly their predicted rows: C1_ctl4r 156 (latch said), C2_chan_win 156
   (free revP said), G1_acc8_ctl 154 (latch said, acc ctl ld, acc ctl sd), G2_acc8_istat 154 (latch said, acc istat ld,
   istw sd), G3_acc4_time 156 (latch said), G4_acc4w_rev 155 (latch said, revP sw pc), G5_acc4w_imask 155 (latch said,
   acc imask sw), G6_skip8_ctl 155 (acc ctl ld, acc ctl sd -- the SILENT form; latch said green, as the seat measured).
   The twelve SILENT bypasses, each red on its own value row(s): S_revPsw/S_revPsd 156 (revP sw/sd pc), S_revPld 155
   (acc8 near, revP ld pc), S_ctlld 156, S_ctlsd 156, S_istld 156, S_istsd 156 (istw sd), S_istsw 156 (istw sw), S_imsw
   156, S_timesd 156 (acc time sd: TIME stayed EVEN), S_40sw 155 (acc 40 lw, acc 40 sw), S_40lw 156.
   RA3 (the flagship ruling): the d->warned-keyed accept shrink in BOTH forms -- W_8r 145/157, CONTROL=FAIL, exactly the
   twelve predicted rows (the eight keeps / read-back rows and the four time ctl rows); W_8w 156/157 (lo keeps -- the
   keeps session seeds +0x40 with an sd AFTER its first refusal).  The flagship seat predicted the 8W form "may escape";
   by the trace in PRETABLE 10 and now by measurement it does not.

FLOOR    (d) the ACCEPT side of every ACCEPTS cell in the guard-growth form is carried by `latch said' (C1, G1-G5 red on it);
         (e) the silent form DISCLOSED by class in item 6 and CAUGHT at the twelve guest-visible cells (S_* each red); the
         pc-window notice channel rowed as a strengthening (C2).  Item 6 no longer claims "any single cell" unqualified.
NOT RE-MEASURED  every table 1-9 kill: no existing session's command list changed (the targeting rule), and the only new
         row in an existing session (`latch said') is in latch x5, whose kills are the 17 re-run here.
RECORDS  the sixth-pass brief called the Opus fifth-closing seat's mutants "P1-P7" (table 9 ran four) and the flagship
         adjudication brief said "six seats CLOSE" while listing seven -- both corrected here, not in the briefs (they are
         the records of what was sent); POSTTABLE 9's FLOOR line "(d) the window x kind cross is closed" is true of the
         LATCH side only -- the ACCEPT side of the same cells was not closed until this table (the flagship ruling).
```

## QUESTIONS

1. **Verify the accept-side enumeration.**  For each ACCEPTS cell, is the ANNOUNCED form (the width/accept guard grown by
   a conjunct, so the cell reaches the announcing decline) caught by `latch said', and is the SILENT form (a bypass that
   declines with no announce) either caught by a value row, EQUIVALENT (as item 6 names), or pinned by an existing row?
   Name any cell whose disposition is missing or wrong, and check the generality argument for `latch said' against the
   function (does every ACCEPTS access really run before the lh +0x06, and can a grown guard at some cell decline WITHOUT
   announcing while the latch is still clear?).
2. **Can each new row's channel vary under the mutant it names?**  In particular the IP2 rows (`istw sd`/`istw sw` -- the
   tail must not assert the line) and `acc time sd` (parity).
3. **Is there a floor gap in the 157-row test?**  The smallest edit to `dev_sgi_ip32.c` that undoes part of the fix's
   behaviour and still scores 157/157, as an exact edit, with the row you expected to catch it.  DISCLOSED items are
   outside the question; say if one is disclosed wrongly.
4. **Which statement in this brief, in POSTTABLE 10, or in the probe header, is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
