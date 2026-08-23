#!/usr/bin/env python3
"""Per-seat OUTCOME tracking: was what the seat said actually right?

*** THIS EXISTS BECAUSE THE LEDGER RECORDED PARTICIPATION AND NOTHING ELSE. ***
Asked on 2026-08-22 which seat is most accurate, the honest answer was "the matrix
cannot tell you". It has 1525 entries across nine seats and not one of them records
whether the seat's claim held up.

The obvious substitute is worse than nothing, and was tried first: grep the notes for
a seat's name near "found"/"caught"/"refuted". That produced 63/60/56/55/53/51/49 --
seven seats within twelve points of each other, which is not a measurement of accuracy
but of how often seats are CO-MENTIONED in the same summary note. A note saying "codex
and grok both found X, deepseek was wrong about Y" credits all three and refutes all
three. Any ranking built on it is an artefact of prose style.

So the outcome has to be attached to the ENTRY, which belongs to exactly one seat, and
it has to be written when the claim is CHECKED rather than reconstructed later.

THE GRADES
----------
  UPHELD      the seat's load-bearing claim was checked and held
  REFUTED     checked and found false
  PARTIAL     some of it held, some did not -- outcome_note says which
  UNVERIFIED  NOT CHECKED.  The default, and it is an absence, not a neutral score.

*** UNVERIFIED IS REPORTED, LOUDLY, AND THAT IS THE WHOLE INTEGRITY OF THIS TOOL. ***
If ungraded entries were hidden, the numbers would silently become "of the claims
someone bothered to grade", and people grade the memorable ones -- the dramatic catch
and the embarrassing miss. Coverage is printed beside every rate so a seat with three
graded entries can never look like a champion.

A SECOND AXIS, DELIBERATELY SEPARATE
------------------------------------
`acted` records whether the round DID something because of this entry. It is not the
same as UPHELD: a seat can be entirely correct and find nothing ("no escape found" is
a real result this project asks for), and a seat can be REFUTED and still have changed
the round for the better by forcing the question. Keeping them apart stops "useful"
and "correct" from being conflated, which is exactly what the note-grep did.

usage:  seat_scorecard.py [--ungraded] [ledger.json]
"""
import collections
import io
import json
import os
import sys

GRADES = ("UPHELD", "REFUTED", "PARTIAL", "UNVERIFIED")
HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    return json.load(io.open(path, encoding="utf-8"))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_ungraded = "--ungraded" in sys.argv
    path = args[0] if args else os.path.join(HERE, "ledger.json")
    d = load(path)

    per = collections.defaultdict(collections.Counter)
    acted = collections.Counter()
    ungraded = collections.defaultdict(list)

    for row in d.get("rows", []):
        for e in row.get("entries", []):
            s = e.get("seat", "?")
            g = e.get("outcome", "UNVERIFIED")
            if g not in GRADES:
                g = "UNVERIFIED"
            per[s][g] += 1
            if e.get("acted"):
                acted[s] += 1
            if g == "UNVERIFIED":
                ungraded[s].append("%s/%s" % (row.get("id", "?"), e.get("phase", "?")))

    print("%-12s %6s %7s %8s %8s %8s %9s %7s"
          % ("seat", "total", "graded", "upheld", "refuted", "partial",
             "coverage", "acted"))
    print("-" * 74)

    #  Order by GRADED count, not by any rate.  Sorting by accuracy would put a seat
    #  with 1/1 above one with 40/44, which is the flattery this tool exists to refuse.
    for s in sorted(per, key=lambda k: -(per[k]["UPHELD"] + per[k]["REFUTED"]
                                         + per[k]["PARTIAL"])):
        c = per[s]
        total = sum(c.values())
        graded = total - c["UNVERIFIED"]
        cov = (graded / total * 100) if total else 0.0
        rate = ("%.0f%%" % (c["UPHELD"] / graded * 100)) if graded else "--"
        print("%-12s %6d %7d %8d %8d %8d %8.0f%% %7d   %s"
              % (s, total, graded, c["UPHELD"], c["REFUTED"], c["PARTIAL"],
                 cov, acted[s], ("upheld " + rate) if graded else ""))

    tot = sum(sum(c.values()) for c in per.values())
    gtot = sum(sum(c.values()) - c["UNVERIFIED"] for c in per.values())
    print("-" * 74)
    print("%d entries, %d graded (%.1f%%)" % (tot, gtot, (gtot / tot * 100) if tot else 0))

    if gtot < tot:
        print()
        print("*** %d ENTRIES ARE UNGRADED.  They are an ABSENCE OF EVIDENCE, not a"
              % (tot - gtot))
        print("    neutral score, and no per-seat rate above should be read as that")
        print("    seat's accuracy until coverage is high.  Grade an entry when its")
        print("    claim is CHECKED -- reconstructing grades later reproduces exactly")
        print("    the recall bias this tool replaced. ***")
    if show_ungraded:
        print()
        for s in sorted(ungraded):
            print("  %s ungraded (%d): %s" % (s, len(ungraded[s]),
                                              ", ".join(ungraded[s][:12])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
