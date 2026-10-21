#!/usr/bin/env python3
"""mk_legs_t2c.py -- #568 table 2c: THREE legs from the repair-diff pass's GLM answer, each by ONE exact find/replace on
fix568b.

usage (WSL python3):  python3 -I -B mk_legs_t2c.py <dev_vme.fix568b.c> <outdir>

  M_DFLTIDNZ   default:  `return 0;' -> `if (idata != 0) return 0;'
  M_DFLTIDZ    default:  `return 0;' -> `if (idata == 0) return 0;'
  M_DIRODATA   population-2 arm: `if (writeflag == MEM_WRITE)' -> `if (writeflag == MEM_WRITE && !(odata & 2))'

The `default:' anchor is the end of that arm's own comment plus its `return 0;' (`return 0;' alone is not unique); the
population-2 anchor is the arm's latch-set line.  Every find must occur EXACTLY ONCE, the fix's md5 must match, no CR --
else NOTHING is written (exit 5).  Writes <outdir>/legs/src/<LEG>.dev_vme.c and <outdir>/legs/<LEG>.diff.  The
predictions were written first, in PRETABLE2C.txt beside this file.
"""
import difflib
import hashlib
import io
import os
import sys

FIXMD5 = "beb120eae1be112b682bd528f103191c"
DFLT = "\t\t    at default verbosity).  */\n\t\treturn 0;\n"
SET = "\t\t\td->warned_unimpl |= 1ULL << (relative_addr >> 2);\n"
LEGS = (
    ("M_DFLTIDNZ", DFLT, "\t\t    at default verbosity).  */\n\t\tif (idata != 0) return 0;\n"),
    ("M_DFLTIDZ", DFLT, "\t\t    at default verbosity).  */\n\t\tif (idata == 0) return 0;\n"),
    ("M_DIRODATA", SET + "\t\t\tif (writeflag == MEM_WRITE)\n",
     SET + "\t\t\tif (writeflag == MEM_WRITE && !(odata & 2))\n"),
)


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="latin-1", newline="") as f:
        f.write(s)


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: mk_legs_t2c.py <dev_vme.fix568b.c> <outdir>\n")
        return 2
    fix, out = rd(sys.argv[1]), sys.argv[2]
    md5 = hashlib.md5(fix.encode("latin-1")).hexdigest()
    bad = []
    if md5 != FIXMD5:
        bad.append("fix md5 %s != %s" % (md5, FIXMD5))
    if "\r" in fix:
        bad.append("CR in the fix")
    for name, find, _ in LEGS:
        n = fix.count(find)
        if n != 1:
            bad.append("%s: find text occurs %d times (want exactly 1)" % (name, n))
    if bad:
        for b in bad:
            sys.stderr.write("REFUSED: %s\n" % b)
        sys.stderr.write("NOTHING WRITTEN\n")
        return 5
    os.makedirs(os.path.join(out, "legs", "src"), exist_ok=True)
    for name, find, repl in LEGS:
        res = fix.replace(find, repl, 1)
        wr(os.path.join(out, "legs", "src", "%s.dev_vme.c" % name), res)
        dl = list(difflib.unified_diff(fix.splitlines(True), res.splitlines(True), fromfile="dev_vme.fix568b.c",
                                       tofile="%s/dev_vme.c" % name, n=3))
        wr(os.path.join(out, "legs", "%s.diff" % name), "".join(dl))
        plus = sum(1 for l in dl if l.startswith("+") and not l.startswith("+++"))
        minus = sum(1 for l in dl if l.startswith("-") and not l.startswith("---"))
        print("%s %s +%d -%d" % (name, hashlib.md5(res.encode("latin-1")).hexdigest(), plus, minus))
    print("MK_LEGS_T2C_DONE (input fix md5 %s)" % md5)
    return 0


if __name__ == "__main__":
    sys.exit(main())
