#!/usr/bin/env python3
"""esc_where.py -- the v7 CONTRACT's two escape disclosures, measured over census_v5.py's own scope (every .err under
GXEMUL-SEC and _scratchpad, .git excluded): (1) every file carrying a `?'-parameter CSI (ESC [ ? ...), any final byte; (2) the
files carrying an ESC that is neither CSI nor OSC (census_v5's OTHERESC); for each, every line where such an escape sits BEFORE
an `ERROR:' on the same line -- the shape the launcher's strip would leave unanchored.  Prints a denominator for each."""
import os, re

PROJ = r"C:\DocumentNoSnc\cc\GXEMUL"
roots = [os.path.join(PROJ, "GXEMUL-SEC"), os.path.join(PROJ, "_scratchpad")]
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
QCSI = re.compile(r"\x1b\[[0-9;]*\?")
OTHERESC = re.compile(r"\x1b(?![\[\]])")
allerr = []
for root in roots:
    for dp, dn, fn in os.walk(root):
        if os.sep + ".git" in dp or dp.endswith(".git"):
            continue
        for f in fn:
            if f.lower().endswith(".err"):
                allerr.append(os.path.join(dp, f))
nread = qfiles = ofiles = qerr = oerr = 0
for p in allerr:
    try:
        raw = open(p, "rb").read().decode("utf-8", "replace")
    except OSError:
        continue
    nread += 1
    if "\x1b" not in raw:
        continue
    q = bool(QCSI.search(raw)); o = bool(OTHERESC.search(raw))
    qfiles += q; ofiles += o
    if q or o:
        print("FILE %s%s %s" % ("Q" if q else "-", "O" if o else "-", p))
    for i, l in enumerate(raw.split("\n"), 1):
        if "ERROR:" not in l or "\x1b" not in l:
            continue
        pre = l[:l.index("ERROR:")]
        stripped = ANSI.sub("", l)
        if QCSI.search(pre):
            qerr += 1; print("  Q-before-ERROR %s:%d col0-after-strip=%s" % (p, i, stripped.startswith("ERROR:")))
        if OTHERESC.search(pre):
            oerr += 1; print("  O-before-ERROR %s:%d col0-after-strip=%s" % (p, i, stripped.startswith("ERROR:")))
print("SUMMARY: %d .err files read | `?'-CSI files %d | other-ESC files %d | lines with a `?'-CSI before ERROR: %d | "
      "lines with an other-ESC before ERROR: %d" % (nread, qfiles, ofiles, qerr, oerr))
