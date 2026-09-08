# LCA interrupt delivery: two unimplemented handlers that terminate the process

**VERDICT LINE FIRST.**

**The tree under review is `GXEMUL-SEC/src/`.** Ignore any other `src/` you find — there is a
pristine 2021 upstream copy at the project root that will make you confidently wrong, and it has
bitten this project more than once. Every line number below is from `GXEMUL-SEC/src/`.

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise a brief
had stated wrongly, and on this very row's sibling you refuted two of my premises last night.
**Check the premises, not just the derivations.**

## 1. THE SITE

`src/devices/dev_lca.c:70-86`, complete and unedited:

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

Both are registered as the machine's interrupt template at `dev_lca.c:414-415`:

```c
	interrupt_template.interrupt_assert = lca_interrupt_assert;
	interrupt_template.interrupt_deassert = lca_interrupt_deassert;
```

`machine_alpha.c:61` does `device_add(machine, "lca")`.

## 2. SETTLED PREMISES — inlined so you need not re-derive them, but say if any is wrong

* **There is NO GUARD.** Unlike every other site in this campaign, no predicate rejects a value
  here. The whole function body is the diagnostic and the process exit. This is why the
  disposition menu that fits refusal decisions — decline, latched decline, accept, backed accept —
  **does not apply**: there is no value being refused.
* **A process exit here is not a decline. Returning without effect is also not "modelling an
  absent device"**: the handler was installed, so something asked for delivery.
* **The architectural fault disposition is NOT available on Alpha.** `memory_rw.c`'s device-failure
  path carries `#ifdef MEM_MIPS` and `#ifdef MEM_M88K` arms and nothing else, and
  `ALPHA_KENTRY_MM` is defined with **zero consumers**.
* **A related declared-but-unused constant exists in the same header**: `ALPHA_PTE_ASM`
  (`alpha_cpu.h:223`) has exactly one occurrence in `src/` — its own `#define`. I mention it only
  because it shows this header declares more than the tree implements; do not assume the two facts
  are connected.
* **`fatal()` does NOT exit.** `debugmsg.c:384` — it has no early-out and returns normally. Only
  the explicit `exit(1)` terminates.
* **PRIMARY SOURCE IS NOW LOCAL.** `_scratchpad/21066_66a_hrm.txt` (Alpha 21066/21066A Hardware
  Reference Manual, EC-QC4GB-TE, 13,876 lines) was fetched yesterday and its citations were
  verified by reading. Relevant sections by line: **§4.1.13 Interrupt Request and Enable Registers
  at `:175`** (HIRR `:177`, SIRR `:179`, ASTRR `:181`), **`:1551`** on the hardware interrupt
  request register, and **§6.4.13 Interrupt Vector and Special Cycle Register at `:510`**.
  *I have NOT read these sections beyond their headings.* You have the file — read them.

## 3. QUESTIONS

**Q1. REACHABILITY, and this is the one that decides severity.** Trace who can call the installed
template. Can an ordinary guest running on `-E alpha -e alphabook1` cause an assert on line 0 (the
ISA interrupt) during normal operation? Name the call path or state plainly that you could not find
one. **If it is unreachable today, say so — that is a real answer and it changes the disposition.**

**Q2. WHAT SHOULD THESE FUNCTIONS DO?** Read §4.1.13 and §6.4.13 in the local manual and say what
the hardware's interrupt request path actually is. Then say what the minimum honest implementation
is in this model, given that the fault disposition is unavailable. Distinguish clearly between
what the manual states and what you are inferring.

**Q3. Is there an in-tree idiom to copy?** Other chipsets in `src/devices/` implement
`*_interrupt_assert`/`_deassert`. Name the closest analogue and say whether its shape transfers to
LCA or whether something about LCA makes it unsuitable. **Grep for the idiom rather than reasoning
from first principles — the tree's own precedents are part of the design space.**

**Q4. What observable behaviour distinguishes a correct implementation from an incomplete one?**
Name the specific state or output a regression check should assert, so that a later partial
implementation does not read as complete.

**Q5. If a reproduction is possible, what is its shape?** A guest instruction sequence on an
unmodified in-tree machine description that reaches the site. If you believe none exists, say so
and give the reason — an honest "not reachable from a guest" is the answer I want if it is true.
