ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress26` -- the GXemul fork's regression and pipeline code, 5 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS26_ALIVE` on its own line, then ONE verdict line:
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
| `regress/sh4_sci_probe.py` | 311 | 1 | 1 |
| `regress/arm_strlen_probe.py` | 302 | 2 | 2 |
| `regress/diff_rtc_range.c` | 290 | 4 | 4 |
| `regress/arm_bfx_width_probe.py` | 288 | 3 | 0 |
| `regress/sh4_tlbda2_probe.py` | 284 | 1 | 1 |

**Their rounds**, oldest first:

- `38537dee` 2026-08-11 Round 102 (#355, #356): the strlen fold answered a question the architecture never asked, and never came up for air  [arm_strlen_probe.py]
- `f50da6b4` 2026-08-11 Round 109 (#363): the gate-14 flake -- the prompt predicate matched the guest's own output  [arm_strlen_probe.py]
- `17de78a0` 2026-08-19 regress: a detector for #429's RTC range check (gate 2: 245 -> 254 checks)  [diff_rtc_range.c]
- `27dd47a0` 2026-08-19 rtcdet pass 3: the measure seat found the cheapest escape on record, and Fable found six wrong records  [diff_rtc_range.c]
- `cd32ed2a` 2026-08-19 rtcdet pass 2: the panel found a real escape, and two of its three claims did not survive  [diff_rtc_range.c]
- `af40df5a` 2026-08-20 Five seats voted to drop constblind as "already fixed" -- and the live instance was mine, from hours earlier  [diff_rtc_range.c]
- `927553fa` 2026-08-22 #452 sh4 TLB data array 2: decline the access instead of ending the host process  [sh4_tlbda2_probe.py]
- `b3ad305a` 2026-08-22 #451 sh4_sci_cmd(): decline the command instead of ending the host process  [sh4_sci_probe.py]
- `01a0339a` 2026-09-07 #510 follow-up: the two SBFX cells codex named, and a false claim in c0c7f55's own message  [arm_bfx_width_probe.py]
- `c0c7f55d` 2026-09-07 #510 armbfxwidth32: UBFX and SBFX built their mask with an undefined shift  [arm_bfx_width_probe.py]
- `eb839923` 2026-09-07 #510 pass 2: the panel was right and I refuted it, plus a broken comment I shipped in 01a0339  [arm_bfx_width_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
