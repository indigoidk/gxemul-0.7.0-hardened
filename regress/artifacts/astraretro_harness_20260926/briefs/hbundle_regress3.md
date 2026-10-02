ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress3` -- the GXemul fork's regression and pipeline code, 2 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS3_ALIVE` on its own line, then ONE verdict line:
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
| `regress/arm_writeback_probe.py` | 725 | 10 | 10 |
| `regress/arm_fold_marker_probe.py` | 720 | 9 | 9 |

**Their rounds**, oldest first:

- `0aceec24` 2026-08-11 #366: correct a detail #365 shipped wrong -- one general-path entry per cold fold arm, not six  [arm_writeback_probe.py]
- `1751ae27` 2026-08-11 Round 108 (#362): unaligned word loads returned the aligned word, unrotated  [arm_writeback_probe.py]
- `221328df` 2026-08-11 Round 104 (#358): five folds were doing work no test could see, and #357 removed the only witness  [arm_fold_marker_probe.py]
- `2c615c3c` 2026-08-11 Round 112 (#367): path attribution stops being a comment and becomes a checked quantity  [arm_writeback_probe.py]
- `396c3f8a` 2026-08-11 Round 106 (#360): the row that asserted an absence still passed when the fold was dead  [arm_fold_marker_probe.py]
- `42bd6822` 2026-08-11 Round 113 (#368): the copyin fold's rotation shipped unreachable, and its row is a cross-path XOR  [arm_fold_marker_probe.py]
- `5b225bc3` 2026-08-11 Round 107 (#361): the last two folds with markers but no rows, and a negative arm that was vacuous alone  [arm_fold_marker_probe.py]
- `a280ee92` 2026-08-11 Round 111 (#365): "unreached" was wrong -- the sites were reached and nothing DISCRIMINATED the fix  [arm_writeback_probe.py]
- `aed12e44` 2026-08-11 Round 103 (#357): the load/store template masked the base writeback, so a post-index loop could not advance  [arm_writeback_probe.py]
- `d1752fa3` 2026-08-11 #370: correct three claims in #368's record after the second review pass caught them  [arm_fold_marker_probe.py]
- `d7bbebba` 2026-08-11 #369: correct #368's xchg-decline mechanism, and record why a one-register XOR suffices  [arm_fold_marker_probe.py]
- `e89e3db2` 2026-08-11 Round 110 (#364): the row-to-site table was inverted, so two shipped rotations were never measured  [arm_writeback_probe.py]
- `f50da6b4` 2026-08-11 Round 109 (#363): the gate-14 flake -- the prompt predicate matched the guest's own output  [arm_fold_marker_probe.py, arm_writeback_probe.py]
- `5f60d0d0` 2026-08-12 Round 124 (#384): #382/#383's pass-2 findings -- a tag split, a copyout coverage gap, records  [arm_fold_marker_probe.py]
- `c113e677` 2026-08-12 Round 123 (#382): the copyin/copyout folds moved byte-reversed words on a BE guest  [arm_fold_marker_probe.py]
- `e55961f0` 2026-08-12 #385: records re-audit — no committed expectation was wrong, six records were  [arm_writeback_probe.py]
- `495a07a6` 2026-08-13 #389 pass-2: eleven records corrections, and two mutant gaps the battery could not see  [arm_writeback_probe.py]
- `d6f860d2` 2026-08-13 #389: LDRD/STRD — two 32-bit words, not one 64-bit swap  [arm_writeback_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
