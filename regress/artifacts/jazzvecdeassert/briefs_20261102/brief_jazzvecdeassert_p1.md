# PANEL PASS 1 -- `jazzvecdeassert` (#578): every access to the Jazz interrupt-source register deasserts the CPU's IRQ3 unconditionally, dropping a level interrupt that is still pending (OB-22, the oldest open bug in the file)

Fired 2026-11-02 20:3x.  HEAD `3cb8bdc1` (the product tree `src/` is unchanged since `987cb596`; the two commits since are records only).
Roster (owner 2026-11-02 20:5x): Grok 4.7, the Ollama cloud seats (glm-5.3, deepseek-v4-pro, minimax-m3, kimi-k3), Opus 5.5, GPT-6 Astra
(codex, hotmail login).  Fable 5.1 adjudicates the final results in the main loop and is not a seat here.  No seat is to build or run
anything: the witness is MEASURED and inlined below.

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not just the
derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from something this brief
did NOT give it is worth more than a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at HEAD `3cb8bdc1`.**  Do not read `./src/` under the project root (a pristine 2021 upstream
copy) nor `est/src/` (the non-git twin; its `dev_jazz.c` is a declared divergence-set file, though its `jazz_jazzio` function is
byte-identical to SEC's today -- section 2).  If your line numbers disagree with mine, say so rather than reconciling.  **If you cannot
read files that is expected** -- every fact you need is inlined.  Name any premise you cannot settle from this packet rather than
guessing.  **VERDICT LINE FIRST** (`VERDICT: PROCEED / PROCEED WITH CHANGES (<n>) / DO NOT PROCEED`), repeated last.
File-reading seats: scope your reading to `GXEMUL-SEC/src/devices/dev_jazz.c`, `dev_ns16550.c`, `src/machines/machine_arc.c`,
`src/cpus/cpu_mips.c` (the interrupt assert at `mips_cpu_interrupt_assert`), `src/include/thirdparty/pica.h`, and
`regress/footbridge_sites_probe.py` (the house shape for a self-contained cold-debugger probe).  Reading only.

## 1. The defect as filed, the proposed fix, and the MEASURED witness

**The filing.**  OB-22 of the July 2026 audit (`OUTSTANDING_BUGS.md:2965`, the original table row: "`devices/dev_jazz.c:613`
(`jazz_jazzio`) | pre-existing, correctness only (NOT a #69 regression): after reporting a vector it deasserts `mips_irq_3` without
clearing `int_asserted` -> possible stuck/missed non-timer JAZZ IRQs until next edge/mask write").  Deferred three times as
"self-healing, correctness-only, would touch the verified arc boot" (CHANGELOG `#70-#88` block: "it sits in the exact arc interrupt
path just stabilized by #69 -- deferred to avoid regressing the verified arc boot; revisit with dedicated arc interrupt testing").
It has no ledger row (named in the bug file only, by the `#555` id-less review's index: "OB-22 (named in this file only)").  It is
the oldest open defect in the queue by filing date; every other July audit item is resolved.

**The site at HEAD** -- `src/devices/dev_jazz.c`, `DEVICE_ACCESS(jazz_jazzio)`, the common tail at `:696-697`:

```c
	/*  This is needed by Windows NT during startup:  */
	INTERRUPT_DEASSERT(d->mips_irq_3);
```

It runs on EVERY access to the `pica_jazzio` register (4 bytes at physical `0xf0000000`; offset 0 reads the interrupt-source vector,
offset 2 reads or writes `jazz_timer_value`, any other offset prints an "unimplemented" `fatal()` and still falls through to it).
The Jazz device keeps the pending local-bus lines in `d->int_asserted` (bits 0-14; bit 15 the interval timer) and drives the CPU's
IRQ3 from `(int_asserted & 0x7fff) && (int_enable_mask & R4030_EXT_IP3)` in `jazz_interrupt_assert()` / `jazz_interrupt_deassert()`
and in the `EXT_IMASK` write arm (section 3).  The tail deasserts the CPU line WITHOUT consulting that predicate: with two lines
pending, the guest's vector read for the first drops IRQ3 while the second is still outstanding, and nothing re-asserts it until some
line is asserted anew (that is the "self-healing" the old entry describes: a fresh `jazz_interrupt_assert()` re-raises IRQ3).

**Proposed fix (tentative; the panel reviews this form and the final diff separately):** make the deassert conditional on the same
predicate the deassert handler uses.  `_scratchpad/w578/product.diff`, applied by `apply_fix578.py`:

```diff
@@ -693,8 +693,15 @@
 		}
 	}
 
-	/*  This is needed by Windows NT during startup:  */
-	INTERRUPT_DEASSERT(d->mips_irq_3);
+	/*  #578: this access used to deassert the CPU's IRQ3 unconditionally
+	    ("needed by Windows NT during startup").  With a second JAZZ line
+	    still pending, the vector read for the first dropped a level
+	    interrupt until some line was asserted anew (OB-22).  Deassert
+	    only when no enabled line is pending -- the predicate
+	    jazz_interrupt_deassert() uses -- so the nothing-pending case the
+	    old comment describes behaves as before.  */
+	if (!((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP3)))
+		INTERRUPT_DEASSERT(d->mips_irq_3);
 
 	if (writeflag == MEM_READ)
 		memory_writemax64(cpu, data, len, odata);
```

Nothing else in the function changes: the vector computation, the `jazz_timer_value` arm, the `default:` prints, the common tail's
`memory_writemax64` and `return 1` are untouched.

**Witness, rung 3, MEASURED 2026-11-02 20:16** -- `regress/artifacts/jazzvecdeassert/witness_20261102/jazz_vector_witness.py` on the
UNMODIFIED in-tree arc/pica machine (`-V -e pica`, the rig kernel loaded for construction only), on a fresh WSL clone of HEAD's product
tree (`/tmp/gxdivw`, binary md5 `b76a7799a3ea`, newer than source) and on that clone plus the diff above (`/tmp/gxfix578`, md5
`d1882f5650a6`).  Every device access is a genuine guest instruction through XKPHYS (`sb` / `lbu` / `sw` / `lw` stubs executed with
`step`), never a debugger `put`; the CPU-side observable is COP0 Cause's IP3 bit (`mips_irq_3` is CPU line 3, `templ.line = 1 <<
(STATUS_IM_SHIFT + 3)` = 0x800, `cpu_mips.c`), read with `print cause`.  Two JAZZ lines are driven from the two ns16550 UARTs
`machine_arc.c` wires for pica (0x80006000 on `jazz.8`, 0x80007000 on `jazz.9`): a UART asserts its line SYNCHRONOUSLY inside the
guest's IER store (`dev_ns16550.c`: the IER write sets `IIR_TXRDY` and calls `dev_ns16550_tick`, which asserts when `MCR.IENABLE` is
set), so the witness runs under single-step.  No interrupt is ever DELIVERED (Status.IE is clear on the cold CPU and the debugger
suppresses exception dispatch while stepping); Cause.IP reflects the asserted lines regardless.

```
row             what                                                  HEAD (witness_head.out)   fixed (witness_fixed.out)
jz imask        EXT_IMASK reads back 0x2 after the guest store        0x2   ok                  0x2   ok     (device signature, R4030)
jz com0 ier     com0 IER reads back 0x2                               0x2   ok                  0x2   ok     (device signature, UART)
jz ip one       Cause.IP3 set after com0's IER write                  0x800 ok                  0x800 ok     (LIVENESS of the path to the CPU)
jz ip both      Cause.IP3 set after com1's IER write too              0x800 ok                  0x800 ok
jz vec          vector reads 0x24 = (8 + 1) << 2                      0x24  ok                  0x24  ok     (device signature, jazzio: RAM cannot answer this)
jz ip after     Cause.IP3 STILL set after the vector read             0x0   FAIL (want 0x800)   0x800 ok     <- THE DEFECT: com0 AND com1 still pending
jz vec again    a second vector read still 0x24                       0x24  ok                  0x24  ok     (the read clears no line)
jz vec com1     com0's IER cleared: the vector names line 9, 0x28     0x28  ok                  0x28  ok
jz ip com1      Cause.IP3 set with com1 alone pending                 0x0   FAIL (want 0x800)   0x800 ok     <- nothing re-asserted it
jz ip reheal    re-enabling com0's IER re-asserts IP3                 0x800 ok                  0x800 ok     (the self-healing mechanism, as a control)
jz ip none      both IERs cleared: IP3 clear                          0x0   ok                  0x0   ok     (the deassert handler works with nothing pending)
jz vec none     vector reads 0 with nothing pending                   0x0   ok                  0x0   ok
jz ip nt        IP3 clear after a vector read with nothing pending    0x0   ok                  0x0   ok     (the Windows NT case the old comment names: unchanged)
RESULT                                                                11/13                     13/13
```

Both red rows read exactly the predicted value (IP3 dropped to 0 by the blanket deassert while a line was pending) and go green on
the fixed build with the same script (clause (i) of the witness rule); both controls of clause (ii) are present and green on both.

## 2. SETTLED PREMISES (C0 output and what was re-read today)

C0 at `3cb8bdc1`: `git log -1 -- src/devices/dev_jazz.c` = `a749cbe0 2026-07-18 Round 38 (#268): R4030 DMA count-register width`;
`grep -c jazzvecdeassert CHANGELOG.md` = 0; `ls regress/ | grep -i jazz` = nothing (no Jazz probe exists; no committed probe imports
`_scratchpad/gxprobe.py` -- every committed cold-debugger probe is self-contained, e.g. `footbridge_sites_probe.py` forks its own pty).
**The round has not shipped.**  The two deassert lines are the 0.7.0 import's (the `#69` round touched the ENABLE-mask logic in this
file, not this tail; the OB-22 table row says "NOT a #69 regression").

* `R4030_EXT_IP3 0x02` (local bus -> MIPS irq 3), `R4030_EXT_IP4 0x04`, `R4030_EXT_IP6 0x10`; `PICA_TIMER_IRQ 15`; `DEV_JAZZ_LENGTH 0x280`
  (`dev_jazz.c:62-80`).  `R4030_SYS_EXT_IMASK = R4030 + 0xe8`, `R4030_SYS_ISA_VECTOR = R4030 + 0x238` (`pica.h:82-85`); the Jazz device is
  registered at `devinit->addr` = 0x80000000 (`machine_arc.c:128`), `pica_jazzio` at 0xf0000000 for 4 bytes (`dev_jazz.c:780-782`).
* Lines on pica (`machine_arc.c:154-222`): ns16550 at 0x80006000 `jazz.8` and 0x80007000 `jazz.9`; `sn` (SONIC) `jazz.4`; `asc` `jazz.5`;
  `fdc` `jazz.1`; `ne2000` on the ISA bridge (`jazz.isa.9`, IRQ4, not this path); `mc146818` on MIPS irq 2 directly.
* The CPU side: `cpu_mips.c:250` registers CPU line i as `templ.line = 1 << (STATUS_IM_SHIFT + i)`, and `mips_cpu_interrupt_assert()` /
  `_deassert()` (`:1884-1892`) OR / AND-NOT that bit into `coproc[0]->reg[COP0_CAUSE]`.  So IRQ3 is Cause bit 11 (0x800).
* Which pica devices can leave a line asserted with no deassert path (the storm risk a conditional deassert would expose)?  Grep census
  of `INTERRUPT_ASSERT`/`INTERRUPT_DEASSERT` per device file at HEAD: `dev_sn.c` 0/0 and `dev_fdc.c` 0/0 (they never assert their line in
  this tree), `dev_asc.c` 1/2, `dev_pckbc.c` 2/2, `dev_ns16550.c` 1/1, `dev_mc146818.c` 1/2, `dev_ne2000.c` 2/1 (ISA path).  Every
  device that asserts a Jazz local-bus line also deasserts it.  **Stated as a question in Q1.**
* `jazz_interrupt_deassert()` already recomputes the CPU line from the predicate when a device drops its line (`:148-157`); the `EXT_IMASK`
  write arm recomputes it when the mask changes (`:451-483`).  The jazzio tail is the ONLY site that deasserts `mips_irq_3` without the
  predicate (`INTERRUPT_DEASSERT(d->mips_irq_3)` occurs at `:154`, `:467` and `:697`; the first two are predicate-gated).
* **The sibling (pre-table SIBLING PARITY):** the ISA vector read `R4030_SYS_ISA_VECTOR` (`:398-416`) reports the lowest pending ISA line
  and touches NO CPU line; the jazzio vector read reports the lowest pending local-bus line and blanket-deasserts IRQ3.  The fix makes the
  two reads behave alike.
* **est twin:** `est/src/devices/dev_jazz.c` is a declared divergence-set path (the ARC/Jazz layer differs between the twins elsewhere), but
  its `jazz_jazzio` function is byte-identical to SEC's today (diff of the 47 lines = empty; its tail is at est `:661-662`).  The
  divergence rule says `build/` compares against est for this path, never against SEC.  **Q5 asks whether the hunk lands in both.**
* `build/` is the pmax tree (no jazzio); the arc rig runs the WSL `/tmp/gxsec-build` tree's binary (`gxemul_arc_rig/gxsec-gxemul`,
  republished by `gate_build.sh`), and gate 4 (`gate_mips.sh`) boots OpenBSD 2.2 on it to `uid=0(root)` -- that boot is the "verified arc
  boot" the three deferrals protected, and it is the gate this round must leave green.  Windows NT is not a rig here and no NT image exists
  on this machine; the "needed by Windows NT during startup" comment cannot be re-measured.
* There is no R4030/Jazz datasheet under `_scratchpad/` (`ls _scratchpad/*.pdf` lists none); the code's own reference is NetBSD's
  `arch/arc/jazz/jazzio.c` (the comment above `jazz_jazzio`).  The hardware semantics assumed here are the LEVEL semantics the rest of
  this file already implements: a line stays asserted until its device drops it, and the CPU line follows the OR of the enabled lines.

**Stated as questions:**
* Is the blanket deassert load-bearing for any guest this project boots?  OpenBSD/arc's jazzio interrupt handler reads the vector and
  dispatches to the device driver, which services and so drops the line; it does not rely on the read clearing anything.  I believe the
  conditional form changes nothing on that boot -- gate 4 measures it, and the brief does not claim it.
* Does the "Windows NT" case depend on the deassert firing WHILE A LINE IS PENDING (which would make it an edge-triggered expectation, or
  a device model that never drops its line), or only on the nothing-pending case the fix preserves?  Unknown and unmeasurable here; the
  premise the fix rests on is that no device in the tree holds a line without a deassert path (the census above).
* Is `0x24 = (8 + 1) << 2` the right vector encoding to pin?  `:667-675`: `v = i + 1` for the lowest set bit i in 0..14, `odata = v << 2`.

## 3. THE CODE, VERBATIM (HEAD `3cb8bdc1`)

`src/devices/dev_jazz.c:657-703`, the whole enclosing function (the fix lands in its common tail):
```c
DEVICE_ACCESS(jazz_jazzio)
{
	struct jazz_data *d = (struct jazz_data *) extra;
	uint64_t idata = 0, odata = 0;
	int i, v;

	if (writeflag == MEM_WRITE)
		idata = memory_readmax64(cpu, data, len);

	switch (relative_addr) {
	case 0:
		v = 0;
		for (i=0; i<15; i++) {
			if (d->int_asserted & (1<<i)) {
				v = i+1;
				break;
			}
		}
		odata = v << 2;
		break;
	case 2:
		/*  TODO: Should this be here?!  */

		if (writeflag == MEM_WRITE)
			d->jazz_timer_value = idata;
		else
			odata = d->jazz_timer_value;
		break;
	default:
		if (writeflag == MEM_WRITE) {
			fatal("[ jazzio: unimplemented write to address 0x%x"
			    ", data=0x%02x ]\n", (int)relative_addr,
			    (int)idata);
		} else {
			fatal("[ jazzio: unimplemented read from address 0x%x"
			    " ]\n", (int)relative_addr);
		}
	}

	/*  This is needed by Windows NT during startup:  */
	INTERRUPT_DEASSERT(d->mips_irq_3);

	if (writeflag == MEM_READ)
		memory_writemax64(cpu, data, len, odata);

	return 1;
}
```

`:138-157`, the two handlers every Jazz line goes through:
```c
void jazz_interrupt_assert(struct interrupt *interrupt)
{
	struct jazz_data *d = (struct jazz_data *) interrupt->extra;
	d->int_asserted |= (1 << interrupt->line);

	if ((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP3))
		INTERRUPT_ASSERT(d->mips_irq_3);
	if ((d->int_asserted & PICA_TIMER_IRQ_MASK) && (d->int_enable_mask & R4030_EXT_IP6))
		INTERRUPT_ASSERT(d->mips_irq_6);
}
void jazz_interrupt_deassert(struct interrupt *interrupt)
{
	struct jazz_data *d = (struct jazz_data *) interrupt->extra;
	d->int_asserted &= ~(1 << interrupt->line);

	if (!((d->int_asserted & 0x7fff) && (d->int_enable_mask & R4030_EXT_IP3)))
		INTERRUPT_DEASSERT(d->mips_irq_3);
	if (!((d->int_asserted & PICA_TIMER_IRQ_MASK) && (d->int_enable_mask & R4030_EXT_IP6)))
		INTERRUPT_DEASSERT(d->mips_irq_6);
}
```

`:451-483`, the `EXT_IMASK` write arm (the third site that drives IRQ3, predicate-gated):
```c
	case R4030_SYS_EXT_IMASK:
		if (writeflag == MEM_WRITE) {
			int old_assert_3 = ((d->int_asserted & 0x7fff) &&
			    (d->int_enable_mask & R4030_EXT_IP3));
			int old_assert_6 = ((d->int_asserted & PICA_TIMER_IRQ_MASK) &&
			    (d->int_enable_mask & R4030_EXT_IP6));
			int new_assert_3, new_assert_6;

			d->int_enable_mask = idata;

			new_assert_3 = ((d->int_asserted & 0x7fff) &&
			    (d->int_enable_mask & R4030_EXT_IP3));
			new_assert_6 = ((d->int_asserted & PICA_TIMER_IRQ_MASK) &&
			    (d->int_enable_mask & R4030_EXT_IP6));

			if (old_assert_3 && !new_assert_3)
				INTERRUPT_DEASSERT(d->mips_irq_3);
			else if (!old_assert_3 && new_assert_3)
				INTERRUPT_ASSERT(d->mips_irq_3);

			if (old_assert_6 && !new_assert_6)
				INTERRUPT_DEASSERT(d->mips_irq_6);
			else if (!old_assert_6 && new_assert_6)
				INTERRUPT_ASSERT(d->mips_irq_6);

			reassert_isa_interrupts(d);
		} else
			odata = d->int_enable_mask;
		break;
```

`:398-416`, the ISA vector read (the sibling; it touches no CPU line):
```c
	case R4030_SYS_ISA_VECTOR:
		debug("[ jazz: R4030_SYS_ISA_VECTOR read (writeflag=%i) ]\n",
		    writeflag);
		{
			uint32_t x = d->isa_int_asserted
			    & d->isa_int_enable_mask;
			odata = 0;
			while (odata < 16) {
				if (x & (1 << odata))
					break;
				odata ++;
			}
			if (odata >= 16)
				odata = 0;
		}
		break;
```

`dev_ns16550.c:92-104` (why a guest IER store asserts the line synchronously) and `:194-200` (the IER arm):
```c
	if (((d->reg[com_ier] & IER_ETXRDY) && (d->reg[com_iir] & IIR_TXRDY)) ||
	    ((d->reg[com_ier] & IER_ERXRDY) && (d->reg[com_iir] & IIR_RXRDY))) {
		d->reg[com_iir] &= ~IIR_NOPEND;
		if (d->reg[com_mcr] & MCR_IENABLE) {
			INTERRUPT_ASSERT(d->irq);
			d->int_asserted = 1;
		}
	} else {
		d->reg[com_iir] |= IIR_NOPEND;
		if (d->int_asserted)
			INTERRUPT_DEASSERT(d->irq);
		d->int_asserted = 0;
	}
...
			/*  Needed for NetBSD 2.0.x, but not 1.6.2?  */
			if (!(d->reg[com_ier] & IER_ETXRDY)
			    && (idata & IER_ETXRDY))
				d->reg[com_iir] |= IIR_TXRDY;

			d->reg[com_ier] = idata;
			dev_ns16550_tick(cpu, d);
```

## 4. THE OPTION SET (name a member I did not)

1. **CONDITIONAL deassert** (proposed): gate the tail's deassert on the predicate the handlers use.  Keeps the nothing-pending behaviour
   byte for byte; changes only the case the witness measured.
2. **DELETE the tail's deassert**: `jazz_interrupt_deassert()` and the mask arm already recompute the CPU line whenever a line or the
   mask changes, so with nothing pending IRQ3 is already clear -- I believe (1) and (2) are observationally EQUIVALENT on every row above
   and on every path in the tree, which makes (2) the smaller diff and (1) the self-documenting one.  **Q3 asks which to ship, and the kill
   table will build (2) as a mutant of (1) to measure the equivalence rather than assert it.**
3. **Deassert only on the vector read (offset 0)**, not on the timer-value or unimplemented accesses -- orthogonal to (1)/(2); narrows
   where the blanket fires but keeps the defect on the vector read itself.  Rejected as the fix; could ride as a precision on (1).
4. **Keep HEAD + document** (the three earlier deferrals' choice).  The witness now measures a guest-visible wrong state, so this is no
   longer the documented-only case.
5. **Re-evaluate and re-assert**: deassert then re-assert if the predicate still holds -- a glitch on the CPU line for nothing; (1) is the
   same without the glitch.

## 5. THE PROPOSED DETECTOR

The witness script itself, re-cast as a committed probe `regress/jazz_vector_probe.py` -- **self-contained** like every committed
cold-debugger probe (its own pty driver in the footbridge shape; `_scratchpad/gxprobe.py` is untracked and no committed probe imports
it), 13 rows, names at 13 characters or fewer (`%-14s`, the gate's `^$v  .*ok$` anchor).  Hosted in `gate_mips.sh`, which already needs
`$ARC_RIG/gxsec-gxemul`: a section after the arc boot runs the probe against that binary (about 40 s), pins `jazz_vector rows run` 13
by EQUALITY, and loops the 13 names.  **Q4 asks whether gate 4 is the right home** (it is the only gate that already holds the arc
binary; a cold probe adds no boot and no load-sensitive oracle).

**Floor, with the predicted scores (a `PRETABLE.out` is written before any table leg runs):**
* (a) the base leg = HEAD: 11/13, measured (`witness_head.out`).
* (b) `M_b`, the unconditional deassert reinstated verbatim: 11/13 (`jz ip after`, `jz ip com1`).
* (c) null medium for a runtime probe: an ABSENT / non-emulator binary -- every session dies, every row None: 0/13.
* (d) the fix ADDS one predicate; DEPENDS-ON weakenings: `M_lowbits` `& 0x7fff` -> `& 0x00ff` (lines 8 and 9 fall outside: deasserts while
  the UARTs are pending) 11/13; `M_ip6` `R4030_EXT_IP3` -> `R4030_EXT_IP6` (the mask carries 0x02 only, so the predicate is never true)
  11/13; `M_timer` `& 0x7fff` -> `& PICA_TIMER_IRQ_MASK` 11/13; `M_inv` the predicate inverted 11/13 (`jz ip after` red; `jz ip nt` stays
  green because IP3 is already clear there -- a one-sided row).  `M_nomask`, the `int_enable_mask` term dropped: predicted 13/13 and
  EQUIVALENT, not an escape -- when the mask has IP3 clear the mask arm has already deasserted IRQ3, so the tail's extra deassert changes
  nothing; the body-tested partition on `int_enable_mask & IP3` is {0, nonzero} and no row holds the 0 cell with a line pending because
  the cell is unobservable through this predicate (disclosed under (e); **Q2 asks you to refute that**).
* (e) the contract: the rows drive two lines (8, 9) and the mask value 0x2; a weakening keyed to a line this table does not drive (0-7,
  10-14) or to the timer bit is disclosed; `M_del` (option 2, the deassert deleted) is predicted 13/13 EQUIVALENT and is recorded as the
  equivalence measurement for Q3, not as an escape.
* (f) not applicable: no address decode is under test (the vector encoding row `jz vec` pins the one value the fix does not touch).

De-escalation does not apply (no host-stopping check is removed).  The gate pin is an EQUALITY on 13.

## 6. DISCLOSED, NOT IN SCOPE

* `jazzlbmask` (open, MED): the Jazz local-bus interrupt ENABLE bits at the LB_IE address are unused -- a different register; untouched.
* `jazzpendingovf` (open): the interval-timer backlog counter has no saturation -- IRQ6, untouched.
* The ISA funnel (`mips_irq_4`, `reassert_isa_interrupts`) is a different path and untouched.
* The `fatal()` prints in the `default:` arm are unlatched and guest-drivable (the `floodclass` class); untouched here.
* Windows NT is not measurable here; the fix preserves the nothing-pending behaviour and the brief claims nothing else about NT.

## 7. QUESTIONS

**Q1, premise audit.**  Which premise in sections 1-5 is false?  In particular: (a) does any pica device assert a Jazz local-bus line and
never deassert it (the census says no -- re-derive it), so that a conditional deassert could leave IRQ3 high and storm the OpenBSD/arc
boot?  (b) is Cause bit 0x800 the right observable for `mips_irq_3`, and does `print cause` read it?  (c) is the ns16550 assert truly
synchronous in the IER store (the `MCR.IENABLE` gating, the `IIR_TXRDY` set)?  (d) the witness rows' encodings and wants (0x24, 0x28,
0x2).  (e) "the two deassert lines are the 0.7.0 import's".

**Q2, the partition.**  Over {no line pending, one line pending, two lines pending} x {IP3 enabled in EXT_IMASK, disabled}: which cells
does the fix change, which does it leave, and does the detector have a member in each reachable cell?  Refute the claim that the
(line pending, mask disabled) cell is unobservable through the tail's predicate.

**Q3, candidate weakenings and the equivalence.**  For each of `M_b`, `M_del`, `M_nomask`, `M_lowbits`, `M_ip6`, `M_timer`, `M_inv`:
EQUIVALENT to the fixed form or not, the input at which it first differs, and the row that reds.  Then: ship the CONDITIONAL form (1) or
the DELETION (2)?  If they are equivalent on every path, which is the honest diff, and what does the record say about the other?

**Q4, the vehicle.**  A self-contained 13-row probe in `gate_mips.sh` against `$ARC_RIG/gxsec-gxemul`.  Is gate 4 the right home, is a
40-second cold probe acceptable there, and is anything in the rows load-sensitive (none free-runs; every step is synchronous)?

**Q5, the twins.**  `dev_jazz.c` is a divergence-set file whose `jazz_jazzio` function is byte-identical in `est/` today.  Land the hunk in
SEC only (the ARC layer is SEC's), or in both so the identical function stays identical?  What does `build/` (the pmax tree, which carries
est's copy) owe at landing?

**Q6, option-set completeness.**  Is there a member section 4 did not name?  Grep the fork for the idiom: how do the other interrupt
controllers in this tree treat a vector / acknowledge read (`dev_8259.c`'s ISR/IRR reads, `dev_footbridge.c`'s IRQStatus, `dev_i80321.c`,
`dev_gc.c`)?

**If, while verifying a claim, you found something ELSE -- say so.**  End with `VERDICT: PROCEED / PROCEED WITH CHANGES (<n>) / DO NOT
PROCEED`, and name every premise you could not settle from this packet.
