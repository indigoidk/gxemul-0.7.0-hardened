ASTRA RETRO-REVIEW (HARNESS) `hbundle_pipeline4` -- the GXemul fork's regression and pipeline code, 6 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_PIPELINE4_ALIVE` on its own line, then ONE verdict line:
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
| `tools/pipeline/check_optpin.py` | 123 | 1 | 1 |
| `tools/pipeline/codex_answer.py` | 121 | 2 | 0 |
| `tools/pipeline/census_floods.py` | 114 | 1 | 1 |
| `tools/pipeline/check_wsl_dollar.py` | 111 | 1 | 1 |
| `tools/pipeline/check_boilerplate.py` | 108 | 2 | 2 |
| `tools/pipeline/check_checkpoint.py` | 81 | 1 | 1 |

**Their rounds**, oldest first:

- `4f342a27` 2026-08-20 Records cluster panelled, and a seat broke the brief's letter to serve its purpose  [check_checkpoint.py]
- `9296fc6f` 2026-08-20 The ledger recorded seats as AGREEING when it only knew they were FIRED  [check_boilerplate.py]
- `c677764d` 2026-08-20 floodclass: two rows filed separately are one class, and the class is 72 files wide  [census_floods.py]
- `fd0ddefb` 2026-08-20 optrow: the audit is done, its answer is "one", and it is now mechanised because audits expire  [check_optpin.py]
- `6852e574` 2026-08-24 precommit X: a cited measurement must exist, and the gate that says so is tested  [check_boilerplate.py]
- `fb0cc783` 2026-08-29 #490 GD-ROM handle_command: two guest-reachable host kills, plus a wsl-dollar hook  [check_wsl_dollar.py]
- `b4d4177c` 2026-09-08 #515 lcaconfbus1kill: one variable meant two things, so a value the register's own guard ACCEPTS armed a host kill in a different handler  [codex_answer.py]
- `74daefdd` 2026-09-09 #516 lcairqstubkill: every ISA interrupt on alphabook1 routed into a function whose whole body was fatal()+exit(1)  [codex_answer.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
