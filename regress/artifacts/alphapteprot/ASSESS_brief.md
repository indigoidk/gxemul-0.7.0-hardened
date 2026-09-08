# alphapteprot -- does the Alpha page walk discard protection information?

## 0. READING SCOPE

Read what you need under `GXEMUL-SEC/src/`, in particular `src/cpus/memory_alpha.c`,
`src/cpus/cpu_dyntrans.c`, `src/core/memory.c` and `src/include/memory.h`. Please avoid
`regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree under review: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root.

**This is a source-analysis question about an existing translation function.** I am not asking for a
guest sequence or a way to reach anything.

## 1. THE FILED CLAIM -- treat it as a claim, not a premise

> *"`memory_alpha.c`: the page walk returns 2 for every successful walk, so `memory_rw` caches
> EVERY walk."*

**I have not verified this.** It was filed from another seat's reading during a different brief.

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise a brief
stated wrongly, and you have twice refuted premises of mine when asked to. **Check the premises, not
just the derivations.**

## 2. ONE THING ALREADY ESTABLISHED, inlined so you need not re-derive it

Another seat established, while designing a witness for a different Alpha row, that:

* Alpha RAM is registered `DM_DYNTRANS_OK | DM_EMULATED_RAM`;
* `MEMORY_NOT_FULL_PAGE` is **256**, not 2;
* therefore **a translate return of 2 IS cacheable** -- it is not the sentinel that suppresses
  caching.

So "returns 2 -> gets cached" appears to hold mechanically. **That is not yet the defect.** The
question is whether caching on that return value is WRONG.

## 3. QUESTIONS -- VERDICT LINE FIRST

**Q1. What does the walker actually return, and for which cases?** Quote it. Is `2` returned for
every successful walk, or does it vary with the PTE's protection bits? If it varies, the filed claim
is wrong and I want to know that.

**Q2. What is the return value's CONTRACT?** Find where `memory_rw` (or the dyntrans caching layer)
consumes it and say what each value means -- readable, writable, both, do-not-cache. Give the
authority for that reading: a definition, a comment, or the consuming code's own branches. **If the
contract is nowhere written down, say so** -- that is itself the finding, and this project treats an
undocumented convention read two ways by two readers as a real defect class.

**Q3. If every successful walk returns the same value, what is LOST?** Concretely: can a page whose
PTE denies write access end up cached as writable, so a later guest store succeeds where the
architecture requires a fault? Or is protection enforced somewhere else entirely -- in which case
the constant return is harmless and the row is documented-only.

**Q4. Is there an in-tree comparison?** Other architectures in this tree have their own
`memory_<arch>.c` walkers. Do any of them return protection-dependent values? **The project's rule
is to grep the fork for the existing idiom rather than reason from first principles**, and a sibling
walker that returns varying values would be strong evidence about what this one owes.

**Q5. What OBSERVABLE distinguishes correct from incorrect here?** Not a guest sequence -- just name
the channel. If the honest answer is that Alpha protection is not modelled at all, so nothing can
observe it, say that plainly; the round would then be documented-only, which is a real disposition
here and not a failure.

**Q6. Severity, argued rather than asserted.** If Q3 comes out "a write-protected page becomes
writable", that is a memory-correctness defect. If it comes out "protection is unmodelled
throughout", it is a fidelity gap. Those rank very differently and I would rather you tell me which
than have me guess.
