# `mapledmaaddr` + `xscaleinten` -- ONE CLASS, TWO SITES: is ACCEPT right, and what would make it wrong?

Nonce: `CODEX_ACCEPTCLASS_20260910`. Open with `VERDICT:` giving your disposition for EACH site
separately, then echo the nonce.

Ordinary robustness maintenance on an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under the
project root, so line numbers off by hundreds mean you are reading one of those. **Verdict line first.**

**Please do not simply ratify.** A recent panel here had seven of nine seats confirm a premise the brief
stated wrongly, and two briefs of mine this week have had premises refuted by a seat that opened the file.
**Check the premises, not just the derivations.** These two are stated so you can refute them.

## THE SHAPE, and my claim is that it is ONE class

Both sites compute the CORRECT value into the place the caller will read, and then terminate the process.

**Site A -- `src/devices/dev_dreamcast_maple.c`, anchor `case 0x04:	/*  MAPLE_DMAADDR  */`,** read arm:
```c
fatal("[ dreamcast_maple: TODO: read from dmaaddr ]\n");
odata = d->dmaaddr;
exit(1);
```
The write arm two lines above stores `d->dmaaddr = idata`. `machine_dreamcast.c` adds the device
unconditionally. SH4.

**Site B -- `src/cpus/cpu_arm_coproc.c`, anchor `void arm_coproc_i80321_6`,** crm 0 / crn 0 load arm:
```c
cpu->cd.arm.r[rd] = cpu->cd.arm.i80321_inten;
fatal("TODO: XScale read from inten?\n");
exit(1);
```
The store arm below writes the same field. `machine_iq80321.c` installs the coprocessor explicitly.
**And the ADJACENT `case 4:` (`i80321_isteer`) has the identical structure with NO `fatal()` and NO
`exit()`** -- which I read as the file's own sibling precedent for accepting. ARM.

## MY PROPOSED DISPOSITION, which I want attacked

Option-set member 4, ACCEPT: **delete the diagnostic and the `exit()`, keep the assignment, add no latch**
-- on the grounds that there is no event to announce, and that a bounded announce would ship a wrong
record in product code (an *"unimplemented"* message about a read that is implemented and is not ignored).
Two deleted lines each.

## THE QUESTIONS

1. **PREMISES AS QUESTIONS.** Are the write/store arms really storing the same field the read arm returns,
   in both cases? Is the `case 4:` sibling really structurally identical, or does it differ in a way that
   explains the asymmetry? Are both really installed by real machine constructors? **If the value the read
   arm returns is NOT actually the right one -- stale, never initialised, wrong width, wrong register --
   then ACCEPT is the wrong member and the round is an IMPLEMENT instead. That is the question I most want
   answered.**
2. **IS THE `TODO` TELLING US SOMETHING?** Both carry an author's `TODO` in the message. A `TODO` may mean
   *"I never checked what this should return"* rather than *"this is unimplemented"*. **Check whether
   either register has semantics the model does not capture** -- side effects on read, clear-on-read
   bits, a value that should be recomputed rather than stored. If so, deleting the kill ships a
   plausible-looking wrong value in place of a loud stop, which is a WORSE outcome and would argue for
   member 3 (decline + latched announce) instead.
3. **ARE THESE ONE CLASS OR TWO?** This project's round-scope rule takes ONE site per round and admits a
   second only in the same file and same semantic class under one fix design with one detector. These are
   different files, different CPU families and different subsystems, so I expect TWO rounds -- but say
   whether the DISPOSITION should be identical, and if not, why.
4. **THE DETECTOR, for each.** The vacuity floor requires a detector that fails on the pre-fix build, on a
   verbatim reinstatement of the removed kill, on a null medium, AND on a NULLED REPAIR (the guard kept,
   its effect removed). For each site name the rows, and per row **the mutant it kills and the observable
   that differs under that mutant.** A row whose named channel cannot vary under its named mutant is
   vacuous by construction and that is knowable now.
   **Two traps I already know about and want you to route around**: (a) *"the host survived"* is NOT a
   channel -- guarded and unguarded code both survive once the kill is gone, so a survival oracle at a
   refusal site is vacuous; (b) a returned ZERO is not evidence, because zero is what several wrong
   implementations also return. **The oracle has to be a value the guest separately STORED and reads back
   EXACTLY.**
5. **THE VEHICLE.** For Site A, `regress/gdrom_default_probe.py` already drives a Dreamcast session with
   guest load/store helpers -- can it carry these rows? For Site B the read is a COPROCESSOR access from
   an ARM guest, which is a different vehicle from the device probes this project mostly writes; say what
   would drive it and whether `gate_arm.sh`'s existing machinery helps.
   **Check the device's registration mode before trusting any read-back oracle**: `memory_rw.c` skips a
   device callback for side-effect-free accesses unless the device declares that reads have no side
   effects, so a debugger-read oracle can silently bypass the handler entirely and prove nothing.
6. **WHAT ELSE IS FATAL IN THESE TWO FILES?** Both were named in a wider audit with several other exits;
   say which of them belong to these rounds and which are separate, and name any that are UNREACHABLE
   with the warrant, because a dead path recorded with its reason is a result rather than an absence.
7. If you found something else, say so.

Read-only: no builds, no probe runs, no edits, no patches. Prose and tables only.
