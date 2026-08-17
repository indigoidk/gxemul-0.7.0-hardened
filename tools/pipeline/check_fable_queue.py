#!/usr/bin/env python3
"""FABLE WORK THAT IS OWED MUST BE QUEUED, NOT MERELY UNDONE.

Owner directive, 2026-08-17: "make sure to gate and queue up any fable work; don't skip it."

Two standing directives make some work only the flagship seat's, so it cannot be reassigned
when its quota is short:

  * `regress` is FABLE-ONLY -- only the flagship seat reviews regression, batched.
  * FULL PANEL ON EVERY STAGE -- Fable is one of the nine, so a stage without it is short.

When Fable is unavailable the honest move is to HOLD the stage and queue the job. The
dishonest move is to let the gap sit silently, and before this check existed there was
nothing between the two: `check_stage_panels.py` reports a HELD stage as waiting, but it
never asked whether anyone had written the job down. **A HELD marker with no queue entry is
a promise nobody recorded**, and it reads on the dashboard exactly like a promise kept.

THREE RULES, each closing a different way to lose the work:

  1. A stage that RAN (two or more seats) and lacks fable5 must carry a HELD marker, or be
     grandfathered. Otherwise it is a stage that simply proceeded without the flagship seat.
  2. Every HELD marker's row must be NAMED IN THE QUEUE FILE. This is the rule the directive
     actually asks for: holding and queueing are one action, not two.
  3. A CLOSED row that changed code and has no `regress` entry owes a regression review. It
     must be named in the queue. A round may not be finished and unreviewed at the same time.

Exit 0 clean, 1 on violations. `--list` shows everything examined.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
#  Overridable so the negative controls can run against COPIES.  A check whose inputs are
#  hardcoded can only be negative-controlled by mutating the real ledger and restoring it --
#  and this project has already had a crashed mutation run leave a tree dirty, with the next
#  run's "original" backup capturing the mutant.  Copies cannot fail that way.
LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
QUEUE = os.environ.get("GXQUEUE") or os.path.join(HERE, "fable_queue.md")

FLAGSHIP = "fable5"
HELD = "[HELD AWAITING SEAT:"
ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"

#  Directive dates.  Work that predates a directive cannot be judged by it.
CUTOFF_FULL_PANEL = "2026-08-16"   # full panel on every stage
CUTOFF_REGRESS_FABLE = "2026-08-15"  # regress becomes flagship-only


def main(argv):
    listing = "--list" in argv
    with open(LEDGER, encoding="utf-8") as f:
        ledger = json.load(f)
    queue = io.open(QUEUE, encoding="utf-8").read() if os.path.exists(QUEUE) else ""
    if not queue:
        print("check_fable_queue: FABLE_QUEUE_FAIL  no queue file at %s" % QUEUE)
        return 1

    short, unqueued_holds, unreviewed = [], [], []
    holds = 0

    for row in ledger["rows"]:
        rid, state = row["id"], row.get("state", "?")
        stages, phases_seen = {}, set()
        for ent in row.get("entries", []):
            ph = ent.get("phase")
            phases_seen.add(ph)
            note = ent.get("note", "")
            d = stages.setdefault(ph, {"seats": set(), "newest": "", "held": False,
                                       "annotated": False})
            if ANNOTATION in note:
                d["annotated"] = True
                continue
            if HELD in note:
                d["held"] = True
                continue
            d["seats"].add(ent.get("seat"))
            d["newest"] = max(d["newest"], ent.get("date", ""))

        for ph, d in stages.items():
            if ph == "regress":
                continue          # flagship-only by directive; rule 3 covers its absence
            if len(d["seats"]) < 2:
                continue          # a one-seat stage is a FILING, not a stage that ran
            if FLAGSHIP in d["seats"] or d["annotated"]:
                continue
            if d["newest"] < CUTOFF_FULL_PANEL:
                continue          # predates the directive
            if d["held"]:
                holds += 1
                if rid not in queue:
                    unqueued_holds.append((rid, ph))
                elif listing:
                    print("  ok    %-14s %-9s HELD and queued" % (rid, ph))
            else:
                short.append((rid, state, ph, len(d["seats"])))

        #  Rule 3: a closed row that changed code owes a regression review.
        if state == "closed" and row.get("commits", "").strip():
            newest = max([e.get("date", "") for e in row.get("entries", [])] or [""])
            if "regress" not in phases_seen and newest >= CUTOFF_REGRESS_FABLE:
                if rid not in queue:
                    unreviewed.append((rid, row.get("commits", "")[:24]))
                elif listing:
                    print("  ok    %-14s regress   owed and queued" % rid)

    bad = len(short) + len(unqueued_holds) + len(unreviewed)
    print("check_fable_queue: %d held-and-queued, %d stages short without a hold, "
          "%d holds not queued, %d closed rows owing a regress review"
          % (holds, len(short), len(unqueued_holds), len(unreviewed)))
    if not bad:
        print("FABLE_QUEUE_PASS  every owed flagship job is either done or written down")
        return 0

    print("FABLE_QUEUE_FAIL")
    for rid, state, ph, n in short:
        print("    %-14s %-8s %-9s ran with %d seats and NO flagship seat, and is not held"
              % (rid, state, ph, n))
    for rid, ph in unqueued_holds:
        print("    %-14s %-9s HELD but NOT NAMED IN THE QUEUE -- a promise nobody recorded"
              % (rid, ph))
    for rid, commits in unreviewed:
        print("    %-14s closed at %s with NO regress entry and not queued" % (rid, commits))
    print()
    print("  Holding a stage and queueing it are ONE action, not two.  Either fire the")
    print("  flagship seat, or add a HELD marker AND name the row in fable_queue.md.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
