# CLOSING PASS 3 -- `crimewidthkill` (#529): is the regression test complete now?  Liveness token `CRIME_CLOSE3_20260913`.

VERDICT LINE FIRST: `CLOSES` (no floor gap remains in the 121-row test) or `GAP: <exact source edit to dev_sgi_ip32.c>`,
then the token.

This is a routine software-testing review of an open-source hardware emulator (GXemul) and its regression test.
"Mutant" means a deliberately modified copy of the emulator's C source used to check that the test notices the change
(standard mutation testing).  Please check the premises, not only the reasoning, and say what you could not check.
Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` only.  File-reading seats: `src/devices/dev_sgi_ip32.c`
(`DEVICE_ACCESS(crime)`), `regress/crime_width_probe.py`, `regress/artifacts/crimewidthkill/`.

## WHY THIS PASS EXISTS, AND WHAT IT IS ASKED TO DO

The second closing pass found gaps in the 111-row test and a measuring seat found one more in the repair; the test was
repaired twice (repair 6: 121 rows; repair 7: the IRQ registers' seed).  Several of those findings were members of
CLASSES that earlier passes had also hit (answers at labels; the latch keyed on the access; re-arm / pre-set by an
accepted access; effects keyed on the address).  This project's rule for that: when two consecutive passes find breaches
of one class, the repair must close the WHOLE CLASS and the contract must say which cells are covered -- and the next
pass VERIFIES THE ENUMERATION rather than hunting single cells.  So this pass is asked, first: is each class's
enumeration (in the probe header's CONTRACT and in POSTTABLE 5's DENOMINATOR) complete and true?  The chain closes on
the first valid pass that finds zero floor breaches; review effort is scoped to the repair diff below, the floor question
to the whole test.

## SETTLED (recorded; re-stated because the questions depend on it)

* **The fix** (unchanged since pass 2; every seat of five passes found it correct): `DEVICE_ACCESS(crime)` used to stop the
  emulator on any access of length other than 8 or 4.  It now prints one latched `(once)` notice per device instance
  (`int warned`, bit `CRIME_W_LEN`) and `goto crime_declined;` past the register switch to the common tail, which answers
  a read 0 and returns 1.
* **The test's history**: 40 rows -> 71 -> 85 -> 111 -> 121 (repairs 6 and 7), SIX mutation-test tables, each with a
  written PRETABLE before it ran; tables 4-6 are 57/57, 59/60 and 27/27 predicted red-row sets exact (the one miss is
  explained in POSTTABLE 5 and was re-run alone).
* **A refused read's answer** is the low `len` bytes of whatever `odata` the decline hands the tail (memory_writemax64),
  sign- or zero-extended by the instruction.  A register-answering mutant is visible only where the register's bytes
  that reach the guest are nonzero: the whole-register form hands over the LOW bytes; the lane form
  (`reg >> (8 * (8 - len - (relative_addr & 7)))`) hands over the bytes the ADDRESS names -- bytes 0-1 at a label.
* **DISCLOSED coverage debt** (the probe header lists it): interior accept slots, an effect keyed on ONE unnamed offset,
  a store landing only at CRIME_TIME (<= 0xffff), joint multi-axis predicates, a function-static latch, widths 3/5/6/7,
  a re-arm or pre-set inside the HARD_RESET branch (it stops the CPUs), and the lane-form answer at REV / CONTROL / TIME
  (the model holds those bytes at 0).  A finding there is not a gap unless you show the disclosure is wrong.

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
artifacts/crimewidthkill/ (killtable_20260913/ through killtable6_20260913/):
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
     istat and sh08b sessions refused only at their own label)
     and the latch PRE-SET before any refusal, in EVERY switch arm an accepted access reaches first in some counted
     session: by an accepted 4-byte access, by a second latch on the CONTROL text reusing bit 0 (Opus closing seat:
     `pre4', `ctl_collide'), and in the REV arm (glm, second closing pass) -- latch x5's prologue; by an 8-byte one,
     warm once (sd first) and time once (ld first); in the INTMASK arm, the IRQ sessions' setup; DOG, the dog session
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
     and at the far block, a refused sb +0x27f and sh +0x27c leave +0x278 reading 0 (Opus, F2 and closing: a store
     landing only >= 0x200, of either width)                                                            hi keeps
     and in the middle of the window (+0x1ff / +0x1fc, every address bit 0-8 set)                       mid keeps
     and at INTMASK, read back by an accepted ld (kimi CLI, second closing pass: a landing that ORs into INTMASK kept
     bit 28, so imask ctl could not see it)                                                             imask keeps
  8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
     `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
     warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
     4-byte arm's re-arm open on the closing pass: 8W, 8R, 4W and 4R in both lanes, and an accepted access into each
     switch arm AND EACH BRANCH an accepted access can take and come back from -- CONTROL 0x0201 (the DOG_ENABLE and
     unimplemented-control branches; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE passed), the REV
     read from the PROM-probe window (the redirect branch), the default arm read and write -- each between two
     refusals                                                                               rearm once, rearm surv
     and in the middle block (an accepted sd between two refusals there)                                mid once
  9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
     (codex, closing pass: `if (relative_addr == CRIME_REV) odata = 1;' passed the 85-row version -- the REV rows
     checked only the pc)          lb/lh rev v0, ctl v0, istat/imask lb/lh v0, dog v0, dog lh v0, time lb/lh v0
     every one at 2 bytes (lh sees every value lb sees) and over a register whose LOW BYTES ARE NONZERO, so a decline
     that answers the register shows (kimi CLI, second closing pass: INTSTAT, INTMASK and DOG held 0 in their low
     bytes and `odata = d->reg[relative_addr / 8]' there passed; codex: `odata = 0x100' at DOG passed the lb-only row)
     -- REV 0x11, CONTROL 0x100, TIME 66-990 (low bytes); INTSTAT/INTMASK 0x0101000010000001 and DOG 0x0123..ef,
     nonzero in the TOP lanes a label's refused read names as well (Opus, second closing pass: a decline answering
     the ADDRESSED lanes of the register passed the 0x10000001 seed 121/121)
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
  * ACCEPT cells at offsets other than +0x00, +0x30, +0x210, +0x1f8 and +0x278: an accept arm narrowed by an address
    strictly INSIDE
    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.
  * an effect ADDED to the decline arm and keyed on ONE UNNAMED offset (item 9 rows the READ answer at every named
    label) -- a refused store that lands only at
    +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only at
    +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at eight default-arm
    offsets; the keeps rows catch a landing at CRIME_DOG, INTMASK, the far block and the middle block.  An effect
    keyed on a single ADDRESS BIT is NOT in this class: every bit 0-9 is carried both ways by a refused access of each
    kind (the mid session sets bits 0-8, the far block bit 9; kimi-k3:cloud, second closing pass, found bits 7 and 8
    carried by no refusal at all).  ONE NAMED CELL IS
    OPEN AND SAID SO (kimi-k3:cloud, closing pass): a refused sb/sh that LANDS only at CRIME_TIME stores <= 0xffff,
    which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
    (the tail recomputes it), CONTROL and REV (the prelude rewrites them) such a landing is EQUIVALENT.
  * an accepted WRITE (4 or 8 bytes) at +0x00 or +0x08 shrunk away: the prelude rewrites CRIME_REV and CRIME_CONTROL on
    every access, so no round trip there can observe whether the store was accepted (the CONTROL arm's effects are
    rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
    needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
  * a decline answering the ADDRESSED LANES of the register at CRIME_REV, CRIME_CONTROL or CRIME_TIME is EQUIVALENT:
    a refused read at a label reads its bytes 0-1, which the model holds at 0 there (the prelude rewrites REV = 0x11
    and CONTROL = 0x100 on every access; TIME is kept to 32 bits).  At INTSTAT, INTMASK and DOG the seeds make those
    lanes nonzero, so the same edit shows (Opus, second closing pass).
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

## THE REPAIR DIFF -- the 111-row test -> the 121-row repair-7 test (`git diff --no-index`, verbatim; 18 hunks)

```diff
diff --git "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable4_20260913\\crime_width_probe.table4.py" "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
index 4ebeef9..7e1a0f9 100644
--- "a/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\artifacts\\crimewidthkill\\killtable4_20260913\\crime_width_probe.table4.py"
+++ "b/C:\\DocumentNoSnc\\CC\\GXEMUL\\GXEMUL-SEC\\regress\\crime_width_probe.py"
@@ -9,5 +9,5 @@ src/devices/dev_sgi_ip32.c, DEVICE_ACCESS(crime): an access whose length is neit
 
 so one guest lb/lbu/lh/lhu/sb/sh anywhere in CRIME (physical 0x14000000, KSEG1 0xb4000000) ended the emulator
-(witnessed 6/6 at rung 3: regress/artifacts/crimewidthkill/crime_width_witness_20260913.py).  #529 DECLINES the width
+(witnessed for all six widths at rung 3: regress/artifacts/crimewidthkill/crime_width_witness_20260913.py).  #529 DECLINES the width
 with one latched `(once)' announce and a `goto' to the function's common tail, skipping the register switch -- the
 #498 sgi_de shape.  A read is answered 0 by the tail, a write is dropped, the PC advances, no exception is raised.
@@ -16,5 +16,5 @@ Every access here is a real MIPS guest instruction through real address decode a
 
 CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
-artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3_20260913/):
+artifacts/crimewidthkill/ (killtable_20260913/ through killtable6_20260913/):
   1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                        <op> surv (six widths), hi surv, latch surv, sb08 run
