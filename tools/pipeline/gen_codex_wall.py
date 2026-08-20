#!/usr/bin/env python3
"""Regenerate the CODEX WALL section of fable_queue.md FROM THE LEDGER.

WHY: section I of `precommit_check.sh` requires that every `[HELD AWAITING SEAT: ...]` marker
is also NAMED IN THE QUEUE -- "holding a stage and queueing it are ONE action, not two."  That
is the right rule, and it fired three times in one evening because the list was maintained BY
HAND: each new panel added held markers, and the queue entry had to be edited to match.

A hand-maintained list of machine-readable facts is a list that goes stale, and this project
has the receipts: `RESUME.md` went stale for 26 rounds, the SEAT LEDGER for five days, the
`gate_offline.sh` floor comment said "16 -> 17" while the code read 18.  The queue entry was
about to join them.

So the section is DERIVED.  Run this after recording a panel; it rewrites exactly the block
between the two markers below and touches nothing else in the file.

    python tools/pipeline/gen_codex_wall.py          rewrite the section
    python tools/pipeline/gen_codex_wall.py --check  exit 1 if the file is out of date

WHAT IT DELIBERATELY DOES NOT DO: it does not invent the prose.  The narrative paragraphs --
why the wall is one outage, what it blocks, the standing authority to proceed -- are written by
a human and live INSIDE the generated block as a constant here, because they are judgement.
Only the ROW LIST and the COUNT are derived.  A generator that wrote the reasoning too would be
a generator nobody reads.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "ledger.json")
QUEUE = os.path.join(HERE, "fable_queue.md")

BEGIN = "<!-- BEGIN GENERATED: codex-wall -- edit gen_codex_wall.py, not this block -->"
END = "<!-- END GENERATED: codex-wall -->"
MARKER = re.compile(r"\[HELD AWAITING SEAT:\s*([a-z0-9_]+)\s*\]", re.I)

PROSE = """
*** TWO DIFFERENT KINDS OF HOLD APPEAR BELOW AND THEY MUST NOT BE READ ALIKE. ***

* **codex** -- a genuine OUTAGE, now DISCHARGED. It hit its usage limit and echoed eleven
  briefs; on 2026-08-20 it answered a health test and all eleven were re-fired against
  byte-identical briefs and verified real. Only the older 08-17/08-18 panels remain.
* **opus5 / fable5** -- NOT an outage. Both are alive and answering. They are held by an
  **owner allocation**: Opus DRIVES (implementing rounds) and Fable ADJUDICATES (it delivered
  the drop docket), with Fable deprioritised as a review seat. The nine cluster panels fired
  panel.sh's seven scriptable seats only, so those assess stages are 7/9 or 8/9.

**That second kind surfaced only when the first was discharged**: with a codex marker present
each stage read HELD and was accepted, and removing it revealed the true count. *One held
marker can mask another gap* -- section H cannot see a shortfall that a different hold covers.

**Neither kind is a blank.** A blank cell and a seat failure must not look alike, and an
allocation is a third thing again: recorded by seat name, per row, with the reason.

**This is ONE outage plus one allocation, not %(n)d decisions, and it is written once rather than once per panel.**
**THE CODEX HISTORY, kept because it calibrates what a wall looks like.** Across ten panels it
produced the identical signature every time -- the echoed brief followed by the usage-limit
error -- in files of 26,992 / 11,180 / 10,036 / 8,323 / 12,414 / 11,938 / 10,726 / 16,694 /
19,649 / 21,348 bytes. *A size check alone scores those as the largest answers in their panels.*
`panel.sh`'s seat check caught each as RATE-LIMITED rather than counting the blank as agreement,
and the discharge re-verified every rerun the same way: delta over the brief, and the absence of
the usage-limit string in the tail.

**A DISCHARGED CODEX FINDING IS HISTORICAL UNLESS RE-CHECKED.** Each rerun answered the brief AS
IT WAS FIRED -- byte-identical, so its answer is comparable with the seats that answered live --
and the tree has moved since. Measured example: its rtcdet verdict was DEFECTIVE on a `+1`
mutant that "admits UINT64_MAX while all nine rows remain green" -- correct against the 9-row
table it was shown, and MEASURED CLOSED against today's 18-row table. Three further codex
recommendations are already settled by measurements on the record (`tfreq` is fixed;
`mrwstore2`'s "produce a real-guest witness" was measured impossible; `constblind`'s drop was
rejected after a live instance was found).

**Action for the remaining rows:** the older 08-17/08-18 panels (`exitsweep`, `ovsync`,
`armbdt`, `b118L`, `b120r`, `dfreq`, `reprowitness`) were NOT re-fired and still carry genuine
codex holds. For `opus5`/`fable5`, fire them against the cluster briefs when the owner's
allocation frees them. **A blank cell, a seat failure and an allocation are three different
things and this file names which is which.**
"""


def held_rows(seat=None):
    """Rows carrying a [HELD AWAITING SEAT: x] marker.  seat=None means ANY seat.

    It used to default to "codex" and callers never passed anything else.  That was fine while
    codex was the only walled seat and WRONG the moment a second one was held: opus5 and fable5
    went held by owner allocation, section I went red naming 54 rows, and the generator that
    exists to keep that list current could not see any of them."""
    led = json.load(io.open(LEDGER, encoding="utf-8"))
    out = []
    for row in led["rows"]:
        stages = {}
        for e in row.get("entries", []):
            m = MARKER.search(e.get("note", "") or "")
            if not m:
                continue
            s = m.group(1).lower()
            if seat and s != seat:
                continue
            stages.setdefault(e.get("phase", "?"), set()).add(s)
        if stages:
            out.append((row["id"],
                        "; ".join("%s:%s" % (ph, ",".join(sorted(v)))
                                  for ph, v in sorted(stages.items()))))
    return sorted(out)


def block():
    rows = held_rows()
    names = " · ".join("`%s` (%s)" % (rid, st) for rid, st in rows)
    return ("%s\n### HELD STAGES -- every row awaiting a seat, derived from the ledger\n\n%s\n%s\n%s"
            % (BEGIN, names, PROSE % {"n": len(rows)}, END))


def main(argv):
    cur = io.open(QUEUE, encoding="utf-8", newline="").read()
    new_block = block()
    if BEGIN in cur and END in cur:
        i, j = cur.index(BEGIN), cur.index(END) + len(END)
        new = cur[:i] + new_block + cur[j:]
    else:
        anchor = "## QUEUED — in priority order\n"
        if anchor not in cur:
            print("gen_codex_wall: anchor heading not found in %s" % QUEUE)
            return 2
        new = cur.replace(anchor, anchor + "\n" + new_block + "\n", 1)

    if "--check" in argv:
        if new != cur:
            print("CODEX_WALL_STALE  fable_queue.md does not match the ledger; re-run without --check")
            return 1
        print("CODEX_WALL_OK  %d held stages, section matches the ledger" % len(held_rows()))
        return 0

    io.open(QUEUE, "w", encoding="utf-8", newline="").write(new)
    print("rewrote the CODEX WALL section: %d held stages" % len(held_rows()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
