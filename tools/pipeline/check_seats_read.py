#!/usr/bin/env python3
"""A SEAT THAT ANSWERED AND WAS NEVER RECORDED IS THE FAILURE THIS CHECKS FOR.

The dashboard renders three different things as the same blank cell:

    (a) the seat was never fired          -- legitimate, but should be said
    (b) the seat failed / hit a quota     -- a SEAT FAILURE, never agreement
    (c) the seat ANSWERED and nobody recorded it   <-- this one

(c) is the dangerous one, because the round is reported as reviewed while a real
answer sits unread on disk.  It happened at least twice and BOTH TIMES THE OWNER
SPOTTED IT BY EYE, not the harness:

  * panel_20260815_202720 / kimi -- 192 KB, unrecorded for a day.  Reading it found
    that gate 2 has ZERO coverage of dev_rtc.c, so #429's fix can be reverted and
    the gate stays green (filed `rtcgate`).
  * panel_20260816_024410 / kimi --  99 KB, unrecorded, in a round that had already
    SHIPPED.  Reading it found that diff_m8invread's spy counts CALLBACK calls, so a
    mutant clearing the dyntrans arrays directly passes all 21 rows (`m8invground`).

Both were real findings.  Neither cost anything to obtain except reading.

THE RULE THIS ENFORCES: once a ledger entry cites a panel directory, EVERY seat in
that directory that produced a substantial answer must be cited by some entry for
that same seat.  Citing a panel dir is the act that puts it in scope -- that is
deliberate, because it means the check has no opinion about panels the ledger has
not claimed, and cannot be gamed by simply not citing anything (a round with no
panel citation at all is caught by the existing pass-2 receipt check instead).

Exit 0 clean, 1 on violations, 2 on usage error.  Verbose listing with --list.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "ledger.json")
#  _scratchpad lives at the PROJECT root.  From GXEMUL-SEC/tools/pipeline/
#  that is three levels up, where it used to be one.  Getting this wrong
#  would make the check find no panels and report "nothing in scope" --
#  a PASS that means nothing, which is the failure this file exists to stop.
PANELS = os.environ.get("GXPANELS") or os.path.normpath(
    os.path.join(HERE, "..", "..", "..", "_scratchpad"))

#  A thinking model that emits only its reasoning preamble produces a few hundred
#  bytes and no verdict.  panel.sh calls that SUSPECT at the same threshold; keeping
#  the two the same means this check and the seat check agree about what an answer is.
MIN_ANSWER = 800

FILE2SEAT = {
    "codex.txt": "codex",
    "agy.txt": "agy",
    "kimi.txt": "kimi",
    "grok.txt": "grok",
    "grok_fg.txt": "grok",           # a foreground re-fire of a truncated seat
    "grok_retry.txt": "grok",
    "codex_pass2.txt": "codex",
    "ollama_glm.txt": "glm",
    "ollama_deepseek.txt": "deepseek",
    "ollama_minimax.txt": "minimax",
}

PANEL_RE = re.compile(r"panel_\d{8}_\d{6}")


def load():
    with open(LEDGER, encoding="utf-8") as f:
        return json.load(f)


def cited_pairs(ledger):
    """(panel_dir, seat) and (panel_dir, filename) the ledger claims, plus the dirs in scope.

    A file is counted as read if the entry NAMES IT, or -- for a seat with only one answer
    file in that directory -- if the entry cites the directory and the seat.  The filename
    form is what closes the two-answers-one-citation hole; the seat form is kept so older
    entries that cite a directory without a filename still count.
    """
    pairs, files, dirs = set(), set(), set()
    for row in ledger["rows"]:
        for ent in row.get("entries", []):
            blob = "%s %s" % (ent.get("ev", ""), ent.get("note", ""))
            for d in PANEL_RE.findall(blob):
                dirs.add(d)
                pairs.add((d, ent.get("seat")))
                for fn in FILE2SEAT:
                    if fn in blob:
                        files.add((d, fn))
    return pairs, files, dirs


def answers_on_disk(panel_dir):
    """(seat, filename) -> size, for one panel directory.

    KEYED ON THE FILE, NOT THE SEAT, and that distinction is the whole point.  The first
    version returned one entry per seat, so a seat with TWO substantial answers in the same
    directory -- codex.txt from pass 1 and codex_pass2.txt from pass 2 -- was satisfied by a
    single citation of either.  Measured: codex's 491 KB pass-1 answer on the m8sarpurge
    panel was never read, and this check passed anyway, because the pass-2 file was cited.
    The seat had answered twice and been read once.  Found when the owner asked for a full
    panel per STAGE and the audit showed research at 8/9 with codex missing.
    """
    out = {}
    base = os.path.join(PANELS, panel_dir)
    for fn, seat in FILE2SEAT.items():
        p = os.path.join(base, fn)
        if os.path.exists(p) and os.path.getsize(p) >= MIN_ANSWER:
            out[(seat, fn)] = os.path.getsize(p)
    return out


def main(argv):
    listing = "--list" in argv
    ledger = load()
    pairs, files, dirs = cited_pairs(ledger)

    if not dirs:
        print("check_seats_read: no ledger entry cites a panel directory; nothing in scope.")
        return 0

    violations = []
    checked = 0
    for d in sorted(dirs):
        if not os.path.isdir(os.path.join(PANELS, d)):
            #  Stated, not silently skipped: a cited directory that is gone cannot be
            #  checked, and pretending otherwise is how a green row means nothing.
            print("  --   %s: cited but NOT ON DISK; cannot verify" % d)
            continue
        onhand = answers_on_disk(d)
        #  How many substantial files this seat has in this directory.  With one, citing the
        #  directory and the seat is enough.  With two or more, the ENTRY MUST NAME THE FILE,
        #  or a single citation silently vouches for an answer nobody opened.
        percount = {}
        for (seat, fn) in onhand:
            percount[seat] = percount.get(seat, 0) + 1
        for (seat, fn), sz in sorted(onhand.items()):
            checked += 1
            named = (d, fn) in files
            covered = named or (percount[seat] == 1 and (d, seat) in pairs)
            if not covered:
                violations.append((d, seat, sz, fn))
            elif listing:
                print("  ok   %s / %-9s %7d b  (%s)" % (d, seat, sz, fn))

    print("check_seats_read: %d substantial answers across %d cited panel dirs"
          % (checked, len(dirs)))
    if not violations:
        print("SEATS_READ_PASS  every seat that answered in a cited panel is recorded")
        return 0

    print("SEATS_READ_FAIL  %d seat answers exist on disk and are recorded NOWHERE:"
          % len(violations))
    for d, seat, sz, fn in violations:
        print("    %s / %-9s %8d b   (%s)" % (d, seat, sz, fn))
    print()
    print("  A seat that answered and was not recorded is NOT a seat failure and NOT")
    print("  agreement -- it is an unread review, and this project has twice found real")
    print("  defects sitting in one.  Read it and add a ledger entry, or if it truly had")
    print("  nothing to say, record THAT with an explicit entry rather than a blank.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
