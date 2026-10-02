ASTRA RETRO-REVIEW `bundle_devices2` -- GXemul fork, the net changes to 7 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_BUNDLE_DEVICES2_ALIVE` on its own line, then ONE verdict line:
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
| `src/devices/dev_luna88k.c` | 83 | 3 | 2 |
| `src/devices/dev_dreamcast_asic.c` | 78 | 5 | 5 |
| `src/devices/dev_pckbc.c` | 57 | 1 | 1 |
| `src/devices/dev_rs5c313.c` | 56 | 1 | 1 |
| `src/devices/dev_fdc.c` | 41 | 1 | 1 |
| `src/devices/dev_disk.c` | 40 | 1 | 1 |
| `src/devices/grep.exe.stackdump` | 37 | 2 | 2 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [dev_disk.c, dev_luna88k.c, grep.exe.stackdump]
- `05488a1e` 2026-07-26 Round 47 (#280): dev_fdc.c -- one host line per guest access to an unmodelled register  [dev_fdc.c]
- `992bccbd` 2026-07-27 Round 52 (#288): the arc keyboard queue discarded itself, and its drain loop starved the guest  [dev_pckbc.c]
- `f52c2fe3` 2026-07-29 Fix #296: SuperH read the FPU rounding-mode field but never used it  [grep.exe.stackdump]
- `e098973c` 2026-08-14 #404: the SH-4 RTC is not settable, and that is recorded rather than guessed  [dev_rs5c313.c]
- `cf4b083c` 2026-08-19 #438 exitsweep: a guest store to INT_ST_MASK0-3 ended the emulator process  [dev_luna88k.c]
- `0798b903` 2026-08-25 ledger semantics, a research stage fired after the round closed, and four rules  [dev_dreamcast_asic.c]
- `97288665` 2026-08-25 #463 close-out: the severity was larger than measured, and the latch is refuted  [dev_dreamcast_asic.c]
- `f1fa6a0a` 2026-08-25 #463 dreamcast_asic: one guest LOAD ended the host, at 64 byte addresses  [dev_dreamcast_asic.c]
- `f4b8dbea` 2026-08-25 #463 pass 2, owed and refused by the gate: four wrong claims, and five more in the corrections  [dev_dreamcast_asic.c]
- `29b450ce` 2026-08-26 #467 + #468: the pty deadline means SILENCE, and the ASIC domain is now ENFORCED  [dev_dreamcast_asic.c]
- `79cd12e8` 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of it...  [dev_luna88k.c]

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
