#!/usr/bin/env python3
"""mutants_adj.py NAME SRC DST -- Opus ADJUDICATION seat, #529 repair 14.

Exact-string edits on the BASELINE (the uncommitted #529 working set).  MUTANT-TEXT-NOT-FOUND
is a hard FAIL, so every find-text doubles as a presence pin.

Same anchor discipline as mutants14.py: NO double-backslash anywhere in this file, because the
Bash -> heredoc -> Python path consumes one level and a silently-zero-match anchor is the
documented trap.
"""
import sys

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src).read()

CLOSE_GOTO = "\t\t}\n\t\tgoto crime_declined;\n"


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("MUTANT TEXT NOT FOUND (or not unique) for %s: %d occurrences" % (name, n))
    s = s.replace(old, new)


def latch_label(lab):
    """M3_timelatch's shape with the label swapped -- the goto moved inside the latch block,
       then re-issued for every label EXCEPT `lab'."""
    sub(CLOSE_GOTO,
        ("\t\t\tgoto crime_declined;\n"
         "\t\t}\n"
         "\t\tif (relative_addr != " + lab + ")\n"
         "\t\t\tgoto crime_declined;\n"))


if name == "base":
    pass

elif name == "M5_revlatch":
    #  THE CLAIM.  O4 derived REV as the second open cell of the decline x latch-SET axis.
    #  Byte-for-byte M3_timelatch with CRIME_TIME -> CRIME_REV.
    latch_label("CRIME_REV")

elif name == "M6_istlatch":
    #  THE NEGATIVE CONTROL.  Same shape at a label M1_gotolatch already proved is reached with
    #  the latch SET.  If this ALSO escapes, the finding is that the shape is invisible per se
    #  and the per-label cell count is not what is being measured.
    latch_label("CRIME_INTSTAT")

else:
    sys.exit("unknown mutant %s" % name)

open(dst, "w").write(s)
print("APPLIED %s" % name)
