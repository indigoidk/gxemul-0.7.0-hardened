#!/usr/bin/env python3
"""Find ledger entries where several seats carry the SAME harvested note.

*** THE LEDGER CAN MANUFACTURE AGREEMENT, AND IT HAS. ***  Found 2026-08-20 by a reviewing
seat looking at `wdcnoirq`: five seats (agy, grok, kimi, deepseek, minimax) carried notes
that differ ONLY in the leading seat name --

    "agy answered this cluster panel. ROUND B, with wdcstandby. The seats were clear ..."
    "grok answered this cluster panel. ROUND B, with wdcstandby. The seats were clear ..."

378, 379, 379, 383 and 382 bytes.  Three of those seats had actually ARGUED IN THEIR OWN
FILES THAT ROUND B WAS TOO NARROW, and deepseek's 5.3 KB answer never mentions the opcode
at issue at all -- yet the record shows five seats concurring with the narrow scope.

Under the PIPELINE doctrine the ledger is the single source of truth.  A harvest that stamps
one summary across every seat's cell does not merely lose detail: it converts "six seats
answered" into "six seats agreed", which is the exact claim the panel exists to earn.  It is
the SEAT-COUNT analogue of the padded-column grep trap -- the number looks right and means
nothing.

*** AND THE FIRST CHECK I WROTE FOR THIS REPORTED GREEN. ***  It hashed the note text, so a
four-character seat-name prefix made five identical paragraphs into five distinct hashes.
Blindness reported as a green line, in the verification of a finding about blindness being
reported as a green line.  Hence: this compares notes with the seat's own name STRIPPED, and
compares the WHOLE note -- it compared a 60-character prefix until 2026-09-17, and the note
at EXCERPT below says what that cost.

Exit 1 if any row has one note shared by >= MIN_SEATS seats harvested after CUTOFF.  Part of
the HARD gate: precommit_check.sh section O fails the commit on BOILERPLATE_FAIL (this header
said "not part of the hard gate yet" until 2026-10-02).  Clusters on or before CUTOFF are
reported, not failed -- see FORWARD-ONLY BY DATE below -- so the harvest is fixed rather than
repeated.
"""
import collections
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "ledger.json")

MIN_SEATS = 3            # two seats sharing a line is a summary; three is a pattern
EXCERPT = 60             # DISPLAY width only -- see below; NOT the comparison key

#  *** THE KEY WAS `note[:60]` AND IT MADE 20 OF 64 CLUSTERS FALSE POSITIVES.
#  Measured 2026-09-17 over every cluster in the ledger; owner-decided the same day. ***
#
#  A 60-character key compares the OPENING SENTENCE, not the note.  Cells that carry
#  each seat's own finding but share an identifying preamble -- `LATE REVIEW of the six
#  rows the seat audit flagged (panel panel_20260917_100431).` is 81 characters before
#  the first seat writes a word (this said 66 until 2026-10-02) -- clustered as boilerplate while satisfying this
#  check's own stated rule, which asks for "each seat its own sentence from its own
#  file".  They HAD their own sentence; the key could not see past the preamble.
#
#  MEASURED over every cluster in the ledger, both keys, same run:
#      OLD  note[:60]   64 clusters   44 genuine   20 NOTES DIFFER (false positives)
#      NEW  full note   54 clusters   54 genuine    0 notes differ
#
#  *** THE OLD KEY FAILED IN BOTH DIRECTIONS, AND THE SECOND HALF IS THE SURPRISE. ***
#  The false positives were expected: 7 of the 20 were LIVE, each with SEVEN genuinely
#  distinct notes sharing only a preamble.  But GENUINE STAMPS ALSO ROSE, 44 -> 54,
#  because a 60-character bucket holding a real stamp ALONGSIDE other notes scored as
#  one MIXED cluster -- so the prefix key reported ten real stamps as parts of mixed
#  buckets, where a reader could not tell them from the false positives.  Truncation
#  cost precision and made those ten illegible; it never bought either.
#
#  THE COST, stated because it is real: boilerplate that shares 500 characters and
#  differs only in a trailing clause is no longer caught.  NO INSTANCE OF THAT SHAPE
#  EXISTS in the 64 measured, and if one appears the answer is a similarity threshold,
#  not a return to a fixed prefix.
#
#  CONTROLLED IN BOTH DIRECTIONS on the day it was written (2026-09-17): BOILERPLATE_PASS
#  with the seven live false positives gone; an INJECTED identical paragraph across four
#  seat cells post-cutoff turns it red and names the row; removing the injection restores
#  green.  The edit then sat UNCOMMITTED in a working tree for fifteen days while the row
#  `boilerplateprefix` read closed (found by a census, 2026-10-02); the controls were
#  re-run on the day it was committed:
#  regress/artifacts/closeassess_20261002/draft/boilerplate_controls_20261002.out.
#
#  *A caution for the next reader, because it cost a wrong number here first:*
#  *`shared_notes` returns its key with newlines replaced by spaces FOR DISPLAY.  A*
#  *verification harness that compares a recomputed key against the RETURNED one*
#  *silently matches nothing for any note containing a newline, and then reports the*
#  *cluster as non-identical.  Recompute the bucket, do not compare against the key.*

