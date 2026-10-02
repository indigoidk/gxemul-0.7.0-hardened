ASTRA RETRO-REVIEW (HARNESS) `hsgideprimopprobe` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HSGIDEPRIMOPPROBE_ALIVE` on its own line, then ONE verdict line:
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
| `regress/sgi_de_primop_probe.py` | 1451 | 13 | 12 |

**Their rounds**, oldest first:

- `80cab9e3` 2026-09-01 #500 follow-up: the CLASS CLOSURE -- and a repair of mine that its own verification sweep falsified  [sgi_de_primop_probe.py]
- `840f3d0a` 2026-09-01 #500 sgideprimop: a drawing op a guest never chose, and the reset value was one  [sgi_de_primop_probe.py]
- `12754f9b` 2026-09-02 #500 pass 11: the adjudication found a RED GATE that shipped in nine commits, and a correct number this chain overwrote  [sgi_de_primop_probe.py]
- `3fb1f8f6` 2026-09-02 #500 pass 12: the panel MEASURED two clean sweeps my "no floor breach" pass had missed, and three seats found the red I left one line below the one...  [sgi_de_primop_probe.py]
- `41a4b1e4` 2026-09-02 #500 pass 9: I stopped asking for mutants and asked which symmetry was half-closed; two seats found two  [sgi_de_primop_probe.py]
- `559ebcf6` 2026-09-02 #500 pass 8: the accept side carried all 24 low bits since pass 4; the decline side carried none  [sgi_de_primop_probe.py]
- `55e4f539` 2026-09-02 #500 pass 7: the repair for "green for the wrong reason" was itself green for the wrong reason, twice  [sgi_de_primop_probe.py]
- `560fa6dc` 2026-09-02 #500 pass 6: two floor breaches, an empty corner of a two-by-two, and a record that did not match its own artifact  [sgi_de_primop_probe.py]
- `8b20eac1` 2026-09-02 #500 pass 5: the disposition I had ACCEPTED was wrong, and a seat overturned it by reading  [sgi_de_primop_probe.py]
- `f871245b` 2026-09-02 #500 pass 10: three defects, one shape -- the empty cell of a 2x2, on three different axes  [sgi_de_primop_probe.py]
- `b78bb0f6` 2026-09-03 #500 pass 15 + pcc2widthkills: the closure that opened six registers is closed, and twelve width kills become a direction split  [sgi_de_primop_probe.py]
- `f52c1579` 2026-09-03 #500 pass 14: the closing pass found a FAMILY of five zero registers, one session closed it, and the contract now states what rows cannot close  [sgi_de_primop_probe.py]
- `e5867e45` 2026-09-12 records: #524's pass-2 receipt and ledger commit, sgi_de_primop's pass-16 contract corrections, and the state of five in-flight rows after a codex ...  [sgi_de_primop_probe.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
