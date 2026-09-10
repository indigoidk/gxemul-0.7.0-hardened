# The 64-bit PowerPC gate hole: no gate in this tree has ever instantiated a 64-bit PPC CPU

Nonce: `CODEX_PPCGATE_20260910`. Open with `VERDICT:` naming the smallest change that closes the hole,
then echo the nonce.

Ordinary regression-harness design on an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under the
project root. **Verdict line first.**

**Please do not simply ratify.** Five briefs of mine this week had premises or proposed repairs corrected
by a seat that opened the file, and every correction improved the round. **Check the premises.**

## THE HOLE, as measured today

Three defects were found in the 64-bit PowerPC rotate-and-mask family this afternoon, all measured at
rung 3, one now fixed and two filed:

* `X(rldicl)` returned **ZERO on every execution** -- 190 of 190 census cells wrong. Fixed (`#522`).
* `X(rldimi)` overwrites destination bits the architecture requires PRESERVED, for every non-zero shift.
* `X(rlwimi)` performs a 32-bit rotate at 64-bit width, so high-half data leaks into the result.

**None of them is visible to any gate, and the reason is structural rather than an oversight.** Both
PowerPC gates drive `macppc -e g4`, which is an MPC7400 -- a **32-bit** part -- and the decoder sends the
whole `rld*` group to its bad path when `cpu->cd.ppc.bits == 32`. So **no gate has ever instantiated a
64-bit PowerPC CPU at all**, and that entire instruction group is untested by construction.

`gate_ppc.sh` states its own scope honestly (*"machine: macppc/G4, NetBSD kernel loaded so the machine
constructs; never executed"*), so nothing here is a false record -- it is a coverage hole that nobody had
named.

## WHAT I THINK, so you can disagree with it

One 64-bit probe closes the whole hole, because the cause is single: no gate selects a 64-bit CPU. The
tree already has `-E bareppc`, whose default CPU is a PPC970 and therefore 64-bit, and a working probe
(`regress/ppc_rldicl_probe.py`, 19 rows, 0.2 s) that drives exactly that.

## THE QUESTIONS

1. **PREMISES AS QUESTIONS.** Re-derive it: which machines and CPU models do the PowerPC gates actually
   select, and is the 32-bit gate on `rld*` really where I say it is? **Is there any gate ANYWHERE in the
   tree -- not just the two PowerPC ones -- that reaches a 64-bit PowerPC CPU?** `gate_crossfamily.sh`
   and `gate_build.sh` are worth checking; if one already does, the hole is smaller than I claim.
2. **WHAT IS THE SMALLEST CHANGE THAT CLOSES IT?** Options I can see: add an `-E bareppc` leg to
   `gate_ppc.sh`; wire the existing 19-row probe in; or add a 64-bit CPU override to an existing macppc
   leg. Say which, and what each would and would not cover.
3. **IS IT A RIDER OR ITS OWN ROUND?** This project treats a gate change as owing its own negative
   controls -- prove the new row fails on a mutant, and prove it does not fire spuriously -- which makes
   it a harness round rather than a rider on a CPU fix. Do you agree, and what are the two controls?
4. **WHAT ELSE IS 64-BIT-ONLY AND THEREFORE UNTESTED?** The `rld*` group is what I found. Enumerate the
   rest: which handlers in `cpu_ppc_instr.c` are reachable only when `bits == 64`, and which of those are
   **not implemented at all** (I am told `rldic`, `rldcl` and `rldcr` fall to the decoder's default --
   check that, and say whether any is compiler-emitted). **A gate leg that runs one instruction closes
   one hole; I would rather know the size of the group first.**
5. **IS THERE A DEEPER VERSION OF THIS QUESTION?** PowerPC is not the only dual-mode family here. Are
   there other architectures where the gates exercise only one width, so a whole mode-gated instruction
   set is untested by construction? **That would make this a class rather than one hole**, and I would
   want it filed as such rather than fixed one architecture at a time.
6. **WHAT WOULD YOU NOT DO?** A gate leg that boots a 64-bit guest would be better evidence than one that
   single-steps planted instructions -- but the tree has no 64-bit PowerPC kernel image, and adding one
   is a different kind of change. Say plainly if the honest answer is that the gate can only reach rung 3
   here.
7. If you found something else, say so.

Read-only: no builds, no gate runs, no edits, no patches. Prose and tables only.
