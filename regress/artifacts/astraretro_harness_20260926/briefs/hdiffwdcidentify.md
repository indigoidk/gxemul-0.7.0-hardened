ASTRA RETRO-REVIEW (HARNESS) `hdiffwdcidentify` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HDIFFWDCIDENTIFY_ALIVE` on its own line, then ONE verdict line:
`VERDICT: <n> findings (<k> CANNOT-FAIL, <s> SELECTS-NOTHING, <x> STATUS-LAUNDERED, <e> ENCODING, <r> RECORD, <o> OTHER);
<c> items checked clean`

**Why you are asked.**  This fork of GXemul 0.7.0 guards several hundred correction rounds with its own regression
harness: Python probes that drive the emulator's debugger through a pty, gate scripts that score them, offline C
differentials, and pipeline checkers run before every commit.  The harness was reviewed as it landed, but mostly
before you (GPT-6 Astra) joined the review panel on 2026-09-04 -- this is your first reading of most of it.  A
regression row that cannot fail is worse than no row, because it reports coverage that does not exist; please look
for exactly that, and do not simply ratify.

**The tree.**  Repository `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC` (git).  Review HEAD ONLY: `git show HEAD:<path>`;
a file's history `git log --format='%h %ad %s' --date=short -- <path>`; one round's change
`git show --format= <sha> -- <path>`.  The WORKING TREE carries other people's uncommitted work -- do not read from
disk.  The emulator source the probes exercise is `src/` in the same repository, at HEAD.

**What counts as a finding.**
1. **CANNOT-FAIL** -- a row or check whose expected value is also what the code would produce WITHOUT the correction
   it guards (for example a survive-only row at a site where the corrected code refuses and the uncorrected code also
   survives), an expectation computed from the value it checks, a row that compares a thing with itself, or a check
   whose failure branch is unreachable.  Name the row and say what both versions of the code would produce.
2. **SELECTS-NOTHING** -- a regex, grep, awk range or parser that can match nothing and then reports success or zero
   (a count of 0 read as "no failures"; a missing section read as a pass; a padded-column pattern longer than its
   column).  Name the input on which it selects nothing.
3. **STATUS-LAUNDERED** -- a failure that surfaces as success: an exit status lost in a pipe or `|| true`, a timeout
   or killed run scored as complete (no completion sentinel checked), a skip scored as a pass, a build failure scored
   as a detection.
4. **ENCODING** -- a hand-assembled instruction word or register value whose fields do not encode what its comment
   says (a wrong register field typically yields 0, which rows expecting 0 accept by accident).  Decode it from the
   manual (`ls _scratchpad/*.txt` under the project root) and cite the line.
5. **RECORD** -- a docstring, comment or header whose claim about the code (a row count, what a row catches, a
   score) is false of the code at HEAD.  Line-number drift is NOT a finding.
6. **OTHER** -- a real defect of the harness that fits none of the above (a load-sensitive wall-clock oracle, a
   shared temporary path two gates both write, a probe no gate runs).

**The files** (lines = the fork's net addition since the import `39748e3c`):

| file | lines | rounds | before 2026-09-04 |
|---|---|---|---|
| `regress/diff_wdc_identify.c` | 5913 | 24 | 21 |

**Their rounds**, oldest first:

- `085766ac` 2026-08-14 #407: #405's detector had four holes and a note that was wrong the flattering way  [diff_wdc_identify.c]
- `2e709cdb` 2026-08-14 #405: ATA IDENTIFY packed its capacity bytes with `% 255`, not `& 255`  [diff_wdc_identify.c]
- `6ab49ad5` 2026-08-14 #410: the wdc detector is DONE, against a written condition instead of a feeling  [diff_wdc_identify.c]
- `ad5228bd` 2026-08-14 #411: #410's stopping condition could be satisfied to the letter while shipping a false pass  [diff_wdc_identify.c]
- `e86e293a` 2026-08-14 #408: the round that fixed stale citations made the identical error, and the detector was relying on -O2 to hide UB  [diff_wdc_identify.c]
- `f70db4bb` 2026-08-14 #409: #408's UB fix cost 148 seconds, and it poisoned one stub out of three  [diff_wdc_identify.c]
- `0922465f` 2026-08-27 #477 wdc ATAPI: a guest data-port WRITE could free the transfer being delivered  [diff_wdc_identify.c]
- `1cec2daf` 2026-08-27 #476 wdc: #475's clamp WOKE a NULL dereference -- two guest accesses killed the host  [diff_wdc_identify.c]
- `1f1a02bb` 2026-08-27 #473 wdc ATAPI DATAIN: bound the initial push, and stop reporting zero at the re-arm  [diff_wdc_identify.c]
- `23430365` 2026-08-27 #479 wdc: a new command did not reset what the old one left  [diff_wdc_identify.c]
- `3403c013` 2026-08-27 #482 wdc: the abort row could not say which state gated the abort  [diff_wdc_identify.c]
- `77b7c03a` 2026-08-27 #485 pass 2: the detector was below the floor TWICE, and the pass the round skipped found it  [diff_wdc_identify.c]
- `7d0b63d4` 2026-08-27 #480 wdc: the detector could not see its own call  [diff_wdc_identify.c]
- `832bed78` 2026-08-27 #478 wdc: an empty ring was read as a full sector, and 512 stale bytes went to the disk  [diff_wdc_identify.c]
- `867c697b` 2026-08-27 #481 wdc: the reset bit was the head-count bit  [diff_wdc_identify.c]
- `ce75b1d2` 2026-08-27 #483 wdc: the sweep pinned the decode across 256 values and the purge at none  [diff_wdc_identify.c]
- `cf300c07` 2026-08-27 #484 wdc: a full ring reported itself empty, and the next push destroyed a byte  [diff_wdc_identify.c]
- `d64a1fc3` 2026-08-27 #475 wdc ATAPI: clamp the byte count to what REMAINS; plus #474's pass-2 second wave  [diff_wdc_identify.c]
- `d8191881` 2026-08-27 #485 wdc: 242 of 256 opcodes ended a command and never raised its interrupt  [diff_wdc_identify.c]
- `d894e35d` 2026-08-27 #474 footbridge TIMER_x_CLEAR read-clears; plus #473's pass-2 corrections  [diff_wdc_identify.c]
- `6a5267c0` 2026-08-30 records: a reopening warrant that was retired before it was quoted, and three tools whose numbers were wrong  [diff_wdc_identify.c]
- `83df95c3` 2026-09-05 Retrospective re-check batch 3a (dev_wdc.c #337..#464): every fix holds; two guest-visible ATAPI defects filed MEDIUM, seven LOW rows, two merges, ...  [diff_wdc_identify.c]
- `db8b1a33` 2026-09-26 #553 latecodex: the codex seat re-fires #550, #551 and #549 promised landed after those commits -- adjudicated under the late-dissent rule, their c...  [diff_wdc_identify.c]
- `f5e155ac` 2026-09-26 #551 wdcidselfcheck: gate 2's wdc_identify self-check exemption discharged, not re-dated -- diff_wdc_identify.c gains a self-check on its two compa...  [diff_wdc_identify.c]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
