# CLOSING PASS 6 -- `crimewidthkill` (#529): does repair 11 close the accepted-kind cross?  Liveness token `CRIME_CLOSE6_20260914`.

VERDICT LINE FIRST: `CLOSES` (no floor gap remains in the 141-row test) or `GAP: <exact source edit to dev_sgi_ip32.c>`,
then the token.

This is a routine software-testing review of an open-source hardware emulator (GXemul) and its regression test.
"Mutant" means a deliberately modified copy of the emulator's C source used to check that the test notices the change
(standard mutation testing).  Please check the premises, not only the reasoning, and say what you could not check.
Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` only.  File-reading seats: `src/devices/dev_sgi_ip32.c`
(`DEVICE_ACCESS(crime)`), `regress/crime_width_probe.py`, `regress/artifacts/crimewidthkill/`.

## WHY THIS PASS EXISTS, AND WHAT IT IS ASKED TO DO

The fifth closing pass found the accepted-kind cross one cell short: the REV PROM-probe window was crossed with 4R, 4W and
8W but not 8R (`ldP'), so a re-arm or pre-set keyed on an accepted 8-byte read from the window scored 141/141 (the Opus
seat measured it; five reading seats named it).  The flagship seat, adjudicating last
(regress/artifacts/lcaisalane/FABLE_C3_RULING_20260914.md, part A), ruled it a FLOOR breach -- repair 10 had already
crossed three of the window's four kinds -- and graded the ENDIANESS-keyed latch, the multi-axis notice-channel joint and
the machine-configuration answer lvalues clause (e) (disclose).  Repair 11 adds `ldP' (floor) and two CONTROL 0x0100
writes (a clause-(e) strengthening, recorded as such), rewrites item 9 (its "every lvalue nonzero" was false), and adds
the three disclosures.  Two consecutive passes breached the accepted-kind cross, so this pass VERIFIES THE ENUMERATION:
is `ACCEPTS' now exactly the (branch side x kind) floor the function's own branches define, with the contract saying
which cells are floor and which are clause-(e) strengthening?

## SETTLED (recorded; re-stated because the questions depend on it)

* **The fix** (unchanged since pass 2; every seat of seven passes found it correct): a refused width is announced once per
  device instance (`int warned`, bit `CRIME_W_LEN`) and `goto crime_declined;` past the register switch to the common
  tail, which answers a read 0 and returns 1.
* **History**: 40 -> 71 -> 85 -> 111 -> 121 -> 127 -> 131 -> 141 rows (repair 11 keeps 141, ACCEPTS 46); NINE mutation-test tables, each with a written
  PRETABLE before it ran and a mechanical prediction checker.
