*** SUPERSEDED 2026-10-21 (the repair-diff pass): line 3 below says the typedef edit leaves the object code
*** "otherwise identical".  It does not -- the comment lines moved DEVINIT's __LINE__ (231 -> 234) and the cast changed
*** -O3's layout: killtable2_20261021/OBJDUMP_fix568_vs_fix568b.txt.  Kept as written; this header is the correction.

**THE REPAIR (not yet built -- everything below is planned, nothing is measured):**
* **fix568b** -- comment-only changes for F3, F4, the typedef rewording + conjunct deletion (F2), and -- if D1 holds --
  the `%llx` format change, which is the one behavioural-text change.  Object code is otherwise identical; the record will
  say so only after comparing the two objects, not from reading.
* **REV 3 of the probe** -- F1's zero-store first-access row; F10 (a)-(c)'s rows if D4 holds; the CONTROL split (F8);
  the neutral stop wording (F9); the docstring (F7, F12).  Every changed or added row named with its mutant and channel
  in a PRETABLE written before the table runs, and that PRETABLE diffed against the row list (the `#490` rule).
* **TABLE 2** -- in a fresh scratch clone: BASE, HEAD, NULL, every table-1 and table-1b leg regenerated on fix568b, plus
  M_IDATA (F1), M_ONENARROW (F2/D5), M_LATCHLEN4 (F10a), M_DFATAL (F10b) and M_LANE0 (F10c).  **M_IDATA is measured on
  the FROZEN rev-2 instrument first** -- if it already reds, F1 is refuted and recorded.
* **Then** the block-only gate both ways on rev 3, the full gate 14 alone, and a pass on the REPAIR DIFF (the repair-
  chain rule: a repair made in response to a pass 2 owes its own pass, scoped to that diff, closing on the first pass
  with zero floor breaches).

**Where I may be fooling myself:**
* F1 is a prediction by one seat, checked only by reading.  If M_IDATA reds on rev 2 I have over-reacted.
* I am about to add rows after a clean table -- the shape that grew `#499` by one cell per pass.  D4 is where you can
  stop me.
* "Comment-only, object code identical" is a claim I will measure, not assert -- the `-g` line tables alone can make the
  objects differ.
* The late-review RECORDS unit (a different item) commits before this round; nothing in it touches dev_vme.c or the probe.
* No seat has yet looked at the probe's FREE-RUNNING sessions' timing budgets under load (30 s per `continue`): three legs
  took 74 s because a stopped pass 2 waited out its budget.  A loaded host could turn a green row red by timeout; the
  rows would then fail LOUDLY (red), not silently, but the gate's wall-clock exposure is real.
