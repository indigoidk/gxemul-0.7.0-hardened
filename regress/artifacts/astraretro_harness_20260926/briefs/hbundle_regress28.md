ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress28` -- the GXemul fork's regression and pipeline code, 5 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS28_ALIVE` on its own line, then ONE verdict line:
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
| `regress/wdc_altoffset_sig_probe.py` | 263 | 2 | 2 |
| `regress/sgi_re_randompixel_probe.py` | 258 | 1 | 0 |
| `regress/arm_memcpy_probe.py` | 254 | 3 | 3 |
| `regress/selftest_absorb.py` | 254 | 3 | 3 |
| `regress/pcc2_default_probe.py` | 249 | 2 | 0 |

**Their rounds**, oldest first:

- `7d3238f0` 2026-08-10 Round 101 (#354): the memcpy fold moved the bytes but never published the registers  [arm_memcpy_probe.py]
- `91f58cde` 2026-08-11 Round 105 (#359): a fold that copied half the bytes passed every check in the gate  [arm_memcpy_probe.py]
- `f50da6b4` 2026-08-11 Round 109 (#363): the gate-14 flake -- the prompt predicate matched the guest's own output  [arm_memcpy_probe.py]
- `4dc1ff8c` 2026-08-15 R2 follow-up: the census could delete the caller's directory, and the round overstated itself  [selftest_absorb.py]
- `81506bd8` 2026-08-15 R2 (#424): the parser selftest ran nowhere, and could not see a mutant that moves text  [selftest_absorb.py]
- `d8399c31` 2026-08-15 r421: the gate can only see the driver's OUTPUT, so the parser gets a pure-function selftest that calls the shipped code  [selftest_absorb.py]
- `67120fd6` 2026-08-30 #495 wdc: a host store during an ATAPI DATA-IN transfer was pushed into the ring, and the guest read its own bytes back as disk data  [wdc_altoffset_sig_probe.py]
- `c1254506` 2026-08-30 #494 wdc: the alt-ctrl handler never decoded its own offset, so a store to a read-only register aborted a live transfer  [wdc_altoffset_sig_probe.py]
- `99b92f96` 2026-09-05 #501 regress review (fable-only) recorded: the 46-row instrument reds on a regression today, measured; three records refinements  [pcc2_default_probe.py]
- `ecc4d3be` 2026-09-05 #501 pcc2defaultkill: the default: arm of DEVICE_ACCESS(pcc2) no longer ends the host; reads keep the served byte, writes are declined, one latched...  [pcc2_default_probe.py]
- `257f56f1` 2026-09-07 #504 sgirandompixel: a failed pixel read handed the caller random() and the write stored it; plus the pass-2 receipt 79cd12e owed, and a measured f...  [sgi_re_randompixel_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
