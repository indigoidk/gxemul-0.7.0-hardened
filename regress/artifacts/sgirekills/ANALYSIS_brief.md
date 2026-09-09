# `dev_sgi_re.c` — a census and ordering question about its terminating arms

**Answer in prose. Do not propose a code change, do not write a test, and do not construct any input
or instruction sequence.** I want the census and the ordering analysis; I will design the repair.

## Read only these files

    src/devices/dev_sgi_re.c
    src/include/thirdparty/crmfbreg.h
    regress/sgi_re_width_probe.py

Do not read `CHANGELOG.md`, `tools/pipeline/ledger.json`, `OUTSTANDING_BUGS.md`, or anything under
`_scratchpad/`.

## Please do not simply ratify

**Where I claim a COUNT or a REACHABILITY, enumerate it and report what you get.** Ask what the
PRODUCER of each value can emit before walking it. A derivation that skips one guard reads exactly
like a correct one — and one of the claims below is already known to have been wrong for four rounds.

**VERDICT LINE FIRST.**

## What I believe, stated so you can refute it

1. The file contains twelve `exit(1)` statements.
2. Eleven are reachable by an ordinary guest access; the twelfth is the trailing `else` of a chain
   shaped `if (len == 4) ... else if (len != 4) ... else ...`, which is provably unreachable.
3. A previous round de-fatalised only the WIDTH guard, and because the width test is evaluated
   FIRST, a legal access still reaches the remaining kills.

## The questions

**Q1. Enumerate every `exit(1)` in the file.** For each: the enclosing function, the guard that
selects it (or "no guard"), and what a guest must do to reach it — an ordinary access, a specific
width, a specific register, or a specific value. **Say plainly which ones you cannot settle from
these files.**

**Q2. Confirm or refute the unreachable one.** Give the exact condition chain and say why the final
arm can or cannot be entered. If it IS reachable, that is the most important thing in your answer.

**Q3. THE ORDERING.** For each reachable kill, say whether it is evaluated BEFORE or AFTER the
width guard that was already de-fatalised. I need to know which kills a guest hits first, because
that determines what a repair must change and in what order.

**Q4. What does `regress/sgi_re_width_probe.py` currently ASSERT about these sites?** I believe six
of its rows assert that the host still dies. If so, name those rows exactly as they are labelled.
**This matters because a successful repair will turn those rows RED by succeeding** — I need to know
precisely which rows must be re-pinned before the code changes, and I want that list from the file
rather than from memory.

**Q5. Are the eleven one class or several?** Group them by what a repair would have to do — the same
guard shape, the same kind of unimplemented feature, the same missing value. I am trying to learn
whether this is one round or several, and grouping by repair-shape is what decides that.

**Q6. What does this file already do elsewhere with an unimplemented case?** Name its existing
non-terminating idioms and where they are. An in-file precedent is worth more than a general
principle.
