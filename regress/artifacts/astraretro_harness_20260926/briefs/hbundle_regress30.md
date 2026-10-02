ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress30` -- the GXemul fork's regression and pipeline code, 7 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS30_ALIVE` on its own line, then ONE verdict line:
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
| `regress/absorb_census.py` | 219 | 3 | 3 |
| `regress/sgi_eaddr_probe.py` | 213 | 2 | 2 |
| `regress/sh4_chcr_witness.py` | 208 | 1 | 1 |
| `regress/sh4_sci_witness.py` | 205 | 1 | 1 |
| `regress/m88k_idle_probe.py` | 204 | 1 | 1 |
| `regress/wdc_latch_census.py` | 200 | 1 | 1 |
| `regress/mips_rounding_probe.py` | 195 | 2 | 2 |

**Their rounds**, oldest first:

- `4453ff2a` 2026-07-30 Fix #301: cvt.d.l converted the integer before the rounding mode existed  [mips_rounding_probe.py]
- `ed242c0d` 2026-08-12 Round 121 (#380): the m88k idle fold ran the bcnd.n delay slot zero times  [m88k_idle_probe.py]
- `6c74b31a` 2026-08-13 #392: the readiness predicate matched the same prompt twice  [mips_rounding_probe.py]
- `4dc1ff8c` 2026-08-15 R2 follow-up: the census could delete the caller's directory, and the round overstated itself  [absorb_census.py]
- `81506bd8` 2026-08-15 R2 (#424): the parser selftest ran nowhere, and could not see a mutant that moves text  [absorb_census.py]
- `c0003e18` 2026-08-15 R2: the census now cleans up even when interrupted (regression-review residue finding)  [absorb_census.py]
- `6b6d5965` 2026-08-21 #446 pass 2: sixteen mutants, sixteen passed -- and a comment-only file passed too  [sgi_eaddr_probe.py]
- `a636a339` 2026-08-21 #448 sh4chcr: a LEGAL DMA configuration ended the host on its resource-select alone  [sh4_chcr_witness.py]
- `bcdbfb88` 2026-08-21 #446 sgiarcbiosoob: a heap overflow no harness had run, and not where ASan pointed  [sgi_eaddr_probe.py]
- `b3ad305a` 2026-08-22 #451 sh4_sci_cmd(): decline the command instead of ending the host process  [sh4_sci_witness.py]
- `d9efd339` 2026-08-29 #492 the six battery reds -- and a detector that passed its own kill table with an L2 breach live in it  [wdc_latch_census.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
