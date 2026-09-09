# Alpha interrupt delivery — an analysis question, not a design one

**Answer in prose. Do not propose a code change, do not write a test, and do not construct any
input sequence.** I want the analysis; I will decide the disposition myself.

## Read only these files (and grep the tree for the idioms the questions name)

    src/devices/dev_lca.c
    src/cpus/cpu_alpha.c   src/cpus/cpu_alpha_palcode.c   src/include/cpu_alpha.h
    src/devices/bus_isa.c
    src/cpus/memory_rw.c
    plus, for comparison, any ONE device that forwards interrupts on a working architecture

Do not read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md` or anything under
`_scratchpad/`. Those are project records, not code.

## Please do not simply ratify

Check the premises below rather than reasoning from them. **Where a claim is about a COUNT or a set
of call sites, enumerate it — grep and report the number.** State plainly anything you cannot settle
from the source.

**VERDICT LINE FIRST.**

## What I believe, stated so you can refute it

1. `dev_lca.c` defines `lca_interrupt_assert` and `lca_interrupt_deassert`, and both are stubs whose
   entire body is a diagnostic followed by process termination — **with no guard at all**, so there
   is no value being refused and no condition selecting the stub.
2. `DEVINIT(lca)` registers those two functions as the interrupt callbacks that `bus_isa_init` wires
   up, so an ordinary ISA interrupt reaches them.
3. There is no Alpha equivalent of the bus-error/exception dispatch that `memory_rw.c` performs for
   MIPS and M88K.

## The questions

**Q1. Is premise 3 true?** Enumerate what `memory_rw.c` does on a failed device access, per
architecture. If Alpha genuinely has no exception-delivery path there, say what a correct one would
have to touch — name the functions and registers, do not write them.

**Q2. What does the Alpha CPU model already have for interrupt delivery?** Is there any existing
mechanism — an interrupt-pending field, a PALcode entry, an IPL check — that a device could raise
into today? Name what exists and what is missing. This is the question I most need answered: I want
to know whether forwarding is a small wiring job or a missing subsystem.

**Q3. How do comparable host bridges on OTHER architectures in this tree forward an ISA interrupt?**
Pick one and describe its path from the device callback to the CPU. I am looking for the in-tree
idiom, because a repair matching an existing idiom is worth far more than one argued from first
principles.

**Q4. Which machines instantiate the LCA device, and what else do they wire to those callbacks?**
If only one machine does, say so; if the callbacks are shared, say which paths reach them.

**Q5. Given all of the above, is a partial repair coherent?** Specifically: if the diagnostic were
kept but bounded, and the termination removed, would the resulting behaviour be *coherent* (the
machine keeps running with interrupts silently dropped) or *incoherent* (some other part of the
model now blocks forever waiting for an acknowledgement that cannot come)? Name what you checked.
