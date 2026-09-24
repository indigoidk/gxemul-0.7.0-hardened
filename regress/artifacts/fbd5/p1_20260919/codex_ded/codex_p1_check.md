# Dedicated codex reading, fbdeclinefive PASS 1 -- audit the design brief's premises and enumerate what it claims

## READING SCOPE AND FORM
Read the design brief `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\fbd5\brief_fbd5_design_BUILT.md` (it inlines the datasheet
lines, the full enclosing function at HEAD 9c28ca5, the proposed rows), then the tree `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`
(HEAD 9c28ca5): `src/devices/dev_footbridge.c`, `src/include/thirdparty/dc21285reg.h`, `regress/footbridge_sites_probe.py`,
`regress/fbpending_drain_probe.py`, `regress/fbpending_witness.py`, `regress/gate_arm.sh` (footbridge section),
`src/core/main.c` and `src/machines/machine.c` (the unknown `-E` path), `src/debugger/debugger_cmds.c` (`quit`), and the
datasheet `C:\DocumentNoSnc\CC\GXEMUL\_scratchpad\dc21285.txt`.  Scope your reading to `GXEMUL-SEC/src/`, `GXEMUL-SEC/regress/*.py`,
that one gate section and the datasheet; do not read `regress/artifacts/`, `tools/pipeline/ledger.json`, CHANGELOG.md or
OUTSTANDING_BUGS.md.  Read-only; run nothing; construct no programs or edits -- this is an ANALYSIS of the design's premises
(what is true) and of which SUPPLIED candidate weakenings the proposed rows would catch.  Ordinary engineering language
(terminating calls, declines, error paths).  VERDICT LINE FIRST; READ (file, anchor) / REASONED / NOT CHECKED; counts with
denominators.

## QUESTIONS
1. Every load-bearing premise in the brief's section 2 -- for each: TRUE / FALSE / NOT CHECKABLE, with the anchor that
   settles it.  In particular: the five sites' line numbers and directions; "the +0x18c read computes odata = d->irq_enable
   before terminating"; "quit exits 0 through normal shutdown"; "the unknown -E name exits 1 before any prompt and its
   diagnostic names the input" (main.c / machine.c: quote); the teardown description; the exit_census count (ten, with the
   line list).
2. The five complaint texts the brief proposes (K4's): is any of them already present in the file (grep count each), and
   does any gate or hygiene rule in `regress/*.sh` grep for the OLD texts (`WARNING: footbridge write to irq status?` etc.)
   or for `ENABLE CLEAR`?  List every consumer.
3. The struct: list `footbridge_data`'s fields; which are latches today (name, type, where set); is there a precedent in
   THIS file for a bit-field latch or only for per-site ints?  Elsewhere in `src/devices/`, how many files use a bit-field
   `warned`-style latch vs per-site ints (counts by grep, with the pattern you used)?
4. The rows A1-A5 / D1-D5 as the brief states them: for each, is the expected value derivable from the code + datasheet
   (show the arithmetic, e.g. IRQ_STATUS read with enable 0x30 and irq_status 0 -> 0), and which of the brief's Q2
   candidates (a)-(k) does it catch, which escape?  Say which candidates NO row catches.
5. The harness legs K1/K2: read each of the three launchers (sites' `run_arm`, drain's and witness's `Session`) and say
   exactly what each would have to observe for K1 (startup rejection) and K2 (quit after a verified prologue) -- which
   existing function returns the fact, or that none does and a new one is needed.  What does the sites probe's `wait()`
   return when the child never prints a prompt because it exited at startup?
6. The reopening rule: are the five sites truly ONE class (same device, same semantic class, same detector, one fix
   design), or does any site differ (e.g. IRQ_ENABLE_CLEAR's read is the only READ among four WRITES -- does that matter
   for the rows or the fix shape)?
7. Standing licence: anything else -- a sibling arm with the same shape the brief did not list, a datasheet fact that
   changes a disposition, an option-set member the brief did not weigh (DELETE / DECLINE / DECLINE + LATCHED ANNOUNCE /
   ACCEPT / FAULT / BACKED ACCEPT / IMPLEMENT).
End with: model, files read (working-tree md5 of each), nothing run.
