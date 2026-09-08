# swpctx returns the old context in the wrong register — one identifier, and I want the round scoped

**VERDICT LINE FIRST.**

You may not be able to open files, so **every fact is inlined**. If a premise cannot be settled from
this packet, **say so plainly** rather than assuming it.

**The tree under review is `GXEMUL-SEC/src/`** — ignore any other `src/` at the project root; a
pristine 2021 upstream copy lives there and reports line numbers off by hundreds.

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise a brief
had stated wrongly, and this week a seat of mine narrowed a claim instead of challenging it, which
hid the defect. **Check the premises, not just the derivations.**

## 1. THE SITE — `src/cpus/cpu_alpha_palcode.c:250-251`, verbatim

```c
		/*  Return old context in v0.  */
		cpu->cd.alpha.r[ALPHA_A0] = cpu->cd.alpha.ctx;
```

**The comment directly above the line says v0. The line writes a0.**

## 2. WHAT I VERIFIED MYSELF — census, with denominators

* **`ALPHA_V0` is the file's return convention, 8 sites:** lines 118, 204, 306, 339, 344, 356, 361
  and 383 all assign `cpu->cd.alpha.r[ALPHA_V0] = ...` as the handler's result.
* **`grep -n "r\[ALPHA_A0\] =" src/cpus/cpu_alpha_palcode.c` returns EXACTLY ONE LINE — 251.**
  So this is not a local convention; it is a population of one against a population of eight.
* **`ALPHA_V0` exists and is not a missing symbol** — it is used correctly a hundred lines above.
* **The ABI wrapper confirms the intent independently.** `alpha_pal_swpctx` in
  `src/include/thirdparty/alpha_cpu.h:449-459`:

```c
static __inline unsigned long
alpha_pal_swpctx(unsigned long ctx)
{
	register unsigned long a0 __asm("$16") = ctx;
	register unsigned long v0 __asm("$0");

	__asm volatile("call_pal %2 # PAL_OSF1_swpctx"
		: "=r" (a0), "=r" (v0)
		: "i" (PAL_OSF1_swpctx), "0" (a0)
		/* clobbers t0, t8..t11, a0 (above) */
		: "$1", "$22", "$23", "$24", "$25", "memory");
```

  **`v0` is `$0` and is an output. `a0` is declared an in-out operand and the comment calls it
  clobbered.** So a correct guest reads the result from v0 and must not rely on a0 — and the model
  writes the result into the register the guest is told to discard, leaving v0 untouched.

* **Ordering in the handler is correct and is NOT part of this defect:** `:251` publishes the OLD
  `ctx` before `:255` overwrites it with the new one (`cpu->cd.alpha.ctx = a0;`).

* **This arm has history:** `#507` fixed a field-name transposition in the same block (`apcb_ptbr`
  assigned twice, `apcb_flags` never). That fix is present and is not in question here.

## 3. WHAT I HAVE **NOT** ESTABLISHED — please treat these as open

* **Reachability.** I have not shown that any guest this project boots calls `swpctx` AND consumes
  the return value. The wrapper exists in the OS header; that is not the same claim.
* **Guest-visible consequence.** The caller reads whatever v0 happened to hold. I have not
  characterised what that is in practice, nor whether any supported guest branches on it.
* **No witness exists.** `witness` is `None` on this row.

## 4. QUESTIONS

**Q1. Is the one-identifier fix — `ALPHA_A0` -> `ALPHA_V0` — correct AND sufficient?** In
particular: should the handler *also* do something to a0, since real PALcode clobbers it and the
wrapper declares it clobbered? Is leaving a0 holding the old context a second (smaller) fidelity
defect, or is it unobservable by construction because no correct caller may read it?

**Q2. SEVERITY.** The row is `med`. A documented PALcode primitive returning its result in the
wrong register, silently, is a wrong-value defect rather than a crash — the harder kind to notice.
**Confirm `med`, or argue up or down.** *Note a related row, `alphatbinegsel`, was raised med -> high
by me this week and the panel confirmed the raise; I do not want that to anchor this one.*

**Q3. REACHABILITY — this is the question that decides whether the round can have a witness.** Can
a guest on unmodified `-E alpha -e alphabook1` reach `swpctx` and observe v0? If you can name the
call path, do. **If you conclude it is not reachable in a booting guest today, say so plainly** —
that is a real answer and it makes this documented-only.

**Q4. WITNESS SHAPE.** If reachable: what is the smallest rung-3 probe? Note two traps this project
has measured on the neighbouring Alpha row: the debugger ALL-FLUSHES between interactions, so a
multi-step sequence must sit inside ONE `step N`; and an oracle that reads back a value which
happens to match the pre-fix value is vacuous. **What must the probe seed v0 with so that "the
handler did nothing to v0" is distinguishable from "the handler wrote the right thing"?**

**Q5. SCOPE.** `:296` in the same arm is `cpu->invalidate_translation_caches(cpu, 0,
INVALIDATE_ALL);` carrying the comment `// TODO: Don't invalidate EVERYTHING!`. A seat reviewing
the neighbouring row warned that swpctx IS the context-switch PAL and that whichever of the two
rows lands second must re-baseline its witness with the other's fix present. **Does that TODO
belong in this round, or is it a separate row?** This project's rule is that a round takes ONE
site, and a second joins only if it is witnessed, in the same semantic class, and covered by the
same detector with no new oracle.
