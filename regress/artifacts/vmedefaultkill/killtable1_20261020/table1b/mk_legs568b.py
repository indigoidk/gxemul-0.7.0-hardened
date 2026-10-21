#!/usr/bin/env python3
"""mk_legs568b.py -- kill table 1b for #568 (vmedefaultkill): the three gap-closing legs, ONE exact find/replace each.

usage (WSL python3):  python3 -I -B mk_legs568b.py <dev_vme.fix568.c> <outdir>

Writes <outdir>/legs/src/<LEG>.dev_vme.c, <outdir>/legs/<LEG>.diff (unified, against fix568) and <outdir>/legs/MANIFEST.txt.
EVERY find text must occur EXACTLY ONCE in the fix, or NOTHING is written and the exit status is 5.  The fix's md5 is
checked; CR anywhere refuses; LF in, LF out (newline="" both ways).  Legs and predictions: table1b/PRETABLE1B.txt.
"""
import difflib
import hashlib
import io
import os
import sys

FIXMD5 = "4e3e7fc220062b429f7d9d6e140fec9e"

# (LEG, one-line edit, find, replace)
LEGS = [
    ("M_DROPIRQEN", "delete the label line `case VME2_IRQEN:' (0x6c reaches default: and FAULTs)",
     "\tcase VME2_IRQEN:\n", ""),
    ("M_T1CMPWRDROP", "T1CMP arm only: `if (writeflag == MEM_WRITE)' -> `if (writeflag == MEM_READ)' (the store is dropped)",
     "\tcase VME2_T1CMP:\n\t\tif (writeflag == MEM_WRITE)\n",
     "\tcase VME2_T1CMP:\n\t\tif (writeflag == MEM_READ)\n"),
    ("M_ADD90", "add `case 0x90:' immediately before `case VME2_SADDR2:' (0x90 joins the decline list)",
     "\tcase VME2_SADDR2:\n", "\tcase 0x90:\n\tcase VME2_SADDR2:\n"),
]


def rd(p):
    with io.open(p, "r", encoding="latin-1", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="latin-1", newline="") as f:
        f.write(s)


def md5s(s):
    return hashlib.md5(s.encode("latin-1")).hexdigest()


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("usage: mk_legs568b.py <dev_vme.fix568.c> <outdir>\n")
        return 2
    fix, out = rd(sys.argv[1]), sys.argv[2]
    bad, made = [], []
    if md5s(fix) != FIXMD5:
        bad.append("fix md5 %s != %s" % (md5s(fix), FIXMD5))
    if "\r" in fix:
        bad.append("CR in the fix")
    for name, what, find, repl in LEGS:
        n = fix.count(find)
        if n != 1:
            bad.append("%s: find text occurs %d times (want exactly 1): %r" % (name, n, find))
            continue
        res = fix.replace(find, repl, 1)
        if res == fix or "\r" in res:
            bad.append("%s: no-op or CR" % name)
            continue
        made.append((name, what, res))
    if bad:
        for b in bad:
            sys.stderr.write("REFUSED: %s\n" % b)
        sys.stderr.write("NOTHING WRITTEN\n")
        return 5
    os.makedirs(os.path.join(out, "legs", "src"), exist_ok=True)
    man = ["# mk_legs568b.py manifest: LEG md5 +lines -lines | edit   (input fix md5 %s)" % FIXMD5]
    for name, what, res in made:
        wr(os.path.join(out, "legs", "src", name + ".dev_vme.c"), res)
        dl = list(difflib.unified_diff(fix.splitlines(True), res.splitlines(True), fromfile="dev_vme.fix568.c",
                                       tofile="%s/dev_vme.c" % name, n=3))
        wr(os.path.join(out, "legs", name + ".diff"), "".join(dl))
        plus = sum(1 for l in dl if l.startswith("+") and not l.startswith("+++"))
        minus = sum(1 for l in dl if l.startswith("-") and not l.startswith("---"))
        man.append("%-15s %s +%d -%d | %s" % (name, md5s(res), plus, minus, what))
    wr(os.path.join(out, "legs", "MANIFEST.txt"), "\n".join(man) + "\n")
    print("\n".join(man))
    print("MK_LEGS568B_DONE %d legs" % len(made))
    return 0


if __name__ == "__main__":
    sys.exit(main())
