# CLOSING PASS 2 -- `crimewidthkill` (#529): is the twice-repaired regression test complete?  Liveness token `CRIME_CLOSE2_20260913`.

VERDICT LINE FIRST: `CLOSES` (no floor gap remains in the 111-row test) or `GAP: <exact source edit to dev_sgi_ip32.c>`,
then the token.

This is a routine software-testing review of an open-source hardware emulator (GXemul) and its regression test.
"Mutant" means a deliberately modified copy of the emulator's C source used to check that the test notices the change
(standard mutation testing).  Please check the premises, not only the reasoning, and say what you could not check.
Tree: `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` only.  File-reading seats: `src/devices/dev_sgi_ip32.c`
(`DEVICE_ACCESS(crime)`), `regress/crime_width_probe.py`, `regress/artifacts/crimewidthkill/`.

## WHY THIS PASS EXISTS, AND HOW IT CLOSES

The first closing pass (7 scriptable seats + a compile-and-measure seat) found gaps in the 85-row test; the test was
repaired (111 rows).  A repair made in answer to a pass owes its own pass: ONE pass on the repair diff, and the chain
closes on the first valid pass that finds ZERO floor breaches.  Review EFFORT is scoped to the repair diff below; the
FLOOR question (does any single-cell edit in the fix's own enumeration score 111/111?) is asked of the whole test.
A zero is only a zero with its denominator -- the table below is the denominator; add to it or break it.

## SETTLED (recorded; re-stated because the questions depend on it)

* **The fix** (unchanged since pass 2; every seat of four passes found it correct): `DEVICE_ACCESS(crime)` used to stop
  the emulator on any access of length other than 8 or 4.  It now prints one latched `(once)` notice per device instance
  (`int warned`, bit `CRIME_W_LEN`) and `goto crime_declined;` past the register switch to the common tail, which answers
  a read 0 and returns 1.
* **Why the switch must be skipped** (each MEASURED): at CRIME_CONTROL (0x08, writes) a refused access would stop every
  CPU or print an unlatched diagnostic; at CRIME_REV (0x00, either direction, from pc 0xbfc051xx) set pc = ra; at
  INTSTAT/INTMASK (0x10/0x18) re-assert the interrupt line; at CRIME_TIME (0x38) advance the clock; at an unnamed offset
  print a `debug()` line; at CRIME_DOG (0x30) nothing (`break;`); CONTROL reads nothing.
* **The test's history**: 40 rows (table 1) -> 71 (pass 2, table 2) -> 85 (shared-findings pass, table 3) -> 111 (the
  first closing pass, table 4, below).  Every table's red-row sets were predicted in writing BEFORE it ran.
* **The standard**: the test must detect any single-label or single-cell change at every OBSERVABLE switch label for
  each refused {1,2-byte} x {read, write} cell (with every idata bit the arm tests written both ways there), every accept
  cell's shrinkage at both window ends plus anchored cells, the notice's text, channel and latch (the latch keyed on any
  single axis: width, direction, label, block), the answer at every named label, state carried across calls, and the
  decline holding in the device states the tail reads (HARDINT set, the line asserted).  An effect keyed on ONE offset
  the switch does not name, or an interior accept slot, or a joint (multi-axis) predicate, is DISCLOSED coverage debt
  (the probe header lists them) -- a finding there is not a gap unless you show the disclosure is wrong.

## WHAT THE FIRST CLOSING PASS FOUND, AND WHAT NOW CATCHES EACH (each MEASURED at 85/85 on the 85-row test)

| finding | from | now caught by |
|---|---|---|
| `len == 8 && relative_addr != 0` (the 8-byte window's NEAR end) | grok | acc8 near (ld +0x00 -> CRIME_REV's 0x11) |
| latch keyed on CRIME_CONTROL; ENDIANESS never written set | glm | sh08b once; sh08b run (sh 0x0900) |
| latch keyed on `relative_addr >= 0x40`; a refused store landing only at TIME | kimi-k3:cloud | hi once; DISCLOSED (<= 0xffff < 0.1 s) |
| `d->warned = 0;` in the 4-byte arm; `odata = 1` at REV / INTSTAT / TIME | codex | rearm once (14 accepted kinds); rev/istat/imask/time v0, dog v0, ctl v0 |
| CONTROL fall-through keyed on an untested data bit (`!(idata & 0x0002)`) | kimi CLI | all-ones refused writes: sb08 msg, sh08b msg/run |
| decline gated on HARDINT / on prev_asserted (a field the tail reads) | Opus | gate run (HARDINT set via MACE, line asserted) |
| latch pre-set by a 4-byte access; a second latch reusing bit 0; re-arm at the TIME arm | Opus | latch x5 prologue; top said; rearm once, time once |
| 2-byte store landing >= 0x200; refused read >= 0x200 answering the slot | Opus | hi keeps (sh +0x27c); top rd v0 |
| latch keyed on the block / on direction x width | Opus | hi once; latch x5, warm once, imask/istat/dog once |
| nonzero-write fall-through at INTSTAT/INTMASK/TIME | Opus | the refused stores there now write 0xff / 0xffff |
| `len == 4 && relative_addr != 0x210` | Opus | top said (a 4R at +0x210 is 0 either way; the notice moves) |

