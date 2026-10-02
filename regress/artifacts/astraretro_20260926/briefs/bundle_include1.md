ASTRA RETRO-REVIEW `bundle_include1` -- GXemul fork, the net changes to 5 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_BUNDLE_INCLUDE1_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <n> findings (<k> CODE live at HEAD, <r> RECORD, <t> TEST-GAP); <c> items checked clean`

**Why you are asked.** This fork of GXemul 0.7.0 has shipped several hundred correction rounds since June 2026. Each
was reviewed by a multi-model panel when it landed, but the panel's Codex seat was GPT-5.6-Sol until 2026-09-04 and
was unavailable on several later days -- so most of these changes have never been read by you. This is that first
reading. Please do not simply ratify: this project's recorded premises have been wrong often enough that a claim
nobody checked is the likeliest place for a defect to sit. Check the premises, not only the derivations.

**The tree.** Repository `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git). Commit `39748e3c` is the unmodified upstream
import; everything after it is the fork. Review HEAD ONLY:
- the fork's net change to a file: `git diff 39748e3c HEAD -- <path>`
- a file as committed: `git show HEAD:<path>`
- one round's change: `git show --format= <sha> -- <path>` (never `git show <sha> | head`: the commit message
  prints first and is long, so a cut shows no diff at all)
- a round's record: its `#NNN` block in `CHANGELOG.md` (`git show HEAD:CHANGELOG.md | grep -n '#NNN'`)

The WORKING-TREE copies carry other people's uncommitted work that is NOT under review, so do not read
`GXEMUL-SEC/src/...` from disk. Ignore every other `src/` under the project root: `src/` (pristine 2021 upstream),
`est/`, `build/`, `build-asan/` and `_archive/` are other copies, and a copy reports line numbers off by hundreds.

**What the fork is for, and so what counts as a finding.**
1. **CODE** -- nothing a guest does (instructions it executes, device registers it reads or writes, disk or network
   data it supplies) should make the emulator index or copy outside an array or buffer, read uninitialised memory,
   divide by zero, shift by the operand width or more, overflow a signed integer, loop without bound, or reach
   `exit()`/`abort()`. Where a round changed guest-visible behaviour, it should match the documented hardware
   (manuals: `ls _scratchpad/*.txt`; cite a line when a finding rests on one). **A round that corrected one path
   and left a sibling in the old state -- another case label, another access width, the read versus the write
   direction, the other array, the other unit -- is a finding.** So is a correction whose guard reads a different
   field from the one its guarded body uses.
2. **RECORD** -- a `/* #NNN: ... */` comment or the round's CHANGELOG sentence that is false of the code at HEAD.
   A line number that has drifted a few lines is NOT a finding; a claim about behaviour the code does not have IS.
3. **TEST-GAP** -- a behaviour a round says it pinned that no regression row under `regress/` observes (name the
   probe you checked). Keep these short; CODE findings matter most.

Upstream code the fork never touched is out of scope unless a fork change relies on it.

**The files** (delta = lines added plus deleted since the import):

| file | delta | rounds | before 2026-09-04 |
|---|---|---|---|
| `src/include/diskimage.h` | 81 | 4 | 4 |
| `src/include/cpu_ppc.h` | 71 | 5 | 5 |
| `src/include/cpu_mips.h` | 68 | 2 | 2 |
| `src/include/thirdparty/dreamcast_sysasicvar.h` | 68 | 3 | 3 |
| `src/include/float_emul.h` | 65 | 7 | 7 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [cpu_ppc.h]
- `5ee491e7` 2026-07-02 corrections batch #120-#154 and feature round #120-#129 (subject abbreviated)  [diskimage.h]
- `de1398e1` 2026-07-17 Hardening/fidelity/debuggability rounds 17–25 (#155–#250)  [cpu_ppc.h]
- `3eaaf3a4` 2026-07-29 Fix #292: single-precision float results were 1 ulp low half the time  [cpu_mips.h, float_emul.h]
- `64400062` 2026-07-29 Fix #294: cvt.w honours the FPU rounding mode; trunc.w provably does not  [float_emul.h]
- `4453ff2a` 2026-07-30 Fix #301: cvt.d.l converted the integer before the rounding mode existed  [float_emul.h]
- `51899d78` 2026-07-30 Fix #299: the single-precision sum was rounded twice; round-to-odd makes the first rounding harmless  [float_emul.h]
- `e644a300` 2026-07-30 Fix #300: the D-format store has nothing to round, so the arithmetic learned to  [float_emul.h]
- `0fc81c5e` 2026-07-31 Fix #306/#307/#308: a family of legal m88k instructions that stopped the machine  [float_emul.h]
- `37daeeef` 2026-07-31 Fix #304/#305: the PowerPC narrowed with a host cast, and threw away every NaN it touched  [cpu_ppc.h]
- `37963fd9` 2026-08-01 Round 87 (#326): twenty-four legal PowerPC encodings stopped the emulator, and every floating-point record form was one of them  [float_emul.h]
- `ad0e67da` 2026-08-01 Round 88 (#327): VX and FEX were stored, and the ISA defines them as derived  [cpu_ppc.h]
- `130ff1b5` 2026-08-02 Round 89 (#330): the exception causes VX and FEX had nothing to derive from  [cpu_ppc.h]
- `792fea09` 2026-08-12 #388: MIPS fold witness, phase A — 34 variants, counters, tlbdump schema  [cpu_mips.h]
- `154d21cd` 2026-08-14 #414: every -d g disk and every floppy reported zero capacity, from one multiplication with two factors nobody computed  [diskimage.h]
- `c6169e06` 2026-08-14 #416: one guest WRITE past the end of a 10 KB image grew it to 512 MB, and the guest was told it succeeded  [diskimage.h]
- `4d0981dc` 2026-08-18 #437: SYNCHRONIZE CACHE told the guest its data was safe and synced the wrong file  [diskimage.h]
- `29b450ce` 2026-08-26 #467 + #468: the pty deadline means SILENCE, and the ASIC domain is now ENFORCED  [dreamcast_sysasicvar.h]
- `4d7b2f41` 2026-08-26 farm harvest: one critical escalation, one confirmation, and TWO briefing failures of mine  [dreamcast_sysasicvar.h]
- `9ca9ccae` 2026-08-26 #466 asiceventaddr: state the domain restriction where the event-adder will read it  [dreamcast_sysasicvar.h]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha that introduced it, or "upstream, relied on by #NNN"> | CODE / RECORD /
TEST-GAP | live at HEAD: yes/no | the concrete guest action or input, and the wrong result | the smallest check that
would settle it (a debugger session, a unit test, a grep) | confidence high/med/low`

If `OUTSTANDING_BUGS.md` at HEAD already files it (`git show HEAD:OUTSTANDING_BUGS.md | grep -n <word>`), say so and
give the id -- that is useful, not a failure.

**Then the denominator.** List the items you checked and found correct, one line each with a line number at HEAD,
and end with `DENOMINATOR: read <h> of <H> hunks of the net diff`. "No finding" and "not looked at" must not look the
same.

Read-only: write nothing, build nothing, run nothing that changes a file.
