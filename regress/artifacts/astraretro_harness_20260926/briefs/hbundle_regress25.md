ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress25` -- the GXemul fork's regression and pipeline code, 4 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS25_ALIVE` on its own line, then ONE verdict line:
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
| `regress/lca_widewrite_probe.py` | 328 | 2 | 0 |
| `regress/diff_diskimage_parse.c` | 324 | 3 | 3 |
| `regress/sh_rounding_probe.py` | 318 | 7 | 7 |
| `regress/ppc_halt_probe.py` | 314 | 3 | 3 |

**Their rounds**, oldest first:

- `f52c2fe3` 2026-07-29 Fix #296: SuperH read the FPU rounding-mode field but never used it  [sh_rounding_probe.py]
- `06445b53` 2026-07-30 Fix #297: ftrc converted with a raw C cast, so the guest's answer depended on the host  [sh_rounding_probe.py]
- `51899d78` 2026-07-30 Fix #299: the single-precision sum was rounded twice; round-to-odd makes the first rounding harmless  [sh_rounding_probe.py]
- `e3d972c1` 2026-07-30 Fix #303: every subnormal decoded wrong, on every architecture at once  [sh_rounding_probe.py]
- `e644a300` 2026-07-30 Fix #300: the D-format store has nothing to round, so the arithmetic learned to  [sh_rounding_probe.py]
- `37963fd9` 2026-08-01 Round 87 (#326): twenty-four legal PowerPC encodings stopped the emulator, and every floating-point record form was one of them  [ppc_halt_probe.py]
- `6f916cd5` 2026-08-05 Round 96 (#344): the negative multiply-adds were never decoded, and halted the emulator  [ppc_halt_probe.py]
- `6c74b31a` 2026-08-13 #392: the readiness predicate matched the same prompt twice  [ppc_halt_probe.py, sh_rounding_probe.py]
- `b460e3db` 2026-08-14 #418: the documented `d:` override did nothing, and the obvious place to fix it rounds the advertised capacity up  [diff_diskimage_parse.c]
- `7e3b1204` 2026-08-19 Fable adjudicates the witness ladder, closes gate3scope, and the SELFCHECK gap is gated  [diff_diskimage_parse.c]
- `eaff9a30` 2026-08-19 selfmutant6: two of five controls built, and the blocker was a MISSING VERDICT TOKEN  [diff_diskimage_parse.c]
- `0f77c7a3` 2026-08-22 L4 accumulator row, the SH manual re-check, and four corrected overclaims  [sh_rounding_probe.py]
- `8bd97e4d` 2026-09-18 #530 lcaisalane: a guest byte access to an ISA port 2 or 3 mod 4 ended the host -- shipped with the width row its own closing verdict owed  [lca_widewrite_probe.py]
- `a11eaac4` 2026-09-19 #538 lcalenzerodrop closes: #530's width row pinned one byte lane of four -- all four rowed, 17/17 as predicted, reproduced on the final instrument  [lca_widewrite_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
