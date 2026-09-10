# `ppcrldimimask` + `ppcrlwimiwidth` -- two MEASURED defects in one instruction family: the fix designs

Nonce: `CODEX_PPCSIBS_20260910`. Open with `VERDICT:` giving the exact edit for EACH site separately,
then echo the nonce.

Ordinary correctness maintenance on a CPU model in an emulator written in C99. **The tree is
`C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere under the
project root. **Verdict line first.**

**Please do not simply ratify.** Four briefs of mine this week had premises refuted by a seat that opened
the file, and every refutation improved the round. **Check the premises, not just the derivations.** In
particular the two "measured" results below came from a seat, and I have not re-derived either myself.

## CONTEXT: a third defect in the same family is already fixed

`X(rldicl)` was writing ZERO to its destination on every execution -- the mask was accumulated into the
rotated value while the destination got `tmp & tmp2` and `tmp2` was never anything but 0. Witnessed at
rung 3, 190 of 190 census cells wrong, repaired by one character. **The sibling audit that came with that
witness found two MORE live defects, and this brief is about those two.**

## SITE A -- `ppcrldimimask`, in `X(rldimi)`

```c
while (sh-- != 0) { ... rotate ... }        /*  post-decrement leaves sh == -1  */
m = mb; tmp = 0;
do { tmp |= ((uint64_t)1 << (63-m)); m ++; } while (m != 63 - sh);
```

`while (sh-- != 0)` **always** exits with `sh == -1`, so `63 - sh` is **always 64** and the mask always
runs to bit 63. The architecture requires the mask to END AT `63 - SH`. Measured, destination seeded 0
and an all-ones source: `SH=8` and `SH=32` both give all-ones where the low byte / low word should have
been PRESERVED; `SH=0` agrees and is the one safe case. **This is the standard bitfield insert, so a
compiler splicing a field destroys everything to the right of it.**

## SITE B -- `ppcrlwimiwidth`, in `X(rlwimi)`

```c
MODE_uint_t tmp = reg(ic->arg[0]), ra = reg(ic->arg[1]);
tmp = sh ? ((tmp << sh) | (tmp >> (32-sh))) : tmp;
```

`cpu_ppc.c` defines `DYNTRANS_DUALMODE_32`, so this file is compiled twice and `MODE_uint_t` is
**`uint64_t`** in the 64-bit build. The architecture specifies a 32-bit rotate over the source's LOW half
only. The right-shift pulls high-half bits into the low 32 bits, where the mask lives. Measured with
source `0xAAAAAAAA0000000F`, shift 4: `got 0x5a5a5a5aaaaaaaf0`, `want 0x5a5a5a5a000000f0`. **Its siblings
`rlwinm` and `rlwnm` cast to `uint32_t` before rotating and are correct; this one never does.**

## THE QUESTIONS

1. **PREMISES AS QUESTIONS -- re-derive both from the source and the architecture manual**
   (`_scratchpad/ppc_pem_32and64_2005.txt` is local; the rldimix and rlwimix RTL is what settles it).
   Is `sh` really always -1 at that point? Is `MODE_uint_t` really 64-bit in the 64-bit build here? **If
   either reading is wrong the round collapses and I want to know.**
2. **THE EXACT EDIT FOR EACH.** For Site A I am told the durable repair is to SAVE `sh` before the rotate
   loop rather than to patch the `63 - sh` expression, because the same `while (sh-- != 0)` idiom appears
   in `rldicl`, `rldicr` and `rldimi` and any future edit reaching for `sh` after the loop will be wrong
   the same way. Do you agree, and does saving it change anything else in those handlers? For Site B, is
   truncating to `uint32_t` before the rotate sufficient, or does the mask/merge below also need
   attention?
3. **ARE THESE ONE ROUND OR TWO?** This project takes ONE site per round; a second joins only if it is
   the same semantic class under one fix design with one detector. They are in the same file and the same
   instruction family but have different root causes (a clobbered loop variable versus a missing
   truncation). Say which way you would split them and why.
4. **WHAT ELSE IN THIS FAMILY IS WRONG?** `rldicr`, `rlwnm`, `rlwinm` are reported CORRECT and `rldic`,
   `rldcl`, `rldcr` reported NOT IMPLEMENTED AT ALL (the decoder's default swallows them). **Re-check all
   six.** An unimplemented but documented, compiler-emitted instruction is its own filing.
5. **THE DETECTOR.** The floor needs failure on the pre-fix build, on a verbatim reinstatement, on a null
   medium, and on a NULLED REPAIR. Name the rows and per row the mutant it kills and the observable that
   differs. **Two traps measured today, both worth routing around:** a row is VACUOUS here exactly when
   the selected window of the rotated source is all zeros, so choose a source where every mask window is
   non-empty; and for Site B a row is vacuous unless the source's two halves DIFFER, because with an
   all-ones source a 64-bit rotate and a true 32-bit one agree bit for bit. **The measuring seat's own
   first draft hit the second trap and corrected it rather than shipping a green row.**
6. **THE GATE HOLE.** No gate in this tree instantiates a 64-bit PowerPC CPU at all -- both PowerPC gates
   drive a 32-bit part, and the decoder sends the whole 64-bit group to its bad path in that mode. So
   these defects are invisible to the gates BY CONSTRUCTION. What is the smallest gate change that would
   close it for the whole family, and is it a rider on these rounds or its own harness round?
7. If you found something else, say so.

Read-only: no builds, no probe runs, no edits, no patches. Prose and tables only.
