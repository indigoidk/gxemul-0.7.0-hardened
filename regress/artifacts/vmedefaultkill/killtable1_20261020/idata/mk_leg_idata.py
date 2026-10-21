#!/usr/bin/env python3
"""mk_leg_idata.py -- #568 "step 0": the ONE leg M_IDATA, by ONE exact find/replace on fix568.

usage (WSL python3):  python3 -I -B mk_leg_idata.py <dev_vme.fix568.c> <outdir>

In the population-2 announce arm ONLY, `if (writeflag == MEM_WRITE)' -> `if (idata)'.  That test occurs 6 times in the
fix, so the find text is anchored on the arm's own latch-set line.  The find must occur EXACTLY ONCE, the fix's md5
must match, no CR -- else NOTHING is written (exit 5).  Writes <outdir>/legs/src/M_IDATA.dev_vme.c and
<outdir>/legs/M_IDATA.diff (unified, against fix568).  LF in, LF out.
"""
import difflib
import hashlib
import io
import os
import sys

FIXMD5 = "4e3e7fc220062b429f7d9d6e140fec9e"
SET = "\t\t\td->warned_unimpl |= 1ULL << (relative_addr >> 2);\n"
FIND = SET + "\t\t\tif (writeflag == MEM_WRITE)\n"
REPL = SET + "\t\t\tif (idata)\n"


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="latin-1", newline="") as f:
        f.write(s)


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: mk_leg_idata.py <dev_vme.fix568.c> <outdir>\n")
        return 2
    fix, out = rd(sys.argv[1]), sys.argv[2]
    md5 = hashlib.md5(fix.encode("latin-1")).hexdigest()
    n = fix.count(FIND)
    bad = []
    if md5 != FIXMD5:
        bad.append("fix md5 %s != %s" % (md5, FIXMD5))
    if "\r" in fix:
        bad.append("CR in the fix")
    if n != 1:
        bad.append("find text occurs %d times (want exactly 1)" % n)
    if bad:
        for b in bad:
            sys.stderr.write("REFUSED: %s\n" % b)
        sys.stderr.write("NOTHING WRITTEN\n")
        return 5
    res = fix.replace(FIND, REPL, 1)
    os.makedirs(os.path.join(out, "legs", "src"), exist_ok=True)
    wr(os.path.join(out, "legs", "src", "M_IDATA.dev_vme.c"), res)
    dl = list(difflib.unified_diff(fix.splitlines(True), res.splitlines(True), fromfile="dev_vme.fix568.c",
                                   tofile="M_IDATA/dev_vme.c", n=3))
    wr(os.path.join(out, "legs", "M_IDATA.diff"), "".join(dl))
    plus = sum(1 for l in dl if l.startswith("+") and not l.startswith("+++"))
    minus = sum(1 for l in dl if l.startswith("-") and not l.startswith("---"))
    print("M_IDATA %s +%d -%d (input fix md5 %s; 'if (writeflag == MEM_WRITE)' occurs %d times in the fix)"
          % (hashlib.md5(res.encode("latin-1")).hexdigest(), plus, minus, md5,
             fix.count("if (writeflag == MEM_WRITE)")))
    print("MK_LEG_IDATA_DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
