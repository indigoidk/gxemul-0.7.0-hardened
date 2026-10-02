#!/usr/bin/env python3
"""mutants_14b.py NAME SRC DST -- #529 table 14: the ONE new mutant repair 15 adds, for the entries-13/17 CHANNEL
check (repair14_20260916/FABLE_RULING_20260917.md B: "name the mutant each kills and the observable that differs ...
If a body-tested-partition mutant escapes -> L2, IN as the pair"; first-hand re-ruling, rerule_20260925/
fable5_rerule_529_20260925.md, item (2)).

  D_nodogclear   the CONTROL arm's DOG branch keeps its test and loses its repair: `idata &= ~CRIME_CONTROL_DOG_ENABLE;'
                 deleted.  An accepted DOG-only write (0x0200, ACCEPTS entries 13/17) then leaves a residue of 0x200 and
                 prints the arm's `CRIME_CONTROL: unimplemented' text, where the fix prints nothing.  It is the clause-(d)
                 shape on the arm's own tested bit -- keep the guard, null its repair -- and the only mutant that moves
                 the cell: the prelude re-forces CONTROL at every access, so the stored value is unobservable.

Exact-string edit on the BASELINE (the uncommitted #529 working set, dev_sgi_ip32.c 8c1d1545).  MUTANT-TEXT-NOT-FOUND is
a hard FAIL, so the find-text doubles as a presence pin.  No double backslash anywhere in this file.
"""
import io, sys

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
s = io.open(src, encoding="latin-1", newline="").read()   # newline="": no CRLF translation on Windows


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("MUTANT TEXT NOT FOUND (or not unique) for %s: %d occurrences" % (name, n))
    s = s.replace(old, new)


if name == "base":
    pass
elif name == "D_nodogclear":
    sub("\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n"
        "\t\t\t\tidata &= ~CRIME_CONTROL_DOG_ENABLE;\n"
        "\t\t\t}\n",
        "\t\t\tif (idata & CRIME_CONTROL_DOG_ENABLE) {\n"
        "\t\t\t}\n")
elif name == "list":
    print("base D_nodogclear")
    sys.exit(0)
else:
    sys.exit("unknown mutant %s" % name)

io.open(dst, "w", encoding="latin-1", newline="").write(s)
print("APPLIED %s" % name)
