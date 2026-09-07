# DATED NOTE beside `PRETABLE.out` -- written 2026-09-06 by the retrospective re-check
# (batch 8b).  THE FILE IS NOT EDITED.

## The mtime of this PRETABLE does not prove its precedence, and git does

The project's rule is that a PRETABLE block is written BEFORE its table runs and that the
file's own mtime is the proof of order.  For THIS file the mtime cannot carry that proof: the
block was appended to across several commits, so its timestamp is that of the LAST append and
post-dates the table logs beside it.

**Precedence is proven instead by git, and the evidence is stronger than an mtime.**  The
version committed as `c2249eb` already contains the block's opening sentence -- *"Written
2026-08-28, BEFORE table 1 ... This file's mtime is the..."* -- and that commit predates the
table logs in this directory.  So the block existed, with its predictions in it, before the
measurements it predicts.  Re-derive rather than trust this note:

    git log --format='%h %ad %s' --date=iso -- regress/artifacts/gdromexitsix/challenge_freeze_20260828/PRETABLE.out
    git show <the earliest such commit>:regress/artifacts/gdromexitsix/challenge_freeze_20260828/PRETABLE.out

## Why the note rather than a fix

Editing the file to "restore" a clean mtime would destroy the only durable evidence there is,
and the round already half-corrected the claim in place (its own text carries *"THIS SELF-GRADE
WAS OVERCLAIMED AND THE MTIMES REFUTE IT.  Corrected 2026-08-28"*).  What was missing was the
POSITIVE proof that replaces the mtime, which is what this note supplies.

**The general lesson, and it applies to every PRETABLE this project writes: an append refreshes
the mtime, so a block that is corrected or extended in place loses its order proof.**  The
standing practice -- corrections go to a SEPARATE `*.correction.out` file beside the original --
exists for exactly this reason, and this file predates that practice.