Refuted on reading and then measured: deepseek's parity-keyed latch (warm once's first refusal is odd) and minimax's
"acc4 at +0x30 unrowed" (it is rowed).

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
artifacts/crimewidthkill/ (killtable_20260913/ through killtable4_20260913/):
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
                                          closing pass), so a fall-through keyed on ANY data bit shows
                                                                                sb08 msg, sh08b msg/run
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
                                           time once, latch x5 (default-arm, low), hi once (the high block,
                                           followed by refusals both >= 0x40 and < 0x200)
     and the latch PRE-SET before any refusal -- by an accepted 4-byte access, or by a second latch on the CONTROL
     text reusing bit 0 (Opus closing seat: `pre4', `ctl_collide') -- latch x5's prologue; by an 8-byte one, warm
     once (sd first) and time once (ld first)
  5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
     session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
     debug() would not (free said)
  6. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this),
     at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
     prelude writes; grok, closing pass: `len == 8 && relative_addr != 0' passed the 85-row version, whose rows sat at
     +0x30 -- an interior slot, not an end), with devsig / devsig hi the 4R cells there; CRIME_DOG +0x30 -- acc8 st+ld
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
     landing only >= 0x200, of either width)
                                                                                                        hi keeps
  8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
     `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
     warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
     4-byte arm's re-arm open on the closing pass: 8W, 8R, 4W and 4R in both lanes, and an accepted access into each
     switch arm, each between two refusals                                                  rearm once, rearm surv
  9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
     (codex, closing pass: `if (relative_addr == CRIME_REV) odata = 1;' passed the 85-row version -- the REV rows
     checked only the pc)                lb/lh rev v0, ctl v0, istat/imask lb/lh v0, dog v0, time lb/lh v0
     and in the far block over a NONZERO slot (Opus closing: a refused read >= 0x200 answering the register)
                                                                                                    top rd v0
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
  * ACCEPT cells at offsets other than +0x30, +0x210 and +0x278: an accept arm narrowed by an address strictly INSIDE
    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.
  * an effect ADDED to the decline arm and keyed on ONE UNNAMED offset (item 9 rows the READ answer at every named
    label) -- a refused store that lands only at
    +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only at
    +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at five default-arm
    offsets; the keeps rows catch a landing at CRIME_DOG and the far block, imask ctl one at INTMASK.  ONE NAMED CELL IS
    OPEN AND SAID SO (kimi-k3:cloud, closing pass): a refused sb/sh that LANDS only at CRIME_TIME stores <= 0xffff,
    which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
    (the tail recomputes it), CONTROL and REV (the prelude rewrites them) such a landing is EQUIVALENT.
  * an accepted WRITE (4 or 8 bytes) at +0x00 or +0x08 shrunk away: the prelude rewrites CRIME_REV and CRIME_CONTROL on
    every access, so no round trip there can observe whether the store was accepted (the CONTROL arm's effects are
    rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
    needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
  * a latch keyed on a JOINT predicate (e.g. only 2-byte refusals at CRIME_TIME), or on one unnamed offset other than the
    default-arm cells the latch rows refuse at: clause (e), the single-axis generating set being the floor.
  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 (the 71-row test) by the Opus seat
    (F2, `sft'); it is the single-unnamed-offset class of the bullet above.
  * a FUNCTION-STATIC latch in place of `d->warned' is NOT equivalent in general -- two IP32 machines in one gxemul
    process would share it -- and this single-machine probe cannot see it (kimi-k3:cloud, F2; the pass-2 Opus seat had
    recorded it "equivalent", which holds only for one machine per process).
  * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
    not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.
  * independence between two CRIME instances (the latch is per instance by construction; IP32 has one CRIME).

```

## THE REPAIR DIFF -- the 85-row test -> the 111-row test (`git diff --no-index`, verbatim; 16 hunks)

```diff
diff --git a/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable3_20260913/crime_width_probe.table3.py b/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py
index 6c9cf4e..3eaf76c 100644
--- a/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/crimewidthkill/killtable3_20260913/crime_width_probe.table3.py
+++ b/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/crime_width_probe.py
@@ -9,5 +9,5 @@ src/devices/dev_sgi_ip32.c, DEVICE_ACCESS(crime): an access whose length is neit
 
 so one guest lb/lbu/lh/lhu/sb/sh anywhere in CRIME (physical 0x14000000, KSEG1 0xb4000000) ended the emulator
-(witnessed 6/6 at rung 3: regress/artifacts/crimewidthkill/crime_width_witness_20260913.py).  #529 DECLINES the width
+(witnessed for all six widths at rung 3: regress/artifacts/crimewidthkill/crime_width_witness_20260913.py).  #529 DECLINES the width
 with one latched `(once)' announce and a `goto' to the function's common tail, skipping the register switch -- the
 #498 sgi_de shape.  A read is answered 0 by the tail, a write is dropped, the PC advances, no exception is raised.
@@ -16,14 +16,19 @@ Every access here is a real MIPS guest instruction through real address decode a
 
 CONTRACT -- the edits this detector is designed to catch (clause (e)), each MEASURED in a kill table under
-artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3_20260913/):
+artifacts/crimewidthkill/ (killtable_20260913/ through killtable4_20260913/):
   1. the kill reinstated verbatim, or any other host death at the width arm, before or after the announce
                                                        <op> surv (six widths), hi surv, latch surv, sb08 run
-  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)      <op> pc, <op> exc, lb/lh/lbu/lhu v0
+  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)   lb/lh/sb/sh pc and exc, lb/lh/lbu/lhu v0
   3. the refused access FALLING INTO THE REGISTER SWITCH -- the goto lost, or narrowed by width, direction, or ADDRESS.
      The switch's observable arms, per refusal cell:
         CRIME_CONTROL (+0x08), writes     sb 0x01 prints the unimplemented-control fatal    sb08 msg
                                           sh 0x0800 stops every CPU (HARD_RESET)            sh08 run, sh08 pc
-                                          and the arm's TESTED idata bits both ways at 2W: sh 0x0201 (DOG set,
-                                          RESET clear) and sh 0x0a00 (both set)             sh08b msg, sh08b run
+                                          and the arm's three TESTED idata bits (DOG 0x200, RESET 0x800,
+                                          ENDIANESS 0x100) each both ways at 2W: sh 0x0201,
+                                          0x0900, 0x0a00 with sh08 0x0800       sh08b msg, sh08b run
+                                          plus ALL-ONES refused writes, sb 0xff and sh 0xffff (kimi CLI,
+                                          closing pass), so a fall-through keyed on ANY data bit shows
+                                                                                sb08 msg, sh08b msg/run
+        and the refused stores at INTSTAT, INTMASK and TIME carry all-ones (0xff / 0xffff) for the same reason
         CRIME_REV (+0x00), reads AND writes, from pc 0xbfc05180: the PROM-probe hack sets pc = ra (it does not test
                                           the direction)                                    lb/lh/sb/sh rev pc
