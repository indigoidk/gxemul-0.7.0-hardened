ASTRA RETRO-REVIEW `cpushinstr` -- GXemul fork, the net changes to 1 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_CPUSHINSTR_ALIVE` on its own line, then ONE verdict line:
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
| `src/cpus/cpu_sh_instr.c` | 977 | 13 | 13 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [cpu_sh_instr.c]
- `5ee491e7` 2026-07-02 corrections batch #120-#154 and feature round #120-#129 (subject abbreviated)  [cpu_sh_instr.c]
- `f52c2fe3` 2026-07-29 Fix #296: SuperH read the FPU rounding-mode field but never used it  [cpu_sh_instr.c]
- `06445b53` 2026-07-30 Fix #297: ftrc converted with a raw C cast, so the guest's answer depended on the host  [cpu_sh_instr.c]
- `51899d78` 2026-07-30 Fix #299: the single-precision sum was rounded twice; round-to-odd makes the first rounding harmless  [cpu_sh_instr.c]
- `e644a300` 2026-07-30 Fix #300: the D-format store has nothing to round, so the arithmetic learned to  [cpu_sh_instr.c]
- `54f72c06` 2026-07-31 Round 80 (#315, #316, #317): the SuperH halts a decode sweep cannot see  [cpu_sh_instr.c]
- `6a2f41c2` 2026-07-31 Round 81 (#318): the store-queue flush round 80 refused to guess at  [cpu_sh_instr.c]
- `f415b919` 2026-07-31 Round 79 (#314): SuperH answered a legal instruction by stopping  [cpu_sh_instr.c]
- `064caaf6` 2026-08-02 Round 72 (#331-#334): there was no gradual underflow, and three architectures were relying on it  [cpu_sh_instr.c]
- `441b2037` 2026-08-03 Round 85 partial (#339): settle why fsrra uses the legacy store  [cpu_sh_instr.c]
- `3ff21380` 2026-08-22 #454 the store-queue PREF transfer is judged READ type, and a gate row pinned the opposite  [cpu_sh_instr.c]
- `d2c32fa3` 2026-08-22 SH re-check pass 2: the corrections were themselves overclaimed, twice  [cpu_sh_instr.c]

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