#  *** FORWARD-ONLY BY DATE, NOT BY ROW, AND THE MEASUREMENT IS WHY. ***  The first draft
#  grandfathered six named rows, because six is what the reporting seat had found.  Running
#  it returned FIFTY-TWO -- essentially every cluster-panel row in the ledger carries one
#  summary stamped across five seat cells.  That is not a handful of sloppy harvests; it is
#  how cluster panels have been recorded throughout, and a per-row allowlist at that scale is
#  the check switched off with extra steps.
#
#  So: everything on or before CUTOFF is REPORTED and not failed; anything after it must give
#  each seat its own sentence.  A rule that retro-fails the archive gets disabled, and a
#  disabled rule is worse than no rule.
CUTOFF = "2026-08-20"


def strip_seat(note, seat):
    """Remove the seat's own name so identical text stops looking distinct."""
    n = re.sub(r"^\s*%s\b[^.]*\.\s*" % re.escape(seat), "", note, count=1, flags=re.I)
    return re.sub(r"\b%s\b" % re.escape(seat), "<seat>", n, flags=re.I).strip()


def shared_notes(rows):
    """[(row_id, [seats], excerpt)] for notes >= MIN_SEATS seats share."""
    out = []
    for rid, row in sorted(rows.items()):
        buckets = collections.defaultdict(set)
        for e in row.get("entries", []):
            note, seat = e.get("note") or "", e.get("seat") or "?"
            if len(note) < 80:
                continue                      # too short to carry a claim either way
            buckets[strip_seat(note, seat).casefold()].add((seat, e.get("date") or ""))
        for key, pairs in buckets.items():
            seats = sorted({s for s, _ in pairs})
            if len(seats) >= MIN_SEATS:
                #  A cluster is LIVE only if every entry in it postdates the cutoff. One old
                #  entry means this is an archived harvest being extended, not a new one
                #  being written badly.
                live = all(dt > CUTOFF for _, dt in pairs if dt)
                out.append((rid, seats, key.replace("\n", " "), live))
    return out


def main(argv):
    ledger = json.load(io.open(LEDGER, encoding="utf-8"))
    rows = {r["id"]: r for r in ledger["rows"]}
    found = shared_notes(rows)
    live = [f for f in found if f[3]]

    for rid, seats, key, is_live in found:
        tag = "SHARED" if is_live else "ARCHIVED"
        print("  %-9s %-13s x%d  %s" % (tag, rid, len(seats), ",".join(seats)))
        print("                          %s..." % key[:EXCERPT])

    print()
    print("  A note shared verbatim by several seats records that they were FIRED, not that")
    print("  they AGREED. Give each seat its own sentence from its own file, or leave the")
    print("  cell empty -- an empty cell is honest and a copied one is not.")
    print()
    if live:
        print("BOILERPLATE_FAIL  %d cluster(s) harvested after %s" % (len(live), CUTOFF))
        return 1
    print("BOILERPLATE_PASS  %d archived (on/before %s), 0 new" % (len(found), CUTOFF))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
