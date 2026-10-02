ASTRA RETRO-REVIEW `bundle_include2` -- GXemul fork, the net changes to 10 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_BUNDLE_INCLUDE2_ALIVE` on its own line, then ONE verdict line:
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
| `src/include/timer.h` | 49 | 2 | 2 |
| `src/include/cpu_arm.h` | 37 | 2 | 2 |
| `src/include/machine.h` | 31 | 2 | 2 |
| `src/include/misc.h` | 27 | 3 | 3 |
| `src/include/cpu_m88k.h` | 25 | 2 | 2 |
| `src/include/opcodes_ppc.h` | 19 | 3 | 3 |
| `src/include/thirdparty/mvme_pcctworeg.h` | 11 | 1 | 0 |
| `src/include/cpu.h` | 10 | 1 | 1 |
| `src/include/net.h` | 7 | 2 | 2 |
| `src/include/thirdparty/bootblock.h` | 6 | 1 | 1 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [bootblock.h, machine.h, misc.h]
- `5ee491e7` 2026-07-02 corrections batch #120-#154 and feature round #120-#129 (subject abbreviated)  [cpu.h, misc.h, net.h]
- `de1398e1` 2026-07-17 Hardening/fidelity/debuggability rounds 17–25 (#155–#250)  [machine.h, net.h]
- `962bf098` 2026-07-18 Round 32 (#259, #260, #261): debugger/net QoL  [misc.h]
- `85cc973a` 2026-07-30 Fix #298: m88k stored its rounding register, read it back, and used it nowhere  [cpu_m88k.h]
- `638eff28` 2026-07-31 Fix #309/#310: two more decoders that stopped the machine on legal code  [opcodes_ppc.h]
- `37963fd9` 2026-08-01 Round 87 (#326): twenty-four legal PowerPC encodings stopped the emulator, and every floating-point record form was one of them  [opcodes_ppc.h]
- `6f916cd5` 2026-08-05 Round 96 (#344): the negative multiply-adds were never decoded, and halted the emulator  [opcodes_ppc.h]
- `2c615c3c` 2026-08-11 Round 112 (#367): path attribution stops being a comment and becomes a checked quantity  [cpu_arm.h]
- `ed242c0d` 2026-08-12 Round 121 (#380): the m88k idle fold ran the bcnd.n delay slot zero times  [cpu_m88k.h]
- `8b1a7fdf` 2026-08-13 #390: one scratch word, two roles — a PC-relative store's base was four bytes high  [cpu_arm.h]
- `863d2389` 2026-08-15 R4 (#427, #428, #429): the timer core clamped one end of a frequency and left the other unbounded  [timer.h]
- `cdc48499` 2026-08-15 R4 follow-up: the round's detector certified six things it could not see  [timer.h]
- `54a2eb44` 2026-09-09 #517 pcc2genctlc040alias: a vendored header defined C040 twice, and the second definition was a different register's bits  [mvme_pcctworeg.h]

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
