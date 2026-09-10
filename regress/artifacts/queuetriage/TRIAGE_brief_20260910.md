# QUEUE TRIAGE -- rank the open rows for the next rounds (read-only; ordinary engineering triage)

Nonce: CODEX_QUEUE_TRIAGE_20260910.  Open with `VERDICT:` followed by your top five row ids in order, then echo the nonce.

**Please do not simply ratify the queue's own severities.**  Re-derive each ranking from what the row's
evidence actually shows.  Where a row's text states a fact about the source, check it against the source.

The tree under review is `C:\DocumentNoSnc\CC\GXEMUL\GXEMUL-SEC\`; ignore any other `src/` under the project root.

## Inputs
* `OUTSTANDING_BUGS.md` -- its "OPEN LIST" head is the live queue; the dated tail entries below it are the
  filings and closures (only OPEN rows live here by the file's charter).
* `tools/pipeline/ledger.json` -- one row per id (`id`, `sev`, `state`, `witness`, `entries`); rows with
  `state` `open` or `held` are candidates.  Two rounds are UNCOMMITTED and in flight and are NOT candidates:
  `lcabadval` (#518) and `sgirandomcolour` (#519); `lcaisalane` is the next round and its pass-1 panel is
  running now -- rank it but do not re-design it.
* `CHANGELOG.md` -- the shipped rounds (`# \`#NNN\`` headers), so a candidate that already shipped is caught.
* `src/` -- for the checks below.

## The owner's ordering rule (verbatim): "Prioritize critical bugs and also easy resolvable ones."
So produce TWO ranked lists:
1. **CRITICAL** -- rows whose defect, if reached, ends the host process, corrupts guest data or memory, or
   hands the guest wrong data silently.  For each: the site (grep anchor), whether a WITNESS exists (the
   row's `witness` field or an artifacts dir under `regress/artifacts/<id>/`), whether a design exists
   (a `codex_design_*` or a design panel dir), and the smallest honest estimate of the fix's shape (one
   guard? a new arm? a new device path?).
2. **EASY** -- rows that a one-to-five-line edit closes with a detector row that can be measured against a
   mutant in one session, where the witness or its obvious construction already exists.  Same fields.

## Checks that turn a ranking into evidence (do them, do not assume)
* `grep -rn 'exit(1)' src/devices/*.c src/cpus/*.c src/machines/*.c | wc -l` and list the sites still
  reachable from a guest access path (a `DEVICE_ACCESS` body, a cpu instruction handler) as opposed to
  init-time or debugger-only.  Which open rows cover them?  Which reachable exits have NO row?
* For every row you rank in the top five of either list, open its site and confirm the defect is still
  present at HEAD `1ce8296` (a row can be overtaken by a later round without being closed).
* For any row whose text says "no witness": say whether `regress/` already holds a probe that drives that
  device on an unmodified machine (grep the probe headers), because that changes the cost from "build a
  witness" to "add a row".

## Output shape
Verdict line; then the two lists as tables (id, sev as filed, sev as you would file it, site anchor,
witness?, design?, fix shape, why); then "reachable exits with no row" as a list; then anything you found
while checking that is not a ranking (a wrong row text, a duplicate, a row the CHANGELOG shows shipped).

Do not run builds or probes; do not propose patches; ordinary read-only triage.
