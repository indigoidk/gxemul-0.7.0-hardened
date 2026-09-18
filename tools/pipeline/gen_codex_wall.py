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
#  GXLEDGER / GXQUEUE (#534): the stage-token controls run this against a FIXTURE, as they do the checkers.
LEDGER = os.environ.get("GXLEDGER") or os.path.join(HERE, "ledger.json")
QUEUE = os.environ.get("GXQUEUE") or os.path.join(HERE, "fable_queue.md")

BEGIN = "<!-- BEGIN GENERATED: codex-wall -- edit gen_codex_wall.py, not this block -->"
END = "<!-- END GENERATED: codex-wall -->"
#  *** THE CLASS CARRIES A COMMA, AND THAT IS THE WHOLE FIX (`holdmarkermulti`). ***
#  It was `[a-z0-9_]+` -- ONE seat name -- so a marker naming several seats failed to
#  match and the stage was neither counted here nor required by section I to appear in
#  the queue.  The enforcement was strongest on the SMALLEST holds and absent on the
#  biggest: `sgirekills` is held awaiting all seven scriptable seats and was reported
#  nowhere.  A seven-seat hold is by construction the one carrying the most owed work.
#
#  IT MUST STAY RESTRICTED.  `ledgerstatelies` QUOTES this literal inside prose holding
#  `*` and `-`; a permissive `[^]]+` would match the quotation and manufacture a PHANTOM
#  hold -- the quoted-marker hazard from the other direction.  That prose is a built-in
#  negative control and is checked in controls.out beside this commit.
#  *** THE CLASS IS A STRICT COMMA-SEPARATED ID LIST, AND THE TWO WARRANTS THIS COMMENT
#  ORIGINALLY GAVE WERE BOTH MEASURED FALSE BY THE opus5 SEAT. ***
#
#  It said the restricted class was proven safe by a "built-in negative control" -- the
#  quoted marker in `ledgerstatelies`.  That control is VACUOUS: the row has ZERO entries
#  and its quotation lives in a row-level `state_note`, which held_rows() never reads.
#  Measured: swapping in the permissive `([^]]+?)` the comment forbade, or even `(.+?)`
#  with DOTALL, passes every control and renders sgirekills BYTE-IDENTICALLY.
#
#  It also said "every defang note quotes the literal it refutes".  Counted in
#  entries[].note: NINE live literals, all of them REAL MARKERS, and ZERO quotations,
#  against 31 defanged spellings.  The convention REWRITES the marker; it does not quote it.
#
#  THE REAL HAZARD IS A PROSE TOKEN LIST.  A sentence naming the marker and then listing
#  words separated by commas matched a loose class and manufactured a hold whose "seats"
#  were `and`, `not`, `a`, `panel`.  A strict `id(,id)*` shape cannot express prose, which
#  is why it is written this way rather than as a character class.
#
#  KNOWN AND ACCEPTED LIMIT: a real marker WRAPPED ACROSS LINES stays invisible.  Newlines
#  are excluded deliberately -- admitting them re-opens the phantom surface -- so the
#  generator requires markers to be written on one line, which is how they are generated.
#  #534 (R5): the literal AND the strict seat-list shape come from stage_tokens.py, which the
#  live-hold rule in check_stage_panels.py also parses with -- one parser, so the two cannot
#  disagree about which seats a marker names.
sys.path.insert(0, HERE)
import stage_tokens as st  # noqa: E402
MARKER = st.HELD_SEATS

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

*** THE PARAGRAPH THAT STOOD HERE WAS A FALSE ACTION-INSTRUCTION, RE-PRINTED INTO
`fable_queue.md` ON EVERY REGENERATION.  Corrected 2026-08-29. ***  It said: *"the older
08-17/08-18 panels (`exitsweep`, `ovsync`, `armbdt`, `b118L`, `b120r`, `dfreq`,
`reprowitness`) were NOT re-fired and still carry genuine codex holds."*

**Codex ANSWERED ALL SEVEN on 2026-08-26** -- verified by counting substantive codex entries
dated on or after that day on each row (ovsync carries three).  Six of the seven had their
stale markers defanged on 2026-08-29.  So this told the operator to re-fire seats that had
already answered, which is worse than a stale comment: a stale comment misleads a reader,
an action-instruction misdirects work.

**Action for the remaining rows:** consult the generated list below rather than any names
hardcoded here -- that is the whole point of generating it.  For `opus5`/`fable5`, fire them
against the cluster briefs when the owner's allocation frees them.  **A blank cell, a seat
failure and an allocation are three different things and this file names which is which.**

*A hardcoded roster inside a GENERATOR is a wrong record waiting for the data to move, which
is the same defect this project has now recorded for the `_scratchpad/*.pdf` inventory and the
seat-status tables.  Name no rows here that the ledger can name for you.*
"""


def held_rows(seat=None):
    """Rows carrying a [HELD AWAITING SEAT: x] marker.  seat=None means ANY seat.

    It used to default to "codex" and callers never passed anything else.  That was fine while
    codex was the only walled seat and WRONG the moment a second one was held: opus5 and fable5
    went held by owner allocation, section I went red naming 54 rows, and the generator that
    exists to keep that list current could not see any of them."""
    led = json.load(io.open(LEDGER, encoding="utf-8"))
    #  DERIVED, never hand-kept: the roster is whatever the ledger says it is.
    KNOWN_SEATS = {x["id"].lower() for x in led.get("seats", []) if x.get("id")}
    out = []
    for row in led["rows"]:
        stages = {}
        #  #534 F2 pass (codex, Opus): list only LIVE holds -- a marker every named seat has since
        #  answered is history, and advertising it as outstanding made the wall and section H
        #  disagree about which stages wait (29 listed here against H's 17).
        by_phase = {}
        for e in row.get("entries", []):
            by_phase.setdefault(e.get("phase", "?"), []).append(e)
        live = {ph: set(st.live_holds(es)) for ph, es in by_phase.items()}
        for e in row.get("entries", []):
            m = MARKER.search(e.get("note", "") or "")
            if not m:
                continue
            #  split: one marker may name several seats.
            #
            #  *** AND EVERY TOKEN IS VALIDATED AGAINST THE LEDGER'S OWN SEAT ROSTER. ***
            #  The kimi seat proposed this as the DURABLE close, and it is right: tuning the
            #  character class is an arms race against prose, while an id that is not a seat
            #  is wrong no matter what shape it arrived in.  An unknown token is rendered
            #  `?token` and announced on stderr rather than dropped -- a malformed marker and
            #  a well-formed one must not look alike, and a SILENT skip would hide exactly the
            #  phantom this validation exists to catch.
            for s in (x.strip().lower() for x in m.group(1).split(",")):
                if not s:
                    continue
                if s not in KNOWN_SEATS:
                    sys.stderr.write(
                        "gen_codex_wall: row %s phase %s: marker names UNKNOWN seat %r"
                        " -- malformed marker or a phantom match\n"
                        % (row["id"], e.get("phase", "?"), s))
                    s = "?" + s
                if seat and s != seat:
                    continue
                if not s.startswith("?") and s not in live.get(e.get("phase", "?"), ()):
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
