ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress22` -- the GXemul fork's regression and pipeline code, 3 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS22_ALIVE` on its own line, then ONE verdict line:
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
| `regress/selfmutant.py` | 414 | 5 | 4 |
| `regress/alpha_swpctx_v0_probe.py` | 411 | 6 | 0 |
| `regress/sh_iprbcd_probe.py` | 392 | 3 | 3 |

**Their rounds**, oldest first:

- `2134a984` 2026-08-16 #436: the detectors could all have stopped detecting, and nothing would have said so  [selfmutant.py]
- `abd7bad9` 2026-08-17 #436 pass 2: four defeats, and the worst was in the control I had just added  [selfmutant.py]
- `f8db56cc` 2026-08-17 A seat ran a gate and deadlocked, and its failure was the most useful of the pass  [selfmutant.py]
- `1a85e27c` 2026-08-19 selfmutant.py: an apparatus failure now says SETUP, and a seat found the escape that would have shipped a vacuous control  [selfmutant.py]
- `0bb8be2b` 2026-08-23 #459: one guest store to 0xffd80010 ended the host on 3 of 5 SH machines  [sh_iprbcd_probe.py]
- `7e5c0f6c` 2026-08-23 #458: SH-4 read two of four interrupt priority registers, and SCIF's came       from a register this machine never maps  [sh_iprbcd_probe.py]
- `e9f8c0cc` 2026-08-23 harness pass 2: two measured false passes fixed, verdict detector shipped  [sh_iprbcd_probe.py]
- `26945158` 2026-09-08 #514 pass 4: a coloured prompt makes a CORRECT build score 1/5, and the seat that found it also refuted an artifact I had just shipped  [alpha_swpctx_v0_probe.py]
- `2ab3d2f0` 2026-09-08 #514 pass 2: the product fix is ratified 6/6 and every other finding was in my detector or my records -- four repaired in-round, one claim withdraw...  [alpha_swpctx_v0_probe.py]
- `3031a306` 2026-09-08 #514 alphaswpctxreg: the context-switch primitive returned its result in the register the ABI tells the caller to discard -- one identifier, rung-3...  [alpha_swpctx_v0_probe.py]
- `bee05ce5` 2026-09-08 #514: the last two escapes pass 4 left open are closed by binding each observation to its STEP, and the repair is measured  [alpha_swpctx_v0_probe.py]
- `f4fecb7f` 2026-09-08 #514 pass 5: my binding repair LOST coverage the positional rule had, and the fix is to compose them rather than replace one with the other  [alpha_swpctx_v0_probe.py]
- `fa5e4e37` 2026-09-08 #514 pass 3: a seat measured two apparatus false passes, one of which I had introduced in the pass-2 repair -- and a duplicate-key guard caught me ...  [alpha_swpctx_v0_probe.py]
- `cdbe7d75` 2026-09-18 #537 fbsmlane: #442's harness printed a verdict token its own self-mutant lane could never read -- the lane runs, pinned on R3  [selfmutant.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