* **A refused read's answer** is the low `len` bytes of the `odata` the decline hands the tail (memory_writemax64).
* **Free-running vs stepped**: a stepped probe cannot tell debug() from fatal(); a free-running one can (verbose == 0).

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
artifacts/crimewidthkill/ (killtable_20260913/ through killtable8_20260914/):
  1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                       <op> surv (six widths), hi surv, latch surv, sb08 run
  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)   lb/lh/sb/sh pc and exc, lb/lh/lbu/lhu v0
  3. the refused access FALLING INTO THE REGISTER SWITCH -- the goto lost, or narrowed by width, direction, or ADDRESS.
     The switch's observable arms, per refusal cell:
        CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
                                          sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
                                          and the arm's three TESTED idata bits (DOG 0x200, RESET 0x800,
                                          ENDIANESS 0x100) each both ways at 2W: sh 0x0201,
                                          0x0900, 0x0a00 with sh08 0x0800       sh08b msg, sh08b run
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
     remaining label (free rev/istat/imask/dog/time said).  *** Until repair 10 the channel was pinned at ONE cell (+0x07):
     `(relative_addr & 8 ? debug : fatal)(' and `(len == 2 ? debug : fatal)(' each scored 131/131 on the 131-row test (codex, the Opus
     seat, fourth closing pass).  One refusal per free-running session -- the latch silences any second one. ***
  6. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this),
     at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
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
     checked only the pc)          lb/lh rev v0, ctl v0, istat/imask lb/lh v0, dog v0, dog lh v0, time lb/lh v0
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
  * a fall-through confined to the two label cells whose arms have NO body for that access, both EQUIVALENT:
      CRIME_DOG (0x30)       `No warning.' -- the arm is `break;'
      CRIME_CONTROL, reads   the arm acts only on MEM_WRITE
    Each measured as a survivor in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
  * ACCEPT cells at unrowed slots: the rows touch accepted accesses at +0x00, +0x04, +0x08, +0x10, +0x18, +0x30,
    +0x34, +0x38, +0x210, +0x214, +0x1f8 and +0x278 (not an exhaustive list of what the window accepts); an accept arm
    narrowed by an address strictly INSIDE the window at an unrowed slot (e.g. `len == 8 && relative_addr != 0x100',
    kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.
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
  * an accepted WRITE (4 or 8 bytes) at +0x00 or +0x08 shrunk away: the prelude rewrites CRIME_REV and CRIME_CONTROL on
    every access, so no round trip there can observe whether the store was accepted (the CONTROL arm's effects are
    rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
    needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
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

## THE REPAIR DIFF -- repair 10 -> repair 11 (the 141-row test, ACCEPTS 43 -> 46) (`git diff --no-index`, verbatim; 6 hunks)

```diff
diff --git "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable8_20260914\\crime_width_probe.table8.py" "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
index 0dc188e..3412750 100644
--- "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable8_20260914\\crime_width_probe.table8.py"
+++ "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
@@ -72,6 +72,8 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable8_20260914/):
      refused once per session, first, so `|| == CRIME_REV' and `|| == CRIME_TIME' passed)
      and the latch PRE-SET before any refusal, over the KIND x LABEL CROSS (`ACCEPTS'): {8W, 8R, 4W, 4R} at every
-     case label, REV also from the PROM-probe window in both directions, CONTROL's writes at both widths x {0x0201,
-     0x0001, 0, 0x0200} (DOG x leftover, all four), and the default arm's six kinds in both 4-byte lanes -- all in
+     case label, REV also from the PROM-probe window at all four kinds (`ldP' since repair 11 -- this said "in both
+     directions" and the window had no 8R; the flagship ruling, closing pass 5), CONTROL's writes at both widths x
+     {0x0201, 0x0001, 0, 0x0200} (DOG x leftover, all four; plus 0x0100 ENDIANESS at both widths, a clause-(e)
+     strengthening -- the arm never branches on it), and the default arm's six kinds in both 4-byte lanes -- all in
      latch x5's prologue, before its first refusal; also warm once (sd first) and time once (ld first).  HARD_RESET's
      true side: disclosed (it stops the CPUs).  *** This said "DERIVED FROM THE FUNCTION'S OWN BRANCHES ... both sides
@@ -116,5 +118,5 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable8_20260914/):
      warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
      4-byte arm's re-arm open on the closing pass -- now the KIND x LABEL CROSS, the SAME list as item 4's pre-set
