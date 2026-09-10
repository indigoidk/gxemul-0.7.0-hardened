# `cpu_arm_coproc.c` -- the other SEVEN host kills, on the architecture whose gate has the most coverage

Nonce: `CODEX_ARMCOPROC_20260910`. Open with `VERDICT:` naming which sites you would file, in priority
order, then echo the nonce.

Ordinary robustness triage on ARM coprocessor handlers in an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under the
project root. **Verdict line first.**

**Please do not simply ratify.** Six briefs of mine this week had premises or proposed repairs corrected
by a seat that opened the file, and every correction improved the round. **Check the premises.** The site
list below is from an earlier census and I have re-derived only one of the eight.

## WHY THIS FILE

A census this morning found **76 guest-reachable error-exit sites across 24 files with no tracker row**.
`cpu_arm_coproc.c` holds **eight**, at lines **62, 177, 264, 313, 324, 333, 419, 530**, ranked I1 at 313
and I2 elsewhere.

**One is already filed and its design is settled.** Line 313 (`xscaleinten`) reads the modelled
interrupt-enable register into the destination and *then* calls `exit(1)`; the disposition is ACCEPT --
delete two lines, keep the assignment, no latch. **This brief is about the other seven.**

**Why this file rather than a bigger pile:** ARM is the architecture with the most existing gate coverage
here (`gate_arm.sh` runs several hundred real decode checks across three machines), so a witness and a
detector have somewhere to live -- unlike most of the remaining census, where the vehicle is the hard part.

## A CORRECTION I ALREADY OWE YOU, so you can use it

When I filed line 313 I claimed its neighbouring case is a clean precedent that "carries no `fatal()` and
no `exit()`". **That is false of the whole case.** Its READ arm is quiet; its WRITE arm assigns the field
and then `exit(1)` on any nonzero value. The asymmetry I relied on is real only in the READ direction.
**So this file has kills on both halves of adjacent cases, and a per-case reading is not enough.**

## THE QUESTIONS

1. **RE-DERIVE THE EIGHT SITES at HEAD**, and give GREP ANCHORS rather than line numbers -- line numbers
   decay and anchors do not. Which coprocessor does each belong to, and which are in a `default:` arm
   versus a specific case?
2. **SPLIT BY REACHABILITY, counted.** (i) reachable by an ordinary guest coprocessor instruction on a
   machine this tree actually builds; (ii) reachable only on a CPU model or coprocessor number nothing
   installs; (iii) provably unreachable, with the guard that makes it so NAMED. **Populations (ii) and
   (iii) are RESULTS when recorded with their warrant** -- a dead path named with its reason stops the
   next round re-finding it. **Say which machine constructors install which coprocessor handlers**, since
   that is what decides (i) versus (ii).
3. **WHICH ARE THE SAME SHAPE AS 313 -- "the value is already computed and then discarded"?** That shape
   has a settled disposition here (ACCEPT, two lines) and would make several sites one cheap round rather
   than several. Which are NOT that shape, and what do they need instead?
4. **IS THE FAULT MEMBER AVAILABLE?** This project's memory layer converts a failed *device* callback into
   an architectural exception for MIPS and M88K only — but these are CPU coprocessor handlers, not device
   accesses, so the relevant mechanism is the CPU's own undefined-instruction path. **Does this tree have
   one reachable from here, and do any of these sites already use it?** Grep for how a neighbouring ARM
   handler rejects an unimplemented coprocessor operation; the tree's own idiom is worth more than an
   argument.
5. **FOR YOUR TOP TWO, give the smallest honest fix and the detector rows.** Two traps measured here this
   week: *"the host survived"* is not a channel at a refusal site, because guarded and unguarded code both
   survive once the kill is gone; and a row asserting only that an access completed is SURVIVE-ONLY and
   cannot tell two arms apart. **A row must observe something that differs between the arms.**
6. **WHAT WOULD YOU NOT FILE, and why?**
7. If you found something else, say so.

Read-only: no builds, no probe runs, no edits, no patches. Prose and tables only.
