# `alphatbinegsel` fix design — the witness is built, so this is about the guard and the detector

**VERDICT LINE FIRST.**

**The tree is `GXEMUL-SEC/src/`** — ignore the pristine 2021 copy at the project root.

**Please do not simply ratify.** Every fact in section 2 was corrected at least once on the way
here, and one of them was corrected by a seat reading the asm rather than the comment beside it.
**Check the premises, not just the derivations.**

## 1. THE DEFECT — settled, and now WITNESSED

`src/cpus/cpu_alpha_palcode.c`, `case 0x33 /* PAL_OSF1_tbi */`:

```c
	if (a0 >= 1)
		cpu->invalidate_translation_caches(cpu, a1, INVALIDATE_VADDR);
	else
		cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);
```

`a0` is a **`uint64_t`** captured at `:165`. `ALPHA_TBIA()` is `alpha_pal_tbi(-2, 0)` and
`ALPHA_TBIAP()` is `alpha_pal_tbi(-1, 0)`, so both compare `>= 1` as TRUE and take the **VADDR**
branch with `a1 = 0` — invalidating cached virtual page **zero** and nothing else.

**THE WITNESS IS BUILT AND RE-VERIFIED**
(`regress/artifacts/alphatbinegsel/witness_agy_20260908/`):

    row          got               want              note
    live         alive             alive             CONTROL: session survives              ok
    tbia fill    0xaaaa0000aaaa    0xaaaa0000aaaa    CONTROL: initial walked load cached    ok
    tbia obs     0xaaaa0000aaaa    0xbbbb0000bbbb    TBIA (a0=-2) must flush and re-walk   FAIL
    tbiap fill   0xcccc0000cccc    0xcccc0000cccc    CONTROL: initial walked load cached    ok
    tbiap obs    0xcccc0000cccc    0xdddd0000dddd    TBIAP (a0=-1) must flush and re-walk  FAIL
    pos fill     0xeeee0000eeee    0xeeee0000eeee    CONTROL: initial walked load cached    ok
    pos obs      0xffff0000ffff    0xffff0000ffff    CONTROL: a POSITIVE selector (a0=2)    ok

**committed 5/7 → fixed 7/7**, same script, unmodified `-E alpha -e alphabook1`. Built by the
measurement seat and **re-run independently against `build/`, reproducing 5/7 with the identical
two failures**. `pos obs` is the attribution control: a positive selector flushes correctly on
**both** builds, so the VADDR path works and the failures are the misdispatch.

## 2. WHAT IS SETTLED — say if any of it is wrong

* **The proposed fix is `if (a0 >= 1 && a0 <= 3)`**, sending both negative selectors to
  `INVALIDATE_ALL`. Confirmed 4/4 by the assess panel and measured 7/7 by the witness.
* **It is COARSE and cannot be otherwise in this tree.** The manual documents the real semantics —
  `21066_66a_hrm.txt:1486`: *"Write operations to the ITBASM register invalidate all entries that
  do not have the ASM bit set."* But `grep -rn ALPHA_PTE_ASM src/` returns **ONE hit, the `#define`
  at `alpha_cpu.h:223`** — nothing consumes it, and `apcb_asn` is written by `swpctx` and read by a
  debug print only. **So ASM=0 selectivity has no representation in the translation cache at all.**
* **The five documented selectors** are `TBIA(-2)`, `TBIAP(-1)`, `TBISI(1)`, `TBISD(2)`, `TBIS(3)`.
* **`#514` did NOT touch this flush** — `git diff --format= 3031a30^ 3031a30 -- <file> | grep -cE
  '^[+-].*invalidate_translation_caches'` is **0**. An earlier claim that this row owed a
  re-baselined witness was withdrawn.
* **The architectural FAULT disposition is unavailable on Alpha**, and `ALPHA_KENTRY_MM`,
  `ALPHA_FEATURE_BWX` and `kentry[]` are all declared-but-unconsumed in this layer — so do not
  assume a mechanism exists because a constant names it.

## 3. QUESTIONS

**Q1. IS `a0 >= 1 && a0 <= 3` THE RIGHT GUARD?** In particular: what should happen for `a0 == 0`,
and for `a0 >= 4` or other undocumented values? The proposed guard sends all of them to
`INVALIDATE_ALL`. **Is over-invalidation the right default for an undocumented selector, or should
an unknown selector be announced?** Note the error direction: over-invalidation costs re-walks and
never stale data — the exact opposite of the defect.

**Q2. SHOULD THE GUARD BE WRITTEN AGAINST THE SIGNED VALUE INSTEAD?** `(int64_t)a0 >= 1 &&
(int64_t)a0 <= 3` reads closer to the architecture's own description and makes the negative
selectors obviously negative. **Which form is less likely to be broken by a later edit**, and does
either change behaviour for any input?

**Q3. WHAT DOES THE DETECTOR OWE BEYOND THE WITNESS?** The witness has three fill/observe pairs and
a positive-selector control. **Name the smallest edit to the repaired guard that the witness would
NOT catch** — and say whether it is worth a row or belongs in a disclosed contract.

**Q4. WHAT OBSERVABLE DISTINGUISHES A CORRECT FIX FROM AN INCOMPLETE ONE?** Specifically: the fix
does not implement ASM selectivity. **What should a regression row assert so that a later partial
ASM implementation does not read as complete?**

**Q5. THE CHANGELOG SENTENCE.** Given the ASM finding, is the honest claim *"we shipped a coarse
repair and deferred the finer semantics"*, or the stronger *"the finer semantics have no
representation in this emulator's translation cache"*? **Write the sentence you would ship.**
