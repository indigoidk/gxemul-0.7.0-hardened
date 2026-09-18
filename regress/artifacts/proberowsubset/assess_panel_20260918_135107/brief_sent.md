# `proberowsubset` ASSESS STAGE -- the six missing seats, by OWNER DECISION 2026-09-18

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
This is a HARNESS question (test tooling in `GXEMUL-SEC/regress/`), no emulator code.  Everything needed is inlined.
**VERDICT LINE FIRST** (BUILD-IT / BUILD-IT-NARROWER / DO-NOT-BUILD).  Check the premises, not only the derivations.

## THE ROW
"The probes cannot score ONE row, so adding a row to a measured detector costs a full re-run -- 4 hours where 20 minutes
would do."  A probe (e.g. `regress/gdrom_default_probe.py`) takes (binary, kernel), runs ~39 independent `session()` calls,
each forking a fresh emulator at settle=8.0 (~18 min a run), and prints one line per row plus a CONTROL line.  A kill table
re-runs the whole probe against every mutant binary.

## SETTLED (measured, re-inlined)
* The Opus seat MEASURED nine consecutive runs of one table: each run ~911 s; rebuild between runs 2-4 s.  **The probe is
  99.7% of the cost; caching mutant binaries saves nothing.  Row subsetting is the entire win.**
* A probe's rows are only composable if every row group runs in its OWN freshly forked emulator.
* The owner ruled the filter "ships as its own round with its own panel and its own negative controls".

## THE PROPOSED SPEC -- FIVE GUARDS (question: is it sufficient?)
  1  a filter must match a nonzero number of rows        4  the UNSET path's denominator is untouched
  2  every named row must exist                           5  CONTROL rows are exempt from filtering, or the control
  3  the denominator prints 'N of M'                          line hard-fails on an empty control set
Guard 5 exists because `GDROM_DEF_CONTROL` prints OK on `all(rows)` and `all([])` is True: a filter excluding every
control row would pass guards 1-4 while the control line reports OK having measured NOTHING.
Granularity: selection must gate SESSIONS, not rows, because 36 of 39 sessions are module-level -- a `row()`-level
filter passes all five guards and saves nothing.  TEST this claim, do not accept it.

## THE ONE PRIOR ANSWER THAT DISSENTS -- codex, 2026-09-08 (regress/artifacts/proberowsubset/codex_rowsel_20260908.txt, verbatim)
**Disposition: no cheap, maintainable general retrofit; leave existing probes unchanged and require explicit case selection in new probes.**

Mechanisms that avoid editing 36 call sites exist. They transfer the work into dependency inference or simulated execution, which is a poor trade for probes maintained mainly by reading them.

The premise also needs tightening: **a row can require multiple sessions.** Static inspection confirms the 36 direct assignments in `gdrom_default_probe.py`, plus three session call sites inside module-level loops. Its [`accept8` row](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py:621) combines eight emulator runs. Conversely, your example has several assertions sharing one transcript. The scheduler therefore needs the relationship between rows and their producers; merely adding a label to `session()` is insufficient.

The shortcuts I would reject are:

| Mechanism without per-site edits | Failure or maintenance cost |
|---|---|
| Select by session ordinal or caller location; return dummy results elsewhere | Insertions change ordinal meaning. Dummy results still enter ordinary computations. An eight-session aggregate can pass after only one real session if skipped sessions contribute empty text and “alive.” |
| Return lazy transcript/status proxies | Conditions, parsing and argument expressions execute **before `row()` receives control**. Those operations force the session anyway. Avoiding that requires deferring the surrounding assertions and computations too. |
| Inspect or transform the source to select session/row blocks | Simple adjacency handles your excerpt, but loops, accumulated transcripts, generated labels and reused variables require dependency analysis. A trustworthy implementation must reject unsupported shapes or maintain explicit mappings. That becomes another execution model reviewers must understand. |

A mechanical source rewrite could reduce the typing involved in introducing explicit case functions. It cannot remove the review of their boundaries and dependencies. **Few edits to the original files does not mean a cheap feature.**

There is one conditional alternative worth distinguishing: **re-score retained raw transcripts when adding assertions that need no new debugger commands.** Recording/replay can sit around the per-probe `session()` implementation without changing its callers. But ordinary row output is insufficient, changed commands require new measurements, and replay must retain provenance for the executable, inputs and capture conditions. Transparent caching by binary pathname would be particularly wrong for a mutation table. This is potentially cheap evidence reuse, not general live row selection.

Your four guards also need strengthening.

The existing [35-row gate checks](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gate_arm.sh:1206) already reject an honestly reported short run. Keep those literal expectations. The dangerous adaptations are shrinking their denominators, counting skipped rows as measured, or issuing normal completion claims from partial execution.

Any future selector should have this contract:

- **Validate against a declared inventory before execution.** Reject empty selections and every unknown requested name, including an unknown mixed with valid names. Automatically included controls must not rescue a zero-match request.
- **Print filtered intent before starting work.** Record requested names, the expanded execution set, planned row count, full inventory count and planned sessions. Expansion includes dependencies, required controls and any companion assertions.
- **Check completion against that plan.** Require the expected row identities exactly once, not merely `passed == len(rows)`. Otherwise a selected run can itself lose rows and shrink to a convincing denominator.
- **Give filtered runs separate result and completion records.** Preserve unset output exactly, including the absence of a new `FULL` banner. A filtered run must never issue the legacy full-run completion token.

That last point has a concrete trap here: [the gate ignores process status with `|| true` and then searches for `OPUS497T_DONE`](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gate_arm.sh:1155). A nonzero exit is insufficient. Even `OPUS497T_DONE_FILTERED` would match its substring search. Use a distinct token that does not contain the legacy token.

Controls are another independent obligation. The current [`GDROM_DEF_CONTROL` expression](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/gdrom_default_probe.py:424) already guards against `all([])` with `rows and`; that historical defect is repaired. **Nonempty still does not mean complete.** One surviving control could certify a selection that omitted two required controls. Define their required identities and execute them, or report the control assessment as incomplete.

For new probes, select **named cases whose bodies own their sessions and assertions**. A case can contain multiple sessions; a requested row resolves to its complete case and required controls. Running sibling assertions is cheap once their transcript exists. The existing [table-driven selector in `m88k_idle_probe.py`](/C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/m88k_idle_probe.py:177) demonstrates why selection is simple when the execution boundary already exists, although its selector should not be copied as a complete validation contract.

I would close this request as **documented-only for existing probes, with case selection required for new ones**. A repeatedly expensive individual probe can justify an explicit conversion later. The evidence supports that targeted investment; it does not support introducing a hidden execution framework across this tree.

## QUESTIONS
Q1. Build it, build it narrower (e.g. only for NEW probes, as codex proposes), or not at all?  What does each cost?
Q2. Are the five guards sufficient?  Name a filter that passes all five and still makes a measurement lie.
Q3. Session-gating vs row-gating: which, and how would a retrofitted probe prove its row groups are independent?


## OPERATIONAL RULE FOR EVERY SEAT (appended by panel.sh, not by the author)

**Do not run `run.sh`, any `gate_*.sh`, or the battery.** Every measurement you need is
inlined above. A gate takes minutes -- longer than your response budget -- and a second
concurrent invocation corrupts the operator run in progress, because the gates share one
log directory. A seat that runs a gate produces no review AND may invalidate someone
else s. Building and running a single detector or mutant in your own temp directory is
fine and encouraged; driving the harness is not.

If you want a measurement that is not inlined, NAME IT and say why. Naming it is worth
far more to this panel than a timeout.
