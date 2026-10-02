# CLOSING PASS 4 -- `crimewidthkill` (#529): do the test's enumerations now follow the function?  Liveness token `CRIME_CLOSE4_20260913`.

VERDICT LINE FIRST: `CLOSES` (no floor gap remains in the 131-row test) or `GAP: <exact source edit to dev_sgi_ip32.c>`,
then the token.

This is a routine software-testing review of an open-source hardware emulator (GXemul) and its regression test.
"Mutant" means a deliberately modified copy of the emulator's C source used to check that the test notices the change
(standard mutation testing).  Please check the premises, not only the reasoning, and say what you could not check.
Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` only.  File-reading seats: `src/devices/dev_sgi_ip32.c`
(`DEVICE_ACCESS(crime)`), `regress/crime_width_probe.py`, `regress/artifacts/crimewidthkill/`.

## WHY THIS PASS EXISTS, AND WHAT IT IS ASKED TO DO

The third closing pass found more gaps, and its measuring seat named the reason all of them existed: **each class's
enumeration had been built from the members earlier passes happened to find, not from the cases the function itself
distinguishes -- so each class stayed open one case over.**  Repairs 8 and 9 re-derive the enumerations FROM
`DEVICE_ACCESS(crime)`'s OWN CONTROL FLOW:

* PRE-SET (before the first refusal) and RE-ARM (between refusals) by an accepted access: both sides of every `if` an
  accepted access can take and come back from -- `len == 8` (W, R); `len == 4` (W, R) x `(relative_addr & 4)`; every
  case label; REV's pc-window test (in, out); CONTROL's `writeflag` test (R, W) x its DOG test (set, clear) x its
  leftover test (nonzero, zero); the default arm (R, W).  HARD_RESET's true side stops the CPUs: disclosed.
* The latch: its SET keyed on any single axis (every label-first session refuses again elsewhere), its TEST letting a
  label through (every label refused again after the latch is set), its NOTICE suppressed at a label or address-bit
  value (the first refusal's own text is checked in every label-first session).
* The ANSWER at every named label, at both widths, over registers whose bytes are all nonzero (INTSTAT/INTMASK seed
  0x0101010111010101, DOG 0x0123456789abcdef, TIME seeded odd); REV/CONTROL/TIME bytes the model holds at 0 disclosed.
* A refused store that lands, keyed on any single address bit: every bit 0-9 both ways among read-back refused stores.

**So this pass is asked to VERIFY THE DERIVATION**: walk the function's branches and the test's sessions and say
whether each class's enumeration is now exactly the function's cases.  The chain closes on the first valid pass that
finds zero floor breaches.

## SETTLED (recorded; re-stated because the questions depend on it)

* **The fix** (unchanged since pass 2; every seat of six passes found it correct): a refused width is announced once per
  device instance (`int warned`, bit `CRIME_W_LEN`) and `goto crime_declined;` past the register switch to the common
  tail, which answers a read 0 and returns 1.
* **History**: 40 -> 71 -> 85 -> 111 -> 121 -> 127 -> 131 rows (repairs 8, 9); SEVEN mutation-test tables, each with a
  written PRETABLE before it ran and a mechanical prediction checker.
* **A refused read's answer** is the low `len` bytes of the `odata` the decline hands the tail (memory_writemax64).
* **DISCLOSED coverage debt** (the probe header lists it): interior accept slots, an effect keyed on ONE unnamed offset
  (SOFTINT included), a store landing only at CRIME_TIME, joint multi-axis predicates, a function-static latch, widths
  3/5/6/7, a re-arm or pre-set inside the HARD_RESET branch, and a byte selection REV/CONTROL/TIME hold at 0.

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
artifacts/crimewidthkill/ (killtable_20260913/ through killtable7_20260913/):
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
     and the latch PRE-SET before any refusal, DERIVED FROM THE FUNCTION'S OWN BRANCHES rather than from the members
     earlier passes found (the Opus third-closing seat's diagnosis, measured on twelve survivors): both sides of every
     `if' an accepted access can take and come back from -- len 8 (W, R); len 4 (W, R) x (relative_addr & 4); every
     case label; REV's pc-window test (in, out); CONTROL's writeflag test (R, W) x its DOG test (set, clear) x its
     leftover test (nonzero, zero); the default arm (R, W) -- all in latch x5's prologue, before its first refusal;
     also warm once (sd first) and time once (ld first).  HARD_RESET's true side: disclosed (it stops the CPUs).
  5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
     session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
     debug() would not (free said)
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
     store had bit 4 set, so a landing keyed on bit 4 clear passed)                                     lo keeps
     and at the far block, a refused sb +0x27f and sh +0x27c leave +0x278 reading 0 (Opus, F2 and closing: a store
     landing only >= 0x200, of either width)                                                            hi keeps
     and in the middle of the window (+0x1ff / +0x1fc, every address bit 0-8 set)                       mid keeps
     and at INTMASK, read back by an accepted ld (kimi CLI, second closing pass: a landing that ORs into INTMASK kept
     bit 28, so imask ctl could not see it)                                                             imask keeps
  8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
     `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
     warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
     4-byte arm's re-arm open on the closing pass -- now DERIVED FROM THE FUNCTION'S OWN BRANCHES, the same set as the
     pre-set list in item 4 (codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing
     seat, measured: a re-arm on CONTROL's read side, its DOG-clear side and its zero-leftover side, each 121/121 on the 121-row test) --
     each accepted kind between two refusals                                                rearm once, rearm surv
     and in the middle block (an accepted sd between two refusals there)                                mid once
  9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
     (codex, closing pass: `if (relative_addr == CRIME_REV) odata = 1;' passed the 85-row version -- the REV rows
     checked only the pc)          lb/lh rev v0, ctl v0, istat/imask lb/lh v0, dog v0, dog lh v0, time lb/lh v0
     every one at 2 bytes (lh sees every value lb sees) and over a register whose LOW BYTES ARE NONZERO, so a decline
     that answers the register shows (kimi CLI, second closing pass: INTSTAT, INTMASK and DOG held 0 in their low
     bytes and `odata = d->reg[relative_addr / 8]' there passed; codex: `odata = 0x100' at DOG passed the lb-only row)
     -- REV 0x11, CONTROL 0x100, TIME 66-990 (low bytes); INTSTAT/INTMASK 0x0101010111010101 and DOG
     0x0123456789abcdef, nonzero in EVERY byte, so ANY selection of the register's bytes shows (Opus, second closing
     pass: the ADDRESSED lanes passed the 0x10000001 seed 121/121 on the 121-row test; glm, third closing pass: the 4-byte path's half,
     `reg >> 32', passed the 0x0101000010000001 one).  CONTROL is answered at both widths (ctl lb v0, ctl v0; the Opus
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
    bit 0; kimi-k3:cloud, second closing pass, found bits 7 and 8 carried by no refusal at all).  A landing at
    CRIME_SOFTINT (0x20, not a switch label) is in this class (deepseek, third closing pass).  ONE NAMED CELL IS
    OPEN AND SAID SO (kimi-k3:cloud, closing pass): a refused sb/sh that LANDS only at CRIME_TIME stores <= 0xffff,
    which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
    (the tail recomputes it), CONTROL and REV (the prelude rewrites them) such a landing is EQUIVALENT.
  * an accepted WRITE (4 or 8 bytes) at +0x00 or +0x08 shrunk away: the prelude rewrites CRIME_REV and CRIME_CONTROL on
    every access, so no round trip there can observe whether the store was accepted (the CONTROL arm's effects are
    rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
    needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
  * a decline answering a selection of the register's bytes at CRIME_REV, CRIME_CONTROL or CRIME_TIME that the model
    holds at 0 there -- the ADDRESSED lanes (bytes 0-1 at a label), or the 4-byte half above the low word -- is
    EQUIVALENT (the prelude rewrites REV = 0x11 and CONTROL = 0x100 on every access; TIME is kept to 32 bits).  At
    INTSTAT, INTMASK and DOG every byte is seeded nonzero, so any selection shows (Opus, second closing pass; glm, third).
  * a latch keyed on a JOINT predicate (e.g. only 2-byte refusals at CRIME_TIME), or on one unnamed offset other than the
    default-arm cells the latch rows refuse at: clause (e), the single-axis generating set being the floor.
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

## THE REPAIR DIFF -- the 121-row test -> the 131-row test (`git diff --no-index`, verbatim; 23 hunks)

```diff
diff --git "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable6_20260913\\crime_width_probe.table6.py" "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
index 7e1a0f9..9439d38 100644
--- "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable6_20260913\\crime_width_probe.table6.py"
+++ "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
@@ -16,5 +16,5 @@ Every access here is a real MIPS guest instruction through real address decode a
 
 CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
-artifacts/crimewidthkill/ (killtable_20260913/ through killtable6_20260913/):
+artifacts/crimewidthkill/ (killtable_20260913/ through killtable7_20260913/):
   1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                        <op> surv (six widths), hi surv, latch surv, sb08 run
@@ -38,5 +38,6 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable6_20260913/):
         CRIME_TIME (+0x38), all four cells: the arm advances TIME, which the NEXT read shows   time lb, sb, lh, sh
         the default arm (any unlabelled offset): a debug() line, printed while stepping      lb/lh/sb/sh nodflt,
