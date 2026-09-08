# alphatbinegsel Q3 -- does the selected branch differ in EFFECT?

## 0. READING SCOPE -- widened deliberately, at your request

My previous brief scoped you away from the invalidation implementation, and you correctly said Q3
could not be settled inside that scope. Read these:

* `src/cpus/cpu_alpha_palcode.c` -- the `tbi` handler (PAL_OSF1_tbi, case 0x33)
* **whatever implements `cpu->invalidate_translation_caches` for Alpha** -- find it; I believe the
  binding is set in `src/cpus/cpu_alpha.c` and the implementation may be shared dyntrans code, but
  do not take either from me
* `src/cpus/cpu_dyntrans.c` and `src/include/cpu.h` as needed to follow that call
* `src/include/thirdparty/alpha_cpu.h` for the selector definitions

Please still avoid `regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree under review: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root.

## 1. WHAT IS ALREADY SETTLED -- do not re-derive, but do say if any of it is wrong

You established these in the previous pass and I am inlining them so this brief stands alone:

* the handler is `case 0x33: /* PAL_OSF1_tbi */`, and the dispatch is

      if (a0 >= 1)
              cpu->invalidate_translation_caches(cpu, a1, INVALIDATE_VADDR);
      else
              cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);

* `a0` is a `uint64_t` local, copied from `cpu->cd.alpha.r[ALPHA_A0]`, which is also `uint64_t`.
  There is no active signed cast; the cast in the commented-out `debug()` has no effect.
* therefore selectors **-1 and -2 take the VADDR branch**: `-2 -> 0xff..fe >= 1` is true.
* `src/include/thirdparty/alpha_cpu.h` defines `ALPHA_TBIA() = alpha_pal_tbi(-2, 0)` ("all TB
  entries") and `ALPHA_TBIAP() = alpha_pal_tbi(-1, 0)` ("all per-process"), so the negative
  selectors are explicitly specified and mean *invalidate broadly*.
* selector `0` is not defined by the header; its fallback to INVALIDATE_ALL is not a header
  requirement.

## 2. THE ONE QUESTION

**Q3. Does `invalidate_translation_caches(cpu, a1, INVALIDATE_VADDR)` differ IN EFFECT from
`invalidate_translation_caches(cpu, 0, INVALIDATE_ALL)` on Alpha?**

Quote the implementation. I want one of these three answers, whichever is true:

* **(a) YES, they differ** -- the VADDR form invalidates only entries matching `a1` and the ALL form
  clears the whole cache. Then `ALPHA_TBIA()` really does flush almost nothing, and the row is a
  live functional defect. Say what a guest would observe: stale translations surviving a flush the
  OS believes succeeded.
* **(b) NO, they are the same** -- e.g. the Alpha binding ignores the flags, or both paths reach the
  same full flush. Then the source is still wrong but the defect is **unobservable**, and I want
  that said plainly rather than dressed up. A row that cannot be observed is documented-only here.
* **(c) It depends on state I have not given you** -- name the state.

**Q4. Given your answer, is there a WITNESS?** This project's ladder wants a real guest instruction
through real dispatch on an unmodified in-tree machine, red before the fix and green after with the
same script, plus a liveness control. If Alpha has no bootable in-tree rig that exercises paging,
say so -- a "no witness constructible, and here is why" is a real answer and the round would then be
documented-only rather than blocked.

**Q5. Is `if (a0 >= 1 && a0 <= 3)` still your recommended repair after reading the implementation?**
If the two branches turn out equivalent, the repair is arguably a no-op that only improves the
source's honesty -- which is a different disposition and a different CHANGELOG claim. Say which.

**Please do not simply ratify.** If anything in section 1 is wrong -- including something you
yourself told me last pass -- say so. I would rather lose the finding than ship it on a premise that
does not hold.
