#!/usr/bin/env python3
"""mutants_15a.py NAME SRC DST -- #529 table 15a: the pass-2 adversarial candidate against repair 15, and its sibling.

  H_noresetclear   the dedicated adversarial grok seat's BREAK (repair15_pass2_20260926/grok_dedicated_r15p2.txt): the
                   CONTROL arm's HARD_RESET branch keeps its test and its CPU stop and loses its CLEAR,
                   `idata &= ~CRIME_CONTROL_HARD_RESET;'.  An accepted 0x800 write still stops every CPU and now also
                   leaves residue 0x800, so the arm prints its `CRIME_CONTROL: unimplemented' text.
  E_noendianclear  the third and last clear in that arm, found by reading it for the class: the unconditional
                   `idata &= ~CRIME_CONTROL_ENDIANESS;' deleted.  An accepted 0x0100 write (ACCEPTS carries two) then
                   leaves residue 0x100 and prints.

Both are the D_nodogclear shape (table 14: a clear nulled, visible only through the residue print).  Exact-string edits
on the BASELINE (the uncommitted #529 working set, dev_sgi_ip32.c 8c1d1545); MUTANT-TEXT-NOT-FOUND is a hard FAIL.
No double backslash anywhere in this file.
"""
import io, sys

name, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
s = io.open(src, encoding="latin-1", newline="").read()


def sub(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit("MUTANT TEXT NOT FOUND (or not unique) for %s: %d occurrences" % (name, n))
    s = s.replace(old, new)


if name == "base":
    pass
elif name == "H_noresetclear":
    sub("\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n"
        "\n"
        "\t\t\t\tidata &= ~CRIME_CONTROL_HARD_RESET;\n"
        "\t\t\t}\n",
        "\t\t\t\t\tcpu->machine->cpus[j]->running = 0;\n"
        "\n"
        "\t\t\t}\n")
elif name == "E_noendianclear":
    sub("\t\t\tidata &= ~CRIME_CONTROL_ENDIANESS;\n"
        "\n"
        "\t\t\tif (idata != 0)\n",
        "\t\t\tif (idata != 0)\n")
elif name == "list":
    print("base H_noresetclear E_noendianclear")
    sys.exit(0)
else:
    sys.exit("unknown mutant %s" % name)

io.open(dst, "w", encoding="latin-1", newline="").write(s)
print("APPLIED %s" % name)
