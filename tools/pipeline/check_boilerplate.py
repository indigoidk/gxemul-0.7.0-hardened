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
falls back to a prefix comparison, because that is what actually varies.

Exit 1 if any row has one note shared by >= MIN_SEATS seats.  Not part of the hard gate yet
(existing rows are grandfathered by GRANDFATHERED below) -- it names them so the harvest is
fixed rather than repeated.
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
PREFIX = 60              # compare this many chars once the seat name is gone

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
            buckets[strip_seat(note, seat)[:PREFIX]].add((seat, e.get("date") or ""))
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
        print("                          %s..." % key[:72])

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
