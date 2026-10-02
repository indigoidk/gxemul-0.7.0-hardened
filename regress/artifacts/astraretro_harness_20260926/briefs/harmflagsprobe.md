ASTRA RETRO-REVIEW (HARNESS) `harmflagsprobe` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HARMFLAGSPROBE_ALIVE` on its own line, then ONE verdict line:
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
| `regress/arm_flags_probe.py` | 1698 | 13 | 13 |

**Their rounds**, oldest first:

- `a06e92fb` 2026-07-31 Round 71 (#311, #312, #313): ARM -- two wrong flags and one more halt  [arm_flags_probe.py]
- `0c1eb584` 2026-08-01 Round 78 addendum (#322) + round 84: the panel overturned one call and stopped another  [arm_flags_probe.py]
- `cbbe1ec0` 2026-08-01 Round 78 (#319, #320, #321): ARM rotations answered by halting -- and a carry read off the complement  [arm_flags_probe.py]
- `85bc4673` 2026-08-02 Round 90 (#329): the Thumb shift paths, where the flags came from a register the instruction never named  [arm_flags_probe.py]
- `d6f3d750` 2026-08-02 Round 77 (#328): three flag defects in the Thumb interpreter  [arm_flags_probe.py]
- `597a71b5` 2026-08-03 Round 83 (#340): folding a compare into a branch changed the flags  [arm_flags_probe.py]
- `4b031420` 2026-08-05 Round 93 (#342): the XOR-swap fold had no "two distinct registers" guard  [arm_flags_probe.py]
- `be6ea08a` 2026-08-05 Round 97 (#346): the cache-clean fold ignored the stride its own arithmetic assumed  [arm_flags_probe.py]
- `d143bd5b` 2026-08-05 Round 94 (#345): the cache-clean fold matched a loop's shape and ignored its registers  [arm_flags_probe.py]
- `dea2fefd` 2026-08-05 Round 98 (#347): the second cache-clean fold skipped a loop and updated nothing  [arm_flags_probe.py]
- `307b1b82` 2026-08-10 Round 100 (#351, #352, #353): the idle-loop fold skipped its writes, aliased a register, and hung the guest  [arm_flags_probe.py]
- `704036ef` 2026-08-10 Round 99 (#348, #349, #350): the cache-clean folds learned their exit flags  [arm_flags_probe.py]
- `f50da6b4` 2026-08-11 Round 109 (#363): the gate-14 flake -- the prompt predicate matched the guest's own output  [arm_flags_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
