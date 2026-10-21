#!/usr/bin/env python3
"""mk_legs_t2d.py -- #568 table 2d: THREE legs from the repair-diff pass's Argon answer, each by ONE exact find/replace on
fix568b.

usage (WSL python3):  python3 -I -B mk_legs_t2d.py <dev_vme.fix568b.c> <outdir>

  M_ZEROSET    the latch set -> `if (writeflag != MEM_WRITE || idata != 0) d->warned_unimpl |= ...;'
  M_SETODATA   the latch set -> `if (!odata) d->warned_unimpl |= ...;'
  M_DFLTFFC    default:  `return 0;' -> `if (relative_addr <= 0xffc) return 0;'

The set's anchor is its own line (the latch TEST spells the field differently); the `default:' anchor is the end of
that arm's comment plus its `return 0;'.  Every find must occur EXACTLY ONCE, the fix's md5 must match, no CR -- else
NOTHING is written (exit 5).  Writes <outdir>/legs/src/<LEG>.dev_vme.c and <outdir>/legs/<LEG>.diff.  The predictions
were written first, in PRETABLE2D.txt beside this file.
"""
import difflib
import hashlib
import io
import os
import sys

FIXMD5 = "beb120eae1be112b682bd528f103191c"
SET = "\t\t\td->warned_unimpl |= 1ULL << (relative_addr >> 2);\n"
DFLT = "\t\t    at default verbosity).  */\n\t\treturn 0;\n"
LEGS = (
    ("M_ZEROSET", SET,
     "\t\t\tif (writeflag != MEM_WRITE || idata != 0) d->warned_unimpl |= 1ULL << (relative_addr >> 2);\n"),
    ("M_SETODATA", SET, "\t\t\tif (!odata) d->warned_unimpl |= 1ULL << (relative_addr >> 2);\n"),
    ("M_DFLTFFC", DFLT, "\t\t    at default verbosity).  */\n\t\tif (relative_addr <= 0xffc) return 0;\n"),
)


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="latin-1", newline="") as f:
        f.write(s)


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: mk_legs_t2d.py <dev_vme.fix568b.c> <outdir>\n")
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
    print("MK_LEGS_T2D_DONE (input fix md5 %s)" % md5)
    return 0


if __name__ == "__main__":
    sys.exit(main())
