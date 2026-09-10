# `mk48nvramkill` -- the FIX DESIGN: which constant is wrong, and which disposition does the tree's own practice support?

Nonce: `CODEX_MK48_DESIGN_20260910`. Open with `VERDICT:` naming the disposition and the exact edit you
would make, then echo the nonce.

Ordinary robustness maintenance on a timekeeper/NVRAM device model in an emulator written in C99. **The
tree is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`**; three unrelated 2021-vintage copies sit elsewhere
under the project root, so line numbers off by hundreds mean you are reading one of those. **Enumerate
arithmetic; do not reason about it.** **Verdict line first.**

**Please do not simply ratify.** A recent panel here had seven of nine seats confirm a premise the brief
stated wrongly. **Check the premises, not just the derivations** -- every one below is a file open away,
and if the boundary is wrong in a way I have not described, that changes the whole round.

## §C -- SETTLED PREMISES (check them)

S1. `src/devices/dev_mk48txx.c` registers the device for `MK48TXX_LEN`, defined as `MK48T08_CLKSZ`
    (**8192**), so `relative_addr` spans `[0, 0x2000)`.
S2. An early accept block sends everything OUTSIDE `[MK48T08_CLKOFF, MK48T08_CLKOFF + MK48TXX_ISEC)` to
    the RAM path with a `goto ret`, storing on write and reading `d->reg[relative_addr]` on read.
S3. `MK48T08_CLKOFF` = `0x1ff0` and `MK48TXX_ISEC` = `9` (both in
    `src/include/thirdparty/mk48txxreg.h`), so the `switch` is reached for exactly `0x1ff0..0x1ff8`.
S4. The `switch` holds exactly ONE case, `MK48T08_CLKOFF + MK48TXX_ICSR` = `0x1ff8`. **So the eight
    offsets `0x1ff0`..`0x1ff7` reach `default:`, print an `unimplemented` diagnostic and call `exit(1)`.**
S5. `src/machines/machine_mvme88k.c` attaches the device unconditionally at `0xfffc0000`.
S6. `d->reg[]` is declared `uint8_t reg[MK48TXX_LEN]`, i.e. **storage for all 8192 offsets already
    exists**, including the eight fatal ones.

## THE QUESTIONS

1. **WHICH CONSTANT IS WRONG, AND WHAT DOES THE CHIP ACTUALLY HAVE AT `CLKOFF+0 .. CLKOFF+7`?** This is
   the question the whole round turns on. `mk48txxreg.h` is vendored third-party material -- read it
   properly. `MK48TXX_ICSR` is 8 and `MK48TXX_ISEC` is 9 through `MK48TXX_IYEAR` at 15, so indices 0..7
   of the clock page are unaccounted for by any `MK48TXX_I*` define. **What are they on an MK48T08?**
   Options I can see, and I want you to say which the header and the sibling drivers support: they are
   ordinary NVRAM; they are a second bank; they are the chip's *other* model's registers (the file says
   *"Only the MK48T08 is implemented so far"*); or the accept block's bound should have been
   `CLKOFF + ICSR` rather than `CLKOFF + ISEC`. **Note the current bound has a second consequence worth
   checking: it hands the REAL time-of-day registers (`ISEC..IYEAR`) to the RAM path** -- is that
   correct, harmless, or a separate defect?
2. **WHICH OPTION-SET MEMBER?** This project's menu is {delete, silent decline, decline + latched
   announce, accept, fault, backed accept, implement}. **Grep the fork for how sibling timekeeper and
   NVRAM devices handle an offset they do not model** -- `dev_mc146818.c` and `dev_rs5c313.c` are the
   obvious neighbours and `dev_rs5c313.c` already cites `mk48txxreg.h` in a comment. The tree's own
   precedent is worth more than an argument. **And check the member is AVAILABLE**: a bus fault needs the
   memory layer to deliver one, which this tree does for only two CPU families, and this device is
   attached to an m88k machine.
3. **THE SMALLEST HONEST EDIT.** Given S6 -- the storage already exists -- I suspect this is a BOUNDARY
   CORRECTION rather than a new policy, i.e. one constant in the accept block. Say whether you agree,
   give the exact edit, and say what it does to each of the nine offsets currently reaching the switch.
   **If a one-constant change would ALSO swallow the `ICSR` case that the switch legitimately handles,
   say so** -- that case does real work (it freezes the clock on a 0->1 transition of the read bit) and
   must keep working.
4. **WHAT BREAKS.** Does any in-tree guest, PROM image or driver depend on the current behaviour? Is
   there any offset where accepting a write would corrupt something the model later reads back as a clock
   value? **The clock registers are re-derived from the host on demand -- check whether a guest WRITE to
   them is silently discarded, silently honoured, or honoured and then overwritten**, because that
   determines whether `d->reg[]` is a safe backing store or a shared one.
5. **THE DETECTOR.** If this round ships a fix, what should its rows be? The vacuity floor requires the
   detector to fail on the pre-fix build, on a verbatim reinstatement of the removed kill, on a null
   medium, AND on a NULLED REPAIR (the guard kept, its effect removed). Name the rows and, for each, the
   mutant it kills and the observable that differs under that mutant. **A row whose named channel cannot
   vary under its named mutant is vacuous by construction, and that is knowable now, before anything
   runs.**
6. **WHAT ELSE IS FATAL OR UNREACHABLE IN THIS FILE?** While you are in it: any other offset, any other
   `exit(`, any decode that cannot be reached.
7. If you found something else, say so.

Read-only: no builds, no probe runs, no edits, no patches. Prose and tables only.
