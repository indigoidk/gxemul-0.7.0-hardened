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

#  ---- HOLD QUESTIONS -----------------------------------------------------------------
#  A STAGE HELD *FOR* A SEAT MUST CARRY THE QUESTION IT IS HELD FOR.  That rule has been in
#  CLAUDE.md since a 46-row batch measured it: the three meta-rows carrying identical
#  boilerplate had their question RECONSTRUCTED from the row's subject, while the two that
#  named it explicitly were the easiest to answer *accurately*.
#
#  *** IT WAS AT 0 FOR 18 ON 2026-08-26. ***  Every held stage in the ledger carried a
#  DISPOSITION note where a question belongs -- "FILE - no measurable effect until a caller
#  survives", "a policy, not a round".  Each is a true statement about the row.  None is a
#  question a seat can answer.
#
#  This is the carrier diagnosing itself: the rule was PROSE in an auto-loaded file, it was
#  known, and it still did not fire.  A seat given a disposition note must GUESS what it is
#  being asked, and a guessed question yields an answer to the wrong question that still
#  LOOKS like a discharged stage -- the seat-failure-counted-as-agreement shape, moved one
#  step earlier.
#
#  DATED CUTOFF, owner decision 2026-08-26, and the same shape check_bugfile_sync.py uses:
#  stages whose newest entry is on or before HOLDQ_CUTOFF are REPORTED and not failed.  A
#  rule that retro-fails 18 pre-existing rows blocks the next commit on reconstruction work
#  nobody scheduled, and a rule that does that gets switched off.  New holds are enforced.
HOLDQ_CUTOFF = "2026-08-26"
FABLE_ONLY = {"regress"}       # owner directive: only the flagship reviews regression
STAGES = ("assess", "research", "review")

#  An annotation entry is not a review.  It exists to say WHY a stage is short, and it must
#  not be counted as one of the seats that answered -- otherwise marking a gap would close it.
ANNOTATION = "[RUN UNDER THE PRE-2026-08-16 POLICY]"

#  A SECOND, DIFFERENT EXEMPTION, and it is deliberately not folded into the first.
#
#  The token above asserts a specific historical fact: the stage ran before the full-panel
#  directive.  On 2026-08-21 a batched flagship pass added a single entry to a row that had been
#  FILED with one seat -- and one filing plus one re-read is counted here as a TWO-OF-NINE STAGE,
#  so section H reddened for a row nobody had convened a panel on.
#
#  *** THE FIRST ATTEMPT AT CLEARING THAT USED THE TOKEN ABOVE, WHICH WOULD HAVE PUT A FALSE
#  STATEMENT IN THE LEDGER TO TURN A GATE GREEN. ***  A 2026-08-21 re-read did not run under the
#  pre-2026-08-16 policy.  Backed out; the honest fix is a token that says what actually
#  happened, because the two situations are not the same and a reader must be able to tell them
#  apart.
#
#  This is a real recurring category rather than a one-off: any pass that sweeps filed rows can
#  promote a filing into a short stage without anyone deciding to.
RE_READ = "[NOT A PANEL STAGE: SINGLE-SEAT RE-READ]"

