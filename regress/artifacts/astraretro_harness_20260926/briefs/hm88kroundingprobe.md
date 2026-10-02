ASTRA RETRO-REVIEW (HARNESS) `hm88kroundingprobe` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HM88KROUNDINGPROBE_ALIVE` on its own line, then ONE verdict line:
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
| `regress/m88k_rounding_probe.py` | 764 | 9 | 9 |

**Their rounds**, oldest first:

- `51899d78` 2026-07-30 Fix #299: the single-precision sum was rounded twice; round-to-odd makes the first rounding harmless  [m88k_rounding_probe.py]
- `85cc973a` 2026-07-30 Fix #298: m88k stored its rounding register, read it back, and used it nowhere  [m88k_rounding_probe.py]
- `96b86a92` 2026-07-30 Fix #302: the m88k truncations were raw C casts, and the third architecture has a third table  [m88k_rounding_probe.py]
- `e3d972c1` 2026-07-30 Fix #303: every subnormal decoded wrong, on every architecture at once  [m88k_rounding_probe.py]
- `e644a300` 2026-07-30 Fix #300: the D-format store has nothing to round, so the arithmetic learned to  [m88k_rounding_probe.py]
- `0fc81c5e` 2026-07-31 Fix #306/#307/#308: a family of legal m88k instructions that stopped the machine  [m88k_rounding_probe.py]
- `d12114d3` 2026-08-01 Round 76 (#323): bcnd rejected two thirds of its own condition masks  [m88k_rounding_probe.py]
- `064caaf6` 2026-08-02 Round 72 (#331-#334): there was no gradual underflow, and three architectures were relying on it  [m88k_rounding_probe.py]
- `6c74b31a` 2026-08-13 #392: the readiness predicate matched the same prompt twice  [m88k_rounding_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
