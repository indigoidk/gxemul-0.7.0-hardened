# `#548` fbdrainwire -- PASS 1, the FLAGSHIP seat (you fire LAST, after all eight other seats and the measuring seat)

Open with the line `FABLE548_ALIVE`, then the FIRST LINE of `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\CHECKPOINT.md`
verbatim, then `VERDICT: <PROCEED | PROCEED WITH CHANGES | DO NOT PROCEED>` and numbered findings.

The tree under review is `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\` (ignore any other `src/`).  READ-ONLY: do not edit any
file under GXEMUL-SEC; measure only in a scratch copy under `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\fable548\` if you
measure at all.  Please do not simply ratify -- a recent panel had seven of nine seats confirm a premise stated wrongly.
**The load-bearing question is at the end: WHICH OF MY DISPOSITIONS IS WRONG.**

## What the round is

`regress/fbpending_drain_probe.py` is `#442`'s rung-3 detector for the footbridge pending-tick bound
(`src/devices/dev_footbridge.c`, `footbridge_pending()` and the bound block in `reload_timer_value()`).  It runs in no
gate; its `EXEMPT` entry in `tools/pipeline/check_probe_wiring.py` lapses 2026-09-27 and every commit's precommit
section R reds from 2026-09-28.  The pass-1 brief proposed wiring it into gate 14 (`regress/gate_arm.sh`, beside
`footbridge_sites_probe.py`) with `--expect-cap 762` and three rows, deleting the exemption in the same edit.

Evidence, all under `GXEMUL-SEC/regress/artifacts/fbdrainwire_20260924/`:
* `p1_brief.md` -- the brief the eight scriptable seats answered;
* `panels/panel_20260924_030347/` -- codex (GPT-6 Astra), agy, grok 4.7, glm, minimax, the kimi seat through
  `kimi-k3:cloud` (the kimi CLI is on its weekly limit: `kimi.txt`), deepseek (answered on its THIRD try; the first
  two were HTTP 500, kept as `ollama_deepseek.try{1,2}_http500.txt`);
* `panels/codex_dedicated_p1.txt` -- the dedicated adversarial codex job;
* `opus5_p1.md` -- the Opus measuring seat (built HEAD bead6ad9 and nine mutants in a scratch clone and ran every one);
* `opus5_p1b.md` -- its follow-up on the `==` mutant (SEE F3 BELOW);
* `p1_draft.diff` -- EVERY drafted edit against HEAD, 9 hunks in 6 files, not yet applied to the tree.  Read the
  hunks, not my summaries of them: the sketch rule says a proposed edit is a sketch until run against its context.
Opus's raw logs are in `C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\opus548\out\` (`results_table.txt`, `runs/`).

## SETTLED PREMISES (measured or read this session; cite them, do not re-derive unless you doubt one)

* The bound at the probe's rate: 50e6 / (256*256) = 762.939453125 Hz exactly; `(int)` gives 762; neither clamp
  engages.  After the fix the counter ranges over [1, 762], so 762 is the tightest cap that cannot false-fail.
* The drained count is ((N-1) mod B) + 1 for N delivered ticks and bound B.  N = 3051 at 4 s on an idle host (Opus: the
  count follows the SIGALRM clock, not the harness's 4.02 s).
* HEAD passes on all four timers (D = X = 3); a bound-removed mutant fails on all four (3051).
* `fbpending_drain_probe.py` has `--timer N` (TIMER_1_* is index 0); its docstring usage line omits it and names the
  file `fbpending_drain.py` (read).
* `regress/diff_fbpending_bound.c` (gate 2) drives the counter through the real `timer_tickN()` callbacks for all four
  timers (R1/R5 loop over `nr`), but EVERY arm it makes is TIMER_ENABLE'd, and R6 re-arms timer 0 from 50 MHz to
  762 Hz with ZERO ticks owed (read).
* With the ceiling deleted, gate 2's R2 prints `ok R2 no signed overflow ... peak 2147483647 trough 1` (Opus,
  measured): the compare precedes the `++`, so an INT_MAX bound resets rather than wrapping.

## THE CONVERGED FINDINGS AND MY DISPOSITIONS

F1 (every seat) -- **the contract sentence "the rows catch any RAISE above 762" is FALSE.**  A raise to B < N wraps:
`freq * 2` (B = 1525) reads 1 and passes (Opus, measured).  DISPOSITION: restate the contract -- the rows catch
REMOVAL, a bound gated on a control bit arm X's CTRL=0 write clears, and a raise past N; everything about the bound's
VALUE is gate 2's.

