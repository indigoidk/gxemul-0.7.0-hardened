#!/usr/bin/env python3
"""mutants529j.py NAME SRC DST -- #529 kill table 10 (repair 12).  Imports table 9's mutator (every earlier mutant by
name), adds the Opus sixth-closing seat's mutants from its mutator copied as run (mutants_c6_opus.py, exec'd), and this
table's own: a SILENT BYPASS at each of the twelve cells repair 12's value rows carry (the flagship ruling, part A, RA1
(ii): "from the enumeration, not from the six mutants that happened to be built"), and the d->warned-keyed accept
shrink in both forms (RA3).  Every find-text occurs EXACTLY ONCE."""
import io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for t in ("killtable9_20260914", "killtable8_20260914", "killtable7_20260913", "killtable6_20260913",
          "killtable5_20260913", "killtable4_20260913", "killtable3_20260913", "killtable2_20260913"):
    sys.path.insert(0, os.path.join(HERE, "..", t))
import mutants529i as I                                    # noqa: E402

M = dict(I.M)
_ns = {}
exec(io.open(os.path.join(HERE, "mutants_c6_opus.py"), encoding="utf-8").read().split("if __name__")[0], _ns)
M.update({k: v for k, v in _ns["M"].items() if k != "base"})

LEN8 = "\tif (len == 8) {\n"


def bypass(cond):
    """a SILENT bypass inserted before the width test: the cell skips to the common tail with no announce"""
    return [(LEN8, "\tif (%s)\n\t\tgoto crime_declined;\n\n" % cond + LEN8)]


W, R_ = "writeflag == MEM_WRITE", "writeflag == MEM_READ"
M.update({
    "S_revPsw": bypass("len == 4 && %s && relative_addr == CRIME_REV" % W),
    "S_revPsd": bypass("len == 8 && %s && relative_addr == CRIME_REV" % W),
    "S_revPld": bypass("len == 8 && %s && relative_addr == CRIME_REV" % R_),
    "S_ctlld": bypass("len == 8 && %s && relative_addr == CRIME_CONTROL" % R_),
    "S_ctlsd": bypass("len == 8 && %s && relative_addr == CRIME_CONTROL" % W),
    "S_istld": bypass("len == 8 && %s && relative_addr == CRIME_INTSTAT" % R_),
    "S_istsd": bypass("len == 8 && %s && relative_addr == CRIME_INTSTAT" % W),
    "S_istsw": bypass("len == 4 && %s && relative_addr == CRIME_INTSTAT" % W),
    "S_imsw": bypass("len == 4 && %s && relative_addr == CRIME_INTMASK" % W),
    "S_timesd": bypass("len == 8 && %s && relative_addr == CRIME_TIME" % W),
    "S_40sw": bypass("len == 4 && %s && relative_addr == 0x40" % W),
    "S_40lw": bypass("len == 4 && %s && relative_addr == 0x40" % R_),
    #  RA3: the accept guard grown by a conjunct on the LATCH -- once any refusal has set CRIME_W_LEN, an 8-byte read
    #  (W_8r) or write (W_8w) falls to the decline arm, which is silent because the latch is set
    "W_8r": [(LEN8, "\tif (len == 8 && !(%s && (d->warned & CRIME_W_LEN))) {\n" % R_)],
    "W_8w": [(LEN8, "\tif (len == 8 && !(%s && (d->warned & CRIME_W_LEN))) {\n" % W)],
})

if __name__ == "__main__":
    if sys.argv[1:2] == ["list"]:
        print(" ".join(M)); sys.exit(0)
    name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    s = io.open(src, newline="").read()
    for find, repl in M[name]:
        n = s.count(find)
        if n != 1:
            sys.stderr.write("MUTANT %s: find-text occurs %d times (want 1)\n" % (name, n)); sys.exit(2)
        s = s.replace(find, repl, 1)
    io.open(dst, "w", newline="").write(s)
    print("APPLIED %s (%d edit(s))" % (name, len(M[name])))
