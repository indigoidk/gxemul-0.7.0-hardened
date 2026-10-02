ASTRA RETRO-REVIEW (HARNESS) `hbundle_pipeline1` -- the GXemul fork's regression and pipeline code, 3 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_PIPELINE1_ALIVE` on its own line, then ONE verdict line:
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
| `tools/pipeline/gen_dashboard.py` | 464 | 9 | 7 |
| `tools/pipeline/check_commit_attribution.py` | 422 | 9 | 5 |
| `tools/pipeline/check_cited_artifacts.py` | 382 | 3 | 3 |

**Their rounds**, oldest first:

- `581b8f36` 2026-08-17 The harness is now in git, and the migration broke one thing that caught itself  [gen_dashboard.py]
- `27dd47a0` 2026-08-19 rtcdet pass 3: the measure seat found the cheapest escape on record, and Fable found six wrong records  [check_commit_attribution.py]
- `7e3b1204` 2026-08-19 Fable adjudicates the witness ladder, closes gate3scope, and the SELFCHECK gap is gated  [gen_dashboard.py]
- `d89229e0` 2026-08-19 R4 detector (#429): the CHANGELOG round block, and the generator now names the file it writes  [gen_dashboard.py]
- `0d0283c9` 2026-08-20 The matrix is a generated file and nothing checked that it was regenerated  [gen_dashboard.py]
- `9296fc6f` 2026-08-20 The ledger recorded seats as AGREEING when it only knew they were FIRED  [check_commit_attribution.py, gen_dashboard.py]
- `a9421817` 2026-08-20 The precommit gate was advisory, and I committed through a red one TWICE today  [check_commit_attribution.py]
- `85bc6ab4` 2026-08-21 probewiring: four rounds of detectors that no gate has ever run  [gen_dashboard.py]
- `6852e574` 2026-08-24 precommit X: a cited measurement must exist, and the gate that says so is tested  [check_cited_artifacts.py]
- `86ea7c0e` 2026-08-24 asicbadaddr: two panels, five adjudicated rulings, and three defects the seats found in tools shipped hours earlier  [check_cited_artifacts.py]
- `e6c7e283` 2026-08-24 harness: a 402 wall read as a format miss, a gate that checked existence not tracked-ness, and two invisible ledger fields  [check_cited_artifacts.py, gen_dashboard.py]
- `f255ad90` 2026-08-26 panel.sh said "re-firing once" and re-fired nothing  [check_commit_attribution.py]
- `64868d24` 2026-08-31 #499's detector port caught three mutants the artifact detector let through  [check_commit_attribution.py]
- `70761347` 2026-09-05 pcc2widthkills passes 5-13 + the 2026-09-04 fix review: the fix approved block by block, the detector 190 -> 251 rows, pass 14 OWED (row stays open)  [check_commit_attribution.py]
- `bbfc942e` 2026-09-07 shiftubcensus: three verified members type-checked -- one guest-visible, one found on the line above; plus the stopword that unblocked it  [check_commit_attribution.py]
- `09ded75c` 2026-09-18 #534 stagetokens: four tools read one ledger field, each with its own copy of what it meant  [gen_dashboard.py]
- `686d179c` 2026-09-18 #531 ip30abortkill + #532 stagetokens: four guest-reachable abort() calls, and the gates that reddened because the record got more honest  [gen_dashboard.py]
- `3e33201d` 2026-09-24 #546 hygienecensus: gate 6's readiness census was 24 probes stale and RED at HEAD -- re-derived by a tool, never by hand, and the tool went through...  [check_commit_attribution.py]
- `bead6ad9` 2026-09-24 #547 upstreamdeleteprose: one word of a comment turns gate 8's delete row green at HEAD; attrabbrev: the rider's nine-seat review repairs a regress...  [check_commit_attribution.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
