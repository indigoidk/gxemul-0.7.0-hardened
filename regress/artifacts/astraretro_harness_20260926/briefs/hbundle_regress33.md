ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress33` -- the GXemul fork's regression and pipeline code, 8 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS33_ALIVE` on its own line, then ONE verdict line:
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
| `regress/gate_upstream.sh` | 144 | 2 | 2 |
| `regress/run.sh` | 135 | 12 | 12 |
| `regress/diag_div_sweep.py` | 125 | 2 | 2 |
| `regress/arcbios_shift_probe.py` | 117 | 1 | 1 |
| `regress/census_tokens.py` | 115 | 1 | 0 |
| `regress/selftest_logdir.py` | 109 | 3 | 3 |
| `regress/gate_ppc_halt.sh` | 97 | 2 | 2 |
| `regress/gate_mips.sh` | 82 | 2 | 2 |

**Their rounds**, oldest first:

- `2050c501` 2026-07-27 Round 55: a regression harness, and the retirement of two gates that could not fail  [gate_mips.sh, run.sh]
- `218ab015` 2026-07-29 Add a check that every emulated machine still starts up cleanly  [run.sh]
- `db562cfb` 2026-07-29 Use plainer words in the docs and comments  [gate_upstream.sh]
- `f52c2fe3` 2026-07-29 Fix #296: SuperH read the FPU rounding-mode field but never used it  [run.sh]
- `ff572782` 2026-07-29 regress: gate 8 -- run upstream GXemul's own test suite, three-way  [gate_upstream.sh, run.sh]
- `4453ff2a` 2026-07-30 Fix #301: cvt.d.l converted the integer before the rounding mode existed  [run.sh]
- `85cc973a` 2026-07-30 Fix #298: m88k stored its rounding register, read it back, and used it nowhere  [run.sh]
- `37daeeef` 2026-07-31 Fix #304/#305: the PowerPC narrowed with a host cast, and threw away every NaN it touched  [run.sh]
- `a06e92fb` 2026-07-31 Round 71 (#311, #312, #313): ARM -- two wrong flags and one more halt  [run.sh]
- `37963fd9` 2026-08-01 Round 87 (#326): twenty-four legal PowerPC encodings stopped the emulator, and every floating-point record form was one of them  [gate_ppc_halt.sh, run.sh]
- `6f916cd5` 2026-08-05 Round 96 (#344): the negative multiply-adds were never decoded, and halted the emulator  [gate_ppc_halt.sh]
- `4ee174d5` 2026-08-12 #388: MIPS fold witness, phase B — probe 9/9, sub-arm mutant attribution, gate 16  [run.sh]
- `a21af04e` 2026-08-13 #399: four gate scripts did not know which gate they were, and a shipped record repeated one of them  [gate_mips.sh, run.sh]
- `ec51520a` 2026-08-13 Give the battery a manifest: it has sixteen gates, and three documents said otherwise  [run.sh]
- `521085b0` 2026-08-15 R3 follow-up 2: R3 decapitated gate 2's OTHER driver selftest, and both its rows stayed green  [selftest_logdir.py]
- `7cfa4667` 2026-08-15 R1 follow-up: the fix added a hazard, and its detector certified half of itself  [selftest_logdir.py]
- `f92e5a1c` 2026-08-15 R1 (#422, #423): the harness could not be pointed anywhere else, and kept no wall time  [selftest_logdir.py]
- `f1f6deec` 2026-08-16 A class ratchet from a seat answer nobody had read, and the gate it went red on  [diag_div_sweep.py]
- `f39b8984` 2026-08-21 #450 arcbiosubsan: ten uncast shifts, and the author had already cast four of them  [arcbios_shift_probe.py]
- `6a5267c0` 2026-08-30 records: a reopening warrant that was retired before it was quoted, and three tools whose numbers were wrong  [diag_div_sweep.py]
- `3e33201d` 2026-09-24 #546 hygienecensus: gate 6's readiness census was 24 probes stale and RED at HEAD -- re-derived by a tool, never by hand, and the tool went through...  [census_tokens.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
