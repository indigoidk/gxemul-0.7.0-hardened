# GXemul hardened fork -- adjudicate four queue items from a code-scanning triage (defensive code-quality review)

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY

A recent panel had seven of nine seats confirm a premise this brief's author stated wrongly.  **Check the premises, not just
the derivations.**  Where I state something as fact, ask whether it is true.  A seat that re-derives a premise from something
this brief did NOT give it is worth more than a seat that agrees.  (Earlier today my own first reading of one item, #135 below,
was wrong; a second seat caught it.)

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/` at commit f58105b7.**  There are pristine-2021-upstream copies of GXemul under the
project root (`./src/` and two under `_archive/`).  They are NOT this fork.  If your line numbers disagree with mine by hundreds
you are reading one of them -- say so rather than reconciling.

**If you cannot read files, that is expected** -- the facts you need are inlined in the appendix.  Name any premise you cannot
settle from this packet rather than guessing at it.

## What happened

GitHub CodeQL scanned an old pushed commit (759f7131) and raised 137 alerts.  A triage mapped them onto HEAD and re-scanned the
printf-format class at HEAD by building with `__attribute__((format(printf, ...)))` added to the four diagnostic functions in
`src/include/misc.h` (`debug`, `fatal`, `debugmsg`, `debugmsg_cpu`), so GCC checked every call.  The triage proposes four queue
items.  This pass adjudicates them BEFORE any fix is written.

Files a file-reading seat may open (read nothing else): `_scratchpad/codescan/CODESCAN_TRIAGE.md`, `_scratchpad/codescan/out/
alerts.tsv`, `_scratchpad/codescan/fmt_warnings.tsv`, and `GXEMUL-SEC/src/` (read-only).

## The four proposed items

1. **fmtmissarg** -- three calls whose format names more conversions than arguments: `src/devices/dev_ps2_stuff.c:239` (a guest
   read of timer 2/3's hold register), `src/devices/dev_mb89352.c:305-309` (a guest non-byte access), `src/cpus/cpu_ppc.c:478`
   (the debugger's PPC601 register dump).  Each prints an unspecified value.
2. **disasmnullmnem** -- four `debug("%s\t", mnem)`-style calls where GCC deduces `mnem` may be NULL:
   `src/cpus/cpu_alpha.c:357`, `:651` (two warnings), `src/cpus/cpu_m88k.c:1437`.  A disassembler switch that does not cover an
   opcode leaves `mnem` NULL; glibc prints "(null)", other C libraries may not.  Reached when guest code is disassembled
   (instruction tracing, the debugger).
3. **arcmemdescnr** -- `src/promemul/arcbios.c:1560-1580`, ARC `GetMemoryDescriptor(ptr)`: `int nr = a0 - base; nr /= s; nr++;`,
   then `V0 = base + s * nr; if (nr >= n_memdescriptors) V0 = 0;`.  A guest `a0` below `base` gives `nr <= 0`, which the test
   misses, so the guest gets a pointer below the descriptor table (and `s * nr` can wrap).  The value only goes back to the
   guest in V0; nothing on the host is accessed with it.
4. **fmtattr** -- GCC at HEAD reports 127 lines with a wrong argument TYPE or an extra argument (145 `-Wformat=` + 13
   `-Wformat-extra-args` warnings).  Dominant shape: `%i`/`%x` given a 64-bit value (59 int vs unsigned long, 43 unsigned int
   vs unsigned long).  Effect on x86-64: a truncated or wrong number in a diagnostic.  Proposal: ONE mechanical round that
   fixes all 127 lines with the tree's idiom (`PRIx64` plus a `(uint64_t)` cast, or an `(int)` cast where the value is
   small) AND makes the four attributes permanent in `misc.h` (guarded by `__GNUC__`), so the compiler rejects the class at
   every build.  The 19 `-Wformat-zero-length` warnings are intentional empty lines (`debugmsg(..., "")`) and need
   `-Wno-format-zero-length` or a `"%s", ""` form.

Proposed for NO action, to be dismissed on GitHub once the fixes land: `dev_fdc.c:101` snprintf (CodeQL "overflowing
snprintf": `buf` is `3*DEV_FDC_LENGTH+1` bytes and the loop writes at most `DEV_FDC_LENGTH` three-character items),
`diskimage.c` fopen after a stat (TOCTOU: the emulator opening its own user's image path), two alerts in
`experiments/dump-hp700rx-rom.c` (a standalone tool outside `src/` that the build does not compile), and 15 integer-multiplication alerts graded
BOUNDED or HOST in the triage's table.

## Questions -- answer in this order, VERDICT LINE FIRST

1. **Premise audit.**  Each of these is load-bearing; say TRUE / FALSE / UNSETTLED with your evidence:
   a. Is every one of the 52 GCC warnings that CodeQL did not report already present at 759f7131?  (The triage checked line
      text against `git show 759f7131:<file>`.)
   b. Does `dev_fb_resize()` really cap both sizes at 10..16384 before the copy loop, so `bytes_per_line * y < 2^30`?
   c. In #135, can a guest really supply `a0 < base`, and is V0 the ONLY use of the result?
   d. Does `dev_mb89352.c:305-309`'s format have three conversions and two arguments?
   e. For the NULL `mnem` sites, name one opcode value that reaches the `debug()` with `mnem` still NULL -- or say none can.
2. **Grade each item:** real or not; severity order among the four; and the witness each can carry under this project's
   ladder (a rung-3 cold-debugger probe on an unmodified machine; a construction or build witness; or `detector:` with the
   compiler as the detector).  For fmtattr, what is the right witness term for a compiler-detected class?
3. **Round shape.**  Should fmtattr be ONE round (127 lines + the attribute) or split (per file, or per subsystem)?  Should
   fmtmissarg fold into fmtattr (the attribute catches it) or stay separate because two of its sites are guest-reachable?
   One round for disasmnullmnem's two CPUs, or two?
4. **The smallest edit that breaks each proposed fix and still passes** its proposed detector -- name the row or check that
   would stay green.
5. **Option-set completeness** for arcmemdescnr's fix (`nr < 1 ||` added to the test, the offset computed in a wide type): is
   there a member this brief did not name -- for example declining any `a0` that is not exactly on a descriptor boundary?
   Grep the fork for how other ARC calls validate a guest pointer.
6. **The no-action list:** for each entry, agree or disagree with dismissing it, with the reason GitHub should record (false
   positive / won't fix / used in tests).

If, while verifying a claim, you found something ELSE -- say so.

**End with one line:** `CSADJ: <n> ITEMS GRADED, <m> PREMISES FALSE, <k> UNSETTLED; ROUND SHAPE <one phrase>`.
