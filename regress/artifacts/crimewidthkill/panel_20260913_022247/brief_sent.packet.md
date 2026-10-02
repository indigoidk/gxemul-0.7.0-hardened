# PASS 2 — `crimewidthkill` (#529): review the fix AND its detector.  Liveness token `CRIME_P2_20260913`.

VERDICT LINE FIRST (`SHIP` or `HOLD: <exact defect>`), then the token.

This is ordinary correctness review of an emulator device model and its regression test.  Please do not ratify:
check the PREMISES, not only the reasoning, and say which ones you could not check from this text.  Tree under review:
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\` only — any other `src/` you find is an unmodified 2021 upstream copy and will
give wrong line numbers.  File-reading seats: `src/devices/dev_sgi_ip32.c`, `regress/crime_width_probe.py`,
`src/cpus/memory_rw.c`, and `regress/artifacts/crimewidthkill/` are the relevant files.

## SETTLED PREMISES (recorded resolutions; re-stated because the questions depend on them)

* **The defect** (rung-3 witness, committed build 3/15, every row red): `DEVICE_ACCESS(crime)` in
  `src/devices/dev_sgi_ip32.c` answered an access of length other than 8 or 4 with
  `fatal("crime access len = %i!\n", len); exit(1);` — one guest `lb`, `lbu`, `lh`, `lhu`, `sb` or `sh` anywhere in the
  IP32 CRIME (physical 0x14000000) ended the emulator.
* **Pass 1 ruled member 3** of the option set (DECLINE + LATCHED `(once)` ANNOUNCE), placed AT the width arm, with a
  `goto` to the function's existing common tail — the shape `DEVICE_ACCESS(sgi_de)` (#498) already uses on the same
  machine.  Rejected: FAULT (`return 0` → the MIPS data bus error through `memory_rw.c`) because no local CRIME document
  warrants a bus error for narrow cycles, and because `fatal()` is not verbosity-gated while the FAULT path's only
  host trace is a `debug()` line that free-running suppresses; falling into the register switch, because the switch
  has guest-visible side effects on a refused width (measured by the pass-1 Opus seat: a halfword `0x0800` at
  `+0x08` stops every CPU through CRIME_CONTROL's HARD_RESET; a narrow read of CRIME_REV from pc `0xbfc051xx` sets
  pc = ra through the PROM-probe hack).
* **`goto crime_declined` vs `return 1` is EQUIVALENT on every channel**: `memory_rw.c` pre-zeroes a device read buffer
  (#95: `if (writeflag == MEM_READ) memset(data, 0, len);` immediately above `paddr -= mem->devices[i].baseaddr;`), so
  the tail's write of `odata = 0` and no write at all leave the same bytes.  The goto is kept for the house shape
  (#498) and because the tail also restores HARDINT and recomputes INTSTAT.
* **`fatal()` does not exit** (`src/core/debugmsg.c`, it has no early-out and no exit); the house latch idiom is N = 1
  per device instance with `(once)` in the message text.
* Side findings FILED, not in this round: `crimectllane` (the CRIME_CONTROL arm matches the exact label 0x08 with RAW
  idata, so a 32-bit write to the high half carries bit 11 into HARD_RESET, while NetBSD's 0x0c write does nothing),
  the unlatched `CRIME_CONTROL: unimplemented control` fatal (`floodclass`), the lazy `-M 48` exit at the first CRIME
  access (above the width arm), and `crimebankorder` (the bank loop writes contiguous offsets where `crimereg.h`
  interleaves CTRL1..CTRL7).

## THE FIX -- the diff, verbatim (`git diff`, working tree vs HEAD 9c91999)

```diff
diff --git a/src/devices/dev_sgi_ip32.c b/src/devices/dev_sgi_ip32.c
index fa96bf5..2c1036d 100644
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
@@ -288,8 +294,27 @@ DEVICE_ACCESS(crime)
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
+		 *  written at CRIME_CONTROL stop every CPU, and a narrow read of
+		 *  CRIME_REV from the PROM probe loop redirect the PC -- both
+		 *  measured.  It is not `return 0' either: that raises a guest
+		 *  bus error (EXCEPTION_DBE, cpus/memory_rw.c), and what real
+		 *  CRIME does on a narrow cycle is not documented here.
+		 */
+		if (!(d->warned & CRIME_W_LEN)) {
+			d->warned |= CRIME_W_LEN;
+			fatal("[ crime: unimplemented len=%i at 0x%x -- declined."
+			    "  (once) ]\n", (int) len, (int) relative_addr);
+		}
+		goto crime_declined;
 	}
 
 	switch (relative_addr) {
@@ -381,6 +406,9 @@ DEVICE_ACCESS(crime)
 		}
 	}
 
+ crime_declined:
+	/*  #529: a declined access jumps here, skipping the register switch,
+	    and is still answered.  */
 	d->reg[CRIME_HARDINT / sizeof(uint64_t)] = preserved_CRIME_HARDINT;
 	d->reg[CRIME_INTSTAT / sizeof(uint64_t)] =
 		(d->reg[CRIME_SOFTINT / sizeof(uint64_t)] |
```

