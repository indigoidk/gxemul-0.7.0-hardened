ASTRA RETRO-REVIEW `devdreamcastgdrom` -- GXemul fork, the net changes to 1 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_DEVDREAMCASTGDROM_ALIVE` on its own line, then ONE verdict line:
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
| `src/devices/dev_dreamcast_gdrom.c` | 1273 | 15 | 15 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `8dd86b5a` 2026-06-28 the fork's first corrections batch, #1-#119 (subject abbreviated; read it with git log)  [dev_dreamcast_gdrom.c]
- `029a1372` 2026-08-23 gdromdmawidth: ASSESSED, NOT CHANGED -- a unanimous panel overturned from source  [dev_dreamcast_gdrom.c]
- `96196f3c` 2026-08-23 #461 aftermath: a goto-fail shape I introduced, two measured-false claims, and five 32/32 escapes filed  [dev_dreamcast_gdrom.c]
- `98a34085` 2026-08-23 #460: GDROM_DATA had no legal first touch -- four exit(1) on one register  [dev_dreamcast_gdrom.c]
- `ba30e64f` 2026-08-23 #461 both `default:` arms of the GD-ROM device ended the host process  [dev_dreamcast_gdrom.c]
- `7c9dd9eb` 2026-08-24 #462 both arms of the GD-ROM DMA trigger (case 0x18) ended the host process on a guest store  [dev_dreamcast_gdrom.c]
- `4d05cf0b` 2026-08-26 #465 dev_dreamcast_gdrom.c: data and data_len were released apart, and the detector ran in no gate  [dev_dreamcast_gdrom.c]
- `5b5089d0` 2026-08-26 #465 pass 2: the panel refuted my own framing, and the "owed" rows already existed  [dev_dreamcast_gdrom.c]
- `84f6682d` 2026-08-27 gdromwarnbits: the PRE-SET trigger fired -- six masks become an enum of bit positions, `warned` widens to uint32_t, and the row does NOT close  [dev_dreamcast_gdrom.c]
- `095aa960` 2026-08-28 #489 gdrom: a guest-supplied length ended the host, and deleting the guard would have been worse  [dev_dreamcast_gdrom.c]
- `84765ec7` 2026-08-28 gdromwarnbits: the bound is now a COMPILE ERROR, and this file already had four  [dev_dreamcast_gdrom.c]
- `fb0cc783` 2026-08-29 #490 GD-ROM handle_command: two guest-reachable host kills, plus a wsl-dollar hook  [dev_dreamcast_gdrom.c]
- `105c15c7` 2026-08-30 #496: the detector's first CLEAN baselines, two more escapes closed, and a selftest that broke because the tree got better  [dev_dreamcast_gdrom.c]
- `439dfd05` 2026-08-30 #496 follow-up: two MEASURED escapes closed, and a deriver that matched itself  [dev_dreamcast_gdrom.c]
- `c516a9c9` 2026-08-30 #496 GD-ROM: two guest-reachable host kills de-fatalised, plus the store that made a naive fix worse than the defect -- and the ADJUDICATION PASS  [dev_dreamcast_gdrom.c]

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
