# alphavmkill -- the last unassessed Alpha row: what should an unmodelled address space do?

## 0. SCOPE

Read `GXEMUL-SEC/src/cpus/memory_alpha.c`, `src/machines/machine_alpha.c`, and whatever else you
need under `GXEMUL-SEC/src/`. Tree under review is `GXEMUL-SEC/src/`; ignore the pristine 2021
`src/` at the project root -- it disagrees by hundreds of lines.

**VERDICT LINE FIRST.**

## 1. THE FILED CLAIM -- treat it as a claim, not a premise

> *"`memory_alpha.c`: a guest virtual address of `0xfffffffd80000000` reaches an unrecoverable
> path -- `fatal()` followed by process termination."*

**I have not verified this.** It is the last of six Alpha rows filed this week and the only one no
seat has assessed.

**Please do not simply ratify.** Five of the other five Alpha assessments refuted at least one
premise I supplied. **Check the premises, not just the derivations.**

## 2. WHAT THE OTHER FIVE ESTABLISHED -- inlined so you need not re-derive

All verified against the source this week, by codex and by me independently:

* `alpha_translate_v2p` handles: KSEG direct-map, a zero-PTBR bootstrap case, and a three-level
  page-table walk. Every SUCCESSFUL return is `2` (`MEMORY_ACCESS_OK_WRITE`); the only PTE checks
  are `ALPHA_PTE_VALID`.
* **There is NO Alpha MM-fault dispatch anywhere.** `ALPHA_KENTRY_MM` and `ALPHA_MMCSR_*` have
  definitions but **no consumers**; `kentry` entries are initialised and assigned, never used to
  dispatch. **Three separate briefs reached that independently** (`alphafaultclaim`).
* so comments in this area claiming the translator or caller "already signalled a fault" are
  **unsupported by the implementation**.
* `_scratchpad/` holds sixteen PDFs and **none is an Alpha reference**, so no architectural claim
  here is locally citable.

## 3. QUESTIONS

**Q1. Is the claim true?** Quote the arm. Which address ranges reach it, and is termination the
actual behaviour or does something recover first?

**Q2. Which member of the option set is right?** The project's standing set:
**1 DELETE · 2 DECLINE (silent) · 3 DECLINE + LATCHED ANNOUNCE · 4 ACCEPT · 5 FAULT · 6 BACKED
ACCEPT · 7 IMPLEMENT.**

*** TWO CAUTIONS THAT ARE NOT RHETORICAL HERE. *** (a) **Member 5 FAULT is not universally
available** -- it works on MIPS and M88K because `memory_rw` dispatches an exception on a failed
device access, and the project has already recorded that **there is no Alpha equivalent**. Given
the no-MM-dispatch finding above, choosing FAULT would oblige building fault delivery first. Say so
if that is your recommendation. (b) **GREP THE FORK FOR THE EXISTING IDIOM** before reasoning from
first principles -- how do the other `memory_<arch>.c` walkers handle an address outside every
modelled space? That census is worth more than an argument.

**Q3. Is this one round or several with the other five?** codex ruled the six Alpha rows are six
separate rounds, no merger having sufficient evidence, and specifically that `alphafaultclaim` and
`alphavmkill` may be grouped *"only after proving they share a file, one fault-handling repair, and
the same fault-delivery oracle."* **The shared missing MM-dispatch is evidence toward exactly that.
Does it now meet the bar, or not?**

**Q4. Is a witness constructible, and can the DEBUGGER reach it?** Note the project's ladder forbids
laundering: a machine or `device_add` introduced *in order to* reach the site is not a witness, and
a debugger `put` that bypasses the guest instruction path is not one either. If the only route is
operator-reachable, say so -- that is a real answer and it caps the severity.

**Q5. Severity, argued rather than asserted.** I have raised one Alpha row to `high` this week
(`alphatbinegsel`, where `ALPHA_TBIA()` invalidates one page instead of all) and left the rest.
**Where does this one sit relative to that?** If it needs a guest already executing privileged code
with a bad address, that is different from a primitive that silently under-flushes during normal
operation.
