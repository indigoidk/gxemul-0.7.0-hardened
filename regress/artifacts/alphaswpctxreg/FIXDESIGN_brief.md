# alphaswpctxreg -- fix design: which register carries swpctx's result?

## 0. READING SCOPE

Read what you need under `GXEMUL-SEC/src/`, in particular `src/cpus/cpu_alpha_palcode.c`,
`src/include/cpu_alpha.h` and `src/include/thirdparty/alpha_cpu.h`. Please avoid
`regress/artifacts/` and `tools/pipeline/ledger.json`.

Tree under review: `GXEMUL-SEC/src/`. Ignore the pristine 2021 `src/` at the project root.

**This is a register-convention question about existing code.** I am not asking for a test sequence
or a way to reach anything; I want the ABI read correctly and the smallest correct edit.

## 1. THE OBSERVATION

In `PAL_OSF1_swpctx`, after saving the outgoing context, the handler has:

    /*  Return old context in v0.  */
    cpu->cd.alpha.r[ALPHA_A0] = cpu->cd.alpha.ctx;

    /*  Load new context:  */
    {
            cpu->cd.alpha.ctx = a0;
            uint64_t new_ksp = load_64bit_word(cpu, cpu->cd.alpha.ctx + 0);
            ...

**The comment says v0; the store is to `ALPHA_A0`.** `ALPHA_V0` exists and is used elsewhere in the
same file. The local `a0` is a `uint64_t` copied from the register file at function entry, so the
"load new context" step still uses the original argument and is unaffected by the store above it.

The kernel-side wrapper in `alpha_cpu.h` is roughly:

    alpha_pal_swpctx(unsigned long ctx)
    {
            ... __asm volatile("call_pal %2 # PAL_OSF1_swpctx"
                    : ...
                    : "i" (PAL_OSF1_swpctx), "0" (a0) ...

## 2. QUESTIONS -- VERDICT LINE FIRST

**Please do not simply ratify.** A recent panel had seven of nine seats confirm a premise a brief
stated wrongly, and you yourself refuted four premises of mine when asked to. **Check the premises,
not just the derivations.** In particular I may be reading the asm constraints wrongly.

**Q1. Quote the full wrapper** and say which register it actually reads the result from, deriving it
from the constraint letters rather than from the comment. `"0"` ties an input to output operand 0 --
say what operand 0 is and which physical register it lands in.

**Q2. Is this ONE defect or TWO?** My reading is that writing `r[ALPHA_A0]` here does two wrong
things at once: it fails to place the result where the caller reads it, **and** it clobbers the
caller's `a0`. If both hold, does the single-character fix (`ALPHA_A0` -> `ALPHA_V0`) repair both,
or does the clobber need separate handling?

**Q3. Does any other PAL handler in this file set a return value, and how?** You noted last pass
that the PAL dispatch a hundred lines up uses `ALPHA_V0` correctly. **Give me the in-tree idiom**,
because the project's rule is to grep the fork for the existing idiom rather than reason from first
principles -- and a fix that matches its siblings is easier to review and harder to get wrong.

**Q4. Is `a0` live after this point for any other reason?** If the handler or its callers rely on
`r[ALPHA_A0]` holding the old context anywhere -- however unlikely -- changing it is not a pure
improvement and I want that named now rather than discovered later.

**Q5. What ORACLE distinguishes the fix from the defect?** Not a guest sequence -- just: what
observable value differs between the two builds, and is it a register the emulator's own debugger
can print? If the answer is "the two are indistinguishable without a guest that reads the return
value", say so; that changes the disposition and the round would have to state it.

**Q6. Does the COMMENT need changing too?** It currently says the right thing while the code does
the wrong thing. After the fix the comment becomes accurate -- but this project treats a comment
that asserts an observable as owing a test row, so say whether the comment as written is a claim
that should be pinned or merely a description.
