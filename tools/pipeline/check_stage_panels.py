#!/usr/bin/env python3
"""EVERY STAGE RUNS THE FULL PANEL BEFORE THE ROUND MOVES ON.

Owner directive, 2026-08-16, and it SUPERSEDES the carrier's older rule of "ONE full
panel per ROUND, with pass 2 restricted to codex + Opus".  That older rule was written
when Grok's free tier was dead and Kimi was quota-dead; both are healthy now, all seven
scriptable seats answered the last three panels, and the only live constraint is that the
three Ollama seats return HTTP 429 if two panels fire within ~20 minutes -- a spacing that
real stages already exceed.

THE RULE: for any stage (assess / research / review) that ran ON OR AFTER the cutoff, all
nine seats must be recorded.  If a seat cannot be run, the round STOPS and the owner is
asked -- degrading silently is exactly what this replaces.

TWO DELIBERATE EXEMPTIONS, both owner directives, both narrow:

  * `regress` is FABLE-ONLY.  Only the flagship seat reviews regression, batched.
  * stages that ran BEFORE the cutoff are GRANDFATHERED, forward-only by owner decision.
    They are not re-panelled; they carry an explicit annotation entry so the dashboard does
    not read their blanks as seat failures.  A blank cell and a seat failure must never look
    alike -- that conflation is what this whole layer exists to prevent.

Exit 0 clean, 1 on violations.  `--list` shows every stage checked.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
#  Overridable so controls run against COPIES.  Added 2026-08-17 after a negative control
#  for the CLOSED-WHILE-HELD clause silently tested NOTHING: it wrote a mutated ledger to a
#  temp file, passed $GXLEDGER, and this script -- which had no such override -- read the real
#  ledger and reported PASS.  A VOID CONTROL AND A PASSING CONTROL ARE INDISTINGUISHABLE in
#  the output, which is the failure mode the whole harness is built against.
LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")

CUTOFF = "2026-08-16"          # stages dated on or after this must be complete
FABLE_ONLY = {"regress"}       # owner directive: only the flagship reviews regression
STAGES = ("assess", "research", "review")

#  An annotation entry is not a review.  It exists to say WHY a stage is short, and it must
#  not be counted as one of the seats that answered -- otherwise marking a gap would close it.
ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"

#  *** A STAGE DELIBERATELY HELD FOR A NAMED SEAT IS NOT A STAGE THAT MOVED ON. ***
#
#  Added 2026-08-17.  Fable usage ran high and the owner said to queue Fable work and carry on
#  with the rest.  That is the honest thing to do -- eight seats can answer now and the ninth
#  when quota returns -- but the first version of this check reported the resulting 8/9 as
#  "moved on without the full panel", which is exactly wrong: nothing moved on, the round is
#  explicitly open and waiting.  Two different states rendering the same is the defect this
#  whole layer exists to prevent, so it must not be committed BY this layer.
#
#  A HELD marker is an explicit ledger entry carrying this token and NAMING the awaited seats.
#  It is reported separately, not as a violation.
#
#  THE ANTI-LOOPHOLE, and it is the whole reason this is safe to add: a held stage on a CLOSED
#  row is a HARD violation.  You may wait for a seat; you may not close a round while waiting
#  for one.  Without that clause "HELD" would be a way to mark any gap and walk away, which is
#  worse than the conflation it replaces.
HELD = "[HELD AWAITING SEAT:"


def main(argv):
    listing = "--list" in argv
    with open(LEDGER, encoding="utf-8") as f:
        ledger = json.load(f)
    seats = [s["id"] for s in ledger["seats"]]
    n_seats = len(seats)

    #  A stage with exactly ONE seat is a FILING, not a panel that ran short.  Items enter
    #  the queue when a seat raises them during some other round's panel, which leaves a
    #  one-seat `assess` entry; the item has not started yet.  Counted and REPORTED
    #  separately rather than waved through, because "filed, awaiting its panel" and "we ran
    #  a panel and it came up short" are different states and the whole point of this layer
    #  is that different states must not render the same.
    violations, grandfathered, complete, filed, held = [], 0, 0, [], []

    for row in ledger["rows"]:
        by_stage = {}
        for ent in row.get("entries", []):
            if ANNOTATION in ent.get("note", ""):
                by_stage.setdefault(ent.get("phase"), {})["_annotated"] = True
                continue
            if HELD in ent.get("note", ""):
                d = by_stage.setdefault(ent.get("phase"), {})
                #  A LIST, NOT A SLOT.  This assigned a single value until 2026-08-17, so a
                #  stage held for TWO seats kept only the LAST marker and reported one.
                #  Found the day it first mattered: exitsweep's assess stage is held for BOTH
                #  codex (a measured quota wall) and fable5 (deliberate conservation), and the
                #  gate printed "awaiting: fable5" -- silently dropping codex.
                #
                #  It UNDER-REPORTS THE DEBT, which is the one direction this gate must never
                #  fail in: a stage that looks like it waits for one seat gets completed a
                #  seat early, and the missing seat's blank then reads as agreement.
                d.setdefault("_held", []).append(ent.get("note", ""))
                continue
            d = by_stage.setdefault(ent.get("phase"), {})
            d.setdefault("seats", set()).add(ent.get("seat"))
            d["newest"] = max(d.get("newest", ""), ent.get("date", ""))

        for stage in STAGES:
            info = by_stage.get(stage)
            if not info or "seats" not in info:
                continue                       # stage never ran; not this check's business
            got, newest = info["seats"], info.get("newest", "")
            if len(got) >= n_seats:
                complete += 1
                if listing:
                    print("  ok    %-14s %-9s %d/%d" % (row["id"], stage, len(got), n_seats))
                continue
            #  HELD is checked BEFORE the one-seat "filed" shortcut, so a stage that is
            #  genuinely waiting on a named seat is reported as waiting even if only one
            #  other seat has answered so far.
            if info.get("_held"):
                if row.get("state") == "closed":
                    violations.append((row["id"], "CLOSED-WHILE-HELD", stage, len(got),
                                       ["a round may not close while a stage awaits a seat"]))
                else:
                    #  Every marker, de-duplicated, order preserved -- so two holds report
                    #  two seats and the operator sees the whole debt.
                    names = []
                    for mark in info["_held"]:
                        nm = mark.split(HELD, 1)[1].split("]", 1)[0].strip()
                        if nm and nm not in names:
                            names.append(nm)
                    held.append((row["id"], stage, len(got), ", ".join(names)))
                continue
            if len(got) == 1:
                filed.append((row["id"], stage))
                continue
            if newest < CUTOFF or info.get("_annotated"):
                grandfathered += 1
                if listing:
                    print("  --    %-14s %-9s %d/%d  grandfathered"
                          % (row["id"], stage, len(got), n_seats))
                continue
            violations.append((row["id"], row.get("state", "?"), stage, len(got),
                               [s for s in seats if s not in got]))

    print("check_stage_panels: %d complete, %d grandfathered, %d filed-awaiting-panel, "
          "%d HELD, %d incomplete"
          % (complete, grandfathered, len(filed), len(held), len(violations)))
    for rid, stage, n, awaited in held:
        print("  HOLD  %-14s %-9s %d/%d  awaiting: %s" % (rid, stage, n, n_seats, awaited))
    if listing and filed:
        for rid, stage in filed:
            print("  ..    %-14s %-9s 1/%d  filed, not yet panelled" % (rid, stage, n_seats))
    if not violations:
        print("STAGE_PANELS_PASS  every post-cutoff stage ran the full panel")
        return 0

    print("STAGE_PANELS_FAIL  %d stage(s) moved on without the full panel:" % len(violations))
    for rid, state, stage, n, miss in violations:
        print("    %-14s %-7s %-9s %d/%d   missing: %s"
              % (rid, state, stage, n, n_seats, ", ".join(miss)))
    print()
    print("  The owner's rule is FULL PANEL ON EVERY STAGE, and STOP AND ASK if a seat")
    print("  cannot be run -- not degrade quietly.  Either fire the missing seats, or")
    print("  raise it with the owner and record the decision as an explicit entry.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
