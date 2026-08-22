#!/usr/bin/env python3
"""#450 DETECTOR: every buf[]-assembly statement in arcbios.c matches its frozen canonical
form EXACTLY -- an exact-statement census, not a pattern.

WHY EXACT STATEMENTS AND NOT A REGEX, measured the same evening this file was written.
The first census was two greps: "14 cast spellings, 0 uncast".  A pass-2 seat killed it
with one token: `(((uint32_t)buf[3]<<24) & 0x7fffffff)` keeps the cast SPELLING, passes
every sanitizer, and silently drops bit 31 -- both rows green over a real value defect.
*** A PATTERN PINS WHAT ITS AUTHOR THOUGHT OF. ***  #444's row S4 met the same failure the
same way and is the precedent: freeze the WHOLE statement, whitespace-normalised, and
exact-match the multiset.  A mask insert, a cast swap, a wrapper, a reordering -- anything
that changes the statement -- now reddens, whether or not the author thought of it.

THE COST, stated so nobody reads it as a defect: a LEGITIMATE edit to any of these
fourteen statements must update the frozen table in the same commit.  That is the accepted
S4 trade -- the table is the reviewable record of what the decode is supposed to say.

THE TABLE WAS GENERATED, NOT TYPED.  Hand-transcribing fourteen long expressions is the
hand-assembled-encoding trap in prose form (five recorded incidents), so the canonical
forms were extracted from the just-reviewed post-#450 file by the same stripper this probe
uses, eyeballed against the diff, and frozen.

WHAT THIS FILE CANNOT SEE, stated rather than discovered: it reads SOURCE.  A compiler bug
or a semantically-equivalent rewrite that changes the statement text reddens it (loud,
safe); a defect in a statement NOT in the table -- some other decode elsewhere -- is out of
scope.  The companion behavioural row in gate 9 (UBSan sweep over the reaching subtypes)
covers execution, and inherits gate 9's staleness caveat (`asanstale`), which is exactly
why THIS row is deliberately binary-independent.

usage:  arcbios_shift_probe.py <path-to-arcbios.c>
"""
import io
import re
import sys

EXPECT_ROWS = 2

#  The fourteen canonical statements, whitespace-stripped, sorted.  FROZEN 2026-08-21
#  from the post-#450 file.  Edit ONLY together with a reviewed change to arcbios.c.
CANON = sorted([
    "child=(uint64_t)buf[0]+((uint64_t)buf[1]<<8)+((uint64_t)buf[2]<<16)+((uint64_t)buf[3]<<24)+((uint64_t)buf[4]<<32)+((uint64_t)buf[5]<<40)+((uint64_t)buf[6]<<48)+((uint64_t)buf[7]<<56)",
    "child=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint64_t)buf[3]<<24)",
    "echild=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint32_t)buf[3]<<24)",
    "echild=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint64_t)buf[3]<<24)+((uint64_t)buf[4]<<32)+((uint64_t)buf[5]<<40)+((uint64_t)buf[6]<<48)+((uint64_t)buf[7]<<56)",
    "eparent=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint32_t)buf[3]<<24)",
    "eparent=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint64_t)buf[3]<<24)+((uint64_t)buf[4]<<32)+((uint64_t)buf[5]<<40)+((uint64_t)buf[6]<<48)+((uint64_t)buf[7]<<56)",
    "epeer=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint32_t)buf[3]<<24)",
    "epeer=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint64_t)buf[3]<<24)+((uint64_t)buf[4]<<32)+((uint64_t)buf[5]<<40)+((uint64_t)buf[6]<<48)+((uint64_t)buf[7]<<56)",
    "parent=(uint64_t)buf[0]+((uint64_t)buf[1]<<8)+((uint64_t)buf[2]<<16)+((uint64_t)buf[3]<<24)+((uint64_t)buf[4]<<32)+((uint64_t)buf[5]<<40)+((uint64_t)buf[6]<<48)+((uint64_t)buf[7]<<56)",
    "parent=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint64_t)buf[3]<<24)",
    "peer=(uint64_t)buf[0]+((uint64_t)buf[1]<<8)+((uint64_t)buf[2]<<16)+((uint64_t)buf[3]<<24)+((uint64_t)buf[4]<<32)+((uint64_t)buf[5]<<40)+((uint64_t)buf[6]<<48)+((uint64_t)buf[7]<<56)",
    "peer=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint64_t)buf[3]<<24)",
    "tmp=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint32_t)buf[3]<<24)",
    "tmp=buf[0]+(buf[1]<<8)+(buf[2]<<16)+((uint64_t)buf[3]<<24)",
])

rows = []


def row(name, ok, got, want):
    rows.append((name, bool(ok)))
    print("  %-4s %-64s" % ("ok" if ok else "FAIL", name))
    if not ok:
        print("       got  %s\n       want %s" % (got, want))


def extract(path):
    s = io.open(path, encoding="utf-8", errors="replace").read()
    #  Strip block comments, line comments and string literals, so a comment quoting the
    #  idiom cannot enter the census (the loud false-positive the v1 grep accepted).
    s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
    s = re.sub(r"//[^\n]*", " ", s)
    s = re.sub(r'"(?:[^"\\]|\\.)*"', '""', s)
    out = []
    for st in re.split(r"[;{}]", s):
        c = re.sub(r"\s+", "", st)
        if "buf[3]" in c and "<<24" in c:
            out.append(c)
    return sorted(out)


def main(argv):
    if len(argv) != 1:
        print("usage:  arcbios_shift_probe.py <path-to-arcbios.c>")
        return 2
    path = argv[0]
    try:
        got = extract(path)
    except OSError as e:
        print("  OPERATIONAL FAILURE: %s" % e)
        print("ARCSHIFT_RESULT=0/%d" % EXPECT_ROWS)
        print("ARCSHIFT_FAIL")
        return 1

    row("C1 every buf[3]<<24 statement matches its frozen canonical form",
        got == CANON,
        "extras=%r missing=%r" % ([g for g in got if g not in CANON],
                                  [c for c in CANON if c not in got]),
        "exact multiset equality with the 14 frozen statements")

    #  There is deliberately NO separate count row.  Six mutants were measured and every
    #  one died to C1; a count row could only fire alone on a DELETED statement, which
    #  reddens C1 too (as "missing").  A row that can never fire alone is decoration, and
    #  this project's own review standard calls that vacuous.

    row("W-id IDENTITY row count -- guards against a stale copy",
        len(rows) + 1 == EXPECT_ROWS, len(rows) + 1, EXPECT_ROWS)

    bad = sum(1 for _, ok in rows if not ok)
    print()
    print("ARCSHIFT_RESULT=%d/%d" % (len(rows) - bad, len(rows)))
    print("ARCSHIFT_PASS" if bad == 0 else "ARCSHIFT_FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