## THE WHOLE ENCLOSING FUNCTION after the fix (every exit path and the common tail)

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
		 *  written at CRIME_CONTROL stop every CPU, and a narrow read of
		 *  CRIME_REV from the PROM probe loop redirect the PC -- both
		 *  measured.  It is not `return 0' either: that raises a guest
		 *  bus error (EXCEPTION_DBE, cpus/memory_rw.c), and what real
		 *  CRIME does on a narrow cycle is not documented here.
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

## THE DETECTOR -- `regress/crime_width_probe.py`, its header (CONTRACT and DISCLOSED) verbatim

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

CONTRACT -- the edits this detector is designed to catch (clause (e)):
  1. the kill reinstated verbatim, or any other host death at the width arm       <op> surv (all six widths), latch surv
  2. FAULT: the width arm returning 0 (a guest data bus error, EXCEPTION_DBE)      <op> pc, <op> exc, lb/lh/lbu/lhu v0
  3. the refused access FALLING INTO THE REGISTER SWITCH (the goto lost, or a
     narrower decline), at each width x direction cell:
        1-byte write  sb 0x01   -> +0x08   the CRIME_CONTROL arm's unimplemented-control fatal   sb08 msg
        2-byte write  sh 0x0800 -> +0x08   the CRIME_CONTROL arm's HARD_RESET stops every CPU    sh08 run, sh08 pc
        1-byte read   lb  at +0 from pc 0xbfc05180   the CRIME_REV PROM-probe hack sets pc = ra  lb rev pc
        2-byte read   lh  at +0 from pc 0xbfc05180                                               lh rev pc
     Each channel carries a LIVE control on an accepted width that shows it can vary:
        rev pc ctl (lw redirects), sw08 halts (sw 0x800 stops the CPUs), sw08 msg ctl (sw 0x01 prints the text).
     *** THE sh08 AND sw08 CHANNELS EXIST BECAUSE OF A SEPARATE DEFECT, `crimectllane' (filed): the switch matches
     CRIME_CONTROL by its exact label 0x08 and reads the RAW idata, so a 32-bit write to the high half, or a halfword at
     +0x08, carries bit 11 into HARD_RESET, while NetBSD's +0x0c write does nothing.  A round that fixes that lane
     removes or moves these channels and owes their re-derivation -- the sw08 controls will go red to say so. ***
  4. the latch removed or never set: five refused accesses in one session owe EXACTLY ONE announce      latch x5
  5. the ACCEPT SET shrunk at any single cell (the de-escalation clause: the deleted exit(1) used to announce this):
        8W acc8 st, 8R acc8 ld, 4R high half acc4 rhi, 4R low half acc4 rlo, 4W low half acc4 wlo, 4W high half acc4 whi
     on CRIME_DOG (0x030), a register the switch gives no side effect ("No warning.").
  6. the announce text: each width's own session prints `unimplemented len=N at 0xA -- declined.' exactly once   <op> said

