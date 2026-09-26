# DEDICATED ADVERSARIAL JOB -- #549 v6's adjudication pass (read-only)

Read `C:\DocumentNoSnc\cc\GXEMUL\GXEMUL-SEC\regress\artifacts\fbctrlportkill_20260924\pass_v6\f2_v6_brief.md` in full --
every seat's findings on v6 (N1..N24) with the main loop's disposition on each, the probe's header verbatim, session B,
and table 6's full-score edits.  The tree is `GXEMUL-SEC/` only; it holds v6 (`regress/fbctrl_port_probe.py`) and the
fix (`src/devices/dev_fbctrl.c`, `case DEV_FBCTRL_PORT:`).

Two floor questions are open, and grok raised both -- so this job is SELF-REVIEW, and you are asked to be HARDER on
them than on anyone else's finding:

* **D1 (N1, latch-clear x bit).**  Read the carrier's joint-cell rule as the brief quotes it.  Is `warned_port == 0` a
  floor cell of the fixed arm, or is the pair (latch, value) a two-axis joint that NOT CLAIMED (0) discloses?  Argue
  AGAINST your own earlier FLOOR reading first; then say which reading survives, and why.
* **D2 (N21, a refusal that writes the constant 5).**  Check the claim against the probe's own rows: which rows read
  PORT after a refusal whose previous selector is not 5, and does any of them see a written 5?  Then test the proposed
  remedy -- one width group anchored at 7 instead of 5: does it CLOSE the class, or MOVE it (a constant equal to the new
  anchor, on bits only that width carries)?  If it moves it, what is the smallest row set that closes it, and does
  that set terminate?

Then: **which of the main loop's ACCEPTED dispositions (N2..N24) is wrong?**  A zero needs its denominator -- list
what you checked.  Open with `VERDICT: <SHIP | SHIP WITH CHANGES | DO NOT SHIP>`.  Do not write any file.
