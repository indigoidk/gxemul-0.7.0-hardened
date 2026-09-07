# `sgirekills` DESIGN PASS -- twelve live terminating calls in `dev_sgi_re.c`, and the row's own count is wrong twice over.  2026-09-06.

## WHAT THIS IS
An ordinary correctness review of a graphics-engine device model in a hardware simulator for obsolete
workstations (GXemul 0.7.0, a maintained fork): the SGI "REX"/rendering engine on the O2-class machines.  Plain
engineering vocabulary; no security framing is intended or wanted, and none of this concerns a production
system.

**The tree under review is `GXEMUL-SEC/src/`.  Ignore any other `src/` you find** -- three pristine-2021
upstream copies sit under the project root and are NOT this fork; one of them bit the main loop last week and
the tell was line numbers off by hundreds.  The file is `GXEMUL-SEC/src/devices/dev_sgi_re.c` (1628 lines).
Cite by grep anchor, not by line number.  **VERDICT LINE FIRST.**

## READ THIS FIRST -- PLEASE DO NOT SIMPLY RATIFY
**This row's count has been wrong three times, twice by me, and the most recent wrong number was produced by a
check written to catch the previous one.**  The title says 21.  I "corrected" it to 19 an hour ago and
justified that by noting two greps agreed -- **both of which count commented-out lines**.  The live figure is
12.  Treat every number below as suspect and re-derive it; that is not politeness, it is the measured base
rate on this row.

## THE CENSUS, DERIVED TONIGHT (re-run it; do not trust it)

    grep -c 'exit(1)' src/devices/dev_sgi_re.c                    -> 19   ALL occurrences
    grep -cE '//[[:space:]]*exit\(1\)' src/devices/dev_sgi_re.c   ->  4   commented-out kills
    grep -cE '^[[:space:]]+exit\(1\);' src/devices/dev_sgi_re.c   -> 12   LIVE, statement position

Three further occurrences sit inside comment PROSE discussing `exit(1)`, which is why the naive count is 19.

**FOUR KILLS ARE ALREADY COMMENTED OUT** -- at the `horrible_getputpixel` `default:` arm, at a `tileptr`
high-bit check, at one `DEVICE_ACCESS` site, and at a `dst_y_step` range check.  *Somebody has already made
this round's decision four times in this file, and I do not know whether they were right to.*

## THE OPTION SET (seven members, and member 5 is not always available)
DELETE · DECLINE (silent) · DECLINE + LATCHED ANNOUNCE · ACCEPT · FAULT · BACKED ACCEPT · **IMPLEMENT**.
Member 7 was added tonight: all six others presume the access is a REFUSAL DECISION, which fails for a stubbed
PATH.  And **FAULT is not portable** -- it works because `memory_rw.c` dispatches an exception on a failed
device access for MIPS and M88K; check that the target CPU here has that before reaching for it.
**Before choosing, grep this file for its OWN existing idiom** -- the four commented-out kills are candidates,
and so is whatever replaced them.

## THE QUESTIONS
1. **What did the four already-disabled kills become, and is that pattern sound?**  On `lcabadval` tonight the
   equivalent question had a sharp answer: its disabled kill left a live `dev = 0` that ALIASES "no selected
   device" to device zero -- a latent defect, not a usable precedent.  **Do these four fall back to something
   safe, or to something similar?**  This is the single most useful thing you can tell me.
2. **Of the twelve live kills, which are guest-reachable and which need a driver doing something no driver
   does?**  `#499` worked on this file recently and its comment block says some arms "still exit(1)" -- so
   part of the file has had attention and part has not.  Distinguish them.
3. **Is `horrible_getputpixel` (the name is upstream's) a per-pixel path?**  If a kill sits inside a
   pixel loop, the disposition differs from a once-per-command register guard, and a latched announce would
   need care about where the latch lives.

## THE SECOND QUESTION, and note what it does NOT assume
Of my premises -- (i) 12 live kills, statement position; (ii) 4 already commented out; (iii) 7 of the 19
occurrences are non-executing; (iv) `#499` touched this file and left some arms killing -- **which is wrong,
if any?**  *A previous brief of mine closed with "assume at least one is wrong" and a seat correctly identified
that instruction itself as the unsupported assumption.  So: if they all hold, say so and say that plainly.*

VERDICT LINE FIRST (`SEVERITY ORDER: <what first>` / `PREMISE <n> IS WRONG: <what>` / `ALL PREMISES HOLD`),
then the disposition you would take per class, then anything else.  Under a page.
