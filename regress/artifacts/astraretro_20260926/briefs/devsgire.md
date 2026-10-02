ASTRA RETRO-REVIEW `devsgire` -- GXemul fork, the net changes to 1 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_DEVSGIRE_ALIVE` on its own line, then ONE verdict line:
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
| `src/devices/dev_sgi_re.c` | 692 | 14 | 8 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [dev_sgi_re.c]
- `112867a6` 2026-08-30 #497 closes: the round's record, plus a live defect in panel.sh that was mine  [dev_sgi_re.c]
- `821eb83b` 2026-08-30 #497 widthkillclass: six guest-reachable host kills in dev_sgi_re.c become latched declines  [dev_sgi_re.c]
- `938b328e` 2026-08-31 #499 L2: two mutants swept the detector clean, one restoring the round's own witness  [dev_sgi_re.c]
- `9f666a8d` 2026-08-31 #499 sgireunmapped: a 2080-byte door closed, with the order proof re-run locally  [dev_sgi_re.c]
- `a481d8b4` 2026-08-31 #499 pass 2, run LATE because the round shipped without one -- and it found three defects  [dev_sgi_re.c]
- `cb28a6f5` 2026-08-31 #498 sgidewidth: a guest `sb` ended the host -- and the OBVIOUS fix scores 24/25  [dev_sgi_re.c]
- `840f3d0a` 2026-09-01 #500 sgideprimop: a drawing op a guest never chose, and the reset value was one  [dev_sgi_re.c]
- `257f56f1` 2026-09-07 #504 sgirandompixel: a failed pixel read handed the caller random() and the write stored it; plus the pass-2 receipt 79cd12e owed, and a measured f...  [dev_sgi_re.c]
- `2956c7e8` 2026-09-07 #509 sgimtedepth4dead: `depth == 4' is unreachable, so tiled MTE always took CI  [dev_sgi_re.c]
- `7a41b3fb` 2026-09-07 #505 #506 #507 #508: four test-first rounds, three new rung-3 witnesses, and a witness row that could not fail  [dev_sgi_re.c]
- `e302c98c` 2026-09-08 #513 sgirekills: six host kills removed from dev_sgi_re read arms, and the detector that shipped with them survived four adversarial passes  [dev_sgi_re.c]
- `fd150657` 2026-09-12 #519 (sgirandomcolour): the colour-mode PUT default arm stored four host random() bytes into guest memory -- reachable with the documented DE_MODE_...  [dev_sgi_re.c]
- `bead6ad9` 2026-09-24 #547 upstreamdeleteprose: one word of a comment turns gate 8's delete row green at HEAD; attrabbrev: the rider's nine-seat review repairs a regress...  [dev_sgi_re.c]

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