F2 (codex x2, grok, glm, kimi-sub, deepseek, minimax; Opus measured) -- **one timer or four.**  Opus built
`if ((nr == 0 || (d->timer_control[nr] & TIMER_ENABLE)) && ...)`: timer 0 reads 3/3, timer 1 reads X = 3051, BOTH
gate-2 differentials pass (every gate-2 arm is enabled), and at rung 3 it brings #442's dead clock back on timer 1
(45 s disabled at 50 MHz: `CLOCK_DEAD=X`).  agy and grok argued one timer (gate 2 covers the callbacks) -- true for
callback bypasses and `nr`-conditioned edits, measured false for the enable-conditioned joint.  DISPOSITION: ALL FOUR
TIMERS, ~17 s each (~67 s).  I read this as L1 (the rows are pre-ship construction), not as a floor repair: the enable
bit is not an operand `footbridge_pending()` reads, so the conjunct is outside clause (d)'s DEPENDS-ON enumeration.

F3 (codex dedicated + codex panel; Opus follow-up) -- **the `==` cutoff.**  `>=` -> `==` in `footbridge_pending()`
is identical while the bound is constant; it never matches again once a re-arm LOWERS the bound below the count.
RESULT: MEASURED (`opus5_p1b.md`, `opus548_measured/harness_matrix.txt`): M_eq passes gate 2 (FBBOUND_PASS, R6 peak 762; `diff_footbridge.c` 864/864, which never calls the callbacks) and the drain (D = X = 3, PASS), identical to HEAD.  At rung 3 a guest CONTROL write from 12207 Hz to 762.94 Hz left M_eq owing 4529 against a bound of 762 (HEAD: 1).  My first repair -- owe 4096 before timer 0's re-arm -- catches M_eq but LOSES M_pendguard (a bound recomputed only while a backlog is owed), which today's R6 catches: the body's `>=` splits a re-arm into two cells (count below the new bound / past it) and each form covered one.  Opus's R6both keeps timer 0's re-arm at count 0 AND re-arms timer 2 with 4096 owed, in ONE row with the same peak == 762 oracle: across 15 mutants it catches the union, no mutant goes red->green, IDENTITY unchanged at 28 rows.  DISPOSITION: L2 -- a clause-(d) mutant of the fix's OWN predicate escaping #442's SHIPPED detectors, repaired in a follow-up commit per the late-dissent rule, in THIS round: adopt R6both (my edit is its code with comments; `diff_fbpending_bound.c` is CRLF and stays so).  The drafted hunk is in `p1_draft.diff`.

F4 (Opus, measured) -- **a bound skipped in TIMER_MODE_PERIODIC escapes EVERY instrument** (the drain on all four
timers, both gate-2 differentials): neither ever sets bit 0x40, though DEVINIT resets every timer to periodic, and at
rung 3 it brings the dead clock back.  Outside clause (d) (the fix reads no mode bit).  DISPOSITION: FILE as
coverage debt (`fbboundmodes`), ranked by the measured dead clock, cheapest fix named (a periodic case in gate 2's R1
table).  The contract discloses it.

F5 (Opus, measured) -- **the probe header's arm X "PLACEMENT DISCRIMINATOR" paragraph is FALSE.**  A bound moved into
DEVICE_TICK reads X = 1 and passes the drain on all four timers: the FREEZE's LOAD write sets the bound to 1 before the
drain counts, so any clamp outside the callback collapses the backlog first.  Gate 2 catches it (R1/R2/R5/R6).
DISPOSITION: correct the paragraph in place (L4) -- what X actually catches is a bound gated on a control bit its CTRL=0
write clears (ENABLE, FCLK_256).

F6 (codex panel; read) -- **"Every planted instruction is checked, as it EXECUTES" overstates:** only the 21 stepped
prologue words and, in arm E, arm D's drain body (0x70-0xe4) are checked.  The accrual loop (0x54-0x6c) and arm X's
disable/re-enable words (0x54/0x58, 0x70/0x74) free-run unchecked.  DISPOSITION: narrow the sentence (L4), and FILE the
residual it exposes: nothing proves arm X was actually DISABLED on a correct build (X reads 3 like D), so a broken
disable encoding would silently turn X into D and lose F2's kill.