DISCLOSED, not rowed:
  * `goto crime_declined' -> `return 1' is EQUIVALENT on every channel: memory_rw pre-zeroes a device read buffer
    (#95, `if (writeflag == MEM_READ) memset(data, 0, len);' in src/cpus/memory_rw.c), so the tail's write of odata = 0
    and no write at all leave the same bytes.  Measured by the pass-1 Opus seat (opus_pass1_20260913/out/rows_return1.out).
  * a refused store's READBACK is non-varying across every candidate (the store is dropped by decline, FAULT and the
    switch's default arm alike -- measured 0xbadcafe unchanged in all of rows_*.out), so it carries no row.
  * the INTSTAT/INTMASK (reassert), TIME (update) and HARDINT (restore) cells a fall-through could reach: effects are
    idempotent or overwritten by the tail, and no observable here separates them.
  * FREE-RUNNING: fatal() is not verbosity-gated, so the announce prints free-running too (measured by the Opus seat);
    this detector steps only.
  * widths 3, 5, 6, 7 (no MIPS load/store issues them); the unaligned-pair instructions (lwl/lwr/swl/swr, ldl/ldr) are
    not rowed.  The RAM-size checks ABOVE the width arm (`-M 48' exits at the first CRIME access) are filed, not here.

Sentinel: CRIMEP_DONE (plus CRIMEP_RESULT=n/N and CRIMEP_CONTROL=OK|FAIL).

```

## The detector on the fixed build (40/40; HEAD scores 11/40 with every control green)

```
CRIME WIDTH PROBE (#529) -- rung 3, unmodified -E sgi -e ip32   binary=/mnt/c/DocumentNoSnc/CC/GXEMUL/build/gxemul  label=FIX
row              got                  want                 note                                     
live             0x12345678           0x12345678           LIVENESS: RAM round trip, same apparatus ok
devsig           0x11                 0x11                 CRIME_REV low half = rev 0x11: a device  ok
devsig hi        0x0                  0x0                  CRIME_REV high half reads 0              ok
rev pc ctl       0x80004000           0x80004000           CONTROL: lw CRIME_REV from 0xbfc051xx -> ra ok
sw08 halts       0xdeadbeef           0xdeadbeef           CONTROL: sw 0x800 +0x08 stops CPUs (crimectllane) ok
sw08 msg ctl     1                    1                    CONTROL: sw 0x01 +0x08 prints the text   ok
acc8 st+ld       0x1122334455667788   0x1122334455667788   8W then 8R at CRIME_DOG                  ok
acc4 rhi         0x11223344           0x11223344           4R of the high half (+0x30)              ok
acc4 rlo         0x55667788           0x55667788           4R of the low half (+0x34)               ok
acc4 wlo         0x112233440badcafe   0x112233440badcafe   4W low half lands, high half kept        ok
acc4 whi         0xdefaced0badcafe    0xdefaced0badcafe    4W high half lands, low half kept        ok
lb v0            0x0                  0x0                  declined read answers 0 (dest seeded 0xdeadbeef) ok
lb pc            0x80001004           0x80001004           pc advances, no vector                   ok
lb exc           0                    0                    cause.ExcCode 0 (a bus error is 7)       ok
lb said          1                    1                    own announce, len=1 at 0x7, once         ok
lb surv          0x12345678           0x12345678           host survives, then a RAM trip           ok
lh v0            0x0                  0x0                  declined read answers 0 (dest seeded 0xdeadbeef) ok
lh pc            0x80001004           0x80001004           pc advances, no vector                   ok
lh exc           0                    0                    cause.ExcCode 0 (a bus error is 7)       ok
lh said          1                    1                    own announce, len=2 at 0x6, once         ok
lh surv          0x12345678           0x12345678           host survives, then a RAM trip           ok
lbu v0           0x0                  0x0                  declined read answers 0 (dest seeded 0xdeadbeef) ok
lbu surv         0x12345678           0x12345678           host survives, then a RAM trip           ok
lhu v0           0x0                  0x0                  declined read answers 0 (dest seeded 0xdeadbeef) ok
lhu surv         0x12345678           0x12345678           host survives, then a RAM trip           ok
sb pc            0x80001004           0x80001004           pc advances, no vector                   ok
sb exc           0                    0                    cause.ExcCode 0 (a bus error is 7)       ok
sb said          1                    1                    own announce, len=1 at 0x1f, once        ok
sb surv          0x12345678           0x12345678           host survives, then a RAM trip           ok
sh pc            0x80001004           0x80001004           pc advances, no vector                   ok
sh exc           0                    0                    cause.ExcCode 0 (a bus error is 7)       ok
sh said          1                    1                    own announce, len=2 at 0x1e, once        ok
sh surv          0x12345678           0x12345678           host survives, then a RAM trip           ok
sh08 pc          0x80001004           0x80001004           2W sh 0x800 +0x08: pc advances           ok
sh08 run         0x12345678           0x12345678           2W: CPUs NOT stopped (RAM trip runs)     ok
sb08 msg         0                    0                    1W sb 0x01 +0x08: no CONTROL text        ok
lb rev pc        0xbfc05184           0xbfc05184           1R at CRIME_REV from 0xbfc05180: pc NOT ra ok
lh rev pc        0xbfc05184           0xbfc05184           2R at CRIME_REV from 0xbfc05180: pc NOT ra ok
latch x5         1                    1                    5 refused accesses -> one (once)         ok
latch surv       0x12345678           0x12345678           host survives all five                   ok

FAILING: 
CRIMEP_RESULT=40/40
CRIMEP_CONTROL=OK
CRIMEP_DONE
```

## KILL TABLE 1 -- the mutants, as the edits applied (`mutants529.py`)

```python
#!/usr/bin/env python3
"""mutants529.py NAME SRC DST -- write the #529 post-fix dev_sgi_ip32.c with one mutant applied.

Every find-text must occur EXACTLY ONCE in the source, or the script refuses (a mutant whose text is not found is a
FAIL, never a silent no-op -- so each mutant also pins the presence of what it edits).  Baseline = the #529 working
set (GXEMUL-SEC/src/devices/dev_sgi_ip32.c with the fix), never HEAD.
"""
import sys

GOTO = "\t\tgoto crime_declined;\n\t}\n\n\tswitch (relative_addr) {"
ARM8 = "\tif (len == 8) {\n\t\tif (writeflag == MEM_WRITE)\n\t\t\td->reg[relative_addr / 8] = idata;"
ARM4 = "\t} else if (len == 4) {\n\t\tif (writeflag == MEM_WRITE) {"
LATCH_SET = "\t\t\td->warned |= CRIME_W_LEN;\n"
LATCH_TEST = "\t\tif (!(d->warned & CRIME_W_LEN)) {"
FMT_ARGS = "(int) len, (int) relative_addr);"
DECL_BODY = ("\t\tif (!(d->warned & CRIME_W_LEN)) {\n"
             "\t\t\td->warned |= CRIME_W_LEN;\n"
             "\t\t\tfatal(\"[ crime: unimplemented len=%i at 0x%x -- declined.\"\n"
             "\t\t\t    \"  (once) ]\\n\", (int) len, (int) relative_addr);\n"
             "\t\t}\n"
             "\t\tgoto crime_declined;\n")


def g(repl):
    return GOTO.replace("goto crime_declined;", repl, 1)


def a4(cond):
    return ARM4.replace("len == 4", "len == 4 && " + cond, 1)


M = {
    "base":     [],
    # floor (b): the removed kill, verbatim, at the width arm
    "revert":   [(DECL_BODY, "\t\tfatal(\"crime access len = %i!\\n\", len);\n\t\texit(1);\n")],
    # member 5: FAULT
    "fault":    [(GOTO, g("return 0;"))],
    # death with status 0 after the announce (the exit0oracle shape)
    "exit0":    [(GOTO, g("exit(0);"))],
    # fall-through into the register switch, whole and per cell
    "fallsw":   [(GOTO, g("/* goto crime_declined; */"))],
    "len1only": [(GOTO, g("if (len == 1) goto crime_declined;"))],
    "len2only": [(GOTO, g("if (len == 2) goto crime_declined;"))],
    "readonly": [(GOTO, g("if (writeflag == MEM_READ) goto crime_declined;"))],
    "wronly":   [(GOTO, g("if (writeflag == MEM_WRITE) goto crime_declined;"))],
    # disclosed EQUIVALENT (memory_rw pre-zeroes the read buffer, #95)
    "return1":  [(GOTO, g("return 1;"))],
    # latch
    "nolatch":  [(LATCH_SET, "")],
    "latchinv": [(LATCH_TEST, "\t\tif (d->warned & CRIME_W_LEN) {")],
    # announce text (contract 6)
    "fmtswap":  [(FMT_ARGS, "(int) relative_addr, (int) len);")],
    # accept-set growth, one cell each (de-escalation clause)
    "acc8w":    [(ARM8, ARM8.replace("len == 8", "len == 8 && writeflag == MEM_READ", 1))],
    "acc8r":    [(ARM8, ARM8.replace("len == 8", "len == 8 && writeflag == MEM_WRITE", 1))],
    "acc4wlo":  [(ARM4, a4("!(writeflag == MEM_WRITE && (relative_addr & 4))"))],
    "acc4whi":  [(ARM4, a4("!(writeflag == MEM_WRITE && !(relative_addr & 4))"))],
    "acc4rlo":  [(ARM4, a4("!(writeflag == MEM_READ && (relative_addr & 4))"))],
    "acc4rhi":  [(ARM4, a4("!(writeflag == MEM_READ && !(relative_addr & 4))"))],
}

if __name__ == "__main__":
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    if name == "list":
        print(" ".join(M))
        sys.exit(0)
    s = open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n))
            sys.exit(2)
        s = s.replace(find, repl, 1)
    open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
```

## KILL TABLE 1 -- results (`POSTTABLE.out`)

```
POSTTABLE -- #529 crimewidthkill kill table 1, written AFTER the table (PRETABLE.out predates it by mtime)
Driver kill529.run-*.sh (frozen copy of kill529.sh); summary table1.out; per-mutant logs/probe_<m>.raw (each ends
CRIMEP_DONE -- checked) and logs/<m>.diff; build logs builds/.  Instrument: crime_width_probe.table1.py, md5
a338b7ae..., byte-identical to regress/crime_width_probe.py as shipped (logs/INSTRUMENT.md5).  Scratch clone
/tmp/gxopuscrime, baseline = the #529 working set (BASELINE_CMP CLEAN, dev_sgi_ip32.c md5 5919a5a7...), rebuilt in
the clone before mutant 1; restored afterwards: cmp clean, binary -nt source, restored == base byte-identical,
sentinel removed.  Every mutant built with rc 0 and a fresh object; none byte-identical to base.

SCORES (40 rows)
    base      40/40  CONTROL=OK
    revert    11/40  CONTROL=OK   the removed kill, verbatim (floor b)
    fault     25/40  CONTROL=OK   return 0 -> EXCEPTION_DBE
    exit0     17/40  CONTROL=OK   exit(0) after the announce
    fallsw    35/40  CONTROL=OK   goto removed: every refused width falls into the switch
    len1only  37/40  CONTROL=OK   goto only for len 1 (2-byte cells fall in)
    len2only  38/40  CONTROL=OK   goto only for len 2 (1-byte cells fall in)
    readonly  37/40  CONTROL=OK   goto only for reads (write cells fall in)
    wronly    38/40  CONTROL=OK   goto only for writes (read cells fall in)
    return1   40/40  CONTROL=OK   PREDICTED EQUIVALENT, measured equivalent (memory_rw pre-zero, #95) -- disclosed
    nolatch   39/40  CONTROL=OK   latch never set
    latchinv  35/40  CONTROL=OK   latch test inverted
    fmtswap   36/40  CONTROL=OK   announce's len/addr swapped
    acc8w     36/40  CONTROL=OK   8W refused
    acc8r     37/40  CONTROL=OK   8R refused
    acc4wlo   38/40  CONTROL=OK   4W low half refused
    acc4whi   37/40  CONTROL=FAIL 4W high half refused
    acc4rlo   38/40  CONTROL=FAIL 4R low half refused
    acc4rhi   38/40  CONTROL=FAIL 4R high half refused
  18 of 18 non-equivalent mutants KILLED; the one equivalent is the one predicted.

ROWS EACH MUTANT REDDENED vs PRETABLE section 4
    revert    all 29 refusal rows                                                        = predicted
    fault     <op> v0/pc/exc x (lb lh lbu lhu sb sh) + sh08 pc + lb/lh rev pc (pc at the vector)   = predicted (+ the
              pc-only rows of the side-effect sessions, which see the vector too)
    exit0     every surv/v0/pc/exc row + sh08 pc/run + rev pc + latch surv; <op> said and latch x5 GREEN
              (announce printed, EOF, status 0)                                          = predicted
    fallsw    sh08 pc, sh08 run, sb08 msg, lb rev pc, lh rev pc                          = predicted, exactly
    len1only  sh08 pc, sh08 run, lh rev pc                                               = predicted, exactly
    len2only  sb08 msg, lb rev pc                                                        = predicted, exactly
    readonly  sh08 pc, sh08 run, sb08 msg                                                = predicted, exactly
    wronly    lb rev pc, lh rev pc                                                       = predicted, exactly
    nolatch   latch x5                                                                   = predicted
    latchinv  <op> said x4, latch x5                                                     = predicted
    fmtswap   <op> said x4                                                               = predicted
    acc8r     acc8 st+ld, acc4 wlo, acc4 whi                                             = predicted
    acc4wlo   acc4 wlo, acc4 whi                                                         = predicted
    acc4whi   acc4 whi  + controls sw08 halts, sw08 msg ctl                              see (b)
    acc4rlo   acc4 rlo  + control devsig                                                 see (b)
    acc4rhi   acc4 rhi  + control rev pc ctl                                             see (b)
    acc8w     acc8 st+ld, acc4 rhi, acc4 rlo, acc4 wlo                                   *** PREDICTION WRONG, see (a)

(a) THE CHANNEL LINE'S OWN CLAIM, checked as PRETABLE promised.  "A row's channel under its mutant is knowable at
    writing time" held for 17 of 18 non-equivalent mutants, ROW SET EXACT.  For acc8w I predicted {acc8, rhi, wlo,
    whi} and measured {acc8, rhi, RLO, wlo}: the accept session is SEQUENTIAL, so with the sd refused the register
    stays 0, the lw of the low half reads 0 (rlo red -- I had missed it), and the later sw of the high half on top of
    the earlier sw of the low half REBUILDS the full word the whi row wants (whi green -- I had predicted it red).
    The kill is unaffected (four rows), and every accept cell still reds under its OWN single-cell mutant.  The
    lesson is narrow and real: in a session where later accesses write the same register, a row's value depends on
    every earlier access, so its channel under a mutant must be traced through the whole sequence, not read off the
    one access it names.

(b) THE CONTROLS THAT REDDENED ARE ACCEPT-CELL COVERAGE BY CONSTRUCTION, NOT CONTROL DEFECTS.  sw08 halts / sw08 msg
    ctl are 4-byte writes to the HIGH half (+0x08), devsig is a 4-byte read of the LOW half (+0x04), rev pc ctl is a
    4-byte read of the HIGH half (+0x00); refusing that cell refuses the control's own access.  So CONTROL=FAIL under
    those three mutants is the controls doing a second job.  No mutant reddened a control through any other route.
    Weak spot disclosed: `devsig hi' wants 0x0, which a refused read also returns, so it cannot vary under acc4rhi --
    it is a device-reads-0 row, not a discriminating control; acc4 rhi and rev pc ctl carry that cell.

EQUIVALENCE, per the rule that a mutant that will not die is a result: return1 is the only survivor and it is the
predicted one, with its warrant named (memory_rw.c's #95 pre-zero); an edit to that warrant re-runs this measurement.

DENOMINATOR for the pass-2 closing question: cells swept -- refusal {1,2} x {R,W} each by a confined fall-through
(len1only, len2only, readonly, wronly) plus the whole fall-through (fallsw); accept {8W, 8R, 4W lo, 4W hi, 4R lo,
4R hi} each by its single-cell growth mutant; the latch (nolatch, latchinv); the text (fmtswap); the dispositions
(revert, fault, exit0, return1).  NOT swept: address-conditioned fall-throughs (a goto keyed on relative_addr), which
reach the switch only at the labels a refused access happens to name -- owed as a pass-2 question, not yet measured.
```

## QUESTIONS

1. **The fix.**  Read the whole function above, every exit path.  Does the declined access do exactly what the comment
   says — skip the switch, answer a read 0, drop a write, advance the PC with no exception, announce once per device
   instance?  Is anything in the PRELUDE (the register refreshes and the RAM-size checks that run before the width arm)
   a problem for a declined access that the placement at the width arm leaves in?  Is `int warned` + `CRIME_W_LEN` the
   house idiom, and is there any other writer of `warned`?
2. **The smallest edit that breaks the fix and still passes all 40 rows.**  Name it as an exact source edit to
   `dev_sgi_ip32.c` (not a label), and say which row you expected to catch it and why that row cannot.  The kill table
   above lists the 19 edits already measured — find one it does not cover.  In particular: the four refusal cells
   {1-byte, 2-byte} x {read, write} are each rowed through ONE switch side effect (CRIME_CONTROL for writes, CRIME_REV's
   PROM-probe hack for reads); a fall-through conditioned on the ADDRESS (e.g. `if (relative_addr != CRIME_CONTROL)
   goto crime_declined;`) — which cells does it reach and which rows see it?
3. **The vacuity floor and the contract.**  Is each accept cell (8W, 8R, 4R high/low, 4W high/low) pinned by a row that
   reds under its OWN single-cell growth mutant, and is each refusal cell pinned by a row that reds under a fall-through
   confined to that cell?  Is anything in the CONTRACT claimed without a measured kill, or anything in DISCLOSED that the
   floor actually owes a row for?
4. **Records.**  Is anything in the comment text of the fix or the probe header false, or stated more strongly than
   the measurements support?
5. **WHICH OF MY STATEMENTS IN THIS BRIEF IS WRONG?**


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
