# alphatbinegsel -- does the TLB-invalidate selector lose its negative cases?

## 0. READING SCOPE

Read only:

* `src/cpus/cpu_alpha_palcode.c` -- the `tbi` handler
* the header that defines the selector constants (find it; I believe it is under
  `src/include/thirdparty/`, but do not take that from me)
* `src/cpus/cpu_alpha.c` / `src/include/cpu_alpha.h` only if the register plumbing is needed

Please do NOT read `regress/artifacts/` or `tools/pipeline/ledger.json`.

The tree under review is `GXEMUL-SEC/src/`. There is another `src/` at the project root which is
pristine 2021 upstream -- ignore it. Line numbers disagreeing with this brief by hundreds mean you
have the wrong copy.

## 1. THE QUESTION

Ordinary emulator-correctness review of an operand's signedness. An earlier seat wrote, on a brief
about something else:

> *"Local `a0` is unsigned. Enumerating the comparison gives `-2 -> VADDR`, `-1 -> VADDR`,
> `0 -> ALL`, `1 -> VADDR`, `2 -> VADDR`, `3 -> VADDR`. The header's independent definitions require
> all-entry and all-per-process invalidation for the negative selectors."*

**I have NOT verified this.** It is one comparison plus the header's constants, and I am asking you
to check it rather than to agree with it.

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise the brief
had stated wrongly. **Check the premises, not just the derivations.** In particular I may have the
selector encoding, the type, or the header wrong.

## 2. WHAT I WANT BACK -- VERDICT LINE FIRST

**Q1. Quote the actual `tbi` handler** and say what type the selector operand has at the point of
comparison, and where that type comes from (the register array's declared type, a local, a cast).
Then enumerate the comparison for selectors -2, -1, 0, 1, 2, 3 and say which branch each takes.

**Q2. Quote the header's definitions** of the selector constants, with the file path. If the header
does not define negative selectors, say so plainly -- that would refute the row, and I would rather
learn that now.

**Q3. Does the branch actually taken differ in EFFECT from the one the header specifies?** This is
the part that decides whether the row is real. A branch that invalidates a single virtual address
where the specification calls for invalidating all entries is a difference; a branch that reaches
the same flush by another route is not. Say which this is, and quote the flush code.

**Q4. What is the smallest correct repair, and what would OBSERVE it?** Note the emulator may not
model a TLB in a way that makes the difference visible from a guest -- if the invalidation is a
no-op or a full flush regardless of selector, then the defect is real in the source and
**unobservable**, and I want that said rather than papered over. Name a channel or say there is
none.

## 3. THE CLUSTER QUESTION -- this one is scoping, not correctness

Six Alpha rows are open, all found in the last two days, all in adjacent code:

    alphatbinegsel    this one -- the tbi selector comparison
    alphaswpctxreg    swpctx stores the old context in a0; the ABI wrapper reads v0, and the
                      comment directly above the store says v0.  ALREADY VERIFIED by me
    alphactxfail      swpctx's context save and load do not check whether the memory accesses
                      succeeded
    alphapteprot      the page walk returns the same protection value for every successful walk,
                      so memory_rw caches every walk identically
    alphafaultclaim   a comment claims a failed page-table walk makes the caller raise a fault;
                      the row says that is unsupported by the code
    alphavmkill       one guest virtual address reaches an unrecoverable error path

**Q5. How many ROUNDS is this?** The project's round-scope rule is: a round takes ONE site; a second
joins only if it is in the same file and same semantic class, covered by one fix design and one
detector with no new oracle. More findings create more candidate rounds, never bigger rounds.

Group them, and say for each group what the ONE fix design and the ONE oracle would be. If a group
needs two oracles it is two rounds -- say so. **I would rather have five small rounds than one that
cannot state its detector.**

**Q6. Which of the six should go FIRST, and why?** Rank by severity and by whether a witness is
constructible, not by how easy the edit is. If one of them is a prerequisite for testing the others
-- for instance if the page-walk row governs whether any Alpha guest paging path is exercisable at
all -- that ordering matters more than severity and I want it named.
