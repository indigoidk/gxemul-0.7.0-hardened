# killtable3 — DELIBERATELY STOPPED MID-RUN.  Not a failed table; an abandoned one.

**This directory holds TWO mutants of a planned nine, and that is on purpose.  Read this
before drawing any conclusion from its contents.**

## What it was

The third kill table for `#489`, against the **18-row** version of
`regress/gdrom_toclen_probe.py` — the version that existed after pass 2's first two escapes
(`zero cond`, `over cond`) were closed.

```
base.raw          22 lines   TOCLEN_RESULT=18/18   controls=OK   reds: none
M1_reinstate.raw   2 lines   NO RESULT LINE -- killed after two control rows
```

## Why it stopped

While it ran, the pass-2 adjudicator returned a **third** escape that no other seat found: the
latch-state collapse, `if (d->cnt != 408 && !(d->warned & GDROM_W_TOCLEN))`, which sweeps an
18-row detector **clean** while re-opening the round's heap overflow for every bad TOC after
the first.

Closing it required a nineteenth row (`latch cond`), and adding a row changes **every
denominator** — so this table was superseded the moment that finding landed.  Running its
remaining seven mutants would have produced ~35 minutes of numbers that no record would ever
cite.

**It was therefore stopped deliberately, via the harness rather than a signal**, and the tree
was restored by the documented procedure: `cp` from **GXEMUL-SEC** (never a script's own
backup), rebuild, and verify BOTH parts — binary `13:23:51` against source `13:23:45` — before
the sentinel was cleared.  The sentinel had correctly recorded the mutant state in the interim.

## *** THE ONE CAVEAT: `M1_reinstate.raw` IS TRUNCATED.  IT IS NOT A SCORE. ***

It contains **two lines** — the `live` and `devsig sh4` control rows — and **no
`TOCLEN_RESULT` line at all**, because the run was stopped mid-probe.  Do not read it as a
mutant result; there is no denominator in it to read.

> *A first draft of this README said something different and more plausible: that the file
> carried a `19` denominator inherited from a later probe edit.  **That was invented rather
> than observed** — `wc -l` says 2 and `grep TOCLEN_RESULT` finds nothing.  Corrected by
> opening the file.  A README written to warn about a wrong record is exactly the wrong place
> to guess.*

**Cite `killtable4_20260828/` for every number.**  This directory is kept only as evidence
that the 18-row detector was measured CLEAN (`base.raw`, 18/18, controls OK) **before** the
third escape was found — which is what makes that escape a real finding rather than an
artefact of the 19-row file.

*The general rule the deliberate stop serves: a probe edited between mutants scores early
mutants against one row set and late ones against another.  That is why the adjudicator's
condition was "complete the table or stop it deliberately, then run ONE final table at the
final row count" — and why table 4 is the only one the round block cites.*
