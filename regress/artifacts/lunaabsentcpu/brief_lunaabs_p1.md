# PASS-1 DESIGN BRIEF -- `lunaabsentcpu` (HIGH, MEASURED): dev_luna88k.c delivers an interrupt to a CPU slot that was never connected, and the emulator process dies.  Tree `GXEMUL-SEC/src/`, HEAD `83df95c` (dev_luna88k.c last touched by cf4b083 / #438).  2026-09-05, ~21:45.

## CONTEXT AND VOCABULARY
An ordinary correctness review of an open-source machine emulator's board-glue device model (GXemul 0.7.0, hardened fork):
`GXEMUL-SEC/src/devices/dev_luna88k.c`, the LUNA-88K interrupt-mask / software-interrupt registers.  The "guest" is the operating
system running inside the emulator (OpenBSD/luna88k boots on the project's m88k rig).  Plain engineering vocabulary: "the emulator
process dies", "a NULL function pointer is called", "a declined store".  Read the project's own records NARROWLY (grep anchors,
a few lines of context; never whole CHANGELOG blocks or the ledger) and paraphrase in neutral terms.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not just the
derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from something this
brief did NOT give it is worth more than a seat that agrees.
**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.**  There are THREE pristine-2021-upstream copies of GXemul under the project root
(`./src/` and two under `_archive/audit-results-*/builds/`).  They are NOT this fork.  If your line numbers disagree with the
anchors here you are reading one of them -- say so rather than reconciling.
**If you cannot read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from this
packet rather than guessing at it.
**Where this brief states an ARITHMETIC claim -- a slot index, a bit position, a count -- ENUMERATE it rather than reasoning
about it.**  Walk the values.  **And ENUMERATE THE RIGHT DOMAIN -- a domain is itself a premise.**  Ask what the PRODUCER (a guest
store's address and value; the configured CPU count) can actually emit.
**VERDICT LINE FIRST**, so your answer survives truncation.  Cite by grep anchor (`grep -nF '<anchor>' <file>`), not by line number.

## 0. HAS THIS ROUND ALREADY SHIPPED?  (two commands, run 21:4x)
    git log -1 -- src/devices/dev_luna88k.c      -> cf4b083 2026-08-19 #438 exitsweep: a guest store to INT_ST_MASK0-3 ended the emulator process
    grep -c lunaabsentcpu CHANGELOG.md            -> 0
    ls regress/luna*                             -> regress/luna_intmask_probe.py (the #438 detector) only
So: NOT shipped.  #438 de-fatalised the low-bits guard in the SAME store arm and shipped `luna_intmask_probe.py`; that probe's D4
row stores 0x84000100 to INT_ST_MASK1 -- bits 31, 26 and 8, so bit 26 is SET and slot 1 stays ARMED for the rest of that session.
It could not see this defect only because a cold debugger has nothing pending and the probe never stores SOFT_INT1.  (The first
draft of this brief said 'bit 26 CLEAR'; the batch-7 adjudication caught it.)  COROLLARY, from the same adjudication: after ONE
arming store, the NEXT device interrupt of any kind (the clock is line 6 -> bit 31; sio line 5 -> bit 30) kills the host on a
running guest -- the SOFT_INT1 route is merely the deterministic, synchronous form.
BATCH-7 ADJUDICATION RULING ON THE OPTION SET (Fable 5.1, ~22:40, before this panel): (a) ALONE -- bound the loop to `d->ncpus`
captured at DEVINIT; (b) is REJECTED for this round (unsourced board-model claim, changes guest-visible readback, reddens the
shipped es438 rows D4/E2) and filed as the question `lunaabsentmaskdecl`; (c) fabricates plumbing; a NULL check guards the
symptom.  This panel is asked to CHECK that ruling, not ratify it (Q3).  Detector shape from the same ruling: W1 kill row +
connected-slot control + a `-n 2` ACCEPT row whose channel is cpu 1 ASSERTING (irq_asserted or the vector entry), not
survival; PRETABLE mutants `cpu <= d->ncpus`, `ncpus` never assigned, `ncpus = 1` hardcoded; plus MASK2/MASK3 readback rows.

## 1. THE DEFECT, MEASURED (rung 3)
Witness `_scratchpad/lunaabs/luna_absentcpu_probe.py` (copy as run: `regress/artifacts/lunaabsentcpu/luna_absentcpu_probe.asrun.py`;
log `regress/artifacts/lunaabsentcpu/witness_head_20260905_2130.out`), ONE cold-debugger session on the COMMITTED UNMODIFIED
`-e luna-88k` (default ONE cpu) with the committed rig image, HEAD binary (`/tmp/gxopus501p4`, its dev_luna88k.c cmp-equal to
`git show HEAD:src/devices/dev_luna88k.c`), real `st`/`ld` guest instructions through real address decode -- each planted word
disassembled by the emulator and its text checked before it was stepped:

    LUNAABS_ROW=live    RESULT=OK     C1 RAM write/read through the same decode: 0x12345678
    LUNAABS_ROW=devsig  RESULT=OK     C2 st 0xfc000000 -> INT_ST_MASK0 (0x65000000); ld back = 0x00fc0000 (the handler's own >>8; RAM cannot produce it)
    LUNAABS_ROW=slot0   RESULT=OK     A1 ATTRIBUTION: MASK0 holds 0xfc000000 (bit 26 set); st 1 -> SOFT_INT0 (0x69000000) -> slot 0 asserts to the CONNECTED cpu 0: SURVIVES; ld SOFT_INT0 = 1 (read clears it)
    LUNAABS_ROW=mask1   RESULT=OK     A2 st 0xfc000000 -> INT_ST_MASK1 (0x65000004) ALONE: survives; ld back = 0x00fc0000 (stored AS-IS for the absent slot)
    LUNAABS_ROW=soft1   RESULT=HALT   W1 st 1 -> SOFT_INT1 (0x69000004): HOST DIED, signal 11 (SIGSEGV), no diagnostic printed
    LUNA_ABSENTCPU_WITNESS=PRE_FIX_SYMPTOM   LUNAABS_RESULT=4/5   PROBE_WALL=1.4s

Two ordinary guest word stores, from supervisor mode (the debugger's default), on the machine this project boots.  Not a
`fatal()`+`exit(1)` and not a graceful `running = 0`: a memory fault in the emulator process.

## 2. SETTLED PREMISES, RE-INLINED (each is a QUESTION if you can check it)
* **The loop.**  `reassert_interrupts()` (anchor `static void reassert_interrupts`) walks `for (cpu = 0; cpu < MAX_CPUS; cpu++)`
  with `#define MAX_CPUS 4`; per slot: `status = d->interrupt_status` (MACHINE-WIDE: set/cleared by the six shared device lines
  via `luna88k_interrupt_assert/deassert`, `1 << (line + 25)`, lines 1..6 -> bits 26..31), `enable = d->interrupt_enable[cpu]`,
  `if (d->software_interrupt_status[cpu]) status |= (1 << 26)`, then `if (status & enable) { if (!d->irqActive[cpu])
  INTERRUPT_ASSERT(d->cpu_irq[cpu]); d->irqActive[cpu] = 1; } else { if (d->irqActive[cpu]) INTERRUPT_DEASSERT(d->cpu_irq[cpu]);
  d->irqActive[cpu] = 0; }`.
* **The macro.**  `src/include/interrupt.h`: `#define INTERRUPT_ASSERT(istruct) (istruct).interrupt_assert(&(istruct))` -- a
  direct call through the struct's function pointer, no NULL check.  Same for DEASSERT.
* **The connection.**  `DEVINIT(luna88k)`: `memset(d, 0, sizeof(struct luna88k_data))`; `INTERRUPT_CONNECT(devinit->interrupt_path,
  d->cpu_irq[0])`; then, under the comment `// HACK for trying out CPUs 1, 2 and 3`, `if (devinit->machine->ncpus >= 2)
  INTERRUPT_CONNECT("machine[0].cpu[1]", d->cpu_irq[1]);` and likewise `>= 3` / `>= 4` for slots 2 and 3.  So on a one-cpu
  machine `cpu_irq[1..3].interrupt_assert` are NULL.  Default cpu count: `m->ncpus = 1;` (emul.c, per the batch-7 reviewer --
  CHECK); the rig boots with the default.
* **The store arms** (anchor `case INT_ST_MASK0:`; the four labels INT_ST_MASK0..3 = 0x65000000/04/08/0c share one arm):
  `cpunr = (addr - INT_ST_MASK0) / 4;` -- so cpunr is 0..3 from the ADDRESS, never compared with `ncpus` -- then on WRITE the
  #438 low-bits latch (`if ((idata & 0x03ffffff) != 0)` ... `fatal(... "stored as-is (reported once per cpu)")` first time,
  `debug()` after), then UNCONDITIONALLY `d->interrupt_enable[cpunr] = idata; reassert_interrupts(d);`.  On READ:
  `odata = currentMask >> 8; odata |= (highestCurrentStatus << 29)` where highestCurrentStatus scans bits 26..31 of
  `interrupt_status & currentMask`.  The SOFT_INT0..3 arm (anchor `case SOFT_INT0:`, 0x69000000/04/08/0c): `cpunr = (addr -
  SOFT_INT0) / 4;` WRITE `d->software_interrupt_status[cpunr] = idata;` READ returns it and clears it; both then
  `reassert_interrupts(d);`.  Neither arm checks `cpunr < ncpus`.
* **The other multi-cpu arm** in the same switch, `case RESET_CPU_ALL:` (0x6d000010), DOES bound by ncpus: `for (int i = 0;
  i < cpu->machine->ncpus; ++i) cpu->machine->cpus[i]->running = 0;`.
* **The common tail** of `DEVICE_ACCESS(luna88k)` (the function runs from `DEVICE_ACCESS(luna88k)` to the closing brace ~380
  lines later; the switch's `default:` prints `unimplemented %i-bit WRITE/READ`, then `// Stop the emulation immediately.
  cpu->running = 0; return 0;`): after the switch, `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata); return 1;`.
  Every implemented arm reaches that tail with `break`.  (The `default:`'s graceful stop is a SEPARATE class and out of scope
  here -- say if you think it is already filed.)
* **The house idiom for a guest-supplied CPU index**: `dev_mp.c`, anchor `which_cpu >= cpu->machine->ncpus`: *"The CPU index
  comes from the guest; reject out-of-range values instead of indexing d->cpus[] out of bounds."* -> `break` (silent decline,
  no latch).  `dev_bebox.c`, anchor `i >= machine->ncpus`: a DEVINIT-time `fatal()`+`exit(1)` for a MISSING cpu (init-time,
  not guest-drivable).  `dev_luna88k.c`'s own `add_cmmu_for_cpu`: `if (cpunr >= devinit->machine->ncpus) return;`.
* **The de-fatalisation option set** (carrier): DELETE / DECLINE (silent) / DECLINE + LATCHED ANNOUNCE / ACCEPT / FAULT /
  BACKED ACCEPT, plus the scope axis (a decline skips every remaining side effect and still answers through the common exit).
  The house latch spelling is `(once)` (deriver: `grep -o '(once)' src/devices/*.c | wc -l`, 25 on 2026-08-31).  #438's own
  latch in this arm says "(reported once per cpu)".
* **What OpenBSD does**: unknown to this brief.  The rig boots to login with the default one cpu and the emulator has never
  died there, so the kernel evidently does not arm slot 1 with a pending bit -- whether it WRITES MASK1..3 at all (zero, or
  a real mask) is NOT settled; a file-reading seat may check `_guest-src-openbsd22/` (OpenBSD 2.2 -- probably no luna88k) and
  should say what it found or that it is absent.

## 3. THE ENCLOSING FUNCTIONS (verbatim, so any edit is run against real control flow)
```c
static void reassert_interrupts(struct luna88k_data *d)
{
	int cpu;

	for (cpu = 0; cpu < MAX_CPUS; cpu++) {
		// General interrupt status is for the entire machine,
		// but the Software interrupts (IPIs) are per CPU.
		uint32_t status = d->interrupt_status;
		uint32_t enable = d->interrupt_enable[cpu];

		if (d->software_interrupt_status[cpu])
			status |= (1 << 26);

	        if (status & enable) {
			if (!d->irqActive[cpu])
		                INTERRUPT_ASSERT(d->cpu_irq[cpu]);

			d->irqActive[cpu] = 1;
		} else {
			if (d->irqActive[cpu])
		                INTERRUPT_DEASSERT(d->cpu_irq[cpu]);

			d->irqActive[cpu] = 0;
		}
	}
}
```
The INT_ST_MASK arm (inside `DEVICE_ACCESS(luna88k)`'s `switch (addr)`; comments condensed, code verbatim):
```c
	case INT_ST_MASK0:	/*  0x65000000: Interrupt status CPU 0.  */
	case INT_ST_MASK1:	/*  0x65000004: Interrupt status CPU 1.  */
	case INT_ST_MASK2:	/*  0x65000008: Interrupt status CPU 2.  */
	case INT_ST_MASK3:	/*  0x6500000c: Interrupt status CPU 3.  */
		cpunr = (addr - INT_ST_MASK0) / 4;
		if (writeflag == MEM_WRITE) {
			if ((idata & 0x03ffffff) != 0x00000000) {
				/* #438 comment block: STORE AS-IS ... The latch is MANDATORY as a capability bound ... */
				if (!d->intmask_lowbits_reported[cpunr]) {
					d->intmask_lowbits_reported[cpunr] = 1;
					fatal("[ luna88k: INT_ST_MASK%i: unimplemented low bits in write 0x%08x; stored as-is (reported once per cpu) ]\n", cpunr, (uint32_t)idata);
				} else {
					debug("[ luna88k: INT_ST_MASK%i: unimplemented low bits in write 0x%08x ]\n", cpunr, (uint32_t)idata);
				}
			}
			d->interrupt_enable[cpunr] = idata;
			reassert_interrupts(d);
		} else {
			uint32_t currentMask = d->interrupt_enable[cpunr];
			uint32_t status = d->interrupt_status & currentMask;
			int highestCurrentStatus = 0;
			odata = currentMask >> 8;
			for (int i = 1; i <= 6; ++i) {
				int m = 1 << (25 + i);
				if (status & m)
					highestCurrentStatus = i;
			}
			odata |= (highestCurrentStatus << 29);
		}
		break;

	case SOFT_INT0:		/*  0x69000000: Software Interrupt status CPU 0.  */
	case SOFT_INT1:		/*  0x69000004: Software Interrupt status CPU 1.  */
	case SOFT_INT2:		/*  0x69000008: Software Interrupt status CPU 2.  */
	case SOFT_INT3:		/*  0x6900000c: Software Interrupt status CPU 3.  */
		cpunr = (addr - SOFT_INT0) / 4;
		if (writeflag == MEM_WRITE) {
			d->software_interrupt_status[cpunr] = idata;
		} else {
			// Reading status clears it.
			odata = d->software_interrupt_status[cpunr];
			d->software_interrupt_status[cpunr] = 0;
		}
		reassert_interrupts(d);
		break;
```
Common tail of the access function: `if (writeflag == MEM_READ) memory_writemax64(cpu, data, len, odata); return 1;`
DEVINIT connection block (verbatim):
```c
	INTERRUPT_CONNECT(devinit->interrupt_path, d->cpu_irq[0]);

	// HACK for trying out CPUs 1, 2 and 3. TODO: Base on devinit->interrupt_path instead.
	if (devinit->machine->ncpus >= 2)
		INTERRUPT_CONNECT("machine[0].cpu[1]", d->cpu_irq[1]);
	if (devinit->machine->ncpus >= 3)
		INTERRUPT_CONNECT("machine[0].cpu[2]", d->cpu_irq[2]);
	if (devinit->machine->ncpus >= 4)
		INTERRUPT_CONNECT("machine[0].cpu[3]", d->cpu_irq[3]);
```
Also relevant: is `d->machine` / `cpu->machine->ncpus` reachable from `reassert_interrupts()`?  It receives only `d`; the
struct has no `machine` pointer today (CHECK: `grep -n 'struct machine' src/devices/dev_luna88k.c`).  Option (a) therefore
needs either a stored `ncpus` in the device struct (set at DEVINIT) or a pointer.

## 4. THE OPTION SET (is there a member this brief did not name?  Grep the fork for the idiom.)
(a) **Bound the loop**: store `d->ncpus = devinit->machine->ncpus` at DEVINIT and walk `cpu < d->ncpus` (or `cpu < MAX_CPUS &&
    d->cpu_irq[cpu].interrupt_assert != NULL`).  Stores to absent slots still land and read back; they just never deliver.
(b) **Decline the store** to MASK/SOFT slots `>= ncpus` (house idiom dev_mp.c: silent `break`; or with a `(once)` latch per
    slot, the #438 shape) -- storing nothing, so a readback of an absent slot returns 0 (as it does today before any store).
    Scope: skip the store AND the reassert; still answer through the common tail (a read of an absent slot returns 0).
(c) **Connect the absent slots to a no-op interrupt** (a static `struct interrupt` whose assert/deassert do nothing) --
    the tree has no such helper today (CHECK: `grep -rn 'noop.*interrupt\|dummy.*interrupt' src/`).
(d) **(a) AND (b)**: the loop cannot reach an unconnected pointer under any future edit, and the register file does not
    pretend to hold state for a CPU that does not exist.
(e) **FAULT**: model the absent slots' registers as unmapped -- rejected by construction here: the four MASK words are one
    `case` arm at fixed addresses on the real board regardless of population; nothing says the board bus-errors them.
Which is the house idiom, and what does OpenBSD (or the LUNA-88K hardware) do with MASK1..3 on a uniprocessor?  The
ACCEPT SIDE the fix owes (de-escalation clause): on a 2-cpu configuration a store to MASK1 + SOFT_INT1 must STILL deliver to
cpu 1 -- how is a 2-cpu luna-88k configured from the command line (`-n 2`?  does the machine description allow it?  does the
rig image boot with it?  a probe row does not need a boot, only the cold debugger), and can a cold-debugger row observe the
delivery (the assert lands in cpu 1's pending state; is there a debugger command that shows it, or does a readback of MASK1's
bits 31..29 -- `highestCurrentStatus` -- show the pending level regardless of delivery?).

## 5. THE DETECTOR PLAN (vacuity floor a-f; rows are owed per ENUMERATED mutant)
Extend `luna_absentcpu_probe.py` (ships as `regress/luna_absentcpu_probe.py`, wired into gate 11 beside `luna_intmask_probe.py`):
  rows live / devsig / slot0 / mask1 / soft1 / live2 as measured, plus  `soft1x2` (a SECOND SOFT_INT1 store: kills a latch
  that declines once then delivers), `mask2`/`soft2` and `mask3`/`soft3` (slots 2 and 3: kills a fix that bounds at `< 2`
  or forgets a label), `timer1` (arm slot 1 with bit 31 and let a machine-wide line assert -- reachable in a cold debugger?
  the timer is a host-timer callback and single-stepping stops host timers, so probably NOT; say so or find a synchronous
  shared line), and the ACCEPT side under a 2-cpu config: `mask1 accept` (store to MASK1 lands: readback 0x00fc0000 under
  option a; under option b the store is DECLINED on 1 cpu but must LAND on 2 cpus -- so the row's expectation depends on the
  configured cpu count, which is a premise the probe must check, not assume).
Mutants: M_REVERT (the loop walks MAX_CPUS again), M_BOUND2 (bound at a literal 2), M_LABEL (SOFT_INT3 arm left unbounded),
M_NULLCHECK (a `!= NULL` check that skips the assert but still sets irqActive -- the interrupt is then LOST for a later
connect: does any row see that?), M_DECLINEALL (decline stores to ALL slots including 0 -- the connected-slot rows must red),
M_LATCHTHENDELIVER (decline once, deliver on the second store), M_STOREBUTNOREASSERT (store lands, reassert skipped: a
readback shows the store but the pending level never updates).  Which of these can a cold-debugger row distinguish?  CHANNEL
per row: which register/result word differs under which mutant -- name any row whose channel cannot vary.

## 6. QUESTIONS
Q1 THE PREMISE AUDIT: which of the settled premises above is wrong?  In particular: is `interrupt_status` really machine-wide
   (one field) while software interrupts are per slot?  Is the default cpu count one, and does the m88k rig boot with it?
   Does anything else in the tree connect `cpu_irq[1..3]` (another device, the machine description)?
Q2 THE SMALLEST EDIT that closes the witness and still leaves a guest-reachable death or a wrong readback -- name the row
   you expect to stay green.
Q3 OPTION-SET COMPLETENESS and the choice: which member, with its warrant (a measured delta, a transferred in-tree warrant,
   or hardware documentation -- none is on disk for the LUNA-88K board; say where it would be needed).  Is (a) alone enough,
   given a future edit could add another walk over MAX_CPUS?  Is (b) alone enough, given a future edit could add another
   writer of `interrupt_enable[]`?  Does OpenBSD's SMP kernel probe MASK1..3 by readback, so that (b)'s 0-readback changes a
   boot on a 1-cpu configuration (the rig would then be the witness: it boots today)?
Q4 THE ACCEPT SIDE: how to configure 2 cpus for the accept rows, and what a cold-debugger row can observe of a delivery to
   cpu 1.  If nothing can, say so and name the free-running shape.
Q5 SEVERITY: HIGH is proposed (a guest-reachable process death by two ordinary word stores on the machine the project boots;
   precedent: `pcc2defaultkill`, `m88kexcdeliver` were ranked on reachability by an ordinary instruction, not on a known driver
   doing it).  Argue it down only with a reason a future reader can check.
Q6 If, while verifying a claim, you found something ELSE -- say so.  (The `default:` arm's `cpu->running = 0; return 0` for any
   unimplemented address in the window is one candidate: is it already filed?  `grep -o '"id": "luna[a-z0-9]*"'
   tools/pipeline/ledger.json` lists the luna rows.)

VERDICT LINE FIRST (PROCEED-WITH-(x) / HOLD / the premise that is wrong), then Q1-Q6, then anything else.  agy is
DELIBERATELY NOT FIRED on this pass (reserved for measurement); the Opus measuring seat is asked separately to build the
option-(d) form in a scratch clone and run the witness + the accept-side row under `-n 2`.
