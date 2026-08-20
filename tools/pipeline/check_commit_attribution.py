#!/usr/bin/env python3
"""DOES THE LEDGER KNOW ABOUT THE WORK THAT SHIPPED?

Usage:
    check_commit_attribution.py [--list] [--all]

The ledger is this project's single source of truth and `gen_dashboard.py` renders the board
from it.  So a row whose work has SHIPPED but whose `commits` field is empty makes the board
under-report finished work and over-report the open queue -- and every decision taken off that
board is then taken off a stale picture.

MEASURED 2026-08-19, which is why this exists.  Of the 40 most recent commits, 33 were named
by NO ledger row.  Most of those are legitimate (a receipt, a records fix, harness work that
closes nothing).  The sharp subset is not:

    commit 6014b7e   subject "selfmutant6 CLOSED: the fifth control, ..."
                     ledger row `selfmutant6`   state=held   commits=(empty)

A commit that announces a row CLOSED, against a row the board still shows as open, is a wrong
record in the direction that matters: it is invisible work.  Thirteen rows were in some form
of this state when the check was written.

------------------------------------------------------------------------------------------
WHAT IT CHECKS, and the three grades are deliberately different failures:

  HARD   a commit subject names row R with a CLOSURE word, and R.state != "closed".
         The commit says the work is done; the board says it is not.  One of the two is
         wrong and neither can be believed until someone looks.

  HARD   R.state == "closed" and a commit subject names R, but R.commits does not list it.
         A closed row that does not name what closed it cannot be attributed -- the same
         defect `nightly_check.sh` fixes for the battery verdict.

  SOFT   a commit subject names an OPEN row and R.commits is empty.  Progress commits on an
         open row are ordinary and this is NOT a failure; it is listed so the drift stays
         visible rather than accumulating silently.

  SOFT   a commit subject names a CLOSED row whose `commits` is EMPTY.  That is a
         DOCUMENTED-ONLY closure -- a duplicate credited elsewhere, or a row closed with no
         code -- and `check_witness.py` already treats the same shape as legitimate ("nothing
         shipped"), so hard-failing it here would put the two checks in contradiction.  Found
         by this check's FIRST REAL USE, not by a control: rtcdet closed as a duplicate of
         rtcgate with empty commits on purpose, while the commit subjects said "rtcdet", and
         the check demanded the row name a commit it had deliberately declined to claim.

         It stays SOFT rather than silent because the shape is also how someone would DODGE
         the check -- close a row that really did ship with empty commits and the hard rule
         evaporates.  Only the closure note distinguishes the two, and only a reader can
         judge it, so the check names the row and declines to grade it.

------------------------------------------------------------------------------------------
*** THE BLINDNESS IS REPORTED, NOT HIDDEN, AND THAT IS THE POINT OF THE LAST SECTION. ***

Row ids shorter than MIN_ID characters (`n2`, `d1`, `a4`, `b1w`, ...) are NOT matched, because
a two-character token matches English text and would fire on unrelated subjects.  A check that
silently skips a third of its subjects while printing a green line is this project's own named
vacuity class -- "a check whose blindness is reported as a green line".  So the skipped ids are
PRINTED EVERY RUN, with their count, whether or not anything failed.  If you want them covered,
the fix is to give them longer ids, not to lower MIN_ID.

*** THE SECOND BLINDNESS: THIS CHECK IS SUBJECT-DRIVEN, so a row is covered only if some
commit happens to NAME it. ***  Found by a negative control that injected three breaks into
`rtcgate` and saw none of them: two commits shipped that row's work and neither subject says
"rtcgate".  Every injection was invisible, and read at first like three detector failures.
A row can therefore have wrong attribution forever and this check will never look at it.
That set is PRINTED EVERY RUN alongside the short-id set, for the same reason: a check that
silently covers a third of its subjects while printing a green line is the vacuity class this
project named.  Widening it (matching commit BODIES, or a `rows:` trailer) is a real option
and is deliberately not taken here -- bodies quote other rows constantly, which would trade
this silent gap for loud false positives.

Matching is on the SUBJECT LINE only, at word boundaries.  The body is excluded deliberately:
commit bodies here quote other rows constantly ("filed separately as n2/n4/tfreq"), and a
mention is not a claim of authorship.

*** RECORDS-ONLY COMMITS ARE NOT AUTHORSHIP EITHER, AND THE FIRST VERSION OF THIS CHECK GOT
THAT WRONG. ***  It reported three commits -- ef01e28, 716934d, 8631dc0, all named "m8820x:
..." -- as a closed row failing to name what closed it.  Verifying instead of believing showed
all three touch ONLY OUTSTANDING_BUGS.md: they are the round's reproduction and research
records, and the row correctly names its five CODE commits.  A row is authored by what shipped,
not by what was written about it.  So a commit whose every path ends in .md is never a hard
failure; it is listed as soft when the row is open, and ignored when the row is closed.

That distinction is the check's own version of the rule it exists to serve, and getting it
wrong would have made the gate fire on every research commit this project makes -- the fastest
possible way to have a gate switched off.
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.normpath(os.path.join(HERE, "..", ".."))
LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")

#  How far back to read.  Not "all history": the ledger's `commits` convention is recent, and
#  older rows were closed under different bookkeeping.  Overridable for an audit.
DEPTH = int(os.environ.get("GXATTR_DEPTH", "60"))

#  Below this length a row id is a word, not an identifier.  See the blindness note above.
MIN_ID = 4

#  A commit subject claiming the work is finished.  Deliberately narrow -- "gate", "record"
#  and "file" are progress verbs here, not closure verbs, and including them would turn every
#  ordinary round into a hard failure.
CLOSURE = re.compile(r"\b(closed|closes|closing)\b", re.I)


def git(*args):
    return subprocess.run(["git", "-C", SEC] + list(args),
                          capture_output=True, text=True).stdout


def records_only(h):
    """True when every path this commit touched is documentation.

    Cheap and cached by the caller: only consulted for commits that already matched a row id,
    which is a handful per run rather than the whole log."""
    paths = [p for p in git("show", "--name-only", "--format=", h).splitlines() if p.strip()]
    return bool(paths) and all(p.lower().endswith((".md", ".txt")) for p in paths)


def main(argv):
    listing = "--list" in argv
    ledger = json.load(io.open(LEDGER, encoding="utf-8"))
    rows = {r["id"]: r for r in ledger["rows"]}

    short = sorted(i for i in rows if len(i) < MIN_ID)
    matchable = {i: r for i, r in rows.items() if len(i) >= MIN_ID}
    pats = {i: re.compile(r"(?<![A-Za-z0-9])%s(?![A-Za-z0-9])" % re.escape(i))
            for i in matchable}

    log = [l.split("\t", 1) for l in
           git("log", "--format=%h\t%s", "-%d" % DEPTH).splitlines() if "\t" in l]

    hard, soft, ok = [], [], 0
    for h, subj in log:
        for rid, pat in pats.items():
            if not pat.search(subj):
                continue
            row = matchable[rid]
            commits = (row.get("commits") or "").split()
            state = row.get("state", "")
            #  *** THE CLOSURE CONTRADICTION IS TESTED FIRST, AND THE ORDER IS LOAD-BEARING.
            #  ***  It sat below the `h in commits` early-out until a negative control caught
            #  it: a row can NAME the commit and still contradict it -- state "in work" under
            #  a commit whose subject says CLOSED -- and the early-out scored that as
            #  attributed.  The injected break went undetected and the run stayed green.
            #  Being listed is not the same as agreeing.
            if CLOSURE.search(subj) and state != "closed":
                hard.append((h, rid, state, "commit says CLOSED; row is %r" % state, subj))
            elif h in commits:
                ok += 1
            elif records_only(h):
                #  Writing ABOUT a row is not authoring it.  Silent for a closed row (the
                #  research records of a finished round are not drift); soft for an open one,
                #  where it is still useful to see the row is being worked.
                if state != "closed":
                    soft.append((h, rid, state, "records-only commit (.md/.txt)", subj))
            elif state == "closed" and not commits:
                #  Documented-only closure: see the header.  Named, never graded.
                soft.append((h, rid, state,
                             "closed documented-only (empty commits) -- read the closure note",
                             subj))
            elif state == "closed":
                hard.append((h, rid, state, "closed row does not name this code commit", subj))
            else:
                soft.append((h, rid, state, "open row, commits empty"
                             if not commits else "open row, commits=%s" % " ".join(commits),
                             subj))

    for label, items in (("HARD", hard), ("SOFT", soft)):
        for h, rid, state, why, subj in items:
            print("  %-6s %-9s %-14s %-8s %s" % (label, h, rid, state, why))
            if listing:
                print("         %s" % subj[:88])
    print()
    print("  scanned %d commits deep; %d subject/row matches already attributed" % (len(log), ok))
    #  ALWAYS printed, pass or fail -- the blindness is part of the result, not a footnote.
    print("  NOT MATCHABLE (id shorter than %d chars, would match English): %d -- %s"
          % (MIN_ID, len(short), " ".join(short) if short else "none"))
    print("  Rows with these ids are INVISIBLE to this check. Lengthen the id to cover one.")

    #  The second blindness -- see the header.  A row that SHIPPED but that no commit subject
    #  ever names is never examined, so its attribution could be wrong indefinitely.  Only
    #  rows with commits are worth listing: an open row nobody has committed against yet is
    #  simply not started.
    subjects = " \n".join(sub for _h, sub in log)
    unnamed = sorted(rid for rid, row in matchable.items()
                     if (row.get("commits") or "").strip() and not pats[rid].search(subjects))
    print("  NEVER NAMED in any scanned subject, yet carry commits: %d -- %s"
          % (len(unnamed), " ".join(unnamed) if unnamed else "none"))
    print("  Those rows shipped work this check cannot see. It reads SUBJECTS, not diffs.")

    if hard:
        print()
        print("ATTRIBUTION_FAIL  %d hard, %d soft" % (len(hard), len(soft)))
        return 1
    print("ATTRIBUTION_PASS  0 hard, %d soft" % len(soft))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
