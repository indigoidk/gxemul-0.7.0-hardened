#!/usr/bin/env python3
"""retro_logs.py -- did the defect corrupt a RECORDED table?  For each AFFECTED frozen driver whose per-mutant
run logs are preserved at HEAD, read every log's LAST non-blank line and test it against that detector's
completion sentinel.  Reads `git show HEAD:<path>` (never the working tree).  A log without its sentinel is
a table row that rests on a run that did not finish.
"""
import io, os, re, subprocess, sys

SEC = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
                   "GXEMUL-SEC")
A = "regress/artifacts/"
WDC = r"^WDC_IDENTIFY_(PASS|FAIL)$"
SETS = [  # (driver, dir, file regex, sentinel regex)
    ("kill479.sh", "wdccmdreset/killtable_20260827", r"\.out$", WDC),
    ("killalt.sh", "wdcaltctrl/killtable_20260827", r"^(base|bin_.*)\.out$", WDC),
    ("kill482.sh", "wdcaltctrlcov/killtable_20260827", r"^(b482base|bin_.*)\.out$", WDC),
    ("kill480.sh / kill480b.sh", "wdccallsite/killtable_20260827", r"^(base|bin_.*)\.out$", WDC),
    ("kill477b.sh", "wdccdbmidxfer/killtable2_20260827", r"\.out$", WDC),
    ("kill478.sh", "wdcdataoutdrain/killtable_20260827", r"^(base|M.*)\.out$", WDC),
    ("author_kill483.sh", "wdcaltctrlfam/killtable_20260827", r"^(b483base|bin_.*)\.out$", WDC),
    ("kill495*.sh", "wdcaddtoinbufbound/killtable_20260830", r"^kill_.*\.out$", r"_DONE$"),
    ("kill494.sh (main)", "wdcaltoffset/killtable_20260830", r"^main_.*\.out$", r"_DONE$"),
    ("kill494.sh (sig)", "wdcaltoffset/killtable_20260830", r"^sig_.*\.out$", r"_DONE$|DONE"),
]


def git(*a):
    return subprocess.run(["git", "-C", SEC] + list(a), capture_output=True).stdout.decode("utf-8", "replace")


def main():
    tot = miss = 0
    for drv, d, frx, srx in SETS:
        names = [n for n in git("ls-tree", "--name-only", "HEAD", A + d + "/").split("\n") if n]
        names = [n for n in names if re.search(frx, n.rsplit("/", 1)[-1])]
        print("== %s  (%s: %d logs; sentinel /%s/)" % (drv, d, len(names), srx))
        for n in names:
            t = git("show", "HEAD:" + n).replace("\r", "")
            lines = [l for l in t.split("\n") if l.strip()]
            last = lines[-1] if lines else "(empty)"
            ok = bool(re.search(srx, last.strip()))
            tot += 1
            miss += not ok
            print("   %-5s %-42s last: %s" % ("ok" if ok else "NOSENT", n.rsplit("/", 1)[-1], last.strip()[:60]))
    print("RETRO: %d preserved per-mutant logs read, %d without their completion sentinel" % (tot, miss))
    print("RETRO_LOGS_DONE")


if __name__ == "__main__":
    main()