@@ -28,6 +28,7 @@ artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3
                                           0x0900, 0x0a00 with sh08 0x0800       sh08b msg, sh08b run
                                           plus ALL-ONES refused writes, sb 0xff and sh 0xffff (kimi CLI,
-                                          closing pass), so a fall-through keyed on ANY data bit shows
-                                                                                sb08 msg, sh08b msg/run
+                                          closing pass), so a fall-through keyed on any bit a 1- or 2-byte
+                                          store can carry shows (bits above 15 never reach a refused access,
+                                          so a conjunct on them is equivalent)  sb08 msg, sh08b msg/run
         and the refused stores at INTSTAT, INTMASK and TIME carry all-ones (0xff / 0xffff) for the same reason
         CRIME_REV (+0x00), reads AND writes, from pc 0xbfc05180: the PROM-probe hack sets pc = ra (it does not test
@@ -54,11 +55,15 @@ artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3
      `relative_addr >= 0x40', on address parity).  A keyed latch shows only when the first refusal in a session falls
      where it does not set, so every axis value is a FIRST refusal followed by another, with an announce count:
-        width 1 / 2 and direction R / W    warm once (sb, write, odd), latch x5 (lh, read, even)
+        width 1 or 2 and direction R or W  warm once (sb, write, odd), latch x5 (lh, read, even)
         each label first                   rev once, sh08b once (CONTROL), istat once, imask once, dog once,
-                                           time once, latch x5 (default-arm, low), hi once (the high block,
-                                           followed by refusals both >= 0x40 and < 0x200)
-     and the latch PRE-SET before any refusal -- by an accepted 4-byte access, or by a second latch on the CONTROL
-     text reusing bit 0 (Opus closing seat: `pre4', `ctl_collide') -- latch x5's prologue; by an 8-byte one, warm
-     once (sd first) and time once (ld first)
+                                           time once, latch x5 (default-arm, low), hi once (the far block,
+                                           followed by refusals there and one below 0x40), mid once
+     and every label-first session refuses again at ANOTHER label (codex, second closing pass: a latch whose bit is
+     keyed on one label, `CRIME_W_LEN << (relative_addr == CRIME_INTMASK)', passed the 111-row version: the imask,
+     istat and sh08b sessions refused only at their own label)
+     and the latch PRE-SET before any refusal, in EVERY switch arm an accepted access reaches first in some counted
+     session: by an accepted 4-byte access, by a second latch on the CONTROL text reusing bit 0 (Opus closing seat:
+     `pre4', `ctl_collide'), and in the REV arm (glm, second closing pass) -- latch x5's prologue; by an 8-byte one,
+     warm once (sd first) and time once (ld first); in the INTMASK arm, the IRQ sessions' setup; DOG, the dog session
   5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
      session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
@@ -67,5 +72,7 @@ artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3
      at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
      prelude writes; grok, closing pass: `len == 8 && relative_addr != 0' passed the 85-row version, whose rows sat at
-     +0x30 -- an interior slot, not an end), with devsig / devsig hi the 4R cells there; CRIME_DOG +0x30 -- acc8 st+ld
+     +0x30 -- an interior slot, not an end), with devsig the 4R-low cell there and `rev pc ctl' the 4R-high one (its
+     redirect needs the access ACCEPTED; `devsig hi' reads 0 either way -- grok, codex, second closing pass, correcting
+     this sentence, which credited devsig hi); CRIME_DOG +0x30 -- acc8 st+ld
      (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi; the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w.  Those rows are ROUND TRIPS and cannot see an
      accept arm that re-maps its register index (kimi-k3:cloud, F2: `d->reg[(relative_addr & 0x3f) / 8]' passed the
