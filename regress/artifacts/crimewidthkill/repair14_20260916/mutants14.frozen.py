#!/usr/bin/env python3
"""mutants14.py NAME SRC DST -- Opus pass-1 seat, #529 repair 14.  Exact-string edits on the
BASELINE (the uncommitted #529 working set).  MUTANT-TEXT-NOT-FOUND is a hard FAIL, so every
find-text doubles as a presence pin.

NOTE: NO double-backslash appears in this file on purpose.  A first draft quoted the fatal()
string with \n and the Bash->heredoc->Python path ate one backslash level, so the anchor
silently matched 0 occurrences -- the carrier's documented trap, met on the first try.  The
anchors below use only single-backslash escapes, which survive that path unchanged."""
import sys

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src).read()

CLOSE_GOTO = "\t\t}\n\t\tgoto crime_declined;\n"
PLAIN_GOTO = "\t\tgoto crime_declined;\n"
WIDTH = "\tif (len == 8) {\n"


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("MUTANT TEXT NOT FOUND (or not unique) for %s: %d occurrences" % (name, n))
    s = s.replace(old, new)


if name == "base":
    pass

elif name == "M1_gotolatch":
    #  The `goto' MOVED INSIDE the latch block: one line, up one line.  The FIRST refusal in a
    #  session declines correctly; EVERY LATER ONE falls through into the register switch, and
    #  SILENTLY, because the latch it just set suppresses the announce.
    sub(CLOSE_GOTO, "\t\t\tgoto crime_declined;\n\t\t}\n")

elif name == "M2_ld278clr":
    #  G-form SILENT bypass, latch-CLEAR, at ACCEPTS entry 46 (ld +0x278, 8R) -- one of the eight
    #  PRE-BLIND entries buckets8.py reports.
    sub(WIDTH,
        ("\tif (relative_addr == 0x278 && len == 8 && writeflag == MEM_READ\n"
         "\t    && !(d->warned & CRIME_W_LEN))\n"
         "\t\tgoto crime_declined;\n"
         "\n" + WIDTH))

elif name == "M4_timeplain":
    #  THE DISCRIMINATING CONTROL for M3: the goto narrowed by LABEL ALONE, no latch conjunct.
    #  Contract item 3 says this shape is rowed; `time lb/sb/lh/sh' should red.
    sub(PLAIN_GOTO,
        "\t\tif (relative_addr != CRIME_TIME)\n\t\t\tgoto crime_declined;\n")

elif name == "M3_timelatch":
    #  The SAME narrowing, conjoined with the latch: the session's FIRST refusal still
    #  declines correctly, so every row that drives its refusal first stays green.
    sub(CLOSE_GOTO,
        ("\t\t\tgoto crime_declined;\n"
         "\t\t}\n"
         "\t\tif (relative_addr != CRIME_TIME)\n"
         "\t\t\tgoto crime_declined;\n"))

else:
    sys.exit("unknown mutant %s" % name)

open(dst, "w").write(s)
print("APPLIED %s" % name)
