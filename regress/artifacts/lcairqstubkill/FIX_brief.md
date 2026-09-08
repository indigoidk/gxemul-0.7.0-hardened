# WHAT SHOULD `lca_interrupt_assert`/`_deassert` DO, AND WHAT ROW DISCRIMINATES THE OPTIONS?

**VERDICT LINE FIRST.** Scope to `GXEMUL-SEC/src/`; ignore any other `src/` under the project root.
**Do not read `regress/artifacts/` or `tools/pipeline/ledger.json`.** Do not write a probe.

## The situation, established by reading and by one measurement

`dev_lca.c` has two interrupt handlers whose entire bodies are `fatal("...TODO\n"); exit(1);` with
no predicate. `DEVINIT(lca)` registers them for `"<machine>.lca"` and hands that same path to
`bus_isa_init`, so every ISA interrupt routes into them. Measured on unmodified `alphabook1`: four
guest instructions ending in a store of `0xAA` to the 8042 command port (`0x1d0000064`) reach
`lca_interrupt_assert` and end the process. A matched control storing the same value to the LPT port
(which never asserts) survives.

## The option set this project uses for a terminating stub

1 DELETE · 2 DECLINE (silent) · 3 DECLINE + bounded/latched announce · 4 ACCEPT ·
5 FAULT · 6 BACKED ACCEPT · 7 IMPLEMENT.

**Members 1–6 all presume a VALUE is being refused. Here there is none** — it is an entire path
stubbed out, which is why member 7 was added to this set from these very functions.

## Questions

1. **What would a correct implementation look like?** The Alpha CPU has an interrupt mechanism; what
   would these two functions have to do to deliver an ISA interrupt to the guest CPU on this
   machine? Name the CPU-side entry point and what state it needs. If the Alpha CPU model in this
   tree cannot accept an asynchronous interrupt at all, **say that plainly** — it changes everything.

2. **Is there an in-tree precedent to copy?** Other chipsets register interrupt handlers that
   forward to a CPU. Name one whose shape transfers, and say what it does that these must also do.

3. **If a full implementation is out of scope, what is the honest interim?** A silent return loses
   interrupts invisibly. A latched announce loses them audibly, once. Which does this tree's own
   practice favour for an unimplemented delivery path, and is there a third option I have not named?

4. *** THE ONE I MOST NEED. *** A witness that only checks "the host survived" **cannot tell these
   apart** — a silent return, a latched announce and a real implementation all survive.
   **What OBSERVABLE distinguishes them?** I want a row that is green for the chosen disposition and
   red for the others. If the only honest answer is "none from a stepped probe", say so and say what
   capability would be needed.

5. **The deassert stub is on the same path** (`isa_interrupt_common` calls `INTERRUPT_DEASSERT` when
   the last unmasked IRR bit clears). Does it need the same treatment, or does its correct behaviour
   differ from the assert side?

6. If you found something else about interrupt routing on this machine, say so.

## Rules

* Answer from the source; name file and function for every behaviour you assert.
* Give the denominator: how many interrupt-handler registrations you examined.
* A clean "your framing in Q3 is wrong because X" is the most useful answer you can give.
