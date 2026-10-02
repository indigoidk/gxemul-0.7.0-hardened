ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress32` -- the GXemul fork's regression and pipeline code, 8 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS32_ALIVE` on its own line, then ONE verdict line:
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
| `regress/gate_mips_rounding.sh` | 176 | 6 | 6 |
| `regress/selftest_mutation_295.sh` | 170 | 2 | 2 |
| `regress/m8820x_sites_probe.py` | 165 | 2 | 2 |
| `regress/sh4_val_witness.py` | 165 | 1 | 1 |
| `regress/sh4_tlbda2_witness.py` | 160 | 1 | 1 |
| `regress/gate_mips_folds.sh` | 153 | 3 | 2 |
| `regress/selftest_budget.py` | 151 | 2 | 2 |
| `regress/selftest_inactivity.py` | 145 | 1 | 1 |

**Their rounds**, oldest first:

- `4453ff2a` 2026-07-30 Fix #301: cvt.d.l converted the integer before the rounding mode existed  [gate_mips_rounding.sh]
- `e3d972c1` 2026-07-30 Fix #303: every subnormal decoded wrong, on every architecture at once  [gate_mips_rounding.sh]
- `622a90a7` 2026-07-31 regress: three round-70B rows could not fail  [gate_mips_rounding.sh]
- `638eff28` 2026-07-31 Fix #309/#310: two more decoders that stopped the machine on legal code  [gate_mips_rounding.sh]
- `4ee174d5` 2026-08-12 #388: MIPS fold witness, phase B — probe 9/9, sub-arm mutant attribution, gate 16  [gate_mips_folds.sh]
- `a3bb9191` 2026-08-12 Round 117 (#376): the #295 detector its reverting mutant demanded  [gate_mips_rounding.sh, selftest_mutation_295.sh]
- `bc42b2ad` 2026-08-12 Round 118 (#377): #376's pass-2 findings -- a wrong measured fact in three records, and a fourth mutant  [gate_mips_rounding.sh, selftest_mutation_295.sh]
- `f55a8e33` 2026-08-12 #388: pass-2 corrections — the bail-detector row, load-bearing value rows, gate fail-closed, records  [gate_mips_folds.sh]
- `48b36b00` 2026-08-15 R3 follow-up: the round's own detector broke the round's own rule, and the offline gate was not offline  [selftest_budget.py]
- `a20ebc5a` 2026-08-15 R3 (#425, #426): the gate graded constants the run never used, and a green row said so  [selftest_budget.py]
- `9494c6a3` 2026-08-16 m8online: the detector that proves a guest can actually reach the device  [m8820x_sites_probe.py]
- `f1f6deec` 2026-08-16 A class ratchet from a seat answer nobody had read, and the gate it went red on  [m8820x_sites_probe.py]
- `e841f443` 2026-08-21 #447 sh4valguards: one guest STORE ended the host, at four sites whose store positions differ  [sh4_val_witness.py]
- `927553fa` 2026-08-22 #452 sh4 TLB data array 2: decline the access instead of ending the host process  [sh4_tlbda2_witness.py]
- `29b450ce` 2026-08-26 #467 + #468: the pty deadline means SILENCE, and the ASIC domain is now ENFORCED  [selftest_inactivity.py]
- `8ea26abb` 2026-09-26 #549 fbctrlportkill: the test machines' framebuffer controller stored an out-of-range port selector and the next DATA access ended the emulator pro...  [gate_mips_folds.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