@@ -79,16 +86,29 @@ artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3
   7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps;
      and at the far block, a refused sb +0x27f and sh +0x27c leave +0x278 reading 0 (Opus, F2 and closing: a store
-     landing only >= 0x200, of either width)
-                                                                                                        hi keeps
+     landing only >= 0x200, of either width)                                                            hi keeps
+     and in the middle of the window (+0x1ff / +0x1fc, every address bit 0-8 set)                       mid keeps
+     and at INTMASK, read back by an accepted ld (kimi CLI, second closing pass: a landing that ORs into INTMASK kept
+     bit 28, so imask ctl could not see it)                                                             imask keeps
   8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
      `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
      warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
      4-byte arm's re-arm open on the closing pass: 8W, 8R, 4W and 4R in both lanes, and an accepted access into each
-     switch arm, each between two refusals                                                  rearm once, rearm surv
+     switch arm AND EACH BRANCH an accepted access can take and come back from -- CONTROL 0x0201 (the DOG_ENABLE and
+     unimplemented-control branches; codex, second closing pass: `d->warned = 0;' inside DOG_ENABLE passed), the REV
+     read from the PROM-probe window (the redirect branch), the default arm read and write -- each between two
+     refusals                                                                               rearm once, rearm surv
+     and in the middle block (an accepted sd between two refusals there)                                mid once
   9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
      (codex, closing pass: `if (relative_addr == CRIME_REV) odata = 1;' passed the 85-row version -- the REV rows
-     checked only the pc)                lb/lh rev v0, ctl v0, istat/imask lb/lh v0, dog v0, time lb/lh v0
-     and in the far block over a NONZERO slot (Opus closing: a refused read >= 0x200 answering the register)
-                                                                                                    top rd v0
+     checked only the pc)          lb/lh rev v0, ctl v0, istat/imask lb/lh v0, dog v0, dog lh v0, time lb/lh v0
+     every one at 2 bytes (lh sees every value lb sees) and over a register whose LOW BYTES ARE NONZERO, so a decline
+     that answers the register shows (kimi CLI, second closing pass: INTSTAT, INTMASK and DOG held 0 in their low
+     bytes and `odata = d->reg[relative_addr / 8]' there passed; codex: `odata = 0x100' at DOG passed the lb-only row)
+     -- REV 0x11, CONTROL 0x100, TIME 66-990 (low bytes); INTSTAT/INTMASK 0x0101000010000001 and DOG 0x0123..ef,
+     nonzero in the TOP lanes a label's refused read names as well (Opus, second closing pass: a decline answering
+     the ADDRESSED lanes of the register passed the 0x10000001 seed 121/121)
+     and in the far block and the middle block over a NONZERO slot, at both widths (Opus closing: a refused read
+     >= 0x200 answering the register; Opus, second closing pass: the 2-byte cell there)
+                                                                   top rd v0, top rd2 v0, mid lb v0, mid lh v0
   10. the decline HOLDS WHILE AN INTERRUPT IS LATCHED: HARDINT set by the guest through MACE and the CRIME line
       asserted, a refused sh 0x0800 at CONTROL still does not stop the CPUs (the Opus closing seat: `if
@@ -100,16 +120,20 @@ DISCLOSED, not rowed:
     (#95, src/cpus/memory_rw.c -- `if (writeflag == MEM_READ)' then `memset(data, 0, len);', immediately above
     `paddr -= mem->devices[i].baseaddr;'), and on a declined access nothing between the entry and the tail writes
-    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 in kill table 1.
+    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 (the then 40-row test) in kill table 1.
   * a fall-through confined to the two label cells whose arms have NO body for that access, both EQUIVALENT:
       CRIME_DOG (0x30)       `No warning.' -- the arm is `break;'
       CRIME_CONTROL, reads   the arm acts only on MEM_WRITE
     Each measured as a survivor in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
-  * ACCEPT cells at offsets other than +0x30, +0x210 and +0x278: an accept arm narrowed by an address strictly INSIDE
-    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71) is not seen.
+  * ACCEPT cells at offsets other than +0x00, +0x30, +0x210, +0x1f8 and +0x278: an accept arm narrowed by an address
+    strictly INSIDE
+    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.
   * an effect ADDED to the decline arm and keyed on ONE UNNAMED offset (item 9 rows the READ answer at every named
     label) -- a refused store that lands only at
     +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only at
-    +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at five default-arm
-    offsets; the keeps rows catch a landing at CRIME_DOG and the far block, imask ctl one at INTMASK.  ONE NAMED CELL IS
+    +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at eight default-arm
+    offsets; the keeps rows catch a landing at CRIME_DOG, INTMASK, the far block and the middle block.  An effect
+    keyed on a single ADDRESS BIT is NOT in this class: every bit 0-9 is carried both ways by a refused access of each
+    kind (the mid session sets bits 0-8, the far block bit 9; kimi-k3:cloud, second closing pass, found bits 7 and 8
+    carried by no refusal at all).  ONE NAMED CELL IS
     OPEN AND SAID SO (kimi-k3:cloud, closing pass): a refused sb/sh that LANDS only at CRIME_TIME stores <= 0xffff,
     which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
@@ -119,7 +143,13 @@ DISCLOSED, not rowed:
     rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
     needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
+  * a decline answering the ADDRESSED LANES of the register at CRIME_REV, CRIME_CONTROL or CRIME_TIME is EQUIVALENT:
+    a refused read at a label reads its bytes 0-1, which the model holds at 0 there (the prelude rewrites REV = 0x11
+    and CONTROL = 0x100 on every access; TIME is kept to 32 bits).  At INTSTAT, INTMASK and DOG the seeds make those
+    lanes nonzero, so the same edit shows (Opus, second closing pass).
   * a latch keyed on a JOINT predicate (e.g. only 2-byte refusals at CRIME_TIME), or on one unnamed offset other than the
     default-arm cells the latch rows refuse at: clause (e), the single-axis generating set being the floor.
