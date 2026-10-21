#!/usr/bin/env python3
"""mk_leg_idatabit.py -- #568 table 2b: the ONE clause-(e) leg M_IDATABIT1, by ONE exact find/replace on fix568b.

usage (WSL python3):  python3 -I -B mk_leg_idatabit.py <dev_vme.fix568b.c> <outdir>

In the population-2 announce arm ONLY, `if (writeflag == MEM_WRITE)' -> `if (writeflag == MEM_WRITE && !(idata & 2))'.
That test occurs several times in the fix, so the find text is anchored on the arm's own latch-set line.  The find must
occur EXACTLY ONCE, the fix's md5 must match, no CR -- else NOTHING is written (exit 5).  Writes
<outdir>/legs/src/M_IDATABIT1.dev_vme.c and <outdir>/legs/M_IDATABIT1.diff (unified, against fix568b).  LF in, LF out.
The prediction was written first, in PRETABLE2B.txt beside this file.
"""
import difflib
import hashlib
import io
import os
import sys

FIXMD5 = "beb120eae1be112b682bd528f103191c"
SET = "\t\t\td->warned_unimpl |= 1ULL << (relative_addr >> 2);\n"
FIND = SET + "\t\t\tif (writeflag == MEM_WRITE)\n"
REPL = SET + "\t\t\tif (writeflag == MEM_WRITE && !(idata & 2))\n"


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="latin-1", newline="") as f:
        f.write(s)


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: mk_leg_idatabit.py <dev_vme.fix568b.c> <outdir>\n")
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
    wr(os.path.join(out, "legs", "src", "M_IDATABIT1.dev_vme.c"), res)
    dl = list(difflib.unified_diff(fix.splitlines(True), res.splitlines(True), fromfile="dev_vme.fix568b.c",
                                   tofile="M_IDATABIT1/dev_vme.c", n=3))
    wr(os.path.join(out, "legs", "M_IDATABIT1.diff"), "".join(dl))
    plus = sum(1 for l in dl if l.startswith("+") and not l.startswith("+++"))
    minus = sum(1 for l in dl if l.startswith("-") and not l.startswith("---"))
    print("M_IDATABIT1 %s +%d -%d (input fix md5 %s; 'if (writeflag == MEM_WRITE)' occurs %d times in the fix)"
          % (hashlib.md5(res.encode("latin-1")).hexdigest(), plus, minus, md5,
             fix.count("if (writeflag == MEM_WRITE)")))
    print("MK_LEG_IDATABIT_DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
