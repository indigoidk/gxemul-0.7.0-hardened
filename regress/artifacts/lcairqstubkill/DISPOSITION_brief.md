# LCA interrupt delivery: what is the honest disposition when the repair cannot complete?

**VERDICT LINE FIRST.**

**The tree is `GXEMUL-SEC/src/`** — ignore the pristine 2021 copy at the project root.

**Please do not simply ratify.** Section 2 is almost entirely YOUR earlier findings, and I want you
harder on them than you were the first time — including whether the *disposition* I am leaning
toward is right, not merely whether the *finding* was. Those are different claims and the second
does not follow from the first.

## 1. THE SITE

`src/devices/dev_lca.c:70-86` — two functions whose entire bodies are a diagnostic and a process
exit, with **no guard at all**:

```c
void lca_interrupt_assert(struct interrupt *interrupt)
{
	fatal("lca_interrupt_assert: TODO\n");
	exit(1);
}
void lca_interrupt_deassert(struct interrupt *interrupt)
{
	fatal("lca_interrupt_deassert: TODO\n");
	exit(1);
}
```

registered at `:414-415` as the machine's interrupt template. `fatal()` only prints; the explicit
`exit(1)` terminates.

## 2. SETTLED — these are your findings and one census of mine

* **GUEST-REACHABLE, path named end to end.** `devinit_lca()` passes its interrupt path to
  `bus_isa_init()` (`:418`), which connects the upstream interrupt (`bus_isa.c:190`) and
  **unconditionally installs the first UART on ISA IRQ 4** (`bus_isa.c:250`). So:
  `dev_ns16550_tick()` → `isa_interrupt_assert()` → `isa_interrupt_common()` →
  `lca_interrupt_assert()` → `exit(1)`, with **no machine-description modification**.
* **LCA line 0 is the AGGREGATE ISA input**, not ISA IRQ 0.
* **FORWARDING CANNOT COMPLETE DELIVERY**, and I verified your reason by census:

      cd.alpha.irq_asserted   written cpu_alpha.c:218,:223   declared cpu_alpha.h:161   READ NOWHERE
      cd.arm.irq_asserted     READ at cpu_dyntrans.c:208
      cd.m88k.irq_asserted    READ at cpu_dyntrans.c:212, :382
      cd.ppc.irq_asserted     READ at cpu_dyntrans.c:243, cpu_ppc.c:309

  **`cpu_dyntrans.c` has no Alpha arm at all.** So a correct forwarding repair sets a flag nothing
  consumes.
* **FOOTBRIDGE is the closest in-tree analogue and does NOT transfer literally:** it registers
  `interrupt->line` as a **bit mask**, LCA registers **index zero**, so a copied
  `status |= interrupt->line` records nothing.
* **The architectural FAULT disposition is unavailable on Alpha** — `memory_rw.c`'s device-failure
  path has `#ifdef MEM_MIPS` and `#ifdef MEM_M88K` arms only, and `ALPHA_KENTRY_MM` has zero
  consumers.
* **A witness attempt was made and did NOT fire.** `regress/artifacts/lcairqstubkill/
  lcairq_probe.asrun.py`: three controls green, the debugger writes visibly land, no assertion
  reached the stub. **Whether a debugger `put` reaches `DEVICE_ACCESS(ns16550)` at all is open**, so
  the attempt is INCONCLUSIVE rather than negative. It is preserved as evidence, classified
  explicitly as NOT a detector.

## 3. THE DISPOSITION QUESTION — this is the whole brief

The menu in this project: **delete** the termination; **decline** silently; **decline with a
bounded, once-only announcement**; **accept**; **accept with backing storage**; **fault**
(unavailable here); **implement**.

**My lean, stated so you can attack it:** a bounded latched announcement plus forwarding — because
deleting the exit and forwarding to a flag nothing reads converts *"the emulator terminates"* into
*"the interrupt is silently dropped"*, and silence is the harder failure to notice.

**Q1. IS THAT LAUNDERING?** A repair that removes a process exit and leaves the machine still unable
to take an interrupt can be described two ways: an honest partial improvement, or a round claiming
to have fixed something while the capability remains absent. **Argue the strongest case AGAINST my
lean**, then say which you actually hold.

**Q2. WHAT IS THE MINIMUM HONEST IMPLEMENTATION?** If forwarding is worth doing at all, what exactly
should the two functions contain — and what should the round's record claim, given that delivery
cannot complete? Be specific about the sentence the CHANGELOG should carry.

**Q3. SHOULD THE ROUND INSTEAD ADD THE ALPHA DISPATCH ARM?** That is a much larger change:
`cpu_dyntrans.c` would need an Alpha case, and the PAL entry path would need to exist. **Is that a
queue item, a different round, or out of scope entirely?** The addition licence here requires a
measured delta or a transferred warrant, never "it cannot hurt".

**Q4. WHAT OBSERVABLE DISTINGUISHES A CORRECT IMPLEMENTATION FROM AN INCOMPLETE ONE?** Name the
specific state or output a regression row should assert, so a later partial implementation does not
read as complete. You gave a four-row table last time; **say which of those rows are buildable
TODAY against the shipped tree, and which presuppose delivery that does not exist.**

**Q5. THE WITNESS.** Given the attempt above did not fire, is a guest-path reproduction achievable
at all — and if so, does it need the UART driven by guest instructions rather than by debugger
writes? **If you believe no witness is achievable without the dispatch arm, say so plainly**; that
is a real answer and it makes this documented-only until the larger change lands.
