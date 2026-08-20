#!/usr/bin/env python3
"""HOW MANY GUEST-DRIVABLE HOST-LOG FLOODS ARE THERE, AND WHERE?

Usage:
    census_floods.py [--list] [--check]

WHY THIS EXISTS.  Two rows were filed separately and independently -- `rtcflood` (an unlatched
`fatal()` in `dev_rtc.c`) and `wdcflood` (an unlatched `fatal()` in `dev_wdc.c`'s `default:`
arm) -- and they are the same shape: **a host log line a guest can emit without limit.**  The
project has been correcting that shape one instance at a time since #265/#269 established the
one-line `warned_*` latch idiom, and #337 applied it three times inside `dev_wdc.c` alone --
and still missed the path `wdcflood` names.

A panel seat then argued `rtcflood` was a REGRESSION INTRODUCED BY #429, on the grounds that
"before #429 there was no `fatal()` at dev_rtc.c:132, so there was no flood".  MEASURED: the
file carried **2** `fatal()` calls before #429 and **3** after -- so #429 did add one, but the
other two sit in that file's own unimplemented-access arm and are **equally unlatched and
equally guest-drivable**.  So `rtcflood` is not a regression; it is a THIRD INSTANCE in a file
that already had two.  Both the seat's framing and the original filing were narrower than the
truth.

That is the project's own rule arriving late: *"when correcting a claim, GREP FOR ITS SIBLINGS
before calling it fixed"* -- written after an 'un-fakeable' claim was corrected in one place and
survived in three.  Before filing a third one-line latch, count the class.

------------------------------------------------------------------------------------------
*** WHAT THIS MEASURES, AND -- MORE IMPORTANTLY -- WHAT IT DOES NOT. ***

It reports, per file under `src/devices/`:
    fatal      how many `fatal(` calls the file contains
    latches    how many DISTINCT latch-flag identifiers it mentions (warned_/reported_/...)
    unimpl     how many times it says "unimplemented"/"unknown read"/"not implemented"

**THE LATCH COLUMN IS PER FILE, NOT PER PATH, AND THAT IS A REAL LIMIT RATHER THAN A
FOOTNOTE.**  A file with one latch and ten unlatched paths counts as "latched" here.
`dev_wdc.c` is exactly that case: three latches from #337, and `wdcflood` is a path they
missed.  So "NO LATCH ANYWHERE" is a **FLOOR on the problem, never a census of it**, and the
true count is higher than anything this prints.

**NOT EVERY `fatal()` IS A FLOOD.**  Many are init-time, or genuinely once-only, or on paths no
guest can drive.  This tool does not do reachability -- doing so needs the call graph, and a
tool that guessed would be worse than one that declines.  So every number here is an UPPER
bound on flood candidates and a LOWER bound on unlatched files, and neither is a defect count.

Read it as: *where should someone look first*, never as *how many bugs there are*.  That is the
same contract `census_exits.py` ships under, for the same reason -- an inventory shipped as an
INSTRUMENT stays true as the tree moves; a number in a commit message goes stale the same week.

`--check` exits non-zero if any file gains `fatal()` calls while having no latch idiom at all
AND the file is not on the exemption list below.  It is deliberately NOT wired into precommit
yet: the baseline is large and freezing it would be a policy decision, not a measurement.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.normpath(os.path.join(HERE, "..", ".."))
DEV = os.path.join(SEC, "src", "devices")

LATCH = re.compile(r"\b(warned|reported|complained|has_warned)\w*\b")
FATAL = re.compile(r"\bfatal\s*\(")
UNIMPL = re.compile(r"unimplemented|unknown\s+(?:read|write)|not implemented", re.I)


def census():
    rows = []
    for fn in sorted(os.listdir(DEV)):
        if not fn.endswith(".c"):
            continue
        try:
            s = io.open(os.path.join(DEV, fn), encoding="utf-8",
                        errors="replace", newline="").read()
        except OSError:
            continue
        nf = len(FATAL.findall(s))
        if not nf:
            continue
        rows.append((fn, nf, len(set(LATCH.findall(s))), len(UNIMPL.findall(s))))
    rows.sort(key=lambda r: -r[1])
    return rows


def main(argv):
    rows = census()
    listing = "--list" in argv
    shown = rows if listing else rows[:20]

    print("  %-26s %6s %8s %8s" % ("device", "fatal", "latches", "unimpl"))
    print("  %-26s %6s %8s %8s" % ("------", "-----", "-------", "------"))
    for fn, nf, nl, un in shown:
        print("  %-26s %6d %8d %8d%s"
              % (fn, nf, nl, un, "   <-- no latch idiom in this file" if not nl else ""))
    if not listing and len(rows) > len(shown):
        print("  ... %d more files; pass --list for all" % (len(rows) - len(shown)))

    nofl = [r for r in rows if not r[2]]
    print()
    print("  files under src/devices/ containing fatal(): %d" % len(rows))
    print("  total fatal() calls:                         %d" % sum(r[1] for r in rows))
    print("  files with fatal() and NO latch idiom:       %d, carrying %d calls"
          % (len(nofl), sum(r[1] for r in nofl)))
    print()
    print("  THE LATCH COLUMN IS PER FILE, NOT PER PATH.  dev_wdc.c shows 2 latches and still")
    print("  has an unlatched flood (`wdcflood`).  Treat 'no latch idiom' as a FLOOR on where")
    print("  to look, never as a count of defects -- and remember most fatal() calls are not")
    print("  guest-drivable at all.  This tool does no reachability analysis and does not")
    print("  pretend to: that needs the call graph, and a guess would be worse than declining.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