-                                          at +0x07, +0x06, +0x1f, +0x1e and +0x27f           hi nodflt
+                                          at +0x07, +0x06, +0x1f, +0x1e, +0x27f  hi nodflt, and
+                                          +0x1ff, +0x1fe, +0x1fc                 mid nodflt
      Each channel carries a LIVE control on an accepted width that shows it can vary:
         rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text),
@@ -61,9 +62,19 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable6_20260913/):
      and every label-first session refuses again at ANOTHER label (codex, second closing pass: a latch whose bit is
      keyed on one label, `CRIME_W_LEN << (relative_addr == CRIME_INTMASK)', passed the 111-row version: the imask,
-     istat and sh08b sessions refused only at their own label)
-     and the latch PRE-SET before any refusal, in EVERY switch arm an accepted access reaches first in some counted
-     session: by an accepted 4-byte access, by a second latch on the CONTROL text reusing bit 0 (Opus closing seat:
-     `pre4', `ctl_collide'), and in the REV arm (glm, second closing pass) -- latch x5's prologue; by an 8-byte one,
-     warm once (sd first) and time once (ld first); in the INTMASK arm, the IRQ sessions' setup; DOG, the dog session
+     istat and sh08b sessions refused only at their own label; codex, third closing pass: the middle block likewise
+     for address bits 7 and 8 -- mid once now refuses at +0x07 as well)
+     and the FIRST refusal's own TEXT in every label-first session (codex, third closing pass: a notice SUPPRESSED at
+     one label, or at one address-bit value, and printed by the follow-up instead, still counted one; every said row
+     sat at an offset with bit 1 set -- rev said is at +0x00, every address bit clear)
+                                            rev said, sh08b said, imask said, istat said, time said, dog said
+     and the latch TEST that lets one label through (`|| relative_addr == L'): every label is refused again AFTER the
+     latch is set somewhere -- REV and TIME in latch x5's tail (the Opus third-closing seat, measured: they were each
+     refused once per session, first, so `|| == CRIME_REV' and `|| == CRIME_TIME' passed)
+     and the latch PRE-SET before any refusal, DERIVED FROM THE FUNCTION'S OWN BRANCHES rather than from the members
+     earlier passes found (the Opus third-closing seat's diagnosis, measured on twelve survivors): both sides of every
+     `if' an accepted access can take and come back from -- len 8 (W, R); len 4 (W, R) x (relative_addr & 4); every
+     case label; REV's pc-window test (in, out); CONTROL's writeflag test (R, W) x its DOG test (set, clear) x its
+     leftover test (nonzero, zero); the default arm (R, W) -- all in latch x5's prologue, before its first refusal;
+     also warm once (sd first) and time once (ld first).  HARD_RESET's true side: disclosed (it stops the CPUs).
   5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
      session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
@@ -85,4 +96,6 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable6_20260913/):
      filed `crimebankorder' disputes; a round that re-orders the banks owes this row's re-derivation. ***
   7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps;
+     and a seeded slot with address bit 4 CLEAR (+0x40; the Opus third-closing seat, measured: every read-back refused
+     store had bit 4 set, so a landing keyed on bit 4 clear passed)                                     lo keeps
      and at the far block, a refused sb +0x27f and sh +0x27c leave +0x278 reading 0 (Opus, F2 and closing: a store
      landing only >= 0x200, of either width)                                                            hi keeps
@@ -93,9 +106,8 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable6_20260913/):
      `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
      warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
-     4-byte arm's re-arm open on the closing pass: 8W, 8R, 4W and 4R in both lanes, and an accepted access into each
-     switch arm AND EACH BRANCH an accepted access can take and come back from -- CONTROL 0x0201 (the DOG_ENABLE and
-     unimplemented-control branches; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE passed), the REV
-     read from the PROM-probe window (the redirect branch), the default arm read and write -- each between two
-     refusals                                                                               rearm once, rearm surv
+     4-byte arm's re-arm open on the closing pass -- now DERIVED FROM THE FUNCTION'S OWN BRANCHES, the same set as the
+     pre-set list in item 4 (codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE; the Opus third-closing
+     seat, measured: a re-arm on CONTROL's read side, its DOG-clear side and its zero-leftover side, each 121/121 on the 121-row test) --
+     each accepted kind between two refusals                                                rearm once, rearm surv
      and in the middle block (an accepted sd between two refusals there)                                mid once
   9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
@@ -105,7 +117,12 @@ artifacts/crimewidthkill/ (killtable_20260913/ through killtable6_20260913/):
      that answers the register shows (kimi CLI, second closing pass: INTSTAT, INTMASK and DOG held 0 in their low
      bytes and `odata = d->reg[relative_addr / 8]' there passed; codex: `odata = 0x100' at DOG passed the lb-only row)
