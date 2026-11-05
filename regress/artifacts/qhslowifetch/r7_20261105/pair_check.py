#!/usr/bin/env python3
"""pair_check.py <sessions dir> -- repair 11's PAIRING INVARIANT, checked from a run's session transcripts.  For each read-ahead cell
`T ra X` and its one-entry partner `T rp X`: the partner's transcript must hold exactly ONE -T halt report and the read-ahead session's
exactly TWO, all textually identical (memory_rw prints the failing paddr and the cpu's pc at the fetch, so identical lines mean the
same full pc and addr at every visit); the MSR command given before `continue` must be the same (both absent = the reset MSR 0); and
the final pc, MSR and SRR0 the `reg` command prints must be the same.  Prints one line per pair and PAIRS_OK=<n>/8."""
import io
import os
import re
import sys

D = sys.argv[1]
TAGS = ["", "me", "odd", "o1m", "o2", "o2m", "o3", "o3m"]
HALT = re.compile(r"^memory READ: from non-existant paddr=\S+ len=\d+ pc=\S+$", re.M)


def read(name):
    t = io.open(os.path.join(D, name.replace(" ", "_") + ".txt"), encoding="latin-1").read()
    stdin = t.split("--- stdin ---", 1)[1].split("--- transcript", 1)[0]
    msrcmd = [l for l in stdin.split("\n") if l.startswith("msr=")]
    seg = t[t.rfind("GXemul> reg"):] if "GXemul> reg" in t else ""
    regs = dict((k, (re.search(r"\b%s\s*=\s*(0x[0-9a-fA-F]+)" % k, seg) or [None, None])[1]) for k in ("pc", "msr", "srr0"))
    return HALT.findall(t), msrcmd, regs


ok = 0
for tag in TAGS:
    two, one = ("T ra " + tag).rstrip(), ("T rp " + tag).rstrip()
    h2, m2, r2 = read(two)
    h1, m1, r1 = read(one)
    good = len(h2) == 2 and len(h1) == 1 and len(set(h2 + h1)) == 1 and m1 == m2 and r1 == r2
    ok += good
    print("%s  %-9s <-> %-9s  halts %d / %d  %s  msr cmd %s  final pc %s msr %s srr0 %s" % (
        "PAIR-OK  " if good else "PAIR-FAIL", two, one, len(h2), len(h1),
        ("same line: " + h1[0].split("from ")[1]) if len(set(h2 + h1)) == 1 and h1 else "LINES DIFFER",
        m1[0] if m1 else "(none: reset 0)", r1["pc"], r1["msr"], r1["srr0"]))
print("PAIRS_OK=%d/8" % ok)
print("PAIR_CHECK_DONE")
