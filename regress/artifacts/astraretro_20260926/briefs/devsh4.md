ASTRA RETRO-REVIEW `devsh4` -- GXemul fork, the net changes to 1 source file(s), at HEAD 8ea26abb

Open your answer with the token `ASTRARETRO_DEVSH4_ALIVE` on its own line, then ONE verdict line:
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
| `src/devices/dev_sh4.c` | 1248 | 18 | 18 |

**Their rounds**, oldest first (the bracket names which of these files each touched):

- `3ab1a406` 2026-07-29 Fix #293: typed input on SuperH was stolen before the serial port saw it  [dev_sh4.c]
- `28ac1f8b` 2026-08-13 #400: the SH-4 timer pinned itself at zero, and a booting guest's clock stopped  [dev_sh4.c]
- `9de16b79` 2026-08-20 #441 sh4bcr: two guest instructions ended the emulator process  [dev_sh4.c]
- `3536d869` 2026-08-21 #443 pass 2: seven mutants all scored 29/29, and my own kill table said so  [dev_sh4.c]
- `6bec468c` 2026-08-21 #443 sh4pcicexit: one guest LOAD ended the host, on 116 of 137 offsets  [dev_sh4.c]
- `a636a339` 2026-08-21 #448 sh4chcr: a LEGAL DMA configuration ended the host on its resource-select alone  [dev_sh4.c]
- `e841f443` 2026-08-21 #447 sh4valguards: one guest STORE ended the host, at four sites whose store positions differ  [dev_sh4.c]
- `f4374117` 2026-08-21 #449 sh4rtcsr: the host died nine milliseconds after the guest store, in a timer callback  [dev_sh4.c]
- `0f77c7a3` 2026-08-22 L4 accumulator row, the SH manual re-check, and four corrected overclaims  [dev_sh4.c]
- `759f7131` 2026-08-22 sh4_chcr: a two-character edit restored a host death at 18/18 -- add the L0 safety row  [dev_sh4.c]
- `927553fa` 2026-08-22 #452 sh4 TLB data array 2: decline the access instead of ending the host process  [dev_sh4.c]
- `b3ad305a` 2026-08-22 #451 sh4_sci_cmd(): decline the command instead of ending the host process  [dev_sh4.c]
- `f532bb6a` 2026-08-22 #453 sh4_dmac_transfer(): the last guest-reachable host death, and hardware accuracy meant NOT sending the interrupt  [dev_sh4.c]
- `0bb8be2b` 2026-08-23 #459: one guest store to 0xffd80010 ended the host on 3 of 5 SH machines  [dev_sh4.c]
- `2965aa1b` 2026-08-23 #459 records: close sh4pclock, file four, grade nine seats  [dev_sh4.c]
- `3ad72e04` 2026-08-23 harness: score-claims gate, verdict-extractor fix, floor clause (d), 2 filings  [dev_sh4.c]
- `7e5c0f6c` 2026-08-23 #458: SH-4 read two of four interrupt priority registers, and SCIF's came       from a register this machine never maps  [dev_sh4.c]
- `e4390ea0` 2026-08-23 #459 pass-2 corrections: three wrong records, all found by measurement  [dev_sh4.c]

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
