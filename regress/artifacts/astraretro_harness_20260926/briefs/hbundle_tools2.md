ASTRA RETRO-REVIEW (HARNESS) `hbundle_tools2` -- the GXemul fork's regression and pipeline code, 7 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_TOOLS2_ALIVE` on its own line, then ONE verdict line:
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
| `tools/adjudicate.sh` | 114 | 3 | 3 |
| `tools/propagate_all_trees.sh` | 105 | 1 | 1 |
| `tools/nightly_battery.sh` | 96 | 1 | 1 |
| `tools/FIRST-RUN-CHECK.sh` | 85 | 1 | 1 |
| `tools/install_hooks.sh` | 79 | 1 | 1 |
| `tools/cxlaunch.sh` | 59 | 1 | 0 |
| `tools/inline_diff.sh` | 42 | 1 | 1 |

**Their rounds**, oldest first:

- `581b8f36` 2026-08-17 The harness is now in git, and the migration broke one thing that caught itself  [FIRST-RUN-CHECK.sh, adjudicate.sh, nightly_battery.sh]
- `a9421817` 2026-08-20 The precommit gate was advisory, and I committed through a red one TWICE today  [install_hooks.sh]
- `673a7a7f` 2026-08-28 panel: migrate the glm seat to glm-5.3-flash:cloud, verified BEFORE the edit  [adjudicate.sh]
- `55ef9db5` 2026-08-29 roster, by owner directive: kimi returns to its CLI, glm-5.3-flash -> glm-5.3 -- and file the RED battery that sat unread for five days  [adjudicate.sh]
- `67120fd6` 2026-08-30 #495 wdc: a host store during an ATAPI DATA-IN transfer was pushed into the ring, and the guest read its own bytes back as disk data  [propagate_all_trees.sh]
- `0cb35605` 2026-08-31 tools/inline_diff.sh: refuse an empty diff instead of reporting it  [inline_diff.sh]
- `7a41b3fb` 2026-09-07 #505 #506 #507 #508: four test-first rounds, three new rung-3 witnesses, and a witness row that could not fail  [cxlaunch.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