-     (`ACCEPTS', 43 kinds; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing seat:
+     (`ACCEPTS', 46 kinds since repair 11 -- 43 before `ldP' and the two ENDIANESS writes; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing seat:
      CONTROL's read, DOG-clear and zero-leftover sides; the fourth closing pass: a re-arm on an accepted WRITE at
      INTSTAT/INTMASK or REV and on CONTROL's 0x0200 cell, each 131/131 on the 131-row test) -- each accepted kind between two refusals
@@ -133,6 +135,10 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable8_20260914/):
      `& 0xffff0000' -- answers 0 to every lb/lh by construction and is EQUIVALENT; this said "ANY selection ... shows"
      until the kimi CLI seat, fourth closing pass.]  And the answer SOURCE other than the addressed register: every
-     lvalue the function reads is nonzero where a refused answer is read, including HARDINT -- latched only in the gate
-     session, where refused lb/lh now read it (kimi-k3:cloud, the Opus seat, fourth closing pass: a decline answering
+     lvalue the function reads that is NONZERO in some session is nonzero where a refused answer is read in that
+     session, HARDINT included -- latched only in the gate session, where refused lb/lh now read it -- and SOFTINT
+     (nonzero in the imask/istat/gate sessions; the Opus fifth-closing seat measured `odata = SOFTINT' red there).
+     [Corrected 2026-09-14, flagship ruling on closing pass 5: this said "every lvalue the function reads is nonzero
+     where a refused answer is read" -- FALSE: `d->use_fb', `flag_for_128MB' and `idata' are 0 at every refused read,
+     and `odata = d->use_fb' scored 141/141 (the Opus seat).  Those are DISCLOSED below.]  The HARDINT source (kimi-k3:cloud, the Opus seat, fourth closing pass: a decline answering
      `d->reg[CRIME_HARDINT / 8]' scored 131/131 on the 131-row test)                                          gate lb v0, gate lh v0.
      CONTROL is answered at both widths (ctl lb v0, ctl v0; the Opus
@@ -183,10 +189,20 @@ DISCLOSED, not rowed:
     rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
     needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
-  * a decline answering a selection of the register's bytes at CRIME_REV, CRIME_CONTROL or CRIME_TIME that the model
-    holds at 0 there -- the ADDRESSED lanes (bytes 0-1 at a label), or the 4-byte half above the low word -- is
-    EQUIVALENT (the prelude rewrites REV = 0x11 and CONTROL = 0x100 on every access; TIME is kept to 32 bits).  At
+  * a decline answering a selection of the register's bytes at CRIME_REV, CRIME_CONTROL or CRIME_TIME CONFINED to
+    bytes the model holds at 0 there -- REV = 0x11: bytes 1-7; CONTROL = 0x100: byte 0 and bytes 2-7; TIME: the 4-byte
+    half above the low word -- is EQUIVALENT (the prelude rewrites REV and CONTROL on every access; TIME is kept to 32
+    bits).  [Corrected 2026-09-14 from closing pass 5 (glm): this read "the ADDRESSED lanes (bytes 0-1 at a label)",
+    which at REV and CONTROL include a NONZERO byte -- item 9's v0 rows exist to catch exactly that selection.]  At
     INTSTAT, INTMASK and DOG every byte is seeded nonzero, so any selection shows (Opus, second closing pass; glm, third).
   * a latch keyed on a JOINT predicate (e.g. only 2-byte refusals at CRIME_TIME), or on one unnamed offset other than the
     default-arm cells the latch rows refuse at: clause (e), the single-axis generating set being the floor.
+  * (closing pass 5; the Opus seat measured each at 141/141 on the 141-row test; the flagship ruling graded each clause
+    (e)) a latch re-armed or pre-set by a CONTROL write's ENDIANESS bit (0x100) -- the arm clears it unconditionally and
+    never branches on it; the two ENDIANESS writes in ACCEPTS since repair 11 are a strengthening, not a floor claim
+    over value bits; the announce CHANNEL keyed on a JOINT of axes (e.g. `(relative_addr == CRIME_INTSTAT && len == 2 ?
+    debug : fatal)(') -- item 5 rows the channel on each SINGLE axis; and a decline answering a MACHINE-CONFIGURATION
+    lvalue (`d->use_fb', `flag_for_128MB'), which holds one value per machine and is 0 on this probe's -M 64 non-graphics
+    ip32 -- a graphics O2 (use_fb = 1) would see `odata = d->use_fb' answer 1.  Unrowable on one machine, like the
+    function-static latch below.
   * a re-arm or pre-set inside the HARD_RESET branch of the CONTROL arm: an accepted write that takes it stops every
     CPU, so nothing can follow it in the session.  Unrowable, not merely unrowed.
@@ -704,7 +720,13 @@ x, _ = ld(A, "lb", CRIME + 0x07, "v0"); c += x
 #  leftover 0) cell (0x0200) each scored 131/131 while changing the announce count.  So the list is now the CROSS:
 #  {8W, 8R, 4W, 4R} at every label (a label is 8-aligned, so its 4-byte access is the high lane), REV also from the
-#  PROM-probe window in both directions (the pc test ignores the direction), CONTROL's writes at both widths x
-#  {0x0201, 0x0001, 0, 0x0200}, and the default arm's six kinds in both 4-byte lanes.  ONE list, used here (re-arm)
-#  AND as latch x5's prologue (pre-set). ***
+#  PROM-probe window, CONTROL's writes at both widths x {0x0201, 0x0001, 0, 0x0200}, and the default arm's six kinds
+#  in both 4-byte lanes.  ONE list, used here (re-arm) AND as latch x5's prologue (pre-set). ***
+#  *** REPAIR 11 (closing pass 5; flagship ruling regress/artifacts/lcaisalane/FABLE_C3_RULING_20260914.md, part A):
+#  the window was crossed with 4R/4W/8W and NOT 8R -- this said "in both directions (the pc test ignores the
+#  direction)", which crossed the window with the DIRECTION on writes only; five seats and the Opus seat's measurement
+#  (a re-arm/pre-set keyed on an accepted 8R from the window, 141/141) put `ldP' in, as a FLOOR cell.  The two CONTROL
+#  0x0100 (ENDIANESS) writes are a CLAUSE-(e) STRENGTHENING, not floor: the arm clears ENDIANESS unconditionally and
+#  never branches on it, so it is outside CONTROL's generating set {DOG, HARD_RESET, leftover}; they are here only
+#  because the Opus seat measured them killing an ENDIANESS-keyed latch with no row disturbed.  46 kinds. ***
 ACCEPTS = (("sd", 0x00, 0), ("ld", 0x00, 0), ("sw", 0x00, 0), ("lw", 0x00, 0),
            ("lwP", 0x00, 0), ("swP", 0x00, 0), ("sdP", 0x00, 0),
@@ -718,4 +740,5 @@ ACCEPTS = (("sd", 0x00, 0), ("ld", 0x00, 0), ("sw", 0x00, 0), ("lw", 0x00, 0),
            ("sd", 0x40, 0), ("ld", 0x40, 0), ("sw", 0x40, 0), ("lw", 0x40, 0),
            ("sw", 0x34, 0x0badcafe), ("lw", 0x34, 0), ("sw", 0x04, 0), ("lw", 0x04, 0),
+           ("ldP", 0x00, 0), ("sw", 0x08, 0x0100), ("sd", 0x08, 0x0100),
            ("sd", 0x278, 0), ("ld", 0x278, 0))
 KINDS = ACCEPTS
```

## THE MUTANTS OF TABLE 9, verbatim (table 8's by name, then the Opus close-5 seat's P1-P7)

```python
M = dict(H.M)
_ns = {}
exec(io.open(os.path.join(HERE, "mutants_c5_opus.py"), encoding="utf-8").read().split("M = {
    "base": [],
    # P1: re-arm inside the PROM-window if, keyed on 8R (ldP -- absent from ACCEPTS)
    "P1_win8r_rearm": [(PCLINE, "\t\t\tif (len == 8 && writeflag == MEM_READ) d->warned = 0;\n" + PCLINE)],
    # P1b: pre-set twin
    "P1b_win8r_preset": [(PCLINE, "\t\t\tif (len == 8 && writeflag == MEM_READ) d->warned |= CRIME_W_LEN;\n" + PCLINE)],
    # P2: re-arm on an accepted CONTROL write carrying ENDIANESS (0x100)
    "P2_ctl_endi_rearm": [(ENDI, "\t\t\tif (idata & CRIME_CONTROL_ENDIANESS) d->warned = 0;\n" + ENDI)],
    # P2b: pre-set twin
    "P2b_ctl_endi_preset": [(ENDI, "\t\t\tif (idata & CRIME_CONTROL_ENDIANESS) d->warned |= CRIME_W_LEN;\n" + ENDI)],
    # P3: channel joint -- INTSTAT and len==2 -> debug
    "P3_chan_istat2": [(FATAL, "\t\t\t(relative_addr == CRIME_INTSTAT && len == 2 ? debug : fatal)(\"[ crime: "
                               "unimplemented len=%i at 0x%x -- declined.\"\n")],
    # P4: answer source = SOFTINT
    "P4_ans_softint": [(GOTO, "\t\todata = d->reg[CRIME_SOFTINT / sizeof(uint64_t)];\n" + GOTO)],
    # P5: answer source = use_fb (machine config, 0 here)
    "P5_ans_usefb": [(GOTO, "\t\todata = d->use_fb;\n" + GOTO)],
    # P6: pre-set on an accepted READ, in the accepted path before the switch
    "P6_pre_read_accpath": [(GOTOSW, "\t\tgoto crime_declined;\n\t}\n\n\tif (writeflag == MEM_READ)\n"
                                     "\t\td->warned |= CRIME_W_LEN;\n\n\tswitch (relative_addr) {\n")],
    # P7: latch bit shifted by address parity
    "P7_latch_addrparity": [(WLINE, "\t\t\td->warned |= CRIME_W_LEN << (relative_addr & 1);\n")],
}

```

## MUTATION-TEST TABLE 9 -- results (`POSTTABLE.out`)

```
POSTTABLE -- #529 kill table 9 (TARGETED, repair 11: ACCEPTS += ldP and the two CONTROL 0x0100 writes; 141 rows).  Written
after the table; PRETABLE.out 11:35:01 predates the launch (kill529i.run-113619.sh, frozen) and every log.

*** THE TABLE RAN IN TWO PARTS, AND BOTH ARE RECORDED. ***  The driver built all 37 legs, restored the clone (`CLONE
RESTORED cmp=clean binary-nt-source=yes', `restored == base (byte-identical)' -- table9.out) and completed 20 probe legs
before the Claude Code process EXITED at ~12:55 on 2026-09-14, killing the four running legs.  On 2026-09-15 the probe
phase ALONE was resumed (_scratchpad/t9resume.sh -> table9.resume.out): the 17 legs without CRIMEP_DONE, from the SAME
binaries the driver built (/tmp/gxcrime529i_bins) and the SAME frozen instrument (/tmp/crime_width_probe.table9.py, cmp-
identical to crime_width_probe.table9.py here), no rebuild, no clone touched, results APPENDED to logs/lane*.out.  The four
killed partial logs are kept as logs/probe_<m>.KILLED.raw (no sentinel; not scored).

INSTRUMENT  crime_width_probe.table9.py BYTE-IDENTICAL to the shipped regress/crime_width_probe.py (repair 11) at launch.
LOGS     37 logs/probe_*.raw, every one ends CRIMEP_DONE, CRIMEP_CONTROL=OK on all 37.
LOAD     four probe lanes; #530's kill table 5 (two lanes) and its closing-pass-4 Opus seat ran concurrently in their own clones.

check_pred.out:  CHECKPRED exact=37 differs=0 of 37 measured (37 predicted)
   base 141/141; the 29 kills whose every table-8 red sat in the two sessions ACCEPTS feeds (17 pre-set -> latch x5, 12
   re-arm -> rearm once) each UNCHANGED by the three added kinds; d3_rearm_wtime 139, nolatch 126, rearm 132 (the three the
   flagship ruling named) unchanged; and the Opus fifth-closing seat's four 141/141 survivors now DETECTED --
   P1_win8r_rearm 140 (rearm once), P1b_win8r_preset 140 (latch x5), P2_ctl_endi_rearm 140 (rearm once),
   P2b_ctl_endi_preset 140 (latch x5) -- exactly the one row each that its augmentation run measured.

FLOOR    (d) the window x kind cross is closed: an accepted 8R from the REV PROM window (`ldP') re-arms and pre-sets the
         latch and both rows see it (P1/P1b), the flagship ruling's floor cell; (e) the two CONTROL 0x0100 writes are a
         CLAUSE-(e) STRENGTHENING (P2/P2b red), recorded as such in the header; item 9 rewritten (its "every lvalue nonzero"
         was false), and the ENDIANESS latch, multi-axis channel joints and machine-configuration lvalues DISCLOSED.
         This replaces POSTTABLE 8's circular "(d) ... at every ACCEPTS kind" line (corrected in place there).
NOT RE-MEASURED  every table 1-8 kill with a red row outside the two sessions whose command lists changed (the targeting
         rule): their kills stand on those rows.
```

## QUESTIONS

1. **Verify the enumeration.**  Derive from `DEVICE_ACCESS(crime)`'s branches the (branch side x accepted kind) cells that
   are floor under the joint-cell rule (a dominating predicate crossed with the body-tested kind partition), and say
   whether `ACCEPTS' (46 kinds) is exactly that set plus the two named clause-(e) strengthenings.  Name any floor cell
   missing, any kind listed that the function cannot take, and any row it feeds whose channel cannot vary.
2. **Is there a floor gap in the repair-11 test?**  The smallest source edit to `dev_sgi_ip32.c` that undoes part of the
   fix's behaviour and still scores 141/141, as an exact edit, with the row you expected to catch it and why it cannot.
   Items on the header's DISCLOSED list are outside the question; say if one is disclosed wrongly.
3. **Which statement in this brief, in POSTTABLE 9, or in the probe header, is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
