ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress11` -- the GXemul fork's regression and pipeline code, 2 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS11_ALIVE` on its own line, then ONE verdict line:
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
| `regress/drive_guest.py` | 623 | 16 | 16 |
| `regress/sgi_re_width_probe.py` | 601 | 5 | 4 |

**Their rounds**, oldest first:

- `2050c501` 2026-07-27 Round 55: a regression harness, and the retirement of two gates that could not fail  [drive_guest.py]
- `3ab1a406` 2026-07-29 Fix #293: typed input on SuperH was stolen before the serial port saw it  [drive_guest.py]
- `fb4ec9d7` 2026-07-29 regress: gate 7 booted three builds against one writable disk image  [drive_guest.py]
- `2cadd41d` 2026-08-15 #420 pass 2: the round reintroduced a race #419 had already fixed, because the corrected version is the one that looks safe to copy  [drive_guest.py]
- `48b36b00` 2026-08-15 R3 follow-up: the round's own detector broke the round's own rule, and the offline gate was not offline  [drive_guest.py]
- `636c0239` 2026-08-15 #420 final panel: the verdict was safe but a row still stated a falsehood, and landisk's computed answer was never compared  [drive_guest.py]
- `7580e2f1` 2026-08-15 #420 adjudication: order the residuals, correct one overclaim, and record five gaps three rounds of harness work did not surface  [drive_guest.py]
- `7cfa4667` 2026-08-15 R1 follow-up: the fix added a hazard, and its detector certified half of itself  [drive_guest.py]
- `a20ebc5a` 2026-08-15 R3 (#425, #426): the gate graded constants the run never used, and a green row said so  [drive_guest.py]
- `a4244db3` 2026-08-15 #420 pass 2b: gate 5's constants were unguardable from the gate, one layer further out than gate 7's  [drive_guest.py]
- `d8399c31` 2026-08-15 r421: the gate can only see the driver's OUTPUT, so the parser gets a pure-function selftest that calls the shipped code  [drive_guest.py]
- `f5b2b60d` 2026-08-15 #420 pass 2c: an optional terminator recreated the wrong answer it was written to prevent, and a guard row passed while stating a falsehood  [drive_guest.py]
- `f92e5a1c` 2026-08-15 R1 (#422, #423): the harness could not be pointed anywhere else, and kept no wall time  [drive_guest.py]
- `fc86a934` 2026-08-15 #420: gate 5 had the same wall-clock defect as gate 7 and broke under load first -- and it is the instrument gate 7 uses to tell load from a regres...  [drive_guest.py]
- `840de826` 2026-08-16 Three failures rendered as one blank cell, and a gate so the third cannot recur  [drive_guest.py]
- `b744299f` 2026-08-25 landiskdisk: the landisk rig now attaches a disk, and dev_wdc.c stops being untested  [drive_guest.py]
- `112867a6` 2026-08-30 #497 closes: the round's record, plus a live defect in panel.sh that was mine  [sgi_re_width_probe.py]
- `3c8eb3a9` 2026-08-30 #497b: the panel found eight defects in my records commit, and one was a regression it shipped  [sgi_re_width_probe.py]
- `e363582a` 2026-08-30 #497 pass 2: the detector ships, and the panel found a MEASURED escape plus two gate defects of mine  [sgi_re_width_probe.py]
- `9f666a8d` 2026-08-31 #499 sgireunmapped: a 2080-byte door closed, with the order proof re-run locally  [sgi_re_width_probe.py]
- `e302c98c` 2026-09-08 #513 sgirekills: six host kills removed from dev_sgi_re read arms, and the detector that shipped with them survived four adversarial passes  [sgi_re_width_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
