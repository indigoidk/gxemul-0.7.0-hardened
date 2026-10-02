ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress19` -- the GXemul fork's regression and pipeline code, 3 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS19_ALIVE` on its own line, then ONE verdict line:
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
| `regress/diff_fbpending_bound.c` | 462 | 4 | 2 |
| `regress/wdc_altdigin_probe.py` | 461 | 1 | 0 |
| `regress/sh_intprio_probe.py` | 449 | 2 | 2 |

**Their rounds**, oldest first:

- `3193d566` 2026-08-20 #442 fbpending: an overflowed counter stopped the emulated clock for 40 seconds  [diff_fbpending_bound.c]
- `3f9ff561` 2026-08-21 #442 pass 2: the round shipped unreviewed, and five of twelve mutants passed both detectors  [diff_fbpending_bound.c]
- `8185920e` 2026-08-22 Track which seat was RIGHT, not just which seat answered  [sh_intprio_probe.py]
- `dc0c9d50` 2026-08-22 #455 an interrupt at priority 0 ended the host process  [sh_intprio_probe.py]
- `599a7a82` 2026-09-12 #525 (wdcaltdigin): the alt-status handler never decoded its offset ON THE READ SIDE, so a read of the Drive Address register returned the ALT-STAT...  [wdc_altdigin_probe.py]
- `cdbe7d75` 2026-09-18 #537 fbsmlane: #442's harness printed a verdict token its own self-mutant lane could never read -- the lane runs, pinned on R3  [diff_fbpending_bound.c]
- `f4f601c4` 2026-09-24 #548 fbdrainwire: #442's drain probe wired into gate 14 on all four timers before its exemption lapsed -- and three floor breaches of #442's own de...  [diff_fbpending_bound.c]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
