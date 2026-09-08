# AUDIT — probe HELPERS that can make a row report green on a wrong build

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**This brief asks for a sweep, not a judgement, and the population is real: 79 probe files with ~95
helper definitions.** I am not asking you to read all of them. **Rank by risk and report what you
actually checked, with a denominator** — "12 of 79 read, 3 defects" is a result; "audited the probes"
is not.

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/regress/`.** HEAD is `7a41b3f`.

**VERDICT LINE FIRST.**

## §C — THE CLASS, with three instances found this week

A probe row can be vacuous because its ORACLE is wrong even when its stimulus is right. All three of
these were found by someone reading the **helper**, not the row list:

**1. SUBSTRING WHERE A VALUE WAS MEANT** — `regress/lca_confwidth_probe.py`, found by you today.
The row tested `"IOC_CONF: 0x100000000" in text`. A diagnostic of `0x1000000000` — one extra literal
zero — **contains** that string, so the row went green on a wrong message. Its mirror: `"...: 0x0" in
text` also matches `0x0abc`. **Repaired** to parse the number and compare integers.

**2. `got` MANUFACTURED FROM A BOOLEAN** — same probe, same row. It printed
`"0x100000000" if full else "other"`, so the reported `got` was **the value it wanted**, not the value
seen. A reader auditing the log could not tell.

**3. FIRST-MATCH HELPER USED FOR A BEFORE/AFTER PAIR** — `regress/gdrom_data_probe.py`'s `printed()`
returns the **first** matching print. A design that samples the same register twice and calls it twice
gets **the same sample both times**, so `0xa8 → 0xa8` would be reported on a build that correctly
changes it.

## The task

**Rank the 79 probes by risk and read the top ones.** Suggested risk signals — challenge them:
* a row whose `got` is a conditional expression rather than a value read from output;
* `in` / `find` / `startswith` used where a numeric or exact comparison was meant;
* a helper that returns the first match, used more than once per row or per session;
* a regex whose value group can match a **prefix** of a longer value;
* a row whose `want` is a boolean-ish string (`"survived"`, `"yes"`, `"ok"`) where both builds produce
  it — the survive-only shape this project already names;
* a helper that returns a sentinel (`"absent"`, `None`, `0`) which some row then compares equal to a
  legitimate value.

## The questions

**Q1 — WHICH PROBES HAVE A ROW THAT CANNOT FAIL?** For each, name the probe, the row, the helper, and
**the concrete edit to the product that would keep it green**. That last part is what separates a real
finding from a style note.

**Q2 — IS THE `printed()` FIRST-MATCH SHAPE USED IN A BEFORE/AFTER PAIR ANYWHERE TODAY?** Instance 3
is currently a *design* hazard for a row not yet written. **Is any shipped row already relying on it?**
That would be a live defect rather than a caution.

**Q3 — WHICH OF THESE ARE GATED?** A vacuous row in a gate-run detector is worse than one in an
ungated probe, because the gate reports it green every battery. `tools/pipeline/check_probe_wiring.py`
knows which are gated. **Rank your findings by that.**

**Q4 — IS THERE A SHARED HELPER WORTH EXTRACTING?** Several probes define their own `printed()`.
**If they differ, say how** — a divergence between two copies of the same helper is the kind of thing
that makes one probe's rows sound and another's vacuous for no visible reason.

**Q5 — WHAT WOULD A MECHANICAL CHECK LOOK LIKE, AND SHOULD IT EXIST?** This project has rejected
checkers before, on measurement: a check that fires on the visible minority of a class while blind to
its dominant form is worse than none. **If you think a check is not worth building, say so** — that is
a real answer and it has precedent here.

## What I am not asking

Do not write patches or probes, and do not run anything. **Nothing ships until the flagship
adjudication on 2026-09-09.**

**If, while verifying a claim, you found something ELSE — say so.**
