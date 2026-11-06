# GXemul hardened fork -- pass 2b on the format round's COMPOSITE diff (a defensive code-quality review)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.**  The tree under review is `GXEMUL-SEC/src/` at HEAD 79df4277 plus the staged
files `_scratchpad/codescan/fmtfix/stage/src/` (47 files).  The pristine-upstream copies under the project root are NOT this fork.

Your pass 2 (`_scratchpad/codescan/fmtfix/p2_astra/codex_fmtp2.txt`) found 7 wrong edits.  All 7 are repaired by
`_scratchpad/codescan/fmtfix/fix_hand3.py`.  Since then, material you did not review was added: `fix_hand2.py` (the 19
`-Wformat-zero-length` calls rewritten `"%s", ""`, and an unreachable `default: mnem = "?"` in the three disassembler switches,
cpu_alpha.c x2 and cpu_m88k.c x1) and `fix_misc_h.py` (misc.h: a `GX_PRINTF` macro, `__attribute__((format(printf, f, a)))` under
`#ifdef __GNUC__` and empty otherwise, applied to debug/fatal/debugmsg/debugmsg_cpu).  The whole change is
`_scratchpad/codescan/fmtfix/COMPOSITE.diff` (against HEAD, 2 lines of context).  MEASURED (`fmtverify2.out`): HEAD + the stage,
built normally, gives 0 compiler warnings of any kind and 0 errors; a seeded mismatch in each of the four functions warns (4/4).
Gate 1 (`regress/gate_build.sh`) already fails on ANY compiler warning, so the permanent attributes make it the enforcing gate.

Read only: the files named above, `_scratchpad/codescan/fmtfix/fmtverify2.out`, and `GXEMUL-SEC/src/` (read-only).

## Questions -- VERDICT LINE FIRST

1. Are the 7 repairs right?  (cpu_ppc.c supplies `x`; cpu_arm.c `%zu`; bt455/dc7085 x2 `PRIx64` with `(uint64_t)idata`, keeping
   the old minimum widths; dev_le.c `PRIu64`.)
2. The material you have not seen: is any zero-length rewrite, unreachable `default:`, or the misc.h macro wrong?  Does a
   `default:` change behaviour on any reachable path?  Does `GX_PRINTF` break any non-GCC build or any caller?
3. THE FLOOR on the composite: is there a mutant of this round's own change that the round's detector (the attributed build plus
   gate 1's zero-warning check plus the four seeded controls) passes?  Your pass named `PRIx64` -> `PRIu64` and
   `(uint64_t)(uint32_t)x`.  Say whether ONE output-checking row (your SGI loader-block `0x100000000` example) is owed in THIS
   round, or the class is disclosed debt in the detector's contract -- with the bound that keeps it from becoming one row per
   call.
4. The inherited truncations you found (luna88k, lunafb, memory.c:626, arcbios A1/A2, ps2_bios A1, dev_ether, LE writes): in this
   round, or filed?

If, while verifying a claim, you found something ELSE -- say so.

**End with one line:** `FMTP2B: <n> REPAIRS WRONG, <m> NEW DEFECTS, ROW <owed / debt>, TRUNCATIONS <round / file>`.
