ASTRA RETRO-REVIEW `bundle_cpus1` -- GXemul fork, the net changes to 8 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_BUNDLE_CPUS1_ALIVE` on its own line, then ONE verdict line:
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
| `src/cpus/memory_sh.c` | 94 | 3 | 3 |
| `src/cpus/memory_ppc.c` | 68 | 2 | 2 |
| `src/cpus/cpu_dyntrans.c` | 54 | 3 | 3 |
| `src/cpus/cpu_alpha_instr.c` | 42 | 1 | 1 |
| `src/cpus/cpu_arm_instr_dpi.c` | 40 | 1 | 1 |
| `src/cpus/grep.exe.stackdump` | 37 | 2 | 2 |
| `src/cpus/cpu_ppc_instr_loadstore.c` | 33 | 1 | 1 |
| `src/cpus/tmp_mips_loadstore_multi.c` | 32 | 1 | 1 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [cpu_dyntrans.c, grep.exe.stackdump, memory_ppc.c]
- `5ee491e7` 2026-07-02 corrections batch #120-#154 and feature round #120-#129 (subject abbreviated)  [cpu_dyntrans.c]
- `de1398e1` 2026-07-17 Hardening/fidelity/debuggability rounds 17–25 (#155–#250)  [cpu_dyntrans.c, memory_ppc.c]
- `f52c2fe3` 2026-07-29 Fix #296: SuperH read the FPU rounding-mode field but never used it  [grep.exe.stackdump]
- `6a2f41c2` 2026-07-31 Round 81 (#318): the store-queue flush round 80 refused to guess at  [memory_sh.c]
- `a06e92fb` 2026-07-31 Round 71 (#311, #312, #313): ARM -- two wrong flags and one more halt  [cpu_arm_instr_dpi.c]
- `064caaf6` 2026-08-02 Round 72 (#331-#334): there was no gradual underflow, and three architectures were relying on it  [cpu_alpha_instr.c]
- `078f88e8` 2026-08-13 Regenerate tmp_mips_loadstore_multi.c: #388 changed the generator and left its tracked output stale  [tmp_mips_loadstore_multi.c]
- `2458cfba` 2026-08-15 R5 (#430, #431): memory_rw translated the first page and then copied straight past it  [cpu_ppc_instr_loadstore.c]
- `0f77c7a3` 2026-08-22 L4 accumulator row, the SH manual re-check, and four corrected overclaims  [memory_sh.c]
- `3ff21380` 2026-08-22 #454 the store-queue PREF transfer is judged READ type, and a gate row pinned the opposite  [memory_sh.c]

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
