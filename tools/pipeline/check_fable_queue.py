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
    #  *** THIS WAS A RAW SUBSTRING TEST OVER THE WHOLE FILE, AND THE GATE WENT GREEN OVER
    #  EXACTLY THE STATE IT EXISTS TO REDDEN. ***  Found 2026-08-21 by the flagship seat in a
    #  batched regress pass: check_fable_queue printed
    #        ok    sh4pcicexit    regress   owed and queued
    #  while the ONLY occurrence of that id in fable_queue.md was a PARENTHETICAL CROSS-REFERENCE
    #  on line 217, inside a different entry ("...one-instruction kills remain in the same file
    #  (`sh4pcicexit`)").  A MENTION satisfied "named in the queue" -- so the round with the worst
    #  detector prior in this project's history (seven of seven mutants escaped, one reinstating
    #  a host kill) had its regress review silently recorded as owed-and-queued when nothing was
    #  written down at all.
    #
    #  The fix idiom already existed three files away and had already been paid for: gate_offline's
    #  SM/SC manifests match stems EXACTLY in a loop, after being bitten by "a stem that is merely
    #  a prefix of another" (gate_offline.sh:1019-1023).  This is the same genus one directory up.
    #
    #  So an id counts as queued in exactly TWO places, and prose is not one of them:
    #    * it HEADS a hand-written entry -- `### <n>. \`id\`` or `### \`id\``;
    #    * or it appears inside the MACHINE-GENERATED wall block, which is a deliberate
    #      enumeration written by gen_codex_wall.py from the ledger, not commentary.
    #
    #  Scoping to the generated block matters and was not obvious: tightening to headings ALONE
    #  turned 0 unqueued holds into 35, because the bulk of held stages are legitimately carried
    #  by that block rather than by prose entries.  A check that reddens on correct state is as
    #  useless as one that greens on wrong state -- the first draft of this fix did exactly that
    #  for one run, and the 35 are the reason this comment exists.
    _raw = io.open(QUEUE, encoding="utf-8").read() if os.path.exists(QUEUE) else ""
    _BEGIN = "<!-- BEGIN GENERATED: codex-wall"
    _END = "<!-- END GENERATED: codex-wall -->"
    _gen = ""
    if _BEGIN in _raw and _END in _raw:
        _gen = _raw[_raw.index(_BEGIN):_raw.index(_END)]
    queue = set(re.findall(r"^###\s*(?:\d+\.\s*)?`([A-Za-z0-9_]+)`", _raw, re.M))
    queue |= set(re.findall(r"`([A-Za-z0-9_]+)`", _gen))
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
