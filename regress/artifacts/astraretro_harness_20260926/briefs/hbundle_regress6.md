ASTRA RETRO-REVIEW (HARNESS) `hbundle_regress6` -- the GXemul fork's regression and pipeline code, 2 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_REGRESS6_ALIVE` on its own line, then ONE verdict line:
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
| `regress/wdc_altoffset_probe.py` | 698 | 2 | 2 |
| `regress/arm_endian_probe.py` | 683 | 11 | 11 |

**Their rounds**, oldest first:

- `327b2a42` 2026-08-11 #373: correct #372's five-vs-six discriminator wording, and record the LDM/STM byte-order sibling  [arm_endian_probe.py]
- `5ae6c0e9` 2026-08-11 Round 115 (#372): the general-path word STORE ignored byte order, because its arm was dead code  [arm_endian_probe.py]
- `276fd0b2` 2026-08-12 Round 120 (#379): #378's pass-2 findings -- a false-green route and five record errors  [arm_endian_probe.py]
- `3757175a` 2026-08-12 #387: #386's pass-2 — the +2-offset detector, the kind pin, eight record precisions  [arm_endian_probe.py]
- `813ee67a` 2026-08-12 #386: swp — byte-order on both sides, rotate on the load, aligned word for both accesses  [arm_endian_probe.py]
- `e9230ad6` 2026-08-12 Round 119 (#378): a BE guest's LDM/STM through a warm page was byte-reversed  [arm_endian_probe.py]
- `03b8c1f1` 2026-08-13 #390 pass-2: the round's own refutation was wrong — LDRD's base WAS four bytes high, and #390 fixed it  [arm_endian_probe.py]
- `2e0675f7` 2026-08-13 #391: a control passed on evidence it never received  [arm_endian_probe.py]
- `7ade6819` 2026-08-13 #391 pass-2 (second correction): the records were wrong in BOTH directions, and a sibling control was fail-open  [arm_endian_probe.py]
- `8b1a7fdf` 2026-08-13 #390: one scratch word, two roles — a PC-relative store's base was four bytes high  [arm_endian_probe.py]
- `d6f860d2` 2026-08-13 #389: LDRD/STRD — two 32-bit words, not one 64-bit swap  [arm_endian_probe.py]
- `67120fd6` 2026-08-30 #495 wdc: a host store during an ATAPI DATA-IN transfer was pushed into the ring, and the guest read its own bytes back as disk data  [wdc_altoffset_probe.py]
- `c1254506` 2026-08-30 #494 wdc: the alt-ctrl handler never decoded its own offset, so a store to a read-only register aborted a live transfer  [wdc_altoffset_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