-     -- REV 0x11, CONTROL 0x100, TIME 66-990 (low bytes); INTSTAT/INTMASK 0x0101000010000001 and DOG 0x0123..ef,
-     nonzero in the TOP lanes a label's refused read names as well (Opus, second closing pass: a decline answering
-     the ADDRESSED lanes of the register passed the 0x10000001 seed 121/121)
+     -- REV 0x11, CONTROL 0x100, TIME 66-990 (low bytes); INTSTAT/INTMASK 0x0101010111010101 and DOG
+     0x0123456789abcdef, nonzero in EVERY byte, so ANY selection of the register's bytes shows (Opus, second closing
+     pass: the ADDRESSED lanes passed the 0x10000001 seed 121/121 on the 121-row test; glm, third closing pass: the 4-byte path's half,
+     `reg >> 32', passed the 0x0101000010000001 one).  CONTROL is answered at both widths (ctl lb v0, ctl v0; the Opus
+     third-closing seat, measured: `odata = 1' keyed on len 1 at CONTROL passed the lh-only row); its low byte is 0, so
+     only a CONSTANT answer can show at lb there.  TIME: at the time rows' refused reads TIME is a multiple of 66 and is
+     0 in 42 of 800 logged cells (the same seat -- this said "0.3% of runs, 66-990 includes 256, 512, 768", and those
+     are not multiples of 66), so the register cell is pinned by a SEEDED odd TIME instead     time sd lb v0, time sd lh v0
      and in the far block and the middle block over a NONZERO slot, at both widths (Opus closing: a refused read
      >= 0x200 answering the register; Opus, second closing pass: the 2-byte cell there)
@@ -125,7 +142,8 @@ DISCLOSED, not rowed:
       CRIME_CONTROL, reads   the arm acts only on MEM_WRITE
     Each measured as a survivor in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
