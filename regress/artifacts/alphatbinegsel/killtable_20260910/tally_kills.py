#!/usr/bin/env python3
"""tally_kills.py -- THE DERIVER for "how many rows carry a measured kill".

    usage:  tally_kills.py [table-dir ...]        (default: t1 t2 t3)

Run this instead of quoting a number.  A count written into a durable record
names its deriver or carries its method inline; a transcribed count decays,
and the rounds that consult it are the rounds that change it.

TWO PARSING TRAPS THIS AVOIDS, both of which produced wrong answers first:

  1. DO NOT split the probe's "FAILING: ..." line on spaces.  Row names
     contain spaces ("tbia obs", "bnd a1z"), so splitting yields fragments --
     it reported ten "rows" for a table that has thirteen, including the
     nonsense tokens "bnd", "obs" and "hi".
  2. Parse the fixed-width NAME COLUMN instead.  Row lines are printed with
     "%-16s %-20s %-20s %-50s %s", so the name is exactly columns 0:16 of any
     line ending in "ok" or "FAIL".

A row with no kill is NOT automatically a defect: the four declared CONTROL
rows and the pre-existing positive control cannot fail under a guard edit by
construction.  What matters is that every ACCEPT row carries one.
"""
import glob, io, os, sys, collections

ACCEPT_PREFIX = "bnd "          # rows this round added to pin the guard

def tally(tdir):
    killed, allrows = collections.defaultdict(list), []
    for f in sorted(glob.glob(os.path.join(tdir, "probe_*.raw"))):
        leg = os.path.basename(f)[6:-4]
        if leg == "RESTORED":
            continue            # a re-run of BASE, not a mutant leg
        for line in io.open(f, encoding="latin-1"):
            stripped = line.rstrip("\n")
            if not stripped.endswith(("ok", "FAIL")):
                continue
            name = line[:16].strip()
            if not name:
                continue
            if leg == "BASE" and name not in allrows:
                allrows.append(name)
            if stripped.endswith("FAIL"):
                killed[name].append(leg)
    return allrows, killed

def main():
    dirs = sys.argv[1:] or ["t1", "t2", "t3"]
    rc = 0
    for tdir in dirs:
        if not os.path.isdir(tdir):
            print("(%s: absent, skipped)" % tdir)
            continue
        allrows, killed = tally(tdir)
        accepts = [r for r in allrows if r.startswith(ACCEPT_PREFIX)]
        unkilled_accepts = [r for r in accepts if r not in killed]
        print("=== %s: %d rows, %d carry a measured kill, %d accept rows ==="
              % (tdir, len(allrows), len(killed), len(accepts)))
        for n in allrows:
            legs = killed.get(n)
            tag = ", ".join(legs) if legs else "-- no kill"
            note = "" if legs or n.startswith(ACCEPT_PREFIX) else "   (declared control)"
            print("   %-10s %s%s" % (n, tag, note))
        if unkilled_accepts:
            print("   *** ACCEPT ROWS WITH NO KILL (vacuous, do not ship): %s"
                  % ", ".join(unkilled_accepts))
            rc = 1
        else:
            print("   every accept row carries a measured kill")
        print()
    return rc

if __name__ == "__main__":
    sys.exit(main())