F7 (codex, grok; Opus measured) -- **two wrong records about the ceiling:** `dev_footbridge.c`'s comment in
`reload_timer_value()` says deleting the ceiling means "the overflow returns", and `gate_offline.sh`'s #442 block says
the no-ceiling mutant "fails ... R2 with peak 2147483647".  Measured: R2 is green with the ceiling deleted.
DISPOSITION: correct BOTH in place in `#548` (L4, measured false; the stopping rule fixes wrong records in-round).  The
`dev_footbridge.c` edit keeps the SAME LINE COUNT, because `CHECK_ALLOCATION`'s `__LINE__` sits below it in the object;
two-part clearance on all four trees.  **Opus recommended FILING these; I am departing from that -- rule on it.**

F8 (grok, codex, agy, Opus) -- **row design:** a unique `FBDRAIN_VERDICT=(PASS|FAIL)` completion guard (REPORT-ONLY
must not count as completion); `FBDRAIN_CONTROL=OK`; the twelve control rows R0 C1 C2 A1 A2 E H1 H2 T L1 L2 P pinned by
DISTINCT GREEN ids (the aggregate stays OK if a row is deleted); `grep -cx 'FBDRAIN_BOUNDED=YES  (cap asserted: 762)'`
(the cap the probe parsed); `grep -cx 'FBDRAIN_CLOCK_DEAD='` (Opus measured the `sed`-extract-and-compare-to-"" form
green on a log with no such line); `FBDRAIN_VERDICT=PASS`; the exit status (`|| fdrc=$?`); `--accrue 4` explicit; no
echo of the MEASURED block; `python3` must START its own line (Opus measured a one-line `for ...; do python3 ...` read
as UNWIRED by section R).  No `rows run` wording (it would move SCORE_CLAIMS_MANIFEST).  DISPOSITION: ACCEPT all.

F9 (Opus, measured under `taskset` with busy loops) -- **a starved host shrinks N.**  12 busy loops on the probe's core:
the removed-bound mutant still read 1183 (1.55x the cap).  A starved run loses teeth SILENTLY, never reds falsely.
DISPOSITION: keep `--accrue 4`, disclose it in the contract; no row (under the fix N is not observable).

F10 (grok, codex; read) -- the EXEMPT deletion owes a rewrite of the dated paragraph above `EXEMPT` (it says the probe
"is still exempt"); the checker's census line "fbpending_drain_probe.py #442 11 rows" is a dated measurement AT
HEAD 3d752b4 and is NOT stale -- DISPOSITION: rewrite the paragraph, leave the census.  `gate_offline.sh:1311` ("it is
NOT run here") gains a pointer to gate 14.  `tools/pipeline/fable_queue.md` says the probe "runs in no gate at all";
that file is not this session's to commit -- recorded as owed text.

F11 (Opus) -- `gatedevicesplit` is OWED since #498; this block adds a device probe on gate 14's OWN `-E cats`
machine (the footbridge_sites precedent, not the #497 foreign-machine kind).  DISPOSITION: say so in the block.

## SCOPE -- the one decision I most want challenged

I propose ONE round touching six files: `regress/gate_arm.sh` (the block), `tools/pipeline/check_probe_wiring.py`
(EXEMPT + paragraph), `regress/fbpending_drain_probe.py` (header text only: usage, F5, F6, "~10 s" -> measured ~17 s),
`regress/diff_fbpending_bound.c` (F3, if measured), `src/devices/dev_footbridge.c` (F7, comment only, same line count),
`regress/gate_offline.sh` (F7 + F10).  Every hunk is `#442`'s detector material or `#442`'s own comments.  The
alternative is `#548` = wiring + probe header + checker, and a separate `#549` for gate 2's R6 and the two ceiling
records -- one more full panel cycle.

## QUESTIONS

1. **Which of my dispositions F1-F11 is wrong?**  Name the count.  Be hardest on F7 (where I overrule the measuring
   seat) and on F2's classification as L1 rather than a floor repair.
2. **Scope:** one round or two?  Is bundling the gate-2 R6 repair into a wiring round a scope breach under the carrier's
   round-scope rule, or is it the same site (#442's bound) and therefore in?
3. **F3:** Is R6both the right repair, and is this correctly L2 (a weakened form of the fix's own predicate, against a shipped detector) rather than coverage debt?  Is the two-cell closure complete -- does the body's `>=` distinguish any other re-arm cell (a count exactly AT the new bound?) that a row is owed for?
4. **F4/F6:** file, or fix in-round?  The owner's standing directive is "prioritize critical bugs and also easy
   resolvable ones"; the carrier's stopping rule files everything that is not a measured false pass or a wrong record.
5. Anything else -- including a member of the option set nobody named.
