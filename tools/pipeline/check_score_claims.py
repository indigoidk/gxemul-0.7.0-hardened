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

    check "<stem> rows run"     "${res#*/}" <N>

*** THE EXAMPLE HERE USED TO BE A REAL PIN WITH A REAL NUMBER, AND A SEAT
POINTED OUT IT HAD ALREADY GONE STALE. ***  Nothing reads a docstring, so a
concrete number in one rots -- inside the very tool built to stop numbers
rotting.  It is a placeholder now: the example teaches the SHAPE, and the
shape is what the regex matches.

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
#  *** THE `x` IN THE LOOKBEHIND IS LOAD-BEARING AND WAS ADDED 2026-08-26 (`scoreclaimhex`).
#  Without it this reads a SLASH-SEPARATED HEX LIST as a score claim: `bases
#  0x00/0x10/0x20/0x30` -- one line of ordinary prose in asic_badaddr_probe.py's
#  docstring -- yielded THREE stale-claim FAILs (`00/0`, `10/0`, `20/0`) against a pin of
#  12, and NONE of them had ever been written. The `00` is preceded by `x`, which the old
#  `(?<![\d/])` happily allowed.
#
#  A FALSE FAIL IS THE OPPOSITE OF THE FAILURE THIS SECTION EXISTS TO CATCH, AND IS STILL
#  EXPENSIVE: a gate that reddens on prose trains its reader to explain away red rows,
#  which is how a real one gets waved through.
#
#  Negative-controlled in BOTH directions before landing: five real score claims
#  (13/13, 26/26, 8/32, "52 / 52", 16/16) all still match; two hex lists
#  (0x00/0x10/0x20/0x30, 0x18/0x1c) no longer do. Zero regressions.
#
#  *** AND A HYPHEN IS THE SAME GAP, FOUND 2026-09-17 BY A FALSE FAIL IT PRODUCED. ***
#  The lookbehind excluded a digit, `x` and `/` -- but not `-`, so an ORDINAL PAIR
#  written `entries-4/8` was reported as a stale score claim of 4/8.  That is this
#  tree's correlate-keying class: the matcher tests a SHAPE (N/M) and the class is a
#  SCORE, so its error is invisible because the output is still a plausible number.
#
#  *** WORSE THAN A FALSE FAIL: THE PRESCRIBED REMEDY WAS TO SHIP A FALSE STATEMENT.
#  The message says "if that is a deliberate historical quote, write '8-row' on the
#  same line" -- which, on a line about array entries, silences the check by writing
#  something untrue into a probe.  A check whose repair corrupts the thing it guards
#  is the shape the carrier already records for the build-tree clearance. ***
#
#  AUDITED FOR SIBLINGS with a denominator rather than fixed on the one instance:
#  710 N/M matches across 121 regress files; the hyphen-aware form drops exactly FOUR
#  and keeps 706.  All four are ordinal pairs, none is a score -- `entries-4/8`
#  (crime_width_probe), `len-3/5` (lca_isalane_probe:96), `opcode-59/63`
#  (ppc_halt_probe:238), `pass 2-3 / 6-7` (sgi_de_primop_probe:985).  THREE OF THE
#  FOUR ARE LATENT: they fire only once their probe gains a gate pin, so the class
#  was four members with one visible.
SCORE = re.compile(r"(?<![\dx/-])(\d+)\s*/\s*(\d+)(?![\d/%])")


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
    dupes = []
    loose = []
    stem_gates = {}
    ambig = set()
    for f in sorted(os.listdir(REGRESS)):
        if not f.startswith("gate_") or not f.endswith(".sh"):
            continue
        p = os.path.join(REGRESS, f)
        txt = io.open(p, encoding="utf-8", errors="replace").read()
        for i, ln in enumerate(txt.split(chr(10)), 1):
            #  a `rows run` line the PIN regex cannot see governs NOTHING,
            #  and the old version simply did not mention them
            if "rows run" in ln and "check" in ln and not PIN.search(ln):
                loose.append((f, i))
        for m in PIN.finditer(txt):
            stem, cnt = m.group(1), int(m.group(2))
            #  *** LAST-WRITE-WINS SILENTLY CHECKED THE WRONG NUMBER, AND A
            #  MEASURING SEAT FOUND A LIVE INSTANCE. ***  `idle` is pinned 9
            #  in gate_arm.sh and 3 in gate_m88k_rounding.sh; sorted order put
            #  m88k last, so every `idle` comment in gate_arm.sh was checked
            #  against 3 and nothing said so.
            #  *** KEYED BY (GATE, STEM), not by stem alone. ***  Comment
            #  search is already scoped to the gate carrying the pin, so a
            #  bare-stem key was simply wrong -- and it collided live:
            #  `idle` is 9 in gate_arm.sh and 3 in gate_m88k_rounding.sh,
            #  sorted order put m88k last, and every `idle` comment in
            #  gate_arm.sh was checked against 3 with nothing saying so.
            #  Two gates may legitimately pin the same stem; only the
            #  DOCSTRING lookup is genuinely ambiguous, and that is reported
            #  below rather than guessed.
            if (f, stem) in pins and pins[(f, stem)][0] != cnt:
                dupes.append((stem, pins[(f, stem)], (cnt, f)))
            if stem in stem_gates and stem_gates[stem][0] != cnt:
                ambig.add(stem)
            stem_gates[stem] = (cnt, f)
            pins[(f, stem)] = (cnt, f)

    bad = []
    for (gate, stem), (want, _g) in sorted(pins.items()):
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
        if stem in ambig:
            #  the same stem pinned to different counts in different gates:
            #  its gate comments are still checked (scoped correctly above),
            #  but which probe docstring it names is genuinely unknowable.
            print("  note  stem %r is pinned to different counts in more than one gate; its DOCSTRING is not checked" % stem)
            continue
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

    for stem, a, b in dupes:
        bad.append("DUPLICATE STEM %r pinned %d in %s and %d in %s -- one of them is being checked against the other's number"
                   % (stem, a[0], a[1], b[0], b[1]))
    if loose:
        #  visibility, not a failure: a single-probe gate legitimately writes
        #  `check "rows run"` with no stem, and there is nothing to associate
        #  it with.  But it must not look governed when it is not.
        print("  note  %d `rows run` line(s) carry no probe stem, so no comment in their gate is checked: %s"
              % (len(loose), ", ".join("%s:%d" % x for x in loose[:6])))
    print("  check_score_claims: %d probes pinned by a gate" % len(pins))
    #  *** THE COUNT WAS A DISPLAY, NOT AN ASSERTION, SO NOTHING FAILED WHEN
    #  IT DROPPED. ***  A measuring seat showed the whole check can be
    #  disarmed with no behaviour change at all: quote the pin literal
    #  (`"32"` instead of `32`) and regress/lib.sh:82 compares it as a string
    #  exactly as before, while this file silently stops governing that
    #  probe.  precommit section U now pins this number.
    print("SCORE_CLAIMS_PINNED=%d" % len(pins))
    if bad:
        for b in bad:
            print("  STALE  " + b)
        print("SCORE_CLAIMS_FAIL  %d stale score claim(s)" % len(bad))
        return 1
    #  Honest about coverage: only stems that resolve to a <stem>_probe.py
    #  have their docstring checked at all.
    with_ds = sum(1 for _g, st in pins
                  if os.path.exists(os.path.join(REGRESS, st + "_probe.py"))
                  or os.path.exists(os.path.join(REGRESS, st + ".py")))
    print("SCORE_CLAIMS_PASS  %d gate comment set(s) checked; %d of %d stems also have a probe docstring checked"
          % (len(pins), with_ds, len(pins)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