-  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 by the Opus seat
+  * a re-arm or pre-set inside the HARD_RESET branch of the CONTROL arm: an accepted write that takes it stops every
+    CPU, so nothing can follow it in the session.  Unrowable, not merely unrowed.
+  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 (the 71-row test) by the Opus seat
     (F2, `sft'); it is the single-unnamed-offset class of the bullet above.
   * a FUNCTION-STATIC latch in place of `d->warned' is NOT equivalent in general -- two IP32 machines in one gxemul
@@ -410,8 +440,11 @@ e, _ = st(A, "sh", CRIME + 0x08, 0x0900)       # glm, closing pass: ENDIANESS (0
 y, _ = st(A, "sh", CRIME + 0x08, 0x0a00)
 f, _ = st(A, "sh", CRIME + 0x08, 0xffff)        # all-ones: every bit a data-keyed narrowing could key on, set
-t, clean = session(x + e + y + f + AFTER + roundtrip(A))
+#  and a follow-up refusal at ANOTHER label (the codex seat, second closing pass: a latch whose bit is keyed on one label,
+#  `CRIME_W_LEN << (relative_addr == L)', is invisible to a session that refuses only at L)
+g, _ = ld(A, "lb", CRIME + 0x07, "t1")
+t, clean = session(x + e + y + f + AFTER + roundtrip(A) + g)
 row("sh08b msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "2W sh 0x0201 +0x08 (DOG set): no CONTROL text")
 row("sh08b run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W sh 0x0900, 0x0a00 +0x08 (E/DOG+RESET): CPUs NOT stopped")
-row("sh08b once", count(t, "-- declined.", clean), 1, "4 refusals at CONTROL, first at CONTROL: one notice")
+row("sh08b once", count(t, "-- declined.", clean), 1, "4 refusals at CONTROL, then +0x07: one notice")
 
 for op in ("lb", "lh"):
@@ -439,5 +472,12 @@ for op, val in (("sb", 0xa5), ("sh", 0xa5a5)):
 #  must leave it low; the accepted `lw' that follows is the CONTROL that the arm reasserts at once.  (Measured by the
 #  pass-2 Opus seat, opus_pass2_20260913/scripts/crime_p2_escape.py E1/E2: a fall-through at the label sets IP2.)
-BIT = 0x10000000
+#  BIT carries bit 0 as well (the kimi CLI seat, second closing pass): a refused read answers the low bytes of whatever
+#  the decline hands the tail, so with a register whose low bytes were 0 a decline that answered THE REGISTER
+#  (`odata = d->reg[relative_addr / 8]' at INTSTAT or INTMASK) read back 0 and passed.  AND in its TOP lanes (the Opus
+#  second-closing seat, measured 121/121 on the 0x10000001 seed): a decline that answers the bytes the ADDRESS names --
+#  `odata = d->reg[relative_addr / 8] >> (8 * (8 - len - (relative_addr & 7)))', the lane the model's own 4-byte read
+#  path uses -- reads bytes 0-1 at the label, which the 0x10000001 seed left 0.  So the seed is nonzero in byte 0, byte 1
+#  and the low byte; INTSTAT = SOFTINT | HARDINT and INTMASK both carry it; the reassert still sees bit 28.
+BIT = 0x0101000010000001
 
 
@@ -467,4 +507,10 @@ for lbl, off in (("imask", 0x18), ("istat", 0x10)):
     x, _ = ld(A, "lw", CRIME + off, "v0"); c += x
     c += ["print cause", "print a0", "print a1"]
+    #  INTMASK read back by an accepted ld after the refused stores (kimi CLI, second closing pass: a landing that ORs
+    #  into INTMASK keeps bit 28, so the reassert rows cannot see it), then a follow-up refusal at ANOTHER label (codex:
+    #  a latch keyed on this one label is invisible to a session that refuses only here)
+    x, _ = ld(A, "ld", CRIME + 0x18, "s2"); c += x
+    x, _ = ld(A, "lb", CRIME + 0x07, "t1"); c += x
+    c += ["print s2"]
     t, clean = session(c)
     row("%s pre" % lbl, ip2(nth(t, "cause", 0)), "clear", "IP2 low after SOFTINT's default-arm store")
@@ -474,14 +520,18 @@ for lbl, off in (("imask", 0x18), ("istat", 0x10)):
     row("%s sh" % lbl, ip2(nth(t, "cause", 4)), "clear", "refused sh +0x%x: no reassert" % off)
     row("%s ctl" % lbl, ip2(nth(t, "cause", 5)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)
-    row("%s once" % lbl, count(t, "-- declined.", clean), 1, "4 refusals, first at +0x%x: one notice" % off)
-    row("%s lb v0" % lbl, pr(t, "a0"), "0x0", "refused lb +0x%x answers 0" % off)
-    row("%s lh v0" % lbl, pr(t, "a1"), "0x0", "refused lh +0x%x answers 0" % off)
+    row("%s once" % lbl, count(t, "-- declined.", clean), 1, "4 refusals at +0x%x, then +0x07: one notice" % off)
+    row("%s lb v0" % lbl, pr(t, "a0"), "0x0", "refused lb +0x%x answers 0 (register 0x0101..01)" % off)
+    row("%s lh v0" % lbl, pr(t, "a1"), "0x0", "refused lh +0x%x answers 0 (register 0x0101..01)" % off)
+    if lbl == "imask":
+        row("imask keeps", pr(t, "s2"), "0x%x" % BIT, "refused sb/sh +0x18 leave INTMASK as stored (ld +0x18)")
 
 # ---- THE DECLINE HOLDS WHILE AN INTERRUPT IS LATCHED (the Opus closing seat: `if (!d->reg[CRIME_HARDINT / 8]) goto
 #  crime_declined;' passed the 85-row version -- every refusal in it ran with HARDINT == 0, and the tail the goto jumps
 #  to READS HARDINT, so the field is a DEPENDS-ON operand; `if (!d->prev_asserted)' passed too).  The guest latches a
-#  hardware interrupt by two MACE stores (ISA interrupt status, then mask -> crime_interrupt_assert -> HARDINT), asserts
-#  the CRIME line (INTMASK and SOFTINT, reasserted by an accepted lw), then a refused sh 0x0800 at CRIME_CONTROL: falling
-#  into the switch there would stop every CPU.  Both controls are rowed: HARDINT reads nonzero and IP2 is set.
+#  hardware interrupt by two MACE stores (ISA interrupt status, then mask -> crime_interrupt_assert -> HARDINT), and
+#  -- INDEPENDENTLY, not as a consequence (grok, second closing pass: HARDINT's bit is not in the mask used here) --
+#  asserts the CRIME line (INTMASK and SOFTINT = BIT, reasserted by an accepted lw), then a refused sh 0x0800 at
+#  CRIME_CONTROL: falling into the switch there would stop every CPU.  Both states are rowed as controls: HARDINT reads
+#  nonzero, and IP2 is set.
 MACE = 0xbf310000                                   # KSEG1 of the `mace addr=0x1f310000' device (dev_sgi_ip32.c)
 A = Addr(CODE)
@@ -510,6 +560,7 @@ row("gate run", pr(t, "v1"), "0x%x" % LIVE_VAL, "refused sh 0x800 +0x08 with an
 #  makes it the wall-clock interval of the intervening debugger commands, ~1e8.  The third `ld' is the CONTROL that the
 #  channel moves.  (Opus pass 2, E3; the tick-spacing wording corrected by the kimi CLI seat on the F2 pass.)
-#  ASSUMPTION, disclosed: no tick boundary falls between the first `ld' and the `ld' that samples s1 (codex, closing pass:
-#  the window runs THROUGH the sampling read, not only to the refused access).  The IRQ rows carry the same assumption:
+#  ASSUMPTION, disclosed: after that FIRST tick, no further tick falls between the first `ld' and the `ld' that samples
+#  s1 (codex, closing pass: the window runs THROUGH the sampling read, not only to the refused access; deepseek and
+#  codex, second closing pass: this sentence said "no tick boundary" while the one above names the first tick).  The IRQ rows carry the same assumption:
 #  dev_crime_tick also calls crime_interrupt_reassert(), so a tick inside a session could raise IP2 on the fixed build
 #  (kimi CLI, closing pass) -- a false red, never a false green; measured stable so far.
@@ -567,14 +618,27 @@ row("warm once", count(t, "-- declined.", clean), 1, "refused, accepted, refused
 #  A re-arm anywhere an accepted access reaches shows as a second notice.  (A re-arm in the common tail, which refusals
 #  also reach, shows in latch x5.)
+#  The second closing pass (codex) found the arm's BRANCHES were not all reached: an accepted CONTROL write carried only
+#  0, 1 or 0x800, so a re-arm inside the DOG_ENABLE branch passed.  So the CONTROL write here is 0x0201 (the DOG branch
+#  and the unimplemented-control branch), the REV read runs from the PROM-probe window (its pc-redirect branch), and the
+#  default arm takes a 4-byte write too.  The HARD_RESET branch cannot be followed by anything (it stops every CPU):
+#  a re-arm there is DISCLOSED.
 A = Addr(CODE)
-c = []
+c = ["ra=0x%x" % RA]
 x, _ = ld(A, "lb", CRIME + 0x07, "v0"); c += x
-for op, off in (("sd", 0x30), ("ld", 0x30), ("sw", 0x34), ("lw", 0x34), ("sw", 0x30), ("lw", 0x30),
-                ("ld", 0x38), ("lw", 0x18), ("lw", 0x10), ("lw", 0x00), ("sw", 0x08), ("lw", 0x04),
-                ("sd", 0x278), ("ld", 0x278)):
-    x, _ = (st(A, op, CRIME + off, 0) if op[0] == "s" else ld(A, op, CRIME + off, "a0")); c += x
+KINDS = (("sd", 0x30), ("ld", 0x30), ("sw", 0x34), ("lw", 0x34), ("sw", 0x30), ("lw", 0x30),
+         ("ld", 0x38), ("lw", 0x18), ("lw", 0x10), ("lw", 0x00), ("lwP", 0x00), ("sw", 0x08), ("lw", 0x04),
+         ("sw", 0x04), ("sd", 0x278), ("ld", 0x278))
+for op, off in KINDS:
+    if op == "lwP":                                 # from pc 0xbfc05180: the REV arm's redirect branch (pc = ra)
+        x, _ = ld(A, "lw", CRIME + off, "a0", at=PROBE_PC)
+    elif op[0] == "s":
+        x, _ = st(A, op, CRIME + off, 0x0201 if off == 0x08 else 0)
+    else:
+        x, _ = ld(A, op, CRIME + off, "a0")
+    c += x
     x, _ = ld(A, "lb", CRIME + 0x06, "v0"); c += x
 t, clean = session(c + roundtrip(A))
-row("rearm once", count(t, "-- declined.", clean), 1, "15 refusals, 14 accepted kinds between: one notice")
+row("rearm once", count(t, "-- declined.", clean), 1, "%d refusals, %d accepted kinds between: one notice"
+    % (len(KINDS) + 1, len(KINDS)))
 row("rearm surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "the whole interleave completes (a RAM trip)")
 
@@ -590,4 +654,5 @@ x, _ = ld(A, "lw", CRIME + 0x210, "t1"); c += x
 x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x
 x, _ = ld(A, "lb", CRIME + 0x27b, "v0"); c += x      # a REFUSED read while the far slot is nonzero (Opus: rd_hi)
+x, _ = ld(A, "lh", CRIME + 0x27a, "s3"); c += x      # and a refused 2-byte read there (Opus, second closing pass)
 x, _ = ld(A, "ld", CRIME + 0x278, "a0"); c += x
 x, _ = ld(A, "lw", CRIME + 0x278, "a1"); c += x
@@ -596,8 +661,10 @@ x, _ = st(A, "sw", CRIME + 0x27c, 0x0a0b0c0d); c += x
 x, _ = st(A, "sw", CRIME + 0x278, 0x11112222); c += x
 x, _ = ld(A, "ld", CRIME + 0x278, "s0"); c += x
-t, clean = session(c + ["print s2", "print a0", "print a1", "print a2", "print s0", "print s1", "print v0"])
+t, clean = session(c + ["print s2", "print a0", "print a1", "print a2", "print s0", "print s1", "print v0",
+                        "print s3"])
 row("top8 anchor", pr(t, "s2"), "0x1", "8R +0x210: bank-1 ctrl the PRELUDE wrote (-M 64)")
 row("top4 anchor", pr(t, "s1"), "0x1", "4R +0x214: the anchored slot's low half")
 row("top rd v0", pr(t, "v0"), "0x0", "refused lb +0x27b over a nonzero slot answers 0")
+row("top rd2 v0", pr(t, "s3"), "0x0", "refused lh +0x27a over a nonzero slot answers 0")
 row("top said", said(t, 1, 0x27b, clean), 1, "lb +0x27b is the first refusal: every access before it accepted")
 row("top8 st+ld", pr(t, "a0"), "0x102030405060708", "8W then 8R at +0x278")
@@ -620,13 +687,45 @@ row("hi keeps", pr(t, "a0"), "0x0", "refused sb +0x27f, sh +0x27c do not land (l
 row("hi once", count(t, "-- declined.", clean), 1, "first refusal +0x27f, then 0x27c/0x27e/0x07: one notice")
 
+# ---- THE MIDDLE OF THE WINDOW, where EVERY address bit 0-8 is set (kimi-k3:cloud, second closing pass: no refused access
+#  set bit 7 or bit 8, so a decline effect keyed on `relative_addr & 0x80' -- `odata = relative_addr & 0x80' -- passed).
+#  Together with the low cells (bits clear) and the far block (bit 9), every address bit is now carried both ways by a
+#  refused access of each kind: the ANSWER (1R, 2R), a LANDING (1W, 2W, read back by an accepted ld), the NOTICE (its
+#  text here, and one count across the session), the DEFAULT ARM not reached, and a RE-ARM by an accepted access in
+#  this block (the sd between the refusals).  +0x1f8 is inside DEV_CRIME_LENGTH (0x280) and reaches the default arm.
+A = Addr(CODE)
+c = []
+x, _ = st(A, "sd", CRIME + 0x1f8, 0x0123456789abcdef); c += x
+x, _ = ld(A, "lb", CRIME + 0x1ff, "v0"); c += x
+x, _ = ld(A, "lh", CRIME + 0x1fe, "a1"); c += x
+x, _ = st(A, "sb", CRIME + 0x1ff, 0xff); c += x
+x, _ = st(A, "sh", CRIME + 0x1fc, 0xffff); c += x
+x, _ = ld(A, "ld", CRIME + 0x1f8, "a0"); c += x
+x, _ = st(A, "sd", CRIME + 0x1f8, 0x0123456789abcdef); c += x
+x, _ = ld(A, "lb", CRIME + 0x1ff, "t1"); c += x
+t, clean = session(c + ["print v0", "print a1", "print a0"] + roundtrip(A))
+mid_dflt = (dflt(t, clean, 0x1ff, False) + dflt(t, clean, 0x1fe, False) + dflt(t, clean, 0x1ff, True) +
+            dflt(t, clean, 0x1fc, True)) if clean else "unclean"
+row("mid said", said(t, 1, 0x1ff, clean), 1, "lb +0x1ff (bits 0-8 set): own announce, once")
+row("mid nodflt", mid_dflt, 0, "switch default arm NOT reached at 0x1ff/0x1fe/0x1fc")
+row("mid lb v0", pr(t, "v0"), "0x0", "refused lb +0x1ff over a seeded slot answers 0")
+row("mid lh v0", pr(t, "a1"), "0x0", "refused lh +0x1fe over a seeded slot answers 0")
+row("mid keeps", pr(t, "a0"), "0x123456789abcdef", "refused sb +0x1ff, sh +0x1fc do not land (ld +0x1f8)")
+row("mid once", count(t, "-- declined.", clean), 1, "5 refusals with an accepted sd between: one notice")
+row("mid surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "the session completes (a RAM trip)")
+
 # ---- the latch, first refusal at CRIME_DOG (the one named label with no session whose FIRST refusal is there) ----
+#  CRIME_DOG is SEEDED first (kimi CLI, second closing pass: with DOG at 0 a decline answering the register read 0), and
+#  read refused at BOTH widths (codex: `odata = 0x100' at DOG left the lb's low byte 0 and passed).
 A = Addr(CODE)
+s, _ = st(A, "sd", CRIME + 0x30, 0x0123456789abcdef)
 x, _ = ld(A, "lb", CRIME + 0x30, "v0")
 y, _ = ld(A, "lb", CRIME + 0x07, "v1")
 z, _ = ld(A, "lh", CRIME + 0x08, "a0")        # a refused read at CRIME_CONTROL (codex, closing pass: answers at labels)
-t, clean = session(x + y + z + ["print v0", "print a0"])
+w, _ = ld(A, "lh", CRIME + 0x30, "t1")
+t, clean = session(s + x + y + z + w + ["print v0", "print a0", "print t1"])
 row("dog once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_DOG, then +0x07: one notice")
-row("dog v0", pr(t, "v0"), "0x0", "refused lb at CRIME_DOG answers 0")
-row("ctl v0", pr(t, "a0"), "0x0", "refused lh at CRIME_CONTROL answers 0")
+row("dog v0", pr(t, "v0"), "0x0", "refused lb at CRIME_DOG (seeded 0x0123..ef) answers 0")
+row("dog lh v0", pr(t, "t1"), "0x0", "refused lh at CRIME_DOG (seeded) answers 0")
+row("ctl v0", pr(t, "a0"), "0x0", "refused lh at CRIME_CONTROL (holds 0x100) answers 0")
 
 # ---- FREE-RUNNING: the announce is a fatal(), so it prints when the guest is NOT single-stepped (a debug() would not) ----
@@ -654,4 +753,8 @@ for op, off, val in (("sw", 0x08, 0x01), ("sw", 0x34, 0x0badcafe)):
     x, _ = st(A, op, CRIME + off, val); c += x
 x, _ = ld(A, "lw", CRIME + 0x34, "a0"); c += x
+#  and an accepted read of CRIME_REV (glm, second closing pass: no counted session reached the REV arm before its first
+#  refusal, so a pre-set there passed).  The other arms are reached first elsewhere: CONTROL here, INTMASK in the IRQ
+#  sessions' setup, DOG in warm once and the dog session, TIME in time once, the default arm here and in the top session.
+x, _ = ld(A, "lw", CRIME + 0x00, "a1"); c += x
 #  lh FIRST (Opus seat, F2): a latch whose bit is taken from the access -- `d->warned |= len' or `|= relative_addr' --
 #  sets bit 0 only for a 1-byte access or an odd address, so the lh at +0x06 would leave it clear and the lb after it
```

## THE MUTANTS OF TABLES 5 AND 6, verbatim (so each named mutant's EDIT is visible, not just its name)

Each entry is (find-text, replacement) on `dev_sgi_ip32.c`; `g(...)` puts its argument in place of the decline arm's
`goto crime_declined;`.

```python
M.update({
    # codex: the latch bit keyed on ONE label (the define is used by both the test and the set)
    "c2_lbl_imask": [(DEFINE, "#define\tCRIME_W_LEN\t\t(1 << (relative_addr == CRIME_INTMASK))")],
    "c2_lbl_istat": [(DEFINE, "#define\tCRIME_W_LEN\t\t(1 << (relative_addr == CRIME_INTSTAT))")],
    "c2_lbl_ctl":   [(DEFINE, "#define\tCRIME_W_LEN\t\t(1 << (relative_addr == CRIME_CONTROL))")],
    # codex: a halfword-only nonzero answer at DOG; kimi CLI: a decline answering THE REGISTER at a label
    "c2_dog100":    [(GOTO, g("if (relative_addr == CRIME_DOG) odata = 0x100; goto crime_declined;"))],
    "c2_reg_imask": [(GOTO, g("if (relative_addr == CRIME_INTMASK) odata = d->reg[relative_addr / 8]; goto crime_declined;"))],
    "c2_reg_istat": [(GOTO, g("if (relative_addr == CRIME_INTSTAT) odata = d->reg[relative_addr / 8]; goto crime_declined;"))],
    "c2_reg_dog":   [(GOTO, g("if (relative_addr == CRIME_DOG) odata = d->reg[relative_addr / 8]; goto crime_declined;"))],
    # kimi CLI: a landing that ORs into INTMASK
    "c2_land_or":   [(GOTO, g("if (writeflag == MEM_WRITE && relative_addr == CRIME_INTMASK) "
                              "d->reg[CRIME_INTMASK / 8] |= idata; goto crime_declined;"))],
    # codex: re-arm inside CONTROL's DOG_ENABLE branch; and the same inside the other branches an accepted access takes
    "c2_rearm_dog": [(DOGBR, DOGBR + "\t\t\t\td->warned = 0;\n")],
    "c2_rearm_txt": [(TXTBR, "\t\t\tif (idata != 0 && ((d->warned = 0) == 0))\n\t\t\t\tfatal(\"[ CRIME_CONTROL: unimplemented \"\n")],
    "c2_rearm_rev": [(REVIF, REVIF + "\t\t\td->warned = 0;\n")],
    # glm: a pre-set in a switch arm -- the INTMASK/INTSTAT arm (PREDICTED DETECTED) and the REV arm (the open member)
    "c2_pre_irq":   [(IRQARM, IRQARM.replace("\t\tcrime_interrupt_reassert(d);\n",
                                             "\t\td->warned |= CRIME_W_LEN;\n\t\tcrime_interrupt_reassert(d);\n"))],
    "c2_pre_rev":   [(REVIF, "\t\td->warned |= CRIME_W_LEN;\n" + REVIF)],
    # kimi-k3:cloud: decline effects keyed on an ADDRESS BIT no refusal carried (bit 7, bit 8)
    "c2_bit7_ans":  [(GOTO, g("odata = relative_addr & 0x80; goto crime_declined;"))],
    "c2_bit8_land": [(GOTO, g("if (writeflag == MEM_WRITE && (relative_addr & 0x100)) d->reg[relative_addr / 8] = idata; "
                              "goto crime_declined;"))],
    "c2_bit7_quiet": [(B.LATCH_TEST, "\t\tif (!(d->warned & CRIME_W_LEN) && !(relative_addr & 0x80)) {")],
    "c2_bit8_ft":   [(GOTO, g("if (!(relative_addr & 0x100)) goto crime_declined;"))],
    "c2_bit8_rearm": [(ARM8, ARM8.replace("\tif (len == 8) {\n", "\tif (len == 8) {\n\t\tif (relative_addr & 0x100) d->warned = 0;\n", 1))],
    "c2_bit8_latch": [(B.LATCH_SET, "\t\t\td->warned |= (relative_addr & 0x100) ? 0 : CRIME_W_LEN;\n")],
})

LANE = "odata = d->reg[relative_addr / 8] >> (8 * (8 - len - (relative_addr & 7))); goto crime_declined;"

M = dict(E.M)
_p = os.path.join(HERE, "mutants_close2_opus_b3.py")
_ns = {}
exec(io.open(_p, encoding="utf-8").read().split("name, path = sys.argv")[0], _ns)
M.update({"q_" + k: v for k, v in _ns["M"].items() if k != "base"})


def lane(label):
    return [(GOTO, g("if (writeflag == MEM_READ && relative_addr == %s) %s" % (label, LANE)))]


M.update({
    # the Opus seat's istat_lane, at the other labels: INTMASK and DOG are seeded and should show;
    # REV, CONTROL and TIME hold 0 in the lanes a label's refused read names -- PREDICTED EQUIVALENT, disclosed
    "l_imask": lane("CRIME_INTMASK"),
    "l_dog":   lane("CRIME_DOG"),
    "l_rev":   lane("CRIME_REV"),
    "l_ctl":   lane("CRIME_CONTROL"),
    "l_time":  lane("CRIME_TIME"),
})

```

## MUTATION-TEST TABLES 5 AND 6 -- results (`POSTTABLE.out` of each)

```
POSTTABLE -- #529 kill table 5 (TARGETED, repair 6), written AFTER the table (PRETABLE.out 17:26 predates the driver's
launch, 17:30, and every log)
Driver kill529e.run-173033.sh (frozen); summary table5.out; lane logs logs/lane{0,1,2}.out; per run logs/probe_<m>.raw (the
121-row repair-6 instrument, crime_width_probe.table5.py) and logs/probe_T4INSTR_<m>.raw (table 4's 111-row instrument)
-- 60 logs, EVERY one ends CRIMEP_DONE (checked), plus logs/probe_c2_bit8_rearm_ALONE.raw (below); logs/<m>.diff;
builds/.  Scratch clone /tmp/gxopuscrime, baseline = the #529 working set (BASELINE_CMP CLEAN, md5 8c1d1545); 49 BUILD_OK
(48 + restored), none byte-identical to base; restored: cmp clean, binary -nt source, restored == base, no sentinel.
Three probe lanes; for part of the run table 6 (three more lanes) and the Opus seat's batch 3 ran beside them.

check_pred.out:  CHECKPRED exact=59 differs=1 of 60 measured (60 predicted)
COUNTS from table5.out: `grep -c '^NEW'' = 48 = base + 47 mutants; `grep -c '^T4INSTR'' = 12.
  47 mutants on the 121-row instrument = 45 DETECTED + 2 predicted EQUIVALENT (dogft, ctlrdft).
  44 of the 45 red-row sets are exactly PRETABLE 5's.  THE ONE THAT DIFFERS, and why:
      c2_bit8_rearm  predicted {mid once}; measured {mid said, mid once}, 119/121.  RE-RUN ALONE (no other emulator
      running; same frozen instrument, md5 7f286f51): identical, logs/probe_c2_bit8_rearm_ALONE.raw.  My trace missed
      that the notice the re-arm lets through is the session's LAST refusal -- lb +0x1ff -- whose text is exactly what
      `mid said' counts, so that row reads 2 as well.  The mutant is detected either way; the miss is the prediction's.
  The 24 re-run earlier kills: all 22 non-equivalent ones still detected, their sets as predicted; the 2 equivalents
  still 121/121.  The 23 new (19 of mine from this pass's findings, the Opus seat's 4): all detected -- among them
      c2_lbl_imask/istat/ctl (a label-keyed latch), c2_dog100, c2_reg_imask/istat/dog (answers over nonzero
      registers), c2_land_or (imask keeps), c2_rearm_dog/txt/rev (branch re-arms), c2_pre_irq, c2_pre_rev,
      c2_bit7_ans, c2_bit8_land/quiet/ft/rearm/latch (address bits 7 and 8), p_rd_hi_lh (top rd2 v0), p_rd_hi_lb,
      p_rd_lh_all (ten 2-byte answer rows), p_soft_gate (102/121, the SOFTINT-gated decline).

TABLE 4's 111-ROW INSTRUMENT -- the second closing panel's claims, MEASURED:
    c2_lbl_imask 111/111 (codex)   c2_lbl_istat 111/111   c2_dog100 111/111 (codex)   c2_rearm_dog 111/111 (codex)
    c2_reg_imask, c2_reg_istat, c2_reg_dog 111/111 (kimi CLI)   c2_land_or 111/111 (kimi CLI)
    c2_bit7_ans 111/111 (kimi-k3:cloud)   c2_pre_rev 111/111 (the open member of glm's class)
    c2_pre_irq 109/111 -- imask once, istat once: glm's own candidate REFUTED by measurement, as predicted
    c2_lbl_ctl 110/111 -- dog once: a CONTROL-keyed latch was already caught by the 111-row test, as predicted
  Every claim the panel made of a real undetected change was real; the 121-row test detects every one.

AND ONE ESCAPE OF THE 121-ROW INSTRUMENT, measured OUTSIDE this table: the Opus second-closing seat's byte-lane answer at
INTSTAT (`odata = reg >> (8*(8-len-(relative_addr&7)))') scored 121/121 (opus_close2_20260913/batch3/
probe121_istat_lane.raw); table 6 measured its INTMASK twin l_imask 121/121 on this instrument.  Repair 7 (the IRQ seed
nonzero in bytes 0-1) closes both -- killtable6_20260913/POSTTABLE.out.

THE CHANNEL LINE: 59 of 60 predicted sets exact; the one miss is above, with its cause.  A second-order observation worth
keeping: the miss is the SAME shape as table 1's acc8w miss -- a session where a later access prints the same text as the
row's own, so a count row keyed on that text moves too.  A count row's channel is every access in the session that can
print its string, not only the access it names.

DENOMINATOR for closing pass 3, cumulative over tables 1-6 (each by a single-cell or single-label change): table 4's list,
plus -- the answer at every named label over a register nonzero in the lanes the refused read names and in its low
byte, at both widths (REV, CONTROL, TIME by low bytes; INTSTAT, INTMASK, DOG by top lanes and low byte; lane-form at REV,
CONTROL, TIME equivalent); a landing at INTMASK; the latch keyed on any single label (each label-first session refuses
again elsewhere); pre-set in the REV arm; re-arm in CONTROL's DOG and text branches and the REV redirect branch; every
address bit 0-9 carried both ways by each kind of refused access (answer 1R/2R, landing 1W/2W, notice, fall-through,
re-arm, latch).  NOT swept, disclosed: a re-arm or pre-set inside the HARD_RESET branch (unrowable); interior accept
slots; one unnamed offset; joint multi-axis predicates; a function-static latch; widths 3/5/6/7.

POSTTABLE -- #529 kill table 6 (TARGETED, repair 7), written AFTER the table (PRETABLE.out 18:40 predates the driver's
launch, 18:47, and every log)
Driver kill529f.run-184731.sh (frozen); summary table6.out; lane logs logs/lane{0,1,2}.out; per run logs/probe_<m>.raw
(the repair-7 instrument, crime_width_probe.table6.py) and logs/probe_T5INSTR_<m>.raw (table 5's repair-6 instrument) --
27 logs, EVERY one ends CRIMEP_DONE (checked); logs/<m>.diff; builds/.  Scratch clone /tmp/gxopuscrime, baseline = the
#529 working set (BASELINE_CMP CLEAN, dev_sgi_ip32.c md5 8c1d1545); 25 BUILD_OK (24 + restored); restored: cmp clean,
binary -nt source, restored == base byte-identical, sentinel removed.  Its builds and probes ran beside table 5's
probe lanes (six emulators at peak); nothing here disagreed with its prediction, so no re-run alone was owed.

check_pred.out:  CHECKPRED exact=27 differs=0 of 27 measured (27 predicted)
COUNTS from table6.out: `grep -c '^NEW'' = 24 = base + 23 mutants; `grep -c '^T5INSTR'' = 3.
  23 mutants on the repair-7 instrument = 20 DETECTED + 3 predicted EQUIVALENT (l_rev, l_ctl, l_time -- the byte-lane
  answer at REV, CONTROL and TIME returns bytes the model holds at 0; disclosed in the probe header).
  Every one of the 20 red-row sets is exactly PRETABLE 6's -- including the four this repair exists for:
      q_istat_lane  119/121  istat lb v0, istat lh v0   (the Opus seat measured it 121/121 on repair 6)
      l_imask       119/121  imask lb v0, imask lh v0
      q_istat_leak, c2_reg_imask, c2_reg_istat  119/121 each (the whole-register answer: still caught)
  and the 15 re-run kills whose sessions repair 7 changed (imask, istat, gate): all still detected, sets unchanged.

TABLE 5's REPAIR-6 INSTRUMENT, MEASURED:
  l_imask    121/121 -- the INTMASK twin of the Opus seat's istat_lane escaped repair 6, as predicted; repair 7 closes it
  l_dog      119/121 -- repair 6's DOG seed (0x0123456789abcdef) already covered DOG's lanes
  q_dog_leak 119/121 -- likewise (the Opus seat measured it 111/111 on the 111-row test)

WHAT THIS TABLE DOES NOT RE-MEASURE, stated: every kill whose red rows include a session repair 7 did not touch stands on
table 5's measurement of repair 6 (the IRQ seed appears only in the imask, istat and gate sessions).

```

## QUESTIONS

1. **Verify the enumeration.**  For each class the CONTRACT claims closed -- the answer at every named label, the latch
   keyed on any single axis of the access, pre-set and re-arm by an accepted access in every arm and branch, effects
   keyed on any single address bit, refused stores that land -- is the enumeration complete and TRUE of the rows?  Name
   any cell the enumeration claims that no row can see, or any cell of the class it omits.
2. **Is there a floor gap in the 121-row test?**  The smallest source edit to `dev_sgi_ip32.c` that undoes part of the
   fix's behaviour and still scores 121/121, as an exact edit, with the row you expected to catch it and why it cannot.
3. **Which statement in this brief, in POSTTABLE 5 or 6, or in the probe header, is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
