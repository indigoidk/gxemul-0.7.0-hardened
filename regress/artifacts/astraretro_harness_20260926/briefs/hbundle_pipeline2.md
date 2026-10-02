ASTRA RETRO-REVIEW (HARNESS) `hbundle_pipeline2` -- the GXemul fork's regression and pipeline code, 6 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_PIPELINE2_ALIVE` on its own line, then ONE verdict line:
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
| `tools/pipeline/check_stage_panels.py` | 303 | 6 | 4 |
| `tools/pipeline/census_exits.py` | 245 | 1 | 1 |
| `tools/pipeline/stage_tokens.py` | 243 | 1 | 0 |
| `tools/pipeline/check_row_states.py` | 223 | 3 | 3 |
| `tools/pipeline/gen_codex_wall.py` | 223 | 6 | 5 |
| `tools/pipeline/check_score_claims.py` | 221 | 4 | 4 |

**Their rounds**, oldest first:

- `188d0764` 2026-08-17 census_exits.py: ship the inventory as an instrument, not a number  [census_exits.py]
- `581b8f36` 2026-08-17 The harness is now in git, and the migration broke one thing that caught itself  [check_stage_panels.py]
- `8b5fc437` 2026-08-17 exitsweep assess: 7 seats answered, and the measure seat overturned the brief  [check_stage_panels.py]
- `01bb94ce` 2026-08-20 Codex wall DISCHARGED -- and removing it revealed a shortfall it had been masking  [gen_codex_wall.py]
- `b584682f` 2026-08-20 m88k cluster panelled, and the queue's held-stage list is now DERIVED after it drifted  [gen_codex_wall.py]
- `c2cf7bc9` 2026-08-21 The queue gate matched ids by substring, so it was green over the one thing it exists to catch  [check_stage_panels.py]
- `3ad72e04` 2026-08-23 harness: score-claims gate, verdict-extractor fix, floor clause (d), 2 filings  [check_score_claims.py]
- `6bfbb9f8` 2026-08-23 precommit W: the queue file must not advertise shipped work (six were)  [check_row_states.py]
- `740213a2` 2026-08-23 precommit W: a ledger row's state must agree with what shipped  [check_row_states.py]
- `8eeeea21` 2026-08-23 verdict extractor: a measured regression in my own fix, and the guard that fixes it  [check_score_claims.py]
- `ba30e64f` 2026-08-23 #461 both `default:` arms of the GD-ROM device ended the host process  [check_row_states.py]
- `e9f8c0cc` 2026-08-23 harness pass 2: two measured false passes fixed, verdict detector shipped  [check_score_claims.py]
- `733a4b65` 2026-08-26 #464 pass 2: one wrong record, one filed escape, and two seats the harness was losing  [check_stage_panels.py]
- `df0dfccb` 2026-08-26 scoreclaimhex FIXED: one character, and the coverage check that had to come with it  [check_score_claims.py]
- `fb0cc783` 2026-08-29 #490 GD-ROM handle_command: two guest-reachable host kills, plus a wsl-dollar hook  [gen_codex_wall.py]
- `3c8eb3a9` 2026-08-30 #497b: the panel found eight defects in my records commit, and one was a regression it shipped  [gen_codex_wall.py]
- `9abd1757` 2026-08-30 holdmarkermulti: adopt the kimi seat's DURABLE close -- validate seat ids, not the regex  [gen_codex_wall.py]
- `09ded75c` 2026-09-18 #534 stagetokens: four tools read one ledger field, each with its own copy of what it meant  [check_stage_panels.py, gen_codex_wall.py, stage_tokens.py]
- `686d179c` 2026-09-18 #531 ip30abortkill + #532 stagetokens: four guest-reachable abort() calls, and the gates that reddened because the record got more honest  [check_stage_panels.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