#  A THIRD EXEMPTION, 2026-09-18, and like the second it exists because neither older token was
#  TRUE of the situation -- which is the only reason this file ever gains a token.
#
#  A session read 23 UNREAD SEAT ANSWERS off disk and recorded each onto the row it discussed.
#  That is strictly an improvement to the record: this project has three times found real
#  defects sitting in an unread review.  **It took both stage gates from GREEN to RED, creating
#  19 violations where HEAD had zero** -- because recording a seat's remark about row X makes
#  row X's stage go from ABSENT (or a 1-seat filing) to a 2..8-seat "short panel", and a short
#  panel is what this check reddens on.
#
#  *** SO THE GATE FIRED BECAUSE THE RECORD GOT MORE HONEST, AND THE ONLY WAY TO GREEN IT WITH
#  THE OLDER TOKENS WOULD HAVE BEEN TO WRITE A FALSE SENTENCE INTO THE LEDGER. ***  RE_READ says
#  SINGLE-SEAT, and several of these carry 2, 3, 4, 6 and even 8 recorded seats; ANNOTATION
#  asserts a pre-2026-08-16 vintage that is simply untrue of a 2026-09-17 entry.  The comment on
#  RE_READ already records the last time someone reached for the nearest token to turn a gate
#  green, and that attempt was backed out.  This is that lesson obeyed rather than re-learned.
#
#  THE DISCRIMINATOR, and it is mechanical rather than a judgement call: read the `ev` field for
#  the panel dir, open that dir's `brief_sent.md`, and ask **WAS THIS PANEL CONVENED ON THIS
#  ROW?**  If the brief's subject is this row (or a deliberate multi-row late review naming it),
#  the stage RAN and this token is a lie.  If the brief is about some other row and a seat merely
#  mentioned this one in passing, no panel was ever convened here.
#
#  *** THAT TEST OVERTURNED THE AUTHOR'S FIRST SORTING, WHICH IS WHY IT IS WRITTEN DOWN AS A
#  COMMAND AND NOT AS ADVICE. ***  Seat COUNT was used first -- "+8 seats must mean a real panel"
#  -- and it was wrong three times over: `diskimagesign`, `pcc2c040assertrow` and
#  `pcc2genctlc040alias` all cite ONE dir, `panel_20260917_100431`, whose brief IS convened on
#  them, so they are real stages; while `asiceventaddr` carries a full EIGHT recorded seats that
#  all cite `panel_20260826_222557`, a pass 2 on a COMMENT-ONLY commit to a vendored header --
#  a different subject entirely, and therefore not a stage at all.  **The count is a CORRELATE
#  of "a panel ran"; the brief's subject is the thing itself.
#
#  *** THE TOKEN STATES THE GENERAL CLAIM AND THE NOTE CARRIES THE SPECIFIC REASON, WHICH IS A
#  DELIBERATE BREAK FROM THE TWO TOKENS ABOVE. ***  Those bake their reason into the literal,
#  and that is exactly what made RE_READ unusable here -- it says SINGLE-SEAT, so a true
#  situation with three seats had no token that fitted.  A first draft of THIS token repeated
#  the mistake: it read INCIDENTAL SEAT MENTION, which is true of eleven of the twelve stages
#  and FALSE of `ip30abortkill' assess, whose two entries are a rung-3 WITNESS BUILD and a
#  ship-order ADJUDICATION -- real work on that very row, and not a panel seat answer at all.
#  The checkable claim both gates need is only ever "no panel was convened on this stage";
#  everything else is provenance, and provenance belongs in prose a reader can check.**
NOPANEL = "[NOT A PANEL STAGE: NO PANEL CONVENED]"

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
            if (ANNOTATION in ent.get("note", "") or RE_READ in ent.get("note", "")
                    or NOPANEL in ent.get("note", "")):
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
                    held.append((row["id"], stage, len(got), ", ".join(names),
                                     newest, (row.get("hold_question") or "").strip()))
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
    noq_new, noq_old = [], []
    for rid, stage, n, awaited, newest, question in held:
        print("  HOLD  %-14s %-9s %d/%d  awaiting: %s" % (rid, stage, n, n_seats, awaited))
        if question:
            continue
        #  Report by DATE, not by count: "18 rows lack a question" is a backlog, while
        #  "this stage was held today and names no question" is an actionable defect.
        (noq_new if newest > HOLDQ_CUTOFF else noq_old).append((rid, stage, awaited, newest))
        print("        *** NO hold_question -- %s ***"
              % ("FAIL, held after %s" % HOLDQ_CUTOFF if newest > HOLDQ_CUTOFF
                 else "warn, held on/before %s" % HOLDQ_CUTOFF))
    if noq_old:
        print("  %d held stage(s) name no question and predate %s -- reported, not failed."
              % (len(noq_old), HOLDQ_CUTOFF))
        print("  They are real debt: a seat fired against a disposition note has to guess")
        print("  the question, and a guessed question still looks like a discharged stage.")
    if listing and filed:
        for rid, stage in filed:
            print("  ..    %-14s %-9s 1/%d  filed, not yet panelled" % (rid, stage, n_seats))
    if not violations and not noq_new:
        print("STAGE_PANELS_PASS  every post-cutoff stage ran the full panel")
        return 0

    if noq_new:
        print("STAGE_PANELS_FAIL  %d held stage(s) name no question:" % len(noq_new))
        for rid, stage, awaited, newest in noq_new:
            print("    %-14s %-9s held %s for %s -- no hold_question"
                  % (rid, stage, newest, awaited))
        print()
        print("  Put the question the seat is being asked in the row's `hold_question`")
        print("  field.  Not the disposition -- the QUESTION.  'FILE - a design change'")
        print("  tells a seat nothing it can answer.")
        if not violations:
            return 1

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
