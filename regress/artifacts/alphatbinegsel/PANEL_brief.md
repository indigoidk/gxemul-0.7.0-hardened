# alphatbinegsel -- assess panel.  Everything is inlined; do not plan to read files.

**VERDICT LINE FIRST.**

Several seats here cannot open the repository at all, so every fact is inlined below. If a premise
cannot be settled from this packet, **say so plainly** rather than assuming it — an honest "not
checkable from here" is the answer I want.

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise a brief
had stated wrongly. **Check the premises, not just the derivations.**

## 1. THE DEFECT, as two file-reading seats established it

`src/cpus/cpu_alpha_palcode.c`, `case 0x33 /* PAL_OSF1_tbi */`:

    if (a0 >= 1)
            cpu->invalidate_translation_caches(cpu, a1, INVALIDATE_VADDR);
    else
            cpu->invalidate_translation_caches(cpu, 0, INVALIDATE_ALL);

* `a0` is a **`uint64_t`** local copied from `cpu->cd.alpha.r[ALPHA_A0]`, itself `uint64_t`. There
  is **no active signed cast** — the only cast sits inside a commented-out `debug()`.
* `src/include/thirdparty/alpha_cpu.h` defines the OS's own wrappers:

      #define ALPHA_TBIA()     alpha_pal_tbi(-2, 0)     /* all TB entries */
      #define ALPHA_TBIAP()    alpha_pal_tbi(-1, 0)     /* all per-process */
      #define ALPHA_TBISI(va)  alpha_pal_tbi(1, (va))
      #define ALPHA_TBISD(va)  alpha_pal_tbi(2, (va))
      #define ALPHA_TBIS(va)   alpha_pal_tbi(3, (va))

* so `-2` compares as `0xfffffffffffffffe >= 1` → **TRUE** → the VADDR branch, with `a1 = 0`.
* the two branches genuinely differ in `cpu_dyntrans.c`: VADDR keeps an entry only when
  `(vaddr_page & vaddr_mask) == (addr_page & vaddr_mask)`; the ALL branch has **no address test**
  and walks every valid entry.
* Alpha uses 8 KiB pages and `vaddr_mask` defaults to `(int64_t)-1` (all ones).

> **THEREFORE `ALPHA_TBIA()` — the OS primitive meaning *invalidate every TLB entry* — invalidates
> cached virtual page ZERO and nothing else, or nothing at all if page 0 is not cached.**

The entry helper NULLs `host_load`, `host_store`, `phys_addr`, `phys_page` and clears `valid`, and
the Alpha load/store fast path consumes those pointers — so surviving mappings keep working after a
flush the guest OS believes succeeded.

## 2. WHAT IS ALREADY SETTLED — do not re-derive, but say if any of it is wrong

* **the repair** proposed is `if (a0 >= 1 && a0 <= 3)`, sending both negative selectors to
  INVALIDATE_ALL. It is **COARSE**: it does not give `ALPHA_TBIAP()` its ASM=0 selectivity.
* **a rung-3 witness IS constructible** on unmodified `-E alpha -e alphabook1`, and its shape is
  known: fill a mapping, remap the PTE behind it, `ALPHA_TBIA()`, then load and see the OLD value.
* *** THE TRAP IN THAT WITNESS: the debugger ALL-FLUSHES between interactions *** — when
  `debugger_n_steps_left_before_interaction` is not positive it calls `cpu_create_or_reset_tc` and
  `invalidate_translation_caches`. **So the fill, remap, tbi and observing load must be inside ONE
  `step N`**, or both builds re-walk and the row is green on the defective build.
* **K0SEG is checked BEFORE `ptbr`**, so a K0SEG address never consults the page table — the
  obvious substrate cannot witness this at all.
* **member 5 FAULT is NOT available on Alpha**: `memory_rw.c`'s device-failure path has
  `#ifdef MEM_MIPS` and `#ifdef MEM_M88K` arms and nothing else, and `ALPHA_KENTRY_MM` is defined
  with no consumers.

## 3. QUESTIONS

**Q1. Is the severity right?** I raised this row med → high, and **that ranking is mine, not a
seat's.** A documented OS primitive silently clearing one page instead of all, during ordinary
operation, with a guest then reaching stale physical backing. **Confirm or correct.**

**Q2. Is the COARSE repair the right thing to ship?** It fixes the misdispatch and does not
implement ASM=0 selectivity. Is shipping that — with the limit disclosed — correct, or does the
round owe the finer semantics?

**Q3. What is the smallest edit that reinstates this defect while looking correct?** For example a
guard that still admits `-2` by another route. This is the adversarial question; name a specific
edit.

**Q4. Is there a channel the witness above would MISS?** It observes a stale value after a remap. Is
there a case where the flush is wrong but the value happens to match — and would the row then be
vacuous?

**Q5. Ordering.** Six Alpha rows are open and a file-reading seat ranked `alphaswpctxreg` first on
the ground that this row's consequences were then unverified. **They are now verified.** Does this
row go first instead?
