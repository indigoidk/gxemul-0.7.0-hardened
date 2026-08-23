#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Catch SCORE CLAIMS that a later edit made stale.

*** WHY THIS EXISTS: FOUR INCIDENTS IN ONE SESSION, ALL THE SAME SHAPE. ***

A round measures a detector at N rows, writes "x/N" into a gate comment, a probe
docstring, a round block and a ledger note -- and then GROWS THE DETECTOR.  The
pin gets updated because the gate fails without it.  The prose does not, because
nothing reads it.

  #458  the gate comment kept a 12-row-era "10/12" beside a 14-row gate
  #459  the CHANGELOG kept "4/22" when the measured number was 5/23
  #460  OUTSTANDING_BUGS re-mapped coordinates to a state never committed
  #461  the round block and gate comment said "7/21, 21/21" at 25 rows

Each was caught by a review seat reading carefully.  The fourth was caught by a
seat that hit its usage limit MID-ANSWER and got one sentence out -- which is
the argument for mechanising it: the catch depended on a seat surviving long
enough to say so.

*** WHAT IT CHECKS, AND THE ASSOCIATION IS THE WHOLE DESIGN. ***

A gate pins each probe's row count:

    check "gdrom_default rows run"     "${gddres#*/}" 25

That pin is AUTHORITATIVE -- the gate fails immediately if it disagrees with the
probe, so it cannot go stale the way prose can.  So: within the gate file, any
COMMENT line that names that probe's stem and carries an `x/y` must use the same
y.  The probe's own docstring is checked the same way.

*** THE FIRST VERSION ONLY FLAGGED DENOMINATORS WITHIN 6 OF THE PIN, AND A PANEL
SEAT MEASURED THAT IT MISSES THE VERY CASES THIS FILE WAS BUILT FOR. ***

The window was meant to separate "this probe's own score" from a quote of some
other measurement.  It does not:

    pin=32  claims x/25   diff=7    silently ignored
    pin=32  claims x/21   diff=11   silently ignored   <- #461's OWN numbers
    pin=32  claims x/12   diff=20   silently ignored   <- #458's OWN numbers

Detectors GROW, so a stale denominator is always SMALLER than the pin -- and the
staler it is, the further away.  The window was backwards, filtering out exactly
the worst cases while catching only the nearly-fresh ones.  Now every denominator
must equal the pin unless its line names its era.

*** WHAT IT DOES NOT CHECK, said plainly rather than left to be discovered. ***

CHANGELOG round blocks and ledger notes are NOT checked, because there is no
mechanical association between a prose paragraph and a probe -- "7/25 pre-fix"
names no probe, and guessing would produce false positives, which is how a check
gets ignored.  Those still depend on a reading seat.  This closes the half where
the pin and the prose sit in the same file, which is where three of the four
incidents were.
"""
import io
import os
import re
import sys

#  This file lives in tools/pipeline/, so the repo root is TWO levels up from
#  the directory it sits in -- three dirnames, not two.  The first draft used
#  two and resolved regress/ to tools/regress/, which does not exist.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGRESS = os.path.join(ROOT, "regress")

#  check "<stem> rows run"     "${x#*/}" N
PIN = re.compile(r'check\s+"(\S+)\s+rows\s+run"\s+"[^"]*"\s+(\d+)')
#  *** A BARE d+/d+ MATCHES A DATE, AND A PANEL SEAT MEASURED IT. ***  On
#  "measured 2026/08/23" the old pattern returned (2026, 08) and would have
#  compared 08 against a row count.  The flanking guards reject anything that
#  is part of a longer slash-run (a date, a path, a/b/c) or a percentage.
SCORE = re.compile(r"(?<![\d/])(\d+)\s*/\s*(\d+)(?![\d/%])")


def comment_lines(path):
    """Yield (lineno, text) for comment lines only -- shell # and C-ish * lines."""
    for i, ln in enumerate(io.open(path, encoding="utf-8",
                                   errors="replace").read().split("\n"), 1):
        st = ln.strip()
        if st.startswith("#") or st.startswith("*") or st.startswith("//"):
            yield i, ln


def docstring(path):
    s = io.open(path, encoding="utf-8", errors="replace").read()
    m = re.match(r'\s*(?:#![^\n]*\n)?(?:#[^\n]*\n)*\s*"""(.*?)"""', s, re.S)
    return m.group(1) if m else ""


def main():
    pins = {}          # stem -> (count, gatefile)
    for f in sorted(os.listdir(REGRESS)):
        if not f.startswith("gate_") or not f.endswith(".sh"):
            continue
        p = os.path.join(REGRESS, f)
        for m in PIN.finditer(io.open(p, encoding="utf-8",
                                      errors="replace").read()):
            pins[m.group(1)] = (int(m.group(2)), f)

    bad = []
    for stem, (want, gate) in sorted(pins.items()):
        #  1. comment lines in the gate that NAME this probe
        gp = os.path.join(REGRESS, gate)
        for lineno, ln in comment_lines(gp):
            if stem not in ln:
                continue
            for a, b in SCORE.findall(ln):
                if int(b) != want:
                    bad.append("%s:%d  names %s and claims %s/%s, pin is %d"
                               % (gate, lineno, stem, a, b, want))
        #  2. the probe's own docstring
        for cand in (stem + "_probe.py", stem + ".py"):
            pp = os.path.join(REGRESS, cand)
            if not os.path.exists(pp):
                continue
            for ln in docstring(pp).split(chr(10)):
                for a, b in SCORE.findall(ln):
                    if int(b) == want:
                        continue
                    #  *** THE ESCAPE IS THE DOCUMENTATION. ***  A deliberate
                    #  historical quote must NAME ITS ERA -- write
                    #  "6/10 (the then 10-row pin)" and this accepts it,
                    #  because a reader can then tell a quote from a stale
                    #  claim.  Nothing else can: they are the same three
                    #  characters.
                    if ("%d-row" % int(b)) in ln:
                        continue
                    bad.append("%s docstring  claims %s/%s, pin is %d (if that is a deliberate historical quote, write '%s-row' on the same line)"
                               % (cand, a, b, want, b))

    print("  check_score_claims: %d probes pinned by a gate" % len(pins))
    if bad:
        for b in bad:
            print("  STALE  " + b)
        print("SCORE_CLAIMS_FAIL  %d stale score claim(s)" % len(bad))
        return 1
    print("SCORE_CLAIMS_PASS  every in-file score claim matches its gate pin")
    return 0


if __name__ == "__main__":
    sys.exit(main())
