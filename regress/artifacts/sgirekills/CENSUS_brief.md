# CENSUS (read-only) — `dev_sgi_re.c`'s twelve `exit(1)` sites: enumerate, classify, and RANK them

## READ THIS FIRST — PLEASE DO NOT SIMPLY RATIFY

**Check the premises, not just the derivations.** **Six briefs of mine this week stated premises that
were false or too broad**, each caught by a seat reading the code rather than my description of it.
**If a premise below is wrong, that is the most valuable thing you can tell me.**

**THE TREE UNDER REVIEW IS `GXEMUL-SEC/src/`.** Three pristine-2021-upstream copies of GXemul sit
under the project root and are NOT this fork.

**SCOPE YOUR READING TO `GXEMUL-SEC/src/` AND `GXEMUL-SEC/regress/*.py`.**

**Where this brief states a COUNT, ENUMERATE its members rather than reasoning about it.**

**VERDICT LINE FIRST.**

---

## §C — SETTLED PREMISES

**S1 — THE COUNT IS TWELVE, and it has been wrong twice.** The deriver is
`grep -cE '^[[:space:]]+exit\(1\);' src/devices/dev_sgi_re.c` and I ran it just now: **12**. The row's
title says 21 and an intermediate correction said 19; **both counted comments**. Please re-derive it
rather than trusting this line — a count that has been wrong twice is exactly the kind this project
insists on re-running.

**S2 — A NEIGHBOURING ROUND ALREADY DE-FATALISED THE WIDTH GUARD, AND IT DID NOT REMOVE THESE.**
`#497` changed the width predicate only. The width test is evaluated **first**, so a legal `ld` still
reaches the kill behind it.

**S3 — *** FIXING THIS WILL TURN A GREEN GATE RED BY SUCCEEDING. *** ** `regress/sgi_re_width_probe.py`
ships **six `ld kill` rows that assert the host still terminates** on an 8-byte access at each of six
windows. They *pin* the defect; they do not repair it. So this round inherits the oracle-correction
ordering: **re-pin the six rows first, measure the committed build RED under the new expectations,
then edit the code.** A round that edits first and re-pins after is indistinguishable from fitting the
test to the binary.

**S4 — A SIBLING SITE IS ALREADY DESIGNED.** In `dev_pcc2.c`, an analogous unconditional
`fatal(); exit(1);` was audited today and its disposition settled as DECLINE + LATCHED ANNOUNCE. The
in-tree idiom for these is a per-instance latch bit plus a `(once)` marker in the message text.

---

## The questions

**Q1 — ENUMERATE ALL TWELVE**, with line number, enclosing function, and the guard or condition that
reaches each. I want the table, not a summary.

**Q2 — CLASSIFY EACH by what the access actually is.** The project's disposition set is
DELETE · DECLINE (silent) · DECLINE + LATCHED ANNOUNCE · ACCEPT · FAULT · BACKED ACCEPT · IMPLEMENT,
and the tell for the last is a site with **no predicate at all** — a whole path stubbed out rather
than a guard rejecting a value. **Which member fits each of the twelve, and why?** Several are
`TODO: read from ...` shapes; say whether those are refusals or unimplemented paths, because the
answer differs.

**Q3 — *** RANK THEM BY HOW CHEAPLY EACH COULD BE FIXED. *** ** This is the question I most want
answered. For each site: does it need a new latch bit, a new row, a new probe session, or nothing but
the edit? **Which two or three are genuinely one-line changes with an existing row already covering
them?** I am looking for the cheapest real improvements, not the most interesting ones.

**Q4 — WHICH ARE REACHABLE, and by what?** Separate (a) reachable by an ordinary guest register
access, (b) reachable only through a path some other defect must first enable, and (c) not reachable
by any guest at all. **Name what you checked**, not just the conclusion.

**Q5 — DO ANY SHARE A LATCH BIT, or would they need one each?** `dev_sgi_re.c`'s enum currently
occupies bits 0..10. This device's own history is that a latch shared between sites is silenced by
the other site's ordinary traffic, so a shared bit is usually wrong here — but twelve new bits is a
lot, and I would like to know whether any of them genuinely group.

**Q6 — WHICH OF THE SIX `ld kill` ROWS WOULD HAVE TO INVERT**, and does inverting them leave any
window with no coverage at all?

## What I am not asking

Do not write a patch, do not write a probe, and do not run anything. I want the census, the
classification and the ranking.

**If, while verifying a claim, you found something ELSE — say so.**
