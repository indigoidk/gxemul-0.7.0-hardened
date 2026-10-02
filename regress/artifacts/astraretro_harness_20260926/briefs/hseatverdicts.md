ASTRA RETRO-REVIEW (HARNESS) `hseatverdicts` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HSEATVERDICTS_ALIVE` on its own line, then ONE verdict line:
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
| `tools/pipeline/seat_verdicts.py` | 910 | 17 | 15 |

**Their rounds**, oldest first:

- `7af59ade` 2026-08-22 Three seats were DOWN and the tooling scored them "answered"  [seat_verdicts.py]
- `b3ad305a` 2026-08-22 #451 sh4_sci_cmd(): decline the command instead of ending the host process  [seat_verdicts.py]
- `d2c32fa3` 2026-08-22 SH re-check pass 2: the corrections were themselves overclaimed, twice  [seat_verdicts.py]
- `dc0c9d50` 2026-08-22 #455 an interrupt at priority 0 ended the host process  [seat_verdicts.py]
- `3ad72e04` 2026-08-23 harness: score-claims gate, verdict-extractor fix, floor clause (d), 2 filings  [seat_verdicts.py]
- `45d74886` 2026-08-23 A wall is a moment, not a state -- and panel.sh could not see this one  [seat_verdicts.py]
- `8eeeea21` 2026-08-23 verdict extractor: a measured regression in my own fix, and the guard that fixes it  [seat_verdicts.py]
- `ba30e64f` 2026-08-23 #461 both `default:` arms of the GD-ROM device ended the host process  [seat_verdicts.py]
- `e9f8c0cc` 2026-08-23 harness pass 2: two measured false passes fixed, verdict detector shipped  [seat_verdicts.py]
- `faffad7a` 2026-08-25 panel.sh fires the kimi substitute, and teaching the checkers about it found three unread reviews  [seat_verdicts.py]
- `733a4b65` 2026-08-26 #464 pass 2: one wrong record, one filed escape, and two seats the harness was losing  [seat_verdicts.py]
- `180afaa3` 2026-08-27 #470 verdictprose: a verdict QUOTED from another panel is no longer read as this seat's  [seat_verdicts.py]
- `1cec2daf` 2026-08-27 #476 wdc: #475's clamp WOKE a NULL dereference -- two guest accesses killed the host  [seat_verdicts.py]
- `cf300c07` 2026-08-27 #484 wdc: a full ring reported itself empty, and the next push destroyed a byte  [seat_verdicts.py]
- `d64a1fc3` 2026-08-27 #475 wdc ATAPI: clamp the byte count to what REMAINS; plus #474's pass-2 second wave  [seat_verdicts.py]
- `79cd12e8` 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of it...  [seat_verdicts.py]
- `257f56f1` 2026-09-07 #504 sgirandompixel: a failed pixel read handed the caller random() and the write stored it; plus the pass-2 receipt 79cd12e owed, and a measured f...  [seat_verdicts.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
