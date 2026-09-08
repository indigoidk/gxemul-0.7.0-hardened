# WHICH ISA DEVICES ON `alphabook1` CAN ASSERT AN INTERRUPT, AND WHAT GUEST ACTION PRODUCES EACH?

**VERDICT LINE FIRST**, then the body.

Scope your reading to **`GXEMUL-SEC/src/`**. Ignore any other `src/` under the project root — there
are three pristine 2021 upstream copies and they give line numbers off by hundreds.
**Do not read `regress/artifacts/` or `tools/pipeline/ledger.json`.**

This is a **reachability census**, not a design task. I want an inventory and a control-flow answer.
**Do not write a probe, choose register values, or propose a code change.**

## Background, stated so you can check it rather than assume it

`machine_alpha.c` instantiates the LCA chipset for `ST_ALPHABOOK1` only. `DEVINIT(lca)` calls:

```c
    bus_isa_init(devinit->machine, interrupt_path,
        BUS_ISA_IDE0 | BUS_ISA_IDE1, LCA_ISA_BASE, LCA_ISA_MEMBASE);
```

and `bus_isa.c` registers sixteen ISA interrupt lines `<base>.isa.0` … `<base>.isa.15`, with
`wdc0_irq = 14` and `wdc1_irq = 15`.

**I believe `bus_isa_init` instantiates a fixed set of devices regardless of the flags, plus extra
ones the flags select. I have not verified that.** The flag set passed here is only
`BUS_ISA_IDE0 | BUS_ISA_IDE1`.

## Questions

1. **ENUMERATE the devices `bus_isa_init` actually creates for this flag set**, and for each one
   give: its ISA IRQ line, and **what makes it assert** — a guest register write, a host timer
   callback (`timer_add` / SIGALRM), a disk operation completing, console input, or something else.
   A table is the ideal answer. **Give the denominator**: how many `device_add` / instantiation
   calls you examined in `bus_isa_init`.

2. **Which of those asserts are SYNCHRONOUS with a guest instruction** — i.e. the assert happens
   inside the guest's own load or store — and which depend on a host timer callback? This
   distinction matters to me and is the main thing I am asking. In this tree,
   `debugger.c` calls `timer_stop()` while the user is interacting and `step N` returns before
   `timer_start()`, so a host-timer-driven event does no work under single-stepping while a
   synchronous one does.

3. **For the wdc (IDE) path specifically:** `DEVICE_TICK(wdc)` is
   `if (d->int_assert) INTERRUPT_ASSERT(d->irq);`. **What sets `int_assert`, and is that setter
   reachable from an ordinary guest register write with no OS booted?** Name the function and the
   register. If it requires a disk image to be attached, say so and say what happens when none is.

4. **Is the PIT/8253 (IRQ 0) instantiated here**, and if so is its assert host-timer-driven? The
   deassert path in `bus_isa.c` has a special case commenting "If IRQ 0 has been cleared, then this
   is a timer interrupt", which suggests it is present — but that is my inference from a comment,
   which is exactly the kind of premise I want checked rather than confirmed.

5. **What are the guest-visible I/O addresses** of the devices you list, on this machine? I am
   asking for the mapping arithmetic (`LCA_ISA_BASE` plus the ISA port offset), not for advice on
   what to do with it.

6. If, while checking this, you found something **else** about how ISA interrupts are routed on this
   machine — say so.

## Rules

* Answer from the source; name file and function for every behaviour you assert.
* Where you are inferring rather than reading, say which.
* A clean "your premise in Q4 is wrong because X" is the most useful answer you can give.
