# `irqassertedunread` -- three CPU families set an interrupt-pending flag that nothing reads.  2026-09-06.

## WHAT THIS IS
An ordinary correctness review of a CPU dispatch loop in a hardware simulator for obsolete workstations
(GXemul 0.7.0, a maintained fork).  Plain engineering vocabulary; no security framing is intended or wanted,
and none of this concerns a production system.

**The tree under review is `GXEMUL-SEC/src/`.  Ignore any other `src/` you find** -- three pristine-2021
upstream copies sit under the project root and are NOT this fork; one of them bit the main loop last week.
Cite by grep anchor, not line number.  **VERDICT LINE FIRST.**

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
This came out of an unrelated design pass as a side remark, and I have done only the cheap census below.  **The
obvious failure mode is that I have found a real gap in two architectures and a deliberate design decision in
the third, and cannot tell them apart from a grep.**  Check the premises, not just the derivation.

## THE CENSUS (run tonight; re-derive it, do not trust it)

    grep -rn 'irq_asserted' --include=*.c --include=*.h src/

**SIX families SET `cpu->cd.<arch>.irq_asserted`** -- alpha, arm, i960, m88k, ppc, riscv -- each in its own
`*_irq_interrupt_assert`/`_deassert` pair, and each declares the field in its `include/cpu_<arch>.h`.

**THREE are CONSUMED**, all in `cpu_dyntrans.c` (plus one more for ppc in `cpu_ppc.c`):

| family | consumer |
|---|---|
| arm   | `cpu->cd.arm.irq_asserted && !(cpu->cd.arm.cpsr & ARM_FLAG_I)` |
| m88k  | `cpu->cd.m88k.irq_asserted && ...` (twice: the dispatch guard and a second site) |
| ppc   | `cpu->cd.ppc.irq_asserted && cpu->cd.ppc.msr & PPC_MSR_EE`, and `cpu_ppc.c` |

**THREE ARE NOT CONSUMED ANYWHERE: `alpha`, `i960`, `riscv`.**  The assert path stores 1, the deassert path
stores 0, and no read of those three fields exists in the tree.

## WHY THIS SURFACED
A design pass on `dev_lca.c` (the Alpha chipset bridge) found its two interrupt callbacks are bare
`fatal("...TODO"); exit(1)` stubs with no guard.  The reviewing seat observed that **removing those exits could
not complete the path anyway**, because the Alpha flag they would feed is never consumed.  That is what
prompted this census, and it widened to three families.

## THE QUESTIONS
1. **Is this a real capability gap, or is delivery routed differently on those three?**  I checked only for
   reads of `irq_asserted` itself.  A family might deliver interrupts through an entirely different mechanism
   -- a per-CPU pending mask, a device-side check, an `int_asserted` cousin under another name -- in which case
   the field is DEAD rather than the capability being absent.  **Those are very different findings and I cannot
   separate them from this grep.**
2. **If the capability is genuinely absent, what is the guest-visible consequence for each family?**  Name it
   concretely: does a timer tick simply never arrive, does a driver hang waiting, or does the machine not boot
   far enough to care?  A capability absent on a machine nobody boots is different from one that silently
   changes a booting guest's behaviour.
3. **Is the field DEAD CODE that should go, or a HOLE that should be filled?**  For each of the three.  If
   riscv is an incomplete port and alpha is a complete one, those want opposite dispositions.

## THE SECOND QUESTION, with the count named
Of my three premises -- (i) six families set it; (ii) exactly three are consumed, all in `cpu_dyntrans.c` plus
`cpu_ppc.c`; (iii) alpha, i960 and riscv have no consumer anywhere -- **WHICH IS WRONG?**  Assume at least one
is: this census used a single grep on a single identifier, which is exactly the correlate-not-the-class
mistake that has produced four wrong counts in this project.

VERDICT LINE FIRST (`REAL GAP: <which families>` / `DEAD FIELD: <which>` / `PREMISE <n> IS WRONG: <what>`),
then the per-family disposition, then anything else.  Under a page.