@@ -45,23 +50,49 @@ artifacts/crimewidthkill/ (killtable_20260913/, killtable2_20260913/, killtable3
      +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
      removes or moves these channels and owes their re-derivation -- the sw08 controls will go red to say so. ***
-  4. the latch removed, never set, or keyed on the access (its bit taken from len, relative_addr or writeflag --
-     Opus, F2): five refused accesses in one session, a 2-byte read at an even address FIRST, owe EXACTLY ONE
-     announce (latch x5); a session whose first refusal is a store owes one too (warm once)
+  4. the latch removed, never set, or KEYED ON THE ACCESS -- the class closed on its single axes after two passes
+     found members (F2: `|= len', `|= relative_addr', `<< writeflag'; closing pass: keyed on CRIME_CONTROL, on
+     `relative_addr >= 0x40', on address parity).  A keyed latch shows only when the first refusal in a session falls
+     where it does not set, so every axis value is a FIRST refusal followed by another, with an announce count:
+        width 1 or 2 and direction R or W  warm once (sb, write, odd), latch x5 (lh, read, even)
+        each label first                   rev once, sh08b once (CONTROL), istat once, imask once, dog once,
+                                           time once, latch x5 (default-arm, low), hi once (the high block,
+                                           followed by refusals both >= 0x40 and < 0x200)
+     and the latch PRE-SET before any refusal -- by an accepted 4-byte access, or by a second latch on the CONTROL
+     text reusing bit 0 (Opus closing seat: `pre4', `ctl_collide') -- latch x5's prologue; by an 8-byte one, warm
+     once (sd first) and time once (ld first)
   5. the announce: its text (`unimplemented len=N at 0xA -- declined.  (once) ]' exactly once in each width's own
      session: lb/lh/sb/sh said, hi said), and its CHANNEL -- fatal(), which prints when the guest free-runs, where a
      debug() would not (free said)
   6. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this),
-     at BOTH ends of the window:  CRIME_DOG +0x30 -- acc8 st+ld (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi;
-     the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w.  Those rows are ROUND TRIPS and cannot see an
+     at BOTH ends of the window:  the FIRST slot +0x00 -- acc8 near (8R, anchored to CRIME_REV's 0x11, which the
+     prelude writes; grok, closing pass: `len == 8 && relative_addr != 0' passed the 85-row version, whose rows sat at
+     +0x30 -- an interior slot, not an end), with devsig / devsig hi the 4R cells there; CRIME_DOG +0x30 -- acc8 st+ld
+     (8W, 8R), acc4 rhi, acc4 rlo, acc4 wlo, acc4 whi; the last slot +0x278 -- top8 st+ld, top4 rhi, top4 rlo, top4 w.  Those rows are ROUND TRIPS and cannot see an
      accept arm that re-maps its register index (kimi-k3:cloud, F2: `d->reg[(relative_addr & 0x3f) / 8]' passed the
      71-row version), so one row is ANCHORED: `top8 anchor' reads bank-1 control at +0x210, a value the PRELUDE writes
-     by bank index (1 for -M 64), not by the decode under test.  *** It pins the model's CURRENT bank layout, which the
+     by bank index (1 for -M 64), not by the decode under test; `top4 anchor' reads its low half with a 4R.  The 4R
+     of its HIGH half answers 0 accepted or refused, so that cell is pinned by the ANNOUNCE instead (Opus closing:
+     `len == 4 && relative_addr != 0x210' passed the 85-row version): every accept cell the top session touches
+     before its one refusal is pinned the same way                                                      top said
+     *** It pins the model's CURRENT bank layout, which the
      filed `crimebankorder' disputes; a round that re-orders the banks owes this row's re-derivation. ***
   7. a refused store that LANDS: CRIME_DOG seeded by an accepted sd survives a refused sb and sh     sb keeps, sh keeps;
-     and at the far block, a refused sb +0x27f leaves +0x278 reading 0 (Opus, F2: a store landing only >= 0x200)
+     and at the far block, a refused sb +0x27f and sh +0x27c leave +0x278 reading 0 (Opus, F2 and closing: a store
+     landing only >= 0x200, of either width)
                                                                                                         hi keeps
   8. state carried ACROSS calls: a declined read after accepted reads of a nonzero register still answers 0 (an
      `odata' made static), and an accepted access between two refusals does not re-arm the announce    warm v0,
-     warm once  (the codex seat, F2)
+     warm once  (the codex seat, F2) -- closed over every place an accepted access can go after codex found the
+     4-byte arm's re-arm open on the closing pass: 8W, 8R, 4W and 4R in both lanes, and an accepted access into each
+     switch arm, each between two refusals                                                  rearm once, rearm surv
+  9. the ANSWER at each named label: a refused read at CRIME_REV, CONTROL, INTSTAT, INTMASK, DOG and TIME answers 0
+     (codex, closing pass: `if (relative_addr == CRIME_REV) odata = 1;' passed the 85-row version -- the REV rows
+     checked only the pc)                lb/lh rev v0, ctl v0, istat/imask lb/lh v0, dog v0, time lb/lh v0
+     and in the far block over a NONZERO slot (Opus closing: a refused read >= 0x200 answering the register)
+                                                                                                    top rd v0
+  10. the decline HOLDS WHILE AN INTERRUPT IS LATCHED: HARDINT set by the guest through MACE and the CRIME line
+      asserted, a refused sh 0x0800 at CONTROL still does not stop the CPUs (the Opus closing seat: `if
+      (!d->reg[CRIME_HARDINT / 8])' -- a field the tail reads -- and `if (!d->prev_asserted)' passed the 85-row
+      version)                                        gate run, with gate hardint and gate line as its controls
 
 DISCLOSED, not rowed:
@@ -69,5 +100,5 @@ DISCLOSED, not rowed:
     (#95, src/cpus/memory_rw.c -- `if (writeflag == MEM_READ)' then `memset(data, 0, len);', immediately above
     `paddr -= mem->devices[i].baseaddr;'), and on a declined access nothing between the entry and the tail writes
-    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 in kill table 1.
+    HARDINT or SOFTINT, so the tail's restore and recompute are identities.  Measured 40/40 (the then 40-row test) in kill table 1.
   * a fall-through confined to the two label cells whose arms have NO body for that access, both EQUIVALENT:
       CRIME_DOG (0x30)       `No warning.' -- the arm is `break;'
@@ -75,10 +106,20 @@ DISCLOSED, not rowed:
     Each measured as a survivor in kill table 2 (`!= CRIME_DOG', the CONTROL-read-only fall-through).
   * ACCEPT cells at offsets other than +0x30, +0x210 and +0x278: an accept arm narrowed by an address strictly INSIDE
-    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71) is not seen.
-  * an effect ADDED to the decline arm and keyed on ONE offset the switch does not name -- a refused store that lands
-    only at +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only
-    at +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at five default-arm
-    offsets; an arbitrary single offset inside a partition the body does not distinguish is clause (e) debt.
-  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 by the Opus seat
+    the window (e.g. `len == 8 && relative_addr != 0x100', kill table 2's acc8mid, 71/71 on the 71-row test) is not seen.
+  * an effect ADDED to the decline arm and keyed on ONE UNNAMED offset (item 9 rows the READ answer at every named
+    label) -- a refused store that lands only at
+    +0x31, a declined read answering nonzero only at +0x20, a silent decline only at +0x100, a fall-through only at
+    +0x40 (kimi CLI, glm, F2).  The rows pin the refusal floor at every observable LABEL and at five default-arm
+    offsets; the keeps rows catch a landing at CRIME_DOG and the far block, imask ctl one at INTMASK.  ONE NAMED CELL IS
+    OPEN AND SAID SO (kimi-k3:cloud, closing pass): a refused sb/sh that LANDS only at CRIME_TIME stores <= 0xffff,
+    which the time rows' 0.1 s threshold cannot tell from the 66-990 the first tick adds -- clause (e) debt.  At INTSTAT
+    (the tail recomputes it), CONTROL and REV (the prelude rewrites them) such a landing is EQUIVALENT.
+  * an accepted WRITE (4 or 8 bytes) at +0x00 or +0x08 shrunk away: the prelude rewrites CRIME_REV and CRIME_CONTROL on
+    every access, so no round trip there can observe whether the store was accepted (the CONTROL arm's effects are
+    rowed separately as sw08 halts / sw08 msg ctl).  The 4R-high cell at +0x00 is carried by `rev pc ctl' (its redirect
+    needs the access ACCEPTED), not by `devsig hi', whose 0 a refused read also returns.
+  * a latch keyed on a JOINT predicate (e.g. only 2-byte refusals at CRIME_TIME), or on one unnamed offset other than the
+    default-arm cells the latch rows refuse at: clause (e), the single-axis generating set being the floor.
+  * a fall-through only at CRIME_SOFTINT (0x20), which the switch does not name -- measured 71/71 (the 71-row test) by the Opus seat
     (F2, `sft'); it is the single-unnamed-offset class of the bullet above.
   * a FUNCTION-STATIC latch in place of `d->warned' is NOT equivalent in general -- two IP32 machines in one gxemul
@@ -275,9 +316,14 @@ c = roundtrip(A)
 x, _ = ld(A, "lw", CRIME + 4, "s1"); c += x
 x, _ = ld(A, "lw", CRIME + 0, "s2"); c += x
-t, clean = session(c + ["print s1", "print s2"])
+x, _ = ld(A, "ld", CRIME + 0, "s3"); c += x
+t, clean = session(c + ["print s1", "print s2", "print s3"])
 row("live", pr(t, "v1"), "0x%x" % LIVE_VAL, "LIVENESS: RAM round trip, same apparatus")
 row("devsig", pr(t, "s1"), "0x11", "CRIME_REV low half = rev 0x11: a device")
 row("devsig hi", pr(t, "s2"), "0x0", "CRIME_REV high half reads 0")
 row("dflt ctl", count(t, "[ crime: read from 0x4,", clean), 1, "CONTROL: default-arm text prints when stepped")
+#  grok, closing pass: the NEAR end of the 8-byte accept window is +0x00, not CRIME_DOG -- `len == 8 && relative_addr
+#  != 0' passed the 85-row version.  Anchored: the prelude writes CRIME_REV's revision on every access, so an 8R there
+#  reads 0x11 from a channel outside the decode (an 8W round trip there is impossible for the same reason: disclosed).
+row("acc8 near", pr(t, "s3"), "0x11", "8R at +0x00 (the window's first slot): CRIME_REV")
 
 # ---- the switch channels are LIVE on an accepted width (else rows 3.x could not vary) ----
@@ -349,6 +395,7 @@ row("sh08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W: CPUs NOT stopped (RAM trip
 A = Addr(CODE)
 x, here = st(A, "sb", CRIME + 0x08, 0x01)
-t, clean = session(x + AFTER + roundtrip(A))
-row("sb08 msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "1W sb 0x01 +0x08: no CONTROL text")
+f, _ = st(A, "sb", CRIME + 0x08, 0xff)          # all-ones (kimi CLI, closing pass): a fall-through keyed on ANY bit
+t, clean = session(x + f + AFTER + roundtrip(A))
+row("sb08 msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "1W sb 0x01, 0xff +0x08: no CONTROL text")
 row("sb08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "1W: the session completes (a RAM trip)")
 
@@ -360,15 +407,22 @@ row("sb08 run", pr(t, "v1"), "0x%x" % LIVE_VAL, "1W: the session completes (a RA
 A = Addr(CODE)
 x, _ = st(A, "sh", CRIME + 0x08, 0x0201)
+e, _ = st(A, "sh", CRIME + 0x08, 0x0900)       # glm, closing pass: ENDIANESS (0x0100) is the arm's third tested bit
 y, _ = st(A, "sh", CRIME + 0x08, 0x0a00)
-t, clean = session(x + y + AFTER + roundtrip(A))
+f, _ = st(A, "sh", CRIME + 0x08, 0xffff)        # all-ones: every bit a data-keyed narrowing could key on, set
+t, clean = session(x + e + y + f + AFTER + roundtrip(A))
 row("sh08b msg", count(t, "CRIME_CONTROL: unimplemented", clean), 0, "2W sh 0x0201 +0x08 (DOG set): no CONTROL text")
-row("sh08b run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W sh 0x0a00 +0x08 (DOG+RESET): CPUs NOT stopped")
+row("sh08b run", pr(t, "v1"), "0x%x" % LIVE_VAL, "2W sh 0x0900, 0x0a00 +0x08 (E/DOG+RESET): CPUs NOT stopped")
+row("sh08b once", count(t, "-- declined.", clean), 1, "4 refusals at CONTROL, first at CONTROL: one notice")
 
 for op in ("lb", "lh"):
     A = Addr(CODE)
     x, _ = ld(A, op, CRIME + 0, "v0", at=PROBE_PC)
-    t, clean = session(["ra=0x%x" % RA] + x + AFTER)
+    more = ld(A, "lb", CRIME + 0x07, "v1")[0] if op == "lb" else []     # a second refusal: the REV-first latch cell
+    t, clean = session(["ra=0x%x" % RA] + x + AFTER + ["print v0"] + more)
     row("%s rev pc" % op, pr(t, "pc"), "0x%x" % (PROBE_PC + 4), "%dR at CRIME_REV from 0xbfc05180: pc NOT ra"
         % (1 if op == "lb" else 2))
+    row("%s rev v0" % op, pr(t, "v0"), "0x0", "refused %s at CRIME_REV answers 0" % op)
+    if op == "lb":
+        row("rev once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_REV, then +0x07: one notice")
 
 #  the CRIME_REV arm's PROM-probe hack does not test writeflag, so the WRITE cells at +0 are side-effect cells too
@@ -403,14 +457,14 @@ for lbl, off in (("imask", 0x18), ("istat", 0x10)):
     x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
     c += ["print cause"]
-    x, _ = ld(A, "lb", CRIME + off, "v0"); c += x
+    x, _ = ld(A, "lb", CRIME + off, "a0"); c += x
     c += ["print cause"]
-    x, _ = st(A, "sb", CRIME + off, 0); c += x
+    x, _ = st(A, "sb", CRIME + off, 0xff); c += x
     c += ["print cause"]
-    x, _ = ld(A, "lh", CRIME + off, "v0"); c += x
+    x, _ = ld(A, "lh", CRIME + off, "a1"); c += x
     c += ["print cause"]
-    x, _ = st(A, "sh", CRIME + off, 0); c += x
+    x, _ = st(A, "sh", CRIME + off, 0xffff); c += x
     c += ["print cause"]
     x, _ = ld(A, "lw", CRIME + off, "v0"); c += x
-    c += ["print cause"]
+    c += ["print cause", "print a0", "print a1"]
     t, clean = session(c)
     row("%s pre" % lbl, ip2(nth(t, "cause", 0)), "clear", "IP2 low after SOFTINT's default-arm store")
@@ -420,13 +474,44 @@ for lbl, off in (("imask", 0x18), ("istat", 0x10)):
     row("%s sh" % lbl, ip2(nth(t, "cause", 4)), "clear", "refused sh +0x%x: no reassert" % off)
     row("%s ctl" % lbl, ip2(nth(t, "cause", 5)), "set", "CONTROL: accepted lw +0x%x reasserts" % off)
+    row("%s once" % lbl, count(t, "-- declined.", clean), 1, "4 refusals, first at +0x%x: one notice" % off)
+    row("%s lb v0" % lbl, pr(t, "a0"), "0x0", "refused lb +0x%x answers 0" % off)
+    row("%s lh v0" % lbl, pr(t, "a1"), "0x0", "refused lh +0x%x answers 0" % off)
+
+# ---- THE DECLINE HOLDS WHILE AN INTERRUPT IS LATCHED (the Opus closing seat: `if (!d->reg[CRIME_HARDINT / 8]) goto
+#  crime_declined;' passed the 85-row version -- every refusal in it ran with HARDINT == 0, and the tail the goto jumps
+#  to READS HARDINT, so the field is a DEPENDS-ON operand; `if (!d->prev_asserted)' passed too).  The guest latches a
+#  hardware interrupt by two MACE stores (ISA interrupt status, then mask -> crime_interrupt_assert -> HARDINT), asserts
+#  the CRIME line (INTMASK and SOFTINT, reasserted by an accepted lw), then a refused sh 0x0800 at CRIME_CONTROL: falling
+#  into the switch there would stop every CPU.  Both controls are rowed: HARDINT reads nonzero and IP2 is set.
+MACE = 0xbf310000                                   # KSEG1 of the `mace addr=0x1f310000' device (dev_sgi_ip32.c)
+A = Addr(CODE)
+c = []
+for off, val in ((0x10, 0x01), (0x18, 0x01)):
+    x, _ = st(A, "sd", MACE + off, val); c += x
+x, _ = st(A, "sd", CRIME + 0x18, BIT); c += x
+x, _ = st(A, "sd", CRIME + 0x20, BIT); c += x
+x, _ = ld(A, "lw", CRIME + 0x18, "a0"); c += x
+x, _ = ld(A, "ld", CRIME + 0x28, "s2"); c += x
+c += ["print s2", "print cause"]
+x, _ = st(A, "sh", CRIME + 0x08, 0x0800); c += x
+t, clean = session(c + roundtrip(A))
+hint = nth(t, "s2", 0)
+row("gate hardint", "set" if hint else ("absent" if hint is None else "clear"), "set",
+    "CONTROL: two MACE stores latch HARDINT (raw %s)" % hint)
+row("gate line", ip2(nth(t, "cause", 0)), "set", "CONTROL: the CRIME line is asserted")
+row("gate run", pr(t, "v1"), "0x%x" % LIVE_VAL, "refused sh 0x800 +0x08 with an irq latched: CPUs run")
 
 # ---- the TIME label: an accepted read returns the value of the PREVIOUS update, then updates -- so a refused access
 #  that reached crime_update_crime_time() would show in the NEXT read.  The first `ld' latches last_microseconds; on the
-#  fixed build nothing else updates TIME before the next `ld' -- the device tick (machine_add_tickfunction, CRIME_TICKSHIFT
-#  14) fires every 2^14 cycles and a session steps only a few dozen instructions -- so that read is far below SMALL (0.1 s
-#  of TIME; each row prints its raw value -- the Opus seat's separate apparatus read 66 or 132); a fall-through at 0x38
+#  fixed build the only other update before the next `ld' is the device tick's FIRST firing -- ticks_till_next starts at
+#  0, so it fires right after the session's first `ld' (the Opus closing seat; this said "nothing else updates TIME"
+#  until then), and it adds the few microseconds since the latch: the 66-990 the rows print (measured across 52 cells
+#  against SMALL = 6.6e6).  Later ticks are 2^14 cycles apart and a session steps a few dozen instructions; a fall-through at 0x38
 #  makes it the wall-clock interval of the intervening debugger commands, ~1e8.  The third `ld' is the CONTROL that the
 #  channel moves.  (Opus pass 2, E3; the tick-spacing wording corrected by the kimi CLI seat on the F2 pass.)
-#  ASSUMPTION, disclosed: no tick boundary falls between the first `ld' and the refused access.
+#  ASSUMPTION, disclosed: no tick boundary falls between the first `ld' and the `ld' that samples s1 (codex, closing pass:
+#  the window runs THROUGH the sampling read, not only to the refused access).  The IRQ rows carry the same assumption:
+#  dev_crime_tick also calls crime_interrupt_reassert(), so a tick inside a session could raise IP2 on the fixed build
+#  (kimi CLI, closing pass) -- a false red, never a false green; measured stable so far.
 SMALL = 66 * 100000
 
@@ -443,11 +528,17 @@ for op in ("lb", "sb", "lh", "sh"):
         x, _ = ld(A, op, CRIME + 0x38, "v0"); c += x
     else:
-        x, _ = st(A, op, CRIME + 0x38, 0); c += x
+        x, _ = st(A, op, CRIME + 0x38, 0xff if op == "sb" else 0xffff); c += x
     x, _ = ld(A, "ld", CRIME + 0x38, "s1"); c += x
     x, _ = ld(A, "ld", CRIME + 0x38, "s2"); c += x
-    t, clean = session(c + ["print s1", "print s2"])
+    if op == "lb":                                  # a second refusal: the TIME-first latch cell
+        x, _ = ld(A, "lb", CRIME + 0x07, "v1"); c += x
+    t, clean = session(c + ["print s1", "print s2", "print v0"])
     s1, s2 = nth(t, "s1", 0), nth(t, "s2", 0)
     row("time %s" % op, mag(s1), "small", "after refused %s +0x38 (raw %s)" % (op, s1))
     row("time %s ctl" % op, mag(s2), "large", "CONTROL: accepted ld moved TIME (raw %s)" % s2)
+    if op in ("lb", "lh"):
+        row("time %s v0" % op, pr(t, "v0"), "0x0", "refused %s +0x38 answers 0" % op)
+    if op == "lb":
+        row("time once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_TIME, then +0x07: one notice")
 
 # ---- a refused store leaves the register it names untouched (CRIME_DOG seeded by an accepted sd) ----
@@ -470,9 +561,33 @@ row("warm v0", pr(t, "v0"), "0x0", "refused lbu AFTER accepted reads of 0x0123..
 row("warm once", count(t, "-- declined.", clean), 1, "refused, accepted, refused: still one announce")
 
+#  RE-ARM, closed over every place an accepted access can go (codex, closing pass: `d->warned = 0;' in the 4-byte arm
+#  passed the 85-row version -- `warm once' interleaves only 8-byte accesses; the Opus seat measured it 85/85).  One
+#  refusal latches; then each ACCEPTED kind -- 8W, 8R, 4W and 4R in both lanes, and an accepted access into each switch
+#  arm (DOG, TIME, INTMASK, INTSTAT, REV, CONTROL, the default arm low and in the far block) -- is followed by a refusal.
+#  A re-arm anywhere an accepted access reaches shows as a second notice.  (A re-arm in the common tail, which refusals
+#  also reach, shows in latch x5.)
+A = Addr(CODE)
+c = []
+x, _ = ld(A, "lb", CRIME + 0x07, "v0"); c += x
+for op, off in (("sd", 0x30), ("ld", 0x30), ("sw", 0x34), ("lw", 0x34), ("sw", 0x30), ("lw", 0x30),
+                ("ld", 0x38), ("lw", 0x18), ("lw", 0x10), ("lw", 0x00), ("sw", 0x08), ("lw", 0x04),
+                ("sd", 0x278), ("ld", 0x278)):
+    x, _ = (st(A, op, CRIME + off, 0) if op[0] == "s" else ld(A, op, CRIME + off, "a0")); c += x
+    x, _ = ld(A, "lb", CRIME + 0x06, "v0"); c += x
+t, clean = session(c + roundtrip(A))
+row("rearm once", count(t, "-- declined.", clean), 1, "15 refusals, 14 accepted kinds between: one notice")
+row("rearm surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "the whole interleave completes (a RAM trip)")
+
 # ---- ACCEPT cells at the window's LAST 8-byte slot (+0x278; no case label, no prelude write) -- the far bound ----
 A = Addr(CODE)
 c = []
 x, _ = ld(A, "ld", CRIME + 0x210, "s2"); c += x
+x, _ = ld(A, "lw", CRIME + 0x214, "s1"); c += x      # 4R of the anchored slot's low half
+#  4R of its HIGH half (the Opus closing seat: `len == 4 && relative_addr != 0x210' passed the 85-row version).  Its
+#  value is 0 accepted or refused -- the prelude rewrites the slot on every access -- so the row is the ANNOUNCE: a
+#  refused accept cell here takes the session's one notice, and `top said' below reads 0.
+x, _ = ld(A, "lw", CRIME + 0x210, "t1"); c += x
 x, _ = st(A, "sd", CRIME + 0x278, 0x0102030405060708); c += x
+x, _ = ld(A, "lb", CRIME + 0x27b, "v0"); c += x      # a REFUSED read while the far slot is nonzero (Opus: rd_hi)
 x, _ = ld(A, "ld", CRIME + 0x278, "a0"); c += x
 x, _ = ld(A, "lw", CRIME + 0x278, "a1"); c += x
@@ -481,6 +596,9 @@ x, _ = st(A, "sw", CRIME + 0x27c, 0x0a0b0c0d); c += x
 x, _ = st(A, "sw", CRIME + 0x278, 0x11112222); c += x
 x, _ = ld(A, "ld", CRIME + 0x278, "s0"); c += x
-t, clean = session(c + ["print s2", "print a0", "print a1", "print a2", "print s0"])
+t, clean = session(c + ["print s2", "print a0", "print a1", "print a2", "print s0", "print s1", "print v0"])
 row("top8 anchor", pr(t, "s2"), "0x1", "8R +0x210: bank-1 ctrl the PRELUDE wrote (-M 64)")
+row("top4 anchor", pr(t, "s1"), "0x1", "4R +0x214: the anchored slot's low half")
+row("top rd v0", pr(t, "v0"), "0x0", "refused lb +0x27b over a nonzero slot answers 0")
+row("top said", said(t, 1, 0x27b, clean), 1, "lb +0x27b is the first refusal: every access before it accepted")
 row("top8 st+ld", pr(t, "a0"), "0x102030405060708", "8W then 8R at +0x278")
 row("top4 rhi", pr(t, "a1"), "0x1020304", "4R high half at +0x278")
@@ -491,10 +609,24 @@ row("top4 w", pr(t, "s0"), "0x111122220a0b0c0d", "4W both halves at +0x278/+0x27
 A = Addr(CODE)
 x, here = st(A, "sb", CRIME + 0x27f, 0xff)
-y, _ = ld(A, "ld", CRIME + 0x278, "a0")        # the refused byte's register, read back by an ACCEPTED ld
-t, clean = session(x + AFTER + roundtrip(A) + y + ["print a0"])
+w, _ = st(A, "sh", CRIME + 0x27c, 0xffff)      # a refused 2-byte store in the far block too (Opus closing: wst_mc2)
+y, _ = ld(A, "ld", CRIME + 0x278, "a0")        # the refused stores' register, read back by an ACCEPTED ld
+z, _ = st(A, "sb", CRIME + 0x27e, 0xee)        # follow-up refusals: one in the high block (a latch keyed on >= 0x40)
+z2, _ = ld(A, "lb", CRIME + 0x07, "v0")        #   and one low (a latch whose bit depends on the block, `lt_blk')
+t, clean = session(x + AFTER + roundtrip(A) + w + y + ["print a0"] + z + z2)
 row("hi said", said(t, 1, 0x27f, clean), 1, "sb +0x27f: own announce, once")
 row("hi nodflt", dflt(t, clean, 0x27f, True), 0, "switch default arm NOT reached at 0x27f")
 row("hi surv", pr(t, "v1"), "0x%x" % LIVE_VAL, "host survives, then a RAM trip")
-row("hi keeps", pr(t, "a0"), "0x0", "refused sb +0x27f does not land (ld +0x278)")
+row("hi keeps", pr(t, "a0"), "0x0", "refused sb +0x27f, sh +0x27c do not land (ld +0x278)")
+row("hi once", count(t, "-- declined.", clean), 1, "first refusal +0x27f, then 0x27c/0x27e/0x07: one notice")
+
+# ---- the latch, first refusal at CRIME_DOG (the one named label with no session whose FIRST refusal is there) ----
+A = Addr(CODE)
+x, _ = ld(A, "lb", CRIME + 0x30, "v0")
+y, _ = ld(A, "lb", CRIME + 0x07, "v1")
+z, _ = ld(A, "lh", CRIME + 0x08, "a0")        # a refused read at CRIME_CONTROL (codex, closing pass: answers at labels)
+t, clean = session(x + y + z + ["print v0", "print a0"])
+row("dog once", count(t, "-- declined.", clean), 1, "first refusal at CRIME_DOG, then +0x07: one notice")
+row("dog v0", pr(t, "v0"), "0x0", "refused lb at CRIME_DOG answers 0")
+row("ctl v0", pr(t, "a0"), "0x0", "refused lh at CRIME_CONTROL answers 0")
 
 # ---- FREE-RUNNING: the announce is a fatal(), so it prints when the guest is NOT single-stepped (a debug() would not) ----
@@ -515,4 +647,11 @@ row("free v0", pr(t, "v0"), "0x0", "free-running lb +7: declined read answers 0"
 A = Addr(CODE)
 c = []
+#  PROLOGUE (the Opus closing seat): accepted accesses BEFORE the first refusal -- a notice PRE-SILENCED by an accepted
+#  access (`d->warned |= CRIME_W_LEN;' in an accept arm, `pre4') shows as zero notices; and an accepted CONTROL write
+#  whose unmodelled bit prints the CONTROL text, so a future second latch on THAT message reusing bit 0 (`ctl_collide')
+#  shows the same way.  8-byte pre-sets show in warm once (sd first) and time once (ld first).
+for op, off, val in (("sw", 0x08, 0x01), ("sw", 0x34, 0x0badcafe)):
+    x, _ = st(A, op, CRIME + off, val); c += x
+x, _ = ld(A, "lw", CRIME + 0x34, "a0"); c += x
 #  lh FIRST (Opus seat, F2): a latch whose bit is taken from the access -- `d->warned |= len' or `|= relative_addr' --
 #  sets bit 0 only for a 1-byte access or an odd address, so the lh at +0x06 would leave it clear and the lb after it
@@ -529,4 +668,5 @@ npass = sum(1 for _, ok in rows if ok)
 st_ = dict(rows)
 control = all(st_.get(n, False) for n in ("live", "devsig", "devsig hi", "dflt ctl", "rev pc ctl", "sw08 halts",
+                                          "gate hardint", "gate line",
                                           "sw08 msg ctl", "imask pre", "imask ctl", "istat pre", "istat ctl",
                                           "time lb ctl", "time sb ctl", "time lh ctl", "time sh ctl"))
```

## MUTATION-TEST TABLE 4 -- predictions and results (`PRETABLE.out` written before the run; `POSTTABLE.out`)

```
POSTTABLE -- #529 kill table 4 (TARGETED), written AFTER the table (PRETABLE.out 13:03 predates the first log, 13:16)
Driver kill529d.run-130744.sh (frozen); summary table4.out; lane logs logs/lane0.out + logs/lane1.out; per run
logs/probe_<m>.raw (the 111-row instrument) and logs/probe_T3INSTR_<m>.raw (table 3's 85-row instrument) -- 57 logs, EVERY
one ends CRIMEP_DONE (checked: `tail -1' over all 57); logs/<m>.diff; builds/.  Instruments: crime_width_probe.table4.py
and ../killtable3_20260913/crime_width_probe.table3.py (md5s in logs/INSTRUMENT.md5).  Scratch clone /tmp/gxopuscrime,
baseline = the #529 working set (BASELINE_CMP CLEAN, dev_sgi_ip32.c md5 8c1d1545), rebuilt in the clone; 48 BUILD_OK
(47 + restored), every mutant a fresh object, none byte-identical to base; restored afterwards: cmp clean, binary -nt
source, restored == base byte-identical, sentinel removed.  Builds serial; probe runs in two lanes (PRETABLE's warrant).

THE PREDICTIONS, CHECKED MECHANICALLY: check_pred.py transcribes PRETABLE 4's red-row sets and compares each run's full
FAILING list, its score, its denominator, its CONTROL line and its sentinel.  Output check_pred.out:
    CHECKPRED exact=57 differs=0 of 57 measured (57 predicted)
COUNTS, derived from table4.out: `grep -c '^NEW'' = 47 = base + 46 mutants; `grep -c '^T3INSTR'' = 10.
  46 mutants on the 111-row test = 43 DETECTED + 3 predicted survivors:
      dogft, ctlrdft    EQUIVALENT (re-measured because dog v0 / ctl v0 now read exactly their cells; both still 0)
      time_land         disclosed, clause (e): the landed store read back as s1 = 255 (sb 0xff) and 65535 (sh 0xffff),
                        both `small' against SMALL = 6.6e6 -- the probe header's disclosure, measured
  Every one of the 43 red-row sets is EXACTLY the set PRETABLE 4 named, including the traced counts: o_rearm4 rearm
  once 10; o_lt_wl latch x5 4, warm once 3, imask/istat once 4, hi once 3, dog once 2; lt_addr's seven label-first
  counts; lt_len sh08b once 4; lt_par warm/rearm/hi once 2 each; lt_rng hi once 3; lt_ctl sh08b once 4; o_pre4 top said 0
  and latch x5 0; o_rd_hi top rd v0 0x8 (the slot's low byte); wst_mc and o_wst_mc2 hi keeps 0xffff; rev_od1 lb/lh rev
  v0 0x1; c_endian sh08b run SENT (0x0900 carries ENDIANESS and HARD_RESET; sh08b msg stayed 0 -- the later sh's did not
  execute after the stop, as predicted); c_bit1 sb08 msg 1, sh08b msg 1, sh08b run SENT; acc8dog's fifteen rows with
  CONTROL=FAIL and hi keeps GREEN; len2only's sixteen.
  Of the 46: 24 are earlier tables' kills RE-RUN by PRETABLE 4's rule (every recorded red row in a changed session) --
  all 22 non-equivalent ones still detected, the 2 equivalents still equivalent; 12 are the Opus closing seat's
  non-duplicate mutants (o_lt_len, o_c_dog byte-identical to lt_len, c_dog -- run once); 10 are the closing panel's.

TABLE 3's 85-ROW INSTRUMENT -- the closing panel's claimed undetected changes, MEASURED
    near8 85/85 (grok)   lt_ctl 85/85 (glm)   lt_rng 85/85 (kimi-k3:cloud)   c_endian 85/85 (glm)   c_bit1 85/85 (kimi CLI)
    rev_od1 85/85, istat_od1 85/85, time_od1 85/85 (codex)   time_land 85/85 (kimi-k3:cloud)
    lt_par 84/85 -- warm once red: deepseek's claimed escape REFUTED by measurement, as PRETABLE 4 predicted
  So nine of the ten panel claims were real undetected changes of the 85-row test; every one of the nine is detected by
  the 111-row test except time_land, which is disclosed.  The Opus seat measured its own twelve at 85/85 in
  ../opus_close_20260913/ (and showed each non-equivalent by a discriminator); all twelve are detected here.

THE INSTRUMENT AS SHIPPED DIFFERS FROM THE FROZEN ONE IN DOCSTRING TEXT ONLY -- stated, not assumed.  After the freeze,
the probe's docstring was edited: (1) five historical n/N quotes re-worded to name their era, because the gate pin's
stem became `crime_width' and check_score_claims.py now scans that docstring (the pin fix is in the #529 records); (2) the
CONTRACT's table list now names killtable4.  Verified: `diff' shows 5 changed docstring lines (+1 afterwards for the
table list); the ast of everything after the docstring hashes identically (md5 prefix 5da8e15ff1 for both), and both
carry 77 row() call sites.  The 111/111 on the fixed build is probe_first6_fix.out (7m54s) and the table's BASE run.

CHANNEL LINE: 57 of 57 predicted sets exact.  The one construction defect this table's writing found (repair 4's top4
anchor could not see acc4_210 -- the notice, not the value, is that cell's channel) was found WHILE WRITING THE
PREDICTION, before any run: the channel check doing its job at writing time.

DENOMINATOR for the second closing pass, cumulative over tables 1-4 (each by a single-cell or single-label change):
the refusal floor {1,2} x {R,W} at every observable label (REV 4 cells; CONTROL writes 2 cells with DOG, RESET and
ENDIANESS each written both ways at 2W plus all-ones refused writes at 1W and 2W; INTSTAT, INTMASK, TIME 4 cells each,
with all-ones refused stores; the default arm 4 cells + the far block); DOG and CONTROL reads by equivalent
fall-throughs; the answer of a refused read at REV, CONTROL, INTSTAT, INTMASK, DOG, TIME and the far block; the accept
cells at +0x00 (8R near end), +0x30, +0x210/+0x214 (anchored, and the notice for the 4R-high cell) and +0x278; a refused
store that lands (DOG, far block, either width); the announce's text, channel, presence, pre-set (4-byte access, a
second latch on bit 0) and re-arm (every accepted kind, the TIME arm); the latch keyed on width, address, direction,
direction x width, label, range and block; state carried across calls; the decline gated on HARDINT or prev_asserted;
the dispositions (revert, fault, exit0, return1).  NOT swept, disclosed in the probe header: interior accept slots
(acc8mid), an effect keyed on one unnamed offset (sft, wstore31, the class), a store landing only at TIME (time_land),
joint multi-axis predicates, a function-static latch (two machines per process), widths 3/5/6/7.
```

## QUESTIONS

1. **Is there a floor gap in the 111-row test?**  Name the smallest source edit to `dev_sgi_ip32.c` that undoes part of
   the fix's behaviour and still scores 111/111 -- as an exact edit -- with the row you expected to detect it and why it
   cannot.  A candidate inside the DISCLOSED list is not a gap unless you show the disclosure is wrong.
2. **Is the repair diff sound?**  Any new row whose oracle cannot vary under the change it names; any control that is not
   live; any timing assumption stated wrongly; any contract sentence the rows do not support.
3. **Which statement in this brief, in POSTTABLE 4, or in the probe header's CONTRACT / DISCLOSED text, is wrong?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
