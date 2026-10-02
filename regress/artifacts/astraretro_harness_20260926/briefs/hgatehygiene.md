ASTRA RETRO-REVIEW (HARNESS) `hgatehygiene` -- the GXemul fork's regression and pipeline code, 1 file(s), at HEAD db8b1a33

Open your answer with the token `ASTRARETRO_HGATEHYGIENE_ALIVE` on its own line, then ONE verdict line:
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
| `regress/gate_hygiene.sh` | 935 | 29 | 27 |

**Their rounds**, oldest first:

- `2050c501` 2026-07-27 Round 55: a regression harness, and the retirement of two gates that could not fail  [gate_hygiene.sh]
- `2b42203a` 2026-08-13 #392 pass-2b: half the fix shipped with no detector, and the truth table never tested the echo  [gate_hygiene.sh]
- `2bccdacd` 2026-08-13 #392 pass-2: the gate could not see a NEW whole-buffer site being added  [gate_hygiene.sh]
- `6ae75c14` 2026-08-13 Freeze the bare-prompt readiness sites: gate_hygiene gains its first source assertion  [gate_hygiene.sh]
- `6c74b31a` 2026-08-13 #392: the readiness predicate matched the same prompt twice  [gate_hygiene.sh]
- `a21af04e` 2026-08-13 #399: four gate scripts did not know which gate they were, and a shipped record repeated one of them  [gate_hygiene.sh]
- `a984c497` 2026-08-13 Harden the readiness ratchet: a check you can step around is not a check  [gate_hygiene.sh]
- `e8b4233f` 2026-08-13 #392 pass-2c: the pin proved token counts, not arms — and the fixed anchor still had a one-word evasion  [gate_hygiene.sh]
- `f1f6deec` 2026-08-16 A class ratchet from a seat answer nobody had read, and the gate it went red on  [gate_hygiene.sh]
- `6014b7e7` 2026-08-19 selfmutant6 CLOSED: the fifth control, and the first committed footbridge witness  [gate_hygiene.sh]
- `9976161a` 2026-08-19 gate_hygiene was LATENTLY RED at HEAD, and the probe that caused it shipped unwired  [gate_hygiene.sh]
- `020a672f` 2026-08-20 #439 the 8253 counter-latch: the driving seat REFUSED the panel's design and measured why  [gate_hygiene.sh]
- `3193d566` 2026-08-20 #442 fbpending: an overflowed counter stopped the emulated clock for 40 seconds  [gate_hygiene.sh]
- `9de16b79` 2026-08-20 #441 sh4bcr: two guest instructions ended the emulator process  [gate_hygiene.sh]
- `3f9ff561` 2026-08-21 #442 pass 2: the round shipped unreviewed, and five of twelve mutants passed both detectors  [gate_hygiene.sh]
- `6bec468c` 2026-08-21 #443 sh4pcicexit: one guest LOAD ended the host, on 116 of 137 offsets  [gate_hygiene.sh]
- `abf665c7` 2026-08-25 probetimebased: alive is True for a process already SIGKILLed -- measured, with a shipped instance  [gate_hygiene.sh]
- `cc27fdf0` 2026-08-27 gates: two readiness pins in gate_hygiene.sh were RED AT HEAD, and nobody had seen it  [gate_hygiene.sh]
- `d9efd339` 2026-08-29 #492 the six battery reds -- and a detector that passed its own kill table with an L2 breach live in it  [gate_hygiene.sh]
- `e3cf79fa` 2026-08-30 gate_hygiene: the class-ratchet census cited line numbers, three of five had drifted  [gate_hygiene.sh]
- `6b4eacf1` 2026-08-31 the weekly battery was going to red on two stale pins, and one of the four causes was mine  [gate_hygiene.sh]
- `9409a827` 2026-08-31 the weekly battery failed on Sunday and nobody looked; the next one would have failed too  [gate_hygiene.sh]
- `9f666a8d` 2026-08-31 #499 sgireunmapped: a 2080-byte door closed, with the order proof re-run locally  [gate_hygiene.sh]
- `840f3d0a` 2026-09-01 #500 sgideprimop: a drawing op a guest never chose, and the reset value was one  [gate_hygiene.sh]
- `12754f9b` 2026-09-02 #500 pass 11: the adjudication found a RED GATE that shipped in nine commits, and a correct number this chain overwrote  [gate_hygiene.sh]
- `3fb1f8f6` 2026-09-02 #500 pass 12: the panel MEASURED two clean sweeps my "no floor breach" pass had missed, and three seats found the red I left one line below the one...  [gate_hygiene.sh]
- `b78bb0f6` 2026-09-03 #500 pass 15 + pcc2widthkills: the closure that opened six registers is closed, and twelve width kills become a direction split  [gate_hygiene.sh]
- `3e33201d` 2026-09-24 #546 hygienecensus: gate 6's readiness census was 24 probes stale and RED at HEAD -- re-derived by a tool, never by hand, and the tool went through...  [gate_hygiene.sh]
- `8ea26abb` 2026-09-26 #549 fbctrlportkill: the test machines' framebuffer controller stored an out-of-range port selector and the next DATA access ended the emulator pro...  [gate_hygiene.sh]

**One block per finding:**
`F<n> | <path>:<line at HEAD> | <#NNN or sha> | CANNOT-FAIL / SELECTS-NOTHING / STATUS-LAUNDERED / ENCODING / RECORD /
OTHER | the concrete input or code state, and the wrong result it produces | the smallest check that would settle it |
confidence high/med/low`
If `OUTSTANDING_BUGS.md` at HEAD already files it, say so and give the id.

**Then the denominator.**  List what you checked and found sound, one line each with a line number at HEAD, and end
with `DENOMINATOR: read <h> of <H> files in full` -- "no finding" and "not looked at" must not look the same.

Read-only: write nothing, build nothing, run nothing that changes a file.
