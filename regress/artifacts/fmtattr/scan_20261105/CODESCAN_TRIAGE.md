# GitHub code scanning -- dedup and review (2026-11-05)

**Source.** 137 open CodeQL alerts on `indigoidk/gxemul-0.7.0-hardened`, all on commit `759f7131`. That is the last push,
2026-08-22, and the local HEAD `f58105b7` is 517 commits later.  The alerts were pulled read-only with
`gh api --paginate .../code-scanning/alerts?state=open` into `alerts_open.json`.  Nothing on GitHub was changed.

**Method.**
- `triage_cs.py` maps each alert's flagged text from `759f7131` onto HEAD (`out/alerts.tsv`, `out/groups.tsv`,
  `out/SUMMARY.txt`).
- `fmtscan.sh` re-scanned the format class at HEAD.  It built HEAD's sources in a scratch dir with
  `__attribute__((format(printf, ...)))` on `debug`, `fatal`, `debugmsg` and `debugmsg_cpu` in `misc.h`, so GCC checks every
  call (`fmt_make.log`, `fmt_warnings.tsv`).
- The 16 multiplication alerts were read at HEAD with every assignment to their operands (`MUL_REVIEW.md`).

| CodeQL rule | alerts | still at HEAD | rewritten since |
|---|---|---|---|
| cpp/wrong-type-format-argument | 116 | 107 | 9 (dev_sgi_re.c 7, dev_sgi_ip32.c 1, dev_lca.c 1) |
| cpp/integer-multiplication-cast-to-long | 16 | 16 | 0 |
| cpp/wrong-number-format-arguments | 3 | 3 | 0 |
| cpp/overflowing-snprintf | 1 | 1 | 0 |
| cpp/toctou-race-condition | 1 | 1 | 0 |

## A. Real bugs, worth one small round

1. **Missing format arguments (3).**  Each format names an argument that is not passed, so it prints garbage.
   - `dev_ps2_stuff.c:239`: a guest read of timer 2/3's hold register.  `timer_nr` is in bounds, since `N_PS2_TIMERS` is 4.
   - `dev_mb89352.c:305-309`: a guest non-byte access to the SCSI controller.  The format has 3 conversions and 2 arguments.
   - `cpu_ppc.c:478`: the debugger's PPC601 register dump.
2. **WITHDRAWN -- a false positive (GPT-6 Astra, adjudication below).**  What this item said: "NULL handed to `%s` (4, GCC
   `-Wformat-overflow`, not in CodeQL's list)".  Each enclosing switch admits exactly the values its inner mnemonic switch
   assigns, so `mnem` is never NULL at these calls; GCC cannot see the coverage.  The original text follows, as a record:
   - Sites: `cpu_alpha.c:357`, `cpu_alpha.c:651` (2) and `cpu_m88k.c:1437`.
   - Cause: a disassembler `mnem` stays NULL for an opcode the switch does not cover.
   - Effect: glibc prints "(null)"; other C libraries crash.
   - Reach: disassembling guest bytes, under `-i` tracing or the debugger.

