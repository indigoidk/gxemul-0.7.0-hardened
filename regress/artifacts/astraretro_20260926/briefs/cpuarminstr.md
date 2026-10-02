ASTRA RETRO-REVIEW `cpuarminstr` -- GXemul fork, the net changes to 1 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_CPUARMINSTR_ALIVE` on its own line, then ONE verdict line:
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
| `src/cpus/cpu_arm_instr.c` | 1304 | 27 | 23 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [cpu_arm_instr.c]
- `5ee491e7` 2026-07-02 corrections batch #120-#154 and feature round #120-#129 (subject abbreviated)  [cpu_arm_instr.c]
- `a06e92fb` 2026-07-31 Round 71 (#311, #312, #313): ARM -- two wrong flags and one more halt  [cpu_arm_instr.c]
- `0c1eb584` 2026-08-01 Round 78 addendum (#322) + round 84: the panel overturned one call and stopped another  [cpu_arm_instr.c]
- `cbbe1ec0` 2026-08-01 Round 78 (#319, #320, #321): ARM rotations answered by halting -- and a carry read off the complement  [cpu_arm_instr.c]
- `597a71b5` 2026-08-03 Round 83 (#340): folding a compare into a branch changed the flags  [cpu_arm_instr.c]
- `4b031420` 2026-08-05 Round 93 (#342): the XOR-swap fold had no "two distinct registers" guard  [cpu_arm_instr.c]
- `be6ea08a` 2026-08-05 Round 97 (#346): the cache-clean fold ignored the stride its own arithmetic assumed  [cpu_arm_instr.c]
- `d143bd5b` 2026-08-05 Round 94 (#345): the cache-clean fold matched a loop's shape and ignored its registers  [cpu_arm_instr.c]
- `dea2fefd` 2026-08-05 Round 98 (#347): the second cache-clean fold skipped a loop and updated nothing  [cpu_arm_instr.c]
- `307b1b82` 2026-08-10 Round 100 (#351, #352, #353): the idle-loop fold skipped its writes, aliased a register, and hung the guest  [cpu_arm_instr.c]
- `704036ef` 2026-08-10 Round 99 (#348, #349, #350): the cache-clean folds learned their exit flags  [cpu_arm_instr.c]
- `7d3238f0` 2026-08-10 Round 101 (#354): the memcpy fold moved the bytes but never published the registers  [cpu_arm_instr.c]
- `1751ae27` 2026-08-11 Round 108 (#362): unaligned word loads returned the aligned word, unrotated  [cpu_arm_instr.c]
- `221328df` 2026-08-11 Round 104 (#358): five folds were doing work no test could see, and #357 removed the only witness  [cpu_arm_instr.c]
- `38537dee` 2026-08-11 Round 102 (#355, #356): the strlen fold answered a question the architecture never asked, and never came up for air  [cpu_arm_instr.c]
- `396c3f8a` 2026-08-11 Round 106 (#360): the row that asserted an absence still passed when the fold was dead  [cpu_arm_instr.c]
- `5b225bc3` 2026-08-11 Round 107 (#361): the last two folds with markers but no rows, and a negative arm that was vacuous alone  [cpu_arm_instr.c]
- `276fd0b2` 2026-08-12 Round 120 (#379): #378's pass-2 findings -- a false-green route and five record errors  [cpu_arm_instr.c]
- `813ee67a` 2026-08-12 #386: swp — byte-order on both sides, rotate on the load, aligned word for both accesses  [cpu_arm_instr.c]
- `c113e677` 2026-08-12 Round 123 (#382): the copyin/copyout folds moved byte-reversed words on a BE guest  [cpu_arm_instr.c]
- `e9230ad6` 2026-08-12 Round 119 (#378): a BE guest's LDM/STM through a warm page was byte-reversed  [cpu_arm_instr.c]
- `8b1a7fdf` 2026-08-13 #390: one scratch word, two roles — a PC-relative store's base was four bytes high  [cpu_arm_instr.c]
- `01a0339a` 2026-09-07 #510 follow-up: the two SBFX cells codex named, and a false claim in c0c7f55's own message  [cpu_arm_instr.c]
- `c0c7f55d` 2026-09-07 #510 armbfxwidth32: UBFX and SBFX built their mask with an undefined shift  [cpu_arm_instr.c]
- `eb839923` 2026-09-07 #510 pass 2: the panel was right and I refuted it, plus a broken comment I shipped in 01a0339  [cpu_arm_instr.c]
- `4dfc7165` 2026-09-12 #524 (armbdt): an ARM block transfer through a cold host page spliced bytes across a word boundary -- the same LDM/STM at the same unaligned base r...  [cpu_arm_instr.c]

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
