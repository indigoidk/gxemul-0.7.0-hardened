# `lcairqstubkill` — DESIGN BRIEF: two unguarded terminations on the ISA interrupt path

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise its author stated wrongly, and on the
round that closed an hour ago **nine defects in my own detector were found by seats and one by me**.
**Check the premises, not just the derivations.** Where I state something as fact, ask whether it is
true. A seat that re-derives a premise from something this brief did NOT give it is worth more than
a seat that agrees.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** There are three pristine-2021-upstream copies of
GXemul under the project root. They are NOT this fork. If your line numbers disagree with mine by
hundreds you are reading one of them — say so rather than reconciling.

**If you cannot read files that is expected** — every fact you need is inlined. Name any premise you
cannot settle from this packet rather than guessing at it.

**Where I state an ARITHMETIC or COUNT claim, ENUMERATE it rather than reasoning about it**, and ask
what the PRODUCER of those values can emit before you walk them.

**VERDICT LINE FIRST.**

## §C0 — has this round already shipped?  Both commands, run before writing this.

```
git log -1 --oneline -- src/devices/dev_lca.c
  b4d4177  #515 lcaconfbus1kill: one variable meant two things ...   (a DIFFERENT handler)

grep -c lcairqstubkill CHANGELOG.md
  0        -- no round has shipped for this row
```

*(I skipped this check on a brief earlier today and a seat spent 84 KB establishing that shipped
work had shipped. It is two commands.)*

## §C — SETTLED PREMISES, each verified locally for this brief

**P1 — the two functions, in full. There is no guard of any kind:**

```c
/*
 *  lca_interrupt_assert():
 *
 *  Line 0 = ISA interrupt.
 */
void lca_interrupt_assert(struct interrupt *interrupt)
{
	fatal("lca_interrupt_assert: TODO\n");
	exit(1);
}

/*
 *  lca_interrupt_deassert():
 *
 *  Line 0 = ISA interrupt.
 */
void lca_interrupt_deassert(struct interrupt *interrupt)
{
	fatal("lca_interrupt_deassert: TODO\n");
	exit(1);
}
```

**No value is being refused and no condition selects the stub.** This is not a refusal decision; it
is an unimplemented path — which matters for the option set below.

**P2 — they are wired as the real ISA interrupt callbacks**, in `DEVINIT(lca)`:

```c
	interrupt_template.line = 0;
	interrupt_template.name = interrupt_path;
	interrupt_template.extra = d;
	interrupt_template.interrupt_assert = lca_interrupt_assert;
	interrupt_template.interrupt_deassert = lca_interrupt_deassert;
	interrupt_handler_register(&interrupt_template);

	bus_isa_init(devinit->machine, interrupt_path,
	    BUS_ISA_IDE0 | BUS_ISA_IDE1, LCA_ISA_BASE, LCA_ISA_MEMBASE);
```

**P3 — WITNESSED TWICE, on two independent guest paths**, rung 3, on unmodified `alphabook1`:
`regress/lca_irqstub_probe.py` (one guest store to the 8042 command port, 3/4) and
`regress/lca_irqstub_uart_probe.py` (three guest byte stores to the ns16550 on IRQ 4, 2/4).

**P4 — *** ALPHA HAS NO INTERRUPT DELIVERY AT ALL. Measured, and it is the premise the whole
disposition turns on. *** ** `cpu->cd.alpha.irq_asserted` is WRITTEN at `cpu_alpha.c:218` and `:223`
and **READ NOWHERE**. `cpu_dyntrans.c` is where a pending interrupt becomes a delivered one and it
tests exactly three architectures — `cd.arm.irq_asserted` (`:208`), `cd.m88k.irq_asserted` (`:212`,
`:382`) and `cd.ppc.irq_asserted` (`:243`). **Alpha is absent from that list.**

So wiring these stubs to `cpu_interrupt()` would set a field nothing reads: **a NO-OP, not a
delivery.** Please check this — it is the load-bearing claim and I want it refuted if it is wrong.

**P5 — `struct lca_data` has NO `warned` field, and `dev_lca.c` contains no latch of any kind.**
This would be the file's first. But `interrupt_template.extra = d` means both callbacks can reach
the device instance through `interrupt->extra`.

## §D — THE OPTION SET, and why the usual members mostly do not apply

The seven members are: 1 DELETE · 2 DECLINE (silent) · 3 DECLINE + BOUNDED (LATCHED) ANNOUNCE ·
4 ACCEPT · 5 FAULT · 6 BACKED ACCEPT · 7 IMPLEMENT.

* **4, 5, 6 presume a value is being refused.** P1 shows nothing is. FAULT additionally has no Alpha
  machinery (`memory_rw.c` dispatches a bus error for MIPS and M88K only).
* **7 IMPLEMENT is a SUBSYSTEM, not a wiring job** — by P4 it requires adding Alpha interrupt
  dispatch to `cpu_dyntrans.c` plus the PALcode entry and IPL check that go with it.
* So the live candidates are **2** and **3**, and my proposal is **3, per-instance**.

## §G — THE QUESTIONS

**Q1. Is P4 right?** If Alpha delivery exists anywhere I have not looked, this whole disposition is
wrong and the round should be an implementation round instead. Please try to refute it.

**Q2. Should the stubs write `irq_asserted` anyway, even though nothing reads it?** The argument for:
a future Alpha dispatch would then find the state already correct. **I lean AGAINST** — it is the
addition-licence's "cannot hurt" shape, shipping a line whose only justification is a subsystem
nobody has scheduled. Is that right?

**Q3. Per-instance latch or function-static?** I propose a `warned` bitfield in `struct lca_data`
reached via `interrupt->extra`, because a function-static latch would mean one guest access to one
device instance permanently silences the diagnostic for every other instance — a class already filed
here as `staticlatchscope`, 28 sites across 11 files. **Is there a reason `dev_lca.c`'s first latch
should not be per-instance?**

**Q4. One latch or two?** Assert and deassert are separate functions. One shared bit is quieter; two
bits distinguish which callback fired. **Which does the house idiom favour, and does it matter that
a driver will usually reach BOTH within one interrupt cycle?**

**Q5. THE DETECTOR PROBLEM, and this is the one I most need help with.** After the fix, "the host
survived and nothing happened" is **indistinguishable from** "the host survived and an interrupt was
delivered" — *because no delivery mechanism exists*. So a survival oracle is vacuous by construction
here, and the only other observable is the latch's own announcement, which fires once.
**Is a detector constructible beyond (a) survival and (b) the announce firing exactly once across
repeated interrupts?** If not, say so plainly — the round then ships with `detector:` as its witness
term and a contract stating that the delivery half is unobservable, which is an honest record rather
than a gap.

**Q6. What does the round's CHANGELOG owe so it cannot be misread?** The fix buys *the host stops
dying*; it does NOT buy *interrupts start working*. I want the record to be impossible to read as
the latter.
