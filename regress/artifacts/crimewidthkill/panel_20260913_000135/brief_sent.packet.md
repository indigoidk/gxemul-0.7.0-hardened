# PASS 1 (DESIGN) — `crimewidthkill`: an unsupported access width to the SGI IP32 CRIME controller ends the process

VERDICT LINE FIRST (`<option-set member>` + one clause), then the liveness token `CRIME_P1_20260913`.

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises,
not just the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a
premise from something this brief did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`** (`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`).  Other copies of GXemul
under the project root are pristine 2021 upstream and are NOT this fork.  **Scope your reading to `GXEMUL-SEC/src/`
and `GXEMUL-SEC/regress/*.py`.**  If you cannot read files that is expected — every fact you need is inlined; name any
premise you cannot settle from this packet.  Where a claim is arithmetic (an offset, a byte lane, a count),
ENUMERATE it rather than reasoning about it.

## THE DEFECT, MEASURED (rung 3, before any edit)

`src/devices/dev_sgi_ip32.c`, `DEVICE_ACCESS(crime)` — the IP32 memory and interrupt controller, registered
`DM_DEFAULT` at physical 0x14000000, length 0x280, backing store `uint64_t reg[0x280 / 8]` — sends every access whose
length is neither 8 nor 4 to `fatal("crime access len = %i!\n", len); exit(1);`.

**Measured** with a cold-debugger witness on the unmodified `-E sgi -e ip32` machine
(`regress/artifacts/crimewidthkill/crime_width_witness_20260913.py`, output `witness_committed.out`): **3/15,
CONTROL=OK**.  The controls pass: a RAM round trip (`live`); a 4-byte read of CRIME_REV's low half at KSEG1 0xb4000004
returns the model's revision 0x11 (`devsig`); its high half at 0xb4000000 reads 0 (`devsig hi`).  Then **each of
`lb`, `lbu`, `lh`, `lhu` (reads) and `sb`, `sh` (writes) ends the process with exit status 1 and the text
`crime access len = N!`**, and the RAM round trip that follows never runs.  One guest byte access to the machine's
interrupt controller terminates the emulator.

## SETTLED PREMISES (each checkable; please check them)

1. **`fatal()` prints and RETURNS; `exit(1)` is the terminating call.**
2. **A device callback returning 0 becomes a GUEST EXCEPTION on MIPS.**  `src/cpus/memory_rw.c`, verbatim:
   ```c
   if (res == 0)
           res = -1;
   /*  If accessing the memory mapped device failed, then return with an exception.  */
   if (res <= 0 && !no_exceptions) {
           debug("[ %s device '%s' addr %08lx failed ]\n", writeflag? "writing to" : "reading from", ...);
   #ifdef MEM_MIPS
           mips_cpu_exception(cpu, cache == CACHE_INSTRUCTION? EXCEPTION_IBE : EXCEPTION_DBE, 0, vaddr, 0, 0, 0, 0);
   #endif
           return MEMORY_ACCESS_FAILED;
   }
   ```
   So option 5 (FAULT, `return 0`) is AVAILABLE on this CPU: the guest takes a data bus error, and the `debug()` line
   prints when single-stepping.  `machine_sgi.c` installs `dev_unreadable` (whose whole access function is
   `return 0;`) ten times, because PROMs and NetBSD probe absent regions and rely on the failure.
3. **The nearest in-tree precedent, SAME MACHINE, SAME KIND OF GUARD:** `src/devices/dev_sgi_re.c` (the CRIME
   rendering engine at 0x15000000) had six width guards of the same shape.  Rounds #497/#499/#513 made them
   **latched declines that reach the common tail**, e.g.:
   ```c
   if (len != 8) {
           if (!(d->warned & SGIRE_W_TLBA_LEN)) {
                   d->warned |= SGIRE_W_TLBA_LEN;
                   fatal("[ sgi_re: unimplemented len=%i for CRIME_RE_TLB_A -- declined.  (once) ]\n", (int) len);
           }
   } else if (writeflag == MEM_WRITE) { ...
   ```
   and that round's detector records `return 0` as a DIFFERENT disposition (it "turns into a guest EXCEPTION_DBE"),
   rejected there.  **Whether that choice transfers here is a question, not a premise** — RE is a graphics engine, CRIME
   is the memory/interrupt controller.
4. **A second precedent in THIS file:** `DEVICE_ACCESS(macepci)` opens with
   `if (len != 4) fatal("[ macepci: unimplemented len %i ]\n", len);` — an UNLATCHED announce, then it proceeds with
   the access.  No termination.
5. **`struct crime_data` has no latch field today** (`reg[]`, `last_microseconds`, `irq`, `prev_asserted`, `use_fb`).
   The house idiom for a guest-drivable diagnostic is a per-instance N = 1 latch with `(once)` in the text.
6. **No CRIME hardware documentation is present locally** (`_scratchpad/*.pdf` has none).  What real CRIME does on a
   byte or halfword access — serve a byte lane, bus-error, or something else — is NOT established here.
7. **Two OTHER terminating calls sit in the same function, above the width guard**, keyed on the MACHINE'S RAM SIZE
   (`physical_ram_in_mb > 1024`, or not a multiple of the bank size) — set by `-M` at launch, not by the guest.  They
   are NOT this round's subject; say so if you disagree.

## THE FULL ENCLOSING FUNCTION (verbatim from the tree; every exit path and the common tail)

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
		fatal("crime access len = %i!\n", len);
		exit(1);
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

	d->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;
	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
		d->reg[CRIME_HARDINT / sizeof(uint64_t)]);

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

## THE OPTION SET (seven members; is there an eighth?)

1 DELETE the two lines and fall through · 2 DECLINE silently · 3 DECLINE + LATCHED ANNOUNCE (the RE precedent) ·
4 ACCEPT (the model already computes the value) · 5 FAULT (`return 0` → guest data bus error; available on MIPS) ·
6 BACKED ACCEPT (invent storage) · 7 IMPLEMENT (serve narrow accesses by byte lane from the 64-bit register array).

Notes a seat should check, not trust:
* **Member 1 is not the same as member 2 here**, because the `switch (relative_addr)` BELOW the width guard has side
  effects.  If a narrow access merely skips the store/load and falls through, the switch still runs.  Enumerate what a
  1- or 2-byte access could reach in it: `CRIME_REV` (0x000) redirects the PC when read from the PROM's cache-probe
  loop; `CRIME_CONTROL` (0x008) on a WRITE tests `idata & CRIME_CONTROL_HARD_RESET` and stops every CPU — is that bit
  within a halfword's `idata`?; `CRIME_INTSTAT`/`CRIME_INTMASK` call `crime_interrupt_reassert()`; `CRIME_TIME` updates
  the time; the default arm prints `debug()`.  Which of these should a refused access trigger?
* **Member 7 needs a byte-lane rule.**  The 4-byte arm treats `reg[]` as big-endian halves (`relative_addr & 4` picks
  the LOW half).  A byte rule would extend that — but is a byte read of a 64-bit control register meaningful on real
  CRIME, and does any guest do it?
* **Member 5 vs 3** is the design question the filing raised: FAULT is "a positive statement that the access could
  not be serviced", delivered as the error real hardware would give — IF real hardware refuses narrow accesses.  With
  no documentation (premise 6), what warrant can each member claim?

## QUESTIONS

1. **Which member, and why?**  Check the warrant against the tree: grep the fork for the idiom, and for how the IP32
   PROM path and guest drivers in this tree reach CRIME.  If you find a guest or PROM that issues a narrow CRIME access,
   that settles a great deal — say where.
2. **Does a refused access run the `switch`?**  For your chosen member, say exactly which lines a 1- and a 2-byte read
   and write execute, including the common tail (`preserved_CRIME_HARDINT` restore, the `INTSTAT` recompute, and the
   `memory_writemax64` on a read).
3. **"What is the SMALLEST EDIT that breaks your fix and still passes"** a detector you would write?  Name the rows you
   would need: the witness's survival and text rows, the accept cells (4 and 8, read and write), the switch
   side-effect cells for a refused access, the value a refused read returns (FAULT leaves the destination untouched; a
   decline writes 0 through the tail — a sentinel-seeded destination tells them apart), and a latch count if member 3.
4. **The premise audit.**  Which settled premise above is wrong or incomplete?

If, while verifying a claim, you found something ELSE — say so.


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
