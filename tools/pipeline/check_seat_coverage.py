#!/usr/bin/env python3
"""PER-SEAT COVERAGE: for every seat, how many of its answers on disk are in the ledger?

*** WHY THIS EXISTS: THE OWNER ASKED "IS DEEPSEEK MISSING?" FIVE TIMES. ***

Each time, answering it took a bespoke script, and the first cut of that script produced an
alarming and MISLEADING number: "82 deepseek answers on disk, 17 recorded, 65 unrecorded".
The 65 were not dropped reviews. They sat in panel directories that NO ledger entry cites at
all -- panels that predate the ledger, where no seat of any kind is recorded. Counting them as
deepseek's problem confused "the ledger did not exist yet" with "this seat's review was lost".

So the report separates the three outcomes, because they need three different responses:

  RECORDED      the answer is in the ledger. Nothing owed.
  PRE-LEDGER    the answer sits in a dir NO entry cites. Not this seat's gap -- the whole
                panel predates the ledger. Owed nothing, and must not be reported as a loss.
  *** GAP ***   the dir IS cited, for OTHER seats, but not for this one. THE ONLY ACTIONABLE
                CLASS: a real review sitting unread while the round reads as reviewed.

It complements `check_seats_read.py` rather than duplicating it. That check asks "did any seat
answer in a cited dir and go unrecorded" and fails the commit if so. This one reports the same
question PER SEAT, plus the pre-ledger denominator -- so "is seat X being dropped?" is one
command with a number, instead of a five-minute audit that can be got wrong.

A sub-threshold file is NEVER an answer: ~55 bytes is an Ollama 429, ~136 is a thinking-model
stall on a brief that told it to read files, ~328 is a quota error page. Each is a SEAT
FAILURE, which must be recorded by name -- a blank cell and a seat failure must not look alike.

Usage:
    python check_seat_coverage.py            # table for every seat
    python check_seat_coverage.py deepseek   # one seat, with every file listed
Exit 1 if any seat has a GAP.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
PANELS = os.environ.get("GXPANELS") or os.path.normpath(
    os.path.join(HERE, "..", "..", "..", "_scratchpad"))

#  Output filename prefix per seat id.  The Ollama seats are written by panel_ollama.py under
#  ollama_<model>.txt; the CLI seats use their own name.
PREFIX = {
    "codex": "codex", "agy": "agy", "kimi": "kimi", "grok": "grok",
    "glm": "ollama_glm", "deepseek": "ollama_deepseek", "minimax": "ollama_minimax",
}
MIN_ANSWER = 800


def main(argv):
    only = argv[0] if argv and not argv[0].startswith("-") else None
    ledger = json.load(io.open(LEDGER, encoding="utf-8"))

    cited = {}
    for row in ledger["rows"]:
        for ent in row.get("entries", []):
            blob = json.dumps(ent)
            for m in re.finditer(r"panel_\d{8}_\d{6}", blob):
                cited.setdefault(m.group(0), set()).add(ent.get("seat"))

    if not os.path.isdir(PANELS):
        print("check_seat_coverage: no panel directory at %s" % PANELS)
        return 0
    dirs = sorted(d for d in os.listdir(PANELS)
                  if d.startswith("panel_") and os.path.isdir(os.path.join(PANELS, d)))

    print("check_seat_coverage: %d panel dirs on disk, %d cited by the ledger"
          % (len(dirs), len(cited)))
    print()
    print("  %-10s %8s %9s %11s %6s %s"
          % ("seat", "answers", "recorded", "pre-ledger", "GAP", "sub-threshold (seat failures)"))
    print("  " + "-" * 74)

    total_gap = 0
    for seat in sorted(PREFIX):
        if only and seat != only:
            continue
        pfx = PREFIX[seat]
        rec = pre = gap = small = 0
        detail = []
        for d in dirs:
            p = os.path.join(PANELS, d)
            files = [f for f in sorted(os.listdir(p))
                     if f.startswith(pfx) and f.endswith(".txt")]
            for f in files:
                sz = os.path.getsize(os.path.join(p, f))
                if sz < MIN_ANSWER:
                    small += 1
                    detail.append((d, f, sz, "sub-threshold"))
                    continue
                seats = cited.get(d)
                if not seats:
                    pre += 1
                    detail.append((d, f, sz, "pre-ledger"))
                elif seat in seats:
                    rec += 1
                    detail.append((d, f, sz, "recorded"))
                else:
                    gap += 1
                    detail.append((d, f, sz, "*** GAP ***"))
        total_gap += gap
        print("  %-10s %8d %9d %11d %6d %s"
              % (seat, rec + pre + gap, rec, pre, gap, small if small else "-"))
        if only:
            print()
            for d, f, sz, state in detail:
                print("      %-22s %-24s %8d  %s" % (d, f, sz, state))

    print()
    if total_gap:
        print("SEAT_COVERAGE_FAIL  %d answer(s) sit in a CITED panel dir and are recorded "
              "nowhere." % total_gap)
        print("  Read them and add a ledger entry.  If a seat truly had nothing to say, record")
        print("  THAT explicitly -- a blank cell and a seat failure must not look alike.")
        return 1
    print("SEAT_COVERAGE_PASS  every answer in a cited panel dir is recorded for its seat.")
    print("  'pre-ledger' answers are owed nothing: no seat is recorded for those dirs, so they")
    print("  are the ledger's own start date and NOT a dropped review for any seat.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
