# Adversarial seat -- `armmmuvehicle` pass 1 (grok, dedicated job)

VERDICT LINE FIRST: `VERDICT: <the single worst defect in the design, in one line>`.

Read the design brief: `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\armmmuvehicle_PASS1_brief_20261009.md`.  Tree under
review: `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\src\` only (the project root holds pristine 2021 upstream copies --
ignore them).  READ-ONLY.

You are the ADVERSARY, not a reviewer.  You wrote the 13-hole condemnation of the 2026-09-17 Thumb witness spec
(`GXEMUL-SEC\regress\artifacts\armthumbabortkill\HOLES_grok_20260917.txt`); this design claims to have absorbed all
13.  Attack it the same way, against the source:

1. **Find the way this vehicle reports GREEN while the MMU fault path is broken** -- a mutant of `memory_arm.c`,
   `arm_exception` or the CP15 c1/c2/c3/c5/c6/c8 handlers that every proposed row survives.  Name the edit and the
   row that stays green.
2. **Find the way this vehicle makes a CONSUMER round's witness lie** (`armthumbabortkill`, `armdesc3kill`,
   `armdacr2kill`): a vehicle property that would make a HEAD red look green, or a POST green look red, once a
   consumer adds its stimulus.
3. **Find any hole of your 13 that the design re-opened**, or a fourteenth you did not name then.

Derive every claim from the source and name the grep anchor.  Separate what you READ from what you REASONED.
**If you found something ELSE -- say so.**
