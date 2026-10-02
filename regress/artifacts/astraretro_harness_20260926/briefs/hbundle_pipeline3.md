ASTRA RETRO-REVIEW (HARNESS) `hbundle_pipeline3` -- the GXemul fork's regression and pipeline code, 8 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HBUNDLE_PIPELINE3_ALIVE` on its own line, then ONE verdict line:
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
| `tools/pipeline/check_witness.py` | 213 | 3 | 3 |
| `tools/pipeline/check_seats_read.py` | 208 | 2 | 2 |
| `tools/pipeline/check_fable_queue.py` | 182 | 5 | 2 |
| `tools/pipeline/check_hook_controls.py` | 171 | 1 | 1 |
| `tools/pipeline/exit_census.py` | 167 | 3 | 3 |
| `tools/pipeline/seat_scorecard.py` | 135 | 2 | 2 |
| `tools/pipeline/check_bugfile_sync.py` | 129 | 2 | 2 |
| `tools/pipeline/check_seat_coverage.py` | 127 | 1 | 1 |

**Their rounds**, oldest first:

- `581b8f36` 2026-08-17 The harness is now in git, and the migration broke one thing that caught itself  [check_seats_read.py]
- `c3d13e57` 2026-08-17 harness: gate the flagship seat's OWED work, not just its missing work  [check_fable_queue.py]
- `9bcae1c2` 2026-08-18 pipeline: answer "is deepseek missing?" with a tool instead of a fifth audit  [check_seat_coverage.py]
- `aa10c9f1` 2026-08-19 witness field: enforce the ladder's own rule, and its first run found a gap in the ladder  [check_witness.py]
- `b16a0eee` 2026-08-20 A row that exists only in the ledger is work a fresh session will not see  [check_bugfile_sync.py]
- `c2cf7bc9` 2026-08-21 The queue gate matched ids by substring, so it was green over the one thing it exists to catch  [check_fable_queue.py]
- `8185920e` 2026-08-22 Track which seat was RIGHT, not just which seat answered  [seat_scorecard.py]
- `9d5fd693` 2026-08-22 #456 the SH test machine could not deliver an interrupt at all  [seat_scorecard.py]
- `faffad7a` 2026-08-25 panel.sh fires the kimi substitute, and teaching the checkers about it found three unread reviews  [check_seats_read.py]
- `baacf9bb` 2026-08-26 #464 wdc: six unlatched fatal() bounded, and the detector's first gate  [check_bugfile_sync.py]
- `7052c3bd` 2026-08-27 ladder: adopt `detector:<path>` as a sixth witness term -- OWNER DECISION, with a bound  [check_witness.py]
- `c8a483f5` 2026-08-27 gdromexitsix pass 1: FOUR false premises, a witness field citing artifacts that do not exist, and a new existence check that failed its own negativ...  [check_witness.py]
- `18893de6` 2026-08-29 #491 diskimage: two -Wsign-compare warnings were costing an entire GATE  [check_hook_controls.py]
- `7262ee3c` 2026-08-30 exit_census: ship the DERIVER, because a fourth number would have been the defect  [exit_census.py]
- `b1661fe8` 2026-08-30 exit_census: classify by enclosing construct -- 99 of 174 sit on a guest access path  [exit_census.py]
- `c0a86689` 2026-08-30 exit_census: a plain non-static function was not a construct boundary, inflating the reachability bucket 97 -> 83  [exit_census.py]
- `7d7e0559` 2026-09-10 records+evidence: the night's three rounds land their measurements while TWO STAY HELD -- #518 on three mutants that still escape its own 67-row in...  [check_fable_queue.py]
- `09ded75c` 2026-09-18 #534 stagetokens: four tools read one ledger field, each with its own copy of what it meant  [check_fable_queue.py]
- `686d179c` 2026-09-18 #531 ip30abortkill + #532 stagetokens: four guest-reachable abort() calls, and the gates that reddened because the record got more honest  [check_fable_queue.py]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
