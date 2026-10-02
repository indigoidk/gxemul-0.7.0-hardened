ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress29` -- the GXemul fork's regression and pipeline code, 6 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS29_ALIVE` on its own line, then ONE verdict line:
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
| `regress/wdc_altoffset_4bit_probe.py` | 240 | 2 | 2 |
| `regress/pcc2_width_witness.py` | 232 | 1 | 1 |
| `regress/gate_crossfamily.sh` | 231 | 11 | 11 |
| `regress/sh4_rtcsr_probe.py` | 225 | 1 | 1 |
| `regress/lca_confwidth_probe.py` | 223 | 2 | 0 |
| `regress/diff_autodev_gen.sh` | 222 | 1 | 1 |

**Their rounds**, oldest first:

- `2050c501` 2026-07-27 Round 55: a regression harness, and the retirement of two gates that could not fail  [gate_crossfamily.sh]
- `a21af04e` 2026-08-13 #399: four gate scripts did not know which gate they were, and a shipped record repeated one of them  [gate_crossfamily.sh]
- `b355dcdb` 2026-08-14 #406: a prose "DEVINIT" in a comment globbed the whole directory into autodev.c  [diff_autodev_gen.sh]
- `48b36b00` 2026-08-15 R3 follow-up: the round's own detector broke the round's own rule, and the offline gate was not offline  [gate_crossfamily.sh]
- `636c0239` 2026-08-15 #420 final panel: the verdict was safe but a row still stated a falsehood, and landisk's computed answer was never compared  [gate_crossfamily.sh]
- `7580e2f1` 2026-08-15 #420 adjudication: order the residuals, correct one overclaim, and record five gaps three rounds of harness work did not surface  [gate_crossfamily.sh]
- `a20ebc5a` 2026-08-15 R3 (#425, #426): the gate graded constants the run never used, and a green row said so  [gate_crossfamily.sh]
- `a4244db3` 2026-08-15 #420 pass 2b: gate 5's constants were unguardable from the gate, one layer further out than gate 7's  [gate_crossfamily.sh]
- `f5b2b60d` 2026-08-15 #420 pass 2c: an optional terminator recreated the wrong answer it was written to prevent, and a guard row passed while stating a falsehood  [gate_crossfamily.sh]
- `f92e5a1c` 2026-08-15 R1 (#422, #423): the harness could not be pointed anywhere else, and kept no wall time  [gate_crossfamily.sh]
- `fc86a934` 2026-08-15 #420: gate 5 had the same wall-clock defect as gate 7 and broke under load first -- and it is the instrument gate 7 uses to tell load from a regres...  [gate_crossfamily.sh]
- `f4374117` 2026-08-21 #449 sh4rtcsr: the host died nine milliseconds after the guest store, in a timer callback  [sh4_rtcsr_probe.py]
- `a4c86f11` 2026-08-26 act on three held-stage findings: an L4 comment, a refuted blocker, and a LATENT re-file  [gate_crossfamily.sh]
- `67120fd6` 2026-08-30 #495 wdc: a host store during an ATAPI DATA-IN transfer was pushed into the ring, and the guest read its own bytes back as disk data  [wdc_altoffset_4bit_probe.py]
- `c1254506` 2026-08-30 #494 wdc: the alt-ctrl handler never decoded its own offset, so a store to a read-only register aborted a live transfer  [wdc_altoffset_4bit_probe.py]
- `b78bb0f6` 2026-09-03 #500 pass 15 + pcc2widthkills: the closure that opened six registers is closed, and twelve width kills become a direction split  [pcc2_width_witness.py]
- `2956c7e8` 2026-09-07 #509 sgimtedepth4dead: `depth == 4' is unreachable, so tiled MTE always took CI  [lca_confwidth_probe.py]
- `7a41b3fb` 2026-09-07 #505 #506 #507 #508: four test-first rounds, three new rung-3 witnesses, and a witness row that could not fail  [lca_confwidth_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
