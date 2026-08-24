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
import collections
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

#  *** A CITATION THAT STILL RESOLVES CAN STILL BE WRONG, AND THE WEAK TEST
#  MISSES IT ENTIRELY. ***  Two stale ledger citations were found on the same
#  day; NEITHER pointed past end-of-file.  `sh4pcic15` cited dev_sh4.c:2822-2836
#  for interrupt wiring that had moved to :2951-2967, leaving the old range
#  pointing at a default arm's fatal() block; `sh4itlbpr` cited :999-1001 for a
#  PR-mask reuse now at :1020-1021, leaving the old range on translation-cache
#  invalidation.  A past-EOF sweep over all 447 ledger citations found ZERO.
#
#  The checkable proxy is not the line, it is the FILE'S AGE against the note's:
#  a citation into a file committed AFTER the entry was written may have drifted.
#  Measured before shipping, because a noisy check gets ignored: across all OPEN
#  rows that is 17 citations and ONE flag, which was a true positive.
#
#  SOFT by design.  Drift is likely, not certain -- an edit below the cited line
#  moves nothing -- so this prints a note and does not fail.  The carrier's rule
#  stands and cannot be mechanised: READ THE LINE BEFORE CITING IT.
CITE = re.compile(r"\b([a-z0-9_]+\.(?:c|h|py|sh)):(\d+)")


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

    #  the soft citation-drift pass, over OPEN rows only -- those are the ones a
    #  future round navigates by
    index = {}
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x != ".git"]
        for f in files:
            index.setdefault(f, os.path.join(root, f))
    seen_mod, drift = {}, collections.Counter()
    for r in d["rows"]:
        if r.get("state") != "open":
            continue
        for e in r.get("entries", []):
            when = e.get("date", "")
            for m in CITE.finditer(e.get("note", "")):
                p = index.get(m.group(1))
                if not p or not when:
                    continue
                if p not in seen_mod:
                    seen_mod[p] = subprocess.run(
                        ["git", "-C", ROOT, "log", "-1", "--format=%ad",
                         "--date=short", "--", p], capture_output=True,
                        text=True, encoding="utf-8").stdout.strip()
                if not (seen_mod[p] and seen_mod[p] > when):
                    continue
                #  *** AND IT MUST BE DISCHARGEABLE, OR IT CRIES WOLF
                #  FOREVER. ***  Correcting a citation does not change the
                #  entry's DATE, so the first version kept flagging a row
                #  whose citation had just been re-derived -- a permanent
                #  note is one nobody reads, which is the failure mode
                #  check_score_claims already warns about.
                #
                #  A note that says it was RE-DERIVED on or after the
                #  file's last commit has already done the work this
                #  check asks for, and says so where a reader sees it.
                note = e.get("note", "")
                if "re-derived" in note.lower():
                    stamps = re.findall(r"\d{4}-\d{2}-\d{2}", note)
                    if any(x >= seen_mod[p] for x in stamps):
                        continue
                drift[(r["id"], m.group(1), seen_mod[p], when)] += 1
    for (rid, f, mod, when), cnt in sorted(drift.items()):
        print("  note  %s cites %s %d time(s) in a note dated %s; that file was"
              " last committed %s -- RE-DERIVE the line before trusting it"
              % (rid, f, cnt, when, mod))

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
