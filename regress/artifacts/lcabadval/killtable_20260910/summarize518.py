#!/usr/bin/env python3
#  #518 lcabadval kill-table SUMMARIZER.  Reads every <mutant>.raw in this directory and prints
#  score + the rows that REDDENED, by parsing the probe's own fixed-width row format
#  ("%-14s %-24s %-24s %-52s %s") -- the row NAME is columns 0..13, which is why this does not
#  split on whitespace: three row names ("def w once", "def r once") are three words.
#
#  A log whose last line is not LCABADVAL_DONE is reported as NO-SENTINEL and its score is NOT
#  read: a preserved log is verified by its completion sentinel, not by its existence.
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ["BASE"] + ["M%d" % i for i in range(1, 40)] + ["BASE2"]


def rows_of(path):
    txt = open(path, encoding="latin-1").read()
    lines = txt.split(chr(10))
    red, tot = [], 0
    for l in lines:
        #  A ROW LINE, and nothing else: the probe prints rows as "%-14s %-24s %-24s %-52s %s",
        #  so a row is >= 70 chars with a blank at column 14.  Without that shape test the
        #  summary line LCABADVAL_WITNESS=FAIL is scored as a reddened row -- which it is not,
        #  and which would inflate every mutant's red list by one.
        if len(l) >= 70 and not l.startswith("LCABADVAL"):
            if not (l.rstrip().endswith("FAIL") or l.rstrip().endswith(" ok")):
                continue
            #  The name field is "%-14s" plus a literal space -- but TWO row names
            #  ("wmask0 declined", "wmask1 declined") are FIFTEEN chars and OVERFLOW it, so a
            #  fixed l[:14] slice silently drops exactly those two rows.  Caught by the
            #  denominator: the parser saw 38 rows in a 40-row log.
            name = l[:14].rstrip() if l[14] == " " else l[:l.index(" ", 14)]
            if not name or name == "row":
                continue
            tot += 1
            if l.rstrip().endswith("FAIL"):
                got = l[15:39].strip()
                want = l[40:64].strip()
                red.append("%s[got %s want %s]" % (name, got, want))
    m = re.search(r"LCABADVAL_RESULT=(\d+)/(\d+)", txt)
    done = lines[-1].strip() == "LCABADVAL_DONE" or (
        len(lines) > 1 and lines[-2].strip() == "LCABADVAL_DONE")
    return (m.group(0) if m else "NO-SCORE"), red, done, tot


def key(fn):
    b = fn[:-4]
    m = re.match(r"M(\d+)_", b)
    if b == "BASE":
        return (0, 0)
    if b == "BASE2":
        return (2, 0)
    return (1, int(m.group(1)) if m else 999)


def main():
    out = []
    for fn in sorted(os.listdir(HERE), key=key):
        if not fn.endswith(".raw"):
            continue
        sc, red, done, tot = rows_of(os.path.join(HERE, fn))
        tag = "" if done else "  *** NO SENTINEL ***"
        out.append("%-24s %-22s %s%s" % (fn[:-4], sc, ("SWEPT CLEAN -- no row reddened"
                   if not red else "; ".join(red)), tag))
    print("%-24s %-22s %s" % ("mutant", "score", "reddened rows"))
    print("-" * 118)
    for l in out:
        print(l)


#  gen_table1.py imports this module for rows_of().  Without the guard the whole summary table
#  printed as a side effect of that import, on top of the generated file.
if __name__ == "__main__":
    main()
