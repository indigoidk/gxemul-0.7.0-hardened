ASTRA RETRO-REVIEW `devwdc` -- GXemul fork, the net changes to 1 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_DEVWDC_ALIVE` on its own line, then ONE verdict line:
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
| `src/devices/dev_wdc.c` | 1273 | 26 | 22 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `052982ae` 2026-08-02 Round 70C (#337): four guest-reachable exit(1) calls in the IDE controller  [dev_wdc.c]
- `c941fe3c` 2026-08-03 #341: dev_wdc's ATAPI read accounted for bytes it never delivered  [dev_wdc.c]
- `085766ac` 2026-08-14 #407: #405's detector had four holes and a note that was wrong the flattering way  [dev_wdc.c]
- `154d21cd` 2026-08-14 #414: every -d g disk and every floppy reported zero capacity, from one multiplication with two factors nobody computed  [dev_wdc.c]
- `2e709cdb` 2026-08-14 #405: ATA IDENTIFY packed its capacity bytes with `% 255`, not `& 255`  [dev_wdc.c]
- `e86e293a` 2026-08-14 #408: the round that fixed stale citations made the identical error, and the detector was relying on -O2 to hide UB  [dev_wdc.c]
- `baacf9bb` 2026-08-26 #464 wdc: six unlatched fatal() bounded, and the detector's first gate  [dev_wdc.c]
- `0922465f` 2026-08-27 #477 wdc ATAPI: a guest data-port WRITE could free the transfer being delivered  [dev_wdc.c]
- `1cec2daf` 2026-08-27 #476 wdc: #475's clamp WOKE a NULL dereference -- two guest accesses killed the host  [dev_wdc.c]
- `1f1a02bb` 2026-08-27 #473 wdc ATAPI DATAIN: bound the initial push, and stop reporting zero at the re-arm  [dev_wdc.c]
- `23430365` 2026-08-27 #479 wdc: a new command did not reset what the old one left  [dev_wdc.c]
- `77b7c03a` 2026-08-27 #485 pass 2: the detector was below the floor TWICE, and the pass the round skipped found it  [dev_wdc.c]
- `7d0b63d4` 2026-08-27 #480 wdc: the detector could not see its own call  [dev_wdc.c]
- `832bed78` 2026-08-27 #478 wdc: an empty ring was read as a full sector, and 512 stale bytes went to the disk  [dev_wdc.c]
- `867c697b` 2026-08-27 #481 wdc: the reset bit was the head-count bit  [dev_wdc.c]
- `cf300c07` 2026-08-27 #484 wdc: a full ring reported itself empty, and the next push destroyed a byte  [dev_wdc.c]
- `d64a1fc3` 2026-08-27 #475 wdc ATAPI: clamp the byte count to what REMAINS; plus #474's pass-2 second wave  [dev_wdc.c]
- `d8191881` 2026-08-27 #485 wdc: 242 of 256 opcodes ended a command and never raised its interrupt  [dev_wdc.c]
- `d894e35d` 2026-08-27 #474 footbridge TIMER_x_CLEAR read-clears; plus #473's pass-2 corrections  [dev_wdc.c]
- `67120fd6` 2026-08-30 #495 wdc: a host store during an ATAPI DATA-IN transfer was pushed into the ring, and the guest read its own bytes back as disk data  [dev_wdc.c]
- `6a5267c0` 2026-08-30 records: a reopening warrant that was retired before it was quoted, and three tools whose numbers were wrong  [dev_wdc.c]
- `c1254506` 2026-08-30 #494 wdc: the alt-ctrl handler never decoded its own offset, so a store to a read-only register aborted a live transfer  [dev_wdc.c]
- `83df95c3` 2026-09-05 Retrospective re-check batch 3a (dev_wdc.c #337..#464): every fix holds; two guest-visible ATAPI defects filed MEDIUM, seven LOW rows, two merges, ...  [dev_wdc.c]
- `79cd12e8` 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of it...  [dev_wdc.c]
- `599a7a82` 2026-09-12 #525 (wdcaltdigin): the alt-status handler never decoded its offset ON THE READ SIDE, so a read of the Drive Address register returned the ALT-STAT...  [dev_wdc.c]
- `e16a8b7c` 2026-09-18 #533 landiskaux: landisk's wdc aux register sat at the PC-layout +0x206, so the kernel's soft reset landed on unmapped memory  [dev_wdc.c]

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
