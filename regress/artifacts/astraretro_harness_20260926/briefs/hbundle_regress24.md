ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress24` -- the GXemul fork's regression and pipeline code, 4 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS24_ALIVE` on its own line, then ONE verdict line:
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
| `regress/gate_ab.sh` | 339 | 7 | 7 |
| `regress/gate_build.sh` | 339 | 10 | 10 |
| `regress/mk48_nvram_probe.py` | 333 | 1 | 0 |
| `regress/lib.sh` | 331 | 9 | 9 |

**Their rounds**, oldest first:

- `2050c501` 2026-07-27 Round 55: a regression harness, and the retirement of two gates that could not fail  [gate_ab.sh, gate_build.sh, lib.sh]
- `8cbc2bb2` 2026-07-28 regress: gate 1's divergence and sync checks were passing on an empty list  [gate_build.sh]
- `db562cfb` 2026-07-29 Use plainer words in the docs and comments  [gate_build.sh]
- `fb4ec9d7` 2026-07-29 regress: gate 7 booted three builds against one writable disk image  [gate_ab.sh]
- `6ae421e9` 2026-08-11 Round 114 (#371): a gate that failed after a green section could report SKIP, hiding the failure  [lib.sh]
- `02ab388e` 2026-08-13 #397: a failed cd made gate 1 report PASS having built nothing  [gate_build.sh]
- `804d8c6e` 2026-08-13 #394: the divergence allowlist recorded which files may differ, never why  [gate_build.sh]
- `860efcb5` 2026-08-13 #398: the guard fired after the thing it was meant to prevent, and withdrawing by deletion was a DoS  [gate_build.sh]
- `a21af04e` 2026-08-13 #399: four gate scripts did not know which gate they were, and a shipped record repeated one of them  [gate_ab.sh]
- `dd288e5d` 2026-08-13 #395: gate 1 reported FAIL and published the arc binary four lines later  [gate_build.sh]
- `fe4038ed` 2026-08-13 #396: the #395 guard had the right quantity at the wrong time, and nine of my own claims were too strong  [gate_build.sh]
- `ca5e6d35` 2026-08-14 #415: #414 was applied to only one of the twin trees, and one allowlist entry hid a third of it  [gate_build.sh]
- `ec308139` 2026-08-14 #419: gate_ab could not tell a slow host from a broken build, and the obvious cure measured worse than the defect  [gate_ab.sh, lib.sh]
- `21ec7d81` 2026-08-15 #419 pass 3: the three measured constants had no coverage, and two live defects in what the round shipped  [gate_ab.sh, lib.sh]
- `3bd696ff` 2026-08-15 #419 pass 4: a crashed emulator was scored BACKSTOP, and a mean was quoted as a worst case  [gate_ab.sh, lib.sh]
- `521085b0` 2026-08-15 R3 follow-up 2: R3 decapitated gate 2's OTHER driver selftest, and both its rows stayed green  [lib.sh]
- `636c0239` 2026-08-15 #420 final panel: the verdict was safe but a row still stated a falsehood, and landisk's computed answer was never compared  [lib.sh]
- `a20ebc5a` 2026-08-15 R3 (#425, #426): the gate graded constants the run never used, and a green row said so  [lib.sh]
- `ce9c0bc5` 2026-08-15 #419 pass 2: the dropped-`-N` mutant survived the round that was built to catch it  [gate_ab.sh]
- `f92e5a1c` 2026-08-15 R1 (#422, #423): the harness could not be pointed anywhere else, and kept no wall time  [lib.sh]
- `867c697b` 2026-08-27 #481 wdc: the reset bit was the head-count bit  [gate_build.sh]
- `21e75609` 2026-09-10 #521 (mk48nvramkill): EIGHT ordinary NVRAM bytes inside a device's own mapped range ended the emulator -- the accept block's lower bound was one te...  [mk48_nvram_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
