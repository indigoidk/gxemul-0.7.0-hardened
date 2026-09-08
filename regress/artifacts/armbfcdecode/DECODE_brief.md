# armbfcdecode -- is BFC decoded as BFI, and what does the fork do with Rn = 15?

## 0. READING SCOPE

Read only these, and please do not read `regress/artifacts/` or `tools/pipeline/ledger.json`:

* `src/cpus/cpu_arm_instr.c` -- the `bfi` handler and its decoder arm
* `src/cpus/cpu_arm_instr_loadstore.c`, `src/cpus/cpu_arm.c` -- only if the decode dispatch needs them
* `_scratchpad/ddi0100i.txt` -- the ARM ARM extract, IF it covers these encodings (see Q3)

The tree under review is `GXEMUL-SEC/src/`. There is another `src/` at the project root which is
pristine 2021 upstream -- ignore it. A seat reporting line numbers that disagree with this brief by
hundreds has read that copy.

## 1. THE QUESTION

This is an ordinary instruction-decode conformance question about an emulator's ARM interpreter.
Nothing here is about security; it is about whether one encoding is dispatched to the right handler.

A previous reading claimed:

> The `bfi` decoder accepts source field 15 and passes `r[15]` to `X(bfi)`, but the architecture
> assigns that encoding to **BFC** (Bit Field Clear) -- so BFC is decoded as *BFI with Rn = PC*.

**That claim has NOT been verified.** It came from one seat's source reading on a different brief.
I am asking you to check it, and to say plainly if it is wrong.

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise that the
brief had stated wrongly. **Check the premises, not just the derivations.**

## 2. SETTLED PREMISES (re-derive if cheap; say so if any is wrong)

These were verified by opening the file for the sibling row `armbfiwidth`, so they are stated as
facts rather than questions -- but they are mine, not the tree's, and I may have mis-read:

* the decoder arm is guarded by `(iword & 0x0fe00070) == 0x07c00010`
* it computes `int lsb = (iword >> 7) & 31; int msb = (iword >> 16) & 31;`
  and packs them as `ic->arg[2] = (msb << 16) + lsb;`
* `X(bfi)` reads `int lsb = (uint8_t)ic->arg[2]; int msb = ic->arg[2] >> 16;`

## 3. WHAT I WANT BACK -- VERDICT LINE FIRST

**Q1. Does the decoder arm distinguish `Rn == 15`?**  Quote the actual lines that select the source
register and say whether any guard excludes 15. If the fork passes `r[15]` into the handler, say
which `arg[]` slot carries it and what `r[15]` holds at that point in this interpreter (the real PC,
a PC+8 value, or something else -- this differs between emulators and it matters).

**Q2. What does `X(bfi)` DO with that operand?**  Specifically: is the inserted value read from the
register, or is there any path where a 15 encoding still produces a clear? Quote the handler.

**Q3. Does the manual in this tree cover these encodings at all?**  BFI/BFC are ARMv6T2/ARMv7
additions and `_scratchpad/ddi0100i.txt` is DDI 0100I, which I believe is ARMv5. **If the encodings
are absent from that file, say so and do not substitute recalled knowledge as if it were the
manual** -- this project has shipped page citations that came from model output rather than from a
local document, and it is trying not to do that again. An honest "not in this manual" is the
answer I want if that is the case.

**Q4. If the claim holds, what is the smallest correct repair, and what would OBSERVE it?**  Note
that a detector row here has to distinguish "cleared the field" from "inserted whatever `r[15]`
held" -- and if `r[15]` can hold a value whose relevant bits are zero, those two are
indistinguishable at that moment. Name a field position and a PC value where they differ, or say
that no such row is constructible and why.

**Q5. Is this genuinely separate from `armbfiwidth`?**  That row is about `(1 << width) - 1` being
undefined for most encodable widths, in the same handler. Same file, adjacent lines, different
defect. Should these be one round or two? I have them as two on the round-scope rule (one fix
design does not cover both, and they need different oracles) -- argue me out of it if that is wrong.
