ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress18` -- the GXemul fork's regression and pipeline code, 3 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS18_ALIVE` on its own line, then ONE verdict line:
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
| `regress/asic_badaddr_probe.py` | 479 | 5 | 4 |
| `regress/sgi_re_rgb_probe.py` | 477 | 1 | 0 |
| `regress/diff_timer.c` | 473 | 4 | 4 |

**Their rounds**, oldest first:

- `863d2389` 2026-08-15 R4 (#427, #428, #429): the timer core clamped one end of a frequency and left the other unbounded  [diff_timer.c]
- `cdc48499` 2026-08-15 R4 follow-up: the round's detector certified six things it could not see  [diff_timer.c]
- `2134a984` 2026-08-16 #436: the detectors could all have stopped detecting, and nothing would have said so  [diff_timer.c]
- `abd7bad9` 2026-08-17 #436 pass 2: four defeats, and the worst was in the control I had just added  [diff_timer.c]
- `f1fa6a0a` 2026-08-25 #463 dreamcast_asic: one guest LOAD ended the host, at 64 byte addresses  [asic_badaddr_probe.py]
- `f4b8dbea` 2026-08-25 #463 pass 2, owed and refused by the gate: four wrong claims, and five more in the corrections  [asic_badaddr_probe.py]
- `d894e35d` 2026-08-27 #474 footbridge TIMER_x_CLEAR read-clears; plus #473's pass-2 corrections  [asic_badaddr_probe.py]
- `d9efd339` 2026-08-29 #492 the six battery reds -- and a detector that passed its own kill table with an L2 breach live in it  [asic_badaddr_probe.py]
- `79cd12e8` 2026-09-06 #502 pass 9-12 and #503: two fixes shipped, a filing overturned to a floor breach and repaired, and a detector's own contract predicting both of it...  [asic_badaddr_probe.py]
- `7a41b3fb` 2026-09-07 #505 #506 #507 #508: four test-first rounds, three new rung-3 witnesses, and a witness row that could not fail  [sgi_re_rgb_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
