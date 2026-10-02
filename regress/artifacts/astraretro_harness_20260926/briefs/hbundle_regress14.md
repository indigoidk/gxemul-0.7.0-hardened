ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress14` -- the GXemul fork's regression and pipeline code, 2 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS14_ALIVE` on its own line, then ONE verdict line:
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
| `regress/sgi_mte_fill_probe.py` | 547 | 2 | 0 |
| `regress/diff_sh4_tmu.c` | 545 | 6 | 6 |

**Their rounds**, oldest first:

- `28ac1f8b` 2026-08-13 #400: the SH-4 timer pinned itself at zero, and a booting guest's clock stopped  [diff_sh4_tmu.c]
- `7dde2b81` 2026-08-13 #401: the eleven rows never once exercised the modulo, which is the correction  [diff_sh4_tmu.c]
- `bd5b9104` 2026-08-14 #403: gcov said the interrupt line had never run, and fourteen wrong versions passed  [diff_sh4_tmu.c]
- `20ce22e9` 2026-08-19 sh4_tmu: pin the half of this harness's own claim that nothing asserted  [diff_sh4_tmu.c]
- `7e3b1204` 2026-08-19 Fable adjudicates the witness ladder, closes gate3scope, and the SELFCHECK gap is gated  [diff_sh4_tmu.c]
- `f4374117` 2026-08-21 #449 sh4rtcsr: the host died nine milliseconds after the guest store, in a timer callback  [diff_sh4_tmu.c]
- `2956c7e8` 2026-09-07 #509 sgimtedepth4dead: `depth == 4' is unreachable, so tiled MTE always took CI  [sgi_mte_fill_probe.py]
- `1ce82969` 2026-09-10 #509 follow-up (sgimtelabelcells): the detector was blind at two of three dispatch labels -- two rows close the floor breach 7g-1 found, measured 1...  [sgi_mte_fill_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