3. **ARC `GetMemoryDescriptor` (CodeQL #135, `arcbios.c:1572-1579`): a guest pointer below the descriptor table gives a
   NEGATIVE `nr`, which `nr >= n_memdescriptors` does not catch, so V0 returns `base + s*nr` (and `s*nr` can wrap).  The
   effect is a wrong pointer handed back to the GUEST only -- no host memory access.  ~~Fix: `nr < 1 ||` in the check~~ --
   WRONG (Astra): `a0 = base-1` gives `nr = 1` (the division truncates toward zero), which `nr < 1` still accepts.  See the
   adjudication for the boundary-membership fix.  Found by Gemini, confirmed by reading; my first reading said BOUNDED and was wrong.

## B. Real but low: the format-type class (one mechanical round)

GCC at HEAD finds **127 lines** with a wrong argument type or an extra argument (145 `-Wformat=` and 13
`-Wformat-extra-args` warnings).
- 108 of CodeQL's 110 live alerts are among them.  The other 2 are in `dump-hp700rx-rom.c`, a standalone tool the build
  does not compile.
- 52 were missed by CodeQL.  All 52 were already present at the push; none was introduced after it.
- The dominant shape is `%i`/`%x` given a 64-bit value: 59 int vs unsigned long, 43 unsigned int vs unsigned long.
- The effect on x86-64 is a truncated or garbled number in a diagnostic, not memory corruption.
- The fix is the tree's own idiom, `PRIx64` with a `(uint64_t)` cast, or an `(int)` cast where the value is small.
- Biggest files: dev_sgi_mec.c 30, dev_dec_ioasic.c 21, cpu_m88k.c 15, diskimage_scsicmd.c 13, dev_sgi_re.c 12.

**C. The structural fix -- recommended in the same round as B.**  Make the four `format(printf, ...)` attributes
permanent in `misc.h`, guarded by `__GNUC__`.  The compiler then refuses the class at every build instead of a periodic
scan finding it.  The 19 `-Wformat-zero-length` warnings are intentional empty lines (`debugmsg(..., "")`); they need
`-Wno-format-zero-length` or a `"%s", ""` form.

## D. No action

- **overflowing-snprintf** `dev_fdc.c:101`: false positive.  `buf` is `3*DEV_FDC_LENGTH+1` bytes, and the loop writes at
  most `DEV_FDC_LENGTH` three-character items, so `snprintf` cannot truncate.
- **toctou** `diskimage.c` (HEAD :2100): the emulator opening its own user's disk image path.  This is outside the
  threat model (no guest control).
- **15 of the 16 integer multiplications**: none can overflow from guest input (#135 is in A3).

| alert | site | operands | verdict |
|---|---|---|---|
| 121, 122 | cpu_mips_instr_unaligned.c:115, :145 | `i < len <= 8`, `dir = +/-1` | BOUNDED |
| 123 | cpu_sh.c (HEAD :1567) | `lo8 <= 255`, factor 2 or 4 | BOUNDED |
| 124-127 | dev_fb.c:905, :332, :175, :176 | init sizes; x clamped; `dev_fb_resize()` caps both sizes at 10..16384 with SIZE_MAX checks (guest-set via dev_fbctrl), so rows*line < 2^30 | BOUNDED |
| 128, 129 | dev_ps2_gif.c:176, :178 | `d->xsize` is only ever 640 (:413); coordinates are 16-bit fields: < 1.3e8 | BOUNDED |
| 130 | dev_pvr.c:2317 | `xsize`/`ysize` from DIWSIZE (masked), `bytes_per_pixel <= 4` | BOUNDED |
| 131 | dev_px.c:326 | `uint32_t` spans; len clamped to `PX_XSIZE`, rows to `PX_YSIZE` (the fork's OB-3 guard, `8dd86b5a`) | BOUNDED |
| 132 | dev_vga.c:492 | `scaleup` from the command line, `font_width = 8` | HOST |
| 133, 134 | file_elf.c:362, :511 | ELF header counts: the user's own kernel file; an `fseek` offset | HOST |
| 136 | arcbios.c:487 | memory-descriptor count from the machine's memory map | BOUNDED |

Gemini 4 Argon's independent reading (`gweb/jobs_20261105_codescan/mul_review/reply.txt`): 2 BOUNDED, 3 HOST, 2 GUEST, 9
UNSETTLED (my packet lacked the operands' definitions).  Settled by reading the source: its GUEST on #135 is RIGHT (now A3);
its GUEST on #128 is WRONG -- it took the local `xsize` at :232 for `d->xsize`, a conflation my packet invited (its writer
grep matched bare `xsize =`).  Its 9 UNSETTLED are settled in the table above.

## E. GitHub housekeeping (needs the owner's yes; nothing done)

- The alerts close by themselves on the next push and rescan.  Pushing is off by owner directive.
- Dismissal candidates, each a change on GitHub, so only on the owner's word:
  - `dev_fdc.c` snprintf: false positive;
  - `diskimage.c` toctou: won't fix;
  - `dump-hp700rx-rom.c` x2: not built;
  - the 15 bounded/host multiplications (#135 is a real, low bug: fix, do not dismiss).

## Proposed queue items

- `fmtmissarg`: section A1.
- `disasmnullmnem`: section A2.
- `arcmemdescnr`: section A3.
- `fmtattr`: sections B and C.  It is one mechanical round, and the attribute lands with the fixes so the build stays
  warning-free.

## ADJUDICATION -- GPT-6 Astra (ultra), 2026-11-05 (`adj/astra/codex_csadj.txt`) and Gemini 4 Argon (`gweb/jobs_20261105_codescan/adj_items/reply.txt`); Fable final owed

Gemini's independent reading AGREES on the four load-bearing points: disasmnullmnem is a false positive (its own derivation of
premise e); `nr < 1` is broken for `a0 = base-1` and the fix needs an alignment/boundary check; one format round with
fmtmissarg folded in; the no-action list.  Its premises a and b were UNSETTLED for want of inlined data (a is settled by
measurement below).  It graded fmtmissarg's severity higher ("potential host memory leak") than Astra; on the reviewed paths
the effect is an unspecified value printed to the user's own console.

`CSADJ: 4 ITEMS GRADED, 1 PREMISES FALSE, 1 UNSETTLED; ROUND SHAPE combined formats plus separate ARC`.

**Gradings.**
- `fmtmissarg` (real) and `arcmemdescnr` (real) are both low severity, ahead of `fmtattr` (real; a diagnostic-correctness class).
- `disasmnullmnem` is a false positive: zero bug-fix rounds.  A two-CPU accommodation is needed only if the build must be
  warning-free.
- None of them is a host-memory corruption on the reviewed paths.

**Round shapes.**  ONE combined format round, with `fmtmissarg` folded in but identified separately, and a separate ARC round.
The format round:
- needs an ENFORCED failure policy (`-Werror=format` or a gate), because the attributes alone only warn;
- needs a negative control for each of the four functions, plus a value above `UINT32_MAX` where full width matters;
- must preserve each message's radix and meaning, not convert everything to hex;
- fixes mb89352 by REMOVING the unsupported trailing value field, since `idata` is still zero at that point.

**ARC fix (option set completed).**  Boundary membership:
1. handle NULL, and fix the low-32-bit NULL test, which aliases ARC64 `0x100000000` to NULL;
2. reject `a0 < base`;
3. take an unsigned wide difference;
4. reject a nonzero remainder and an out-of-range index, BEFORE any multiplication.

Rows: NULL, the first and last descriptors, `base-1`, `base-s`, `base-2*s`, a misaligned interior pointer, and a large-offset
alias.  The ARC32 rung-3 witness is `A0 = base-24` returning `base-12` today.

**New finding.**  `src/console/x11.c:551` has a stray comma that splits a format string, so `%i` consumes a string pointer.  The
fix is to remove the comma, not to cast.

**Counts corrected.**  145 `-Wformat=` warnings, INCLUDING the 3 missing-argument ones, plus 13 extra-argument warnings, on 127
unique lines.  Wrong-type and extra-argument warnings alone occupy 125 lines; mb89352 is in both groups.

**Premise (a) settled by MEASUREMENT, not by the adjudication.**  The same attributed build of the pushed commit 759f7131
(`fmtscanp.out`, `fmtp_make.log`) gives 190 format warnings against HEAD's 181.  Matched by file, kind and message shape:
- 0 warnings at HEAD are absent at the push;
- the 9 that disappeared are exactly the 9 CodeQL alerts rewritten since (dev_sgi_re.c 7, dev_lca.c 1, dev_sgi_ip32.c 1).

**Dismissal reasons, corrected.**

| alert(s) | reason |
|---|---|
| fdc #117 | false positive |
| diskimage #137 | won't fix: a real host race, outside the threat model |
| ROM tool #1/#2 | won't fix: real mismatches, deprioritised, not a false positive |
| MIPS #121/#122, SH #123 | false positive |
| fb init #124 | won't fix / HOST: NOT bounded -- a host VGA scale of 53 overflows `int` at dev_fb.c:905 |
| fb #125-#127 | false positive |
| ps2 GIF #128/#129 | won't fix: disabled demonstration code, `test_triangle` called only under `#if 0` (dev_ps2_gif.c:424); my "16-bit coordinates" provenance was another path's |
| PVR #130, PX #131 | false positive |
| VGA #132 | won't fix / HOST |
| ELF #133/#134 | false positive: entry sizes must equal fixed sizes or loading exits, so the products are < 2^22 |
| ARC init #136 | false positive |