-  * ACCEPT cells at offsets other than +0x00, +0x30, +0x210, +0x1f8 and +0x278: an accept arm narrowed by an address
-    strictly INSIDE
-    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.
+  * ACCEPT cells at unrowed slots: the rows touch accepted accesses at +0x00, +0x04, +0x08, +0x10, +0x18, +0x30,
+    +0x34, +0x38, +0x210, +0x214, +0x1f8 and +0x278 (not an exhaustive list of what the window accepts); an accept arm
+    narrowed by an address strictly INSIDE the window at an unrowed slot (e.g. `len == 8 && relative_addr != 0x100',
+    kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.
   * an effect ADDED to the decline arm and keyed on ONE UNNAMED offset (item 9 rows the READ answer at every named
     label) -- a refused store that lands only at
@@ -134,6 +152,7 @@ DISCLOSED, not rowed:
     offsets; the keeps rows catch a landing at CRIME_DOG, INTMASK, the far block and the middle block.  An effect
     keyed on a single ADDRESS BIT is NOT in this class: every bit 0-9 is carried both ways by a refused access of each
-    kind (the mid session sets bits 0-8, the far block bit 9; kimi-k3:cloud, second closing pass, found bits 7 and 8
-    carried by no refusal at all).  ONE NAMED CELL IS
+    kind that can carry it (the mid session sets bits 0-8, the far block bit 9; an aligned 2-byte access never sets
+    bit 0; kimi-k3:cloud, second closing pass, found bits 7 and 8 carried by no refusal at all).  A landing at
+    CRIME_SOFTINT (0x20, not a switch label) is in this class (deepseek, third closing pass).  ONE NAMED CELL IS
     OPEN AND SAID SO (kimi-k3:cloud, closing pass): a refused sb/sh that LANDS only at CRIME_TIME stores <= 0xffff,
     which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
@@ -143,8 +162,8 @@ DISCLOSED, not rowed:
     rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
     needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
-  * a decline answering the ADDRESSED LANES of the register at CRIME_REV, CRIME_CONTROL or CRIME_TIME is EQUIVALENT:
-    a refused read at a label reads its bytes 0-1, which the model holds at 0 there (the prelude rewrites REV = 0x11
-    and CONTROL = 0x100 on every access; TIME is kept to 32 bits).  At INTSTAT, INTMASK and DOG the seeds make those
-    lanes nonzero, so the same edit shows (Opus, second closing pass).
+  * a decline answering a selection of the register's bytes at CRIME_REV, CRIME_CONTROL or CRIME_TIME that the model
+    holds at 0 there -- the ADDRESSED lanes (bytes 0-1 at a label), or the 4-byte half above the low word -- is
+    EQUIVALENT (the prelude rewrites REV = 0x11 and CONTROL = 0x100 on every access; TIME is kept to 32 bits).  At
+    INTSTAT, INTMASK and DOG every byte is seeded nonzero, so any selection shows (Opus, second closing pass; glm, third).
   * a latch keyed on a JOINT predicate (e.g. only 2-byte refusals at CRIME_TIME), or on one unnamed offset other than the
     default-arm cells the latch rows refuse at: clause (e), the single-axis generating set being the floor.
@@ -447,4 +466,7 @@ row("sh08b msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "2W sh 0x02
 row("sh08b run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W sh 0x0900, 0x0a00 +0x08 (E/DOG+RESET): CPUs NOT stopped")
 row("sh08b once", count(t, "-- declined.", clean), 1, "4 refusals at CONTROL, then +0x07: one notice")
+#  the FIRST refusal's own text (codex, third closing pass: a notice suppressed at one label -- or at one address-bit
+#  value -- and printed instead by the +0x07 follow-up still counts one; every said row sat at an offset with bit 1 set)
+row("sh08b said", said(t, 2, 0x8, clean), 1, "sh +0x08 (first refusal): its own announce")
 
 for op in ("lb", "lh"):
@@ -458,4 +480,5 @@ for op in ("lb", "lh"):
     if op == "lb":
         row("rev once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_REV, then +0x07: one notice")
+        row("rev said", said(t, 1, 0x0, clean), 1, "lb +0x00 (first refusal, every address bit clear): its own announce")
 
 #  the CRIME_REV arm's PROM-probe hack does not test writeflag, so the WRITE cells at +0 are side-effect cells too
@@ -479,5 +502,8 @@ for op, val in (("sb", 0xa5), ("sh", 0xa5a5)):
 #  path uses -- reads bytes 0-1 at the label, which the 0x10000001 seed left 0.  So the seed is nonzero in byte 0, byte 1
 #  and the low byte; INTSTAT = SOFTINT | HARDINT and INTMASK both carry it; the reassert still sees bit 28.
-BIT = 0x0101000010000001
+#  And glm (third closing pass) found a THIRD byte selection -- the 4-byte path's half, `reg >> 32' -- whose low bytes
+#  that seed left 0.  So the seed is now nonzero in EVERY byte: no selection of the register's bytes can answer 0.  (DOG,
+#  the far slot and the middle slot are seeded every-byte-nonzero already.)
+BIT = 0x0101010111010101
 
 
@@ -521,4 +547,5 @@ for lbl, off in (("imask", 0x18), ("istat", 0x10)):
     row("%s ctl" % lbl, ip2(nth(t, "cause", 5)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)
     row("%s once" % lbl, count(t, "-- declined.", clean), 1, "4 refusals at +0x%x, then +0x07: one notice" % off)
+    row("%s said" % lbl, said(t, 1, off, clean), 1, "lb +0x%x (first refusal): its own announce" % off)
     row("%s lb v0" % lbl, pr(t, "a0"), "0x0", "refused lb +0x%x answers 0 (register 0x0101..01)" % off)
     row("%s lh v0" % lbl, pr(t, "a1"), "0x0", "refused lh +0x%x answers 0 (register 0x0101..01)" % off)
@@ -592,4 +619,5 @@ for op in ("lb", "sb", "lh", "sh"):
     if op == "lb":
         row("time once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_TIME, then +0x07: one notice")
+        row("time said", said(t, 1, 0x38, clean), 1, "lb +0x38 (first refusal): its own announce")
 
 # ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----
@@ -606,9 +634,16 @@ x, _ = ld(A, "ld", CRIME + 0x30, "a1"); c += x
 #  accepted access (`d->warned = 0;' in an accept arm), which `latch x5' -- no accepted access -- cannot.
 x, _ = ld(A, "lbu", CRIME + 0x07, "v0"); c += x
-t, clean = session(c + ["print a0", "print a1", "print v0"])
+#  a SEEDED slot with address bit 4 CLEAR (the Opus third-closing seat, measured: every refused store the rows read back
+#  had bit 4 set, so a landing keyed on bit 4 clear passed); +0x40 reaches the default arm
+x, _ = st(A, "sd", CRIME + 0x40, 0x0123456789abcdef); c += x
+x, _ = st(A, "sb", CRIME + 0x47, 0xff); c += x
+x, _ = st(A, "sh", CRIME + 0x44, 0xffff); c += x
+x, _ = ld(A, "ld", CRIME + 0x40, "s2"); c += x
+t, clean = session(c + ["print a0", "print a1", "print v0", "print s2"])
 row("sb keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x37 leaves CRIME_DOG as seeded")
 row("sh keeps", pr(t, "a1"), "0x123456789abcdef", "refused sh +0x30 leaves CRIME_DOG as seeded")
 row("warm v0", pr(t, "v0"), "0x0", "refused lbu AFTER accepted reads of 0x0123..: still 0")
 row("warm once", count(t, "-- declined.", clean), 1, "refused, accepted, refused: still one announce")
+row("lo keeps", pr(t, "s2"), "0x123456789abcdef", "refused sb +0x47, sh +0x44 (bit 4 clear) leave +0x40 seeded")
 
 #  RE-ARM, closed over every place an accepted access can go (codex, closing pass: `d->warned = 0;' in the 4-byte arm
@@ -626,12 +661,19 @@ A = Addr(CODE)
 c = ["ra=0x%x" % RA]
 x, _ = ld(A, "lb", CRIME + 0x07, "v0"); c += x
-KINDS = (("sd", 0x30), ("ld", 0x30), ("sw", 0x34), ("lw", 0x34), ("sw", 0x30), ("lw", 0x30),
-         ("ld", 0x38), ("lw", 0x18), ("lw", 0x10), ("lw", 0x00), ("lwP", 0x00), ("sw", 0x08), ("lw", 0x04),
-         ("sw", 0x04), ("sd", 0x278), ("ld", 0x278))
-for op, off in KINDS:
+#  The THIRD closing pass (the Opus seat, measured) found the list still built from the members earlier passes had
+#  found rather than from the function: a CONTROL READ, a CONTROL write with DOG clear, and one whose leftover bits are
+#  zero each re-armed at 121/121.  So the kinds are now DERIVED FROM DEVICE_ACCESS(crime)'s OWN BRANCHES -- both sides
+#  of every `if' an accepted access can take and come back from: len 8 (W, R), len 4 (W, R) x (relative_addr & 4),
+#  every case label, the REV pc-window test (in, out), CONTROL's writeflag test (R, W) x its DOG test (set, clear) x
+#  its leftover test (nonzero, zero), the default arm (R, W).  HARD_RESET's true side stops the CPUs: disclosed.
+KINDS = (("sd", 0x30, 0), ("ld", 0x30, 0), ("sw", 0x34, 0), ("lw", 0x34, 0), ("sw", 0x30, 0), ("lw", 0x30, 0),
+         ("ld", 0x38, 0), ("lw", 0x18, 0), ("lw", 0x10, 0), ("lw", 0x00, 0), ("lwP", 0x00, 0),
+         ("sw", 0x08, 0x0201), ("sw", 0x08, 0x0001), ("sw", 0x08, 0), ("lw", 0x08, 0),
+         ("lw", 0x04, 0), ("sw", 0x04, 0), ("sd", 0x278, 0), ("ld", 0x278, 0))
+for op, off, val in KINDS:
     if op == "lwP":                                 # from pc 0xbfc05180: the REV arm's redirect branch (pc = ra)
         x, _ = ld(A, "lw", CRIME + off, "a0", at=PROBE_PC)
     elif op[0] == "s":
-        x, _ = st(A, op, CRIME + off, 0x0201 if off == 0x08 else 0)
+        x, _ = st(A, op, CRIME + off, val)
     else:
         x, _ = ld(A, op, CRIME + off, "a0")
@@ -674,5 +716,8 @@ row("top4 w", pr(t, "s0"), "0x111122220a0b0c0d", "4W both halves at +0x278/+0x27
 
 # ---- a refused width at the window's LAST byte: declined, announced, default arm not reached ----
+#  The far slot is SEEDED first (codex, third closing pass: a refused store that CLEARS -- `&= idata' -- left the unseeded
+#  slot at 0, which `hi keeps' wanted).
 A = Addr(CODE)
+sf, _ = st(A, "sd", CRIME + 0x278, 0x0123456789abcdef)
 x, here = st(A, "sb", CRIME + 0x27f, 0xff)
 w, _ = st(A, "sh", CRIME + 0x27c, 0xffff)      # a refused 2-byte store in the far block too (Opus closing: wst_mc2)
@@ -680,9 +725,9 @@ y, _ = ld(A, "ld", CRIME + 0x278, "a0")        # the refused stores' register, r
 z, _ = st(A, "sb", CRIME + 0x27e, 0xee)        # follow-up refusals: one in the high block (a latch keyed on >= 0x40)
 z2, _ = ld(A, "lb", CRIME + 0x07, "v0")        #   and one low (a latch whose bit depends on the block, `lt_blk')
-t, clean = session(x + AFTER + roundtrip(A) + w + y + ["print a0"] + z + z2)
+t, clean = session(sf + x + AFTER + roundtrip(A) + w + y + ["print a0"] + z + z2)
 row("hi said", said(t, 1, 0x27f, clean), 1, "sb +0x27f: own announce, once")
 row("hi nodflt", dflt(t, clean, 0x27f, True), 0, "switch default arm NOT reached at 0x27f")
 row("hi surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
-row("hi keeps", pr(t, "a0"), "0x0", "refused sb +0x27f, sh +0x27c do not land (ld +0x278)")
+row("hi keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x27f, sh +0x27c leave the seeded slot (ld +0x278)")
 row("hi once", count(t, "-- declined.", clean), 1, "first refusal +0x27f, then 0x27c/0x27e/0x07: one notice")
 
@@ -703,4 +748,7 @@ x, _ = ld(A, "ld", CRIME + 0x1f8, "a0"); c += x
 x, _ = st(A, "sd", CRIME + 0x1f8, 0x0123456789abcdef); c += x
 x, _ = ld(A, "lb", CRIME + 0x1ff, "t1"); c += x
+#  and a follow-up refusal with bits 7 and 8 CLEAR (codex, third closing pass: a latch whose bit is keyed on address bit 7
+#  or 8 was invisible -- the middle block's refusals all set them, every other session's all clear them)
+x, _ = ld(A, "lb", CRIME + 0x07, "s3"); c += x
 t, clean = session(c + ["print v0", "print a1", "print a0"] + roundtrip(A))
 mid_dflt = (dflt(t, clean, 0x1ff, False) + dflt(t, clean, 0x1fe, False) + dflt(t, clean, 0x1ff, True) +
@@ -711,5 +759,5 @@ row("mid lb v0", pr(t, "v0"), "0x0", "refused lb +0x1ff over a seeded slot answe
 row("mid lh v0", pr(t, "a1"), "0x0", "refused lh +0x1fe over a seeded slot answers 0")
 row("mid keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x1ff, sh +0x1fc do not land (ld +0x1f8)")
-row("mid once", count(t, "-- declined.", clean), 1, "5 refusals with an accepted sd between: one notice")
+row("mid once", count(t, "-- declined.", clean), 1, "5 refusals, an accepted sd between, then +0x07: one notice")
 row("mid surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "the session completes (a RAM trip)")
 
@@ -723,9 +771,23 @@ y, _ = ld(A, "lb", CRIME + 0x07, "v1")
 z, _ = ld(A, "lh", CRIME + 0x08, "a0")        # a refused read at CRIME_CONTROL (codex, closing pass: answers at labels)
 w, _ = ld(A, "lh", CRIME + 0x30, "t1")
-t, clean = session(s + x + y + z + w + ["print v0", "print a0", "print t1"])
+#  CONTROL's 1-byte answer cell (the Opus third-closing seat, measured: `odata = 1' keyed on len 1 at CONTROL passed --
+#  the only refused read there was an lh), and TIME's answer over a SEEDED register: at the TIME rows' refused reads
+#  TIME is whatever the first tick added, a multiple of 66, and it is 0 in 42 of 800 logged cells (the same seat), so
+#  a decline answering the register there was invisible in those runs.  Seeded ODD by an accepted sd, TIME stays odd
+#  (every update adds a multiple of 66), so its low byte and low halfword are never 0.
+w2, _ = ld(A, "lb", CRIME + 0x08, "a1")
+ts, _ = st(A, "sd", CRIME + 0x38, 0x11111111)
+tb, _ = ld(A, "lb", CRIME + 0x38, "s0")
+th, _ = ld(A, "lh", CRIME + 0x38, "s1")
+t, clean = session(s + x + y + z + w + w2 + ts + tb + th + ["print v0", "print a0", "print t1", "print a1", "print s0",
+                                                              "print s1"])
 row("dog once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_DOG, then +0x07: one notice")
+row("dog said", said(t, 1, 0x30, clean), 1, "lb +0x30 (first refusal): its own announce")
 row("dog v0", pr(t, "v0"), "0x0", "refused lb at CRIME_DOG (seeded 0x0123..ef) answers 0")
 row("dog lh v0", pr(t, "t1"), "0x0", "refused lh at CRIME_DOG (seeded) answers 0")
 row("ctl v0", pr(t, "a0"), "0x0", "refused lh at CRIME_CONTROL (holds 0x100) answers 0")
+row("ctl lb v0", pr(t, "a1"), "0x0", "refused lb at CRIME_CONTROL answers 0")
+row("time sd lb v0", pr(t, "s0"), "0x0", "refused lb at CRIME_TIME (seeded odd) answers 0")
+row("time sd lh v0", pr(t, "s1"), "0x0", "refused lh at CRIME_TIME (seeded odd) answers 0")
 
 # ---- FREE-RUNNING: the announce is a fatal(), so it prints when the guest is NOT single-stepped (a debug() would not) ----
@@ -745,16 +807,27 @@ row("free v0", pr(t, "v0"), "0x0", "free-running lb +7: declined read answers 0"
 # ---- the latch: five refused accesses, one session, exactly one announce ----
 A = Addr(CODE)
-c = []
+c = ["ra=0x%x" % RA]
 #  PROLOGUE (the Opus closing seat): accepted accesses BEFORE the first refusal -- a notice PRE-SILENCED by an accepted
 #  access (`d->warned |= CRIME_W_LEN;' in an accept arm, `pre4') shows as zero notices; and an accepted CONTROL write
 #  whose unmodelled bit prints the CONTROL text, so a future second latch on THAT message reusing bit 0 (`ctl_collide')
-#  shows the same way.  8-byte pre-sets show in warm once (sd first) and time once (ld first).
-for op, off, val in (("sw", 0x08, 0x01), ("sw", 0x34, 0x0badcafe)):
+#  shows the same way.  CLOSED OVER EVERY ARM AND EVERY BRANCH an accepted access can take and come back from (glm,
+#  second closing pass: the REV arm; codex, grok, kimi, third closing pass: CONTROL's DOG_ENABLE branch -- the 0x01 write
+#  here skipped it -- the REV redirect branch, and the INTSTAT case alone -- each reached only AFTER some session's
+#  first refusal, where a pre-set is invisible):
+#      CONTROL  sw 0x0201 (DOG set, leftover nonzero), sw 0x0001 (DOG clear, leftover nonzero), sw 0 (DOG clear,
+#               leftover zero), lw (CONTROL's read side) -- the Opus third-closing seat, measured: a pre-set on the
+#               read side, and (by reading) on the zero-leftover side, passed; HARD_RESET is disclosed (it stops the CPUs)
+#      REV      lw from the PROM-probe window (the redirect branch) AND from ordinary code (the branch not taken)
+#      INTSTAT, INTMASK   lw +0x10, lw +0x18        DOG  ld +0x30        TIME  ld +0x38
+#      default  sw/lw +0x34 (4-byte, low lane), sd +0x278 (8-byte, far block)
+for op, off, val in (("sw", 0x08, 0x0201), ("sw", 0x08, 0x0001), ("sw", 0x08, 0), ("sw", 0x34, 0x0badcafe)):
     x, _ = st(A, op, CRIME + off, val); c += x
 x, _ = ld(A, "lw", CRIME + 0x34, "a0"); c += x
-#  and an accepted read of CRIME_REV (glm, second closing pass: no counted session reached the REV arm before its first
-#  refusal, so a pre-set there passed).  The other arms are reached first elsewhere: CONTROL here, INTMASK in the IRQ
-#  sessions' setup, DOG in warm once and the dog session, TIME in time once, the default arm here and in the top session.
+x, _ = ld(A, "lw", CRIME + 0x08, "a0"); c += x
+x, _ = ld(A, "lw", CRIME + 0x00, "a1", at=PROBE_PC); c += x
 x, _ = ld(A, "lw", CRIME + 0x00, "a1"); c += x
+for op, off in (("lw", 0x10), ("lw", 0x18), ("ld", 0x30), ("ld", 0x38)):
+    x, _ = ld(A, op, CRIME + off, "a2"); c += x
+x, _ = st(A, "sd", CRIME + 0x278, 0); c += x
 #  lh FIRST (Opus seat, F2): a latch whose bit is taken from the access -- `d->warned |= len' or `|= relative_addr' --
 #  sets bit 0 only for a 1-byte access or an odd address, so the lh at +0x06 would leave it clear and the lb after it
@@ -764,6 +837,11 @@ for op, off in (("lh", 6), ("lb", 7), ("lbu", 0x3f)):
 for op, off, val in (("sb", 0x37, 0xab), ("sh", 0x36, 0xabcd)):
     x, _ = st(A, op, CRIME + off, val); c += x
+#  and refusals at CRIME_REV and CRIME_TIME AFTER the latch is set (the Opus third-closing seat, measured: a latch TEST
+#  that lets one label through -- `|| relative_addr == CRIME_REV' -- passed, because REV and TIME were each refused only
+#  once per session, first; every other label is refused again after the latch is set somewhere)
+for off in (0x00, 0x38):
+    x, _ = ld(A, "lb", CRIME + off, "v0"); c += x
 t, clean = session(c + roundtrip(A))
-row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses -> one (once)")
+row("latch x5", count(t, "-- declined.", clean), 1, "5 refused accesses, then +0x00, +0x38 -> one (once)")
 row("latch surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives all five")
 
```

## THE MUTANTS OF TABLE 7, verbatim (this pass's panel findings, then the Opus seat's twelve)

```python
M = {
    "base": [],
    "rearm_ctlrd": [(CTLCASE, CTLCASE + "\t\tif (writeflag == MEM_READ) d->warned = 0;\n")],
    "rearm_dogclr": [(DOGIF, DOGIF[:-1] + " else\n\t\t\t\td->warned = 0;\n")],
    "rearm_ctl0": [(TXT, TXT + "\t\t\telse\n\t\t\t\td->warned = 0;\n")],
    "pre_istat": [(ISTAT, ISTAT + "\t\td->warned |= CRIME_W_LEN;\n")],
    "pre_revbr": [(REVBR, REVBR + "\t\t\td->warned |= CRIME_W_LEN;\n")],
    "pre_dogbr": [(DOGIF, DOGIF.replace("\t\t\t}\n", "\t\t\t\td->warned |= CRIME_W_LEN;\n\t\t\t}\n"))],
    "byp_rev": [(LTEST, "\t\tif (!(d->warned & CRIME_W_LEN) || relative_addr == CRIME_REV) {\n")],
    "byp_time": [(LTEST, "\t\tif (!(d->warned & CRIME_W_LEN) || relative_addr == CRIME_TIME) {\n")],
    "ans_hi32_b5": g("if (!(relative_addr & 0x20)) odata = d->reg[relative_addr / 8] >> 32;"),
    "land_b4clr": g("if (writeflag == MEM_WRITE && !(relative_addr & 0x10)) d->reg[relative_addr / 8] = idata;"),
    "ans_ctl_lb": g("if (len == 1 && relative_addr == CRIME_CONTROL) odata = 1;"),
    "pre_ctlrd": [(CTLCASE, CTLCASE + "\t\tif (writeflag == MEM_READ) d->warned |= CRIME_W_LEN;\n")],
}

```

## MUTATION-TEST TABLE 7 -- results (`POSTTABLE.out`)

```
POSTTABLE -- #529 kill table 7 (TARGETED, repairs 8 + 9), written AFTER the table (PRETABLE.out 22:07 predates both
launches and every log)

TWO LAUNCHES, and the first one is part of the record.
  * kill529g.run-220726.sh -- ABORTED.  Mutant c3_pre_ctl0 was mis-built: its `else' was inserted after the FIRST line of
    CONTROL's multi-line `fatal(...)' call, so the source did not compile -> BUILD_FAIL, and that driver EXITED LEAVING
    THE CLONE MUTANT.  Restored by hand (cmp clean, binary fresh, == base, sentinel removed) before anything else ran.
    Its output is preserved as table7.ABORTED-220726.out.  Two repairs followed: the mutant now anchors on the WHOLE
    statement (TXTEND = the call's last line), and the driver gained restore_and_exit on every apply/build failure.
  * kill529g.run-221006.sh -- the table of record -> table7.out (ends KILL529G_DONE).  It was launched with REUSE=1
    (reuse a binary whose mutant diff is byte-identical to an earlier launch's); that option was INEFFECTIVE except for
    `base', because a unified diff's header carries the files' mtimes -- every other mutant was rebuilt.  Disclosed so
    nobody reads REUSE as having skipped a build: 70 mutants BUILD_OK + `restored', `REUSED base (diff identical)'.

CLONE /tmp/gxopuscrime: BASELINE_CMP CLEAN; restored -- cmp clean, binary -nt source, `restored == base
(byte-identical)', no .MUTANT (re-checked by hand after the run: CMP_CLEAN, FRESH, no sentinel).  No mutant binary
identical to base.
INSTRUMENT: crime_width_probe.table7.py is BYTE-IDENTICAL to the shipped regress/crime_width_probe.py (cmp).  Table 6's
121-row instrument (crime_width_probe.table6.frozen.py) for the T6INSTR legs.
LOGS: 78 logs/probe_*.raw, EVERY one ends CRIMEP_DONE (checked); `grep -c '^NEW'' = 71 (base + 70 mutants),
`grep -c '^T6INSTR'' = 7.  Four probe lanes; this table's builds and probes also ran beside #530's kill table 1 (two
lanes, 00:4x-01:0x) and the rung-3 seat's builds (-j2) -- the oracles are step-counted, and no leg left its prediction,
so no re-run alone was owed.

check_pred.out:  CHECKPRED exact=78 differs=0 of 78 measured (78 predicted)

  NEW, on the 131-row repair-9 instrument (71 legs):
    base 131/131.
    predicted EQUIVALENT, 131/131 as predicted: dogft, ctlrdft, l_ctl, l_time (a byte selection the model holds at 0).
    predicted SURVIVOR, disclosed, 131/131 as predicted: c3_soft_land (a landing at SOFTINT -- one unnamed offset, the
      contract's DISCLOSED class; deepseek's closing-pass-3 finding, graded there as inside the disclosure).
    DETECTED, every red-row set exactly PRETABLE 7's: the remaining 64 --
      * the 45 targeted re-runs (earlier kills whose every red row sat in a session repairs 8/9 changed): all still
        detected, sets unchanged;
      * closing pass 3's panel findings (codex, grok, kimi, glm): c3_lat_b7/b8, c3_quiet_b1/imask, c3_pre_dog/revbr/
        istat, c3_far_and, c3_half_istat/imask -- all now red;
      * the two pre-set cells the Opus seat named by reading: c3_pre_ctl0 (the zero-leftover side), c3_pre_dogclr
        (the DOG-clear side) -- both red;
      * the Opus seat's twelve measured survivors (r_*): every one red, on the row the branch-derived enumeration
        predicted -- r_rearm_ctlrd, r_rearm_dogclr, r_rearm_ctl0, r_pre_istat, r_pre_revbr, r_pre_dogbr, r_byp_rev,
        r_byp_time, r_ans_hi32_b5, r_land_b4clr, r_ans_ctl_lb, r_pre_ctlrd.

  T6INSTR, the panel's claimed undetected changes on table 6's 121-row instrument (7 legs): c3_lat_b7, c3_lat_b8,
    c3_quiet_b1, c3_quiet_imask, c3_far_and, c3_half_istat, c3_half_imask -- ALL SEVEN 121/121.  Every claim was REAL:
    each escaped the instrument closing pass 3 reviewed, and each is detected by repairs 8/9.

WHAT THIS TABLE DOES NOT RE-MEASURE, stated: every earlier kill with a red row in a session repairs 8/9 did not change
stands on its earlier table's measurement (the targeting rule, PRETABLE 7).  The Opus seat's twelve were measured by
that seat at 121/121 on repair 7's instrument (opus_close3_20260913/) and are not re-run on it here.
```

## QUESTIONS

1. **Verify the derivation.**  Walk `DEVICE_ACCESS(crime)`'s branches: is every branch side an accepted access can take
   and return from covered before the first refusal (pre-set) and between refusals (re-arm)?  Is each latch, answer and
   landing enumeration now exactly the function's cases?  Name any case the derivation omits, or any it claims that no
   row can see.
2. **Is there a floor gap in the 131-row test?**  The smallest source edit to `dev_sgi_ip32.c` that undoes part of the
   fix's behaviour and still scores 131/131, as an exact edit, with the row you expected to catch it and why it cannot.
3. **Which statement in this brief, in POSTTABLE 7, or in the probe header, is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
