ASTRA RETRO-REVIEW `devasc` -- GXemul fork, the net changes to 1 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_DEVASC_ALIVE` on its own line, then ONE verdict line:
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
| `src/devices/dev_asc.c` | 410 | 11 | 11 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [dev_asc.c]
- `de1398e1` 2026-07-17 Hardening/fidelity/debuggability rounds 17–25 (#155–#250)  [dev_asc.c]
- `508ab233` 2026-07-18 Round 36 (#265, #266): ASC FIFO occupancy + chip-reset IRQ hygiene  [dev_asc.c]
- `794c4159` 2026-07-18 Round 34 (#263): ASC/R4030 DMA accounting -- heap disclosure + over-transfer  [dev_asc.c]
- `87c062aa` 2026-07-18 Round 35 (#264): ASC zero-length DATA_OUT host-abort -> guest disconnect  [dev_asc.c]
- `be95418e` 2026-07-25 Round 40 (#269, #270): self-review fixes -- ASC FIFO diagnostic flood, breakpoint-listing honesty  [dev_asc.c]
- `26de8803` 2026-07-26 Round 50 (#286): the DATA_IN counter still reported the count REQUESTED, not the count that MOVED  [dev_asc.c]
- `2b52fca4` 2026-07-26 Round 49 (#283): ASC -- a short DATA_OUT DMA committed bytes the guest never supplied  [dev_asc.c]
- `85220652` 2026-07-26 Round 49 (#284): ASC -- the COMMAND-phase DMA counter said "nothing moved" and "complete" at once  [dev_asc.c]
- `a0d34f4c` 2026-07-26 Round 48 (#281, #282): ASC -- a short DATA_IN transfer reported as if the full count had moved  [dev_asc.c]
- `d917a664` 2026-07-26 Round 44 (#276, #277): ASC -- two guest-repeatable diagnostic floods, fixed in deliberately opposite ways  [dev_asc.c]

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
