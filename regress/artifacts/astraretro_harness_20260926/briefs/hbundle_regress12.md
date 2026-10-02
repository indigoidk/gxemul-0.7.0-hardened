ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress12` -- the GXemul fork's regression and pipeline code, 2 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS12_ALIVE` on its own line, then ONE verdict line:
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
| `regress/sh4_chcr_probe.py` | 601 | 5 | 5 |
| `regress/pcc2_c040_probe.py` | 597 | 3 | 0 |

**Their rounds**, oldest first:

- `a636a339` 2026-08-21 #448 sh4chcr: a LEGAL DMA configuration ended the host on its resource-select alone  [sh4_chcr_probe.py]
- `0f77c7a3` 2026-08-22 L4 accumulator row, the SH manual re-check, and four corrected overclaims  [sh4_chcr_probe.py]
- `759f7131` 2026-08-22 sh4_chcr: a two-character edit restored a host death at 18/18 -- add the L0 safety row  [sh4_chcr_probe.py]
- `f532bb6a` 2026-08-22 #453 sh4_dmac_transfer(): the last guest-reachable host death, and hardware accuracy meant NOT sending the interrupt  [sh4_chcr_probe.py]
- `2b40eb76` 2026-08-26 sh4dmacie regress review: the close STANDS, and my closure note undersold its own commit  [sh4_chcr_probe.py]
- `9fa07fe9` 2026-09-08 #512 pcc2c040kill: one legal guest byte store ended the host  [pcc2_c040_probe.py]
- `1f2b27ab` 2026-09-10 #512 follow-up (pcc2c040ctlq): the accept row the de-escalation clause owed was keyed on the fix's own retired text and could not fail -- measured ...  [pcc2_c040_probe.py]
- `bb8efbf0` 2026-09-18 #535 pcc2c040mienannounce: #512's detector missed the cell a real driver writes -- and ran in no gate at all  [pcc2_c040_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
