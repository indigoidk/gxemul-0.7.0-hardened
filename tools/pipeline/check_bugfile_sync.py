#!/usr/bin/env python3
"""Every OPEN ledger row must also be findable in OUTSTANDING_BUGS.md.

*** THIS GAP HAS NOW HAPPENED TWICE, AND THE FIRST FIX WAS A HAND-WRITTEN CATCH-UP COMMIT. ***
`f7eac43` is titled, in full, "OUTSTANDING_BUGS: the R4-detector round's residuals, which went
to the ledger and not here."  One round later it recurred at TWENTY-ONE rows.  A check a human
has to remember is a check that eventually does not happen, so it is mechanised here.

WHY BOTH FILES EXIST, because the obvious reaction is "delete one".  They answer different
questions and this project has been bitten from BOTH directions:

  * `ledger.json` is the pipeline's source of truth -- per-seat, per-phase, machine-read by
    gen_dashboard.py and check_stage_panels.py.  A round with no ledger row is invisible to
    section H.  That was `es438`, and fixing it produced `lunafuse`, which was filed in
    OUTSTANDING_BUGS and given no ledger row -- so the fix reproduced the defect one layer in.
  * `OUTSTANDING_BUGS.md` is what a HUMAN (or a fresh session) reads to find the live queue.
    CLAUDE.md names it explicitly as a first-stop-each-session file.  Twenty-one rows filed on
    2026-08-20 were absent from it, so a fresh session reading the queue would not have seen a
    day's work.

The reverse direction is already clean (no OUTSTANDING_BUGS header lacks a ledger row), which
is what the es438 fix bought.  This closes the other direction.

SCOPE, deliberately narrow.  Only OPEN rows are required: the bug file's own charter says
"Only genuinely OPEN items live here.  Resolved ones are removed, not annotated", so demanding
an entry for a closed or dropped row would fight the file's design and push it toward the
accumulating-index failure that #270 exists to prevent.

FORWARD-ONLY BY DATE, like section O: rows whose newest entry is on or before CUTOFF are
reported and not failed.  A rule that retro-fails the archive gets switched off.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "ledger.json")
BUGS = os.path.join(HERE, os.pardir, os.pardir, "OUTSTANDING_BUGS.md")

CUTOFF = "2026-08-20"
OPEN_STATES = ("held", "in work", "active", "pending")


def newest_date(row):
    ds = [e.get("date") or "" for e in row.get("entries", [])]
    return max(ds) if ds else ""


def unsynced(rows, text):
    """[(id, state, date)] for OPEN rows the bug file does not name."""
    out = []
    for rid, row in sorted(rows.items()):
        if row.get("state") not in OPEN_STATES:
            continue
        #  Match the id as a markdown code span or a heading -- not a bare substring, which
        #  would let a two-letter id like `n2` match any English word containing it.  That is
        #  the padded-column grep trap in another costume.
        if re.search(r"`%s`" % re.escape(rid), text) or \
           re.search(r"^#+\s+%s\b" % re.escape(rid), text, re.M):
            continue
        out.append((rid, row.get("state", "?"), newest_date(row)))
    return out


def main(argv):
    ledger = json.load(io.open(LEDGER, encoding="utf-8"))
    rows = {r["id"]: r for r in ledger["rows"]}
    text = io.open(BUGS, encoding="utf-8", errors="replace").read()

    missing = unsynced(rows, text)
    live = [m for m in missing if m[2] > CUTOFF]

    for rid, state, date in missing:
        tag = "MISSING" if (date > CUTOFF) else "ARCHIVED"
        print("  %-9s %-16s %-8s newest entry %s" % (tag, rid, state, date or "(none)"))

    print()
    print("  An OPEN row nobody can find by reading OUTSTANDING_BUGS.md is work a fresh")
    print("  session will not see. The ledger is the pipeline's truth; the bug file is the")
    print("  human queue, and CLAUDE.md names it as a first-stop-each-session file.")
    print()
    if live:
        print("BUGFILE_SYNC_FAIL  %d open row(s) filed after %s with no entry"
              % (len(live), CUTOFF))
        return 1
    print("BUGFILE_SYNC_PASS  %d archived (on/before %s), 0 new" % (len(missing), CUTOFF))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
