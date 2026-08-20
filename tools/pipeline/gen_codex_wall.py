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
**This is ONE outage, not %(n)d decisions, and it is written once rather than once per panel.**
Codex hit its usage limit and is walled to **2026-08-22 12:12**. Across six panels in a single
evening it produced the identical signature every time -- the echoed brief followed by the
usage-limit error -- in files of 26,992 / 11,180 / 10,036 / 8,323 / 12,414 / 11,938 bytes.
*A size check alone scores those as the largest answers in their panels;* `panel.sh`'s seat
check caught each as RATE-LIMITED rather than counting the blank as agreement.

**Every other seat answered every panel.** agy, grok, kimi, glm, deepseek and minimax each
produced a substantive answer on all six. So nothing here is waiting on Codex to be ACTIONABLE
-- it is waiting on Codex to be COMPLETE under the full-panel rule.

**The closures this wall is blocking**, and they are the only real cost: `m8invpred` (DROP,
unanimous), `fbextrate` (DROP, three seats), `sigunsafe` (DROP, two seats), `gcsections` (DROP,
two seats). Each was recommended by the seats that answered and NOT executed, because a drop is
a closure and *"unanimous among the seats that answered"* is how a six-seat verdict gets
reported as a nine-seat one. Section H already refused one such closure tonight, correctly.

**This entry is not about Fable.** The queue is where a held stage is named regardless of which
seat holds it -- the rule section I enforces, and the rule that caught these sitting
held-but-unqueued in the first place.

**Standing authority for proceeding meanwhile:** the owner directed *"if there is anything else
in the matrix that can be ran by any other model other than codex; please proceed"*. Recorded,
never silent.

**Action after 2026-08-22:** re-fire codex against the briefs under `_scratchpad/brief_*.md`,
record its answer on each or record explicitly that it added nothing beyond the confirmed set
-- **a blank cell and a seat failure must not look alike** -- then execute the held drops.
"""


def held_rows(seat="codex"):
    led = json.load(io.open(LEDGER, encoding="utf-8"))
    out = []
    for row in led["rows"]:
        stages = sorted({e.get("phase", "?") for e in row.get("entries", [])
                         if (MARKER.search(e.get("note", "") or "") or [None])
                         and MARKER.search(e.get("note", "") or "")
                         and MARKER.search(e["note"]).group(1).lower() == seat})
        if stages:
            out.append((row["id"], ",".join(stages)))
    return sorted(out)


def block():
    rows = held_rows()
    names = " · ".join("`%s` (%s)" % (rid, st) for rid, st in rows)
    return ("%s\n### THE CODEX WALL -- one outage, %d held stages\n\n%s\n%s\n%s"
            % (BEGIN, len(rows), names, PROSE % {"n": len(rows)}, END))


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
