#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Catch a ledger row whose STATE disagrees with what the repo shipped.

*** WHY THIS EXISTS: A ROUND WAS NEARLY REDONE FROM SCRATCH. ***

`sqreadtype` sat at state `open` with a witness field reading "the
oracle-correction rule requires the NEW pin measured RED on the COMMITTED build
before any source edit -- that measurement is the round's warrant and is
PENDING".  The round had shipped hours earlier as `3ff2138`, and that
measurement is recorded in its own CHANGELOG block: re-pinned oracle 26/31 RED
on the committed build, 31/31 on the fixed build, in that order.

It was caught by accident.  The row was picked as the NEXT round, and the source
comment already said "#454: JUDGED AS A READ".  Without that coincidence the
work would have been redone.

The carrier already names this class -- a state-vs-substance mismatch, where
"a future reader who trusts states reads that as 'not done', which is false".
Nothing checked it.

*** THE FIRST DESIGN WAS VACUOUS, AND ITS POSITIVE CONTROL SAID SO. ***

It looked for the row's id in a commit SUBJECT.  Reinstating `sqreadtype` as
open did not flag it, because commit subjects here carry ROUND NUMBERS -- the
one that shipped it reads "#454 the store-queue PREF transfer is judged READ
type" -- and name no row at all.  Measured: the id appears zero times in that
commit's message and zero times in its ledger diff.  A check that cannot catch
the incident that motivated it is worse than no check, and only running the
positive control revealed it.

*** THE ASSOCIATION THAT WORKS IS THE `witness` FIELD, and it is there by
design. ***

A row's `witness` names the artefact that proves the defect reachable --
`probe:<path>`, `boot:<rig>`, `construction:<gate>` -- forward-only since
2026-08-19.  A row that names a PROBE is asserting that probe exists.  So:

    an `open` row whose witness names a probe file that has been COMMITTED
    is a row claiming to be unstarted while its detector is in the tree.

That is narrow on purpose.  It says nothing about rows with `witness: none`
(the honest state for an unstarted item), nothing about `in work` (which means
exactly "committed something, still working", so a commit proves nothing), and
nothing about rows whose witness is a boot or a construction gate that predates
them.

Measured on the tree the day it was written: the reinstated defect is FLAGGED,
naming the probe and the shipping commit; with the row correctly closed, 0
flagged, and no other open row trips it.

A row may opt out with `"state_note"` explaining why code shipped under its name
while it is genuinely still open -- a partial fix, or a sibling site left for a
later round.  The note is required to say which; an empty opt-out is the silent
exemption this harness keeps being bitten by.
"""
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEDGER = os.path.join(ROOT, "tools", "pipeline", "ledger.json")

#  `probe:regress/foo_probe.py` possibly followed by prose -- the witness field
#  is free text after the artefact, and sqreadtype's ran to three sentences.
WITNESS = re.compile(r"probe:(\S+?\.py)")


def commits_for(path):
    out = subprocess.run(["git", "-C", ROOT, "log", "--oneline", "--", path],
                         capture_output=True, text=True,
                         encoding="utf-8", errors="replace").stdout
    return [l for l in out.split("\n") if l.strip()]


def main():
    d = json.load(io.open(LEDGER, encoding="utf-8"))
    bad, exempt, checked = [], 0, 0

    for r in d["rows"]:
        if r.get("state") != "open":
            continue
        checked += 1
        m = WITNESS.search(r.get("witness") or "")
        if not m:
            continue
        if r.get("state_note"):
            exempt += 1
            continue
        c = commits_for(m.group(1))
        if not c:
            continue                    # probe named but never committed: fine
        bad.append("%s is state=open, but its witness names %s, which is "
                   "COMMITTED (%d commit(s)).\n"
                   "              most recent: %s\n"
                   "              A row whose detector is in the tree is not "
                   "unstarted.  Close it, or add a \"state_note\" saying what "
                   "is genuinely left."
                   % (r["id"], m.group(1), len(c), c[0][:72]))

    print("  check_row_states: %d open row(s) checked, %d exempt by state_note"
          % (checked, exempt))
    if bad:
        for b in bad:
            print("  STALE  " + b)
        print("ROW_STATES_FAIL  %d row(s) whose state disagrees with what "
              "shipped" % len(bad))
        return 1
    print("ROW_STATES_PASS  no open row names a committed detector")
    return 0


if __name__ == "__main__":
    sys.exit(main())
