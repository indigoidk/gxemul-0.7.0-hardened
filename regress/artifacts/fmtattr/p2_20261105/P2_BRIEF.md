# GXemul hardened fork -- pass 2 on the format-fix diff (a defensive code-quality review)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.**  The tree under review is `GXEMUL-SEC/src/` at HEAD 79df4277 plus the staged
edits below; the pristine-upstream copies under the project root are NOT this fork.

**What this is.**  The diagnostic functions `debug`, `fatal`, `debugmsg` and `debugmsg_cpu` are printf-like.  With
`__attribute__((format(printf, ...)))` added to their declarations in `src/include/misc.h` (a scratch build), GCC reported 158
format warnings at HEAD (145 `-Wformat=`, 13 `-Wformat-extra-args`).  Gemini 4 Argon drafted exact-text edits; a script applied
126 of them, and the main loop made 2 by hand (`x11.c`: only the stray comma after "This is not really\n" removed; `cpu_mips.c`:
an `(int)` cast on an ASID masked to a byte).  MEASURED: the same attributed build with the edits has 0 `-Wformat=` and 0
`-Wformat-extra-args` warnings, `make` rc 0, the binary builds.  Still reported and out of this round's scope: 19
`-Wformat-zero-length` (intentional empty lines) and 4 `-Wformat-overflow` (disassembler NULL-`%s` warnings already adjudicated
as false positives).

Read only these: `_scratchpad/codescan/fmtfix/FIX.diff` (the whole change, unified, against HEAD),
`_scratchpad/codescan/fmtfix/WHY.txt` (Gemini's one-line reason per edit), `_scratchpad/codescan/fmtfix/fix_hand.py` (the 2 hand
fixes), the staged files under `_scratchpad/codescan/fmtfix/stage/src/`, the build log `_scratchpad/codescan/fmtfix/v_make.log`,
and `GXEMUL-SEC/src/` (read-only) for context.

**The rules the edits had to follow:** preserve each message's meaning and radix (a `%i` stays decimal, a `%x` stays hex); a 64-bit
value in hex is `"0x%" PRIx64` with a `(uint64_t)` cast; an `(int)`/`(unsigned)` cast only where the value is small by
construction (an offset inside a device's own window, a register number, a byte, a loop index); `size_t` -> `%zu`; a pointer ->
`%p` with `(void *)`; a missing argument is added only if its value exists at that point, otherwise the conversion is removed
(mb89352: `idata` is still zero there, so its field is removed); an extra argument: check for a stray comma or a missing
conversion first.

## Questions -- VERDICT LINE FIRST

1. Name every edit that CHANGES a message's meaning or radix, or prints a different value than before for any input.
2. Name every narrowing cast (`(int)`, `(unsigned)`, `(uint32_t)`) whose value can exceed 32 bits on a reachable path -- the
   case where the fix silences the compiler and keeps the truncation.  Give the path.
3. Are the three missing-argument fixes right (dev_ps2_stuff.c timer hold, dev_mb89352.c wide access, cpu_ppc.c PPC601 dump)?
4. Is any edit outside a format call, or does any edit change code that is not a diagnostic?
5. The smallest edit that would re-break one of these and still pass the attributed build -- for example a `(uint32_t)` cast
   on a 64-bit value printed with `PRIx64`.  Which of the 158 sites are exposed to that, and is a row owed?

If, while verifying a claim, you found something ELSE -- say so.

**End with one line:** `FMTP2: <n> EDITS WRONG, <m> NARROWINGS UNSAFE, <k> OTHER; VERDICT <ship / fix first>`.
