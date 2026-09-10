# `crimewidthkill` + `vmedefaultkill` -- the two rows where FAULT is actually AVAILABLE: is it the right member?

Nonce: `CODEX_FAULTPAIR_20260910`. Open with `VERDICT:` giving your disposition for EACH site separately,
then echo the nonce.

Ordinary robustness maintenance on an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under the
project root, so line numbers off by hundreds mean you are reading one of those. **Verdict line first.**

**Please do not simply ratify.** Three briefs of mine this week have had premises refuted by a seat that
opened the file, and each refutation improved the round. **Check the premises, not just the derivations.**

## WHY THESE TWO ARE ONE BRIEF

This project's disposition menu is {delete, silent decline, decline + latched announce, accept, fault,
backed accept, implement}, and it has a standing caution that **FAULT is usually UNAVAILABLE**:
`memory_rw.c` converts a failed device callback into an architectural access exception for **MIPS and
M88K only**. Almost every round in this queue therefore reaches for DECLINE by default.

**These two sites are the exception -- one is on MIPS and one is on M88K -- so for once the choice is
real.** I want it made deliberately rather than by habit. They are separate rounds; I am asking one
question about both because the question is the same.

## SITE A -- `crimewidthkill`, MIPS

`src/devices/dev_sgi_ip32.c`, grep anchor `fatal("crime access len = %i!\n", len);`. The handler is
`if (len == 8) {...} else if (len == 4) {...} else { fatal(...); exit(1); }`. **Every other access length
-- 1, 2, and anything wider -- ends the emulator.** `machine_sgi.c` installs it via `dev_crime_init(...,
0x14000000, ...)` on the IP32 machines; CRIME is the memory and interrupt controller.

## SITE B -- `vmedefaultkill`, M88K

`src/devices/dev_vme.c`, the `default:` arm. It announces with **`debug()`** -- which has an early-out and
is therefore invisible at default verbosity -- and then calls `exit(1)`. **So the emulator dies with no
output explaining why.** `machine_mvme88k.c` installs it unconditionally at `VME2_BASE`.

## THE QUESTIONS

1. **PREMISES AS QUESTIONS.** Are the guards really as I describe? Is `len` really unconstrained at Site
   A, or does something upstream restrict it -- and if so, which access widths can a guest actually
   present to a device handler on MIPS? At Site B, is the `default:` arm really reachable, and is
   `debug()` really silenced at default verbosity in the way I claim? **If either kill is unreachable,
   say so with the warrant; a dead path recorded with its reason is a result rather than an absence.**
2. **FAULT OR DECLINE, PER SITE, WITH A REASON THAT IS NOT AESTHETIC.** `return 0` from these handlers
   delivers a real bus error to the guest. Is that what the hardware does? **Grep the fork for
   `dev_unreadable.c` and for how `machine_sgi.c` uses it** -- that device's whole access function is
   `return 0`, and it is installed ten times so that absent hardware faults, because the PROM and NetBSD
   probe those regions and RELY on the failure. Does that precedent transfer to a REGISTER-WIDTH refusal
   and to an UNIMPLEMENTED-REGISTER refusal, or is it only about absent address space?
3. **THE HAZARD I MOST WANT CHECKED: does a bus error here break a guest that currently works?** These
   are not absent devices; they are present devices refusing one access. A PROM that probes a register
   width and gets a machine check may behave worse than one that gets a benign zero. **Say which guests
   in this tree touch these paths**, and whether returning failure is observably safer than returning
   zero quietly.
4. **SITE B HAS A SECOND DEFECT INSIDE THE FIRST, and I want it disposed explicitly.** Whatever member
   you choose, the `debug()` announcement is the wrong level for an event that ends or refuses a guest
   access -- every sibling kill in this queue uses `fatal()`, which this fork has measured cannot be
   silenced by `-q`. Should the round promote it? That is a second change and must be deliberate rather
   than inherited.
5. **THE DETECTOR, per site.** The vacuity floor requires failing on the pre-fix build, on a verbatim
   reinstatement of the removed kill, on a null medium, AND on a NULLED REPAIR. Name the rows and per row
   **the mutant it kills and the observable that differs under it.** Two traps to route around: *"the
   host survived"* is not a channel at a refusal site, since guarded and unguarded code both survive once
   the kill is gone; and if you choose FAULT, the observable is an ARCHITECTURAL EXCEPTION in the guest,
   which is a different oracle from a returned value and needs its own liveness control.
6. **WHAT ELSE IS FATAL IN THESE TWO FILES**, and which of it belongs to these rounds versus a separate
   one?
7. If you found something else, say so.

Read-only: no builds, no probe runs, no edits, no patches. Prose and tables only.
